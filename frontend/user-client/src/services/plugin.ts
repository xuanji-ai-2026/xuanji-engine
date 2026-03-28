import apiService from './api';
import type {
  Plugin,
  InstalledPlugin,
  InstallPluginRequest,
  PluginReview,
  PaginationRequest,
  PaginationResponse,
} from '@/types';

class PluginService {
  // 插件市场

  // 获取插件列表
  async getPluginList(
    params: PaginationRequest
  ): Promise<PaginationResponse<Plugin>> {
    const response = await apiService.get<PaginationResponse<Plugin>>(
      '/plugins/market',
      { params }
    );
    return response.data as PaginationResponse<Plugin>;
  }

  // 获取单个插件详情
  async getPlugin(id: string): Promise<Plugin> {
    const response = await apiService.get<Plugin>(`/plugins/market/${id}`);
    return response.data as Plugin;
  }

  // 搜索插件
  async searchPlugins(query: string, params?: PaginationRequest): Promise<PaginationResponse<Plugin>> {
    const response = await apiService.get<PaginationResponse<Plugin>>(
      '/plugins/market/search',
      { params: { ...params, query } }
    );
    return response.data as PaginationResponse<Plugin>;
  }

  // 获取插件评论
  async getPluginReviews(
    pluginId: string,
    params?: PaginationRequest
  ): Promise<PaginationResponse<PluginReview>> {
    const response = await apiService.get<PaginationResponse<PluginReview>>(
      `/plugins/market/${pluginId}/reviews`,
      { params }
    );
    return response.data as PaginationResponse<PluginReview>;
  }

  // 添加评论
  async addReview(
    pluginId: string,
    data: { rating: number; title?: string; content: string }
  ): Promise<PluginReview> {
    const response = await apiService.post<PluginReview>(
      `/plugins/market/${pluginId}/reviews`,
      data
    );
    return response.data as PluginReview;
  }

  // 已安装插件

  // 获取已安装插件列表
  async getInstalledPlugins(
    params?: PaginationRequest
  ): Promise<PaginationResponse<InstalledPlugin>> {
    const response = await apiService.get<PaginationResponse<InstalledPlugin>>(
      '/plugins/installed',
      { params }
    );
    return response.data as PaginationResponse<InstalledPlugin>;
  }

  // 安装插件
  async installPlugin(data: InstallPluginRequest): Promise<InstalledPlugin> {
    const response = await apiService.post<InstalledPlugin>('/plugins/install', data);
    return response.data as InstalledPlugin;
  }

  // 卸载插件
  async uninstallPlugin(pluginId: string): Promise<void> {
    await apiService.delete(`/plugins/installed/${pluginId}`);
  }

  // 启用插件
  async enablePlugin(pluginId: string): Promise<InstalledPlugin> {
    const response = await apiService.post(`/plugins/installed/${pluginId}/enable`);
    return response.data as InstalledPlugin;
  }

  // 禁用插件
  async disablePlugin(pluginId: string): Promise<InstalledPlugin> {
    const response = await apiService.post(`/plugins/installed/${pluginId}/disable`);
    return response.data as InstalledPlugin;
  }

  // 更新插件
  async updatePlugin(pluginId: string): Promise<InstalledPlugin> {
    const response = await apiService.post(`/plugins/installed/${pluginId}/update`);
    return response.data as InstalledPlugin;
  }

  // 配置插件
  async configurePlugin(
    pluginId: string,
    settings: Record<string, unknown>
  ): Promise<InstalledPlugin> {
    const response = await apiService.patch(`/plugins/installed/${pluginId}/settings`, {
      settings,
    });
    return response.data as InstalledPlugin;
  }

  // 获取插件配置
  async getPluginSettings(pluginId: string): Promise<Record<string, unknown>> {
    const response = await apiService.get(`/plugins/installed/${pluginId}/settings`);
    return response.data as Record<string, unknown>;
  }

  // 获取插件分类
  async getCategories(): Promise<string[]> {
    const response = await apiService.get<string[]>('/plugins/categories');
    return response.data as string[];
  }
}

export const pluginService = new PluginService();
export default pluginService;
