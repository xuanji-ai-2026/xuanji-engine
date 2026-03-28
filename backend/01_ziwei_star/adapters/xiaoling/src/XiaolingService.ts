/**
 * 小灵（Xiaoling）模拟服务端实现
 * 用于演示和测试适配层功能
 */

import type {
  Response,
  SystemStatus,
  ServiceStatus,
  PerformanceMetrics,
  UserActivity,
  ActivityAnalytics,
  OperationStrategy,
  ThemeConfig,
  LayoutConfig,
  UserInfo,
  UserBehavior,
  StatisticsPoint,
  TrendingAnalysis,
  CustomReport,
} from '../types/xiaoling.types';

export class XiaolingService {
  private services: Map<string, ServiceStatus> = new Map();
  private users: Map<string, UserInfo> = new Map();
  private reports: Map<string, CustomReport> = new Map();

  constructor() {
    this.initializeMockData();
  }

  // ==================== 初始化模拟数据 ====================

  private initializeMockData(): void {
    // 初始化服务状态
    this.services.set('api-gateway', {
      name: 'api-gateway',
      status: 'running',
      cpu: 45.2,
      memory: 52.8,
      connections: 1243,
    });

    this.services.set('auth-service', {
      name: 'auth-service',
      status: 'running',
      cpu: 23.7,
      memory: 38.2,
      connections: 456,
    });

    this.services.set('user-service', {
      name: 'user-service',
      status: 'running',
      cpu: 56.3,
      memory: 67.5,
      connections: 892,
    });

    this.services.set('data-service', {
      name: 'data-service',
      status: 'running',
      cpu: 34.1,
      memory: 45.9,
      connections: 678,
    });

    // 初始化模拟用户
    this.users.set('user-001', {
      id: 'user-001',
      username: 'zhangsan',
      email: 'zhangsan@example.com',
      role: 'admin',
      status: 'active',
      createdAt: Date.now() - 86400000 * 30,
      lastLogin: Date.now() - 3600000,
    });

    this.users.set('user-002', {
      id: 'user-002',
      username: 'lisi',
      email: 'lisi@example.com',
      role: 'user',
      status: 'active',
      createdAt: Date.now() - 86400000 * 15,
      lastLogin: Date.now() - 7200000,
    });

    this.users.set('user-003', {
      id: 'user-003',
      username: 'wangwu',
      email: 'wangwu@example.com',
      role: 'user',
      status: 'inactive',
      createdAt: Date.now() - 86400000 * 7,
      lastLogin: Date.now() - 86400000 * 3,
    });
  }

  // ==================== 系统总控接口 ====================

  async getSystemStatus(): Promise<SystemStatus> {
    const allRunning = Array.from(this.services.values()).every(
      (s) => s.status === 'running'
    );

    return {
      status: allRunning ? 'running' : 'error',
      uptime: process.uptime(),
      version: '2.1.0',
      environment: 'development',
    };
  }

  async getServiceStatuses(): Promise<ServiceStatus[]> {
    return Array.from(this.services.values()).map((service) => ({
      ...service,
      cpu: Math.random() * 60 + 20,
      memory: Math.random() * 50 + 30,
      connections: Math.floor(Math.random() * 1000 + 100),
    }));
  }

  async getServiceStatus(serviceName: string): Promise<ServiceStatus | null> {
    const service = this.services.get(serviceName);
    return service ? { ...service } : null;
  }

  async controlService(serviceName: string, action: 'start' | 'stop' | 'restart'): Promise<{ success: boolean; message: string }> {
    const service = this.services.get(serviceName);

    if (!service) {
      return {
        success: false,
        message: `Service ${serviceName} not found`,
      };
    }

    // 模拟操作延迟
    await new Promise((resolve) => setTimeout(resolve, 500));

    switch (action) {
      case 'start':
        service.status = 'running';
        break;
      case 'stop':
        service.status = 'stopped';
        break;
      case 'restart':
        service.status = 'running';
        break;
    }

    return {
      success: true,
      message: `Service ${serviceName} ${action}ed successfully`,
    };
  }

  async getPerformanceMetrics(period?: { start: number; end: number }): Promise<PerformanceMetrics[]> {
    const count = 24; // 24小时数据
    const metrics: PerformanceMetrics[] = [];

    for (let i = 0; i < count; i++) {
      metrics.push({
        timestamp: Date.now() - (count - i) * 3600000,
        cpu: Math.random() * 40 + 30,
        memory: Math.random() * 30 + 50,
        disk: Math.random() * 20 + 40,
        network: {
          inbound: Math.random() * 1000000,
          outbound: Math.random() * 800000,
        },
        requests: {
          total: Math.floor(Math.random() * 10000 + 5000),
          success: Math.floor(Math.random() * 9500 + 4500),
          error: Math.floor(Math.random() * 500),
          avgResponseTime: Math.random() * 500 + 100,
        },
      });
    }

    return metrics;
  }

