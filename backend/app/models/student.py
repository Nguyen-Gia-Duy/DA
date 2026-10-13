from datetime import datetime, date
import enum
from sqlalchemy import String, Date, Enum, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class AcademicStatus(str, enum.Enum):
    STUDYING = "STUDYING"
    SUSPENDED = "SUSPENDED"
    DROPPED_OUT = "DROPPED_OUT"
    GRADUATED = "GRADUATED"

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=False
    )
    student_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    administrative_class_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("administrative_classes.id", ondelete="RESTRICT"), 
        nullable=False
    )
    department_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("departments.id", ondelete="RESTRICT"), 
        nullable=False
    )
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), default=Gender.MALE, nullable=False)
    academic_status: Mapped[AcademicStatus] = mapped_column(
        Enum(AcademicStatus), 
        default=AcademicStatus.STUDYING, 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        onupdate=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="student")
    administrative_class: Mapped["AdministrativeClass"] = relationship("AdministrativeClass", back_populates="students")
    department: Mapped["Department"] = relationship("Department", back_populates="students")
    enrollments: Mapped[list["Enrollment"]] = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    face_profile: Mapped["FaceProfile | None"] = relationship("FaceProfile", back_populates="student", uselist=False, cascade="all, delete-orphan")
    attendance_records: Mapped[list["AttendanceRecord"]] = relationship("AttendanceRecord", back_populates="student")
    recognition_attempts: Mapped[list["RecognitionAttempt"]] = relationship("RecognitionAttempt", back_populates="student")
