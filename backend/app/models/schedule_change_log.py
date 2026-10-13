from datetime import datetime
import enum
from typing import Any
from sqlalchemy import String, Enum, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class ScheduleChangeType(str, enum.Enum):
    CLASSROOM_CHANGED = "CLASSROOM_CHANGED"
    TIME_CHANGED = "TIME_CHANGED"
    MAKEUP_CLASS = "MAKEUP_CLASS"
    CANCELLED = "CANCELLED"

class ScheduleChangeLog(Base):
    __tablename__ = "schedule_change_logs"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    schedule_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("schedules.id", ondelete="CASCADE"), 
        nullable=False
    )
    changed_by_user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("users.id", ondelete="RESTRICT"), 
        nullable=False
    )
    change_type: Mapped[ScheduleChangeType] = mapped_column(
        Enum(ScheduleChangeType), 
        nullable=False
    )
    old_values: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    new_values: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="change_logs")
    changed_by_user: Mapped["User"] = relationship("User")
