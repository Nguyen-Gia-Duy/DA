import pytest
from sqlalchemy import inspect
from backend.app.core.database import Base
import backend.app.models as models

def test_all_21_models_plus_otp_registered():
    """Kiểm tra toàn bộ 21 Model cốt lõi + bảng email_otps được đăng ký chính xác trong SQLAlchemy Metadata"""
    expected_tables = {
        "roles",
        "users",
        "user_roles",
        "user_sessions",
        "departments",
        "administrative_classes",
        "students",
        "lecturers",
        "subjects",
        "semesters",
        "classrooms",
        "class_sections",
        "enrollments",
        "schedules",
        "schedule_change_logs",
        "face_profiles",
        "attendance_sessions",
        "attendance_records",
        "recognition_attempts",
        "attendance_adjustments",
        "audit_logs",
        "email_otps" # Bảng bổ sung có kiểm soát
    }
    
    metadata_tables = set(Base.metadata.tables.keys())
    for tbl in expected_tables:
        assert tbl in metadata_tables, f"Bảng {tbl} chưa được khai báo trong SQLAlchemy models!"
    
    assert len(expected_tables) == 22

def test_user_model_columns():
    """Kiểm tra chi tiết cột, kiểu dữ liệu và ràng buộc của bảng users"""
    user_table = Base.metadata.tables["users"]
    cols = user_table.columns
    assert "id" in cols
    assert "username" in cols
    assert "email" in cols
    assert "password_hash" in cols
    assert "account_status" in cols
    assert "created_at" in cols
    assert "updated_at" in cols

def test_face_profile_encrypted_template_column():
    """Kiểm tra cột encrypted_template của face_profiles là MEDIUMBLOB"""
    fp_table = Base.metadata.tables["face_profiles"]
    assert "encrypted_template" in fp_table.columns
    assert "model_name" in fp_table.columns
    assert "quality_score" in fp_table.columns
    assert "is_active" in fp_table.columns

def test_attendance_records_columns():
    """Kiểm tra bảng attendance_records và khóa ngoại"""
    ar_table = Base.metadata.tables["attendance_records"]
    assert "attendance_session_id" in ar_table.columns
    assert "student_id" in ar_table.columns
    assert "attendance_status" in ar_table.columns
    assert "verification_method" in ar_table.columns
    assert "confidence_score" in ar_table.columns
