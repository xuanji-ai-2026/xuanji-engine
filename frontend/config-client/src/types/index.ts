// 用户相关类型
export interface User {
  id: string
  username: string
  email: string
  realName: string
  avatar?: string
  role: UserRole
  status: UserStatus
  department?: string
  position?: string
  phone?: string
  createdAt: string
  lastLoginAt?: string
}

export type UserRole = 'admin' | 'manager' | 'operator' | 'viewer'
export type UserStatus = 'active' | 'inactive' | 'locked' | 'pending'

// 认证请求类型
export interface AuthRequest {
  id: string
  userId: string
  userName: string
  requestType: AuthRequestType
  reason: string
  attachments?: string[]
  status: RequestStatus
  priority: Priority
  requesterName: string
  requesterPhone?: string
  createdAt: string
  updatedAt: string
  reviewedAt?: string
  reviewedBy?: string
  reviewComment?: string
}

export type AuthRequestType = 'login' | 'password_reset' | 'privilege_upgrade' | 'account_recovery' | 'two_factor_enable'
export type RequestStatus = 'pending' | 'approved' | 'rejected' | 'processing'
export type Priority = 'low' | 'medium' | 'high' | 'urgent'

// 配置请求类型
export interface ConfigRequest {
  id: string
  userId: string
  userName: string
  configType: ConfigType
  description: string
  configData: Record<string, unknown>
  attachments?: string[]
  status: RequestStatus
  progress: number
  priority: Priority
  estimatedCompletion?: string
  createdAt: string
  updatedAt: string
  startedAt?: string
  completedAt?: string
  assignedTo?: string
  notes?: string
}

export type ConfigType =
  | 'system_config'
  | 'network_config'
  | 'security_config'
  | 'service_config'
  | 'database_config'
  | 'api_config'
  | 'feature_config'
  | 'custom_config'

// 工作台任务类型
export interface Task {
  id: string
  title: string
  description: string
  type: TaskType
  status: TaskStatus
  priority: Priority
  assignee?: string
  assigneeName?: string
  createdBy: string
  createdAt: string
  updatedAt: string
  dueDate?: string
  completedAt?: string
  tags?: string[]
  attachments?: string[]
  subtasks?: Subtask[]
}

export type TaskType = 'auth_request' | 'config_request' | 'maintenance' | 'review' | 'custom'
export type TaskStatus = 'todo' | 'in_progress' | 'review' | 'completed' | 'cancelled'

export interface Subtask {
  id: string
  title: string
  completed: boolean
  completedAt?: string
}

// 通知类型
export interface Notification {
  id: string
  type: NotificationType
  title: string
  message: string
  targetId?: string
  targetType?: string
  priority: Priority
  read: boolean
  createdAt: string
  userId: string
}

export type NotificationType = 'auth_request' | 'config_request' | 'task_assigned' | 'task_completed' | 'system' | 'alert'

// 统计数据类型
export interface Statistics {
  totalUsers: number
  activeUsers: number
  pendingAuthRequests: number
  pendingConfigRequests: number
  completedTasks: number
  inProgressTasks: number
  overdueTasks: number
  systemHealth: 'healthy' | 'warning' | 'critical'
}

// 搜索过滤类型
export interface SearchFilters {
  keyword?: string
  status?: string[]
  priority?: string[]
  dateRange?: {
    start: string
    end: string
  }
  assignee?: string
  department?: string
}

export interface PaginationParams {
  page: number
  pageSize: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

// API响应类型
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

// 表单相关类型
export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'textarea' | 'select' | 'multiselect' | 'date' | 'file'
  required?: boolean
  placeholder?: string
  options?: Array<{ label: string; value: string }>
  validation?: {
    pattern?: RegExp
    minLength?: number
    maxLength?: number
    min?: number
    max?: number
  }
}

// 智能助手消息类型
export interface AssistantMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
  attachments?: string[]
  suggestedActions?: Array<{
    label: string
    action: string
    params?: Record<string, unknown>
  }>
}

export interface Conversation {
  id: string
  title: string
  messages: AssistantMessage[]
  createdAt: string
  updatedAt: string
}

// 进度日志类型
export interface ProgressLog {
  id: string
  requestId: string
  message: string
  progress: number
  createdAt: string
  createdBy: string
}

// ============ 认证协助模块扩展类型 ============

// 认证历史记录
export interface AuthHistory {
  id: string
  requestId: string
  userId: string
  userName: string
  action: 'created' | 'approved' | 'rejected' | 'processing' | 'cancelled'
  actionBy: string
  actionByName: string
  actionAt: string
  comment?: string
  status: RequestStatus
}

