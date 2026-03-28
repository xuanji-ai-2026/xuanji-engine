// 插件相关类型
export interface Plugin {
  id: string;
  name: string;
  displayName: string;
  description: string;
  version: string;
  author: string;
  icon?: string;
  screenshots: string[];
  category: PluginCategory;
  tags: string[];
  status: 'active' | 'beta' | 'deprecated';
  pricing: PluginPricing;
  rating: number;
  reviewCount: number;
  downloadCount: number;
  installCount: number;
  features: string[];
  permissions: string[];
  dependencies: string[];
  compatibility: string[];
  documentation?: string;
  sourceCode?: string;
  createdAt: string;
  updatedAt: string;
}

export type PluginCategory =
  | 'productivity'
  | 'entertainment'
  | 'education'
  | 'finance'
  | 'health'
  | 'social'
  | 'tools'
  | 'ai'
  | 'integration';

export interface PluginPricing {
  type: 'free' | 'paid' | 'freemium';
  price?: number;
  currency?: string;
  trialPeriod?: number;
  subscription?: {
    monthly?: number;
    yearly?: number;
  };
}

export interface InstalledPlugin {
  pluginId: string;
  version: string;
  status: 'active' | 'inactive' | 'error';
  installedAt: string;
  updatedAt: string;
  settings?: Record<string, unknown>;
  permissions: string[];
}

export interface InstallPluginRequest {
  pluginId: string;
  version?: string;
}

export interface PluginReview {
  id: string;
  pluginId: string;
  userId: string;
  username: string;
  avatar?: string;
  rating: number;
  title?: string;
  content: string;
  createdAt: string;
  updatedAt: string;
  helpfulCount: number;
}
