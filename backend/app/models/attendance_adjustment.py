from datetime import datetime
from sqlalchemy import Text, Enum, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base
from backend.app.models.attendance_record import AttendanceStatus

class AttendanceAdjustment(Base):
    __tablename__ = "attendance_adjustments"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    attendance_record_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("attendance_records.id", ondelete="CASCADE"), 
        nullable=False
    )
    adjusted_by_user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("users.id", ondelete="RESTRICT"), 
        nullable=False
    )
    previous_status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus), 
        nullable=False
    )
    new_status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus), 
        nullable=False
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    attendance_record: Mapped["AttendanceRecord"] = relationship("AttendanceRecord", back_populates="adjustments")
    adjusted_by_user: Mapped["User"] = relationship("User")
