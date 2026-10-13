
import os
from typing import List

from sqlalchemy.engine import URL
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    PROJECT_NAME: str = "FaceAttend Enterprise"
    API_V1_STR: str = "/api"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DEBUG: bool = False

    # MySQL Configuration
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "faceattend"
    MYSQL_CHARSET: str = "utf8mb4"

    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_RECYCLE: int = 3600

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        url = URL.create(
            drivername="mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            database=self.MYSQL_DATABASE,
            query={"charset": self.MYSQL_CHARSET},
        )
        return url.render_as_string(hide_password=False)

    # JWT Authentication
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Biometrics & Encryption
    EMBEDDING_ENCRYPTION_KEY: str = ""
    ENCRYPTION_KEY_VERSION: str = "v1"

    # AI Recognition Parameters
    FACE_DETECTION_MODEL: str = "buffalo_l"
    DETECTION_THRESHOLD: float = 0.65
    RECOGNITION_SIMILARITY_THRESHOLD: float = 0.60
    MIN_FACE_SIZE: int = 60
    BLUR_LAPLACIAN_THRESHOLD: float = 100.0
    LIVENESS_CONFIDENCE_THRESHOLD: float = 0.75

    # SMTP Gmail
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = ""
    EMAILS_FROM_NAME: str = "Hệ thống FaceAttend Enterprise"
    OTP_EXPIRE_MINUTES: int = 10
    OTP_MAX_ATTEMPTS: int = 5

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            ),
            ".env"
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
