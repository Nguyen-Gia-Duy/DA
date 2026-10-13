# FACEATTEND ENTERPRISE – HỆ THỐNG QUẢN LÝ SINH VIÊN VÀ ĐIỂM DANH TỰ ĐỘNG BẰNG NHẬN DIỆN KHUÔN MẶT AI

> **Đồ án tốt nghiệp ngành Công nghệ Thông tin**  
> **Kiến trúc:** ReactJS (TypeScript) + FastAPI + SQLAlchemy 2.x + MySQL + OpenCV + InsightFace (ArcFace 512D) + AES-256 GCM + SMTP Gmail OTP.

---

## I. TỔNG QUAN HỆ THỐNG

**FaceAttend Enterprise** là giải pháp điểm danh sinh viên tự động ứng dụng Trí tuệ Nhân tạo và Thị giác Máy tính (AI Computer Vision) dành cho các trường đại học và cơ sở giáo dục. Hệ thống giải quyết triệt để các vấn đề của phương pháp điểm danh truyền thống (tốn thời gian, điểm danh hộ, sai sót dữ liệu) thông qua:

1. **Nhận diện khuôn mặt thời gian thực**: Trích xuất vector đặc trưng sinh trắc học 512 chiều (L2-normalized embedding) bằng mạng nơ-ron sâu ArcFace/InsightFace chạy trên ONNX Runtime.
2. **Đăng ký đa góc mặt tự động (Multi-pose Auto-capture)**: Tự động phát hiện và chụp 3 góc độ: **Trực diện (Frontal)**, **Quay trái (Left)**, **Quay phải (Right)** với kiểm tra chất lượng ảnh (độ nét Laplacian, ánh sáng, góc nghiêng).
3. **Bảo mật sinh trắc học cấp Enterprise**: Không lưu trữ ảnh khuôn mặt gốc lâu dài. Mẫu đặc trưng được mã hóa nhị phân bằng thuật toán **AES-256 GCM** trước khi lưu vào bảng `face_profiles.encrypted_template`.
4. **Xác thực OTP qua Gmail SMTP**: Sinh viên kích hoạt tài khoản và đặt lại mật khẩu bằng mã OTP 6 chữ số gửi qua Gmail, băm bảo mật SHA-256 HMAC, giới hạn 5 lần thử và hết hạn sau 10 phút.
5. **Chạy chung cổng 8000 duy nhất**: FastAPI phục vụ trực tiếp Single Page Application (SPA) React tại `/`, các API tại `/api` và tài liệu tương tác tại `/docs`.

---

## II. DANH MỤC 21 BẢNG MYSQL CỐT LÕI & BẢNG MIGRATION

Toàn bộ 21 bảng được ánh xạ 1:1 sang 21 file model SQLAlchemy riêng biệt trong `backend/app/models/`:

