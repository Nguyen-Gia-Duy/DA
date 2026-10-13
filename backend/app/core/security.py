import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import numpy as np
from passlib.context import CryptContext
from jose import JWTError, jwt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_random_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)

def generate_otp_code(digits: int = 6) -> str:
    return "".join(secrets.choice("0123456789") for _ in range(digits))

def hash_otp(otp: str) -> str:
    """Hash OTP sử dụng SHA-256 HMAC với secret key hệ thống"""
    key = settings.JWT_SECRET_KEY.encode("utf-8")
    return hmac.new(key, otp.encode("utf-8"), hashlib.sha256).hexdigest()

def verify_otp_hash(plain_otp: str, hashed_otp: str) -> bool:
    expected = hash_otp(plain_otp)
    return hmac.compare_digest(expected, hashed_otp)

# --- Mã hóa an toàn vector đặc trưng khuôn mặt (AES-256 GCM) ---

def _get_encryption_key() -> bytes:
    key_hex = settings.EMBEDDING_ENCRYPTION_KEY
    try:
        key_bytes = bytes.fromhex(key_hex)
        if len(key_bytes) == 32:
            return key_bytes
    except ValueError:
        pass
    # Fallback pad/truncate to 32 bytes
    return hashlib.sha256(key_hex.encode("utf-8")).digest()

def encrypt_face_embedding(embedding: np.ndarray) -> bytes:
    """Mã hóa numpy array 512-dim embedding thành bytes nhị phân an toàn với AES-256 GCM"""
    data_bytes = embedding.astype(np.float32).tobytes()
    key = _get_encryption_key()
    iv = secrets.token_bytes(12)  # GCM 96-bit IV
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()
    ciphertext = encryptor.update(data_bytes) + encryptor.finalize()
    # Format: IV (12 bytes) + TAG (16 bytes) + CIPHERTEXT
    return iv + encryptor.tag + ciphertext

def decrypt_face_embedding(encrypted_bytes: bytes) -> np.ndarray:
    """Giải mã template sinh trắc học thành numpy array float32 512 chiều"""
    if len(encrypted_bytes) < 28:
        raise ValueError("Dữ liệu template sinh trắc học không hợp lệ")
    iv = encrypted_bytes[:12]
    tag = encrypted_bytes[12:28]
    ciphertext = encrypted_bytes[28:]
    key = _get_encryption_key()
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()
    data_bytes = decryptor.update(ciphertext) + decryptor.finalize()
    return np.frombuffer(data_bytes, dtype=np.float32)
