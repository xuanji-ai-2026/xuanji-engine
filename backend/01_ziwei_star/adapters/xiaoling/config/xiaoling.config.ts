/**
 * 小灵（Xiaoling）适配层配置
 * 管理端智能助手配置
 */

export interface XiaolingConfig {
  // WebSocket 配置
  websocket: {
    enabled: boolean;
    url: string;
    reconnectInterval: number;
    maxRetries: number;
  };

  // HTTP API 配置
  http: {
    baseUrl: string;
    timeout: number;
    maxRetries: number;
  };

  // 缓存配置
  cache: {
    enabled: boolean;
    ttl: number; // 秒
    maxSize: number;
  };

  // 性能监控配置
  performance: {
    enabled: boolean;
    sampleRate: number; // 采样率 0-1
    alertThreshold: {
      cpu: number; // 百分比
      memory: number; // 百分比
      responseTime: number; // 毫秒
    };
  };

  // 日志配置
  logging: {
    level: 'debug' | 'info' | 'warn' | 'error';
    enableConsole: boolean;
    enableFile: boolean;
    maxFileSize: number;
  };
}

export const defaultConfig: XiaolingConfig = {
  websocket: {
    enabled: true,
    url: 'ws://localhost:5000/xiaoling',
    reconnectInterval: 3000,
    maxRetries: 5,
  },

  http: {
    baseUrl: 'http://localhost:5000/api/xiaoling',
    timeout: 10000,
    maxRetries: 3,
  },

  cache: {
    enabled: true,
    ttl: 300,
    maxSize: 1000,
  },

  performance: {
    enabled: true,
    sampleRate: 0.1,
    alertThreshold: {
      cpu: 80,
      memory: 85,
      responseTime: 3000,
    },
  },

  logging: {
    level: 'info',
    enableConsole: true,
    enableFile: false,
    maxFileSize: 10485760, // 10MB
  },
};
