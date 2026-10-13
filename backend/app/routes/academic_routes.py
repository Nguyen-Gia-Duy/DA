from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user, require_roles
from backend.app.controllers.academic_controller import academic_controller
from backend.app.schemas.academic import (
    DepartmentCreate, AdministrativeClassCreate, StudentCreate, LecturerCreate,
    SubjectCreate, ClassSectionCreate, EnrollmentCreate, ScheduleCreate, ScheduleChangeLogCreate
)
from backend.app.models.user import User

router = APIRouter(prefix="", tags=["Quản lý Đào tạo"])

# Departments
@router.get("/departments", summary="Danh sách khoa")
def list_departments(db: Session = Depends(get_db)):
    return academic_controller.get_departments(db)

@router.post("/departments", summary="Thêm khoa mới", dependencies=[Depends(require_roles(["ADMIN"]))])
def create_department(data: DepartmentCreate, db: Session = Depends(get_db)):
    return academic_controller.create_department(data, db)

# Administrative Classes
@router.get("/administrative-classes", summary="Danh sách lớp hành chính")
def list_admin_classes(department_id: Optional[int] = None, db: Session = Depends(get_db)):
    return academic_controller.get_admin_classes(department_id, db)

@router.post("/administrative-classes", summary="Tạo lớp hành chính", dependencies=[Depends(require_roles(["ADMIN"]))])
def create_admin_class(data: AdministrativeClassCreate, db: Session = Depends(get_db)):
    return academic_controller.create_admin_class(data, db)

# Students
@router.get("/students", summary="Danh sách sinh viên", dependencies=[Depends(require_roles(["ADMIN", "LECTURER"]))])
def list_students(search: Optional[str] = None, dept_id: Optional[int] = None, db: Session = Depends(get_db)):
    return academic_controller.get_students(search, dept_id, db)

@router.post("/students", summary="Thêm sinh viên mới", dependencies=[Depends(require_roles(["ADMIN"]))])
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    return academic_controller.create_student(data, db)

# Lecturers
@router.get("/lecturers", summary="Danh sách giảng viên", dependencies=[Depends(require_roles(["ADMIN"]))])
def list_lecturers(db: Session = Depends(get_db)):
    return academic_controller.get_lecturers(db)

# Subjects
@router.get("/subjects", summary="Danh sách môn học")
def list_subjects(db: Session = Depends(get_db)):
    return academic_controller.get_subjects(db)

@router.post("/subjects", summary="Thêm môn học mới", dependencies=[Depends(require_roles(["ADMIN"]))])
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    return academic_controller.create_subject(data, db)

# Semesters & Classrooms
@router.get("/semesters", summary="Danh sách học kỳ")
def list_semesters(db: Session = Depends(get_db)):
    return academic_controller.get_semesters(db)

@router.get("/classrooms", summary="Danh sách phòng học")
def list_classrooms(db: Session = Depends(get_db)):
    return academic_controller.get_classrooms(db)

# Class Sections
@router.get("/class-sections", summary="Danh sách lớp học phần")
def list_class_sections(lecturer_id: Optional[int] = None, semester_id: Optional[int] = None, db: Session = Depends(get_db)):
    return academic_controller.get_class_sections(lecturer_id, semester_id, db)

@router.post("/class-sections", summary="Tạo lớp học phần mới", dependencies=[Depends(require_roles(["ADMIN"]))])
def create_class_section(data: ClassSectionCreate, db: Session = Depends(get_db)):
    return academic_controller.create_class_section(data, db)

# Enrollments
@router.post("/enrollments", summary="Đăng ký học phần", dependencies=[Depends(require_roles(["ADMIN", "STUDENT"]))])
def enroll_student(data: EnrollmentCreate, db: Session = Depends(get_db)):
    return academic_controller.enroll_student(data, db)

# Schedules
@router.post("/schedules", summary="Xếp lịch học phần", dependencies=[Depends(require_roles(["ADMIN"]))])
def create_schedule(data: ScheduleCreate, db: Session = Depends(get_db)):
    return academic_controller.create_schedule(data, db)

@router.post("/schedule-change-logs", summary="Ghi nhật ký thay đổi lịch học", dependencies=[Depends(require_roles(["ADMIN", "LECTURER"]))])
def log_schedule_change(data: ScheduleChangeLogCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return academic_controller.log_schedule_change(current_user.id, data, db)
