const config = {
  // API 配置
  api: {
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    timeout: 30000,
  },

  // 应用配置
  app: {
    name: '玄玑引擎用户端',
    version: '1.0.0',
    description: 'AI数字人智能配置平台',
  },

  // 认证配置
  auth: {
    tokenKey: 'xuanji_token',
    refreshTokenKey: 'xuanji_refresh_token',
    userKey: 'xuanji_user',
    tokenExpiry: 24 * 60 * 60 * 1000, // 24 hours
  },

  // WebSocket 配置
  ws: {
    baseURL: import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:5000',
    reconnectInterval: 5000,
    maxReconnectAttempts: 10,
  },

  // 文件上传配置
  upload: {
    maxSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: ['image/*', 'audio/*', 'video/*', 'application/pdf'],
    chunkSize: 5 * 1024 * 1024, // 5MB
  },

  // 限制配置
  limits: {
    maxDigitalHumans: 10,
    maxChatsPerDay: 100,
    maxPlugins: 20,
    maxFileSize: 50 * 1024 * 1024, // 50MB
  },

  // 默认配置
  defaults: {
    theme: 'light' as const,
    language: 'zh-CN' as const,
    timezone: 'Asia/Shanghai',
  },

  // 功能开关
  features: {
    enableVoiceInput: true,
    enableVoiceOutput: true,
    enableAutoSave: true,
    enableRealtimeSync: true,
  },
};

export default config;
