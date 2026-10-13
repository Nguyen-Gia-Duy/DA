from backend.app.schemas.auth import (
    LoginRequest, TokenResponse, RegisterStudentRequest, VerifyOTPRequest,
    ResendOTPRequest, ForgotPasswordRequest, ResetPasswordRequest, ChangePasswordRequest, UserProfileResponse
)
from backend.app.schemas.academic import (
    DepartmentCreate, DepartmentResponse,
    AdministrativeClassCreate, AdministrativeClassResponse,
    StudentCreate, StudentResponse,
    LecturerCreate, LecturerResponse,
    SubjectCreate, SubjectResponse,
    SemesterCreate, SemesterResponse,
    ClassroomCreate, ClassroomResponse,
    ClassSectionCreate, ClassSectionResponse,
    EnrollmentCreate, EnrollmentResponse,
    ScheduleCreate, ScheduleResponse,
    ScheduleChangeLogCreate, ScheduleChangeLogResponse
)
from backend.app.schemas.attendance import (
    FaceRegisterRequest, FaceProfileResponse,
    AttendanceSessionCreate, AttendanceSessionResponse,
    FaceCheckInRequest, FaceCheckInResult,
    AttendanceRecordResponse, AttendanceAdjustmentCreate,
    RecognitionAttemptResponse
)
from backend.app.schemas.dashboard import (
    AdminDashboardStats, LecturerDashboardStats, StudentDashboardStats
)

__all__ = [
    "LoginRequest", "TokenResponse", "RegisterStudentRequest", "VerifyOTPRequest",
    "ResendOTPRequest", "ForgotPasswordRequest", "ResetPasswordRequest", "ChangePasswordRequest", "UserProfileResponse",
    "DepartmentCreate", "DepartmentResponse",
    "AdministrativeClassCreate", "AdministrativeClassResponse",
    "StudentCreate", "StudentResponse",
    "LecturerCreate", "LecturerResponse",
    "SubjectCreate", "SubjectResponse",
    "SemesterCreate", "SemesterResponse",
    "ClassroomCreate", "ClassroomResponse",
    "ClassSectionCreate", "ClassSectionResponse",
    "EnrollmentCreate", "EnrollmentResponse",
    "ScheduleCreate", "ScheduleResponse",
    "ScheduleChangeLogCreate", "ScheduleChangeLogResponse",
    "FaceRegisterRequest", "FaceProfileResponse",
    "AttendanceSessionCreate", "AttendanceSessionResponse",
    "FaceCheckInRequest", "FaceCheckInResult",
    "AttendanceRecordResponse", "AttendanceAdjustmentCreate",
    "RecognitionAttemptResponse",
    "AdminDashboardStats", "LecturerDashboardStats", "StudentDashboardStats"
]
