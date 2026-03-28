/**
 * 小灵（Xiaoling）适配层核心类
 * 提供管理端智能助手的完整功能接口
 */

import { XiaolingConfig, defaultConfig } from '../config/xiaoling.config';
import type {
  Response,
  SystemStatus,
  ServiceStatus,
  PerformanceMetrics,
  ServiceControlParams,
  UserActivity,
  ActivityAnalytics,
  OperationStrategy,
  ReportConfig,
  ThemeConfig,
  LayoutConfig,
  UIPreviewConfig,
  UserInfo,
  UserBehavior,
  BatchUserOperation,
  StatisticsQuery,
  StatisticsPoint,
  TrendAnalysis,
  CustomReport,
} from '../types/xiaoling.types';

export class XiaolingAdapter {
  private config: XiaolingConfig;
  private wsConnection: WebSocket | null = null;
  private cache: Map<string, { data: any; expiry: number }> = new Map();
  private reconnectAttempts = 0;
  private eventHandlers: Map<string, Set<Function>> = new Map();

  constructor(config?: Partial<XiaolingConfig>) {
    this.config = { ...defaultConfig, ...config };
    this.initializeWebSocket();
  }

  // ==================== WebSocket 连接管理 ====================

  private initializeWebSocket(): void {
    if (!this.config.websocket.enabled) {
      return;
    }

    try {
      this.wsConnection = new WebSocket(this.config.websocket.url);

      this.wsConnection.onopen = () => {
        this.log('info', 'WebSocket connected');
        this.reconnectAttempts = 0;
        this.emit('connected');
      };

      this.wsConnection.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleWebSocketMessage(data);
        } catch (error) {
          this.log('error', 'Failed to parse WebSocket message', error);
        }
      };

      this.wsConnection.onerror = (error) => {
        this.log('error', 'WebSocket error', error);
        this.emit('error', error);
      };

