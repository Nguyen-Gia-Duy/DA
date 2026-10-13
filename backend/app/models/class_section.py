from datetime import datetime
import enum
from sqlalchemy import String, Integer, Enum, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class SectionStatus(str, enum.Enum):
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class ClassSection(Base):
    __tablename__ = "class_sections"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    section_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    subject_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("subjects.id", ondelete="RESTRICT"), 
        nullable=False
    )
    semester_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("semesters.id", ondelete="RESTRICT"), 
        nullable=False
    )
    lecturer_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("lecturers.id", ondelete="RESTRICT"), 
        nullable=False
    )
    max_capacity: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    current_enrollment: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[SectionStatus] = mapped_column(
        Enum(SectionStatus), 
        default=SectionStatus.ACTIVE, 
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
    subject: Mapped["Subject"] = relationship("Subject", back_populates="class_sections")
    semester: Mapped["Semester"] = relationship("Semester", back_populates="class_sections")
    lecturer: Mapped["Lecturer"] = relationship("Lecturer", back_populates="class_sections")
    enrollments: Mapped[list["Enrollment"]] = relationship("Enrollment", back_populates="class_section", cascade="all, delete-orphan")
    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="class_section", cascade="all, delete-orphan")
    attendance_sessions: Mapped[list["AttendanceSession"]] = relationship("AttendanceSession", back_populates="class_section", cascade="all, delete-orphan")
