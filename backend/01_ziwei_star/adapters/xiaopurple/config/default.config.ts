/**
 * 小紫 - 默认配置
 */

import { XiaopurpleConfig } from '../types';

export const defaultConfig: XiaopurpleConfig = {
  // 核心连接配置
  coreApiUrl: 'http://localhost:8080/api',
  wsEndpoint: 'ws://localhost:8080/ws',
  apiKey: undefined,

  // 对话配置
  dialog: {
    maxHistoryLength: 100,
    timeout: 30000,  // 30秒
    enableVoice: true,
    enableStream: true
  },

  // 引导配置
  guidance: {
    enabled: true,
    autoStartOnboarding: true,
    skipThreshold: 3  // 连续跳过3次后不再提示
  },

  // 推荐配置
  recommendation: {
    enabled: true,
    maxRecommendations: 5,
    behaviorRetentionDays: 30,
    minConfidenceThreshold: 0.5
  },

  // 诊断配置
  diagnostic: {
    enabled: true,
    autoDiagnose: true,
    maxRetries: 3
  },

  // 自动化配置
  automation: {
    enabled: true,
    requireConfirmation: true,
    maxConcurrentTasks: 5
  },

  // 日志配置
  logging: {
    level: 'info',
    enableConsole: true
  }
};
