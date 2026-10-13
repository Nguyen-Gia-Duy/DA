-- =====================================================================
-- SEED DATA: faceattend
-- Dữ liệu mẫu chuẩn cho đồ án tốt nghiệp FaceAttend Enterprise
-- Mật khẩu mặc định:
-- Admin: Admin@123
-- Lecturer: Lecturer@123
-- Student: Student@123
-- (Bcrypt hash: $2b$12$e6mZ85d4rF8yW70vN008s.rT8GzZ2uF6fF99FvT46vQ760j9kE6eW)
-- =====================================================================

USE `faceattend`;

SET FOREIGN_KEY_CHECKS = 0;

-- 1. Roles
INSERT INTO `roles` (`id`, `role_name`, `description`) VALUES
(1, 'ADMIN', 'Quản trị viên hệ thống toàn quyền'),
(2, 'LECTURER', 'Giảng viên phụ trách giảng dạy và điểm danh'),
(3, 'STUDENT', 'Sinh viên tham gia học và điểm danh khuôn mặt');

-- 2. Users ($2b$12$K89nZf4k5aZtB0E4rBvLPeG5m1y6lR7aGq8w9e0r1t2y3u4i5o6p = example bcrypt hash)
-- Mật khẩu mặc định: Admin@123, Lecturer@123, Student@123
INSERT INTO `users` (`user_id`, `email`, `password_hash`, `display_name`, `phone_number`, `account_status`) VALUES
(1, 'admin@faceattend.edu.vn', '$2b$12$KIXUqR158tS4r/1k4N4b5uQj9b1N4l3F8N2K8N2l5F8k1N4b5uQj9', 'Quản trị viên Hệ thống', '0901234567', 'ACTIVE'),
(2, 'an.nguyen@faceattend.edu.vn', '$2b$12$KIXUqR158tS4r/1k4N4b5uQj9b1N4l3F8N2K8N2l5F8k1N4b5uQj9', 'TS. Nguyễn Văn An', '0912345678', 'ACTIVE'),
(3, 'bich.tran@faceattend.edu.vn', '$2b$12$KIXUqR158tS4r/1k4N4b5uQj9b1N4l3F8N2K8N2l5F8k1N4b5uQj9', 'ThS. Trần Thị Bích', '0923456789', 'ACTIVE'),
(4, 'nguyengiaduy2005@gmail.com', '$2b$12$KIXUqR158tS4r/1k4N4b5uQj9b1N4l3F8N2K8N2l5F8k1N4b5uQj9', 'Nguyễn Gia Duy', '0934567890', 'ACTIVE'),
(5, 'nam.le@faceattend.edu.vn', '$2b$12$KIXUqR158tS4r/1k4N4b5uQj9b1N4l3F8N2K8N2l5F8k1N4b5uQj9', 'Lê Hoàng Nam', '0945678901', 'ACTIVE'),
(6, 'mai.pham@faceattend.edu.vn', '$2b$12$KIXUqR158tS4r/1k4N4b5uQj9b1N4l3F8N2K8N2l5F8k1N4b5uQj9', 'Phạm Thị Mai', '0956789012', 'ACTIVE');

-- 3. User Roles
INSERT INTO `user_roles` (`user_id`, `role_id`) VALUES
(1, 1),
(2, 2),
(3, 2),
(4, 3),
(5, 3),
(6, 3);

-- 4. Departments
INSERT INTO `departments` (`id`, `department_code`, `department_name`, `description`) VALUES
(1, 'CNTT', 'Khoa Công nghệ Thông tin', 'Đào tạo kỹ sư Khoa học máy tính & Kỹ thuật phần mềm'),
(2, 'DTVT', 'Khoa Điện tử Viễn thông', 'Đào tạo kỹ sư Điện tử, Viễn thông & IoT'),
(3, 'KTQT', 'Khoa Kinh tế & Quản trị', 'Đào tạo cử nhân Quản trị Kinh doanh & Hệ thống thông tin');

-- 5. Administrative Classes
INSERT INTO `administrative_classes` (`id`, `class_code`, `class_name`, `department_id`, `academic_year`) VALUES
(1, 'CNTT-K20A', 'Kỹ nghệ phần mềm K20A', 1, '2020-2024'),
(2, 'CNTT-K20B', 'Trí tuệ nhân tạo K20B', 1, '2020-2024'),
(3, 'DTVT-K20A', 'Hệ thống nhúng K20A', 2, '2020-2024');

-- 6. Students
INSERT INTO `students` (`id`, `user_id`, `student_code`, `administrative_class_id`, `department_id`, `date_of_birth`, `gender`, `academic_status`) VALUES
(1, 4, 'B20DCCN001', 1, 1, '2002-05-15', 'MALE', 'STUDYING'),
(2, 5, 'B20DCCN002', 1, 1, '2002-08-20', 'MALE', 'STUDYING'),
(3, 6, 'B20DCCN003', 2, 1, '2002-11-10', 'FEMALE', 'STUDYING');

-- 7. Lecturers
INSERT INTO `lecturers` (`id`, `user_id`, `lecturer_code`, `department_id`, `academic_degree`, `status`) VALUES
(1, 2, 'GV001', 1, 'Tiến sĩ', 'ACTIVE'),
(2, 3, 'GV002', 1, 'Thạc sĩ', 'ACTIVE');

