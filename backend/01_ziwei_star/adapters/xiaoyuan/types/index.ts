/**
 * 小元 - 开发者端智能助手适配层
 * 类型定义文件
 */

// ==================== 基础类型 ====================

export enum MessageType {
  TEXT = 'text',
  VOICE = 'voice',
  IMAGE = 'image',
  SYSTEM = 'system',
  CODE = 'code',
  ERROR = 'error'
}

export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
  SYSTEM = 'system',
  TOOL = 'tool'
}

export enum ConnectionStatus {
  DISCONNECTED = 'disconnected',
  CONNECTING = 'connecting',
  CONNECTED = 'connected',
  ERROR = 'error'
}

export enum ServiceType {
  API_MANAGEMENT = 'api_management',
  PLUGIN_DEVELOPMENT = 'plugin_development',
  SDK_MANAGEMENT = 'sdk_management',
  CODE_REVIEW = 'code_review'
}

// ==================== API 管理相关类型 ====================

export interface ApiEndpoint {
  id: string;
  path: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  description: string;
  tags: string[];
  parameters: ApiParameter[];
  requestBody?: ApiSchema;
  responses: Record<number, ApiSchema>;
  authRequired: boolean;
  rateLimit?: {
    requests: number;
    per: number: // seconds
  };
}

export interface ApiParameter {
  name: string;
  type: string;
  required: boolean;
  description: string;
  example?: any;
  validation?: string;
}

export interface ApiSchema {
  type: string;
  properties?: Record<string, any>;
  items?: any;
  required?: string[];
  description?: string;
  example?: any;
}

export interface ApiTestRequest {
  endpointId: string;
  method: string;
  url: string;
  headers: Record<string, string>;
  body?: any;
  queryParams?: Record<string, string>;
}

export interface ApiTestResponse {
  success: boolean;
  status: number;
  headers: Record<string, string>;
  body: any;
  duration: number;
  timestamp: number;
}

export interface ApiGenerationRequest {
  description: string;
  endpointName?: string;
  method?: string;
  existingApis?: ApiEndpoint[];
}

// ==================== 插件开发相关类型 ====================

export interface PluginTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  type: 'ui' | 'api' | 'middleware' | 'service';
  language: 'typescript' | 'javascript' | 'python';
  framework?: string;
  files: PluginFile[];
  dependencies: Record<string, string>;
  config?: PluginConfig;
}

export interface PluginFile {
  path: string;
  content: string;
  description?: string;
  isEntry?: boolean;
}

export interface PluginConfig {
  id: string;
  name: string;
  version: string;
  permissions: string[];
  settings: PluginSetting[];
}

export interface PluginSetting {
  key: string;
  type: 'string' | 'number' | 'boolean' | 'select' | 'textarea';
  label: string;
  description?: string;
  defaultValue?: any;
  required?: boolean;
  options?: Array<{ value: any; label: string }>;
}

export interface PluginApiGuide {
  pluginId: string;
  apiEndpoints: ApiEndpoint[];
  usageExamples: CodeExample[];
  integrationSteps: IntegrationStep[];
  testingGuide: TestingGuide;
}

export interface CodeExample {
  title: string;
  description: string;
  language: string;
  code: string;
}

export interface IntegrationStep {
  step: number;
  title: string;
  description: string;
  code?: string;
  files?: string[];
}

export interface TestingGuide {
  unitTests: CodeExample[];
  integrationTests: CodeExample[];
  manualTests: TestScenario[];
}

export interface TestScenario {
  title: string;
  description: string;
  steps: string[];
  expectedResult: string;
}

// ==================== SDK 管理相关类型 ====================

export interface SdkVersion {
  name: string;
  version: string;
  releaseDate: string;
  type: 'major' | 'minor' | 'patch';
  changelog: string[];
  downloadUrl?: string;
  breakingChanges?: string[];
}

export interface SdkInfo {
  name: string;
  currentVersion: string;
  latestVersion: string;
  versions: SdkVersion[];
  platforms: string[];
  languages: string[];
  documentationUrl: string;
  repositoryUrl: string;
}

export interface SdkIntegrationGuide {
  sdkName: string;
  platform: string;
  language: string;
  installationSteps: string[];
  configurationSteps: ConfigurationStep[];
  usageExamples: CodeExample[];
  commonIssues: CommonIssue[];
}

export interface ConfigurationStep {
  step: number;
  title: string;
  description: string;
  code?: string;
  files?: {
    path: string;
    content: string;
  }[];
}

export interface CommonIssue {
  title: string;
  description: string;
  solution: string;
  code?: string;
}

export interface SdkUpdate {
  sdkName: string;
  fromVersion: string;
  toVersion: string;
  type: 'major' | 'minor' | 'patch';
  changes: string[];
  breakingChanges: string[];
  migrationGuide?: CodeExample[];
}

// ==================== 代码审查相关类型 ====================

