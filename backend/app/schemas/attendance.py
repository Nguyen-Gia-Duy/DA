from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime, date

class FaceRegisterRequest(BaseModel):
    image_base64: str = Field(..., description="Ảnh khuôn mặt trực diện định dạng Base64 (data:image/jpeg;base64,...)")
    consent_biometric: bool = Field(..., description="Đồng ý thu thập và xử lý dữ liệu sinh trắc học")
    image_left_base64: Optional[str] = Field(None, description="Ảnh khuôn mặt quay trái (tùy chọn)")
    image_right_base64: Optional[str] = Field(None, description="Ảnh khuôn mặt quay phải (tùy chọn)")

class VerifyPoseRequest(BaseModel):
    image_base64: str = Field(..., description="Ảnh frame camera để phân tích tư thế mặt và chất lượng")

class VerifyPoseResponse(BaseModel):
    face_detected: bool
    pose_type: str # FRONTAL, LEFT, RIGHT, UNKNOWN
    yaw_angle: float
    roll_angle: float
    is_clear: bool
    is_bright: bool
    quality_score: float
    feedback: str
    id: int
    student_id: int
    student_code: str
    student_name: str
    model_name: str
    quality_score: float
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class AttendanceSessionCreate(BaseModel):
    class_section_id: int
    schedule_id: Optional[int] = None
    grace_period_minutes: int = 15

class AttendanceSessionResponse(BaseModel):
    id: int
    class_section_id: int
    section_code: str
    subject_name: str
    lecturer_name: str
    schedule_id: Optional[int] = None
    session_code: str
    session_date: date
    start_time: datetime
    end_time: Optional[datetime] = None
    session_status: str
    grace_period_minutes: int
    total_enrolled: int = 0
    present_count: int = 0
    late_count: int = 0
    absent_count: int = 0
    created_at: datetime
    class Config:
        from_attributes = True

class FaceCheckInRequest(BaseModel):
    session_code: str
    image_base64: str
    device_info: Optional[str] = "Web Camera"

class FaceCheckInResult(BaseModel):
    success: bool
    attendance_status: str # PRESENT, LATE, NEEDS_REVIEW
    student_id: Optional[int] = None
    student_code: Optional[str] = None
    student_name: Optional[str] = None
    similarity_score: Optional[float] = None
    message: str
    check_in_time: Optional[datetime] = None

class AttendanceRecordResponse(BaseModel):
    id: int
    attendance_session_id: int
    student_id: int
    student_code: str
    student_name: str
    class_code: Optional[str] = None
    attendance_status: str
    check_in_time: Optional[datetime] = None
    verification_method: str
    confidence_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class AttendanceAdjustmentCreate(BaseModel):
    attendance_record_id: int
    new_status: str # PRESENT, LATE, ABSENT, EXCUSED, NEEDS_REVIEW
    reason: str

class RecognitionAttemptResponse(BaseModel):
    id: int
    attendance_session_id: int
    session_code: Optional[str] = None
    student_id: Optional[int] = None
    student_name: Optional[str] = None
    attempt_status: str
    similarity_score: Optional[float] = None
    failure_reason: Optional[str] = None
    ip_address: Optional[str] = None
    attempt_time: datetime
    class Config:
        from_attributes = True
