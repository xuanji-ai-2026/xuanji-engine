// 用户相关类型
export interface User {
  id: string
  name: string
  email: string
  avatar?: string
  role: 'admin' | 'user' | 'manager' | 'viewer'
  status: 'active' | 'inactive' | 'pending' | 'suspended'
  createdAt: string
  lastLoginAt?: string
  phone?: string
  department?: string
}

export interface UserFilters {
  keyword?: string
  role?: string
  status?: string
  department?: string
  dateRange?: [string, string]
}

export interface UserStats {
  total: number
  active: number
  inactive: number
  pending: number
}

// 数字人相关类型
export interface DigitalHuman {
  id: string
  name: string
  avatar?: string
  type: 'customer_service' | 'assistant' | 'expert' | 'custom'
  model: string
  status: 'active' | 'inactive' | 'training' | 'maintenance'
  capabilities: string[]
  configuration: Record<string, unknown>
  createdAt: string
  updatedAt: string
  usageStats: {
    totalSessions: number
    avgResponseTime: number
    satisfaction: number
  }
}

export interface DigitalHumanConfig {
  personality: string
  temperature: number
  maxTokens: number
  systemPrompt: string
  knowledgeSources: string[]
}

// 知识源相关类型
export interface KnowledgeSource {
  id: string
  name: string
  type: 'document' | 'database' | 'api' | 'website' | 'custom'
  status: 'active' | 'syncing' | 'error' | 'inactive'
  config: Record<string, unknown>
  stats: {
    documents: number
    size: number
    lastSyncAt?: string
  }
  createdAt: string
  updatedAt: string
}

// 插件相关类型
export interface Plugin {
  id: string
  name: string
  version: string
  description: string
  author: string
  status: 'active' | 'inactive' | 'reviewing' | 'rejected'
  type: 'integration' | 'extension' | 'theme' | 'tool'
  config: Record<string, unknown>
  metrics: {
    installs: number
    rating: number
    reviews: number
  }
  createdAt: string
  updatedAt: string
}

// 系统配置类型
export interface SystemConfig {
  logo?: string
  favicon?: string
  theme: 'light' | 'dark' | 'auto'
  primaryColor: string
  accentColor: string
  backgroundImage?: string
  layout: 'sidebar' | 'top' | 'mixed'
}

export interface UIConfig {
  sidebar: {
    collapsed: boolean
    width: number
    position: 'left' | 'right'
  }
  header: {
    height: number
    visible: boolean
  }
  animations: {
    enabled: boolean
    duration: number
  }
}

// 更新和公告类型
export interface Update {
  id: string
  version: string
  type: 'major' | 'minor' | 'patch' | 'hotfix'
  description: string
  changes: string[]
  releaseDate: string
  downloadUrl?: string
  mandatory: boolean
}

export interface Announcement {
  id: string
  title: string
  content: string
  type: 'info' | 'warning' | 'error' | 'success'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  startDate: string
  endDate?: string
  targetUsers?: string[]
}

// 运营数据类型
export interface OperationMetrics {
  system: {
    uptime: number
    cpu: number
    memory: number
    disk: number
  }
  performance: {
    avgResponseTime: number
    errorRate: number
    requestCount: number
  }
  security: {
    threatsBlocked: number
    loginAttempts: number
    securityScore: number
  }
  business: {
    activeUsers: number
    revenue: number
    conversionRate: number
    churnRate: number
  }
}

// 智能助手小灵相关类型
export interface AssistantAlert {
  id: string
  type: 'warning' | 'error' | 'info' | 'success'
  severity: 'low' | 'medium' | 'high' | 'critical'
  title: string
  message: string
  timestamp: string
  actionUrl?: string
  acknowledged: boolean
}

export interface AssistantSuggestion {
  id: string
  category: 'performance' | 'security' | 'feature' | 'optimization'
  title: string
  description: string
  impact: string
  effort: 'low' | 'medium' | 'high'
  estimatedBenefit?: string
}

// 通用类型
export interface Pagination {
  page: number
  pageSize: number
  total: number
}

export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
  error?: string
}

export interface TableParams {
  pagination: Pagination
  filters?: Record<string, unknown>
  sorter?: {
    field: string
    order: 'asc' | 'desc'
  }
}
