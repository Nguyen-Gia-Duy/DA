from typing import Optional
from sqlalchemy.orm import Session
from backend.app.services.academic_service import academic_service
from backend.app.schemas.academic import (
    DepartmentCreate, AdministrativeClassCreate, StudentCreate, LecturerCreate,
    SubjectCreate, ClassSectionCreate, EnrollmentCreate, ScheduleCreate, ScheduleChangeLogCreate
)

class AcademicController:

    # Departments
    @staticmethod
    def get_departments(db: Session):
        return academic_service.get_departments(db)

    @staticmethod
    def create_department(data: DepartmentCreate, db: Session):
        return academic_service.create_department(db, data)

    # Administrative classes
    @staticmethod
    def get_admin_classes(department_id: Optional[int], db: Session):
        return academic_service.get_admin_classes(db, department_id)

    @staticmethod
    def create_admin_class(data: AdministrativeClassCreate, db: Session):
        return academic_service.create_admin_class(db, data)

    # Students
    @staticmethod
    def get_students(search: Optional[str], dept_id: Optional[int], db: Session):
        return academic_service.get_students(db, search, dept_id)

    @staticmethod
    def create_student(data: StudentCreate, db: Session):
        return academic_service.create_student(db, data)

    # Lecturers
    @staticmethod
    def get_lecturers(db: Session):
        return academic_service.get_lecturers(db)

    # Subjects
    @staticmethod
    def get_subjects(db: Session):
        return academic_service.get_subjects(db)

    @staticmethod
    def create_subject(data: SubjectCreate, db: Session):
        return academic_service.create_subject(db, data)

    # Semesters & Classrooms
    @staticmethod
    def get_semesters(db: Session):
        return academic_service.get_semesters(db)

    @staticmethod
    def get_classrooms(db: Session):
        return academic_service.get_classrooms(db)

    # Class sections
    @staticmethod
    def get_class_sections(lecturer_id: Optional[int], semester_id: Optional[int], db: Session):
        return academic_service.get_class_sections(db, lecturer_id, semester_id)

    @staticmethod
    def create_class_section(data: ClassSectionCreate, db: Session):
        return academic_service.create_class_section(db, data)

    # Enrollments
    @staticmethod
    def enroll_student(data: EnrollmentCreate, db: Session):
        return academic_service.enroll_student(db, data)

    # Schedules
    @staticmethod
    def create_schedule(data: ScheduleCreate, db: Session):
        return academic_service.create_schedule(db, data)

    @staticmethod
    def log_schedule_change(user_id: int, data: ScheduleChangeLogCreate, db: Session):
        return academic_service.log_schedule_change(db, user_id, data)

academic_controller = AcademicController()
