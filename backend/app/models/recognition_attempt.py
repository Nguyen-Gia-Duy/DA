from datetime import datetime
import enum
from sqlalchemy import String, Float, Enum, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class RecognitionAttemptStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED_NO_FACE = "FAILED_NO_FACE"
    FAILED_MULTIPLE_FACES = "FAILED_MULTIPLE_FACES"
    FAILED_LOW_CONFIDENCE = "FAILED_LOW_CONFIDENCE"
    FAILED_SPOOF_SUSPECTED = "FAILED_SPOOF_SUSPECTED"
    FAILED_NOT_ENROLLED = "FAILED_NOT_ENROLLED"

class RecognitionAttempt(Base):
    __tablename__ = "recognition_attempts"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    attendance_session_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("attendance_sessions.id", ondelete="CASCADE"), 
        nullable=False
    )
    student_id: Mapped[int | None] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("students.id", ondelete="SET NULL"), 
        nullable=True
    )
    attempt_status: Mapped[RecognitionAttemptStatus] = mapped_column(
        Enum(RecognitionAttemptStatus), 
        nullable=False
    )
    similarity_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    attempt_time: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    attendance_session: Mapped["AttendanceSession"] = relationship("AttendanceSession", back_populates="recognition_attempts")
    student: Mapped["Student | None"] = relationship("Student", back_populates="recognition_attempts")
