/**
 * 小微适配层 - 类型定义
 * 版本: v1.0.0
 * 描述: 配置端智能助手适配层的类型定义
 */

// ==================== 基础类型 ====================

export interface XiaoweiConfig {
  /** 紫微元灵核心 WebSocket 地址 */
  coreWsUrl: string;
  /** 紫微元灵核心 HTTP 地址 */
  coreHttpUrl: string;
  /** 适配器唯一标识 */
  adapterId: string;
  /** 认证 Token */
  authToken: string;
  /** 日志级别 */
  logLevel: 'debug' | 'info' | 'warn' | 'error';
  /** 消息超时时间（毫秒） */
  timeout: number;
}

export enum ResponseStatus {
  SUCCESS = 'success',
  ERROR = 'error',
  PARTIAL = 'partial'
}

export interface BaseResponse<T = any> {
  status: ResponseStatus;
  data?: T;
  error?: string;
  timestamp: number;
}

// ==================== 消息类型 ====================

export enum MessageType {
  // 配置相关
  CONFIG_QUERY = 'config.query',
  CONFIG_MODIFY = 'config.modify',
  CONFIG_VALIDATE = 'config.validate',
  CONFIG_BATCH = 'config.batch',
  
  // 工作台相关
  WORKBENCH_GUIDE = 'workbench.guide',
  WORKBENCH_SUGGEST = 'workbench.suggest',
  WORKBENCH_FLOW = 'workbench.flow',
  
  // 认证相关
  AUTH_VERIFY = 'auth.verify',
  AUTH_CONFIGURE = 'auth.configure',
  AUTH_SECURITY_CHECK = 'auth.security_check',
  
  // 用户管理相关
  USER_QUERY = 'user.query',
  USER_CONFIGURE = 'user.configure',
  USER_BATCH = 'user.batch',
  
  // 通用
  PING = 'ping',
  PONG = 'pong'
}

export interface Message {
  id: string;
  type: MessageType;
  payload: any;
  timestamp: number;
}

// ==================== 配置类型 ====================

export interface ConfigItem {
  /** 配置键 */
  key: string;
  /** 配置值 */
  value: any;
  /** 配置类型 */
  type: 'string' | 'number' | 'boolean' | 'object' | 'array';
  /** 描述 */
  description?: string;
  /** 默认值 */
  defaultValue?: any;
  /** 是否必填 */
  required?: boolean;
  /** 验证规则 */
  validation?: ValidationRule;
}

export interface ValidationRule {
  /** 最小值 */
  min?: number;
  /** 最大值 */
  max?: number;
  /** 正则表达式 */
  pattern?: string;
  /** 枚举值 */
  enum?: any[];
  /** 自定义验证函数 */
  custom?: (value: any) => boolean | string;
}

export interface ConfigQueryParams {
  /** 查询的配置键（支持通配符） */
  keys?: string[];
  /** 分组 */
  group?: string;
  /** 是否返回默认值 */
  includeDefault?: boolean;
}

export interface ConfigModifyParams {
  /** 配置键值对 */
  items: Record<string, any>;
  /** 是否验证 */
  validate?: boolean;
  /** 是否持久化 */
  persist?: boolean;
}

export interface ConfigValidationError {
  /** 配置键 */
  key: string;
  /** 错误消息 */
  message: string;
  /** 当前值 */
  currentValue: any;
}

export interface ValidationResult {
  /** 是否通过 */
  valid: boolean;
  /** 错误列表 */
  errors: ConfigValidationError[];
  /** 警告列表 */
  warnings: string[];
}

// ==================== 工作台类型 ====================

export interface WorkbenchStep {
  /** 步骤 ID */
  id: string;
  /** 步骤名称 */
  name: string;
  /** 步骤描述 */
  description: string;
  /** 步骤顺序 */
  order: number;
  /** 所需权限 */
  permissions?: string[];
  /** 执行命令 */
  command?: string;
}

export interface WorkbenchGuide {
  /** 引导 ID */
  id: string;
  /** 引导标题 */
  title: string;
  /** 引导描述 */
  description: string;
  /** 步骤列表 */
  steps: WorkbenchStep[];
  /** 预计时间 */
  estimatedTime: string;
}

