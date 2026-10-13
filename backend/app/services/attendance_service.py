import secrets
from datetime import datetime, timezone, timedelta, date
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.app.core.config import settings
from backend.app.core.security import decrypt_face_embedding
from backend.app.models.attendance_session import AttendanceSession, SessionStatus
from backend.app.models.attendance_record import AttendanceRecord, AttendanceStatus, VerificationMethod
from backend.app.models.recognition_attempt import RecognitionAttempt, RecognitionAttemptStatus
from backend.app.models.attendance_adjustment import AttendanceAdjustment
from backend.app.models.class_section import ClassSection
from backend.app.models.enrollment import Enrollment, EnrollmentStatus
from backend.app.models.student import Student, AcademicStatus
from backend.app.models.lecturer import Lecturer
from backend.app.models.face_profile import FaceProfile
from backend.app.models.subject import Subject
from backend.app.models.user import User
from backend.app.models.audit_log import AuditLog
from backend.app.ai.face_detector import detector
from backend.app.ai.face_embedding import embedding_extractor
from backend.app.ai.face_recognition import face_recognizer
from backend.app.ai.image_quality import quality_analyzer
from backend.app.ai.face_security import security_guard
from backend.app.services.face_service import face_service
from backend.app.schemas.attendance import AttendanceSessionCreate, AttendanceAdjustmentCreate

