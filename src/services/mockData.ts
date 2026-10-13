import { User, Student, Lecturer, Department, AdministrativeClass, Subject, Semester, Classroom, ClassSection, AttendanceSession, AttendanceRecord, RecognitionAttempt, AuditLog } from '../types';

export const INITIAL_USERS: User[] = [
  {
    id: 1,
    username: 'admin',
    email: 'admin@faceattend.edu.vn',
    full_name: 'Quản trị viên Hệ thống',
    phone: '0901234567',
    account_status: 'ACTIVE',
    roles: ['ADMIN'],
    created_at: '2024-09-01T00:00:00Z',
  },
  {
    id: 2,
    username: 'gv.an.nguyen',
    email: 'an.nguyen@faceattend.edu.vn',
    full_name: 'TS. Nguyễn Văn An',
    phone: '0912345678',
    account_status: 'ACTIVE',
    roles: ['LECTURER'],
    lecturer_id: 1,
    lecturer_code: 'GV001',
    created_at: '2024-09-01T00:00:00Z',
  },
  {
    id: 4,
    username: 'sv.b20dccn001',
    email: 'nguyengiaduy2005@gmail.com',
    full_name: 'Nguyễn Gia Duy',
    phone: '0934567890',
    account_status: 'ACTIVE',
    roles: ['STUDENT'],
    student_id: 1,
    student_code: 'B20DCCN001',
    created_at: '2024-09-01T00:00:00Z',
  },
];

export const INITIAL_DEPARTMENTS: Department[] = [
  { id: 1, department_code: 'CNTT', department_name: 'Khoa Công nghệ Thông tin', description: 'Kỹ thuật phần mềm & AI', created_at: '2024-09-01T00:00:00Z' },
  { id: 2, department_code: 'DTVT', department_name: 'Khoa Điện tử Viễn thông', description: 'IoT & Hệ thống nhúng', created_at: '2024-09-01T00:00:00Z' },
  { id: 3, department_code: 'KTQT', department_name: 'Khoa Kinh tế & Quản trị', description: 'Quản trị Kinh doanh', created_at: '2024-09-01T00:00:00Z' },
];

export const INITIAL_ADMIN_CLASSES: AdministrativeClass[] = [
  { id: 1, class_code: 'CNTT-K20A', class_name: 'Kỹ nghệ phần mềm K20A', department_id: 1, department_name: 'Khoa Công nghệ Thông tin', academic_year: '2020-2024', created_at: '2024-09-01T00:00:00Z' },
  { id: 2, class_code: 'CNTT-K20B', class_name: 'Trí tuệ nhân tạo K20B', department_id: 1, department_name: 'Khoa Công nghệ Thông tin', academic_year: '2020-2024', created_at: '2024-09-01T00:00:00Z' },
];

export const INITIAL_STUDENTS: Student[] = [
  {
    id: 1,
    user_id: 4,
    student_code: 'B20DCCN001',
    full_name: 'Nguyễn Gia Duy',
    email: 'nguyengiaduy2005@gmail.com',
    phone: '0934567890',
    administrative_class_id: 1,
    class_code: 'CNTT-K20A',
    department_id: 1,
    department_name: 'Khoa Công nghệ Thông tin',
    date_of_birth: '2002-05-15',
    gender: 'MALE',
    academic_status: 'STUDYING',
    has_face_profile: true,
    created_at: '2024-09-01T00:00:00Z',
  },
  {
    id: 2,
    user_id: 5,
    student_code: 'B20DCCN002',
    full_name: 'Lê Hoàng Nam',
    email: 'nam.le@faceattend.edu.vn',
    phone: '0945678901',
    administrative_class_id: 1,
    class_code: 'CNTT-K20A',
    department_id: 1,
    department_name: 'Khoa Công nghệ Thông tin',
    date_of_birth: '2002-08-20',
    gender: 'MALE',
    academic_status: 'STUDYING',
    has_face_profile: true,
    created_at: '2024-09-01T00:00:00Z',
  },
  {
    id: 3,
    user_id: 6,
    student_code: 'B20DCCN003',
    full_name: 'Phạm Thị Mai',
    email: 'mai.pham@faceattend.edu.vn',
    phone: '0956789012',
    administrative_class_id: 2,
    class_code: 'CNTT-K20B',
    department_id: 1,
    department_name: 'Khoa Công nghệ Thông tin',
    date_of_birth: '2002-11-10',
    gender: 'FEMALE',
    academic_status: 'STUDYING',
    has_face_profile: false,
    created_at: '2024-09-01T00:00:00Z',
  },
];

export const INITIAL_LECTURERS: Lecturer[] = [
  {
    id: 1,
    user_id: 2,
    lecturer_code: 'GV001',
    full_name: 'TS. Nguyễn Văn An',
    email: 'an.nguyen@faceattend.edu.vn',
    phone: '0912345678',
    department_id: 1,
    department_name: 'Khoa Công nghệ Thông tin',
    academic_degree: 'Tiến sĩ',
    status: 'ACTIVE',
    created_at: '2024-09-01T00:00:00Z',
  },
];

export const INITIAL_SUBJECTS: Subject[] = [
  { id: 1, subject_code: 'INT1340', subject_name: 'Trí tuệ Nhân tạo & Thị giác Máy tính', credits: 3, department_id: 1, department_name: 'Khoa Công nghệ Thông tin', description: 'Deep Learning, CNN, Face Detection & Recognition', created_at: '2024-09-01T00:00:00Z' },
  { id: 2, subject_code: 'INT1420', subject_name: 'Kiến trúc Phần mềm Nâng cao', credits: 3, department_id: 1, department_name: 'Khoa Công nghệ Thông tin', description: 'Microservices & Enterprise Patterns', created_at: '2024-09-01T00:00:00Z' },
];

