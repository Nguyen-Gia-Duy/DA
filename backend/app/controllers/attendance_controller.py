from fastapi import Request
from sqlalchemy.orm import Session
from backend.app.services.attendance_service import attendance_service
from backend.app.services.face_service import face_service
from backend.app.schemas.attendance import (
    FaceRegisterRequest, AttendanceSessionCreate, FaceCheckInRequest, AttendanceAdjustmentCreate
)
from backend.app.models.user import User

class AttendanceController:

    # Biometric Face Registration
    @staticmethod
    def register_face(request: Request, current_user: User, data: FaceRegisterRequest, db: Session):
        if not current_user.student:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Chỉ tài khoản sinh viên mới được đăng ký khuôn mặt.")
        ip = request.client.host if request.client else None
        return face_service.register_face_profile(
            db=db,
            student_id=current_user.student.id,
            image_base64=data.image_base64,
            consent_biometric=data.consent_biometric,
            user_id=current_user.id,
            image_left_base64=data.image_left_base64,
            image_right_base64=data.image_right_base64,
            ip_address=ip
        )

    @staticmethod
    def verify_pose(image_base64: str):
        return face_service.analyze_live_pose(image_base64)

    @staticmethod
    def revoke_face(request: Request, current_user: User, db: Session):
        if not current_user.student:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Chỉ sinh viên mới có thể thu hồi dữ liệu khuôn mặt.")
        ip = request.client.host if request.client else None
        return face_service.revoke_face_profile(db, current_user.student.id, current_user.id, ip)

    @staticmethod
    def get_face_status(current_user: User, db: Session):
        if not current_user.student:
            return {"registered": False, "profile": None}
        return face_service.get_face_profile_status(db, current_user.student.id)

    # Attendance Session
    @staticmethod
    def open_session(current_user: User, data: AttendanceSessionCreate, db: Session):
        if not current_user.lecturer:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Chỉ tài khoản giảng viên mới được mở phiên điểm danh.")
        return attendance_service.open_session(db, current_user.lecturer.id, data)

    @staticmethod
    def close_session(current_user: User, session_id: int, db: Session):
        if not current_user.lecturer:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Chỉ giảng viên phụ trách mới được đóng phiên.")
        return attendance_service.close_session(db, current_user.lecturer.id, session_id)

    # Face Check-in
    @staticmethod
    def check_in(request: Request, current_user: User, data: FaceCheckInRequest, db: Session):
        if not current_user.student:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Chỉ tài khoản sinh viên mới được thực hiện điểm danh.")
        ip = request.client.host if request.client else None
        return attendance_service.check_in_by_face(
            db=db,
            session_code=data.session_code,
            student_id=current_user.student.id,
            image_base64=data.image_base64,
            device_info=data.device_info or "Web Camera",
            ip_address=ip
        )

    # Session Records & Adjustments
    @staticmethod
    def get_session_records(session_id: int, db: Session):
        return attendance_service.get_session_records(db, session_id)

    @staticmethod
    def adjust_attendance(current_user: User, data: AttendanceAdjustmentCreate, db: Session):
        return attendance_service.adjust_attendance(db, current_user.id, data)

attendance_controller = AttendanceController()