  // ==================== 运营管理协助 ====================

  async getUserActivities(period: { start: number; end: number }): Promise<UserActivity[]> {
    return [
      {
        userId: 'user-001',
        username: 'zhangsan',
        lastActive: Date.now() - 3600000,
        sessionCount: 45,
        totalDuration: 86400 * 2, // 2小时
        dailyActions: 234,
        weeklyActions: 1567,
        monthlyActions: 6234,
      },
      {
        userId: 'user-002',
        username: 'lisi',
        lastActive: Date.now() - 7200000,
        sessionCount: 28,
        totalDuration: 86400, // 1小时
        dailyActions: 156,
        weeklyActions: 987,
        monthlyActions: 4123,
      },
    ];
  }

  async getActivityAnalytics(period: 'daily' | 'weekly' | 'monthly'): Promise<ActivityAnalytics> {
    const multipliers = { daily: 1, weekly: 7, monthly: 30 };

    return {
      period,
      activeUsers: Math.floor(Math.random() * 500 + 200) * multipliers[period],
      newUsers: Math.floor(Math.random() * 50 + 10) * multipliers[period],
      returningUsers: Math.floor(Math.random() * 400 + 150) * multipliers[period],
      averageSessionDuration: Math.floor(Math.random() * 1800 + 600),
      peakHours: [9, 10, 14, 15, 20, 21],
      topActions: [
        { action: 'view_dashboard', count: 1234 },
        { action: 'search_user', count: 892 },
        { action: 'generate_report', count: 567 },
        { action: 'view_analytics', count: 445 },
      ],
    };
  }

  async getOperationStrategies(category?: string): Promise<OperationStrategy[]> {
    const allStrategies: OperationStrategy[] = [
      {
        id: 'strategy-001',
        title: '提升用户留存率',
        description: '通过个性化推荐和推送通知提高用户留存',
        priority: 'high',
        category: 'user_retention',
        metrics: {
          expectedImpact: '+15%',
          difficulty: 'medium',
          estimatedCost: '¥50,000',
        },
        actions: [
          '实现个性化内容推荐算法',
          '优化用户首次使用流程',
          '增加用户引导和提示',
        ],
      },
      {
        id: 'strategy-002',
        title: '提高转化率',
        description: '优化关键路径，提升用户转化率',
        priority: 'high',
        category: 'conversion',
        metrics: {
          expectedImpact: '+20%',
          difficulty: 'easy',
          estimatedCost: '¥20,000',
        },
        actions: [
          '优化注册流程',
          '改进支付体验',
          '增加社交分享激励',
        ],
      },
      {
        id: 'strategy-003',
        title: '增强用户参与度',
        description: '通过互动功能提高用户参与度',
        priority: 'medium',
        category: 'engagement',
        metrics: {
          expectedImpact: '+10%',
          difficulty: 'medium',
          estimatedCost: '¥30,000',
        },
        actions: [
          '添加用户评论功能',
          '创建社区活动',
          '实现用户等级系统',
        ],
      },
    ];

    if (category) {
      return allStrategies.filter((s) => s.category === category);
    }

    return allStrategies;
  }

  // ==================== UI配置协助 ====================

  async getThemes(): Promise<ThemeConfig[]> {
    return [
      {
      id: 'light',
      name: '浅色主题',
      colors: {
        primary: '#1890ff',
        secondary: '#52c41a',
        background: '#ffffff',
        surface: '#f5f5f5',
        text: '#000000',
        textSecondary: '#666666',
        border: '#d9d9d9',
        success: '#52c41a',
        warning: '#faad14',
        error: '#ff4d4f',
      },
      typography: {
        fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
        fontSize: { xs: '12px', sm: '14px', md: '16px', lg: '18px', xl: '20px' },
        fontWeight: { normal: 400, medium: 500, bold: 700 },
      },
      spacing: { xs: 4, sm: 8, md: 16, lg: 24, xl: 32 },
      borderRadius: { sm: 4, md: 8, lg: 12 },
      shadows: true,
    },
    {
      id: 'dark',
      name: '深色主题',
      colors: {
        primary: '#177ddc',
        secondary: '#49aa19',
        background: '#1f1f1f',
        surface: '#141414',
        text: '#ffffff',
        textSecondary: '#aaaaaa',
        border: '#303030',
        success: '#49aa19',
        warning: '#d89614',
        error: '#cf1322',
      },
      typography: {
        fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
        fontSize: { xs: '12px', sm: '14px', md: '16px', lg: '18px', xl: '20px' },
        fontWeight: { normal: 400, medium: 500, bold: 700 },
      },
      spacing: { xs: 4, sm: 8, md: 16, lg: 24, xl: 32 },
      borderRadius: { sm: 4, md: 8, lg: 12 },
      shadows: true,
    },
  ];
  }

