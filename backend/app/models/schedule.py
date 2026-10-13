from datetime import datetime, time, date
import enum
from sqlalchemy import Time, Date, Enum, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class DayOfWeek(str, enum.Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    class_section_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("class_sections.id", ondelete="CASCADE"), 
        nullable=False
    )
    classroom_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("classrooms.id", ondelete="RESTRICT"), 
        nullable=False
    )
    day_of_week: Mapped[DayOfWeek] = mapped_column(Enum(DayOfWeek), nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    class_section: Mapped["ClassSection"] = relationship("ClassSection", back_populates="schedules")
    classroom: Mapped["Classroom"] = relationship("Classroom", back_populates="schedules")
    change_logs: Mapped[list["ScheduleChangeLog"]] = relationship("ScheduleChangeLog", back_populates="schedule", cascade="all, delete-orphan")
    attendance_sessions: Mapped[list["AttendanceSession"]] = relationship("AttendanceSession", back_populates="schedule")
