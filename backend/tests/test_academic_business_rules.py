import pytest
from datetime import datetime, timedelta, timezone
from backend.app.core.security import (
    create_access_token, decode_access_token, hash_otp, verify_otp_hash,
    verify_password, get_password_hash
)

def test_jwt_creation_and_expiration():
    """Kiểm tra tạo JWT token và giải mã payload"""
    data = {"sub": "123", "username": "admin", "roles": ["ADMIN"]}
    token = create_access_token(data, expires_delta=timedelta(minutes=30))
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "123"
    assert decoded["username"] == "admin"
    assert "ADMIN" in decoded["roles"]

def test_otp_hmac_hashing_and_verification():
    """Kiểm tra cơ chế hash OTP bằng SHA-256 HMAC (không lưu plaintext)"""
    otp = "481920"
    otp_hash = hash_otp(otp)
    assert otp_hash != otp
    assert verify_otp_hash(otp, otp_hash) is True
    assert verify_otp_hash("000000", otp_hash) is False

def test_password_bcrypt():
    """Kiểm tra hash và xác thực mật khẩu Bcrypt"""
    raw_pwd = "MySecretPassword@123"
    hashed = get_password_hash(raw_pwd)
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False
