import axios, { AxiosInstance, AxiosResponse } from 'axios';
import type {
  ApiKey,
  CallStatistics,
  CallTrend,
  ApiDocument,
  DebugRequest,
  ApiResponse,
  PaginatedResponse,
  PaginationParams,
} from '../types';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 请求拦截器
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // 响应拦截器
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // 未授权，跳转登录
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // ============================================
  // API密钥管理
  // ============================================

  async getApiKeys(params?: PaginationParams): Promise<ApiResponse<PaginatedResponse<ApiKey>>> {
    const response = await this.client.get('/api-keys', { params });
    return response.data;
  }

  async createApiKey(data: { name: string; permissions: string[] }): Promise<ApiResponse<ApiKey>> {
    const response = await this.client.post('/api-keys', data);
    return response.data;
  }

  async updateApiKey(id: string, data: Partial<ApiKey>): Promise<ApiResponse<ApiKey>> {
    const response = await this.client.put(`/api-keys/${id}`, data);
    return response.data;
  }

  async deleteApiKey(id: string): Promise<ApiResponse<void>> {
    const response = await this.client.delete(`/api-keys/${id}`);
    return response.data;
  }

  async revokeApiKey(id: string): Promise<ApiResponse<void>> {
    const response = await this.client.post(`/api-keys/${id}/revoke`);
    return response.data;
  }

  // ============================================
  // 调用统计
  // ============================================

  async getStatistics(period: string): Promise<ApiResponse<CallStatistics>> {
    const response = await this.client.get('/statistics', { params: { period } });
    return response.data;
  }

  async getCallTrends(period: string): Promise<ApiResponse<CallTrend[]>> {
    const response = await this.client.get('/statistics/trends', { params: { period } });
    return response.data;
  }

  // ============================================
  // 调试工具
  // ============================================

  async sendDebugRequest(data: {
    method: string;
    url: string;
    headers?: Record<string, string>;
    body?: any;
  }): Promise<ApiResponse<DebugRequest>> {
    const response = await this.client.post('/debug/send', data);
    return response.data;
  }

  async getDebugHistory(params?: PaginationParams): Promise<ApiResponse<PaginatedResponse<DebugRequest>>> {
    const response = await this.client.get('/debug/history', { params });
    return response.data;
  }

  // ============================================
  // API文档
  // ============================================

  async getApiDocuments(): Promise<ApiResponse<ApiDocument[]>> {
    const response = await this.client.get('/documents');
    return response.data;
  }

  async getApiDocument(id: string): Promise<ApiResponse<ApiDocument>> {
    const response = await this.client.get(`/documents/${id}`);
    return response.data;
  }

  async generateExampleCode(endpointId: string, language: string): Promise<ApiResponse<any>> {
    const response = await this.client.get(`/documents/${endpointId}/example`, { params: { language } });
    return response.data;
  }
}

export const apiService = new ApiService();
