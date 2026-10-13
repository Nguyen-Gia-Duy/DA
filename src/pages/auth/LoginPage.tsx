import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { LogIn, Shield, School, GraduationCap, AlertCircle, Sparkles } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const { login, user, activeRole } = useAuth();
  const navigate = useNavigate();
  const [usernameOrEmail, setUsernameOrEmail] = useState('admin');
  const [password, setPassword] = useState('Admin@123');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  React.useEffect(() => {
    if (user && activeRole) {
      if (activeRole === 'ADMIN') navigate('/admin/dashboard', { replace: true });
      else if (activeRole === 'LECTURER') navigate('/lecturer/dashboard', { replace: true });
      else navigate('/student/dashboard', { replace: true });
    }
  }, [user, activeRole, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const loggedUser = await login(usernameOrEmail, password);
      if (loggedUser.roles.includes('ADMIN')) {
        navigate('/admin/dashboard');
      } else if (loggedUser.roles.includes('LECTURER')) {
        navigate('/lecturer/dashboard');
      } else {
        navigate('/student/dashboard');
      }
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin tài khoản và mật khẩu.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const fillCredentials = (user: string, pass: string, role: 'ADMIN' | 'LECTURER' | 'STUDENT') => {
    setUsernameOrEmail(user);
    setPassword(pass);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-700 via-indigo-600 to-sky-500 flex items-center justify-center text-white shadow-xl shadow-blue-500/25 font-black text-2xl tracking-wider">
            FA
          </div>
        </div>
        <h2 className="mt-4 text-center text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          FACEATTEND ENTERPRISE
        </h2>
        <p className="mt-1 text-center text-xs text-slate-600 dark:text-slate-400">
          Hệ thống Quản lý Sinh viên & Điểm danh Nhận diện Khuôn mặt AI
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <div className="bg-white dark:bg-slate-900 py-8 px-6 sm:px-10 shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-200/80 dark:border-slate-800 rounded-3xl">
          {error && (
            <div className="mb-5 p-3.5 rounded-xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/60 text-red-700 dark:text-red-300 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                Tài khoản hoặc Email
              </label>
              <input
                type="text"
                required
                value={usernameOrEmail}
                onChange={(e) => setUsernameOrEmail(e.target.value)}
                placeholder="VD: admin, an.nguyen@faceattend.edu.vn"
                className="mt-1.5 w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-slate-900 dark:text-white"
              />
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Mật khẩu
                </label>
                <Link
                  to="/forgot-password"
                  className="text-xs text-blue-600 dark:text-blue-400 hover:underline font-medium"
                >
                  Quên mật khẩu?
                </Link>
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Nhập mật khẩu"
                className="mt-1.5 w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-slate-900 dark:text-white"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl text-sm font-bold shadow-lg shadow-blue-500/25 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <LogIn className="w-4 h-4" />
              {loading ? 'Đang xác thực...' : 'Đăng nhập Hệ thống'}
            </button>
          </form>

          {/* Preset Persona Quick Fill Buttons */}
          <div className="mt-6 pt-6 border-t border-slate-100 dark:border-slate-800">
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2.5 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>Tài khoản trải nghiệm mẫu:</span>
            </div>
            <div className="grid grid-cols-3 gap-2 text-xs">
              <button
                type="button"
                onClick={() => fillCredentials('admin', 'Admin@123', 'ADMIN')}
                className="p-2 rounded-xl bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900/50 text-red-700 dark:text-red-300 hover:bg-red-100 font-semibold flex flex-col items-center gap-1 text-center transition-colors"
              >
                <Shield className="w-4 h-4" />
                <span>Admin</span>
              </button>

              <button
                type="button"
                onClick={() => fillCredentials('gv.an.nguyen', 'Lecturer@123', 'LECTURER')}
                className="p-2 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/50 text-amber-700 dark:text-amber-300 hover:bg-amber-100 font-semibold flex flex-col items-center gap-1 text-center transition-colors"
              >
                <School className="w-4 h-4" />
                <span>Giảng viên</span>
              </button>

              <button
                type="button"
                onClick={() => fillCredentials('sv.b20dccn001', 'Student@123', 'STUDENT')}
                className="p-2 rounded-xl bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-900/50 text-blue-700 dark:text-blue-300 hover:bg-blue-100 font-semibold flex flex-col items-center gap-1 text-center transition-colors"
              >
                <GraduationCap className="w-4 h-4" />
                <span>Sinh viên</span>
              </button>
            </div>
          </div>

          <div className="mt-6 text-center text-xs text-slate-500 dark:text-slate-400">
            Sinh viên chưa kích hoạt tài khoản?{' '}
            <Link to="/register" className="font-semibold text-blue-600 dark:text-blue-400 hover:underline">
              Đăng ký & Nhận OTP Gmail
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