| STT | Tên bảng MySQL | File Model Python | Chức năng nghiệp vụ |
|:---:|:---|:---|:---|
| 1 | `roles` | `role.py` | Vai trò hệ thống: `ADMIN`, `LECTURER`, `STUDENT` |
| 2 | `users` | `user.py` | Tài khoản, mật khẩu băm Bcrypt, trạng thái `ACTIVE`, `PENDING`... |
| 3 | `user_roles` | `user_role.py` | Liên kết nhiều vai trò cho tài khoản |
| 4 | `user_sessions` | `user_session.py` | Quản lý phiên làm việc JWT và thu hồi token |
| 5 | `departments` | `department.py` | Khoa / Viện quản lý đào tạo |
| 6 | `administrative_classes` | `administrative_class.py` | Lớp hành chính / sinh hoạt niên khóa |
| 7 | `students` | `student.py` | Hồ sơ sinh viên, mã MSSV duy nhất, lớp, khoa |
| 8 | `lecturers` | `lecturer.py` | Hồ sơ giảng viên, học hàm / học vị |
| 9 | `subjects` | `subject.py` | Danh mục môn học, số tín chỉ |
| 10 | `semesters` | `semester.py` | Học kỳ đào tạo, ngày bắt đầu / kết thúc |
| 11 | `classrooms` | `classroom.py` | Phòng học, tòa nhà, sức chứa |
| 12 | `class_sections` | `class_section.py` | Lớp học phần, giảng viên phụ trách, sĩ số tối đa |
| 13 | `enrollments` | `enrollment.py` | Sinh viên đăng ký lớp học phần |
| 14 | `schedules` | `schedule.py` | Lịch học trong tuần, khung giờ, phòng học |
| 15 | `schedule_change_logs` | `schedule_change_log.py` | Nhật ký đổi phòng, đổi giờ, học bù |
| 16 | `face_profiles` | `face_profile.py` | Vector khuôn mặt mã hóa `MEDIUMBLOB` (AES-256 GCM) |
| 17 | `attendance_sessions` | `attendance_session.py` | Phiên điểm danh theo buổi học (`OPEN`, `CLOSED`) |
| 18 | `attendance_records` | `attendance_record.py` | Kết quả điểm danh: `PRESENT`, `LATE`, `ABSENT`... |
| 19 | `recognition_attempts` | `recognition_attempt.py` | Lịch sử nỗ lực nhận diện AI, lý do thất bại |
| 20 | `attendance_adjustments` | `attendance_adjustment.py` | Lịch sử giảng viên điều chỉnh kết quả thủ công |
| 21 | `audit_logs` | `audit_log.py` | Nhật ký kiểm toán bảo mật toàn hệ thống |
| 22 | `email_otps` | `email_otp.py` | **Bổ sung qua Alembic Migration**: Lưu mã OTP 6 chữ số băm SHA-256 HMAC |

### Lý do bổ sung Migration:
- **`backend/alembic/versions/0001_add_email_otps_and_pending_status.py`**:
  1. Thêm bảng `email_otps` để lưu mã OTP đăng ký / quên mật khẩu mà không làm thay đổi các bảng hiện tại.
  2. Bổ sung giá trị `PENDING` vào ENUM `account_status` của bảng `users` nhằm đáp ứng quy trình sinh viên đăng ký chờ kích hoạt Gmail OTP.

---

## III. HƯỚNG DẪN CÀI ĐẶT & CHẠY TRÊN MACOS

### 1. Yêu cầu môi trường
- macOS 12.0+ (Apple Silicon M1/M2/M3 hoặc Intel).
- Python 3.11 hoặc 3.12 (`brew install python@3.11`).
- Node.js 18+ & npm (`brew install node`).
- MySQL 8.x đang chạy (`brew install mysql` hoặc MySQL Workbench).

### 2. Khởi tạo Cơ sở Dữ liệu MySQL
Mở MySQL Workbench hoặc Terminal và chạy lệnh nạp dữ liệu:
```bash
# Nạp cấu trúc 21 bảng
mysql -u root -p < database/faceattend_schema.sql

# Nạp dữ liệu mẫu seed data
mysql -u root -p < database/seed_data.sql
```

### 3. Cấu hình biến môi trường (`.env`)
Tạo file `backend/.env` từ file mẫu:
```bash
cp backend/.env.example backend/.env
```
Cập nhật thông tin kết nối MySQL và Gmail trong `backend/.env`:
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=Mật_khẩu_mysql_của_bạn
MYSQL_DATABASE=faceattend

