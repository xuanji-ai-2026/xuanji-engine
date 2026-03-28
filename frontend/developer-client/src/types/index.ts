// ============================================
// API管理模块类型定义
// ============================================

export interface ApiKey {
  id: string;
  name: string;
  key: string;
  permissions: Permission[];
  createdAt: string;
  expiresAt?: string;
  lastUsedAt?: string;
  status: 'active' | 'revoked' | 'expired';
}

export interface Permission {
  id: string;
  name: string;
  description: string;
  granted: boolean;
}

export interface CallStatistics {
  totalCalls: number;
  successCalls: number;
  errorCalls: number;
  cost: number;
  period: 'today' | 'week' | 'month' | 'year';
}

export interface CallTrend {
  date: string;
  calls: number;
  cost: number;
  errorRate: number;
}

export interface ApiDocument {
  id: string;
  name: string;
  version: string;
  description: string;
  endpoints: ApiEndpoint[];
  examples: CodeExample[];
}

export interface ApiEndpoint {
  id: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  path: string;
  description: string;
  parameters: Parameter[];
  responses: ResponseSchema[];
}

export interface Parameter {
  name: string;
  type: string;
  required: boolean;
  description: string;
  example?: any;
}

export interface ResponseSchema {
  statusCode: number;
  description: string;
  schema: any;
}

export interface CodeExample {
  language: string;
  code: string;
}

export interface DebugRequest {
  id: string;
  timestamp: string;
  method: string;
  url: string;
  headers: Record<string, string>;
  body?: any;
  response?: any;
  statusCode?: number;
  duration: number;
}

// ============================================
// 插件开发模块类型定义
// ============================================

export interface Plugin {
  id: string;
  name: string;
  version: string;
  description: string;
  author: string;
  status: 'draft' | 'submitted' | 'approved' | 'rejected' | 'published';
  createdAt: string;
  updatedAt: string;
  category: string;
  tags: string[];
  icon?: string;
  downloads?: number;
  rating?: number;
  price?: number;
}

export interface PluginConfig {
  id: string;
  pluginId: string;
  config: Record<string, any>;
  environment: 'development' | 'testing' | 'production';
}

export interface PluginDependency {
  name: string;
  version: string;
  required: boolean;
}

export interface PluginTestResult {
  id: string;
  timestamp: string;
  testType: 'unit' | 'integration' | 'performance';
  passed: number;
  failed: number;
  duration: number;
  details: TestCase[];
}

export interface TestCase {
  name: string;
  passed: boolean;
  message?: string;
  duration: number;
}

export interface PluginTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  thumbnail?: string;
  files: TemplateFile[];
}

export interface TemplateFile {
  path: string;
  content: string;
}

export interface PluginLogEntry {
  id: string;
  timestamp: string;
  level: 'info' | 'warn' | 'error' | 'debug';
  message: string;
  context?: any;
}

export interface CodeSnippet {
  id: string;
  title: string;
  language: string;
  code: string;
  description: string;
  tags: string[];
}

// ============================================
// SDK管理模块类型定义
// ============================================

export interface Sdk {
  id: string;
  name: string;
  platform: 'javascript' | 'python' | 'java' | 'go' | 'rust' | 'php' | 'csharp';
  version: string;
  description: string;
  downloadUrl: string;
  size: number;
  releasedAt: string;
  documentationUrl: string;
  changelog: ChangelogEntry[];
}

export interface ChangelogEntry {
  version: string;
  date: string;
  changes: string[];
  type: 'major' | 'minor' | 'patch';
}

export interface IntegrationGuide {
  id: string;
  sdk: string;
  steps: IntegrationStep[];
  quickStart: string;
  examples: CodeExample[];
}

export interface IntegrationStep {
  step: number;
  title: string;
  description: string;
  code?: string;
}

// ============================================
// 智能助手小元类型定义
// ============================================

export interface AssistantMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface CodeGenerationRequest {
  description: string;
  language: string;
  context?: string;
  framework?: string;
}

export interface CodeGenerationResult {
  code: string;
  explanation: string;
  suggestions: string[];
}

export interface ErrorDiagnostic {
  id: string;
  severity: 'error' | 'warning' | 'info';
  message: string;
  code?: string;
  line?: number;
  column?: number;
  fixSuggestion?: string;
}

export interface OptimizationSuggestion {
  id: string;
  type: 'performance' | 'security' | 'maintainability' | 'best-practice';
  title: string;
  description: string;
  code: string;
  improvedCode: string;
  impact: 'high' | 'medium' | 'low';
}

// ============================================
// 通用类型定义
// ============================================

export interface PaginationParams {
  page: number;
  pageSize: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
}

export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}

export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  role: 'admin' | 'developer' | 'viewer';
  createdAt: string;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  read: boolean;
  createdAt: string;
}

export interface ThemeConfig {
  mode: 'light' | 'dark' | 'auto';
  primaryColor: string;
}
