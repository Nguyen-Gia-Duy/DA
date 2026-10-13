import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

export const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Request interceptor: Gắn JWT Token vào Header Bearer
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('faceattend_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Nếu dev server trả về HTML (index.html fallback) thay vì JSON API
    if (typeof response.data === 'string' && response.data.trim().startsWith('<')) {
      const error = new AxiosError(
        'Máy chủ API chưa khởi động hoặc trả về HTML thay vì dữ liệu JSON.',
        'ERR_BAD_RESPONSE',
        response.config,
        response.request,
        response
      );
      return Promise.reject(error);
    }
    return response;
  },
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Khi token hết hạn hoặc không hợp lệ
      const currentPath = window.location.pathname;
      if (!currentPath.includes('/login') && !currentPath.includes('/register')) {
        localStorage.removeItem('faceattend_token');
        localStorage.removeItem('faceattend_user');
      }
    }
    return Promise.reject(error);
  }
);

export default api;