export interface WorkbenchSuggestion {
  /** 建议 ID */
  id: string;
  /** 建议标题 */
  title: string;
  /** 建议描述 */
  description: string;
  /** 操作类型 */
  action: 'navigation' | 'command' | 'config_change' | 'create';
  /** 目标 URL 或命令 */
  target: string;
  /** 优先级 */
  priority: 'high' | 'medium' | 'low';
  /** 相关配置键 */
  relatedConfigs?: string[];
}

export interface BatchConfigOperation {
  /** 操作类型 */
  type: 'set' | 'delete' | 'reset';
  /** 配置键 */
  key: string;
  /** 配置值（set 时需要） */
  value?: any;
}

// ==================== 认证类型 ====================

export interface AuthVerifyParams {
  /** 用户标识 */
  userId: string;
  /** 认证令牌 */
  token?: string;
  /** 验证类型 */
  type: 'token' | 'session' | 'certificate';
}

export interface AuthResult {
  /** 是否验证通过 */
  success: boolean;
  /** 用户信息 */
  user?: UserInfo;
  /** 权限列表 */
  permissions?: string[];
  /** 过期时间 */
  expiresAt?: number;
}

export interface UserInfo {
  /** 用户 ID */
  id: string;
  /** 用户名 */
  username: string;
  /** 角色 */
  role: string;
  /** 部门 */
  department?: string;
  /** 邮箱 */
  email?: string;
}

export interface AuthConfigureParams {
  /** 认证方式 */
  method: 'jwt' | 'oauth2' | 'ldap' | 'custom';
  /** 配置参数 */
  config: Record<string, any>;
}

export interface SecurityCheckResult {
  /** 安全评分 */
  score: number;
  /** 风险级别 */
  riskLevel: 'low' | 'medium' | 'high';
  /** 问题列表 */
  issues: SecurityIssue[];
  /** 建议列表 */
  recommendations: string[];
}

export interface SecurityIssue {
  /** 问题 ID */
  id: string;
  /** 问题描述 */
  description: string;
  /** 严重程度 */
  severity: 'critical' | 'high' | 'medium' | 'low';
  /** 受影响的配置 */
  affectedConfig?: string;
  /** 修复建议 */
  fix?: string;
}

// ==================== 用户管理类型 ====================

export interface UserQueryParams {
  /** 查询条件 */
  filters: UserFilter;
  /** 分页 */
  pagination?: Pagination;
  /** 排序 */
  sort?: Sort;
}

export interface UserFilter {
  /** 用户名（支持模糊匹配） */
  username?: string;
  /** 角色 */
  role?: string;
  /** 部门 */
  department?: string;
  /** 状态 */
  status?: 'active' | 'inactive' | 'suspended';
}

export interface Pagination {
  /** 页码 */
  page: number;
  /** 每页数量 */
  pageSize: number;
}

export interface Sort {
  /** 排序字段 */
  field: string;
  /** 排序方向 */
  direction: 'asc' | 'desc';
}

export interface UserConfigureParams {
  /** 用户 ID */
  userId: string;
  /** 配置更新 */
  updates: Partial<UserInfo> & {
    preferences?: Record<string, any>;
  };
}

export interface BatchUserOperation {
  /** 操作类型 */
  type: 'create' | 'update' | 'delete' | 'activate' | 'deactivate';
  /** 用户 ID（update/delete/activate/deactivate 时需要） */
  userId?: string;
  /** 用户数据（create 时需要） */
  userData?: Partial<UserInfo>;
  /** 批量条件（批量操作时使用） */
  filter?: UserFilter;
}

// ==================== WebSocket 事件 ====================

export type WebSocketEventHandler = (data: any) => void;

export interface WebSocketEvents {
  /** 连接建立 */
  onConnect?: WebSocketEventHandler;
  /** 连接断开 */
  onDisconnect?: WebSocketEventHandler;
  /** 消息接收 */
  onMessage?: WebSocketEventHandler;
  /** 错误处理 */
  onError?: (error: Error) => void;
}
