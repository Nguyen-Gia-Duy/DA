from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.app.core.config import settings
from backend.app.core.security import (
    verify_password, get_password_hash, create_access_token,
    generate_otp_code, hash_otp, verify_otp_hash, generate_random_token
)
from backend.app.models.user import User, AccountStatus
from backend.app.models.role import Role
from backend.app.models.user_role import UserRole
from backend.app.models.user_session import UserSession
from backend.app.models.student import Student
from backend.app.models.lecturer import Lecturer
from backend.app.models.email_otp import EmailOTP, OTPPurpose
from backend.app.models.audit_log import AuditLog
from backend.app.services.email_service import email_service
from backend.app.schemas.auth import RegisterStudentRequest, LoginRequest, VerifyOTPRequest, ResetPasswordRequest

class AuthService:

    @staticmethod
    def register_student(db: Session, req: RegisterStudentRequest, ip_address: Optional[str] = None) -> Dict[str, Any]:
        # 1. Kiểm tra mã sinh viên có trong hệ thống không
        student = db.query(Student).filter(Student.student_code == req.student_code.strip()).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mã sinh viên '{req.student_code}' không tồn tại trong danh sách đào tạo nhà trường cấp."
            )

        # 2. Kiểm tra tài khoản người dùng liên kết
        existing_user = db.query(User).filter(User.id == student.user_id).first()
        if existing_user and existing_user.account_status == AccountStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mã sinh viên này đã được đăng ký và kích hoạt tài khoản."
            )

        # 3. Kiểm tra email đã có người dùng khác sử dụng chưa
        email_taken = db.query(User).filter(User.email == req.email, User.id != student.user_id).first()
        if email_taken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email này đã được sử dụng cho một tài khoản khác trong hệ thống."
            )

        # 4. Cập nhật hoặc tạo tài khoản sinh viên ở trạng thái PENDING
        if existing_user:
            existing_user.email = req.email
            existing_user.full_name = req.full_name
            existing_user.password_hash = get_password_hash(req.password)
            existing_user.account_status = AccountStatus.PENDING
            existing_user.phone = req.phone
            user = existing_user
        else:
            user = User(
                username=req.student_code.lower(),
                email=req.email,
                full_name=req.full_name,
                password_hash=get_password_hash(req.password),
                account_status=AccountStatus.PENDING,
                phone=req.phone
            )
            db.add(user)
            db.flush()
            student.user_id = user.id

            # Gán vai trò STUDENT
            student_role = db.query(Role).filter(Role.role_name == "STUDENT").first()
            if student_role:
                db.add(UserRole(user_id=user.id, role_id=student_role.id))

        # 5. Tạo OTP 6 chữ số và lưu hash
        otp_plain = generate_otp_code(6)
        otp_hash_val = hash_otp(otp_plain)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

        otp_record = EmailOTP(
            user_id=user.id,
            otp_hash=otp_hash_val,
            purpose=OTPPurpose.REGISTRATION,
            expires_at=expires_at,
            attempts=0
        )
        db.add(otp_record)

        # Ghi log kiểm toán
        db.add(AuditLog(
            user_id=user.id,
            action="STUDENT_REGISTRATION_REQUESTED",
            entity_type="users",
            entity_id=str(user.id),
            details={"student_code": req.student_code, "email": req.email},
            ip_address=ip_address
        ))

        db.commit()

        # 6. Gửi OTP qua Gmail
        email_sent = email_service.send_otp_email(
            to_email=req.email,
            recipient_name=req.full_name,
            otp_code=otp_plain,
            purpose_text="kích hoạt tài khoản sinh viên"
        )

        return {
            "success": True,
            "message": f"Mã xác thực OTP đã được gửi tới {req.email}. Hiệu lực {settings.OTP_EXPIRE_MINUTES} phút.",
            "email": req.email,
            "debug_otp": otp_plain if settings.DEBUG else None
        }

    @staticmethod
    def verify_registration_otp(db: Session, req: VerifyOTPRequest, ip_address: Optional[str] = None) -> Dict[str, Any]:
        user = db.query(User).filter(User.email == req.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản với email này.")

        # Lấy OTP đăng ký mới nhất chưa tiêu thụ
        otp_record = (
            db.query(EmailOTP)
            .filter(
                EmailOTP.user_id == user.id,
                EmailOTP.purpose == OTPPurpose.REGISTRATION,
                EmailOTP.consumed_at.is_(None)
            )
            .order_by(EmailOTP.id.desc())
            .first()
        )

        if not otp_record:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không có mã OTP hợp lệ hoặc mã đã được sử dụng.")

        # Kiểm tra số lần thử tối đa
        if otp_record.attempts >= settings.OTP_MAX_ATTEMPTS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã OTP đã vượt quá số lần nhập sai cho phép. Vui lòng gửi lại OTP.")

        # Kiểm tra hết hạn
        now_utc = datetime.now(timezone.utc)
        if otp_record.expires_at.replace(tzinfo=timezone.utc) < now_utc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã OTP đã hết hạn. Vui lòng yêu cầu mã mới.")

        # Kiểm tra tính khớp mã OTP
        if not verify_otp_hash(req.otp_code.strip(), otp_record.otp_hash):
            otp_record.attempts += 1
            db.commit()
            remaining = settings.OTP_MAX_ATTEMPTS - otp_record.attempts
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mã OTP không chính xác. Bạn còn {remaining} lần thử."
            )

        # Kích hoạt tài khoản
        otp_record.consumed_at = datetime.now(timezone.utc)
        user.account_status = AccountStatus.ACTIVE
        db.add(AuditLog(
            user_id=user.id,
            action="ACCOUNT_ACTIVATED_VIA_OTP",
            entity_type="users",
            entity_id=str(user.id),
            details={"email": user.email},
            ip_address=ip_address
        ))
        db.commit()

        # Gửi email thông báo kích hoạt thành công
        email_service.send_activation_success_email(user.email, user.full_name)

        return {
            "success": True,
            "message": "Kích hoạt tài khoản thành công! Bạn có thể đăng nhập ngay bây giờ."
        }

    @staticmethod
    def resend_otp(db: Session, email: str) -> Dict[str, Any]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản với email này.")

        otp_plain = generate_otp_code(6)
        otp_hash_val = hash_otp(otp_plain)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

        otp_record = EmailOTP(
            user_id=user.id,
            otp_hash=otp_hash_val,
            purpose=OTPPurpose.REGISTRATION if user.account_status == AccountStatus.PENDING else OTPPurpose.RESET_PASSWORD,
            expires_at=expires_at,
            attempts=0
        )
        db.add(otp_record)
        db.commit()

        email_service.send_otp_email(
            to_email=user.email,
            recipient_name=user.full_name,
            otp_code=otp_plain,
            purpose_text="xác thực tài khoản"
        )

        return {
            "success": True,
            "message": f"Mã OTP mới đã được gửi tới {email}."
        }

    @staticmethod
    def login(db: Session, req: LoginRequest, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Dict[str, Any]:
        user = db.query(User).filter(
            (User.username == req.username_or_email) | (User.email == req.username_or_email)
        ).first()

        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tài khoản hoặc mật khẩu không chính xác."
            )

        if user.account_status == AccountStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản của bạn chưa được xác thực email. Vui lòng nhập mã OTP để kích hoạt."
            )
        elif user.account_status != AccountStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Tài khoản không được phép truy cập (Trạng thái: {user.account_status.value})."
            )

        # Lấy danh sách Roles
        roles = [
            r[0] for r in (
                db.query(Role.role_name)
                .join(UserRole, UserRole.role_id == Role.id)
                .filter(UserRole.user_id == user.id)
                .all()
            )
        ]

        # Kiểm tra thông tin Student / Lecturer
        student = db.query(Student).filter(Student.user_id == user.id).first()
        lecturer = db.query(Lecturer).filter(Lecturer.user_id == user.id).first()

        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "roles": roles,
            "student_id": student.id if student else None,
            "lecturer_id": lecturer.id if lecturer else None,
        }
        access_token = create_access_token(token_data)

        # Lưu session vào user_sessions
        session_token = generate_random_token(48)
        user_session = UserSession(
            user_id=user.id,
            session_token=session_token,
            ip_address=ip_address,
            user_agent=user_agent,
            is_revoked=False,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        db.add(user_session)

        # Ghi log
        db.add(AuditLog(
            user_id=user.id,
            action="USER_LOGIN_SUCCESS",
            entity_type="users",
            entity_id=str(user.id),
            details={"roles": roles},
            ip_address=ip_address
        ))
        db.commit()

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "roles": roles,
            "student_id": student.id if student else None,
            "student_code": student.student_code if student else None,
            "lecturer_id": lecturer.id if lecturer else None,
            "lecturer_code": lecturer.lecturer_code if lecturer else None,
        }

    @staticmethod
    def forgot_password(db: Session, email: str) -> Dict[str, Any]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản với email này.")

        otp_plain = generate_otp_code(6)
        otp_record = EmailOTP(
            user_id=user.id,
            otp_hash=hash_otp(otp_plain),
            purpose=OTPPurpose.RESET_PASSWORD,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
            attempts=0
        )
        db.add(otp_record)
        db.commit()

        email_service.send_otp_email(
            to_email=user.email,
            recipient_name=user.full_name,
            otp_code=otp_plain,
            purpose_text="đặt lại mật khẩu"
        )
        return {"success": True, "message": f"Mã OTP đặt lại mật khẩu đã được gửi tới {email}."}

    @staticmethod
    def reset_password(db: Session, req: ResetPasswordRequest) -> Dict[str, Any]:
        user = db.query(User).filter(User.email == req.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản.")

        otp_record = (
            db.query(EmailOTP)
            .filter(
                EmailOTP.user_id == user.id,
                EmailOTP.purpose == OTPPurpose.RESET_PASSWORD,
                EmailOTP.consumed_at.is_(None)
            )
            .order_by(EmailOTP.id.desc())
            .first()
        )

        if not otp_record or not verify_otp_hash(req.otp_code.strip(), otp_record.otp_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã OTP không chính xác hoặc đã hết hạn.")

        user.password_hash = get_password_hash(req.new_password)
        otp_record.consumed_at = datetime.now(timezone.utc)
        db.commit()

        return {"success": True, "message": "Đặt lại mật khẩu thành công. Vui lòng đăng nhập với mật khẩu mới."}

auth_service = AuthService()
