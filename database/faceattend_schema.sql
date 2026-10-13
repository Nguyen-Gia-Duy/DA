-- =====================================================================
-- DATABASE: faceattend
-- HỆ THỐNG QUẢN LÝ SINH VIÊN VÀ ĐIỂM DANH TỰ ĐỘNG BẰNG NHẬN DIỆN KHUÔN MẶT AI
-- Chuẩn kiến trúc MySQL 8.x / InnoDB
-- =====================================================================

CREATE DATABASE IF NOT EXISTS `faceattend` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `faceattend`;

SET FOREIGN_KEY_CHECKS = 0;

-- 1. Bảng roles: Vai trò trong hệ thống (ADMIN, LECTURER, STUDENT)
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `role_name` VARCHAR(50) NOT NULL UNIQUE,
    `description` VARCHAR(255) NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Bảng users: Tài khoản người dùng (Chuẩn hóa chính xác theo schema MySQL faceattend)
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `user_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(191) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `display_name` VARCHAR(150) NOT NULL,
    `phone_number` VARCHAR(20) NULL,
    `account_status` ENUM('ACTIVE', 'PENDING', 'DISABLED', 'LOCKED') NOT NULL DEFAULT 'PENDING',
    `last_login_at` DATETIME(6) NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`user_id`),
    INDEX `idx_users_email` (`email`),
    INDEX `idx_users_status` (`account_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Bảng user_roles: Phân vai trò cho tài khoản
DROP TABLE IF EXISTS `user_roles`;
CREATE TABLE `user_roles` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL,
    `role_id` BIGINT UNSIGNED NOT NULL,
    `assigned_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_user_role` (`user_id`, `role_id`),
    CONSTRAINT `fk_user_roles_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_roles_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Bảng user_sessions: Phiên đăng nhập & token thu hồi
DROP TABLE IF EXISTS `user_sessions`;
CREATE TABLE `user_sessions` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL,
    `session_token` VARCHAR(255) NOT NULL UNIQUE,
    `ip_address` VARCHAR(45) NULL,
    `user_agent` VARCHAR(255) NULL,
    `is_revoked` TINYINT(1) NOT NULL DEFAULT 0,
    `expires_at` DATETIME(6) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    INDEX `idx_sessions_user` (`user_id`),
    INDEX `idx_sessions_token` (`session_token`),
    CONSTRAINT `fk_user_sessions_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Bảng departments: Khoa / Viện đào tạo
DROP TABLE IF EXISTS `departments`;
CREATE TABLE `departments` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `department_code` VARCHAR(50) NOT NULL UNIQUE,
    `department_name` VARCHAR(150) NOT NULL,
    `description` VARCHAR(255) NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Bảng administrative_classes: Lớp hành chính / sinh hoạt
DROP TABLE IF EXISTS `administrative_classes`;
CREATE TABLE `administrative_classes` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `class_code` VARCHAR(50) NOT NULL UNIQUE,
    `class_name` VARCHAR(150) NOT NULL,
    `department_id` BIGINT UNSIGNED NOT NULL,
    `academic_year` VARCHAR(20) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_admin_classes_dept` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Bảng students: Thông tin sinh viên
DROP TABLE IF EXISTS `students`;
CREATE TABLE `students` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL UNIQUE,
    `student_code` VARCHAR(50) NOT NULL UNIQUE,
    `administrative_class_id` BIGINT UNSIGNED NOT NULL,
    `department_id` BIGINT UNSIGNED NOT NULL,
    `date_of_birth` DATE NULL,
    `gender` ENUM('MALE', 'FEMALE', 'OTHER') NOT NULL DEFAULT 'MALE',
    `academic_status` ENUM('STUDYING', 'SUSPENDED', 'DROPPED_OUT', 'GRADUATED') NOT NULL DEFAULT 'STUDYING',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    INDEX `idx_students_code` (`student_code`),
    CONSTRAINT `fk_students_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_students_admin_class` FOREIGN KEY (`administrative_class_id`) REFERENCES `administrative_classes` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_students_dept` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Bảng lecturers: Thông tin giảng viên
DROP TABLE IF EXISTS `lecturers`;
CREATE TABLE `lecturers` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL UNIQUE,
    `lecturer_code` VARCHAR(50) NOT NULL UNIQUE,
    `department_id` BIGINT UNSIGNED NOT NULL,
    `academic_degree` VARCHAR(50) NULL,
    `status` ENUM('ACTIVE', 'ON_LEAVE', 'RETIRED') NOT NULL DEFAULT 'ACTIVE',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    INDEX `idx_lecturers_code` (`lecturer_code`),
    CONSTRAINT `fk_lecturers_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_lecturers_dept` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Bảng subjects: Môn học
