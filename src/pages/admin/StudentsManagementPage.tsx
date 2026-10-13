import React, { useState, useEffect } from 'react';
import DataTable, { Column } from '../../components/DataTable';
import { Student, Department, AdministrativeClass } from '../../types';
import { INITIAL_STUDENTS, INITIAL_DEPARTMENTS, INITIAL_ADMIN_CLASSES } from '../../services/mockData';
import api from '../../services/api';
import { UserPlus, CheckCircle2, XCircle, ShieldCheck, Camera, Sparkles } from 'lucide-react';

export const StudentsManagementPage: React.FC = () => {
  const [students, setStudents] = useState<Student[]>(INITIAL_STUDENTS);
  const [departments, setDepartments] = useState<Department[]>(INITIAL_DEPARTMENTS);
  const [adminClasses, setAdminClasses] = useState<AdministrativeClass[]>(INITIAL_ADMIN_CLASSES);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newStudent, setNewStudent] = useState({
    student_code: '',
    full_name: '',
    email: '',
    phone: '',
    administrative_class_id: 1,
    department_id: 1,
    gender: 'MALE',
    date_of_birth: '2002-01-01',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [resSt, resDept, resClass] = await Promise.all([
          api.get('/students'),
          api.get('/departments'),
          api.get('/administrative-classes'),
        ]);
        if (resSt.data?.length) setStudents(resSt.data);
        if (resDept.data?.length) setDepartments(resDept.data);
        if (resClass.data?.length) setAdminClasses(resClass.data);
      } catch (err) {
        // Fallback to initial seed data
      }
    };
    fetchData();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.post('/students', newStudent);
      const created: Student = {
        id: res.data?.id || Date.now(),
        user_id: Date.now(),
        student_code: newStudent.student_code,
        full_name: newStudent.full_name,
        email: newStudent.email,
        phone: newStudent.phone,
        administrative_class_id: newStudent.administrative_class_id,
        class_code: adminClasses.find((c) => c.id === newStudent.administrative_class_id)?.class_code,
        department_id: newStudent.department_id,
        department_name: departments.find((d) => d.id === newStudent.department_id)?.department_name,
        gender: newStudent.gender as any,
        academic_status: 'STUDYING',
        has_face_profile: false,
        created_at: new Date().toISOString(),
      };
      setStudents([created, ...students]);
      setIsModalOpen(false);
      setNewStudent({
        student_code: '',
        full_name: '',
        email: '',
        phone: '',
        administrative_class_id: 1,
        department_id: 1,
        gender: 'MALE',
        date_of_birth: '2002-01-01',
      });
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Thêm sinh viên thất bại');
    }
  };

  const columns: Column<Student>[] = [
    {
      header: 'MSSV',
      accessorKey: 'student_code',
      cell: (item) => (
        <span className="font-mono font-bold text-blue-600 dark:text-blue-400">
          {item.student_code}
        </span>
      ),
    },
    {
      header: 'Họ và Tên',
      accessorKey: 'full_name',
      cell: (item) => (
        <div>
          <div className="font-semibold text-slate-900 dark:text-white">{item.full_name}</div>
          <div className="text-xs text-slate-400">{item.email}</div>
        </div>
      ),
    },
    {
      header: 'Lớp sinh hoạt',
      accessorKey: 'class_code',
      cell: (item) => (
        <span className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-medium">
          {item.class_code || 'CNTT-K20A'}
        </span>
      ),
    },
    {
      header: 'Khoa đào tạo',
      accessorKey: 'department_name',
      cell: (item) => <span className="text-xs">{item.department_name || 'CNTT'}</span>,
    },
    {
      header: 'Hồ sơ Khuôn mặt AI',
      cell: (item) =>
        item.has_face_profile ? (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300">
            <CheckCircle2 className="w-3.5 h-3.5" /> Đã đăng ký (512D)
          </span>
        ) : (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300">
            <XCircle className="w-3.5 h-3.5" /> Chưa đăng ký
          </span>
        ),
    },
    {
      header: 'Trạng thái học tập',
      accessorKey: 'academic_status',
      cell: (item) => (
        <span className="text-xs font-medium text-slate-600 dark:text-slate-300">
          {item.academic_status === 'STUDYING'
            ? 'Đang theo học'
            : item.academic_status === 'DROPPED_OUT'
            ? 'Thôi học'
            : item.academic_status}
        </span>
      ),
    },
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
            QUẢN LÝ SINH VIÊN
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Danh sách sinh viên, trạng thái hồ sơ sinh trắc học và quản lý học phần
          </p>
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold flex items-center gap-2 shadow-md shadow-blue-500/20 transition-all"
        >
          <UserPlus className="w-4 h-4" /> Thêm sinh viên mới
        </button>
      </div>

      <DataTable
        columns={columns}
        data={students}
        searchPlaceholder="Tìm kiếm sinh viên theo tên, MSSV, email..."
        searchFilter={(item, q) =>
          item.student_code.toLowerCase().includes(q.toLowerCase()) ||
          item.full_name.toLowerCase().includes(q.toLowerCase()) ||
          item.email.toLowerCase().includes(q.toLowerCase())
        }
      />

      {/* Modal Thêm sinh viên */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 dark:border-slate-800">
            <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-4">
              Thêm hồ sơ sinh viên mới
            </h2>
            <form onSubmit={handleCreate} className="space-y-4 text-xs">
              <div>
                <label className="font-semibold text-slate-700 dark:text-slate-300">Mã sinh viên (MSSV)</label>
                <input
                  type="text"
                  required
                  value={newStudent.student_code}
                  onChange={(e) => setNewStudent({ ...newStudent, student_code: e.target.value })}
                  placeholder="VD: B20DCCN004"
                  className="mt-1 w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700 dark:text-slate-300">Họ và tên</label>
                <input
                  type="text"
                  required
                  value={newStudent.full_name}
                  onChange={(e) => setNewStudent({ ...newStudent, full_name: e.target.value })}
                  placeholder="VD: Hoàng Văn Tuấn"
                  className="mt-1 w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700 dark:text-slate-300">Email trường cấp</label>
                <input
                  type="email"
                  required
                  value={newStudent.email}
                  onChange={(e) => setNewStudent({ ...newStudent, email: e.target.value })}
                  placeholder="tuan.hoang@faceattend.edu.vn"
                  className="mt-1 w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 dark:text-slate-300">Khoa</label>
                  <select
                    value={newStudent.department_id}
                    onChange={(e) => setNewStudent({ ...newStudent, department_id: Number(e.target.value) })}
                    className="mt-1 w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
                  >
                    {departments.map((d) => (
                      <option key={d.id} value={d.id}>{d.department_name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="font-semibold text-slate-700 dark:text-slate-300">Lớp sinh hoạt</label>
                  <select
                    value={newStudent.administrative_class_id}
                    onChange={(e) => setNewStudent({ ...newStudent, administrative_class_id: Number(e.target.value) })}
                    className="mt-1 w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
                  >
                    {adminClasses.map((c) => (
                      <option key={c.id} value={c.id}>{c.class_code}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-200"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold"
                >
                  Lưu sinh viên
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentsManagementPage;
