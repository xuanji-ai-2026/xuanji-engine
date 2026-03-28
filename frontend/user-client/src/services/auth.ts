import apiService from './api';
import type {
  LoginRequest,
  RegisterRequest,
  ForgotPasswordRequest,
  ResetPasswordRequest,
  AuthResponse,
  UpdateProfileRequest,
  User,
} from '@/types';
import config from '@/config';

class AuthService {
  // 登录
  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await apiService.post<AuthResponse>('/auth/login', data);
    if (response.data) {
      this.saveAuthData(response.data);
    }
    return response.data as AuthResponse;
  }

  // 注册
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await apiService.post<AuthResponse>('/auth/register', data);
    if (response.data) {
      this.saveAuthData(response.data);
    }
    return response.data as AuthResponse;
  }

  // 登出
  async logout(): Promise<void> {
    try {
      await apiService.post('/auth/logout');
    } finally {
      this.clearAuthData();
    }
  }

  // 忘记密码
  async forgotPassword(data: ForgotPasswordRequest): Promise<void> {
    await apiService.post('/auth/forgot-password', data);
  }

  // 重置密码
  async resetPassword(data: ResetPasswordRequest): Promise<void> {
    await apiService.post('/auth/reset-password', data);
  }

  // 获取当前用户信息
  async getCurrentUser(): Promise<User> {
    const response = await apiService.get<User>('/auth/me');
    return response.data as User;
  }

  // 更新用户信息
  async updateProfile(data: UpdateProfileRequest): Promise<User> {
    const response = await apiService.patch<User>('/auth/profile', data);
    const updatedUser = response.data as User;
    localStorage.setItem(config.auth.userKey, JSON.stringify(updatedUser));
    return updatedUser;
  }

  // 修改密码
  async changePassword(data: {
    oldPassword: string;
    newPassword: string;
  }): Promise<void> {
    await apiService.post('/auth/change-password', data);
  }

  // 刷新Token
  async refreshToken(): Promise<AuthResponse> {
    const refreshToken = localStorage.getItem(config.auth.refreshTokenKey);
    const response = await apiService.post<AuthResponse>('/auth/refresh', {
      refreshToken,
    });
    if (response.data) {
      this.saveAuthData(response.data);
    }
    return response.data as AuthResponse;
  }

  // 验证邮箱
  async verifyEmail(token: string): Promise<void> {
    await apiService.post('/auth/verify-email', { token });
  }

  // 发送验证码
  async sendVerificationCode(email: string): Promise<void> {
    await apiService.post('/auth/send-verification-code', { email });
  }

  // 保存认证数据
  private saveAuthData(data: AuthResponse): void {
    localStorage.setItem(config.auth.tokenKey, data.token);
    localStorage.setItem(config.auth.refreshTokenKey, data.refreshToken);
    localStorage.setItem(config.auth.userKey, JSON.stringify(data.user));
  }

  // 清除认证数据
  private clearAuthData(): void {
    localStorage.removeItem(config.auth.tokenKey);
    localStorage.removeItem(config.auth.refreshTokenKey);
    localStorage.removeItem(config.auth.userKey);
  }

  // 从本地存储获取用户信息
  getLocalUser(): User | null {
    const userStr = localStorage.getItem(config.auth.userKey);
    return userStr ? JSON.parse(userStr) : null;
  }

  // 检查是否已认证
  isAuthenticated(): boolean {
    return !!localStorage.getItem(config.auth.tokenKey);
  }
}

export const authService = new AuthService();
export default authService;
