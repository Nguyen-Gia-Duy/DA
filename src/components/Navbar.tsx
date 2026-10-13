import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { LogOut, User as UserIcon, Shield, GraduationCap, School } from 'lucide-react';
import { RoleName } from '../types';

export const Navbar: React.FC = () => {
  const { user, activeRole, logout } = useAuth();

  const getRoleBadge = (role: RoleName | null) => {
    switch (role) {
      case 'ADMIN':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300">
            <Shield className="w-3.5 h-3.5" /> Quản trị viên
          </span>
        );
      case 'LECTURER':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300">
            <School className="w-3.5 h-3.5" /> Giảng viên
          </span>
        );
      case 'STUDENT':
      default:
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300">
            <GraduationCap className="w-3.5 h-3.5" /> Sinh viên
          </span>
        );
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 shadow-xs">
      <div className="px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        {/* Brand & Project Identity */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-700 via-indigo-600 to-sky-500 flex items-center justify-center text-white shadow-md shadow-blue-500/20 font-black tracking-wider text-lg">
            FA
          </div>
          <div>
            <h1 className="text-base font-bold text-slate-900 dark:text-white leading-tight flex items-center gap-2">
              FACEATTEND <span className="text-xs px-1.5 py-0.5 rounded bg-blue-600 text-white font-medium">ENTERPRISE</span>
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Hệ thống Điểm danh AI & Quản lý Đào tạo
            </p>
          </div>
        </div>

        {/* Right Section: User Profile & Logout */}
        <div className="flex items-center gap-3 sm:gap-4">
          <div className="flex items-center gap-3 pl-2 sm:pl-4">
            <div className="text-right hidden sm:block">
              <div className="text-sm font-semibold text-slate-900 dark:text-white">
                {user?.full_name || user?.username || 'Khách'}
              </div>
              <div className="flex justify-end mt-0.5">
                {getRoleBadge(activeRole)}
              </div>
            </div>

            <div className="w-9 h-9 rounded-full bg-blue-100 dark:bg-blue-900/60 border border-blue-200 dark:border-blue-700 flex items-center justify-center text-blue-700 dark:text-blue-300 font-semibold text-sm shadow-xs">
              {user?.full_name ? user.full_name.charAt(0) : <UserIcon className="w-4 h-4" />}
            </div>

            <button
              onClick={logout}
              title="Đăng xuất"
              className="p-2 text-slate-500 hover:text-red-600 dark:text-slate-400 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 rounded-lg transition-colors flex items-center gap-1.5 text-xs font-medium"
            >
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:inline">Đăng xuất</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