class AttendanceService:

    @staticmethod
    def open_session(db: Session, lecturer_id: int, data: AttendanceSessionCreate) -> AttendanceSession:
        section = db.query(ClassSection).filter(ClassSection.id == data.class_section_id).first()
        if not section:
            raise HTTPException(status_code=404, detail="Lớp học phần không tồn tại.")

        if section.lecturer_id != lecturer_id:
            raise HTTPException(
                status_code=403,
                detail="Bạn không có quyền mở phiên điểm danh cho lớp học phần không được phân công."
            )

        # Kiểm tra phiên đang mở của lớp này
        active_session = db.query(AttendanceSession).filter(
            AttendanceSession.class_section_id == data.class_section_id,
            AttendanceSession.session_status == SessionStatus.OPEN
        ).first()
        if active_session:
            raise HTTPException(
                status_code=400,
                detail=f"Lớp học phần này đang có một phiên điểm danh mở (Mã phiên: {active_session.session_code}). Vui lòng đóng phiên cũ trước."
            )

        now = datetime.now()
        session_code = f"SES-{section.section_code}-{now.strftime('%Y%m%d%H%M')}-{secrets.token_hex(2).upper()}"

        session = AttendanceSession(
            class_section_id=data.class_section_id,
            schedule_id=data.schedule_id,
            lecturer_id=lecturer_id,
            session_code=session_code,
            session_date=now.date(),
            start_time=now,
            session_status=SessionStatus.OPEN,
            grace_period_minutes=data.grace_period_minutes
        )
        db.add(session)
        db.flush()

        # Tự động tạo bản ghi danh sách điểm danh ban đầu cho các sinh viên đã ghi danh ở trạng thái ABSENT
        enrollments = db.query(Enrollment).filter(
            Enrollment.class_section_id == data.class_section_id,
            Enrollment.enrollment_status == EnrollmentStatus.ENROLLED
        ).all()

        for en in enrollments:
            rec = AttendanceRecord(
                attendance_session_id=session.id,
                student_id=en.student_id,
                attendance_status=AttendanceStatus.ABSENT,
                verification_method=VerificationMethod.AI_FACE
            )
            db.add(rec)

        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def close_session(db: Session, lecturer_id: int, session_id: int) -> AttendanceSession:
        session = db.query(AttendanceSession).filter(AttendanceSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Phiên điểm danh không tồn tại.")

        if session.lecturer_id != lecturer_id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền đóng phiên điểm danh của giảng viên khác.")

        session.session_status = SessionStatus.CLOSED
        session.end_time = datetime.now()
        db.commit()
        db.refresh(session)
        return session

    @classmethod
    def check_in_by_face(
        cls, db: Session, session_code: str, student_id: int, image_base64: str,
        device_info: str = "Web Camera", ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        # 1. Tìm phiên điểm danh
        session = db.query(AttendanceSession).filter(AttendanceSession.session_code == session_code.strip()).first()
        if not session:
            raise HTTPException(status_code=404, detail="Không tìm thấy phiên điểm danh với mã cung cấp.")

        if session.session_status != SessionStatus.OPEN:
            raise HTTPException(
                status_code=400,
                detail=f"Phiên điểm danh đã kết thúc hoặc bị hủy (Trạng thái: {session.session_status.value})."
            )

        # 2. Kiểm tra sinh viên có trong lớp học phần không
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ sinh viên.")

        if student.academic_status == AcademicStatus.DROPPED_OUT:
            raise HTTPException(status_code=400, detail="Sinh viên đã thôi học, không thể điểm danh.")

        enrollment = db.query(Enrollment).filter(
            Enrollment.class_section_id == session.class_section_id,
            Enrollment.student_id == student_id,
            Enrollment.enrollment_status == EnrollmentStatus.ENROLLED
        ).first()
        if not enrollment:
            # Ghi nhận thất bại: Không thuộc lớp
            db.add(RecognitionAttempt(
                attendance_session_id=session.id,
                student_id=student.id,
                attempt_status=RecognitionAttemptStatus.FAILED_NOT_ENROLLED,
                failure_reason="Sinh viên không đăng ký lớp học phần này",
                ip_address=ip_address
            ))
            db.commit()
            raise HTTPException(status_code=403, detail="Bạn không đăng ký lớp học phần này, không thể điểm danh.")

        # 3. Kiểm tra đã điểm danh thành công trước đó chưa (Chống điểm danh trùng)
        record = db.query(AttendanceRecord).filter(
            AttendanceRecord.attendance_session_id == session.id,
            AttendanceRecord.student_id == student.id
        ).first()

        if record and record.attendance_status in [AttendanceStatus.PRESENT, AttendanceStatus.LATE]:
            raise HTTPException(
                status_code=400,
                detail=f"Bạn đã điểm danh thành công lúc {record.check_in_time.strftime('%H:%M:%S')} (Trạng thái: {record.attendance_status.value})."
            )

        # 4. Kiểm tra hồ sơ khuôn mặt của sinh viên
        face_profile = db.query(FaceProfile).filter(FaceProfile.student_id == student.id, FaceProfile.is_active == True).first()
        if not face_profile:
            raise HTTPException(
                status_code=400,
                detail="Bạn chưa đăng ký dữ liệu khuôn mặt. Vui lòng vào mục 'Đăng ký khuôn mặt' để cập nhật."
            )

        # 5. Xử lý ảnh chụp camera bằng OpenCV
        image = face_service.decode_base64_image(image_base64)
        detected_faces = detector.detect_faces(image)

        # Kiểm tra số lượng khuôn mặt
        face_check = security_guard.check_single_face(len(detected_faces))
        if not face_check["valid"]:
            status_enum = RecognitionAttemptStatus.FAILED_NO_FACE if len(detected_faces) == 0 else RecognitionAttemptStatus.FAILED_MULTIPLE_FACES
            db.add(RecognitionAttempt(
                attendance_session_id=session.id,
                student_id=student.id,
                attempt_status=status_enum,
                failure_reason=face_check["reason"],
                ip_address=ip_address
            ))
            db.commit()
            raise HTTPException(status_code=400, detail=face_check["reason"])

        target_face = detected_faces[0]
        bbox = target_face["bbox"]

        # Kiểm tra chất lượng ảnh
        quality = quality_analyzer.evaluate(image, bbox)
        if not quality["passed"]:
            db.add(RecognitionAttempt(
                attendance_session_id=session.id,
                student_id=student.id,
                attempt_status=RecognitionAttemptStatus.FAILED_LOW_CONFIDENCE,
                failure_reason=quality["error_message"],
                ip_address=ip_address
            ))
            db.commit()
            raise HTTPException(status_code=400, detail=f"Chất lượng ảnh không đạt: {quality['error_message']}")

        # Kiểm tra chống giả mạo
        face_crop = detector.crop_face(image, bbox)
        liveness = security_guard.check_frequency_liveness(face_crop)
        if not liveness["is_live"]:
            db.add(RecognitionAttempt(
                attendance_session_id=session.id,
                student_id=student.id,
                attempt_status=RecognitionAttemptStatus.FAILED_SPOOF_SUSPECTED,
                failure_reason=liveness["reason"],
                ip_address=ip_address
            ))
            db.commit()
            raise HTTPException(status_code=400, detail=f"Cảnh báo sinh trắc học: {liveness['reason']}")

        # 6. Trích xuất query embedding
        raw_face = target_face.get("raw_face")
        if raw_face is not None:
            query_embedding = embedding_extractor.extract_from_raw_face(raw_face)
        else:
            query_embedding = embedding_extractor.extract_deterministic_fallback(face_crop)

        # 7. Giải mã template sinh trắc học đã lưu an toàn
        stored_embedding = decrypt_face_embedding(face_profile.encrypted_template)

        # 8. Tính Cosine similarity
        match_result = face_recognizer.compare_templates(query_embedding, stored_embedding)
        similarity = match_result["similarity_score"]

        now = datetime.now()

        # 9. Đánh giá kết quả nhận diện
        if not match_result["is_match"]:
            db.add(RecognitionAttempt(
                attendance_session_id=session.id,
                student_id=student.id,
                attempt_status=RecognitionAttemptStatus.FAILED_LOW_CONFIDENCE,
                similarity_score=similarity,
                failure_reason=f"Độ tương đồng thấp ({similarity:.3f} < {match_result['threshold']})",
                ip_address=ip_address
            ))
            db.commit()
            raise HTTPException(
                status_code=400,
                detail=f"Nhận diện không khớp! Độ tương đồng {similarity:.2f} chưa đạt ngưỡng yêu cầu ({match_result['threshold']:.2f})."
            )

        # 10. Xác định trạng thái PRESENT hoặc LATE theo thời gian ân hạn (Grace Period)
        elapsed_minutes = (now - session.start_time).total_seconds() / 60.0
        new_status = AttendanceStatus.PRESENT if elapsed_minutes <= session.grace_period_minutes else AttendanceStatus.LATE

        if record:
            record.attendance_status = new_status
            record.check_in_time = now
            record.device_info = device_info
            record.verification_method = VerificationMethod.AI_FACE
            record.confidence_score = similarity
        else:
            record = AttendanceRecord(
                attendance_session_id=session.id,
                student_id=student.id,
                attendance_status=new_status,
                check_in_time=now,
                device_info=device_info,
                verification_method=VerificationMethod.AI_FACE,
                confidence_score=similarity
            )
            db.add(record)

        # Ghi nhận nỗ lực nhận diện thành công
        db.add(RecognitionAttempt(
            attendance_session_id=session.id,
            student_id=student.id,
            attempt_status=RecognitionAttemptStatus.SUCCESS,
            similarity_score=similarity,
            ip_address=ip_address
        ))

        db.commit()

        status_vi = "Có mặt đúng giờ" if new_status == AttendanceStatus.PRESENT else "Đi muộn"
        return {
            "success": True,
            "attendance_status": new_status.value,
            "student_id": student.id,
            "student_code": student.student_code,
            "similarity_score": similarity,
            "message": f"Điểm danh thành công: {status_vi}! (Độ tin cậy: {similarity*100:.1f}%)",
            "check_in_time": now
        }

    @staticmethod
    def adjust_attendance(db: Session, lecturer_user_id: int, data: AttendanceAdjustmentCreate) -> AttendanceRecord:
        record = db.query(AttendanceRecord).filter(AttendanceRecord.id == data.attendance_record_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Bản ghi điểm danh không tồn tại.")

        prev_status = record.attendance_status
        new_status_enum = AttendanceStatus(data.new_status)

        adjustment = AttendanceAdjustment(
            attendance_record_id=record.id,
            adjusted_by_user_id=lecturer_user_id,
            previous_status=prev_status,
            new_status=new_status_enum,
            reason=data.reason
        )
        db.add(adjustment)

        record.attendance_status = new_status_enum
        record.verification_method = VerificationMethod.ADJUSTMENT
        if not record.check_in_time and new_status_enum in [AttendanceStatus.PRESENT, AttendanceStatus.LATE]:
            record.check_in_time = datetime.now()

        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_session_records(db: Session, session_id: int) -> List[Dict[str, Any]]:
        records = (
            db.query(AttendanceRecord, Student, User)
            .join(Student, AttendanceRecord.student_id == Student.id)
            .join(User, Student.user_id == User.id)
            .filter(AttendanceRecord.attendance_session_id == session_id)
            .all()
        )
        results = []
        for rec, st, u in records:
            results.append({
                "id": rec.id,
                "attendance_session_id": rec.attendance_session_id,
                "student_id": st.id,
                "student_code": st.student_code,
                "student_name": u.full_name,
                "attendance_status": rec.attendance_status.value,
                "check_in_time": rec.check_in_time,
                "verification_method": rec.verification_method.value,
                "confidence_score": rec.confidence_score,
                "created_at": rec.created_at,
                "updated_at": rec.updated_at
            })
        return results

attendance_service = AttendanceService()
