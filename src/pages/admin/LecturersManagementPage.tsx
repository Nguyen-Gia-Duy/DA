import React, { useState } from 'react';
import DataTable, { Column } from '../../components/DataTable';
import { Lecturer } from '../../types';
import { INITIAL_LECTURERS } from '../../services/mockData';
import { UserCheck, Mail, Phone, Building2 } from 'lucide-react';

export const LecturersManagementPage: React.FC = () => {
  const [lecturers] = useState<Lecturer[]>(INITIAL_LECTURERS);

  const columns: Column<Lecturer>[] = [
    {
      header: 'Mã GV',
      accessorKey: 'lecturer_code',
      cell: (i) => <span className="font-mono font-bold text-indigo-600 dark:text-indigo-400">{i.lecturer_code}</span>,
    },
    {
      header: 'Họ và tên',
      accessorKey: 'full_name',
      cell: (i) => (
        <div>
          <div className="font-semibold text-slate-900 dark:text-white">{i.full_name}</div>
          <div className="text-xs text-slate-400">{i.academic_degree || 'Tiến sĩ'}</div>
        </div>
      ),
    },
    {
      header: 'Email & Số điện thoại',
      cell: (i) => (
        <div className="text-xs space-y-0.5">
          <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-300">
            <Mail className="w-3.5 h-3.5 text-slate-400" /> {i.email}
          </div>
          <div className="flex items-center gap-1.5 text-slate-400">
            <Phone className="w-3.5 h-3.5" /> {i.phone || '0912345678'}
          </div>
        </div>
      ),
    },
    {
      header: 'Khoa đào tạo',
      accessorKey: 'department_name',
      cell: (i) => (
        <span className="inline-flex items-center gap-1 text-xs">
          <Building2 className="w-3.5 h-3.5 text-slate-400" /> {i.department_name}
        </span>
      ),
    },
    {
      header: 'Trạng thái',
      accessorKey: 'status',
      cell: (i) => (
        <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
          Đang công tác (ACTIVE)
        </span>
      ),
    },
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
          QUẢN LÝ GIẢNG VIÊN
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Danh sách giảng viên phụ trách giảng dạy và giám sát các phiên điểm danh học phần
        </p>
      </div>

      <DataTable
        columns={columns}
        data={lecturers}
        searchPlaceholder="Tìm kiếm giảng viên theo tên, mã GV, email..."
        searchFilter={(item, q) =>
          item.lecturer_code.toLowerCase().includes(q.toLowerCase()) ||
          item.full_name.toLowerCase().includes(q.toLowerCase()) ||
          item.email.toLowerCase().includes(q.toLowerCase())
        }
      />
    </div>
  );
};

export default LecturersManagementPage;
