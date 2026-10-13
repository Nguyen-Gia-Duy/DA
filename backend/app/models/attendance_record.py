from datetime import datetime
import enum
from sqlalchemy import String, Float, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class AttendanceStatus(str, enum.Enum):
    PRESENT = "PRESENT"
    LATE = "LATE"
    ABSENT = "ABSENT"
    EXCUSED = "EXCUSED"
    NEEDS_REVIEW = "NEEDS_REVIEW"

class VerificationMethod(str, enum.Enum):
    AI_FACE = "AI_FACE"
    MANUAL_LECTURER = "MANUAL_LECTURER"
    ADJUSTMENT = "ADJUSTMENT"

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    attendance_session_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("attendance_sessions.id", ondelete="CASCADE"), 
        nullable=False
    )
    student_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("students.id", ondelete="CASCADE"), 
        nullable=False
    )
    attendance_status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus), 
        default=AttendanceStatus.ABSENT, 
        nullable=False,
        index=True
    )
    check_in_time: Mapped[datetime | None] = mapped_column(DATETIME(fsp=6), nullable=True)
    device_info: Mapped[str | None] = mapped_column(String(255), nullable=True)
    verification_method: Mapped[VerificationMethod] = mapped_column(
        Enum(VerificationMethod), 
        default=VerificationMethod.AI_FACE, 
        nullable=False
    )
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
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

    __table_args__ = (
        UniqueConstraint("attendance_session_id", "student_id", name="uq_session_student"),
    )

    # Relationships
    attendance_session: Mapped["AttendanceSession"] = relationship("AttendanceSession", back_populates="attendance_records")
    student: Mapped["Student"] = relationship("Student", back_populates="attendance_records")
    adjustments: Mapped[list["AttendanceAdjustment"]] = relationship("AttendanceAdjustment", back_populates="attendance_record", cascade="all, delete-orphan")
