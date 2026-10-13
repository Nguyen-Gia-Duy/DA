import React from 'react';
import { Link } from 'react-router-dom';
import { Home, ShieldAlert } from 'lucide-react';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col items-center justify-center p-6 text-center">
      <div className="w-16 h-16 rounded-3xl bg-blue-100 dark:bg-blue-900/50 text-blue-600 flex items-center justify-center font-black text-2xl mb-4">
        404
      </div>
      <h1 className="text-xl font-bold text-slate-900 dark:text-white">Không tìm thấy trang yêu cầu</h1>
      <p className="text-xs text-slate-500 mt-1 max-w-sm">
        Đường dẫn bạn đang truy cập không tồn tại hoặc đã bị di chuyển.
      </p>
      <Link
        to="/"
        className="mt-6 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold flex items-center gap-2"
      >
        <Home className="w-4 h-4" /> Về trang chủ
      </Link>
    </div>
  );
};

export const UnauthorizedPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col items-center justify-center p-6 text-center">
      <ShieldAlert className="w-16 h-16 text-red-500 mb-4" />
      <h1 className="text-xl font-bold text-slate-900 dark:text-white">Truy cập bị từ chối (403 Forbidden)</h1>
      <p className="text-xs text-slate-500 mt-1 max-w-sm">
        Tài khoản của bạn không có quyền truy cập vào phân hệ này. Vui lòng chuyển vai trò tương ứng trên thanh điều hướng.
      </p>
      <Link
        to="/"
        className="mt-6 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold flex items-center gap-2"
      >
        <Home className="w-4 h-4" /> Về trang tổng quan
      </Link>
    </div>
  );
};
