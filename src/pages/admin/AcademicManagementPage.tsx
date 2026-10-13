import React, { useState } from 'react';
import DataTable, { Column } from '../../components/DataTable';
import { Department, Subject, ClassSection, Classroom, AdministrativeClass, Semester } from '../../types';
import {
  INITIAL_DEPARTMENTS,
  INITIAL_SUBJECTS,
  INITIAL_CLASS_SECTIONS,
  INITIAL_CLASSROOMS,
  INITIAL_ADMIN_CLASSES,
  INITIAL_SEMESTERS,
} from '../../services/mockData';
import { Building2, BookOpen, Layers, School, DoorOpen, Calendar } from 'lucide-react';

export const AcademicManagementPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'depts' | 'subjects' | 'sections' | 'rooms' | 'classes' | 'semesters'>('sections');

  // Columns for Sections
  const sectionCols: Column<ClassSection>[] = [
    { header: 'Mã lớp HP', accessorKey: 'section_code', cell: (i) => <span className="font-mono font-bold text-blue-600">{i.section_code}</span> },
    { header: 'Tên môn học', accessorKey: 'subject_name' },
    { header: 'Giảng viên phụ trách', accessorKey: 'lecturer_name' },
    { header: 'Học kỳ', accessorKey: 'semester_name' },
    {
      header: 'Sĩ số',
      cell: (i) => (
        <span className="font-semibold">
          {i.current_enrollment} / {i.max_capacity} sinh viên
        </span>
      ),
    },
    {
      header: 'Trạng thái',
      cell: (i) => (
        <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
          {i.status}
        </span>
      ),
    },
  ];

  // Columns for Subjects
  const subjectCols: Column<Subject>[] = [
    { header: 'Mã môn', accessorKey: 'subject_code', cell: (i) => <span className="font-mono font-bold">{i.subject_code}</span> },
    { header: 'Tên môn học', accessorKey: 'subject_name', cell: (i) => <span className="font-semibold">{i.subject_name}</span> },
    { header: 'Số tín chỉ', accessorKey: 'credits', cell: (i) => <span>{i.credits} TC</span> },
    { header: 'Khoa phụ trách', accessorKey: 'department_name' },
  ];

  // Columns for Departments
  const deptCols: Column<Department>[] = [
    { header: 'Mã khoa', accessorKey: 'department_code', cell: (i) => <span className="font-mono font-bold">{i.department_code}</span> },
    { header: 'Tên khoa / Viện', accessorKey: 'department_name', cell: (i) => <span className="font-semibold">{i.department_name}</span> },
    { header: 'Mô tả', accessorKey: 'description' },
  ];

  // Columns for Classrooms
  const roomCols: Column<Classroom>[] = [
    { header: 'Mã phòng', accessorKey: 'room_code', cell: (i) => <span className="font-mono font-bold">{i.room_code}</span> },
    { header: 'Tòa nhà', accessorKey: 'building' },
    { header: 'Sức chứa', accessorKey: 'capacity', cell: (i) => <span>{i.capacity} chỗ</span> },
    { header: 'Loại phòng', accessorKey: 'room_type' },
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
          QUẢN LÝ DANH MỤC ĐÀO TẠO
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Quản lý các bảng cơ sở: Khoa, Môn học, Lớp học phần, Phòng học và Học kỳ trong hệ thống đào tạo
        </p>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 dark:border-slate-800 pb-3 overflow-x-auto text-xs font-semibold">
        <button
          onClick={() => setActiveTab('sections')}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl transition-all ${
            activeTab === 'sections'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <Layers className="w-4 h-4" /> Lớp học phần ({INITIAL_CLASS_SECTIONS.length})
        </button>

        <button
          onClick={() => setActiveTab('subjects')}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl transition-all ${
            activeTab === 'subjects'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <BookOpen className="w-4 h-4" /> Môn học ({INITIAL_SUBJECTS.length})
        </button>

        <button
          onClick={() => setActiveTab('depts')}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl transition-all ${
            activeTab === 'depts'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <Building2 className="w-4 h-4" /> Khoa đào tạo ({INITIAL_DEPARTMENTS.length})
        </button>

        <button
          onClick={() => setActiveTab('rooms')}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl transition-all ${
            activeTab === 'rooms'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <DoorOpen className="w-4 h-4" /> Phòng học ({INITIAL_CLASSROOMS.length})
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'sections' && (
        <DataTable
          columns={sectionCols}
          data={INITIAL_CLASS_SECTIONS}
          searchPlaceholder="Tìm kiếm mã lớp học phần, môn học..."
          searchFilter={(item, q) =>
            item.section_code.toLowerCase().includes(q.toLowerCase()) ||
            (item.subject_name || '').toLowerCase().includes(q.toLowerCase())
          }
        />
      )}

      {activeTab === 'subjects' && (
        <DataTable
          columns={subjectCols}
          data={INITIAL_SUBJECTS}
          searchPlaceholder="Tìm kiếm mã môn học, tên môn..."
          searchFilter={(item, q) =>
            item.subject_code.toLowerCase().includes(q.toLowerCase()) ||
            item.subject_name.toLowerCase().includes(q.toLowerCase())
          }
        />
      )}

      {activeTab === 'depts' && (
        <DataTable
          columns={deptCols}
          data={INITIAL_DEPARTMENTS}
          searchPlaceholder="Tìm kiếm mã khoa, tên khoa..."
          searchFilter={(item, q) =>
            item.department_code.toLowerCase().includes(q.toLowerCase()) ||
            item.department_name.toLowerCase().includes(q.toLowerCase())
          }
        />
      )}

      {activeTab === 'rooms' && (
        <DataTable
          columns={roomCols}
          data={INITIAL_CLASSROOMS}
          searchPlaceholder="Tìm kiếm phòng học..."
          searchFilter={(item, q) => item.room_code.toLowerCase().includes(q.toLowerCase())}
        />
      )}
    </div>
  );
};

export default AcademicManagementPage;
