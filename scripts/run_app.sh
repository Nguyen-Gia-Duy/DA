#!/bin/bash
# =====================================================================
# FACEATTEND ENTERPRISE - SCRIPT KHỞI ĐỘNG HỆ THỐNG TRÊN MACOS / LINUX
# Tự động Build Frontend và Phục vụ toàn bộ hệ thống trên Port 8000
# http://127.0.0.1:8000
# =====================================================================

set -e

echo "====================================================================="
echo "   FACEATTEND ENTERPRISE - HỆ THỐNG ĐIỂM DANH KHUÔN MẶT AI"
echo "====================================================================="

# 1. Kiểm tra môi trường Node.js & npm
if ! command -v npm &> /dev/null; then
    echo "❌ Lỗi: Chưa cài đặt Node.js / npm. Vui lòng cài đặt qua 'brew install node'."
    exit 1
fi

# 2. Kiểm tra Python 3
PYTHON_CMD="python3"
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Lỗi: Chưa tìm thấy Python 3. Vui lòng cài đặt qua 'brew install python@3.11'."
    exit 1
fi

# 3. Tạo virtual environment nếu chưa có
if [ ! -d "backend/venv" ]; then
    echo "📦 Đang khởi tạo môi trường ảo Python venv tại backend/venv..."
    $PYTHON_CMD -m venv backend/venv
fi

# Kích hoạt venv
source backend/venv/bin/activate
echo "✅ Đã kích hoạt môi trường ảo: $(python --version)"

# 4. Cài đặt các gói phụ thuộc Backend
echo "📦 Đang cài đặt thư viện Python từ backend/requirements.txt..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# 5. Cấu hình file .env
if [ ! -f "backend/.env" ]; then
    echo "⚙️  Chưa tìm thấy backend/.env. Đang sao chép từ backend/.env.example..."
    cp backend/.env.example backend/.env
    echo "⚠️  Vui lòng cấu hình mật khẩu MySQL và Gmail App Password trong backend/.env nếu cần!"
fi

# 6. Build Frontend React thành thư mục dist
echo "🔨 Đang Build giao diện Frontend React (Vite)..."
npm install
npm run build
echo "✅ Build Frontend thành công! Thư mục 'dist' đã sẵn sàng."

# 7. Khởi động FastAPI Server trên cổng 8000
echo "====================================================================="
echo "🚀 Đang khởi động hệ thống FaceAttend Enterprise trên Cổng 8000..."
echo "👉 Giao diện ứng dụng:  http://127.0.0.1:8000"
echo "👉 Tài liệu Swagger API: http://127.0.0.1:8000/docs"
echo "👉 API ReDoc:            http://127.0.0.1:8000/redoc"
echo "====================================================================="

uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
