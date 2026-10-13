from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    full_name: str
    email: str
    roles: List[str]
    student_id: Optional[int] = None
    student_code: Optional[str] = None
    lecturer_id: Optional[int] = None
    lecturer_code: Optional[str] = None

class RegisterStudentRequest(BaseModel):
    student_code: str = Field(..., description="Mã sinh viên do nhà trường cấp")
    full_name: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = None

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp_code: str = Field(..., min_length=6, max_length=6)

class ResendOTPRequest(BaseModel):
    email: EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp_code: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=6)

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)

class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    account_status: str
    roles: List[str]
    created_at: datetime
