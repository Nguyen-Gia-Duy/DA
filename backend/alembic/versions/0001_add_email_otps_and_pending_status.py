"""Bổ sung bảng email_otps và cập nhật trạng thái PENDING cho users.account_status

Revision ID: 0001_add_email_otps_and_pending_status
Revises: 
Create Date: 2026-10-13 00:00:00.000000

Mô tả lý do tạo migration:
- Database nền tảng faceattend gồm 21 bảng chưa có bảng lưu mã OTP xác thực email khi sinh viên đăng ký hoặc đổi mật khẩu.
- Migration này tạo bảng `email_otps` với các trường: id, user_id, otp_hash, purpose, expires_at, attempts, consumed_at, created_at.
- Đồng thời cập nhật ENUM `account_status` của bảng `users` để bổ sung giá trị 'PENDING' phục vụ quy trình sinh viên đăng ký chờ xác minh OTP qua Gmail, bảo toàn dữ liệu hiện có (ACTIVE, INACTIVE, SUSPENDED).
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = "0001_add_email_otps_and_pending_status"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Cập nhật ENUM account_status trên bảng users để bổ sung giá trị PENDING
    # Giữ nguyên kiểu dữ liệu, index và dữ liệu hiện có
    op.execute("""
        ALTER TABLE `users` 
        MODIFY COLUMN `account_status` ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED', 'PENDING') 
        NOT NULL DEFAULT 'PENDING'
    """)

    # 2. Tạo bảng email_otps có kiểm soát
    op.create_table(
        "email_otps",
        sa.Column("id", mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column("user_id", mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column("otp_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "purpose",
            sa.Enum("REGISTRATION", "RESET_PASSWORD", "LOGIN_VERIFICATION", name="otppurpose"),
            server_default="REGISTRATION",
            nullable=False,
        ),
        sa.Column("expires_at", mysql.DATETIME(fsp=6), nullable=False),
        sa.Column("attempts", sa.Integer(), server_default="0", nullable=False),
        sa.Column("consumed_at", mysql.DATETIME(fsp=6), nullable=True),
        sa.Column("created_at", mysql.DATETIME(fsp=6), server_default=sa.text("CURRENT_TIMESTAMP(6)"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE", name="fk_email_otps_user"),
        sa.PrimaryKeyConstraint("id"),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
        mysql_engine="InnoDB",
    )
    op.create_index("idx_email_otps_user", "email_otps", ["user_id"], unique=False)

def downgrade() -> None:
    op.drop_index("idx_email_otps_user", table_name="email_otps")
    op.drop_table("email_otps")
    op.execute("""
        ALTER TABLE `users` 
        MODIFY COLUMN `account_status` ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED') 
        NOT NULL DEFAULT 'INACTIVE'
    """)
