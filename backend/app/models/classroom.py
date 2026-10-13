from datetime import datetime
import enum
from sqlalchemy import String, Integer, Boolean, Enum, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class RoomType(str, enum.Enum):
    LECTURE_HALL = "LECTURE_HALL"
    LAB = "LAB"
    NORMAL = "NORMAL"

class Classroom(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    room_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    building: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    room_type: Mapped[RoomType] = mapped_column(
        Enum(RoomType), 
        default=RoomType.NORMAL, 
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="classroom")
