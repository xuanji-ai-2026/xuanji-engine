/**
 * 邮箱验证
 */
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * 手机号验证（中国大陆）
 */
export function validatePhone(phone: string): boolean {
  const phoneRegex = /^1[3-9]\d{9}$/;
  return phoneRegex.test(phone);
}

/**
 * 密码强度验证
 */
export function validatePassword(password: string): {
  valid: boolean;
  strength: 'weak' | 'medium' | 'strong';
  message: string;
} {
  if (password.length < 8) {
    return {
      valid: false,
      strength: 'weak',
      message: '密码长度至少8位',
    };
  }

  let score = 0;
  if (/[a-z]/.test(password)) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/\d/.test(password)) score++;
  if (/[^a-zA-Z0-9]/.test(password)) score++;

  if (score < 2) {
    return {
      valid: false,
      strength: 'weak',
      message: '密码强度太弱，建议包含大小写字母、数字和特殊字符',
    };
  }

  if (score < 4) {
    return {
      valid: true,
      strength: 'medium',
      message: '密码强度中等',
    };
  }

  return {
    valid: true,
    strength: 'strong',
    message: '密码强度很好',
  };
}

/**
 * 用户名验证
 */
export function validateUsername(username: string): boolean {
  // 4-20位，字母、数字、下划线
  const usernameRegex = /^[a-zA-Z0-9_]{4,20}$/;
  return usernameRegex.test(username);
}

/**
 * URL验证
 */
export function validateUrl(url: string): boolean {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

/**
 * 验证码验证
 */
export function validateCode(code: string, length: number = 6): boolean {
  return /^\d+$/.test(code) && code.length === length;
}

/**
 * 文件大小验证
 */
export function validateFileSize(
  file: File,
  maxSize: number
): { valid: boolean; message?: string } {
  if (file.size > maxSize) {
    return {
      valid: false,
      message: `文件大小不能超过 ${(maxSize / 1024 / 1024).toFixed(2)}MB`,
    };
  }
  return { valid: true };
}

/**
 * 文件类型验证
 */
export function validateFileType(
  file: File,
  allowedTypes: string[]
): { valid: boolean; message?: string } {
  if (!allowedTypes.some((type) => file.type.match(type.replace('*', '.*')))) {
    return {
      valid: false,
      message: '不支持的文件类型',
    };
  }
  return { valid: true };
}

/**
 * 必填验证
 */
export function validateRequired(value: unknown): boolean {
  if (value === null || value === undefined) return false;
  if (typeof value === 'string') return value.trim().length > 0;
  if (Array.isArray(value)) return value.length > 0;
  return true;
}

/**
 * 最小值验证
 */
export function validateMin(value: number, min: number): boolean {
  return value >= min;
}

/**
 * 最大值验证
 */
export function validateMax(value: number, max: number): boolean {
  return value <= max;
}

/**
 * 长度验证
 */
export function validateLength(value: string, min: number, max: number): boolean {
  return value.length >= min && value.length <= max;
}

/**
 * 正则表达式验证
 */
export function validatePattern(value: string, pattern: RegExp): boolean {
  return pattern.test(value);
}
