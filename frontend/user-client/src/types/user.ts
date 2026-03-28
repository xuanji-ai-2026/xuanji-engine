// 用户相关类型
export interface User {
  id: string;
  username: string;
  email: string;
  phone?: string;
  avatar?: string;
  nickname?: string;
  bio?: string;
  createdAt: string;
  updatedAt: string;
  emailVerified?: boolean;
  status: 'active' | 'inactive' | 'suspended';
}

// 用户注册/登录请求
export interface LoginRequest {
  username: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  phone?: string;
  verificationCode?: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  password: string;
  confirmPassword: string;
}

// 用户信息更新
export interface UpdateProfileRequest {
  nickname?: string;
  avatar?: string;
  bio?: string;
  phone?: string;
}

// 认证响应
export interface AuthResponse {
  user: User;
  token: string;
  refreshToken: string;
  expiresIn: number;
}