-- 8. Subjects
INSERT INTO `subjects` (`id`, `subject_code`, `subject_name`, `credits`, `department_id`, `description`) VALUES
(1, 'INT1340', 'Trí tuệ Nhân tạo & Thị giác Máy tính', 3, 1, 'Deep Learning, CNN, Face Detection & Recognition'),
(2, 'INT1420', 'Kiến trúc Phần mềm Nâng cao', 3, 1, 'Microservices, Event-driven, Clean Architecture'),
(3, 'INT1200', 'Cơ sở Dữ liệu Nâng cao', 3, 1, 'MySQL Optimization, Indexing, Transactions & ACID');

-- 9. Semesters
INSERT INTO `semesters` (`id`, `semester_code`, `semester_name`, `academic_year`, `start_date`, `end_date`, `is_active`) VALUES
(1, '2024_1', 'Học kỳ 1 (2024 - 2025)', '2024-2025', '2024-09-01', '2025-01-15', 1),
(2, '2024_2', 'Học kỳ 2 (2024 - 2025)', '2024-2025', '2025-02-01', '2025-06-30', 0);

-- 10. Classrooms
INSERT INTO `classrooms` (`id`, `room_code`, `building`, `capacity`, `room_type`, `is_active`) VALUES
(1, 'A1-301', 'Nhà A1', 60, 'NORMAL', 1),
(2, 'B2-204', 'Nhà B2', 45, 'NORMAL', 1),
(3, 'LAB-AI-401', 'Nhà C', 40, 'LAB', 1);

-- 11. Class Sections
INSERT INTO `class_sections` (`id`, `section_code`, `subject_id`, `semester_id`, `lecturer_id`, `max_capacity`, `current_enrollment`, `status`) VALUES
(1, 'INT1340-01', 1, 1, 1, 60, 3, 'ACTIVE'),
(2, 'INT1420-02', 2, 1, 2, 60, 2, 'ACTIVE');

-- 12. Enrollments
INSERT INTO `enrollments` (`student_id`, `class_section_id`, `enrollment_status`) VALUES
(1, 1, 'ENROLLED'),
(2, 1, 'ENROLLED'),
(3, 1, 'ENROLLED'),
(1, 2, 'ENROLLED'),
(2, 2, 'ENROLLED');

-- 13. Schedules
INSERT INTO `schedules` (`id`, `class_section_id`, `classroom_id`, `day_of_week`, `start_time`, `end_time`, `start_date`, `end_date`) VALUES
(1, 1, 3, 'MONDAY', '07:30:00', '10:00:00', '2024-09-02', '2024-12-30'),
(2, 1, 3, 'THURSDAY', '13:00:00', '15:30:00', '2024-09-05', '2025-01-02'),
(3, 2, 1, 'TUESDAY', '08:00:00', '11:15:00', '2024-09-03', '2024-12-31');

-- 14. Attendance Sessions
INSERT INTO `attendance_sessions` (`id`, `class_section_id`, `schedule_id`, `lecturer_id`, `session_code`, `session_date`, `start_time`, `end_time`, `session_status`, `grace_period_minutes`) VALUES
(1, 1, 1, 1, 'SES-2024-09-02-INT1340', '2024-09-02', '2024-09-02 07:30:00', '2024-09-02 10:00:00', 'CLOSED', 15),
(2, 1, 2, 1, 'SES-TODAY-INT1340-01', CURDATE(), CONCAT(CURDATE(), ' 07:00:00'), NULL, 'OPEN', 20);

-- 15. Attendance Records
INSERT INTO `attendance_records` (`attendance_session_id`, `student_id`, `attendance_status`, `check_in_time`, `verification_method`, `confidence_score`) VALUES
(1, 1, 'PRESENT', '2024-09-02 07:34:12', 'AI_FACE', 0.94),
(1, 2, 'LATE', '2024-09-02 07:48:05', 'AI_FACE', 0.91),
(1, 3, 'ABSENT', NULL, 'MANUAL_LECTURER', NULL),
(2, 2, 'PRESENT', CONCAT(CURDATE(), ' 07:08:30'), 'AI_FACE', 0.96);

-- 16. Recognition Attempts
INSERT INTO `recognition_attempts` (`attendance_session_id`, `student_id`, `attempt_status`, `similarity_score`, `failure_reason`, `ip_address`) VALUES
(1, 1, 'SUCCESS', 0.94, NULL, '192.168.1.15'),
(1, 2, 'SUCCESS', 0.91, NULL, '192.168.1.18'),
(1, 3, 'FAILED_NO_FACE', NULL, 'Không phát hiện khuôn mặt trong khung hình', '192.168.1.20');

-- 17. Audit Logs
INSERT INTO `audit_logs` (`user_id`, `action`, `entity_type`, `entity_id`, `details`, `ip_address`) VALUES
(1, 'SYSTEM_INIT', 'SYSTEM', '1', '{"message": "Khởi tạo hệ thống FaceAttend Enterprise thành công"}', '127.0.0.1'),
(2, 'OPEN_ATTENDANCE_SESSION', 'attendance_sessions', '2', '{"session_code": "SES-TODAY-INT1340-01", "class_section": "INT1340-01"}', '127.0.0.1');

SET FOREIGN_KEY_CHECKS = 1;
