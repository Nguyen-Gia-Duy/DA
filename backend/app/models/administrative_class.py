from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class AdministrativeClass(Base):
    __tablename__ = "administrative_classes"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    class_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    class_name: Mapped[str] = mapped_column(String(150), nullable=False)
    department_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("departments.id", ondelete="RESTRICT"), 
        nullable=False
    )
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    department: Mapped["Department"] = relationship("Department", back_populates="administrative_classes")
    students: Mapped[list["Student"]] = relationship("Student", back_populates="administrative_class")
