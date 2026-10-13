from datetime import datetime
import enum
from sqlalchemy import String, Integer, Enum, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class OTPPurpose(str, enum.Enum):
    REGISTRATION = "REGISTRATION"
    RESET_PASSWORD = "RESET_PASSWORD"
    LOGIN_VERIFICATION = "LOGIN_VERIFICATION"

class EmailOTP(Base):
    __tablename__ = "email_otps"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    otp_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    purpose: Mapped[OTPPurpose] = mapped_column(
        Enum(OTPPurpose), 
        default=OTPPurpose.REGISTRATION, 
        nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    consumed_at: Mapped[datetime | None] = mapped_column(DATETIME(fsp=6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="email_otps")
