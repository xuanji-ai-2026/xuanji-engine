/**
 * 小灵（Xiaoling）适配层入口文件
 */

export { XiaolingAdapter } from './XiaolingAdapter';
export { XiaolingService } from './XiaolingService';

export type {
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
  PaginationParams,
  PaginatedResponse,
} from '../types/xiaoling.types';

export type { XiaolingConfig } from '../config/xiaoling.config';

export { defaultConfig } from '../config/xiaoling.config';

// 便捷导出
export { default as Xiaoling } from './XiaolingAdapter';
