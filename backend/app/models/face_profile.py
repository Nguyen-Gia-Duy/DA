from datetime import datetime
from sqlalchemy import String, Float, Boolean, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, MEDIUMBLOB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class FaceProfile(Base):
    __tablename__ = "face_profiles"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("students.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=False
    )
    encrypted_template: Mapped[bytes] = mapped_column(MEDIUMBLOB, nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), default="insightface/buffalo_l", nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), default="1.0", nullable=False)
    encryption_key_version: Mapped[str] = mapped_column(String(50), default="v1", nullable=False)
    consent_version: Mapped[str] = mapped_column(String(50), default="gdpr_biometric_v1", nullable=False)
    quality_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
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
    student: Mapped["Student"] = relationship("Student", back_populates="face_profile")
