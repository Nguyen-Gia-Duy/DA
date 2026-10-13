from datetime import datetime, date
from sqlalchemy import String, Date, Boolean, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class Semester(Base):
    __tablename__ = "semesters"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    semester_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    semester_name: Mapped[str] = mapped_column(String(100), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    class_sections: Mapped[list["ClassSection"]] = relationship("ClassSection", back_populates="semester")
