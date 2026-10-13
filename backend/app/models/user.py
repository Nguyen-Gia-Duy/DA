from datetime import datetime
import enum
from sqlalchemy import String, Enum, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class AccountStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    DISABLED = "DISABLED"
    LOCKED = "LOCKED"

class User(Base):
    __tablename__ = "users"

    # Ánh xạ chuẩn 1:1 với schema MySQL database faceattend
    user_id: Mapped[int] = mapped_column("user_id", BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column("email", String(191), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column("password_hash", String(255), nullable=False)
    display_name: Mapped[str] = mapped_column("display_name", String(150), nullable=False)
    phone_number: Mapped[str | None] = mapped_column("phone_number", String(20), nullable=True)
    account_status: Mapped[AccountStatus] = mapped_column(
        "account_status",
        Enum(AccountStatus), 
        default=AccountStatus.PENDING, 
        nullable=False,
        index=True
    )
    last_login_at: Mapped[datetime | None] = mapped_column("last_login_at", DATETIME(fsp=6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        DATETIME(fsp=6), 
        default=func.current_timestamp(6), 
        onupdate=func.current_timestamp(6), 
        nullable=False
    )

    # Thuộc tính tiện ích (Python Aliases) đồng bộ hóa logic
    @property
    def id(self) -> int:
        return self.user_id

    @id.setter
    def id(self, val: int):
        self.user_id = val

    @property
    def full_name(self) -> str:
        return self.display_name

    @full_name.setter
    def full_name(self, val: str):
        self.display_name = val

    @property
    def phone(self) -> str | None:
        return self.phone_number

    @phone.setter
    def phone(self, val: str | None):
        self.phone_number = val

    @property
    def username(self) -> str:
        return self.email.split("@")[0]

    # Relationships (Đúng khóa ngoại foreign_keys=['user_id'] trỏ vào users.user_id)
    user_roles: Mapped[list["UserRole"]] = relationship("UserRole", back_populates="user", cascade="all, delete-orphan", foreign_keys="[UserRole.user_id]")
    sessions: Mapped[list["UserSession"]] = relationship("UserSession", back_populates="user", cascade="all, delete-orphan", foreign_keys="[UserSession.user_id]")
    student: Mapped["Student | None"] = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan", foreign_keys="[Student.user_id]")
    lecturer: Mapped["Lecturer | None"] = relationship("Lecturer", back_populates="user", uselist=False, cascade="all, delete-orphan", foreign_keys="[Lecturer.user_id]")
    email_otps: Mapped[list["EmailOTP"]] = relationship("EmailOTP", back_populates="user", cascade="all, delete-orphan", foreign_keys="[EmailOTP.user_id]")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="user", foreign_keys="[AuditLog.user_id]")
