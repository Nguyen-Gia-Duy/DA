from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AdminDashboardStats(BaseModel):
    total_students: int
    total_lecturers: int
    total_departments: int
    total_class_sections: int
    total_subjects: int
    total_attendance_sessions: int
    overall_attendance_rate: float
    today_sessions_count: int
    late_count: int
    absent_count: int
    failed_attempts_count: int
    attendance_trends: List[Dict[str, Any]]
    recent_activities: List[Dict[str, Any]]

class LecturerDashboardStats(BaseModel):
    assigned_sections_count: int
    total_students: int
    active_sessions_count: int
    average_attendance_rate: float
    upcoming_schedules: List[Dict[str, Any]]
    recent_sessions: List[Dict[str, Any]]

class StudentDashboardStats(BaseModel):
    student_id: int
    student_code: str
    student_name: str
    class_name: str
    has_face_profile: bool
    enrolled_courses_count: int
    total_attended_sessions: int
    attendance_rate: float
    today_classes: List[Dict[str, Any]]
    recent_attendance_history: List[Dict[str, Any]]
