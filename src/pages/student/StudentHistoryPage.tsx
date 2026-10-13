import React from 'react';
import DataTable, { Column } from '../../components/DataTable';
import { AttendanceRecord } from '../../types';
import { INITIAL_ATTENDANCE_RECORDS } from '../../services/mockData';
import { Clock, CheckCircle2, XCircle } from 'lucide-react';

export const StudentHistoryPage: React.FC = () => {
  const records = INITIAL_ATTENDANCE_RECORDS;

  const columns: Column<AttendanceRecord>[] = [
    {
      header: 'Thời gian điểm danh',
      accessorKey: 'check_in_time',
      cell: (i) => (
        <span className="text-xs text-slate-500">
          {i.check_in_time ? new Date(i.check_in_time).toLocaleTimeString('vi-VN') : '—'}{' '}
          {i.check_in_time ? new Date(i.check_in_time).toLocaleDateString('vi-VN') : '—'}
        </span>
      ),
    },
    {
      header: 'Môn học / Học phần',
      cell: () => <span className="font-semibold text-slate-900 dark:text-white">Trí tuệ Nhân tạo & Thị giác Máy tính (INT1340-01)</span>,
    },
    {
      header: 'Kết quả điểm danh',
      accessorKey: 'attendance_status',
      cell: (i) =>
        i.attendance_status === 'PRESENT' ? (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
            <CheckCircle2 className="w-3.5 h-3.5" /> CÓ MẶT ĐÚNG GIỜ
          </span>
        ) : i.attendance_status === 'LATE' ? (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300">
            <Clock className="w-3.5 h-3.5" /> ĐI MUỘN
          </span>
        ) : (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300">
            <XCircle className="w-3.5 h-3.5" /> VẮNG MẶT
          </span>
        ),
    },
    {
      header: 'Phương thức',
      accessorKey: 'verification_method',
      cell: (i) => (
        <span className="text-xs font-mono text-slate-500">
          {i.verification_method === 'AI_FACE' ? 'Nhận diện khuôn mặt AI' : i.verification_method}
        </span>
      ),
    },
    {
      header: 'Độ khớp khuôn mặt',
      accessorKey: 'confidence_score',
      cell: (i) =>
        i.confidence_score ? (
          <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">
            {(i.confidence_score * 100).toFixed(1)}%
          </span>
        ) : (
          <span className="text-slate-400">—</span>
        ),
    },
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
          <Clock className="w-7 h-7 text-blue-600" />
          LỊCH SỬ ĐIỂM DANH & BÁO CÁO CHUYÊN CẦN
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Theo dõi toàn bộ lịch sử điểm danh của cá nhân sinh viên qua các buổi học
        </p>
      </div>

      <DataTable columns={columns} data={records} searchPlaceholder="Tìm kiếm buổi học..." />
    </div>
  );
};

export default StudentHistoryPage;
