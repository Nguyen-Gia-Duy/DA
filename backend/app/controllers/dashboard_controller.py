from sqlalchemy.orm import Session
from backend.app.services.dashboard_service import dashboard_service
from backend.app.models.user import User

class DashboardController:

    @staticmethod
    def get_admin_dashboard(db: Session):
        return dashboard_service.get_admin_dashboard(db)

    @staticmethod
    def get_lecturer_dashboard(current_user: User, db: Session):
        if not current_user.lecturer:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Không tìm thấy hồ sơ giảng viên.")
        return dashboard_service.get_lecturer_dashboard(db, current_user.lecturer.id)

    @staticmethod
    def get_student_dashboard(current_user: User, db: Session):
        if not current_user.student:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Không tìm thấy hồ sơ sinh viên.")
        return dashboard_service.get_student_dashboard(db, current_user.student.id)

dashboard_controller = DashboardController()
