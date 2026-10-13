from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    department_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    department_name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    administrative_classes: Mapped[list["AdministrativeClass"]] = relationship("AdministrativeClass", back_populates="department")
    students: Mapped[list["Student"]] = relationship("Student", back_populates="department")
    lecturers: Mapped[list["Lecturer"]] = relationship("Lecturer", back_populates="department")
    subjects: Mapped[list["Subject"]] = relationship("Subject", back_populates="department")
