import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  LayoutDashboard,
  Users,
  GraduationCap,
  BookOpen,
  Calendar,
  Camera,
  CheckCircle2,
  FileText,
  Clock,
  ShieldCheck,
  History,
  Layers,
  Settings,
  HelpCircle,
} from 'lucide-react';

interface NavItem {
  name: string;
  path: string;
  icon: React.ReactNode;
}

export const Sidebar: React.FC = () => {
  const { activeRole } = useAuth();

  const getNavItems = (): NavItem[] => {
    switch (activeRole) {
      case 'ADMIN':
        return [
          { name: 'Dashboard Tổng quan', path: '/admin/dashboard', icon: <LayoutDashboard className="w-5 h-5" /> },
          { name: 'Quản lý Sinh viên', path: '/admin/students', icon: <GraduationCap className="w-5 h-5" /> },
          { name: 'Quản lý Giảng viên', path: '/admin/lecturers', icon: <Users className="w-5 h-5" /> },
          { name: 'Quản lý Đào tạo', path: '/admin/academic', icon: <BookOpen className="w-5 h-5" /> },
          { name: 'Phiên điểm danh', path: '/admin/sessions', icon: <CheckCircle2 className="w-5 h-5" /> },
          { name: 'Nhận diện AI & Log', path: '/admin/recognition-attempts', icon: <History className="w-5 h-5" /> },
          { name: 'Nhật ký Kiểm toán', path: '/admin/audit-logs', icon: <FileText className="w-5 h-5" /> },
        ];
      case 'LECTURER':
        return [
          { name: 'Dashboard Giảng viên', path: '/lecturer/dashboard', icon: <LayoutDashboard className="w-5 h-5" /> },
          { name: 'Lớp học phần phụ trách', path: '/lecturer/sections', icon: <Layers className="w-5 h-5" /> },
          { name: 'Phiên điểm danh Trực tiếp', path: '/lecturer/live-attendance', icon: <Camera className="w-5 h-5" /> },
          { name: 'Lịch giảng dạy', path: '/lecturer/schedules', icon: <Calendar className="w-5 h-5" /> },
        ];
      case 'STUDENT':
      default:
        return [
          { name: 'Dashboard Sinh viên', path: '/student/dashboard', icon: <LayoutDashboard className="w-5 h-5" /> },
          { name: 'Đăng ký Khuôn mặt AI', path: '/student/register-face', icon: <Camera className="w-5 h-5" /> },
          { name: 'Điểm danh Trực tiếp', path: '/student/check-in', icon: <CheckCircle2 className="w-5 h-5" /> },
          { name: 'Lịch sử & Chuyên cần', path: '/student/history', icon: <Clock className="w-5 h-5" /> },
        ];
    }
  };

  const navItems = getNavItems();

  return (
    <aside className="w-64 shrink-0 bg-slate-50 dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col justify-between p-4 h-[calc(100vh-4rem)] sticky top-16 overflow-y-auto">
      <div className="space-y-6">
        <div>
          <div className="px-3 mb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
            {activeRole === 'ADMIN' ? 'HỆ THỐNG QUẢN TRỊ' : activeRole === 'LECTURER' ? 'GIẢNG VIÊN ĐÀO TẠO' : 'CỔNG SINH VIÊN'}
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/30'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white'
                  }`
                }
              >
                {item.icon}
                <span>{item.name}</span>
              </NavLink>
            ))}
          </nav>
        </div>
      </div>

      {/* Database & Technology Card */}
      <div className="mt-6 p-3.5 rounded-xl bg-blue-50/70 dark:bg-slate-800/80 border border-blue-100 dark:border-slate-700/60">
        <div className="flex items-center gap-2 text-xs font-semibold text-blue-900 dark:text-blue-300">
          <ShieldCheck className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          <span>MySQL & AI Vision</span>
        </div>
        <p className="mt-1 text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
          InsightFace + ArcFace 512D. Mã hóa AES-256 GCM. 21 bảng quan hệ chuẩn.
        </p>
      </div>
    </aside>
  );
};

export default Sidebar;
