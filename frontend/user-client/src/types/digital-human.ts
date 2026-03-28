// 数字人相关类型
export interface DigitalHuman {
  id: string;
  userId: string;
  name: string;
  displayName: string;
  avatar?: string;
  description?: string;
  personality: Personality;
  emotion: EmotionSettings;
  plugins: string[];
  knowledgeBaseId?: string;
  status: 'active' | 'inactive' | 'training' | 'error';
  modelConfig: ModelConfig;
  createdAt: string;
  updatedAt: string;
  lastUsedAt?: string;
}

export interface Personality {
  traits: PersonalityTrait[];
  tone: 'formal' | 'casual' | 'friendly' | 'professional' | 'humorous';
  language: 'zh-CN' | 'en-US' | 'ja-JP' | 'ko-KR';
  responseStyle: 'concise' | 'detailed' | 'creative' | 'analytical';
  customPrompt?: string;
}

export interface PersonalityTrait {
  name: string;
  value: number; // 0-100
  description?: string;
}

export interface EmotionSettings {
  enabled: boolean;
  baseEmotion: 'happy' | 'calm' | 'excited' | 'serious' | 'gentle';
  emotionSensitivity: number; // 0-100
  emotionExpression: 'subtle' | 'moderate' | 'expressive';
  customEmotions?: Record<string, number>;
}

export interface ModelConfig {
  model: string;
  temperature: number;
  maxTokens: number;
  topP: number;
  frequencyPenalty: number;
  presencePenalty: number;
}

export interface CreateDigitalHumanRequest {
  name: string;
  displayName: string;
  description?: string;
  personality?: Partial<Personality>;
  emotion?: Partial<EmotionSettings>;
  modelConfig?: Partial<ModelConfig>;
  templateId?: string;
}

export interface UpdateDigitalHumanRequest {
  displayName?: string;
  description?: string;
  personality?: Partial<Personality>;
  emotion?: Partial<EmotionSettings>;
  modelConfig?: Partial<ModelConfig>;
  plugins?: string[];
  knowledgeBaseId?: string;
}

// 数字人模板
export interface DigitalHumanTemplate {
  id: string;
  name: string;
  displayName: string;
  description: string;
  category: string;
  thumbnail: string;
  personality: Personality;
  emotion: EmotionSettings;
  modelConfig: ModelConfig;
  isPublic: boolean;
  usageCount: number;
}
