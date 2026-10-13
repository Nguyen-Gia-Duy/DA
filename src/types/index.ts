export type RoleName = 'ADMIN' | 'LECTURER' | 'STUDENT';

export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  phone?: string;
  avatar_url?: string;
  account_status: 'ACTIVE' | 'INACTIVE' | 'SUSPENDED' | 'PENDING';
  roles: RoleName[];
  student_id?: number;
  student_code?: string;
  lecturer_id?: number;
  lecturer_code?: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id: number;
  username: string;
  full_name: string;
  email: string;
  roles: RoleName[];
  student_id?: number;
  student_code?: string;
  lecturer_id?: number;
  lecturer_code?: string;
}

export interface Department {
  id: number;
  department_code: string;
  department_name: string;
  description?: string;
  created_at: string;
}

export interface AdministrativeClass {
  id: number;
  class_code: string;
  class_name: string;
  department_id: number;
  department_name?: string;
  academic_year: string;
  created_at: string;
}

export interface Student {
  id: number;
  user_id: number;
  student_code: string;
  full_name: string;
  email: string;
  phone?: string;
  administrative_class_id: number;
  class_code?: string;
  department_id: number;
  department_name?: string;
  date_of_birth?: string;
  gender: 'MALE' | 'FEMALE' | 'OTHER';
  academic_status: 'STUDYING' | 'SUSPENDED' | 'DROPPED_OUT' | 'GRADUATED';
  has_face_profile: boolean;
  created_at: string;
}

export interface Lecturer {
  id: number;
  user_id: number;
  lecturer_code: string;
  full_name: string;
  email: string;
  phone?: string;
  department_id: number;
  department_name?: string;
  academic_degree?: string;
  status: 'ACTIVE' | 'ON_LEAVE' | 'RETIRED';
  created_at: string;
}

export interface Subject {
  id: number;
  subject_code: string;
  subject_name: string;
  credits: number;
  department_id: number;
  department_name?: string;
  description?: string;
  created_at: string;
}

export interface Semester {
  id: number;
  semester_code: string;
  semester_name: string;
  academic_year: string;
  start_date: string;
  end_date: string;
  is_active: boolean;
  created_at: string;
}

export interface Classroom {
  id: number;
  room_code: string;
  building: string;
  capacity: number;
  room_type: 'LECTURE_HALL' | 'LAB' | 'NORMAL';
  is_active: boolean;
  created_at: string;
}

export interface ClassSection {
  id: number;
  section_code: string;
  subject_id: number;
  subject_code?: string;
  subject_name?: string;
  semester_id: number;
  semester_name?: string;
  lecturer_id: number;
  lecturer_name?: string;
  max_capacity: number;
  current_enrollment: number;
  status: 'PLANNING' | 'ACTIVE' | 'COMPLETED' | 'CANCELLED';
  created_at: string;
}

export interface AttendanceSession {
  id: number;
  class_section_id: number;
  section_code: string;
  subject_name: string;
  lecturer_name: string;
  session_code: string;
  session_date: string;
  start_time: string;
  end_time?: string;
  session_status: 'OPEN' | 'CLOSED' | 'CANCELLED';
  grace_period_minutes: number;
  total_enrolled?: number;
  present_count?: number;
  late_count?: number;
  absent_count?: number;
  created_at: string;
}

export interface AttendanceRecord {
  id: number;
  attendance_session_id: number;
  student_id: number;
  student_code: string;
  student_name: string;
  attendance_status: 'PRESENT' | 'LATE' | 'ABSENT' | 'EXCUSED' | 'NEEDS_REVIEW';
  check_in_time?: string;
  verification_method: 'AI_FACE' | 'MANUAL_LECTURER' | 'ADJUSTMENT';
  confidence_score?: number;
  created_at: string;
  updated_at: string;
}

export interface RecognitionAttempt {
  id: number;
  attendance_session_id: number;
  student_id?: number;
  student_code?: string;
  student_name?: string;
  attempt_status: 'SUCCESS' | 'FAILED_NO_FACE' | 'FAILED_MULTIPLE_FACES' | 'FAILED_LOW_CONFIDENCE' | 'FAILED_SPOOF_SUSPECTED' | 'FAILED_NOT_ENROLLED';
  similarity_score?: number;
  failure_reason?: string;
  ip_address?: string;
  attempt_time: string;
}

export interface AuditLog {
  id: number;
  user_id?: number;
  user_name: string;
  user_email?: string;
  action: string;
  entity_type: string;
  entity_id?: string;
  details?: any;
  ip_address?: string;
  created_at: string;
}

export interface AdminDashboardData {
  total_students: number;
  total_lecturers: number;
  total_departments: number;
  total_class_sections: number;
  total_subjects: number;
  total_attendance_sessions: number;
  overall_attendance_rate: number;
  today_sessions_count: number;
  late_count: number;
  absent_count: number;
  failed_attempts_count: number;
  attendance_trends: Array<{
    date: string;
    present: number;
    late: number;
    absent: number;
  }>;
  recent_activities: Array<{
    id: number;
    action: string;
    user_name: string;
    entity_type: string;
    created_at: string;
  }>;
}

export interface LecturerDashboardData {
  assigned_sections_count: number;
  total_students: number;
  active_sessions_count: number;
  average_attendance_rate: number;
  recent_sessions: Array<{
    id: number;
    session_code: string;
    section_code: string;
    subject_name: string;
    session_date: string;
    status: string;
  }>;
}

export interface StudentDashboardData {
  student_id: number;
  student_code: string;
  student_name: string;
  class_name: string;
  has_face_profile: boolean;
  enrolled_courses_count: number;
  total_attended_sessions: number;
  attendance_rate: number;
  recent_attendance_history: Array<{
    id: number;
    section_code: string;
    subject_name: string;
    session_date: string;
    check_in_time: string;
    status: string;
    confidence_score?: number;
  }>;
}