export interface CodeReviewRequest {
  code: string;
  language: string;
  filePath?: string;
  context?: string;
  rules?: ReviewRule[];
}

export interface ReviewRule {
  id: string;
  name: string;
  category: 'quality' | 'security' | 'performance' | 'style';
  severity: 'low' | 'medium' | 'high' | 'critical';
  enabled: boolean;
  config?: Record<string, any>;
}

export interface CodeReviewResult {
  overallScore: number;  // 0-100
  summary: string;
  issues: ReviewIssue[];
  suggestions: ReviewSuggestion[];
  metrics: CodeMetrics;
  timestamp: number;
}

export interface ReviewIssue {
  id: string;
  category: 'quality' | 'security' | 'performance' | 'style';
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  line?: number;
  column?: number;
  rule: string;
  codeSnippet?: string;
  suggestedFix?: string;
}

export interface ReviewSuggestion {
  type: 'refactor' | 'optimization' | 'modernize' | 'best-practice';
  title: string;
  description: string;
  codeSnippet?: string;
  suggestedCode?: string;
  impact: 'low' | 'medium' | 'high';
}

export interface CodeMetrics {
  linesOfCode: number;
  complexity: number;
  maintainabilityIndex: number;
  technicalDebt: number;
  testCoverage?: number;
}

export interface SecurityVulnerability {
  id: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  cwe?: string;
  title: string;
  description: string;
  location: {
    file: string;
    line: number;
    column: number;
  };
  codeSnippet: string;
  recommendation: string;
  references?: string[];
}

// ==================== 消息类型 ====================

export interface BaseMessage {
  id: string;
  type: MessageType;
  role: MessageRole;
  timestamp: number;
  metadata?: Record<string, any>;
}

export interface TextMessage extends BaseMessage {
  type: MessageType.TEXT;
  content: string;
  serviceType?: ServiceType;
}

export interface CodeMessage extends BaseMessage {
  type: MessageType.CODE;
  content: string;
  language: string;
  codeBlock?: string;
  explanation?: string;
}

export interface ErrorMessage extends BaseMessage {
  type: MessageType.ERROR;
  content: string;
  code?: string;
  stackTrace?: string;
  recoveryHint?: string;
}

export type Message = TextMessage | CodeMessage | ErrorMessage;

// ==================== 会话管理 ====================

export interface Session {
  id: string;
  userId: string;
  messages: Message[];
  context: SessionContext;
  state: SessionState;
  createdAt: number;
  updatedAt: number;
}

export interface SessionContext {
  currentService?: ServiceType;
  selectedApiEndpoint?: string;
  selectedPlugin?: string;
  selectedSdk?: string;
  codeReviewContext?: {
    code: string;
    language: string;
  };
  additionalData?: Record<string, any>;
}

export interface SessionState {
  status: ConnectionStatus;
  pendingAction?: string;
  lastActivity: number;
}

// ==================== 配置类型 ====================

export interface XiaoyuanConfig {
  // 核心连接
  coreApiUrl: string;
  wsEndpoint: string;
  apiKey?: string;

  // 服务配置
  services: {
    apiManagement: {
      enabled: boolean;
      autoDocument: boolean;
      testingEnabled: boolean;
    };
    pluginDevelopment: {
      enabled: boolean;
      templatesPath: string;
      autoGenerateDocs: boolean;
    };
    sdkManagement: {
      enabled: boolean;
      checkUpdatesInterval: number;  // milliseconds
      autoNotify: boolean;
    };
    codeReview: {
      enabled: boolean;
      strictMode: boolean;
      customRules?: ReviewRule[];
    };
  };

  // 对话配置
  dialog: {
    maxHistoryLength: number;
    timeout: number;
    enableStream: boolean;
  };

  // 开发者配置
  developer: {
    preferredLanguage: string;
    preferredFramework?: string;
    codeStyle: string;  // 'eslint', 'prettier', etc.
  };

  // 日志配置
  logging: {
    level: 'debug' | 'info' | 'warn' | 'error';
    enableConsole: boolean;
    filePath?: string;
  };
}

// ==================== 事件类型 ====================

export interface AdapterEvent {
  type: string;
  data: any;
  timestamp: number;
}

export type EventHandler = (event: AdapterEvent) => void;

// ==================== API 响应类型 ====================

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  code?: number;
}

export interface StreamResponse {
  done: boolean;
  chunk?: string;
  error?: string;
}

// ==================== WebSocket 消息 ====================

export interface WSMessage {
  type: 'connect' | 'message' | 'heartbeat' | 'close' | 'error';
  payload: any;
  messageId?: string;
}

// ==================== 诊断类型 ====================

export interface DiagnosticReport {
  timestamp: number;
  health: 'healthy' | 'degraded' | 'unhealthy';
  checks: DiagnosticCheck[];
}

export interface DiagnosticCheck {
  name: string;
  status: 'pass' | 'fail' | 'warning';
  message: string;
  details?: Record<string, any>;
}
