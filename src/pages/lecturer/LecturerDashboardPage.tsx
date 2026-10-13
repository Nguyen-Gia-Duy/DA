import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Layers, Users, CalendarCheck, TrendingUp, Camera, Clock, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { INITIAL_CLASS_SECTIONS, INITIAL_ATTENDANCE_SESSIONS } from '../../services/mockData';

export const LecturerDashboardPage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="p-6 lg:p-8 space-y-8 max-w-6xl mx-auto">
      {/* Banner */}
      <div className="p-6 lg:p-8 bg-gradient-to-r from-slate-900 via-indigo-950 to-blue-900 rounded-3xl text-white shadow-xl shadow-indigo-900/15 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-amber-400">
            CỔNG THÔNG TIN GIẢNG VIÊN
          </span>
          <h1 className="text-2xl font-black mt-1">Xin chào, {user?.full_name || 'TS. Nguyễn Văn An'}</h1>
          <p className="text-xs text-slate-300 mt-1">
            Mã giảng viên: <strong>{user?.lecturer_code || 'GV001'}</strong> | Khoa: Công nghệ Thông tin
          </p>
        </div>

        <Link
          to="/lecturer/live-attendance"
          className="px-5 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-2xl text-xs font-bold shadow-lg shadow-blue-500/25 flex items-center gap-2 transition-all"
        >
          <Camera className="w-4 h-4" /> Mở phiên điểm danh ngay
        </Link>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-xs">
          <div className="text-xs text-slate-400 font-semibold">Lớp học phần phụ trách</div>
          <div className="text-2xl font-black text-slate-900 dark:text-white mt-1">
            {INITIAL_CLASS_SECTIONS.length} Lớp
          </div>
        </div>

        <div className="p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-xs">
          <div className="text-xs text-slate-400 font-semibold">Tổng số sinh viên</div>
          <div className="text-2xl font-black text-slate-900 dark:text-white mt-1">3 sinh viên</div>
        </div>

        <div className="p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-xs">
          <div className="text-xs text-slate-400 font-semibold">Phiên điểm danh đã tạo</div>
          <div className="text-2xl font-black text-blue-600 dark:text-blue-400 mt-1">
            {INITIAL_ATTENDANCE_SESSIONS.length} Phiên
          </div>
        </div>

        <div className="p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-xs">
          <div className="text-xs text-slate-400 font-semibold">Tỷ lệ chuyên cần TB</div>
          <div className="text-2xl font-black text-emerald-600 dark:text-emerald-400 mt-1">89.2%</div>
        </div>
      </div>

      {/* Assigned Classes */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-xs">
        <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4">
          Lớp học phần phân công học kỳ này
        </h2>
        <div className="divide-y divide-slate-100 dark:divide-slate-800 text-xs">
          {INITIAL_CLASS_SECTIONS.map((sec) => (
            <div key={sec.id} className="py-4 flex items-center justify-between">
              <div>
                <span className="font-mono font-bold text-blue-600 text-sm">{sec.section_code}</span>
                <span className="font-semibold text-slate-900 dark:text-white ml-2">
                  {sec.subject_name}
                </span>
                <div className="text-slate-400 mt-0.5">
                  Sĩ số: {sec.current_enrollment}/{sec.max_capacity} sinh viên | Học kỳ 1 (2024-2025)
                </div>
              </div>

              <Link
                to="/lecturer/live-attendance"
                className="px-3.5 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-blue-50 dark:hover:bg-blue-950/40 text-blue-600 dark:text-blue-400 rounded-xl font-bold flex items-center gap-1.5 transition-colors"
              >
                Giám sát điểm danh <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LecturerDashboardPage;