  async getLayouts(): Promise<LayoutConfig[]> {
    return [
      {
        name: 'default',
        description: '默认布局',
        structure: {
          header: { enabled: true, height: 64, fixed: true },
          sidebar: { enabled: true, width: 256, collapsible: true, position: 'left' },
          footer: { enabled: true, height: 48, fixed: false },
        },
        breakpoints: { mobile: 768, tablet: 1024, desktop: 1280 },
      },
      {
        name: 'compact',
        description: '紧凑布局',
        structure: {
          header: { enabled: true, height: 48, fixed: true },
          sidebar: { enabled: true, width: 200, collapsible: true, position: 'left' },
          footer: { enabled: false, height: 0, fixed: false },
        },
        breakpoints: { mobile: 640, tablet: 900, desktop: 1200 },
      },
    ];
  }

  // ==================== 用户管理协助 ====================

  async getUserInfo(userId: string): Promise<UserInfo | null> {
    return this.users.get(userId) || null;
  }

  async searchUsers(query: string): Promise<UserInfo[]> {
    const lowerQuery = query.toLowerCase();
    return Array.from(this.users.values()).filter(
      (user) =>
        user.username.toLowerCase().includes(lowerQuery) ||
        user.email?.toLowerCase().includes(lowerQuery)
    );
  }

  async getUserBehavior(userId: string): Promise<UserBehavior | null> {
    if (!this.users.has(userId)) {
      return null;
    }

    return {
      userId,
      actions: Array.from({ length: 20 }, (_, i) => ({
        type: ['view', 'click', 'submit'][Math.floor(Math.random() * 3)],
        timestamp: Date.now() - Math.random() * 86400000,
        details: { page: '/dashboard', element: 'button' },
      })),
      patterns: {
        mostActiveTime: '14:00-16:00',
        favoriteFeatures: ['dashboard', 'reports', 'analytics'],
        averageSessionDuration: 1800,
      },
      riskLevel: 'low',
    };
  }

  async batchUserOperation(operation: any): Promise<{ processed: number; failed: number; results: any[] }> {
    const processed = operation.userIds.length;
    const failed = Math.floor(Math.random() * processed * 0.1);

    return {
      processed,
      failed,
      results: operation.userIds.map((id: string) => ({
        userId: id,
        success: Math.random() > 0.1,
        message: Math.random() > 0.1 ? 'Success' : 'Failed',
      })),
    };
  }

  // ==================== 数据统计协助 ====================

  async queryStatistics(query: any): Promise<StatisticsPoint[]> {
    const points: StatisticsPoint[] = [];
    const now = Date.now();

    for (let i = 0; i < 30; i++) {
      points.push({
        timestamp: now - (29 - i) * 3600000,
        value: Math.random() * 1000 + 500,
      });
    }

    return points;
  }

  async getTrendAnalysis(metric: string, period: { start: number; end: number }): Promise<TrendingAnalysis> {
    const current = Math.random() * 1000 + 500;
    const previous = Math.random() * 1000 + 400;
    const change = current - previous;
    const changePercent = (change / previous) * 100;

    const data: StatisticsPoint[] = [];
    const prediction: StatisticsPoint[] = [];
    const now = Date.now();

    for (let i = 0; i < 30; i++) {
      data.push({
        timestamp: now - (29 - i) * 3600000,
        value: Math.random() * 1000 + 500,
      });
    }

    for (let i = 0; i < 7; i++) {
      prediction.push({
        timestamp: now + (i + 1) * 3600000,
        value: current + (change / 7) * (i + 1),
      });
    }

    return {
      metric,
      current,
      previous,
      change,
      changePercent,
      trend: change > 5 ? 'up' : change < -5 ? 'down' : 'stable',
      data,
      prediction,
    };
  }

  async createCustomReport(report: Omit<CustomReport, 'id'>): Promise<CustomReport> {
    const newReport: CustomReport = {
      ...report,
      id: `report-${Date.now()}`,
    };

    this.reports.set(newReport.id, newReport);
    return newReport;
  }

  async getCustomReports(): Promise<CustomReport[]> {
    return Array.from(this.reports.values());
  }

  async getCustomReport(reportId: string): Promise<CustomReport | null> {
    return this.reports.get(reportId) || null;
  }

  async updateCustomReport(reportId: string, updates: Partial<CustomReport>): Promise<CustomReport | null> {
    const report = this.reports.get(reportId);
    if (!report) return null;

    const updated = { ...report, ...updates };
    this.reports.set(reportId, updated);
    return updated;
  }

  async deleteCustomReport(reportId: string): Promise<boolean> {
    return this.reports.delete(reportId);
  }
}

export default XiaolingService;
