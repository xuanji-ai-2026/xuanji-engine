// 智能助手小紫相关类型
export interface AssistantMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  type: 'text' | 'voice' | 'action' | 'recommendation';
  metadata?: {
    actionType?: string;
    actionData?: Record<string, unknown>;
    recommendations?: string[];
  };
}

export interface AssistantContext {
  currentModule: string;
  recentActions: string[];
  userPreferences: Record<string, unknown>;
  digitalHumanCount: number;
  activePlugins: number;
  balance: number;
}

export interface AssistantAction {
  type: 'navigate' | 'configure' | 'create' | 'guide' | 'recommend';
  target: string;
  params?: Record<string, unknown>;
  description: string;
}

export interface VoiceInteraction {
  enabled: boolean;
  language: 'zh-CN' | 'en-US';
  autoStart: boolean;
  voiceId: string;
}

export interface GuideStep {
  id: string;
  title: string;
  content: string;
  target?: string;
  position?: 'top' | 'bottom' | 'left' | 'right';
  action?: string;
  image?: string;
}

export interface OnboardingGuide {
  id: string;
  userId: string;
  step: number;
  completed: boolean;
  startedAt: string;
  completedAt?: string;
}

export interface Recommendation {
  id: string;
  type: 'plugin' | 'digital-human' | 'feature' | 'config';
  title: string;
  description: string;
  imageUrl?: string;
  actionUrl?: string;
  priority: number;
  dismissed?: boolean;
}