# Cấu hình Gmail App Password để gửi OTP thật
SMTP_USER=nguyengiaduy2005@gmail.com
SMTP_PASSWORD=Mật_khẩu_ứng_dụng_16_ký_tự_từ_Google
```

### 4. Khởi chạy 1 lệnh duy nhất (Phục vụ chung Cổng 8000)
Chạy script tự động hóa đi kèm:
```bash
./scripts/run_app.sh
```
Script sẽ tự động:
1. Tạo môi trường ảo Python `backend/venv` và kích hoạt.
2. Cài đặt thư viện từ `backend/requirements.txt`.
3. Build mã nguồn React TypeScript thành thư mục `dist`.
4. Khởi chạy máy chủ FastAPI phục vụ toàn bộ trên cổng **8000**.

Truy cập trình duyệt:
- **Giao diện ứng dụng**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Tài liệu Swagger API**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Tài liệu ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## IV. TÀI KHOẢN MẪU ĐỂ ĐÁNH GIÁ ĐỒ ÁN

Hệ thống đã tích hợp sẵn thanh chuyển vai trò nhanh (**Persona Switcher**) ở góc trên bên phải để người chấm đồ án có thể đổi ngay giữa 3 phân hệ:

| Vai trò | Tên đăng nhập | Email | Mật khẩu mặc định | Quyền hạn |
|:---|:---|:---|:---|:---|
| **ADMIN** | `admin` | `admin@faceattend.edu.vn` | `Admin@123` | Quản trị toàn hệ thống, danh mục, kiểm toán |
| **LECTURER** | `gv.an.nguyen` | `an.nguyen@faceattend.edu.vn` | `Lecturer@123` | Quản lý lớp học phần, mở/đóng phiên điểm danh |
| **STUDENT** | `sv.b20dccn001` | `nguyengiaduy2005@gmail.com` | `Student@123` | Đăng ký khuôn mặt AI 3 góc, điểm danh camera |

---

## V. CÁCH LẤY GMAIL APP PASSWORD ĐỂ GỬI OTP

1. Đăng nhập tài khoản Google của bạn.
2. Vào **Bảo mật (Security)** -> Bật **Xác thực 2 bước (2-Step Verification)** nếu chưa bật.
3. Tìm kiếm **Mật khẩu ứng dụng (App passwords)**: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
4. Đặt tên ứng dụng là `FaceAttend Enterprise`.
5. Google sẽ cấp mã 16 ký tự (VD: `abcd efgh ijkl mnop`).
6. Dán mã này vào biến `SMTP_PASSWORD` trong file `backend/.env`.

---

## VI. QUY TRÌNH ĐIỂM DANH & NHẬN DIỆN KHUÔN MẶT AI

```text
[Giảng viên]                                      [Sinh viên]
     │                                                 │
     ├─► Chọn lớp học phần INT1340-01                  │
     ├─► Nhấn "Khởi tạo & Mở phiên"                    │
     ├─► Nhận Session Code: SES-TODAY-INT1340-01       │
     │   (Hệ thống tạo sẵn bản ghi ABSENT)             │
     │                                                 │
     │                                                 ├─► Nhập mã phiên SES-TODAY-INT1340-01
     │                                                 ├─► Mở Camera nhận diện
     │                                                 ├─► Kiểm tra 1 khuôn mặt & độ nét
     │                                                 ├─► InsightFace trích xuất Embedding
     │                                                 ├─► Giải mã Template (AES-256 GCM)
     │                                                 ├─► Tính Cosine Similarity >= 0.60
     │                                                 ├─► Cập nhật: PRESENT hoặc LATE
     │                                                 └─► Ghi nhận attempt vào database
     │                                                 
     ├─► Bảng Live Monitor tự động nhảy trạng thái ───► Có mặt (95.0%)
     └─► Nhấn "Đóng phiên điểm danh"
```

---

## VII. BẢO MẬT & BẢO TOÀN DỮ LIỆU
- Mọi mật khẩu người dùng được băm bằng thuật toán **Bcrypt** với salt ngẫu nhiên.
- Mọi mã OTP xác thực email được băm bằng thuật toán **SHA-256 HMAC**.
- Mẫu sinh trắc học được mã hóa bằng **AES-256 GCM** chuẩn NIST.
- Cơ chế chống gian lận kiểm tra phân tích tần số Fourier và ràng buộc duy nhất 1 khuôn mặt.
- Mọi biến đổi dữ liệu điểm danh thủ công đều phải lưu lý do điều chỉnh vào `attendance_adjustments` và ghi vết vào `audit_logs`.
