import React, { useState } from 'react';
import DataTable, { Column } from '../../components/DataTable';
import { AttendanceSession, AttendanceRecord } from '../../types';
import { INITIAL_ATTENDANCE_SESSIONS, INITIAL_ATTENDANCE_RECORDS } from '../../services/mockData';
import { CheckCircle2, Clock, Eye, AlertCircle } from 'lucide-react';

export const SessionsManagementPage: React.FC = () => {
  const [sessions] = useState<AttendanceSession[]>(INITIAL_ATTENDANCE_SESSIONS);
  const [selectedSession, setSelectedSession] = useState<AttendanceSession | null>(null);
  const [sessionRecords, setSessionRecords] = useState<AttendanceRecord[]>(INITIAL_ATTENDANCE_RECORDS);

  const columns: Column<AttendanceSession>[] = [
    {
      header: 'Mã phiên (Session Code)',
      accessorKey: 'session_code',
      cell: (i) => <span className="font-mono font-bold text-blue-600">{i.session_code}</span>,
    },
    { header: 'Lớp học phần', accessorKey: 'section_code' },
    { header: 'Môn học', accessorKey: 'subject_name' },
    { header: 'Giảng viên', accessorKey: 'lecturer_name' },
    { header: 'Ngày điểm danh', accessorKey: 'session_date' },
    {
      header: 'Trạng thái phiên',
      accessorKey: 'session_status',
      cell: (i) =>
        i.session_status === 'OPEN' ? (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" /> ĐANG MỞ
          </span>
        ) : (
          <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
            ĐÃ ĐÓNG
          </span>
        ),
    },
    {
      header: 'Thao tác',
      cell: (i) => (
        <button
          onClick={() => setSelectedSession(i)}
          className="px-3 py-1.5 bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 rounded-lg text-xs font-semibold hover:bg-blue-100 transition-colors flex items-center gap-1.5"
        >
          <Eye className="w-3.5 h-3.5" /> Chi tiết điểm danh
        </button>
      ),
    },
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
          QUẢN LÝ CÁC PHIÊN ĐIỂM DANH
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Theo dõi trạng thái các phiên điểm danh theo buổi học và hồ sơ đối chiếu kết quả sinh viên
        </p>
      </div>

      <DataTable
        columns={columns}
        data={sessions}
        searchPlaceholder="Tìm kiếm mã phiên, môn học, lớp..."
        searchFilter={(item, q) =>
          item.session_code.toLowerCase().includes(q.toLowerCase()) ||
          item.section_code.toLowerCase().includes(q.toLowerCase()) ||
          item.subject_name.toLowerCase().includes(q.toLowerCase())
        }
      />

      {/* Modal chi tiết kết quả sinh viên */}
      {selectedSession && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 rounded-3xl max-w-2xl w-full p-6 shadow-2xl border border-slate-200 dark:border-slate-800">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  Kết quả phiên: {selectedSession.session_code}
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  {selectedSession.subject_name} | Lớp {selectedSession.section_code}
                </p>
              </div>
              <button
                onClick={() => setSelectedSession(null)}
                className="text-slate-400 hover:text-slate-600 text-sm font-bold"
              >
                ✕ Đóng
              </button>
            </div>

            <div className="mt-4 max-h-96 overflow-y-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-100 dark:border-slate-800 text-slate-400 font-semibold uppercase">
                    <th className="py-2.5 px-3">MSSV</th>
                    <th className="py-2.5 px-3">Họ và tên</th>
                    <th className="py-2.5 px-3">Trạng thái</th>
                    <th className="py-2.5 px-3">Giờ điểm danh</th>
                    <th className="py-2.5 px-3">Độ tin cậy AI</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  {sessionRecords.map((r) => (
                    <tr key={r.id}>
                      <td className="py-3 px-3 font-mono font-bold text-blue-600">{r.student_code}</td>
                      <td className="py-3 px-3 font-semibold">{r.student_name}</td>
                      <td className="py-3 px-3">
                        <span
                          className={`px-2 py-0.5 rounded-full font-bold ${
                            r.attendance_status === 'PRESENT'
                              ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                              : r.attendance_status === 'LATE'
                              ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'
                              : 'bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300'
                          }`}
                        >
                          {r.attendance_status}
                        </span>
                      </td>
                      <td className="py-3 px-3 text-slate-500">
                        {r.check_in_time ? new Date(r.check_in_time).toLocaleTimeString('vi-VN') : '—'}
                      </td>
                      <td className="py-3 px-3 font-mono">
                        {r.confidence_score ? `${(r.confidence_score * 100).toFixed(1)}%` : '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SessionsManagementPage;
