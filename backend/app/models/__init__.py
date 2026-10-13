from backend.app.core.database import Base

# Import all 21 original models + email_otp
from backend.app.models.role import Role
from backend.app.models.user import User, AccountStatus
from backend.app.models.user_role import UserRole
from backend.app.models.user_session import UserSession
from backend.app.models.department import Department
from backend.app.models.administrative_class import AdministrativeClass
from backend.app.models.student import Student, Gender, AcademicStatus
from backend.app.models.lecturer import Lecturer, LecturerStatus
from backend.app.models.subject import Subject
from backend.app.models.semester import Semester
from backend.app.models.classroom import Classroom, RoomType
from backend.app.models.class_section import ClassSection, SectionStatus
from backend.app.models.enrollment import Enrollment, EnrollmentStatus
from backend.app.models.schedule import Schedule, DayOfWeek
from backend.app.models.schedule_change_log import ScheduleChangeLog, ScheduleChangeType
from backend.app.models.face_profile import FaceProfile
from backend.app.models.attendance_session import AttendanceSession, SessionStatus
from backend.app.models.attendance_record import AttendanceRecord, AttendanceStatus, VerificationMethod
from backend.app.models.recognition_attempt import RecognitionAttempt, RecognitionAttemptStatus
from backend.app.models.attendance_adjustment import AttendanceAdjustment
from backend.app.models.audit_log import AuditLog
from backend.app.models.email_otp import EmailOTP, OTPPurpose

__all__ = [
    "Base",
    "Role",
    "User",
    "AccountStatus",
    "UserRole",
    "UserSession",
    "Department",
    "AdministrativeClass",
    "Student",
    "Gender",
    "AcademicStatus",
    "Lecturer",
    "LecturerStatus",
    "Subject",
    "Semester",
    "Classroom",
    "RoomType",
    "ClassSection",
    "SectionStatus",
    "Enrollment",
    "EnrollmentStatus",
    "Schedule",
    "DayOfWeek",
    "ScheduleChangeLog",
    "ScheduleChangeType",
    "FaceProfile",
    "AttendanceSession",
    "SessionStatus",
    "AttendanceRecord",
    "AttendanceStatus",
    "VerificationMethod",
    "RecognitionAttempt",
    "RecognitionAttemptStatus",
    "AttendanceAdjustment",
    "AuditLog",
    "EmailOTP",
    "OTPPurpose",
]
