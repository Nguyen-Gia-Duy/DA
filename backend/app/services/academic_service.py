import json
from datetime import datetime, date, time
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status
from backend.app.models.department import Department
from backend.app.models.administrative_class import AdministrativeClass
from backend.app.models.student import Student, AcademicStatus
from backend.app.models.lecturer import Lecturer, LecturerStatus
from backend.app.models.subject import Subject
from backend.app.models.semester import Semester
from backend.app.models.classroom import Classroom
from backend.app.models.class_section import ClassSection, SectionStatus
from backend.app.models.enrollment import Enrollment, EnrollmentStatus
from backend.app.models.schedule import Schedule, DayOfWeek
from backend.app.models.schedule_change_log import ScheduleChangeLog, ScheduleChangeType
from backend.app.models.user import User, AccountStatus
from backend.app.models.role import Role
from backend.app.models.user_role import UserRole
from backend.app.core.security import get_password_hash
from backend.app.schemas.academic import (
    DepartmentCreate, AdministrativeClassCreate, StudentCreate, LecturerCreate,
    SubjectCreate, SemesterCreate, ClassroomCreate, ClassSectionCreate, EnrollmentCreate,
    ScheduleCreate, ScheduleChangeLogCreate
)

class AcademicService:

    # 1. Departments
    @staticmethod
    def get_departments(db: Session) -> List[Department]:
        return db.query(Department).all()

    @staticmethod
    def create_department(db: Session, data: DepartmentCreate) -> Department:
        existing = db.query(Department).filter(Department.department_code == data.department_code).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Mã khoa '{data.department_code}' đã tồn tại.")
        dept = Department(**data.model_dump())
        db.add(dept)
        db.commit()
        db.refresh(dept)
        return dept

    # 2. Administrative Classes
    @staticmethod
    def get_admin_classes(db: Session, department_id: Optional[int] = None) -> List[Dict[str, Any]]:
        query = db.query(AdministrativeClass, Department.department_name).join(Department, AdministrativeClass.department_id == Department.id)
        if department_id:
            query = query.filter(AdministrativeClass.department_id == department_id)
        results = []
        for ac, dept_name in query.all():
            results.append({
                "id": ac.id,
                "class_code": ac.class_code,
                "class_name": ac.class_name,
                "department_id": ac.department_id,
                "department_name": dept_name,
                "academic_year": ac.academic_year,
                "created_at": ac.created_at
            })
        return results

    @staticmethod
    def create_admin_class(db: Session, data: AdministrativeClassCreate) -> AdministrativeClass:
        existing = db.query(AdministrativeClass).filter(AdministrativeClass.class_code == data.class_code).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Mã lớp hành chính '{data.class_code}' đã tồn tại.")
        ac = AdministrativeClass(**data.model_dump())
        db.add(ac)
        db.commit()
        db.refresh(ac)
        return ac

    # 3. Students
    @staticmethod
    def get_students(db: Session, search: Optional[str] = None, dept_id: Optional[int] = None) -> List[Dict[str, Any]]:
        query = (
            db.query(Student, User, AdministrativeClass.class_code, Department.department_name)
            .join(User, Student.user_id == User.id)
            .join(AdministrativeClass, Student.administrative_class_id == AdministrativeClass.id)
            .join(Department, Student.department_id == Department.id)
        )
        if dept_id:
            query = query.filter(Student.department_id == dept_id)
        if search:
            s = f"%{search}%"
            query = query.filter(
                or_(
                    Student.student_code.ilike(s),
                    User.full_name.ilike(s),
                    User.email.ilike(s)
                )
            )
        
        results = []
        for st, u, c_code, d_name in query.all():
            has_face = bool(st.face_profile and st.face_profile.is_active)
            results.append({
                "id": st.id,
                "user_id": st.user_id,
                "student_code": st.student_code,
                "full_name": u.full_name,
                "email": u.email,
                "phone": u.phone,
                "administrative_class_id": st.administrative_class_id,
                "class_code": c_code,
                "department_id": st.department_id,
                "department_name": d_name,
                "date_of_birth": st.date_of_birth,
                "gender": st.gender.value,
                "academic_status": st.academic_status.value,
                "has_face_profile": has_face,
                "created_at": st.created_at
            })
        return results

    @staticmethod
    def create_student(db: Session, data: StudentCreate) -> Dict[str, Any]:
        existing = db.query(Student).filter(Student.student_code == data.student_code).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Mã sinh viên '{data.student_code}' đã tồn tại.")

        existing_user = db.query(User).filter(User.email == data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail=f"Email '{data.email}' đã được sử dụng.")

        # Tạo user tương ứng
        user = User(
            username=data.student_code.lower(),
            email=data.email,
            password_hash=get_password_hash("Student@123"), # Default password
            full_name=data.full_name,
            phone=data.phone,
            account_status=AccountStatus.ACTIVE
        )
        db.add(user)
        db.flush()

        role = db.query(Role).filter(Role.role_name == "STUDENT").first()
        if role:
            db.add(UserRole(user_id=user.id, role_id=role.id))

        student = Student(
            user_id=user.id,
            student_code=data.student_code,
            administrative_class_id=data.administrative_class_id,
            department_id=data.department_id,
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            academic_status=data.academic_status
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        return {"id": student.id, "student_code": student.student_code, "full_name": user.full_name}

    # 4. Lecturers
    @staticmethod
    def get_lecturers(db: Session) -> List[Dict[str, Any]]:
        query = (
            db.query(Lecturer, User, Department.department_name)
            .join(User, Lecturer.user_id == User.id)
            .join(Department, Lecturer.department_id == Department.id)
        )
        results = []
        for lec, u, d_name in query.all():
            results.append({
                "id": lec.id,
                "user_id": lec.user_id,
                "lecturer_code": lec.lecturer_code,
                "full_name": u.full_name,
                "email": u.email,
                "phone": u.phone,
                "department_id": lec.department_id,
                "department_name": d_name,
                "academic_degree": lec.academic_degree,
                "status": lec.status.value,
                "created_at": lec.created_at
            })
        return results

    # 5. Subjects
    @staticmethod
    def get_subjects(db: Session) -> List[Dict[str, Any]]:
        query = db.query(Subject, Department.department_name).join(Department, Subject.department_id == Department.id)
        results = []
        for sub, d_name in query.all():
            results.append({
                "id": sub.id,
                "subject_code": sub.subject_code,
                "subject_name": sub.subject_name,
                "credits": sub.credits,
                "department_id": sub.department_id,
                "department_name": d_name,
                "description": sub.description,
                "created_at": sub.created_at
            })
        return results

    @staticmethod
    def create_subject(db: Session, data: SubjectCreate) -> Subject:
        existing = db.query(Subject).filter(Subject.subject_code == data.subject_code).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Mã môn học '{data.subject_code}' đã tồn tại.")
        sub = Subject(**data.model_dump())
        db.add(sub)
        db.commit()
        db.refresh(sub)
        return sub

    # 6. Semesters & Classrooms
    @staticmethod
    def get_semesters(db: Session) -> List[Semester]:
        return db.query(Semester).order_by(Semester.start_date.desc()).all()

    @staticmethod
    def get_classrooms(db: Session) -> List[Classroom]:
        return db.query(Classroom).all()

    # 7. Class Sections
    @staticmethod
    def get_class_sections(db: Session, lecturer_id: Optional[int] = None, semester_id: Optional[int] = None) -> List[Dict[str, Any]]:
        query = (
            db.query(ClassSection, Subject, Lecturer, User, Semester)
            .join(Subject, ClassSection.subject_id == Subject.id)
            .join(Lecturer, ClassSection.lecturer_id == Lecturer.id)
            .join(User, Lecturer.user_id == User.id)
            .join(Semester, ClassSection.semester_id == Semester.id)
        )
        if lecturer_id:
            query = query.filter(ClassSection.lecturer_id == lecturer_id)
        if semester_id:
            query = query.filter(ClassSection.semester_id == semester_id)

        results = []
        for cs, sub, lec, u, sem in query.all():
            results.append({
                "id": cs.id,
                "section_code": cs.section_code,
                "subject_id": cs.subject_id,
                "subject_code": sub.subject_code,
                "subject_name": sub.subject_name,
                "semester_id": cs.semester_id,
                "semester_name": sem.semester_name,
                "lecturer_id": cs.lecturer_id,
                "lecturer_name": u.full_name,
                "max_capacity": cs.max_capacity,
                "current_enrollment": cs.current_enrollment,
                "status": cs.status.value,
                "created_at": cs.created_at
            })
        return results

    @staticmethod
    def create_class_section(db: Session, data: ClassSectionCreate) -> ClassSection:
        existing = db.query(ClassSection).filter(ClassSection.section_code == data.section_code).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Mã lớp học phần '{data.section_code}' đã tồn tại.")
        cs = ClassSection(**data.model_dump(), current_enrollment=0, status=SectionStatus.ACTIVE)
        db.add(cs)
        db.commit()
        db.refresh(cs)
        return cs

    # 8. Enrollments (Đăng ký học phần & kiểm tra sĩ số)
    @staticmethod
    def enroll_student(db: Session, data: EnrollmentCreate) -> Enrollment:
        section = db.query(ClassSection).filter(ClassSection.id == data.class_section_id).first()
        if not section:
            raise HTTPException(status_code=404, detail="Lớp học phần không tồn tại.")

        student = db.query(Student).filter(Student.id == data.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Sinh viên không tồn tại.")
        if student.academic_status == AcademicStatus.DROPPED_OUT:
            raise HTTPException(status_code=400, detail="Sinh viên đã thôi học, không được phép đăng ký học phần.")

        # Kiểm tra trùng đăng ký
        existing = db.query(Enrollment).filter(
            Enrollment.student_id == data.student_id,
            Enrollment.class_section_id == data.class_section_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Sinh viên đã đăng ký lớp học phần này trước đó.")

        # Kiểm tra vượt sĩ số
        if section.current_enrollment >= section.max_capacity:
            raise HTTPException(status_code=400, detail=f"Lớp học phần đã đủ sĩ số tối đa ({section.max_capacity} sinh viên).")

        enrollment = Enrollment(
            student_id=data.student_id,
            class_section_id=data.class_section_id,
            enrollment_status=EnrollmentStatus.ENROLLED
        )
        db.add(enrollment)
        section.current_enrollment += 1
        db.commit()
        db.refresh(enrollment)
        return enrollment

    # 9. Schedules (Kiểm tra xung đột phòng và giảng viên)
    @staticmethod
    def create_schedule(db: Session, data: ScheduleCreate) -> Schedule:
        section = db.query(ClassSection).filter(ClassSection.id == data.class_section_id).first()
        if not section:
            raise HTTPException(status_code=404, detail="Lớp học phần không tồn tại.")

        # Kiểm tra trùng phòng học cùng thứ và khung giờ
        room_conflict = db.query(Schedule).filter(
            Schedule.classroom_id == data.classroom_id,
            Schedule.day_of_week == data.day_of_week,
            Schedule.start_date <= data.end_date,
            Schedule.end_date >= data.start_date,
            Schedule.start_time < data.end_time,
            Schedule.end_time > data.start_time
        ).first()

        if room_conflict:
            raise HTTPException(
                status_code=400,
                detail=f"Xung đột lịch: Phòng học đã được xếp cho lớp học phần khác vào {data.day_of_week} ({data.start_time} - {data.end_time})."
            )

        # Kiểm tra trùng lịch giảng viên
        lecturer_conflict = (
            db.query(Schedule)
            .join(ClassSection, Schedule.class_section_id == ClassSection.id)
            .filter(
                ClassSection.lecturer_id == section.lecturer_id,
                Schedule.day_of_week == data.day_of_week,
                Schedule.start_date <= data.end_date,
                Schedule.end_date >= data.start_date,
                Schedule.start_time < data.end_time,
                Schedule.end_time > data.start_time
            ).first()
        )
        if lecturer_conflict:
            raise HTTPException(
                status_code=400,
                detail=f"Xung đột lịch: Giảng viên đã có lịch dạy lớp khác vào khung giờ này ({data.start_time} - {data.end_time})."
            )

        schedule = Schedule(**data.model_dump())
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule

    @staticmethod
    def log_schedule_change(db: Session, user_id: int, data: ScheduleChangeLogCreate) -> ScheduleChangeLog:
        schedule = db.query(Schedule).filter(Schedule.id == data.schedule_id).first()
        if not schedule:
            raise HTTPException(status_code=404, detail="Lịch học không tồn tại.")

        old_values = {
            "classroom_id": schedule.classroom_id,
            "start_time": str(schedule.start_time),
            "end_time": str(schedule.end_time)
        }
        new_values = {}

        if data.new_classroom_id:
            schedule.classroom_id = data.new_classroom_id
            new_values["classroom_id"] = data.new_classroom_id
        if data.new_start_time:
            schedule.start_time = data.new_start_time
            new_values["start_time"] = data.new_start_time
        if data.new_end_time:
            schedule.end_time = data.new_end_time
            new_values["end_time"] = data.new_end_time

        log = ScheduleChangeLog(
            schedule_id=data.schedule_id,
            changed_by_user_id=user_id,
            change_type=data.change_type,
            old_values=old_values,
            new_values=new_values,
            reason=data.reason
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

academic_service = AcademicService()
