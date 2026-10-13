from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user, require_roles
from backend.app.controllers.dashboard_controller import dashboard_controller
from backend.app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Thống kê & Báo cáo Dashboard"])

@router.get("/admin", summary="Dữ liệu Dashboard Quản trị viên", dependencies=[Depends(require_roles(["ADMIN"]))])
def get_admin_dashboard(db: Session = Depends(get_db)):
    return dashboard_controller.get_admin_dashboard(db)

@router.get("/lecturer", summary="Dữ liệu Dashboard Giảng viên", dependencies=[Depends(require_roles(["LECTURER"]))])
def get_lecturer_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return dashboard_controller.get_lecturer_dashboard(current_user, db)

@router.get("/student", summary="Dữ liệu Dashboard Sinh viên", dependencies=[Depends(require_roles(["STUDENT"]))])
def get_student_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return dashboard_controller.get_student_dashboard(current_user, db)
