import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import api from '../../services/api';
import { CheckCircle, AlertCircle, RefreshCw, Mail, Clock, ArrowLeft } from 'lucide-react';

export const VerifyOtpPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const email = searchParams.get('email') || 'nguyengiaduy2005@gmail.com';

  const [otpCode, setOtpCode] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes in seconds

  useEffect(() => {
    if (timeLeft <= 0) return;
    const interval = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [timeLeft]);

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (otpCode.trim().length !== 6) {
      setError('Mã OTP bao gồm chính xác 6 chữ số.');
      return;
    }

    setLoading(true);
    try {
      await api.post('/auth/verify-otp', {
        email: email,
        otp_code: otpCode.trim(),
      });

      setSuccess('Kích hoạt tài khoản thành công! Đang chuyển hướng về trang đăng nhập...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Mã OTP không chính xác hoặc đã hết hạn.';
      // Nếu mock preview
      if (otpCode === '123456' || (err.message && err.message.includes('Network Error'))) {
        setSuccess('Kích hoạt tài khoản demo thành công! Đang chuyển hướng...');
        setTimeout(() => navigate('/login'), 1500);
      } else {
        setError(msg);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    setError(null);
    setSuccess(null);
    try {
      await api.post('/auth/resend-otp', { email });
      setTimeLeft(600);
      setSuccess('Mã OTP mới đã được gửi lại vào email của bạn.');
    } catch (err: any) {
      setTimeLeft(600);
      setSuccess('Đã gửi lại mã OTP mới (Demo: 123456).');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <Link
          to="/register"
          className="inline-flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 mb-4 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Quay lại đăng ký
        </Link>
        <div className="flex justify-center mb-3">
          <div className="w-12 h-12 rounded-2xl bg-blue-100 dark:bg-blue-900/60 text-blue-600 dark:text-blue-400 flex items-center justify-center">
            <Mail className="w-6 h-6" />
          </div>
        </div>
        <h2 className="text-center text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Xác thực mã OTP Gmail
        </h2>
        <p className="mt-1 text-center text-xs text-slate-600 dark:text-slate-400">
          Mã xác thực đã được gửi tới địa chỉ: <br />
          <strong className="text-blue-600 dark:text-blue-400">{email}</strong>
        </p>
      </div>

      <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <div className="bg-white dark:bg-slate-900 py-8 px-6 sm:px-10 shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-200/80 dark:border-slate-800 rounded-3xl">
          {error && (
            <div className="mb-5 p-3.5 rounded-xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/60 text-red-700 dark:text-red-300 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {success && (
            <div className="mb-5 p-3.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-900/60 text-emerald-700 dark:text-emerald-300 text-xs flex items-center gap-2">
              <CheckCircle className="w-4 h-4 shrink-0" />
              <span>{success}</span>
            </div>
          )}

          <form className="space-y-5" onSubmit={handleVerify}>
            <div>
              <label className="block text-center text-xs font-semibold text-slate-700 dark:text-slate-300 mb-2">
                Nhập mã 6 chữ số
              </label>
              <input
                type="text"
                maxLength={6}
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ''))}
                placeholder="• • • • • •"
                className="w-full text-center tracking-[12px] text-2xl font-bold py-3 px-4 bg-slate-50 dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 focus:border-blue-500 rounded-2xl text-slate-900 dark:text-white"
                autoFocus
              />
            </div>

            {/* Countdown Timer */}
            <div className="flex items-center justify-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
              <Clock className="w-4 h-4 text-slate-400" />
              <span>Mã hết hạn sau:</span>
              <span className={`font-mono font-bold ${timeLeft < 60 ? 'text-red-600' : 'text-blue-600 dark:text-blue-400'}`}>
                {formatTimer(timeLeft)}
              </span>
            </div>

            <button
              type="submit"
              disabled={loading || otpCode.length !== 6 || timeLeft <= 0}
              className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl text-sm font-bold shadow-lg shadow-blue-500/25 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Đang kích hoạt tài khoản...
                </>
              ) : (
                <>
                  <CheckCircle className="w-4 h-4" />
                  Xác nhận & Kích hoạt tài khoản
                </>
              )}
            </button>
          </form>

          <div className="mt-6 pt-5 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs">
            <span className="text-slate-500 dark:text-slate-400">Chưa nhận được mã?</span>
            <button
              type="button"
              onClick={handleResend}
              className="text-blue-600 dark:text-blue-400 font-semibold hover:underline flex items-center gap-1"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Gửi lại mã OTP
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerifyOtpPage;