DROP TABLE IF EXISTS `subjects`;
CREATE TABLE `subjects` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `subject_code` VARCHAR(50) NOT NULL UNIQUE,
    `subject_name` VARCHAR(150) NOT NULL,
    `credits` INT NOT NULL DEFAULT 3,
    `department_id` BIGINT UNSIGNED NOT NULL,
    `description` TEXT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_subjects_dept` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. Bảng semesters: Học kỳ
DROP TABLE IF EXISTS `semesters`;
CREATE TABLE `semesters` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `semester_code` VARCHAR(50) NOT NULL UNIQUE,
    `semester_name` VARCHAR(100) NOT NULL,
    `academic_year` VARCHAR(20) NOT NULL,
    `start_date` DATE NOT NULL,
    `end_date` DATE NOT NULL,
    `is_active` TINYINT(1) NOT NULL DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. Bảng classrooms: Phòng học
DROP TABLE IF EXISTS `classrooms`;
CREATE TABLE `classrooms` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `room_code` VARCHAR(50) NOT NULL UNIQUE,
    `building` VARCHAR(50) NOT NULL,
    `capacity` INT NOT NULL DEFAULT 60,
    `room_type` ENUM('LECTURE_HALL', 'LAB', 'NORMAL') NOT NULL DEFAULT 'NORMAL',
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. Bảng class_sections: Lớp học phần
DROP TABLE IF EXISTS `class_sections`;
CREATE TABLE `class_sections` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `section_code` VARCHAR(50) NOT NULL UNIQUE,
    `subject_id` BIGINT UNSIGNED NOT NULL,
    `semester_id` BIGINT UNSIGNED NOT NULL,
    `lecturer_id` BIGINT UNSIGNED NOT NULL,
    `max_capacity` INT NOT NULL DEFAULT 60,
    `current_enrollment` INT NOT NULL DEFAULT 0,
    `status` ENUM('PLANNING', 'ACTIVE', 'COMPLETED', 'CANCELLED') NOT NULL DEFAULT 'ACTIVE',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_sections_subject` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_sections_semester` FOREIGN KEY (`semester_id`) REFERENCES `semesters` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_sections_lecturer` FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 13. Bảng enrollments: Sinh viên đăng ký lớp học phần
DROP TABLE IF EXISTS `enrollments`;
CREATE TABLE `enrollments` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `student_id` BIGINT UNSIGNED NOT NULL,
    `class_section_id` BIGINT UNSIGNED NOT NULL,
    `enrollment_status` ENUM('ENROLLED', 'DROPPED', 'WITHDRAWN') NOT NULL DEFAULT 'ENROLLED',
    `registered_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_student_section` (`student_id`, `class_section_id`),
    CONSTRAINT `fk_enrollments_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_enrollments_section` FOREIGN KEY (`class_section_id`) REFERENCES `class_sections` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 14. Bảng schedules: Lịch học các lớp học phần
DROP TABLE IF EXISTS `schedules`;
CREATE TABLE `schedules` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `class_section_id` BIGINT UNSIGNED NOT NULL,
    `classroom_id` BIGINT UNSIGNED NOT NULL,
    `day_of_week` ENUM('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY') NOT NULL,
    `start_time` TIME NOT NULL,
    `end_time` TIME NOT NULL,
    `start_date` DATE NOT NULL,
    `end_date` DATE NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_schedules_section` FOREIGN KEY (`class_section_id`) REFERENCES `class_sections` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_schedules_classroom` FOREIGN KEY (`classroom_id`) REFERENCES `classrooms` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 15. Bảng schedule_change_logs: Lịch sử thay đổi / bù lịch
