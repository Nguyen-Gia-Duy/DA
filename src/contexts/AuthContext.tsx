import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { User, RoleName } from '../types';
import api from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  activeRole: RoleName | null;
  isLoading: boolean;
  login: (usernameOrEmail: string, password: string) => Promise<User>;
  logout: () => void;
  hasRole: (role: RoleName) => boolean;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [activeRole, setActiveRole] = useState<RoleName | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Xác minh phiên qua backend FastAPI (/api/auth/me) khi tải lại trang
  useEffect(() => {
    let isMounted = true;

    const verifySession = async () => {
      const savedToken = localStorage.getItem('faceattend_token');
      if (!savedToken) {
        if (isMounted) {
          setUser(null);
          setToken(null);
          setActiveRole(null);
          setIsLoading(false);
        }
        return;
      }

      try {
        const res = await api.get('/auth/me', {
          headers: {
            Authorization: `Bearer ${savedToken}`,
          },
        });

        const me = res.data;
        if (me && me.id && Array.isArray(me.roles) && isMounted) {
          const verifiedUser: User = {
            id: me.id,
            username: me.username,
            email: me.email,
            full_name: me.full_name,
            phone: me.phone,
            avatar_url: me.avatar_url,
            account_status: me.account_status,
            roles: me.roles,
            student_id: me.student_id,
            lecturer_id: me.lecturer_id,
            created_at: me.created_at,
          };

          setUser(verifiedUser);
          setToken(savedToken);
          // Role chỉ nhận từ backend, ưu tiên role cao nhất
          const primaryRole = me.roles.includes('ADMIN')
            ? 'ADMIN'
            : me.roles.includes('LECTURER')
            ? 'LECTURER'
            : me.roles[0] || 'STUDENT';
          setActiveRole(primaryRole);
        } else {
          throw new Error('Cấu trúc dữ liệu người dùng không hợp lệ');
        }
      } catch (err) {
        // Token không hợp lệ hoặc hết hạn => đăng xuất an toàn
        localStorage.removeItem('faceattend_token');
        localStorage.removeItem('faceattend_user');
        if (isMounted) {
          setUser(null);
          setToken(null);
          setActiveRole(null);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    verifySession();

    return () => {
      isMounted = false;
    };
  }, []);

  const login = async (usernameOrEmail: string, password: string): Promise<User> => {
    setIsLoading(true);
    try {
      const res = await api.post('/auth/login', {
        username_or_email: usernameOrEmail.trim(),
        password: password,
      });

      const data = res.data;
      if (!data || !data.access_token || !Array.isArray(data.roles)) {
        throw new Error('Dữ liệu phản hồi từ máy chủ không hợp lệ.');
      }

      const loggedUser: User = {
        id: data.user_id,
        username: data.username,
        email: data.email,
        full_name: data.full_name,
        account_status: 'ACTIVE',
        roles: data.roles,
        student_id: data.student_id,
        student_code: data.student_code,
        lecturer_id: data.lecturer_id,
        lecturer_code: data.lecturer_code,
        created_at: new Date().toISOString(),
      };

      const primaryRole = loggedUser.roles.includes('ADMIN')
        ? 'ADMIN'
        : loggedUser.roles.includes('LECTURER')
        ? 'LECTURER'
        : loggedUser.roles[0] || 'STUDENT';

      setUser(loggedUser);
      setToken(data.access_token);
      setActiveRole(primaryRole);
      localStorage.setItem('faceattend_token', data.access_token);
      localStorage.removeItem('faceattend_user'); // Không phụ thuộc vào user cache
      return loggedUser;
    } catch (err: any) {
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = useCallback(() => {
    setUser(null);
    setToken(null);
    setActiveRole(null);
    localStorage.removeItem('faceattend_token');
    localStorage.removeItem('faceattend_user');
  }, []);

  const refreshUser = useCallback(async () => {
    const savedToken = localStorage.getItem('faceattend_token');
    if (!savedToken) return;
    try {
      const res = await api.get('/auth/me');
      const me = res.data;
      if (me && me.id) {
        const updatedUser: User = {
          id: me.id,
          username: me.username,
          email: me.email,
          full_name: me.full_name,
          phone: me.phone,
          avatar_url: me.avatar_url,
          account_status: me.account_status,
          roles: me.roles,
          student_id: me.student_id,
          lecturer_id: me.lecturer_id,
          created_at: me.created_at,
        };
        setUser(updatedUser);
        const primaryRole = updatedUser.roles.includes('ADMIN')
          ? 'ADMIN'
          : updatedUser.roles.includes('LECTURER')
          ? 'LECTURER'
          : updatedUser.roles[0] || 'STUDENT';
        setActiveRole(primaryRole);
      }
    } catch (e) {
      logout();
    }
  }, [logout]);

  const hasRole = (role: RoleName): boolean => {
    return user ? user.roles.includes(role) : false;
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        activeRole,
        isLoading,
        login,
        logout,
        hasRole,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
