from fastapi import Request
from sqlalchemy.orm import Session
from backend.app.schemas.auth import (
    RegisterStudentRequest, VerifyOTPRequest, ResendOTPRequest,
    LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from backend.app.services.auth_service import auth_service
from backend.app.models.user import User

class AuthController:

    @staticmethod
    def register_student(request: Request, data: RegisterStudentRequest, db: Session):
        ip = request.client.host if request.client else None
        return auth_service.register_student(db, data, ip_address=ip)

    @staticmethod
    def verify_otp(request: Request, data: VerifyOTPRequest, db: Session):
        ip = request.client.host if request.client else None
        return auth_service.verify_registration_otp(db, data, ip_address=ip)

    @staticmethod
    def resend_otp(data: ResendOTPRequest, db: Session):
        return auth_service.resend_otp(db, data.email)

    @staticmethod
    def login(request: Request, data: LoginRequest, db: Session):
        ip = request.client.host if request.client else None
        ua = request.headers.get("user-agent")
        return auth_service.login(db, data, ip_address=ip, user_agent=ua)

    @staticmethod
    def forgot_password(data: ForgotPasswordRequest, db: Session):
        return auth_service.forgot_password(db, data.email)

    @staticmethod
    def reset_password(data: ResetPasswordRequest, db: Session):
        return auth_service.reset_password(db, data)

    @staticmethod
    def get_me(current_user: User, db: Session):
        roles = [ur.role.role_name for ur in current_user.user_roles]
        student_id = current_user.student.id if current_user.student else None
        lecturer_id = current_user.lecturer.id if current_user.lecturer else None
        return {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "phone": current_user.phone,
            "avatar_url": current_user.avatar_url,
            "account_status": current_user.account_status.value,
            "roles": roles,
            "student_id": student_id,
            "lecturer_id": lecturer_id,
            "created_at": current_user.created_at
        }

auth_controller = AuthController()
