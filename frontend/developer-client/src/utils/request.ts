import axios, { AxiosError } from 'axios';

export interface ApiError {
  message: string;
  code?: string;
  details?: any;
}

export function handleApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ message: string; code?: string }>;
    if (axiosError.response?.data) {
      return {
        message: axiosError.response.data.message || '请求失败',
        code: axiosError.response.data.code,
        details: axiosError.response.data,
      };
    }
    if (axiosError.message) {
      return { message: axiosError.message };
    }
  }
  if (error instanceof Error) {
    return { message: error.message };
  }
  return { message: '未知错误' };
}

export async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  delay = 1000
): Promise<T> {
  let lastError: Error | undefined;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (i < maxRetries - 1) {
        await new Promise((resolve) => setTimeout(resolve, delay * (i + 1)));
      }
    }
  }

  throw lastError || new Error('请求失败');
}
