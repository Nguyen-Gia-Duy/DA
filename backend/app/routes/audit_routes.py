from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import require_roles
from backend.app.models.audit_log import AuditLog
from backend.app.models.recognition_attempt import RecognitionAttempt
from backend.app.models.user import User
from backend.app.models.student import Student

router = APIRouter(prefix="", tags=["Nhật ký Kiểm toán & Nhận diện AI"])

@router.get("/audit-logs", summary="Danh sách nhật ký kiểm toán hệ thống", dependencies=[Depends(require_roles(["ADMIN"]))])
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = (
        db.query(AuditLog, User.full_name, User.email)
        .outerjoin(User, AuditLog.user_id == User.id)
        .order_by(AuditLog.id.desc())
        .limit(limit)
        .all()
    )
    results = []
    for log, name, email in logs:
        results.append({
            "id": log.id,
            "user_id": log.user_id,
            "user_name": name or "Hệ thống",
            "user_email": email,
            "action": log.action,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "created_at": log.created_at
        })
    return results

@router.get("/recognition-attempts", summary="Danh sách lịch sử các lần nhận diện AI", dependencies=[Depends(require_roles(["ADMIN", "LECTURER"]))])
def get_recognition_attempts(limit: int = 50, db: Session = Depends(get_db)):
    attempts = (
        db.query(RecognitionAttempt, Student, User)
        .outerjoin(Student, RecognitionAttempt.student_id == Student.id)
        .outerjoin(User, Student.user_id == User.id)
        .order_by(RecognitionAttempt.id.desc())
        .limit(limit)
        .all()
    )
    results = []
    for att, st, u in attempts:
        results.append({
            "id": att.id,
            "attendance_session_id": att.attendance_session_id,
            "student_id": att.student_id,
            "student_code": st.student_code if st else None,
            "student_name": u.full_name if u else None,
            "attempt_status": att.attempt_status.value,
            "similarity_score": att.similarity_score,
            "failure_reason": att.failure_reason,
            "ip_address": att.ip_address,
            "attempt_time": att.attempt_time
        })
    return results
