import axios from 'axios';
import type {
  Plugin,
  PluginConfig,
  PluginDependency,
  PluginTestResult,
  PluginTemplate,
  PluginLogEntry,
  CodeSnippet,
  ApiResponse,
  PaginatedResponse,
  PaginationParams,
} from '../types';

class PluginService {
  private client = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
    timeout: 30000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // ============================================
  // 插件管理
  // ============================================

  async getPlugins(params?: PaginationParams & { status?: string }): Promise<ApiResponse<PaginatedResponse<Plugin>>> {
    const response = await this.client.get('/plugins', { params });
    return response.data;
  }

  async getPlugin(id: string): Promise<ApiResponse<Plugin>> {
    const response = await this.client.get(`/plugins/${id}`);
    return response.data;
  }

  async createPlugin(data: Partial<Plugin>): Promise<ApiResponse<Plugin>> {
    const response = await this.client.post('/plugins', data);
    return response.data;
  }

  async updatePlugin(id: string, data: Partial<Plugin>): Promise<ApiResponse<Plugin>> {
    const response = await this.client.put(`/plugins/${id}`, data);
    return response.data;
  }

  async deletePlugin(id: string): Promise<ApiResponse<void>> {
    const response = await this.client.delete(`/plugins/${id}`);
    return response.data;
  }

  async uploadPlugin(id: string, file: File): Promise<ApiResponse<void>> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await this.client.post(`/plugins/${id}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async submitForReview(id: string): Promise<ApiResponse<void>> {
    const response = await this.client.post(`/plugins/${id}/submit`);
    return response.data;
  }

  // ============================================
  // 插件配置
  // ============================================

  async getPluginConfig(pluginId: string): Promise<ApiResponse<PluginConfig>> {
    const response = await this.client.get(`/plugins/${pluginId}/config`);
    return response.data;
  }

  async updatePluginConfig(pluginId: string, config: Record<string, any>): Promise<ApiResponse<PluginConfig>> {
    const response = await this.client.put(`/plugins/${pluginId}/config`, { config });
    return response.data;
  }

  // ============================================
  // 插件依赖
  // ============================================

  async getPluginDependencies(pluginId: string): Promise<ApiResponse<PluginDependency[]>> {
    const response = await this.client.get(`/plugins/${pluginId}/dependencies`);
    return response.data;
  }

  async installDependency(pluginId: string, dependency: string): Promise<ApiResponse<void>> {
    const response = await this.client.post(`/plugins/${pluginId}/dependencies`, { dependency });
    return response.data;
  }

  async checkDependencies(pluginId: string): Promise<ApiResponse<{ compatible: boolean; issues: string[] }>> {
    const response = await this.client.get(`/plugins/${pluginId}/dependencies/check`);
    return response.data;
  }

  // ============================================
  // 插件测试
  // ============================================

  async runTest(pluginId: string, testType: 'unit' | 'integration' | 'performance'): Promise<ApiResponse<PluginTestResult>> {
    const response = await this.client.post(`/plugins/${pluginId}/test`, { testType });
    return response.data;
  }

  async getTestResults(pluginId: string): Promise<ApiResponse<PluginTestResult[]>> {
    const response = await this.client.get(`/plugins/${pluginId}/tests`);
    return response.data;
  }

  // ============================================
  // 插件日志
  // ============================================

  async getPluginLogs(pluginId: string, params?: { level?: string; limit?: number }): Promise<ApiResponse<PluginLogEntry[]>> {
    const response = await this.client.get(`/plugins/${pluginId}/logs`, { params });
    return response.data;
  }

  async clearPluginLogs(pluginId: string): Promise<ApiResponse<void>> {
    const response = await this.client.delete(`/plugins/${pluginId}/logs`);
    return response.data;
  }

  // ============================================
  // 插件模板
  // ============================================

  async getTemplates(): Promise<ApiResponse<PluginTemplate[]>> {
    const response = await this.client.get('/plugins/templates');
    return response.data;
  }

  async getTemplate(id: string): Promise<ApiResponse<PluginTemplate>> {
    const response = await this.client.get(`/plugins/templates/${id}`);
    return response.data;
  }

  async createPluginFromTemplate(templateId: string, name: string): Promise<ApiResponse<Plugin>> {
    const response = await this.client.post('/plugins/from-template', { templateId, name });
    return response.data;
  }

  // ============================================
  // 代码片段
  // ============================================

  async getCodeSnippets(): Promise<ApiResponse<CodeSnippet[]>> {
    const response = await this.client.get('/plugins/snippets');
    return response.data;
  }

  async createCodeSnippet(data: Partial<CodeSnippet>): Promise<ApiResponse<CodeSnippet>> {
    const response = await this.client.post('/plugins/snippets', data);
    return response.data;
  }

  async deleteCodeSnippet(id: string): Promise<ApiResponse<void>> {
    const response = await this.client.delete(`/plugins/snippets/${id}`);
    return response.data;
  }

  // ============================================
  // 插件市场
  // ============================================

  async searchMarketplace(query: string, params?: PaginationParams): Promise<ApiResponse<PaginatedResponse<Plugin>>> {
    const response = await this.client.get('/plugins/marketplace/search', { params: { query, ...params } });
    return response.data;
  }

  async installPlugin(id: string): Promise<ApiResponse<void>> {
    const response = await this.client.post(`/plugins/marketplace/${id}/install`);
    return response.data;
  }

  async uninstallPlugin(id: string): Promise<ApiResponse<void>> {
    const response = await this.client.delete(`/plugins/marketplace/${id}/uninstall`);
    return response.data;
  }

  async updatePluginVersion(id: string): Promise<ApiResponse<void>> {
    const response = await this.client.post(`/plugins/marketplace/${id}/update`);
    return response.data;
  }
}

export const pluginService = new PluginService();
