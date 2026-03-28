// 对话相关类型
export interface ChatMessage {
  id: string;
  chatId: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  metadata?: {
    digitalHumanId?: string;
    model?: string;
    tokens?: number;
    latency?: number;
    error?: string;
  };
  attachments?: ChatAttachment[];
}

export interface ChatAttachment {
  id: string;
  type: 'image' | 'audio' | 'video' | 'file';
  url: string;
  name: string;
  size: number;
  mimeType: string;
}

export interface Chat {
  id: string;
  userId: string;
  digitalHumanId: string;
  title: string;
  status: 'active' | 'archived' | 'deleted';
  messageCount: number;
  createdAt: string;
  updatedAt: string;
  lastMessageAt?: string;
  digitalHuman?: DigitalHumanSummary;
}

export interface DigitalHumanSummary {
  id: string;
  name: string;
  displayName: string;
  avatar?: string;
}

export interface SendMessageRequest {
  content: string;
  attachments?: ChatAttachment[];
  stream?: boolean;
  options?: {
    temperature?: number;
    maxTokens?: number;
  };
}

export interface ChatStreamResponse {
  delta: string;
  done: boolean;
  metadata?: Record<string, unknown>;
}

export interface VoiceInputConfig {
  enabled: boolean;
  language: 'zh-CN' | 'en-US' | 'ja-JP' | 'ko-KR';
  autoSubmit: boolean;
  timeout: number;
}

export interface VoiceOutputConfig {
  enabled: boolean;
  voice: string;
  speed: number;
  pitch: number;
  volume: number;
}