// 认证统计数据
export interface AuthStatistics {
  totalRequests: number
  pendingRequests: number
  approvedRequests: number
  rejectedRequests: number
  processingRequests: number
  averageProcessingTime: number // 分钟
  requestsByType: Record<AuthRequestType, number>
  requestsByPriority: Record<Priority, number>
  monthlyTrend: Array<{ month: string; count: number }>
  approvalRate: number // 百分比
}

// 认证驳回原因
export interface RejectReason {
  id: string
  code: string
  reason: string
  category: string
  isActive: boolean
  createdAt: string
}

// 认证资料审核
export interface MaterialReview {
  id: string
  requestId: string
  materialType: string
  materialUrl: string
  reviewStatus: 'pending' | 'approved' | 'rejected'
  reviewedBy?: string
  reviewedAt?: string
  reviewComment?: string
}

// 认证申诉
export interface Appeal {
  id: string
  requestId: string
  userId: string
  userName: string
  reason: string
  evidence?: string[]
  status: 'pending' | 'under_review' | 'approved' | 'rejected'
  createdAt: string
  updatedAt: string
  reviewedBy?: string
  reviewedAt?: string
  reviewComment?: string
}

// 认证标签
export interface AuthTag {
  id: string
  name: string
  color: string
  description?: string
  createdAt: string
}

// 认证操作日志
export interface AuthOperationLog {
  id: string
  requestId: string
  userId: string
  userName: string
  operation: string
  details: Record<string, unknown>
  ip: string
  userAgent: string
  createdAt: string
}

// ============ 配置协助模块扩展类型 ============

// 配置模板
export interface ConfigTemplate {
  id: string
  name: string
  description: string
  configType: ConfigType
  templateData: Record<string, unknown>
  version: string
  isActive: boolean
  createdBy: string
  createdAt: string
  updatedAt: string
}

// 配置版本
export interface ConfigVersion {
  id: string
  configId: string
  version: string
  configData: Record<string, unknown>
  changeLog: string
  createdBy: string
  createdAt: string
}

// 配置冲突
export interface ConfigConflict {
  id: string
  configId: string
  conflictType: 'duplicate' | 'incompatible' | 'dependency'
  description: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  status: 'unresolved' | 'resolved' | 'ignored'
  detectedAt: string
  resolvedAt?: string
}

// 配置依赖
export interface ConfigDependency {
  id: string
  sourceConfigId: string
  targetConfigId: string
  dependencyType: 'required' | 'optional' | 'exclusive'
  description: string
}

// 配置差异
export interface ConfigDiff {
  field: string
  oldValue: unknown
  newValue: unknown
  changeType: 'added' | 'removed' | 'modified'
}

// 配置备份
export interface ConfigBackup {
  id: string
  configId: string
  version: string
  backupData: Record<string, unknown>
  createdBy: string
  createdAt: string
  size: number // bytes
}

// 配置自动化脚本
export interface ConfigScript {
  id: string
  name: string
  description: string
  scriptType: 'validation' | 'transformation' | 'deployment'
  scriptContent: string
  isActive: boolean
  createdBy: string
  createdAt: string
  updatedAt: string
}

// 配置统计数据
export interface ConfigStatistics {
  totalRequests: number
  pendingRequests: number
  completedRequests: number
  averageProcessingTime: number
  requestsByType: Record<ConfigType, number>
  requestsByPriority: Record<Priority, number>
  conflictCount: number
  templateUsage: Array<{ templateName: string; usageCount: number }>
  monthlyTrend: Array<{ month: string; count: number }>
}

// 配置部署记录
export interface DeploymentRecord {
  id: string
  configId: string
  version: string
  environment: 'dev' | 'staging' | 'production'
  status: 'pending' | 'deploying' | 'success' | 'failed' | 'rolled_back'
  deployedBy: string
  deployedAt: string
  rollbackVersion?: string
  rollbackAt?: string
  logs: string
}

// 配置测试结果
export interface TestResult {
  id: string
  configId: string
  testName: string
  status: 'passed' | 'failed' | 'skipped'
  message: string
  duration: number
  executedAt: string
  executedBy: string
}

// 配置审计日志
export interface AuditLog {
  id: string
  configId: string
  action: 'created' | 'updated' | 'deleted' | 'deployed' | 'rolled_back'
  actionBy: string
  actionByName: string
  changes: Record<string, ConfigDiff>
  ip: string
  userAgent: string
  createdAt: string
}

// ============ 工作台模块扩展类型 ============

// 任务看板列
export interface KanbanColumn {
  id: string
  title: string
  status: TaskStatus
  taskIds: string[]
  order: number
}

