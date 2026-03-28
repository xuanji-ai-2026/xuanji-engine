import axios from 'axios';
import type {
  Sdk,
  ChangelogEntry,
  IntegrationGuide,
  ApiResponse,
} from '../types';

class SdkService {
  private client = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
    timeout: 30000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // ============================================
  // SDK管理
  // ============================================

  async getSdks(): Promise<ApiResponse<Sdk[]>> {
    const response = await this.client.get('/sdks');
    return response.data;
  }

  async getSdk(id: string): Promise<ApiResponse<Sdk>> {
    const response = await this.client.get(`/sdks/${id}`);
    return response.data;
  }

  async downloadSdk(id: string): Promise<Blob> {
    const response = await this.client.get(`/sdks/${id}/download`, {
      responseType: 'blob',
    });
    return response.data;
  }

  async getSdkChangelog(id: string): Promise<ApiResponse<ChangelogEntry[]>> {
    const response = await this.client.get(`/sdks/${id}/changelog`);
    return response.data;
  }

  // ============================================
  // 集成文档
  // ============================================

  async getIntegrationGuide(sdkId: string): Promise<ApiResponse<IntegrationGuide>> {
    const response = await this.client.get(`/sdks/${sdkId}/guide`);
    return response.data;
  }

  async generateIntegrationCode(sdkId: string, language: string): Promise<ApiResponse<{ code: string }>> {
    const response = await this.client.get(`/sdks/${sdkId}/generate-code`, { params: { language } });
    return response.data;
  }
}

export const sdkService = new SdkService();
