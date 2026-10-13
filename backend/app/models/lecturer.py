from datetime import datetime
import enum
from sqlalchemy import String, Enum, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class LecturerStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ON_LEAVE = "ON_LEAVE"
    RETIRED = "RETIRED"

class Lecturer(Base):
    __tablename__ = "lecturers"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=False
    )
    lecturer_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    department_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("departments.id", ondelete="RESTRICT"), 
        nullable=False
    )
    academic_degree: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[LecturerStatus] = mapped_column(
        Enum(LecturerStatus), 
        default=LecturerStatus.ACTIVE, 
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
    user: Mapped["User"] = relationship("User", back_populates="lecturer")
    department: Mapped["Department"] = relationship("Department", back_populates="lecturers")
    class_sections: Mapped[list["ClassSection"]] = relationship("ClassSection", back_populates="lecturer")
    attendance_sessions: Mapped[list["AttendanceSession"]] = relationship("AttendanceSession", back_populates="lecturer")
