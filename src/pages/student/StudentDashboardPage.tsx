import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import {
  GraduationCap,
  CheckCircle2,
  Clock,
  Camera,
  ShieldCheck,
  AlertCircle,
  BookOpen,
  Calendar,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { INITIAL_ATTENDANCE_RECORDS } from '../../services/mockData';

export const StudentDashboardPage: React.FC = () => {
  const { user } = useAuth();

  const attendedCount = INITIAL_ATTENDANCE_RECORDS.filter((r) => r.student_id === 1 && (r.attendance_status === 'PRESENT' || r.attendance_status === 'LATE')).length;
  const totalCount = INITIAL_ATTENDANCE_RECORDS.filter((r) => r.student_id === 1).length || 1;
  const rate = Math.round((attendedCount / totalCount) * 100);

  return (
    <div className="p-6 lg:p-8 space-y-8 max-w-6xl mx-auto">
      {/* Student Banner */}
      <div className="p-6 lg:p-8 bg-gradient-to-r from-blue-700 via-indigo-700 to-sky-600 rounded-3xl text-white shadow-xl shadow-blue-500/15 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center font-black text-2xl border border-white/30">
            {user?.full_name ? user.full_name.charAt(0) : 'S'}
          </div>
          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-sky-200">
              CỔNG THÔNG TIN SINH VIÊN
            </div>
            <h1 className="text-2xl font-black">{user?.full_name || 'Nguyễn Gia Duy'}</h1>
            <p className="text-xs text-sky-100 mt-1">
              MSSV: <strong>{user?.student_code || 'B20DCCN001'}</strong> | Lớp sinh hoạt: <strong>CNTT-K20A</strong> | Khoa: CNTT
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/student/check-in"
            className="px-5 py-2.5 bg-white text-blue-700 hover:bg-sky-50 rounded-xl text-xs font-bold shadow-md transition-all flex items-center gap-2"
          >
            <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Điểm danh ngay
          </Link>
          <Link
            to="/student/register-face"
            className="px-4 py-2.5 bg-blue-800/80 hover:bg-blue-800 text-white rounded-xl text-xs font-semibold border border-white/20 transition-all flex items-center gap-1.5"
          >
            <Camera className="w-4 h-4" /> Khuôn mặt AI
          </Link>
        </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Attendance Rate */}
        <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Tỷ lệ Chuyên cần</div>
            <div className="text-3xl font-black text-blue-600 dark:text-blue-400 mt-1">{rate}%</div>
            <div className="text-[11px] text-emerald-600 font-medium mt-1">Đủ điều kiện dự thi</div>
          </div>
          <div className="w-14 h-14 rounded-2xl bg-blue-50 dark:bg-blue-950/50 flex items-center justify-center text-blue-600">
            <CheckCircle2 className="w-7 h-7" />
          </div>
        </div>

        {/* Face Profile Status */}
        <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Hồ sơ Khuôn mặt AI</div>
            <div className="text-lg font-bold text-slate-900 dark:text-white mt-1">Đã kích hoạt</div>
            <div className="text-[11px] text-slate-500 mt-1">Mã hóa AES-256 GCM (ArcFace 512D)</div>
          </div>
          <div className="w-14 h-14 rounded-2xl bg-emerald-50 dark:bg-emerald-950/50 flex items-center justify-center text-emerald-600">
            <ShieldCheck className="w-7 h-7" />
          </div>
        </div>

        {/* Enrolled Courses */}
        <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Học phần kỳ này</div>
            <div className="text-3xl font-black text-slate-900 dark:text-white mt-1">2 Lớp</div>
            <div className="text-[11px] text-slate-500 mt-1">INT1340 & INT1420</div>
          </div>
          <div className="w-14 h-14 rounded-2xl bg-indigo-50 dark:bg-indigo-950/50 flex items-center justify-center text-indigo-600">
            <BookOpen className="w-7 h-7" />
          </div>
        </div>
      </div>

      {/* Attendance History Table */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-xs">
        <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
          <Clock className="w-4 h-4 text-slate-400" />
          Lịch sử Điểm danh Gần đây của bạn
        </h2>

        <div className="divide-y divide-slate-100 dark:divide-slate-800 text-xs">
          <div className="py-3 flex items-center justify-between">
            <div>
              <div className="font-bold text-slate-900 dark:text-white">
                Trí tuệ Nhân tạo & Thị giác Máy tính (INT1340-01)
              </div>
              <div className="text-slate-400 mt-0.5">Phiên: SES-TODAY-INT1340-01 | Hôm nay</div>
            </div>
            <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
              CÓ MẶT (95.0%)
            </span>
          </div>

          <div className="py-3 flex items-center justify-between">
            <div>
              <div className="font-bold text-slate-900 dark:text-white">
                Kiến trúc Phần mềm Nâng cao (INT1420-02)
              </div>
              <div className="text-slate-400 mt-0.5">Phiên: SES-2024-09-02-INT1420 | 02/09/2024</div>
            </div>
            <span className="px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300">
              ĐI MUỘN (91.0%)
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboardPage;
