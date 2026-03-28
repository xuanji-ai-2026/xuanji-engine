/**
 * 小紫 - 用户端智能助手适配层
 * 类型定义文件
 */

// ==================== 基础类型 ====================

export enum MessageType {
  TEXT = 'text',
  VOICE = 'voice',
  IMAGE = 'image',
  SYSTEM = 'system',
  ACTION = 'action'
}

export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
  SYSTEM = 'system'
}

export enum ConnectionState {
  DISCONNECTED = 'disconnected',
  CONNECTING = 'connecting',
  CONNECTED = 'connected',
  ERROR = 'error'
}

export enum GuideType {
  NEW_ONBOARDING = 'new_onboarding',    // 新用户引导
  FEATURE_DISCOVERY = 'feature_discovery', // 功能发现
  OPERATION_HINT = 'operation_hint',    // 操作提示
  TROUBLESHOOTING = 'troubleshooting'   // 故障排除
}

export enum RecommendationType {
  CONFIGURATION = 'configuration',       // 配置推荐
  FEATURE = 'feature',                   // 功能推荐
  BEST_PRACTICE = 'best_practice',       // 最佳实践
  OPTIMIZATION = 'optimization'         // 优化建议
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
}

export interface VoiceMessage extends BaseMessage {
  type: MessageType.VOICE;
  audioData: ArrayBuffer | string;  // 二进制数据或 URL
  transcript?: string;
  duration?: number;
}

export interface ImageMessage extends BaseMessage {
  type: MessageType.IMAGE;
  imageData: string;  // base64 或 URL
  caption?: string;
}

export interface SystemMessage extends BaseMessage {
  type: MessageType.SYSTEM;
  content: string;
  level: 'info' | 'warning' | 'error' | 'success';
}

export type Message = TextMessage | VoiceMessage | ImageMessage | SystemMessage;

// ==================== 对话会话 ====================

export interface Conversation {
  id: string;
  userId: string;
  sessionId: string;
  messages: Message[];
  state: Record<string, any>;
  createdAt: number;
  updatedAt: number;
}

// ==================== 智能引导相关 ====================

export interface GuideStep {
  id: string;
  title: string;
  content: string;
  type: GuideType;
  order: number;
  actionable?: boolean;
  actions?: GuideAction[];
  nextStepId?: string;
  skipCondition?: string;  // 跳过条件表达式
}

export interface GuideAction {
  id: string;
  label: string;
  type: 'navigation' | 'api_call' | 'ui_highlight';
  payload: Record<string, any>;
}

export interface GuideFlow {
  id: string;
  name: string;
  description: string;
  type: GuideType;
  steps: GuideStep[];
  prerequisites?: string[];  // 前置条件
}

export interface GuideState {
  flowId: string;
  currentStepId: string;
  completedSteps: string[];
  startTime: number;
  progress: number;  // 0-100
}

// ==================== 推荐引擎相关 ====================

export interface UserBehavior {
  timestamp: number;
  action: string;
  context: Record<string, any>;
  features: string[];
}

export interface Recommendation {
  id: string;
  type: RecommendationType;
  title: string;
  description: string;
  priority: number;  // 0-100
  confidence: number;  // 0-1
  actions?: RecommendationAction[];
  expiresAt?: number;
}

export interface RecommendationAction {
  type: 'apply' | 'dismiss' | 'snooze';
'': string;
}

export interface UserProfile {
  userId: string;
  preferences: Record<string, any>;
  behaviors: UserBehavior[];
  skillLevel: 'beginner' | 'intermediate' | 'advanced';
  lastActiveTime: number;
}

// ==================== 问题诊断相关 ====================

export interface DiagnosticResult {
  id: string;
  timestamp: number;
  issueType: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  symptoms: string[];
  solutions: Solution[];
  requiresHuman: boolean;
}

export interface Solution {
  id: string;
  title: string;
  description: string;
  steps: string[];
  autoFix?: boolean;
  estimatedTime?: number;  // 估算时间（秒）
}

// ==================== 自动化操作相关 ====================

export interface AutomationTask {
  id: string;
  type: 'form_fill' | 'navigation' | 'batch_operation';
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  steps: AutomationStep[];
  result?: any;
  error?: string;
}

export interface AutomationStep {
  id: string;
  type: string;
  selector?: string;  // UI 选择器
  value?: any;
  action: string;
  options?: Record<string, any>;
}

// ==================== 适配器配置 ====================

export interface XiaopurpleConfig {
  // 核心连接
  coreApiUrl: string;
WSEndpoint: string;
  apiKey?: string;

  // 对话配置
  dialog: {
    maxHistoryLength: number;
    timeout: number;
    enableVoice: boolean;
    enableStream: boolean;
  };

  // 引导配置
  guidance: {
    enabled: boolean;
    autoStartOnboarding: boolean;
    skipThreshold: number;  // 连续跳过多少次后不再提示
  };

  // 推荐配置
  recommendation: {
    enabled: boolean;
    maxRecommendations: number;
    behaviorRetentionDays: number;
    minConfidenceThreshold: number;
  };

  // 诊断配置
  diagnostic: {
    enabled: boolean;
    autoDiagnose: boolean;
    maxRetries: number;
  };

  // 自动化配置
  automation: {
    enabled: boolean;
    requireConfirmation: boolean;
    maxConcurrentTasks: number;
  };

  // 日志配置
  logging: {
    level: 'debug' | 'info' | 'warn' | 'error';
    enableConsole: boolean;
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
