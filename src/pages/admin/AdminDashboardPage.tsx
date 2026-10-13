import React, { useState, useEffect } from 'react';
import {
  Users,
  GraduationCap,
  Building2,
  BookOpen,
  CalendarCheck,
  TrendingUp,
  AlertTriangle,
  Clock,
  CheckCircle2,
  ShieldAlert,
} from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';
import api from '../../services/api';
import { AdminDashboardData } from '../../types';
import { INITIAL_STUDENTS, INITIAL_LECTURERS, INITIAL_DEPARTMENTS, INITIAL_CLASS_SECTIONS, INITIAL_SUBJECTS, INITIAL_ATTENDANCE_SESSIONS, INITIAL_AUDIT_LOGS } from '../../services/mockData';

export const AdminDashboardPage: React.FC = () => {
  const [stats, setStats] = useState<AdminDashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await api.get('/dashboard/admin');
        if (
          res.data &&
          typeof res.data === 'object' &&
          Array.isArray(res.data.attendance_trends) &&
          Array.isArray(res.data.recent_activities)
        ) {
          setStats(res.data);
        } else {
          throw new Error('Dữ liệu API dashboard chưa đầy đủ cấu trúc.');
        }
      } catch (err) {
        // Fallback calculated from seed data
        setStats({
          total_students: INITIAL_STUDENTS.length,
          total_lecturers: INITIAL_LECTURERS.length,
          total_departments: INITIAL_DEPARTMENTS.length,
          total_class_sections: INITIAL_CLASS_SECTIONS.length,
          total_subjects: INITIAL_SUBJECTS.length,
          total_attendance_sessions: INITIAL_ATTENDANCE_SESSIONS.length,
          overall_attendance_rate: 88.5,
          today_sessions_count: 1,
          late_count: 2,
          absent_count: 1,
          failed_attempts_count: 1,
          attendance_trends: [
            { date: 'Thứ 2', present: 28, late: 2, absent: 1 },
            { date: 'Thứ 3', present: 32, late: 4, absent: 2 },
            { date: 'Thứ 4', present: 30, late: 1, absent: 0 },
            { date: 'Thứ 5', present: 29, late: 3, absent: 2 },
            { date: 'Thứ 6', present: 34, late: 2, absent: 1 },
            { date: 'Thứ 7', present: 22, late: 1, absent: 1 },
            { date: 'Hôm nay', present: 31, late: 3, absent: 1 },
          ],
          recent_activities: INITIAL_AUDIT_LOGS.map((l) => ({
            id: l.id,
            action: l.action,
            user_name: l.user_name,
            entity_type: l.entity_type,
            created_at: new Date(l.created_at).toLocaleDateString('vi-VN'),
          })),
        });
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading || !stats) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const statCards = [
    { title: 'Tổng sinh viên', value: stats.total_students, icon: <GraduationCap className="w-6 h-6 text-blue-600" />, bg: 'bg-blue-50 dark:bg-blue-950/40' },
    { title: 'Giảng viên', value: stats.total_lecturers, icon: <Users className="w-6 h-6 text-indigo-600" />, bg: 'bg-indigo-50 dark:bg-indigo-950/40' },
    { title: 'Khoa đào tạo', value: stats.total_departments, icon: <Building2 className="w-6 h-6 text-emerald-600" />, bg: 'bg-emerald-50 dark:bg-emerald-950/40' },
    { title: 'Lớp học phần', value: stats.total_class_sections, icon: <BookOpen className="w-6 h-6 text-amber-600" />, bg: 'bg-amber-50 dark:bg-amber-950/40' },
    { title: 'Phiên điểm danh', value: stats.total_attendance_sessions, icon: <CalendarCheck className="w-6 h-6 text-purple-600" />, bg: 'bg-purple-50 dark:bg-purple-950/40' },
    { title: 'Tỷ lệ chuyên cần', value: `${stats.overall_attendance_rate}%`, icon: <TrendingUp className="w-6 h-6 text-teal-600" />, bg: 'bg-teal-50 dark:bg-teal-950/40' },
  ];

  return (
    <div className="p-6 lg:p-8 space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
          BẢNG ĐIỀU KHIỂN QUẢN TRỊ VIÊN
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Giám sát thời gian thực quy trình đào tạo và thống kê điểm danh sinh trắc học khuôn mặt AI
        </p>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {statCards.map((card, idx) => (
          <div
            key={idx}
            className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xs flex flex-col justify-between"
          >
            <div className={`w-10 h-10 rounded-xl ${card.bg} flex items-center justify-center mb-3`}>
              {card.icon}
            </div>
            <div>
              <div className="text-xl font-bold text-slate-900 dark:text-white">{card.value}</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{card.title}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts & Security Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Attendance Trends BarChart */}
        <div className="lg:col-span-2 p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-bold text-slate-900 dark:text-white">
                Biểu đồ Tần suất Điểm danh 7 ngày qua
              </h2>
              <p className="text-xs text-slate-400">Số lượng sinh viên có mặt đúng giờ, đi muộn và vắng</p>
            </div>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.attendance_trends || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="date" tick={{ fontSize: 12, fill: '#64748b' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 12, fill: '#64748b' }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    borderRadius: '12px',
                    color: '#fff',
                    border: 'none',
                    fontSize: '12px',
                  }}
                />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Bar dataKey="present" name="Có mặt (PRESENT)" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="late" name="Đi muộn (LATE)" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                <Bar dataKey="absent" name="Vắng mặt (ABSENT)" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Security & Anomaly Card */}
        <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <ShieldAlert className="w-5 h-5 text-red-500" />
                Cảnh báo Nhận diện AI
              </h2>
            </div>
            <div className="space-y-3.5 text-xs">
              <div className="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 flex items-center justify-between">
                <span className="text-slate-600 dark:text-slate-400">Nỗ lực nhận diện thất bại:</span>
                <span className="font-bold text-red-600 bg-red-100 dark:bg-red-950 px-2 py-0.5 rounded-lg">
                  {stats.failed_attempts_count} lượt
                </span>
              </div>
              <div className="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 flex items-center justify-between">
                <span className="text-slate-600 dark:text-slate-400">Sinh viên đi muộn hôm nay:</span>
                <span className="font-bold text-amber-600 bg-amber-100 dark:bg-amber-950 px-2 py-0.5 rounded-lg">
                  {stats.late_count} sinh viên
                </span>
              </div>
              <div className="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 flex items-center justify-between">
                <span className="text-slate-600 dark:text-slate-400">Sinh viên vắng buổi học:</span>
                <span className="font-bold text-slate-700 dark:text-slate-300">
                  {stats.absent_count} sinh viên
                </span>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800 text-[11px] text-slate-400">
            Hệ thống tự động ghi nhật ký mọi nỗ lực không khớp hoặc nghi vấn gian lận vào bảng <code>recognition_attempts</code>.
          </div>
        </div>
      </div>

      {/* Recent Activities */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-xs">
        <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
          <Clock className="w-4 h-4 text-slate-400" />
          Nhật ký Hoạt động Hệ thống Gần đây (Audit Logs)
        </h2>
        <div className="divide-y divide-slate-100 dark:divide-slate-800 text-xs">
          {(stats.recent_activities || []).map((act) => (
            <div key={act.id} className="py-3 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="w-2 h-2 rounded-full bg-blue-500" />
                <span className="font-semibold text-slate-800 dark:text-slate-200">{act.user_name}</span>
                <span className="text-slate-500 dark:text-slate-400">đã thực hiện thao tác:</span>
                <code className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-blue-600 dark:text-blue-400 font-mono">
                  {act.action}
                </code>
              </div>
              <span className="text-slate-400">{act.created_at}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboardPage;
