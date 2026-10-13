from datetime import datetime
from sqlalchemy import String, Integer, Text, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    subject_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    subject_name: Mapped[str] = mapped_column(String(150), nullable=False)
    credits: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    department_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("departments.id", ondelete="RESTRICT"), 
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    department: Mapped["Department"] = relationship("Department", back_populates="subjects")
    class_sections: Mapped[list["ClassSection"]] = relationship("ClassSection", back_populates="subject")
