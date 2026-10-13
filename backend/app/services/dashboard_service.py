from datetime import datetime, date, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.models.student import Student
from backend.app.models.lecturer import Lecturer
from backend.app.models.department import Department
from backend.app.models.class_section import ClassSection
from backend.app.models.subject import Subject
from backend.app.models.attendance_session import AttendanceSession, SessionStatus
from backend.app.models.attendance_record import AttendanceRecord, AttendanceStatus
from backend.app.models.recognition_attempt import RecognitionAttempt, RecognitionAttemptStatus
from backend.app.models.audit_log import AuditLog
from backend.app.models.enrollment import Enrollment, EnrollmentStatus
from backend.app.models.schedule import Schedule
from backend.app.models.user import User

class DashboardService:

    @staticmethod
    def get_admin_dashboard(db: Session) -> Dict[str, Any]:
        total_students = db.query(func.count(Student.id)).scalar() or 0
        total_lecturers = db.query(func.count(Lecturer.id)).scalar() or 0
        total_departments = db.query(func.count(Department.id)).scalar() or 0
        total_class_sections = db.query(func.count(ClassSection.id)).scalar() or 0
        total_subjects = db.query(func.count(Subject.id)).scalar() or 0
        total_sessions = db.query(func.count(AttendanceSession.id)).scalar() or 0

        # Thống kê điểm danh
        present_count = db.query(func.count(AttendanceRecord.id)).filter(AttendanceRecord.attendance_status == AttendanceStatus.PRESENT).scalar() or 0
        late_count = db.query(func.count(AttendanceRecord.id)).filter(AttendanceRecord.attendance_status == AttendanceStatus.LATE).scalar() or 0
        absent_count = db.query(func.count(AttendanceRecord.id)).filter(AttendanceRecord.attendance_status == AttendanceStatus.ABSENT).scalar() or 0
        total_records = present_count + late_count + absent_count
        attendance_rate = round(((present_count + late_count) / total_records * 100.0), 1) if total_records > 0 else 0.0

        # Thất bại nhận diện
        failed_attempts = db.query(func.count(RecognitionAttempt.id)).filter(
            RecognitionAttempt.attempt_status != RecognitionAttemptStatus.SUCCESS
        ).scalar() or 0

        today = date.today()
        today_sessions = db.query(func.count(AttendanceSession.id)).filter(AttendanceSession.session_date == today).scalar() or 0

        # Biểu đồ xu hướng điểm danh 7 ngày qua
        trends = []
        for i in range(6, -1, -1):
            target_date = today - timedelta(days=i)
            day_str = target_date.strftime("%d/%m")
            p_day = (
                db.query(func.count(AttendanceRecord.id))
                .join(AttendanceSession, AttendanceRecord.attendance_session_id == AttendanceSession.id)
                .filter(AttendanceSession.session_date == target_date, AttendanceRecord.attendance_status == AttendanceStatus.PRESENT)
                .scalar() or 0
            )
            l_day = (
                db.query(func.count(AttendanceRecord.id))
                .join(AttendanceSession, AttendanceRecord.attendance_session_id == AttendanceSession.id)
                .filter(AttendanceSession.session_date == target_date, AttendanceRecord.attendance_status == AttendanceStatus.LATE)
                .scalar() or 0
            )
            a_day = (
                db.query(func.count(AttendanceRecord.id))
                .join(AttendanceSession, AttendanceRecord.attendance_session_id == AttendanceSession.id)
                .filter(AttendanceSession.session_date == target_date, AttendanceRecord.attendance_status == AttendanceStatus.ABSENT)
                .scalar() or 0
            )
            trends.append({
                "date": day_str,
                "present": p_day,
                "late": l_day,
                "absent": a_day
            })

        # Hoạt động gần đây
        recent_logs = (
            db.query(AuditLog, User.full_name)
            .outerjoin(User, AuditLog.user_id == User.id)
            .order_by(AuditLog.id.desc())
            .limit(10)
            .all()
        )
        activities = []
        for log, full_name in recent_logs:
            activities.append({
                "id": log.id,
                "action": log.action,
                "user_name": full_name or "Hệ thống",
                "entity_type": log.entity_type,
                "created_at": log.created_at.strftime("%H:%M %d/%m/%Y")
            })

        return {
            "total_students": total_students,
            "total_lecturers": total_lecturers,
            "total_departments": total_departments,
            "total_class_sections": total_class_sections,
            "total_subjects": total_subjects,
            "total_attendance_sessions": total_sessions,
            "overall_attendance_rate": attendance_rate,
            "today_sessions_count": today_sessions,
            "late_count": late_count,
            "absent_count": absent_count,
            "failed_attempts_count": failed_attempts,
            "attendance_trends": trends,
            "recent_activities": activities
        }

    @staticmethod
    def get_lecturer_dashboard(db: Session, lecturer_id: int) -> Dict[str, Any]:
        sections_count = db.query(func.count(ClassSection.id)).filter(ClassSection.lecturer_id == lecturer_id).scalar() or 0
        total_students = (
            db.query(func.count(Enrollment.id))
            .join(ClassSection, Enrollment.class_section_id == ClassSection.id)
            .filter(ClassSection.lecturer_id == lecturer_id, Enrollment.enrollment_status == EnrollmentStatus.ENROLLED)
            .scalar() or 0
        )
        active_sessions = db.query(func.count(AttendanceSession.id)).filter(
            AttendanceSession.lecturer_id == lecturer_id,
            AttendanceSession.session_status == SessionStatus.OPEN
        ).scalar() or 0

        # Tỷ lệ chuyên cần
        present = (
            db.query(func.count(AttendanceRecord.id))
            .join(AttendanceSession, AttendanceRecord.attendance_session_id == AttendanceSession.id)
            .filter(AttendanceSession.lecturer_id == lecturer_id, AttendanceRecord.attendance_status.in_([AttendanceStatus.PRESENT, AttendanceStatus.LATE]))
            .scalar() or 0
        )
        total_recs = (
            db.query(func.count(AttendanceRecord.id))
            .join(AttendanceSession, AttendanceRecord.attendance_session_id == AttendanceSession.id)
            .filter(AttendanceSession.lecturer_id == lecturer_id)
            .scalar() or 0
        )
        rate = round((present / total_recs * 100.0), 1) if total_recs > 0 else 0.0

        # Các phiên gần đây
        recent_sessions = (
            db.query(AttendanceSession, ClassSection.section_code, Subject.subject_name)
            .join(ClassSection, AttendanceSession.class_section_id == ClassSection.id)
            .join(Subject, ClassSection.subject_id == Subject.id)
            .filter(AttendanceSession.lecturer_id == lecturer_id)
            .order_by(AttendanceSession.id.desc())
            .limit(5)
            .all()
        )
        sessions_list = []
        for s, sec_code, sub_name in recent_sessions:
            sessions_list.append({
                "id": s.id,
                "session_code": s.session_code,
                "section_code": sec_code,
                "subject_name": sub_name,
                "session_date": s.session_date.strftime("%d/%m/%Y"),
                "status": s.session_status.value
            })

        return {
            "assigned_sections_count": sections_count,
            "total_students": total_students,
            "active_sessions_count": active_sessions,
            "average_attendance_rate": rate,
            "upcoming_schedules": [],
            "recent_sessions": sessions_list
        }

    @staticmethod
    def get_student_dashboard(db: Session, student_id: int) -> Dict[str, Any]:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return {}

        enrolled_count = db.query(func.count(Enrollment.id)).filter(
            Enrollment.student_id == student_id,
            Enrollment.enrollment_status == EnrollmentStatus.ENROLLED
        ).scalar() or 0

        attended_count = db.query(func.count(AttendanceRecord.id)).filter(
            AttendanceRecord.student_id == student_id,
            AttendanceRecord.attendance_status.in_([AttendanceStatus.PRESENT, AttendanceStatus.LATE])
        ).scalar() or 0

        total_sessions = db.query(func.count(AttendanceRecord.id)).filter(
            AttendanceRecord.student_id == student_id
        ).scalar() or 0

        rate = round((attended_count / total_sessions * 100.0), 1) if total_sessions > 0 else 100.0

        # Lịch sử điểm danh 10 buổi gần nhất
        recent_records = (
            db.query(AttendanceRecord, AttendanceSession, ClassSection.section_code, Subject.subject_name)
            .join(AttendanceSession, AttendanceRecord.attendance_session_id == AttendanceSession.id)
            .join(ClassSection, AttendanceSession.class_section_id == ClassSection.id)
            .join(Subject, ClassSection.subject_id == Subject.id)
            .filter(AttendanceRecord.student_id == student_id)
            .order_by(AttendanceRecord.id.desc())
            .limit(10)
            .all()
        )
        history = []
        for rec, s, sec_code, sub_name in recent_records:
            history.append({
                "id": rec.id,
                "section_code": sec_code,
                "subject_name": sub_name,
                "session_date": s.session_date.strftime("%d/%m/%Y"),
                "check_in_time": rec.check_in_time.strftime("%H:%M:%S") if rec.check_in_time else "Chưa ghi nhận",
                "status": rec.attendance_status.value,
                "confidence_score": rec.confidence_score
            })

        return {
            "student_id": student.id,
            "student_code": student.student_code,
            "student_name": student.user.full_name,
            "class_name": student.administrative_class.class_name,
            "has_face_profile": bool(student.face_profile and student.face_profile.is_active),
            "enrolled_courses_count": enrolled_count,
            "total_attended_sessions": attended_count,
            "attendance_rate": rate,
            "today_classes": [],
            "recent_attendance_history": history
        }

dashboard_service = DashboardService()
