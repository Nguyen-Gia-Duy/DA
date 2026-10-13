from datetime import datetime
import enum
from sqlalchemy import Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class EnrollmentStatus(str, enum.Enum):
    ENROLLED = "ENROLLED"
    DROPPED = "DROPPED"
    WITHDRAWN = "WITHDRAWN"

class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("students.id", ondelete="CASCADE"), 
        nullable=False
    )
    class_section_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("class_sections.id", ondelete="CASCADE"), 
        nullable=False
    )
    enrollment_status: Mapped[EnrollmentStatus] = mapped_column(
        Enum(EnrollmentStatus), 
        default=EnrollmentStatus.ENROLLED, 
        nullable=False
    )
    registered_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("student_id", "class_section_id", name="uq_student_section"),
    )

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="enrollments")
    class_section: Mapped["ClassSection"] = relationship("ClassSection", back_populates="enrollments")
