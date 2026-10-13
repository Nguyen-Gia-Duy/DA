import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import logging

from backend.app.core.config import settings
from backend.app.core.database import check_db_connection
from backend.app.routes.auth_routes import router as auth_router
from backend.app.routes.academic_routes import router as academic_router
from backend.app.routes.attendance_routes import router as attendance_router
from backend.app.routes.dashboard_routes import router as dashboard_router
from backend.app.routes.audit_routes import router as audit_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Khởi động FaceAttend Enterprise API Server...")
    is_connected = check_db_connection()
    if is_connected:
        logger.info("Kết nối MySQL 'faceattend' thành công.")
    else:
        logger.warning("Cảnh báo: Chưa thể kết nối MySQL 'faceattend'. Vui lòng kiểm tra thông tin trong .env.")
    yield
    logger.info("Dừng FaceAttend Enterprise API Server.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Hệ thống Quản lý Sinh viên và Điểm danh Tự động bằng Nhận diện Khuôn mặt AI (Đồ án tốt nghiệp CNTT)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các nhóm API Route dưới tiền tố /api
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(academic_router, prefix=settings.API_V1_STR)
app.include_router(attendance_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(audit_router, prefix=settings.API_V1_STR)

@app.get("/api/health", tags=["Hệ thống"])
def health_check():
    db_ok = check_db_connection()
    return {
        "status": "healthy" if db_ok else "database_disconnected",
        "app": settings.PROJECT_NAME,
        "database": "connected" if db_ok else "error",
        "version": "1.0.0"
    }

# Phục vụ Single Page Application (SPA) React từ thư mục `dist` trên cổng 8000
FRONTEND_DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../dist"))
ASSETS_DIR = os.path.join(FRONTEND_DIST_DIR, "assets")

if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa_frontend(request: Request, full_path: str):
    """
    SPA Fallback: Bất kỳ URL nào không bắt đầu bằng /api hoặc /docs sẽ trả về index.html của React.
    Đảm bảo React Router hoạt động mượt mà khi refresh trang trên cổng 8000.
    """
    if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("redoc"):
        return JSONResponse(status_code=404, content={"detail": "API endpoint not found"})

    index_html = os.path.join(FRONTEND_DIST_DIR, "index.html")
    if os.path.exists(index_html):
        return FileResponse(index_html)
    return JSONResponse(
        status_code=200,
        content={
            "message": "FaceAttend Enterprise API Server đang chạy trên cổng 8000.",
            "docs": "/docs",
            "frontend_status": "Vui lòng chạy 'npm run build' để tạo thư mục dist/ nếu muốn phục vụ giao diện React qua cổng này."
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
