from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.controllers.auth_controller import auth_controller
from backend.app.schemas.auth import (
    RegisterStudentRequest, VerifyOTPRequest, ResendOTPRequest,
    LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from backend.app.models.user import User

router = APIRouter(prefix="/auth", tags=["Xác thực & Tài khoản"])

@router.post("/register-student", summary="Đăng ký tài khoản sinh viên và gửi OTP qua Gmail")
def register_student(request: Request, data: RegisterStudentRequest, db: Session = Depends(get_db)):
    return auth_controller.register_student(request, data, db)

@router.post("/verify-otp", summary="Xác thực OTP kích hoạt tài khoản")
def verify_otp(request: Request, data: VerifyOTPRequest, db: Session = Depends(get_db)):
    return auth_controller.verify_otp(request, data, db)

@router.post("/resend-otp", summary="Gửi lại mã xác thực OTP qua Gmail")
def resend_otp(data: ResendOTPRequest, db: Session = Depends(get_db)):
    return auth_controller.resend_otp(data, db)

@router.post("/login", summary="Đăng nhập tài khoản bằng JWT Token")
def login(request: Request, data: LoginRequest, db: Session = Depends(get_db)):
    return auth_controller.login(request, data, db)

@router.post("/forgot-password", summary="Yêu cầu OTP đặt lại mật khẩu")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return auth_controller.forgot_password(data, db)

@router.post("/reset-password", summary="Đặt lại mật khẩu mới bằng OTP")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    return auth_controller.reset_password(data, db)

@router.get("/me", summary="Lấy thông tin tài khoản đang đăng nhập")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return auth_controller.get_me(current_user, db)