// 任务里程碑
export interface Milestone {
  id: string
  title: string
  description?: string
  targetDate: string
  status: 'not_started' | 'in_progress' | 'completed' | 'overdue'
  taskIds: string[]
  progress: number
}

// 任务评论
export interface TaskComment {
  id: string
  taskId: string
  userId: string
  userName: string
  content: string
  createdAt: string
  updatedAt: string
  attachments?: string[]
}

// 任务工时
export interface TaskTimeLog {
  id: string
  taskId: string
  userId: string
  userName: string
  hours: number
  date: string
  description?: string
}

// 任务模板
export interface TaskTemplate {
  id: string
  name: string
  description: string
  defaultTitle: string
  defaultDescription: string
  defaultPriority: Priority
  estimatedHours: number
  checklist?: Array<{ title: string; defaultChecked: boolean }>
  isActive: boolean
  createdBy: string
  createdAt: string
}

// 任务统计数据
export interface TaskStatistics {
  totalTasks: number
  completedTasks: number
  inProgressTasks: number
  overdueTasks: number
  averageCompletionTime: number
  tasksByStatus: Record<TaskStatus, number>
  tasksByPriority: Record<Priority, number>
  tasksByType: Record<TaskType, number>
  userPerformance: Array<{
    userId: string
    userName: string
    completedCount: number
    averageTime: number
  }>
  monthlyTrend: Array<{ month: string; count: number }>
}

// ============ 用户管理模块扩展类型 ============

// 用户分组
export interface UserGroup {
  id: string
  name: string
  description?: string
  userIds: string[]
  createdAt: string
  updatedAt: string
}

// 用户标签
export interface UserTag {
  id: string
  name: string
  color: string
  description?: string
}

// 用户行为记录
export interface UserBehavior {
  id: string
  userId: string
  action: string
  resource: string
  details: Record<string, unknown>
  ip: string
  userAgent: string
  createdAt: string
}

// 用户生命周期事件
export interface LifecycleEvent {
  id: string
  userId: string
  eventType: 'created' | 'activated' | 'deactivated' | 'role_changed' | 'deleted'
  details: Record<string, unknown>
  createdAt: string
  createdBy: string
}

// 用户权限模板
export interface PermissionTemplate {
  id: string
  name: string
  description: string
  permissions: string[]
  isActive: boolean
  createdAt: string
  updatedAt: string
}

// 用户API密钥
export interface ApiKey {
  id: string
  userId: string
  keyName: string
  keyPrefix: string
  scopes: string[]
  isActive: boolean
  expiresAt?: string
  lastUsedAt?: string
  createdAt: string
}

// 用户OAuth集成
export interface OAuthIntegration {
  id: string
  userId: string
  provider: 'google' | 'github' | 'microsoft' | 'custom'
  providerId: string
  email: string
  isActive: boolean
  linkedAt: string
  lastSyncAt?: string
}

// ============ 智能助手模块扩展类型 ============

// 知识库条目
export interface KnowledgeEntry {
  id: string
  title: string
  content: string
  category: string
  tags: string[]
  createdAt: string
  updatedAt: string
  createdBy: string
}

// 情感分析结果
export interface SentimentAnalysis {
  id: string
  messageId: string
  sentiment: 'positive' | 'neutral' | 'negative'
  confidence: number
  emotions: {
    joy?: number
    sadness?: number
    anger?: number
    fear?: number
    surprise?: number
  }
  analyzedAt: string
}

// ============ 通用类型 ============

// 图表数据点
export interface ChartDataPoint {
  label: string
  value: number
  date?: string
}

// 报表参数
export interface ReportParams {
  startDate: string
  endDate: string
  type: string
  format: 'pdf' | 'excel' | 'csv'
  filters?: Record<string, unknown>
}

// 导出选项
export interface ExportOptions {
  format: 'csv' | 'excel' | 'json' | 'pdf'
  fields: string[]
  dateRange?: {
    start: string
    end: string
  }
}

// 批量操作结果
export interface BatchOperationResult {
  success: number
  failed: number
  errors: Array<{ id: string; error: string }>
}

// 规则条件
export interface RuleCondition {
  field: string
  operator: 'equals' | 'not_equals' | 'contains' | 'greater_than' | 'less_than' | 'in'
  value: unknown
}

// 自动分配规则
export interface AssignmentRule {
  id: string
  name: string
  description: string
  conditions: RuleCondition[]
  assignTo: string
  priority: number
  isActive: boolean
}

// 通知模板
export interface NotificationTemplate {
  id: string
  type: string
  title: string
  content: string
  variables: string[]
  isActive: boolean
}
