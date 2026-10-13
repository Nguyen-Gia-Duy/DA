import React, { useState } from 'react';
import DataTable, { Column } from '../../components/DataTable';
import { AuditLog } from '../../types';
import { INITIAL_AUDIT_LOGS } from '../../services/mockData';
import { FileText, Shield, Clock } from 'lucide-react';

export const AuditLogsPage: React.FC = () => {
  const [logs] = useState<AuditLog[]>(INITIAL_AUDIT_LOGS);

  const columns: Column<AuditLog>[] = [
    {
      header: 'Thời gian',
      accessorKey: 'created_at',
      cell: (i) => (
        <span className="text-xs text-slate-500">
          {new Date(i.created_at).toLocaleTimeString('vi-VN')} {new Date(i.created_at).toLocaleDateString('vi-VN')}
        </span>
      ),
    },
    {
      header: 'Người thực hiện',
      accessorKey: 'user_name',
      cell: (i) => <span className="font-semibold text-slate-800 dark:text-slate-200">{i.user_name}</span>,
    },
    {
      header: 'Hành động (Action)',
      accessorKey: 'action',
      cell: (i) => (
        <span className="px-2.5 py-1 rounded-lg bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 font-mono text-xs font-semibold">
          {i.action}
        </span>
      ),
    },
    {
      header: 'Bảng đối tượng',
      accessorKey: 'entity_type',
      cell: (i) => <code className="text-xs font-mono text-slate-600 dark:text-slate-400">{i.entity_type}</code>,
    },
    {
      header: 'Chi tiết (Details)',
      cell: (i) => (
        <pre className="text-[11px] font-mono text-slate-500 max-w-xs truncate">
          {JSON.stringify(i.details)}
        </pre>
      ),
    },
    {
      header: 'Địa chỉ IP',
      accessorKey: 'ip_address',
      cell: (i) => <span className="font-mono text-xs text-slate-400">{i.ip_address || '127.0.0.1'}</span>,
    },
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
          <FileText className="w-7 h-7 text-blue-600" />
          NHẬT KÝ KIỂM TOÁN HỆ THỐNG (AUDIT LOGS)
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Lưu vết toàn bộ thao tác thêm, sửa, xóa, đăng nhập và điểm danh của người dùng trong bảng <code>audit_logs</code>
        </p>
      </div>

      <DataTable
        columns={columns}
        data={logs}
        searchPlaceholder="Tìm kiếm nhật ký theo người dùng, hành động..."
        searchFilter={(item, q) =>
          item.action.toLowerCase().includes(q.toLowerCase()) ||
          item.user_name.toLowerCase().includes(q.toLowerCase()) ||
          item.entity_type.toLowerCase().includes(q.toLowerCase())
        }
      />
    </div>
  );
};

export default AuditLogsPage;
