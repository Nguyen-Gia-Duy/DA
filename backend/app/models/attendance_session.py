from datetime import datetime, date
import enum
from sqlalchemy import String, Date, Integer, Enum, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class SessionStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    class_section_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("class_sections.id", ondelete="CASCADE"), 
        nullable=False
    )
    schedule_id: Mapped[int | None] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("schedules.id", ondelete="SET NULL"), 
        nullable=True
    )
    lecturer_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("lecturers.id", ondelete="RESTRICT"), 
        nullable=False
    )
    session_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    session_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    end_time: Mapped[datetime | None] = mapped_column(DATETIME(fsp=6), nullable=True)
    session_status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus), 
        default=SessionStatus.OPEN, 
        nullable=False,
        index=True
    )
    grace_period_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    class_section: Mapped["ClassSection"] = relationship("ClassSection", back_populates="attendance_sessions")
    schedule: Mapped["Schedule | None"] = relationship("Schedule", back_populates="attendance_sessions")
    lecturer: Mapped["Lecturer"] = relationship("Lecturer", back_populates="attendance_sessions")
    attendance_records: Mapped[list["AttendanceRecord"]] = relationship("AttendanceRecord", back_populates="attendance_session", cascade="all, delete-orphan")
    recognition_attempts: Mapped[list["RecognitionAttempt"]] = relationship("RecognitionAttempt", back_populates="attendance_session", cascade="all, delete-orphan")
