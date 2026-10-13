from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime, date, time

# Department
class DepartmentBase(BaseModel):
    department_code: str
    department_name: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Administrative Class
class AdministrativeClassBase(BaseModel):
    class_code: str
    class_name: str
    department_id: int
    academic_year: str

class AdministrativeClassCreate(AdministrativeClassBase):
    pass

class AdministrativeClassResponse(AdministrativeClassBase):
    id: int
    department_name: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

# Student
class StudentBase(BaseModel):
    student_code: str
    administrative_class_id: int
    department_id: int
    date_of_birth: Optional[date] = None
    gender: str = "MALE"
    academic_status: str = "STUDYING"

class StudentCreate(StudentBase):
    full_name: str
    email: str
    phone: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    user_id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    class_code: Optional[str] = None
    department_name: Optional[str] = None
    has_face_profile: bool = False
    created_at: datetime
    class Config:
        from_attributes = True

# Lecturer
class LecturerBase(BaseModel):
    lecturer_code: str
    department_id: int
    academic_degree: Optional[str] = "Thạc sĩ"
    status: str = "ACTIVE"

class LecturerCreate(LecturerBase):
    full_name: str
    email: str
    phone: Optional[str] = None

class LecturerResponse(LecturerBase):
    id: int
    user_id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    department_name: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

# Subject
class SubjectBase(BaseModel):
    subject_code: str
    subject_name: str
    credits: int = 3
    department_id: int
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int
    department_name: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

# Semester
class SemesterBase(BaseModel):
    semester_code: str
    semester_name: str
    academic_year: str
    start_date: date
    end_date: date
    is_active: bool = False

class SemesterCreate(SemesterBase):
    pass

class SemesterResponse(SemesterBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Classroom
class ClassroomBase(BaseModel):
    room_code: str
    building: str
    capacity: int = 60
    room_type: str = "NORMAL"
    is_active: bool = True

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomResponse(ClassroomBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Class Section
class ClassSectionBase(BaseModel):
    section_code: str
    subject_id: int
    semester_id: int
    lecturer_id: int
    max_capacity: int = 60

class ClassSectionCreate(ClassSectionBase):
    pass

class ClassSectionResponse(ClassSectionBase):
    id: int
    current_enrollment: int
    status: str
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None
    lecturer_name: Optional[str] = None
    semester_name: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

# Enrollment
class EnrollmentCreate(BaseModel):
    student_id: int
    class_section_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    class_section_id: int
    enrollment_status: str
    student_code: Optional[str] = None
    student_name: Optional[str] = None
    section_code: Optional[str] = None
    registered_at: datetime
    class Config:
        from_attributes = True

# Schedule
class ScheduleBase(BaseModel):
    class_section_id: int
    classroom_id: int
    day_of_week: str
    start_time: str # "07:30:00"
    end_time: str   # "10:00:00"
    start_date: date
    end_date: date

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int
    room_code: Optional[str] = None
    building: Optional[str] = None
    section_code: Optional[str] = None
    subject_name: Optional[str] = None
    lecturer_name: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

# Schedule Change Log
class ScheduleChangeLogCreate(BaseModel):
    schedule_id: int
    change_type: str
    new_classroom_id: Optional[int] = None
    new_start_time: Optional[str] = None
    new_end_time: Optional[str] = None
    reason: str

class ScheduleChangeLogResponse(BaseModel):
    id: int
    schedule_id: int
    changed_by_user_id: int
    changed_by_name: Optional[str] = None
    change_type: str
    old_values: Optional[Any] = None
    new_values: Optional[Any] = None
    reason: str
    created_at: datetime
    class Config:
        from_attributes = True