export const INITIAL_SEMESTERS: Semester[] = [
  { id: 1, semester_code: '2024_1', semester_name: 'Học kỳ 1 (2024 - 2025)', academic_year: '2024-2025', start_date: '2024-09-01', end_date: '2025-01-15', is_active: true, created_at: '2024-09-01T00:00:00Z' },
];

export const INITIAL_CLASSROOMS: Classroom[] = [
  { id: 1, room_code: 'A1-301', building: 'Nhà A1', capacity: 60, room_type: 'NORMAL', is_active: true, created_at: '2024-09-01T00:00:00Z' },
  { id: 2, room_code: 'LAB-AI-401', building: 'Nhà C', capacity: 40, room_type: 'LAB', is_active: true, created_at: '2024-09-01T00:00:00Z' },
];

export const INITIAL_CLASS_SECTIONS: ClassSection[] = [
  {
    id: 1,
    section_code: 'INT1340-01',
    subject_id: 1,
    subject_code: 'INT1340',
    subject_name: 'Trí tuệ Nhân tạo & Thị giác Máy tính',
    semester_id: 1,
    semester_name: 'Học kỳ 1 (2024 - 2025)',
    lecturer_id: 1,
    lecturer_name: 'TS. Nguyễn Văn An',
    max_capacity: 60,
    current_enrollment: 3,
    status: 'ACTIVE',
    created_at: '2024-09-01T00:00:00Z',
  },
];

export const INITIAL_ATTENDANCE_SESSIONS: AttendanceSession[] = [
  {
    id: 1,
    class_section_id: 1,
    section_code: 'INT1340-01',
    subject_name: 'Trí tuệ Nhân tạo & Thị giác Máy tính',
    lecturer_name: 'TS. Nguyễn Văn An',
    session_code: 'SES-TODAY-INT1340-01',
    session_date: new Date().toISOString().split('T')[0],
    start_time: new Date(Date.now() - 25 * 60000).toISOString(),
    session_status: 'OPEN',
    grace_period_minutes: 20,
    total_enrolled: 3,
    present_count: 1,
    late_count: 1,
    absent_count: 1,
    created_at: new Date().toISOString(),
  },
];

export const INITIAL_ATTENDANCE_RECORDS: AttendanceRecord[] = [
  {
    id: 1,
    attendance_session_id: 1,
    student_id: 1,
    student_code: 'B20DCCN001',
    student_name: 'Nguyễn Gia Duy',
    attendance_status: 'PRESENT',
    check_in_time: new Date(Date.now() - 20 * 60000).toISOString(),
    verification_method: 'AI_FACE',
    confidence_score: 0.95,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 2,
    attendance_session_id: 1,
    student_id: 2,
    student_code: 'B20DCCN002',
    student_name: 'Lê Hoàng Nam',
    attendance_status: 'LATE',
    check_in_time: new Date(Date.now() - 2 * 60000).toISOString(),
    verification_method: 'AI_FACE',
    confidence_score: 0.91,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 3,
    attendance_session_id: 1,
    student_id: 3,
    student_code: 'B20DCCN003',
    student_name: 'Phạm Thị Mai',
    attendance_status: 'ABSENT',
    verification_method: 'AI_FACE',
    confidence_score: undefined,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

export const INITIAL_RECOGNITION_ATTEMPTS: RecognitionAttempt[] = [
  {
    id: 1,
    attendance_session_id: 1,
    student_id: 1,
    student_code: 'B20DCCN001',
    student_name: 'Nguyễn Gia Duy',
    attempt_status: 'SUCCESS',
    similarity_score: 0.95,
    ip_address: '192.168.1.15',
    attempt_time: new Date(Date.now() - 20 * 60000).toISOString(),
  },
  {
    id: 2,
    attendance_session_id: 1,
    student_id: 2,
    student_code: 'B20DCCN002',
    student_name: 'Lê Hoàng Nam',
    attempt_status: 'SUCCESS',
    similarity_score: 0.91,
    ip_address: '192.168.1.18',
    attempt_time: new Date(Date.now() - 2 * 60000).toISOString(),
  },
  {
    id: 3,
    attendance_session_id: 1,
    student_id: 3,
    student_code: 'B20DCCN003',
    student_name: 'Phạm Thị Mai',
    attempt_status: 'FAILED_NO_FACE',
    failure_reason: 'Không phát hiện khuôn mặt trong khung hình',
    ip_address: '192.168.1.20',
    attempt_time: new Date(Date.now() - 15 * 60000).toISOString(),
  },
];

export const INITIAL_AUDIT_LOGS: AuditLog[] = [
  {
    id: 1,
    user_id: 1,
    user_name: 'Quản trị viên Hệ thống',
    action: 'SYSTEM_INIT',
    entity_type: 'SYSTEM',
    entity_id: '1',
    details: { message: 'Khởi tạo hệ thống FaceAttend Enterprise thành công' },
    ip_address: '127.0.0.1',
    created_at: '2024-09-01T00:00:00Z',
  },
  {
    id: 2,
    user_id: 2,
    user_name: 'TS. Nguyễn Văn An',
    action: 'OPEN_ATTENDANCE_SESSION',
    entity_type: 'attendance_sessions',
    entity_id: '1',
    details: { session_code: 'SES-TODAY-INT1340-01', class_section: 'INT1340-01' },
    ip_address: '127.0.0.1',
    created_at: new Date(Date.now() - 30 * 60000).toISOString(),
  },
];
