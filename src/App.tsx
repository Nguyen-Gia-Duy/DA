import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { RoleName } from './types';
import MainLayout from './layouts/MainLayout';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import VerifyOtpPage from './pages/auth/VerifyOtpPage';
import AdminDashboardPage from './pages/admin/AdminDashboardPage';
import StudentsManagementPage from './pages/admin/StudentsManagementPage';
import LecturersManagementPage from './pages/admin/LecturersManagementPage';
import AcademicManagementPage from './pages/admin/AcademicManagementPage';
import SessionsManagementPage from './pages/admin/SessionsManagementPage';
import RecognitionAttemptsPage from './pages/admin/RecognitionAttemptsPage';
import AuditLogsPage from './pages/admin/AuditLogsPage';
import LecturerDashboardPage from './pages/lecturer/LecturerDashboardPage';
import LiveAttendancePage from './pages/lecturer/LiveAttendancePage';
import StudentDashboardPage from './pages/student/StudentDashboardPage';
import FaceRegistrationPage from './pages/student/FaceRegistrationPage';
import FaceCheckInPage from './pages/student/FaceCheckInPage';
import StudentHistoryPage from './pages/student/StudentHistoryPage';
import { NotFoundPage } from './pages/NotFoundPage';
import { ShieldAlert } from 'lucide-react';

// Thành phần bảo vệ định tuyến (Role-Based Route Guard)
interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: RoleName[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, allowedRoles }) => {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col items-center justify-center p-4">
        <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4" />
        <p className="text-xs font-semibold text-slate-500 dark:text-slate-400">
          Đang xác thực phiên làm việc FaceAttend Enterprise...
        </p>
      </div>
    );
  }

  // 1. Chưa đăng nhập -> Chuyển về /login
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // 2. Kiểm tra quyền hạn theo vai trò (Roles)
  if (allowedRoles && allowedRoles.length > 0) {
    const hasPermission = allowedRoles.some((role) => user.roles.includes(role));
    if (!hasPermission) {
      // Điều hướng về dashboard phù hợp với vai trò của tài khoản
      if (user.roles.includes('ADMIN')) {
        return <Navigate to="/admin/dashboard" replace />;
      } else if (user.roles.includes('LECTURER')) {
        return <Navigate to="/lecturer/dashboard" replace />;
      } else if (user.roles.includes('STUDENT')) {
        return <Navigate to="/student/dashboard" replace />;
      } else {
        return (
          <div className="p-8 max-w-md mx-auto my-16 bg-white dark:bg-slate-900 rounded-3xl border border-red-200 dark:border-red-900/60 p-6 text-center shadow-lg">
            <ShieldAlert className="w-12 h-12 text-red-500 mx-auto mb-3" />
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">Không có quyền truy cập</h2>
            <p className="text-xs text-slate-500 mt-2">
              Tài khoản của bạn không được phân quyền để truy cập trang này. Vui lòng liên hệ Quản trị viên.
            </p>
          </div>
        );
      }
    }
  }

  return <>{children}</>;
};

// Điều hướng trang chủ dựa trên vai trò thực tế của người dùng
const RoleBasedRedirect: React.FC = () => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.roles.includes('ADMIN')) {
    return <Navigate to="/admin/dashboard" replace />;
  } else if (user.roles.includes('LECTURER')) {
    return <Navigate to="/lecturer/dashboard" replace />;
  } else {
    return <Navigate to="/student/dashboard" replace />;
  }
};

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Auth Routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/verify-otp" element={<VerifyOtpPage />} />

          {/* Root Redirector */}
          <Route path="/" element={<RoleBasedRedirect />} />

          {/* Protected Routes inside MainLayout */}
          <Route element={<MainLayout />}>
            {/* Admin Exclusive Routes */}
            <Route
              path="/admin/dashboard"
              element={
                <ProtectedRoute allowedRoles={['ADMIN']}>
                  <AdminDashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/students"
              element={
                <ProtectedRoute allowedRoles={['ADMIN']}>
                  <StudentsManagementPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/lecturers"
              element={
                <ProtectedRoute allowedRoles={['ADMIN']}>
                  <LecturersManagementPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/academic"
              element={
                <ProtectedRoute allowedRoles={['ADMIN']}>
                  <AcademicManagementPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/sessions"
              element={
                <ProtectedRoute allowedRoles={['ADMIN']}>
                  <SessionsManagementPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/recognition-attempts"
              element={
                <ProtectedRoute allowedRoles={['ADMIN']}>
                  <RecognitionAttemptsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/audit-logs"
              element={
                <ProtectedRoute allowedRoles={['ADMIN']}>
                  <AuditLogsPage />
                </ProtectedRoute>
              }
            />

            {/* Lecturer Exclusive Routes */}
            <Route
              path="/lecturer/dashboard"
              element={
                <ProtectedRoute allowedRoles={['LECTURER', 'ADMIN']}>
                  <LecturerDashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/lecturer/sections"
              element={
                <ProtectedRoute allowedRoles={['LECTURER', 'ADMIN']}>
                  <AcademicManagementPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/lecturer/live-attendance"
              element={
                <ProtectedRoute allowedRoles={['LECTURER', 'ADMIN']}>
                  <LiveAttendancePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/lecturer/schedules"
              element={
                <ProtectedRoute allowedRoles={['LECTURER', 'ADMIN']}>
                  <AcademicManagementPage />
                </ProtectedRoute>
              }
            />

            {/* Student Exclusive Routes */}
            <Route
              path="/student/dashboard"
              element={
                <ProtectedRoute allowedRoles={['STUDENT', 'ADMIN']}>
                  <StudentDashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/student/register-face"
              element={
                <ProtectedRoute allowedRoles={['STUDENT', 'ADMIN']}>
                  <FaceRegistrationPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/student/check-in"
              element={
                <ProtectedRoute allowedRoles={['STUDENT', 'ADMIN']}>
                  <FaceCheckInPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/student/history"
              element={
                <ProtectedRoute allowedRoles={['STUDENT', 'ADMIN']}>
                  <StudentHistoryPage />
                </ProtectedRoute>
              }
            />
          </Route>

          {/* 404 Catch-all */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
