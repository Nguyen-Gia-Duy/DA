from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user, require_roles
from backend.app.controllers.attendance_controller import attendance_controller
from backend.app.schemas.attendance import (
    FaceRegisterRequest, AttendanceSessionCreate, FaceCheckInRequest, AttendanceAdjustmentCreate
)
from backend.app.models.user import User

router = APIRouter(prefix="", tags=["Điểm danh & Nhận diện Khuôn mặt AI"])

# Biometric Face Registration
@router.post("/face-profiles/register", summary="Đăng ký hồ sơ sinh trắc học khuôn mặt đa góc (Trực diện, Trái, Phải)", dependencies=[Depends(require_roles(["STUDENT"]))])
def register_face(
    request: Request,
    data: FaceRegisterRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return attendance_controller.register_face(request, current_user, data, db)

@router.post("/face-profiles/verify-pose", summary="Phân tích góc quay và chất lượng ảnh tức thời cho auto-capture")
def verify_pose(data: dict):
    image_base64 = data.get("image_base64", "")
    return attendance_controller.verify_pose(image_base64)

@router.delete("/face-profiles/revoke", summary="Thu hồi sự đồng ý và hủy kích hoạt hồ sơ sinh trắc học", dependencies=[Depends(require_roles(["STUDENT"]))])
def revoke_face(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return attendance_controller.revoke_face(request, current_user, db)

@router.get("/face-profiles/status", summary="Kiểm tra trạng thái hồ sơ khuôn mặt của tôi", dependencies=[Depends(require_roles(["STUDENT"]))])
def get_face_status(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return attendance_controller.get_face_status(current_user, db)

# Attendance Session Management
@router.post("/attendance-sessions/open", summary="Giảng viên mở phiên điểm danh", dependencies=[Depends(require_roles(["LECTURER"]))])
def open_session(
    data: AttendanceSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return attendance_controller.open_session(current_user, data, db)

@router.post("/attendance-sessions/{session_id}/close", summary="Giảng viên đóng phiên điểm danh", dependencies=[Depends(require_roles(["LECTURER"]))])
def close_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return attendance_controller.close_session(current_user, session_id, db)

# Face Check-in
@router.post("/attendance-records/check-in-face", summary="Sinh viên điểm danh bằng camera nhận diện AI", dependencies=[Depends(require_roles(["STUDENT"]))])
def check_in(
    request: Request,
    data: FaceCheckInRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return attendance_controller.check_in(request, current_user, data, db)

# Attendance Records & Adjustment
@router.get("/attendance-sessions/{session_id}/records", summary="Xem kết quả điểm danh của phiên học", dependencies=[Depends(require_roles(["ADMIN", "LECTURER"]))])
def get_session_records(session_id: int, db: Session = Depends(get_db)):
    return attendance_controller.get_session_records(session_id, db)

@router.post("/attendance-adjustments", summary="Điều chỉnh trạng thái điểm danh thủ công", dependencies=[Depends(require_roles(["ADMIN", "LECTURER"]))])
def adjust_attendance(
    data: AttendanceAdjustmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return attendance_controller.adjust_attendance(current_user, data, db)