DROP TABLE IF EXISTS `schedule_change_logs`;
CREATE TABLE `schedule_change_logs` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `schedule_id` BIGINT UNSIGNED NOT NULL,
    `changed_by_user_id` BIGINT UNSIGNED NOT NULL,
    `change_type` ENUM('CLASSROOM_CHANGED', 'TIME_CHANGED', 'MAKEUP_CLASS', 'CANCELLED') NOT NULL,
    `old_values` JSON NULL,
    `new_values` JSON NULL,
    `reason` VARCHAR(255) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_change_logs_schedule` FOREIGN KEY (`schedule_id`) REFERENCES `schedules` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_change_logs_user` FOREIGN KEY (`changed_by_user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 16. Bảng face_profiles: Hồ sơ sinh trắc học khuôn mặt
DROP TABLE IF EXISTS `face_profiles`;
CREATE TABLE `face_profiles` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `student_id` BIGINT UNSIGNED NOT NULL UNIQUE,
    `encrypted_template` MEDIUMBLOB NOT NULL,
    `model_name` VARCHAR(100) NOT NULL DEFAULT 'insightface/buffalo_l',
    `model_version` VARCHAR(50) NOT NULL DEFAULT '1.0',
    `encryption_key_version` VARCHAR(50) NOT NULL DEFAULT 'v1',
    `consent_version` VARCHAR(50) NOT NULL DEFAULT 'gdpr_biometric_v1',
    `quality_score` FLOAT NOT NULL DEFAULT 0.0,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_face_profiles_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 17. Bảng attendance_sessions: Phiên điểm danh theo buổi học
DROP TABLE IF EXISTS `attendance_sessions`;
CREATE TABLE `attendance_sessions` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `class_section_id` BIGINT UNSIGNED NOT NULL,
    `schedule_id` BIGINT UNSIGNED NULL,
    `lecturer_id` BIGINT UNSIGNED NOT NULL,
    `session_code` VARCHAR(50) NOT NULL UNIQUE,
    `session_date` DATE NOT NULL,
    `start_time` DATETIME(6) NOT NULL,
    `end_time` DATETIME(6) NULL,
    `session_status` ENUM('OPEN', 'CLOSED', 'CANCELLED') NOT NULL DEFAULT 'OPEN',
    `grace_period_minutes` INT NOT NULL DEFAULT 15,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    INDEX `idx_sessions_status` (`session_status`),
    CONSTRAINT `fk_att_sessions_section` FOREIGN KEY (`class_section_id`) REFERENCES `class_sections` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_att_sessions_schedule` FOREIGN KEY (`schedule_id`) REFERENCES `schedules` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_att_sessions_lecturer` FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 18. Bảng attendance_records: Kết quả điểm danh sinh viên
DROP TABLE IF EXISTS `attendance_records`;
CREATE TABLE `attendance_records` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `attendance_session_id` BIGINT UNSIGNED NOT NULL,
    `student_id` BIGINT UNSIGNED NOT NULL,
    `attendance_status` ENUM('PRESENT', 'LATE', 'ABSENT', 'EXCUSED', 'NEEDS_REVIEW') NOT NULL DEFAULT 'ABSENT',
    `check_in_time` DATETIME(6) NULL,
    `device_info` VARCHAR(255) NULL,
    `verification_method` ENUM('AI_FACE', 'MANUAL_LECTURER', 'ADJUSTMENT') NOT NULL DEFAULT 'AI_FACE',
    `confidence_score` FLOAT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_session_student` (`attendance_session_id`, `student_id`),
    INDEX `idx_att_records_status` (`attendance_status`),
    CONSTRAINT `fk_att_records_session` FOREIGN KEY (`attendance_session_id`) REFERENCES `attendance_sessions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_att_records_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 19. Bảng recognition_attempts: Lịch sử nhận diện AI
DROP TABLE IF EXISTS `recognition_attempts`;
CREATE TABLE `recognition_attempts` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `attendance_session_id` BIGINT UNSIGNED NOT NULL,
    `student_id` BIGINT UNSIGNED NULL,
    `attempt_status` ENUM('SUCCESS', 'FAILED_NO_FACE', 'FAILED_MULTIPLE_FACES', 'FAILED_LOW_CONFIDENCE', 'FAILED_SPOOF_SUSPECTED', 'FAILED_NOT_ENROLLED') NOT NULL,
    `similarity_score` FLOAT NULL,
    `failure_reason` VARCHAR(255) NULL,
    `ip_address` VARCHAR(45) NULL,
    `attempt_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_recog_session` FOREIGN KEY (`attendance_session_id`) REFERENCES `attendance_sessions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_recog_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 20. Bảng attendance_adjustments: Lịch sử điều chỉnh điểm danh
DROP TABLE IF EXISTS `attendance_adjustments`;
CREATE TABLE `attendance_adjustments` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `attendance_record_id` BIGINT UNSIGNED NOT NULL,
    `adjusted_by_user_id` BIGINT UNSIGNED NOT NULL,
    `previous_status` ENUM('PRESENT', 'LATE', 'ABSENT', 'EXCUSED', 'NEEDS_REVIEW') NOT NULL,
    `new_status` ENUM('PRESENT', 'LATE', 'ABSENT', 'EXCUSED', 'NEEDS_REVIEW') NOT NULL,
    `reason` TEXT NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_adjustments_record` FOREIGN KEY (`attendance_record_id`) REFERENCES `attendance_records` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_adjustments_user` FOREIGN KEY (`adjusted_by_user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 21. Bảng audit_logs: Nhật ký kiểm toán toàn hệ thống
DROP TABLE IF EXISTS `audit_logs`;
CREATE TABLE `audit_logs` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NULL,
    `action` VARCHAR(100) NOT NULL,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` VARCHAR(50) NULL,
    `details` JSON NULL,
    `ip_address` VARCHAR(45) NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    INDEX `idx_audit_user` (`user_id`),
    INDEX `idx_audit_action` (`action`),
    CONSTRAINT `fk_audit_logs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 22. Bảng email_otps (Bổ sung qua Migration): Mã OTP xác thực email / đổi mật khẩu
DROP TABLE IF EXISTS `email_otps`;
CREATE TABLE `email_otps` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL,
    `otp_hash` VARCHAR(255) NOT NULL,
    `purpose` ENUM('REGISTRATION', 'RESET_PASSWORD', 'LOGIN_VERIFICATION') NOT NULL DEFAULT 'REGISTRATION',
    `expires_at` DATETIME(6) NOT NULL,
    `attempts` INT NOT NULL DEFAULT 0,
    `consumed_at` DATETIME(6) NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`),
    INDEX `idx_email_otps_user` (`user_id`),
    CONSTRAINT `fk_email_otps_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
