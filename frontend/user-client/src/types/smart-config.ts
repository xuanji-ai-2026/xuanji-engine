// 智能配置相关类型
export interface SmartConfigSession {
  id: string;
  userId: string;
  status: 'pending' | 'active' | 'completed' | 'failed';
  configType: 'digital-human' | 'chat' | 'plugin' | 'knowledge';
  currentStep: number;
  totalSteps: number;
  progress: number;
  data: Record<string, unknown>;
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
}

export interface ConfigMessage {
  id: string;
  sessionId: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface SmartConfigRequest {
  message: string;
  sessionId?: string;
  context?: Record<string, unknown>;
}

export interface SmartConfigResponse {
  message: string;
  action: 'continue' | 'complete' | 'clarify';
  data?: Record<string, unknown>;
  suggestions?: string[];
  nextQuestions?: string[];
}

// 配置历史
export interface ConfigHistory {
  id: string;
  userId: string;
  configType: string;
  configName: string;
  configData: Record<string, unknown>;
  version: number;
  appliedAt: string;
  appliedBy: string;
  description?: string;
}

// 配置模板
export interface ConfigTemplate {
  id: string;
  name: string;
  displayName: string;
  description: string;
  category: string;
  tags: string[];
  configSchema: Record<string, unknown>;
  defaultValues: Record<string, unknown>;
  isPublic: boolean;
  usageCount: number;
  createdAt: string;
  updatedAt: string;
}
