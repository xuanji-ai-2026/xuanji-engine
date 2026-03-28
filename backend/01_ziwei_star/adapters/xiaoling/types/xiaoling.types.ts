/**
 * 小灵（Xiaoling）适配层类型定义
 */

// ==================== 通用类型 ====================

export interface Response<T = any> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  timestamp: number;
}

export interface PaginationParams {
  page: number;
  pageSize: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// ==================== 系统总控类型 ====================

export interface SystemStatus {
  status: 'running' | 'stopped' | 'error' | 'maintenance';
  uptime: number;
  version: string;
  environment: 'development' | 'staging' | 'production';
}

export interface ServiceStatus {
  name: string;
  status: 'running' | 'stopped' | 'error';
  cpu: number;
  memory: number;
  connections: number;
  lastError?: string;
}

export interface PerformanceMetrics {
  timestamp: number;
  cpu: number;
  memory: number;
  disk: number;
  network: {
    inbound: number;
    outbound: number;
  };
  requests: {
    total: number;
    success: number;
    error: number;
    avgResponseTime: number;
  };
  custom?: Record<string, number>;
}

export interface ServiceControlParams {
  serviceName: string;
  action: 'start' | 'stop' | 'restart';
  force?: boolean;
}

// ==================== 运营管理类型 ====================

export interface UserActivity {
  userId: string;
  username: string;
  lastActive: number;
  sessionCount: number;
  totalDuration: number;
  dailyActions: number;
  weeklyActions: number;
  monthlyActions: number;
}

export interface ActivityAnalytics {
  period: 'daily' | 'weekly' | 'monthly';
  activeUsers: number;
  newUsers: number;
  returningUsers: number;
  averageSessionDuration: number;
  peakHours: number[];
  topActions: Array<{
    action: string;
    count: number;
  }>;
}

export interface OperationStrategy {
  id: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  category: 'user_retention' | 'engagement' | 'conversion' | 'support';
  metrics: {
    expectedImpact: string;
    difficulty: 'easy' | 'medium' | 'hard';
    estimatedCost: string;
  };
  actions: string[];
}

export interface ReportConfig {
  type: 'user_activity' | 'performance' | 'revenue' | 'custom';
  period: {
    start: number;
    end: number;
  };
  metrics: string[];
  format: 'json' | 'csv' | 'excel' | 'pdf';
  filters?: Record<string, any>;
}

// ==================== UI配置类型 ====================

export interface ThemeConfig {
  id: string;
  name: string;
  description?: string;
  colors: {
    primary: string;
    secondary: string;
    background: string;
    surface: string;
    text: string;
    textSecondary: string;
    border: string;
    success: string;
    warning: string;
    error: string;
  };
  typography: {
    fontFamily: string;
    fontSize: {
      xs: string;
      sm: string;
      md: string;
      lg: string;
      xl: string;
    };
    fontWeight: {
      normal: number;
      medium: number;
      bold: number;
    };
  };
  spacing: {
    xs: number;
    sm: number;
    md: number;
    lg: number;
    xl: number;
  };
  borderRadius: {
    sm: number;
    md: number;
    lg: number;
  };
  shadows: boolean;
}

export interface LayoutConfig {
  name: string;
  description?: string;
  structure: {
    header: {
      enabled: boolean;
      height: number;
      fixed: boolean;
    };
    sidebar: {
      enabled: boolean;
      width: number;
      collapsible: boolean;
      position: 'left' | 'right';
    };
    footer: {
      enabled: boolean;
      height: number;
      fixed: boolean;
    };
  };
  breakpoints: {
    mobile: number;
    tablet: number;
    desktop: number;
  };
}

export interface UIPreviewConfig {
  theme: string;
  layout: string;
  screen: 'mobile' | 'tablet' | 'desktop';
  data?: Record<string, any>;
}

// ==================== 用户管理类型 ====================

export interface UserInfo {
  id: string;
  username: string;
  email?: string;
  phone?: string;
  avatar?: string;
  role: string;
  status: 'active' | 'inactive' | 'banned';
  createdAt: number;
  lastLogin: number;
  metadata?: Record<string, any>;
}

export interface UserBehavior {
  userId: string;
  actions: Array<{
    type: string;
    timestamp: number;
    details: any;
  }>;
  patterns: {
    mostActiveTime: string;
    favoriteFeatures: string[];
    averageSessionDuration: number;
  };
  riskLevel: 'low' | 'medium' | 'high';
}

export interface BatchUserOperation {
  operation: 'activate' | 'deactivate' | 'ban' | 'unban' | 'delete' | 'update_role';
  userIds: string[];
  params?: Record<string, any>;
  dryRun?: boolean;
}

// ==================== 数据统计类型 ====================

export interface StatisticsQuery {
  metric: string;
  period: {
    start: number;
    end: number;
  };
  granularity: 'hour' | 'day' | 'week' | 'month';
  filters?: Record<string, any>;
  groupBy?: string[];
}

export interface StatisticsPoint {
  timestamp: number;
  value: number;
  metadata?: Record<string, any>;
}

export interface TrendAnalysis {
  metric: string;
  current: number;
  previous: number;
  change: number;
  changePercent: number;
  trend: 'up' | 'down' | 'stable';
  data: StatisticsPoint[];
  prediction?: StatisticsPoint[];
}

export interface CustomReport {
  id: string;
  name: string;
  description?: string;
  query: StatisticsQuery;
  visualization: {
    type: 'line' | 'bar' | 'pie' | 'table' | 'card';
    config?: any;
  };
  schedule?: {
    enabled: boolean;
    frequency: string;
    recipients: string[];
  };
}
