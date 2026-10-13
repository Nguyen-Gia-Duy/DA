import React, { useState } from 'react';
import {
  Camera,
  Play,
  Square,
  Users,
  CheckCircle2,
  Clock,
  XCircle,
  Edit3,
  ShieldCheck,
  AlertCircle,
  Sparkles,
} from 'lucide-react';
import {
  INITIAL_ATTENDANCE_SESSIONS,
  INITIAL_ATTENDANCE_RECORDS,
  INITIAL_CLASS_SECTIONS,
} from '../../services/mockData';
import { AttendanceSession, AttendanceRecord } from '../../types';

export const LiveAttendancePage: React.FC = () => {
  const [activeSession, setActiveSession] = useState<AttendanceSession | null>(
    INITIAL_ATTENDANCE_SESSIONS[0]
  );
  const [records, setRecords] = useState<AttendanceRecord[]>(INITIAL_ATTENDANCE_RECORDS);
  const [selectedSectionId, setSelectedSectionId] = useState<number>(1);
  const [gracePeriod, setGracePeriod] = useState<number>(15);
  const [isAdjustModalOpen, setIsAdjustModalOpen] = useState<boolean>(false);
  const [selectedRecord, setSelectedRecord] = useState<AttendanceRecord | null>(null);
  const [adjustedStatus, setAdjustedStatus] = useState<string>('EXCUSED');
  const [adjustReason, setAdjustReason] = useState<string>('Có phép xin nghỉ từ trước');

  // Mở phiên mới
  const handleOpenSession = () => {
    const sec = INITIAL_CLASS_SECTIONS.find((s) => s.id === selectedSectionId);
    if (!sec) return;

    const newCode = `SES-${sec.section_code}-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}-OPEN`;
    const newSession: AttendanceSession = {
      id: Date.now(),
      class_section_id: sec.id,
      section_code: sec.section_code,
      subject_name: sec.subject_name || 'INT1340',
      lecturer_name: 'TS. Nguyễn Văn An',
      session_code: newCode,
      session_date: new Date().toISOString().split('T')[0],
      start_time: new Date().toISOString(),
      session_status: 'OPEN',
      grace_period_minutes: gracePeriod,
      total_enrolled: 3,
      present_count: 0,
      late_count: 0,
      absent_count: 3,
      created_at: new Date().toISOString(),
    };
    setActiveSession(newSession);

    // Reset records to ABSENT
    setRecords([
      { id: 101, attendance_session_id: newSession.id, student_id: 1, student_code: 'B20DCCN001', student_name: 'Nguyễn Gia Duy', attendance_status: 'ABSENT', verification_method: 'AI_FACE', created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 102, attendance_session_id: newSession.id, student_id: 2, student_code: 'B20DCCN002', student_name: 'Lê Hoàng Nam', attendance_status: 'ABSENT', verification_method: 'AI_FACE', created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 103, attendance_session_id: newSession.id, student_id: 3, student_code: 'B20DCCN003', student_name: 'Phạm Thị Mai', attendance_status: 'ABSENT', verification_method: 'AI_FACE', created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
    ]);
  };

  // Đóng phiên
  const handleCloseSession = () => {
    if (!activeSession) return;
    setActiveSession({
      ...activeSession,
      session_status: 'CLOSED',
      end_time: new Date().toISOString(),
    });
  };

  // Điều chỉnh thủ công
  const handleSaveAdjustment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedRecord) return;

    setRecords((prev) =>
      prev.map((r) =>
        r.id === selectedRecord.id
          ? {
              ...r,
              attendance_status: adjustedStatus as any,
              verification_method: 'ADJUSTMENT',
              updated_at: new Date().toISOString(),
            }
          : r
      )
    );
    setIsAdjustModalOpen(false);
  };

  const presentCount = records.filter((r) => r.attendance_status === 'PRESENT').length;
  const lateCount = records.filter((r) => r.attendance_status === 'LATE').length;
  const absentCount = records.filter((r) => r.attendance_status === 'ABSENT').length;

  return (
    <div className="p-6 lg:p-8 space-y-6">
      {/* Title */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
            GIÁM SÁT ĐIỂM DANH TRỰC TIẾP (LIVE MONITOR)
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Mở phiên điểm danh thời gian thực, quản lý mã phiên và giám sát nhận diện AI từng sinh viên
          </p>
        </div>

        {activeSession && activeSession.session_status === 'OPEN' ? (
          <button
            onClick={handleCloseSession}
            className="px-4 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-bold flex items-center gap-2 shadow-lg shadow-red-500/20 transition-all"
          >
            <Square className="w-4 h-4 fill-current" /> Đóng phiên điểm danh
          </button>
        ) : (
          <div className="flex items-center gap-2">
            <select
              value={selectedSectionId}
              onChange={(e) => setSelectedSectionId(Number(e.target.value))}
              className="px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs font-medium"
            >
              {INITIAL_CLASS_SECTIONS.map((sec) => (
                <option key={sec.id} value={sec.id}>
                  {sec.section_code} - {sec.subject_name}
                </option>
              ))}
            </select>
            <button
              onClick={handleOpenSession}
              className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold flex items-center gap-2 shadow-lg shadow-emerald-500/20 transition-all"
            >
              <Play className="w-4 h-4 fill-current" /> Khởi tạo & Mở phiên
            </button>
          </div>
        )}
      </div>

      {/* Active Session Info Box */}
      {activeSession ? (
        <div className="p-6 bg-gradient-to-tr from-slate-900 to-blue-950 text-white rounded-3xl shadow-xl border border-blue-900/40 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-blue-900/60">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span
                  className={`w-3 h-3 rounded-full ${
                    activeSession.session_status === 'OPEN'
                      ? 'bg-emerald-500 animate-ping'
                      : 'bg-slate-500'
                  }`}
                />
                <span className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                  {activeSession.session_status === 'OPEN'
                    ? 'PHIÊN ĐIỂM DANH ĐANG MỞ'
                    : 'PHIÊN ĐÃ KẾT THÚC'}
                </span>
              </div>
              <h2 className="text-xl font-extrabold">{activeSession.subject_name}</h2>
              <p className="text-xs text-slate-300 mt-0.5">
                Lớp học phần: <strong>{activeSession.section_code}</strong> | Giảng viên:{' '}
                {activeSession.lecturer_name}
              </p>
            </div>

            <div className="bg-slate-800/80 backdrop-blur-md px-5 py-3 rounded-2xl border border-slate-700 text-center">
              <span className="text-[10px] text-slate-400 uppercase tracking-widest block font-semibold">
                MÃ PHIÊN ĐIỂM DANH (CUNG CẤP CHO SINH VIÊN)
              </span>
              <span className="font-mono text-xl font-black text-amber-400 tracking-wider">
                {activeSession.session_code}
              </span>
            </div>
          </div>

          {/* Metrics Row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
            <div className="p-3.5 bg-slate-800/50 rounded-2xl border border-slate-700/60">
              <div className="text-xs text-slate-400">Tổng sĩ số</div>
              <div className="text-xl font-bold mt-1">{records.length} sinh viên</div>
            </div>
            <div className="p-3.5 bg-emerald-950/40 rounded-2xl border border-emerald-800/60 text-emerald-300">
              <div className="text-xs text-emerald-400">Có mặt đúng giờ</div>
              <div className="text-xl font-bold mt-1">{presentCount}</div>
            </div>
            <div className="p-3.5 bg-amber-950/40 rounded-2xl border border-amber-800/60 text-amber-300">
              <div className="text-xs text-amber-400">Đi muộn (Late)</div>
              <div className="text-xl font-bold mt-1">{lateCount}</div>
            </div>
            <div className="p-3.5 bg-red-950/40 rounded-2xl border border-red-800/60 text-red-300">
              <div className="text-xs text-red-400">Vắng mặt</div>
              <div className="text-xl font-bold mt-1">{absentCount}</div>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-8 text-center bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl">
          <AlertCircle className="w-10 h-10 text-amber-500 mx-auto mb-2" />
          <h3 className="font-bold text-slate-800 dark:text-white">Chưa có phiên điểm danh nào đang mở</h3>
          <p className="text-xs text-slate-500 mt-1">Chọn lớp học phần và nhấn "Khởi tạo & Mở phiên" để bắt đầu.</p>
        </div>
      )}

      {/* Roster & Check-in Table */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-xs">
        <h3 className="text-base font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
          <Users className="w-4 h-4 text-slate-400" />
          Danh sách Sinh viên & Kết quả Nhận diện AI
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-400 font-semibold uppercase">
                <th className="py-3 px-4">MSSV</th>
                <th className="py-3 px-4">Họ và tên</th>
                <th className="py-3 px-4">Trạng thái điểm danh</th>
                <th className="py-3 px-4">Thời gian nhận diện</th>
                <th className="py-3 px-4">Độ tương đồng AI</th>
                <th className="py-3 px-4 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {records.map((r) => (
                <tr key={r.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">
                  <td className="py-3.5 px-4 font-mono font-bold text-blue-600 dark:text-blue-400">
                    {r.student_code}
                  </td>
                  <td className="py-3.5 px-4 font-semibold text-slate-900 dark:text-white">
                    {r.student_name}
                  </td>
                  <td className="py-3.5 px-4">
                    {r.attendance_status === 'PRESENT' && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                        <CheckCircle2 className="w-3.5 h-3.5" /> CÓ MẶT
                      </span>
                    )}
                    {r.attendance_status === 'LATE' && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-bold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300">
                        <Clock className="w-3.5 h-3.5" /> ĐI MUỘN
                      </span>
                    )}
                    {r.attendance_status === 'ABSENT' && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-bold bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300">
                        <XCircle className="w-3.5 h-3.5" /> VẮNG MẶT
                      </span>
                    )}
                    {r.attendance_status === 'EXCUSED' && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-bold bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300">
                        CÓ PHÉP
                      </span>
                    )}
                  </td>
                  <td className="py-3.5 px-4 text-slate-500">
                    {r.check_in_time ? new Date(r.check_in_time).toLocaleTimeString('vi-VN') : '—'}
                  </td>
                  <td className="py-3.5 px-4">
                    {r.confidence_score ? (
                      <span className="font-mono font-semibold text-emerald-600 dark:text-emerald-400">
                        {(r.confidence_score * 100).toFixed(1)}%
                      </span>
                    ) : (
                      <span className="text-slate-400">—</span>
                    )}
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={() => {
                        setSelectedRecord(r);
                        setAdjustedStatus(r.attendance_status);
                        setIsAdjustModalOpen(true);
                      }}
                      className="p-1.5 text-slate-500 hover:text-blue-600 dark:hover:text-blue-400 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                      title="Điều chỉnh thủ công"
                    >
                      <Edit3 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal Điều chỉnh điểm danh */}
      {isAdjustModalOpen && selectedRecord && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-200 dark:border-slate-800">
            <h3 className="text-base font-bold text-slate-900 dark:text-white mb-2">
              Điều chỉnh trạng thái điểm danh
            </h3>
            <p className="text-xs text-slate-500 mb-4">
              Sinh viên: <strong>{selectedRecord.student_name}</strong> ({selectedRecord.student_code})
            </p>

            <form onSubmit={handleSaveAdjustment} className="space-y-4 text-xs">
              <div>
                <label className="font-semibold text-slate-700 dark:text-slate-300">Trạng thái mới</label>
                <select
                  value={adjustedStatus}
                  onChange={(e) => setAdjustedStatus(e.target.value)}
                  className="mt-1 w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
                >
                  <option value="PRESENT">Có mặt (PRESENT)</option>
                  <option value="LATE">Đi muộn (LATE)</option>
                  <option value="ABSENT">Vắng mặt (ABSENT)</option>
                  <option value="EXCUSED">Nghỉ có phép (EXCUSED)</option>
                  <option value="NEEDS_REVIEW">Cần xem xét lại (NEEDS_REVIEW)</option>
                </select>
              </div>

              <div>
                <label className="font-semibold text-slate-700 dark:text-slate-300">Lý do điều chỉnh (Bắt buộc theo chuẩn audit)</label>
                <textarea
                  rows={3}
                  required
                  value={adjustReason}
                  onChange={(e) => setAdjustReason(e.target.value)}
                  placeholder="VD: Sinh viên xin phép qua email / Thiết bị camera gặp sự cố"
                  className="mt-1 w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
                />
              </div>

              <div className="flex justify-end gap-2 mt-6">
                <button
                  type="button"
                  onClick={() => setIsAdjustModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold"
                >
                  Lưu thay đổi
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default LiveAttendancePage;