      this.wsConnection.onclose = () => {
        this.log('warn', 'WebSocket disconnected');
        this.emit('disconnected');
        this.scheduleReconnect();
      };
    } catch (error) {
      this.log('error', 'Failed to initialize WebSocket', error);
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= this.config.websocket.maxRetries) {
      this.log('error', 'Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    setTimeout(() => {
      this.log('info', `Attempting reconnection (${this.reconnectAttempts}/${this.config.websocket.maxRetries})`);
      this.initializeWebSocket();
    }, this.config.websocket.reconnectInterval);
  }

  private handleWebSocketMessage(data: any): void {
    const { type, payload } = data;
    this.emit(type, payload);
  }

  // ==================== 事件系统 ====================

  on(event: string, handler: Function): void {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, new Set());
    }
    this.eventHandlers.get(event)!.add(handler);
  }

  off(event: string, handler: Function): void {
    const handlers = this.eventHandlers.get(event);
    if (handlers) {
      handlers.delete(handler);
    }
  }

  private emit(event: string, data?: any): void {
    const handlers = this.eventHandlers.get(event);
    if (handlers) {
      handlers.forEach((handler) => handler(data));
    }
  }

  // ==================== 缓存管理 ====================

  private setCache(key: string, data: any): void {
    if (!this.config.cache.enabled) {
      return;
    }

    const expiry = Date.now() + this.config.cache.ttl * 1000;

    if (this.cache.size >= this.config.cache.maxSize) {
      const firstKey = this.cache.keys().next().value;
      if (firstKey) {
        this.cache.delete(firstKey);
      }
    }

    this.cache.set(key, { data, expiry });
  }

  private getCache<T>(key: string): T | null {
    const cached = this.cache.get(key);
    if (!cached) {
      return null;
    }

    if (Date.now() > cached.expiry) {
      this.cache.delete(key);
      return null;
    }

    return cached.data as T;
  }

  private clearCache(pattern?: string): void {
    if (!pattern) {
      this.cache.clear();
      return;
    }

    for (const key of this.cache.keys()) {
      if (key.includes(pattern)) {
        this.cache.delete(key);
      }
    }
  }

  // ==================== HTTP API 请求 ====================

  private async httpRequest<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<Response<T>> {
    const url = `${this.config.http.baseUrl}${endpoint}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(
      () => controller.abort(),
      this.config.http.timeout
    );

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      clearTimeout(timeoutId);

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: {
            code: response.status.toString(),
            message: data.message || 'Request failed',
            details: data,
          },
          timestamp: Date.now(),
        };
      }

      return {
        success: true,
        data: data as T,
        timestamp: Date.now(),
      };
    } catch (error) {
      clearTimeout(timeoutId);
      this.log('error', `HTTP request failed: ${endpoint}`, error);

      return {
        success: false,
        error: {
          code: 'NETWORK_ERROR',
          message: error instanceof Error ? error.message : 'Unknown error',
        },
        timestamp: Date.now(),
      };
    }
  }

  // ==================== 日志系统 ====================

  private log(level: 'debug' | 'info' | 'warn' | 'error', message: string, data?: any): void {
    if (!this.config.logging.enableConsole) {
      return;
    }

    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] [Xiaoling] [${level.toUpperCase()}] ${message}`;

    switch (level) {
      case 'debug':
        if (this.config.logging.level === 'debug') {
          console.debug(logMessage, data);
        }
        break;
      case 'info':
        if (['debug', 'info'].includes(this.config.logging.level)) {
          console.info(logMessage, data);
        }
        break;
      case 'warn':
        if (['debug', 'info', 'warn'].includes(this.config.logging.level)) {
          console.warn(logMessage, data);
        }
        break;
      case 'error':
        console.error(logMessage, data);
        break;
    }
  }

  // ==================== 系统总控接口 ====================

  /**
   * 获取系统状态
   */
  async getSystemStatus(): Promise<Response<SystemStatus>> {
    const cacheKey = 'system:status';
    const cached = this.getCache<SystemStatus>(cacheKey);

    if (cached) {
      return { success: true, data: cached, timestamp: Date.now() };
    }

    const result = await this.httpRequest<SystemStatus>('/system/status');

    if (result.success && result.data) {
      this.setCache(cacheKey, result.data);
    }

    return result;
  }

  /**
   * 获取所有服务状态
   */
  async getServiceStatuses(): Promise<Response<ServiceStatus[]>> {
    return this.httpRequest<ServiceStatus[]>('/system/services');
  }

  /**
   * 获取单个服务状态
   */
  async getServiceStatus(serviceName: string): Promise<Response<ServiceStatus>> {
    return this.httpRequest<ServiceStatus>(`/system/services/${serviceName}`);
  }

  /**
   * 控制服务启停
   */
  async controlService(
    params: ServiceControlParams
  ): Promise<Response<{ success: boolean; message: string }>> {
    this.clearCache('system:status');
    return this.httpRequest('/system/control', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  /**
   * 获取性能指标
   */
  async getPerformanceMetrics(
    period?: { start: number; end: number }
  ): Promise<Response<PerformanceMetrics[]>> {
    const endpoint = period
      ? `/system/metrics?start=${period.start}&end=${period.end}`
      : '/system/metrics';

    return this.httpRequest<PerformanceMetrics[]>(endpoint);
  }

  // ==================== 运营管理协助 ====================

  /**
   * 获取用户活跃度数据
   */
  async getUserActivities(
    period: { start: number; end: number }
  ): Promise<Response<UserActivity[]>> {
    return this.httpRequest<UserActivity[]>(
      `/operations/activities?start=${period.start}&end=${period.end}`
    );
  }

  /**
   * 获取活跃度分析
   */
  async getActivityAnalytics(
    period: 'daily' | 'weekly' | 'monthly'
  ): Promise<Response<ActivityAnalytics>> {
    return this.httpRequest<ActivityAnalytics>(
      `/operations/analytics/${period}`
    );
  }

  /**
   * 获取运营策略建议
   */
  async getOperationStrategies(
    category?: string
  ): Promise<Response<OperationStrategy[]>> {
    const endpoint = category
      ? `/operations/strategies?category=${category}`
      : '/operations/strategies';

    return this.httpRequest<OperationStrategy[]>(endpoint);
  }

  /**
   * 生成数据报表
   */
  async generateReport(config: ReportConfig): Promise<Response<{ url: string; id: string }>> {
    return this.httpRequest('/operations/reports', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  }

  // ==================== UI配置协助 ====================

  /**
   * 获取主题配置
   */
  async getTheme(themeId: string): Promise<Response<ThemeConfig>> {
    return this.httpRequest<ThemeConfig>(`/ui/themes/${themeId}`);
  }

  /**
   * 获取所有主题
   */
  async getThemes(): Promise<Response<ThemeConfig[]>> {
    return this.httpRequest<ThemeConfig[]>('/ui/themes');
  }

  /**
   * 更新主题配置
   */
  async updateTheme(themeId: string, config: Partial<ThemeConfig>): Promise<Response<ThemeConfig>> {
    return this.httpRequest<ThemeConfig>(`/ui/themes/${themeId}`, {
      method: 'PATCH',
      body: JSON.stringify(config),
    });
  }

  /**
   * 获取布局配置
   */
  async getLayout(layoutName: string): Promise<Response<LayoutConfig>> {
    return this.httpRequest<LayoutConfig>(`/ui/layouts/${layoutName}`);
  }

  /**
   * 获取所有布局
   */
  async getLayouts(): Promise<Response<LayoutConfig[]>> {
    return this.httpRequest<LayoutConfig[]>('/ui/layouts');
  }

  /**
   * 更新布局配置
   */
  async updateLayout(layoutName: string, config: Partial<LayoutConfig>): Promise<Response<LayoutConfig>> {
    return this.httpRequest<LayoutConfig>(`/ui/layouts/${layoutName}`, {
      method: 'PATCH',
      body: JSON.stringify(config),
    });
  }

  /**
   * 预览UI效果
   */
  async previewUI(config: UIPreviewConfig): Promise<Response<{ screenshot: string; html: string }>> {
    return this.httpRequest('/ui/preview', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  }

  // ==================== 用户管理协助 ====================

  /**
   * 获取用户信息
   */
  async getUserInfo(userId: string): Promise<Response<UserInfo>> {
    return this.httpRequest<UserInfo>(`/users/${userId}`);
  }

  /**
   * 搜索用户
   */
  async searchUsers(
    query: string,
    filters?: Record<string, any>
  ): Promise<Response<UserInfo[]>> {
    const params = new URLSearchParams({ query, ...filters });
    return this.httpRequest<UserInfo[]>(`/users/search?${params.toString()}`);
  }

  /**
   * 获取用户行为分析
   */
  async getUserBehavior(userId: string): Promise<Response<UserBehavior>> {
    return this.httpRequest<UserBehavior>(`/users/${userId}/behavior`);
  }

  /**
   * 批量用户操作
   */
  async batchUserOperation(
    operation: BatchUserOperation
  ): Promise<Response<{ processed: number; failed: number; results: any[] {}}>> {
    return this.httpRequest('/users/batch', {
      method: 'POST',
      body: JSON.stringify(operation),
    });
  }

  /**
   * 获取用户列表（分页）
   */
  async getUserList(page: number, pageSize: number, filters?: Record<string, any>): Promise<Response<{
    items: UserInfo[];
    total: number;
    page: number;
    pageSize: number;
  }>> {
    const params = new URLSearchParams({
      page: page.toString(),
      pageSize: pageSize.toString(),
      ...filters,
    });

    return this.httpRequest(`/users?${params.toString()}`);
  }

  // ==================== 数据统计协助 ====================

  /**
   * 查询统计数据
   */
  async queryStatistics(
    query: StatisticsQuery
  ): Promise<Response<StatisticsPoint[]>> {
    return this.httpRequest<StatisticsPoint[]>('/statistics/query', {
      method: 'POST',
      body: JSON.stringify(query),
    });
  }

  /**
   * 获取趋势分析
   */
  async getTrendAnalysis(
    metric: string,
    period: { start: number; end: number }
  ): Promise<Response<TrendAnalysis>> {
    return this.httpRequest<TrendAnalysis>(
      `/statistics/trend/${metric}?start=${period.start}&end=${period.end}`
    );
  }

  /**
   * 创建自定义报表
   */
  async createCustomReport(report: Omit<CustomReport, 'id'>): Promise<Response<CustomReport>> {
    return this.httpRequest<CustomReport>('/statistics/reports', {
      method: 'POST',
      body: JSON.stringify(report),
    });
  }

  /**
   * 获取自定义报表
   */
  async getCustomReport(reportId: string): Promise<Response<CustomReport>> {
    return this.httpRequest<CustomReport>(`/statistics/reports/${reportId}`);
  }

  /**
   * 获取所有自定义报表
   */
  async getCustomReports(): Promise<Response<CustomReport[]>> {
    return this.httpRequest<CustomReport[]>('/statistics/reports');
  }

  /**
   * 更新自定义报表
   */
  async updateCustomReport(
    reportId: string,
    report: Partial<CustomReport>
  ): Promise<Response<CustomReport>> {
    return this.httpRequest<CustomReport>(`/statistics/reports/${reportId}`, {
      method: 'PATCH',
      body: JSON.stringify(report),
    });
  }

  /**
   * 删除自定义报表
   */
  async deleteCustomReport(reportId: string): Promise<Response<{ success: boolean }>> {
    return this.httpRequest(`/statistics/reports/${reportId}`, {
      method: 'DELETE',
    });
  }

  // ==================== 工具方法 ====================

  /**
   * 测试连接
   */
  async testConnection(): Promise<Response<{ connected: boolean; latency: number }>> {
    const start = Date.now();

    try {
      const result = await this.getSystemStatus();
      const latency = Date.now() - start;

      return {
        success: true,
        data: {
          connected: result.success,
          latency,
        },
        timestamp: Date.now(),
      };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'CONNECTION_ERROR',
          message: error instanceof Error ? error.message : 'Unknown error',
        },
        timestamp: Date.now(),
      };
    }
  }

  /**
   * 清理资源
   */
  destroy(): void {
    if (this.wsConnection) {
      this.wsConnection.close();
      this.wsConnection = null;
    }

    this.cache.clear();
    this.eventHandlers.clear();

    this.log('info', 'Xiaoling adapter destroyed');
  }
}

export default XiaolingAdapter;
