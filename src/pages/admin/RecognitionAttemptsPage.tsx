import React, { useState } from 'react';
import DataTable, { Column } from '../../components/DataTable';
import { RecognitionAttempt } from '../../types';
import { INITIAL_RECOGNITION_ATTEMPTS } from '../../services/mockData';
import { ShieldAlert, CheckCircle2, XCircle, AlertTriangle, Cpu } from 'lucide-react';

export const RecognitionAttemptsPage: React.FC = () => {
  const [attempts] = useState<RecognitionAttempt[]>(INITIAL_RECOGNITION_ATTEMPTS);

  const columns: Column<RecognitionAttempt>[] = [
    {
      header: 'Thời gian',
      accessorKey: 'attempt_time',
      cell: (i) => <span className="text-xs text-slate-500">{new Date(i.attempt_time).toLocaleTimeString('vi-VN')} {new Date(i.attempt_time).toLocaleDateString('vi-VN')}</span>,
    },
    {
      header: 'Sinh viên',
      cell: (i) => (
        <div>
          <div className="font-semibold text-slate-900 dark:text-white">{i.student_name || 'Khách/Chưa xác định'}</div>
          <div className="text-[11px] font-mono text-blue-600">{i.student_code || '—'}</div>
        </div>
      ),
    },
    {
      header: 'Kết quả AI',
      accessorKey: 'attempt_status',
      cell: (i) => {
        switch (i.attempt_status) {
          case 'SUCCESS':
            return (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                <CheckCircle2 className="w-3.5 h-3.5" /> THÀNH CÔNG
              </span>
            );
          case 'FAILED_NO_FACE':
            return (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300">
                <AlertTriangle className="w-3.5 h-3.5" /> KHÔNG THẤY MẶT
              </span>
            );
          case 'FAILED_LOW_CONFIDENCE':
            return (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300">
                <XCircle className="w-3.5 h-3.5" /> ĐỘ KHỚP THẤP
              </span>
            );
          default:
            return (
              <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 dark:bg-slate-800 text-slate-600">
                {i.attempt_status}
              </span>
            );
        }
      },
    },
    {
      header: 'Độ tương đồng (Cosine)',
      accessorKey: 'similarity_score',
      cell: (i) =>
        i.similarity_score ? (
          <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">
            {(i.similarity_score * 100).toFixed(1)}%
          </span>
        ) : (
          <span className="text-slate-400">—</span>
        ),
    },
    {
      header: 'Nguyên nhân thất bại',
      accessorKey: 'failure_reason',
      cell: (i) => <span className="text-xs text-red-600 dark:text-red-400">{i.failure_reason || '—'}</span>,
    },
    {
      header: 'Địa chỉ IP',
      accessorKey: 'ip_address',
      cell: (i) => <span className="font-mono text-xs text-slate-500">{i.ip_address || '127.0.0.1'}</span>,
    },
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
          <Cpu className="w-7 h-7 text-blue-600" />
          NHẬT KÝ NHẬN DIỆN KHUÔN MẶT AI (RECOGNITION ATTEMPTS)
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Theo dõi toàn bộ các lần quét camera, độ tin cậy Cosine Similarity và cảnh báo bất thường trong bảng <code>recognition_attempts</code>
        </p>
      </div>

      <DataTable
        columns={columns}
        data={attempts}
        searchPlaceholder="Tìm kiếm nhật ký nhận diện theo tên sinh viên, MSSV..."
        searchFilter={(item, q) =>
          (item.student_name || '').toLowerCase().includes(q.toLowerCase()) ||
          (item.student_code || '').toLowerCase().includes(q.toLowerCase()) ||
          item.attempt_status.toLowerCase().includes(q.toLowerCase())
        }
      />
    </div>
  );
};

export default RecognitionAttemptsPage;
