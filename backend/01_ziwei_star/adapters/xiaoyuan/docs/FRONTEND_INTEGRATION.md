# 小元适配器 - 前端集成示例

本文档提供了在前端应用中集成小元适配器的详细示例和最佳实践。

---

## 目录

1. [React + TypeScript 集成](#react--typescript-集成)
2. [原生 JavaScript 集成](#原生-javascript-集成)
3. [Vue 3 + TypeScript 集成](#vue-3--typescript-集成)
4. [使用 WebSocket 实时通信](#使用-websocket-实时通信)
5. [常见使用场景](#常见使用场景)

---

## React + TypeScript 集成

### 1. 安装依赖

```bash
npm install @xuanji-ai/xiaoyuan-adapter
```

### 2. 创建适配器 Hook

```typescript
// src/hooks/useXiaoyuan.ts
import { useState, useEffect, useCallback } from 'react';
import { XiaoyuanAdapter } from '@xuanji-ai/xiaoyuan-adapter';
import type { Message, Session, ServiceType } from '@xuanji-ai/xiaoyuan-adapter/types';

export const useXiaoyuan = (apiKey: string) => {
  const [adapter, setAdapter] = useState<XiaoyuanAdapter | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // 初始化适配器
  useEffect(() => {
    const initAdapter = async () => {
      try {
        const newAdapter = new XiaoyuanAdapter({
          apiKey,
          coreApiUrl: 'http://localhost:5000/api',
          wsEndpoint: 'ws://localhost:5000/ws',
        });

        // 设置事件监听器
        newAdapter.on('connected', () => {
          setIsConnected(true);
        });

        newAdapter.on('disconnected', () => {
          setIsConnected(false);
        });

        newsetAdapter.on('error', (error) => {
          console.error('Adapter error:', error);
        });

        // 连接到核心服务
        await newAdapter.connect();
        setAdapter(newAdapter);

        // 创建会话
        const newSession = await newAdapter.createSession('user-' + Date.now());
        setSession(newSession);

      } catch (error) {
        console.error('Failed to initialize adapter:', error);
      }
    };

    initAdapter();

    return () => {
      adapter?.disconnect();
    };
  }, [apiKey]);

  // 发送消息
  const sendMessage = useCallback(async (
    content: string,
    serviceType?: ServiceType,
    codeBlock?: string
  ) => {
    if (!adapter || !session || !isConnected) {
      throw new Error('Adapter not ready');
    }

    setIsLoading(true);

    try {
      const message = codeBlock
        ? {
            type: 'code' as const,
            role: 'user' as const,
            content,
            language: 'typescript',
            codeBlock,
            timestamp: Date.now(),
          }
        : {
            type: 'text' as const,
            role: 'user' as const,
            content,
            timestamp: Date.now(),
            serviceType,
          };

      const response = await adapter.handleMessage(session.id, message);
      setMessages(prev => [...prev, message, response]);

      return response;
    } catch (error) {
      console.error('Failed to send message:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [adapter, session, isConnected]);

  return {
    adapter,
    session,
    messages,
    isConnected,
    isLoading,
    sendMessage,
  };
};
```

### 3. 创建聊天组件

```typescript
// src/components/Chat.tsx
import React, { useState, useRef, useEffect } from 'react';
import { useXiaoyuan } from '../hooks/useXiaoyuan';
import { ServiceType } from '@xuanji-ai/xiaoyuan-adapter/types';

export const Chat: React.FC<{ apiKey: string }> = ({ apiKey }) => {
  const { messages, isConnected, isLoading, sendMessage } = useXiaoyuan(apiKey);
  const [input, setInput] = useState('');
  const [serviceType, setServiceType] = useState<ServiceType | undefined>(ServiceType.API_MANAGEMENT);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 自动滚动到最新消息
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    try {
      await sendMessage(input, serviceType);
      setInput('');
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>小元 - 开发者助手</h2>
        <div className="connection-status">
          <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`} />
          {isConnected ? '已连接' : '未连接'}
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              {message.type === 'code' && message.codeBlock ? (
                <pre>
                  <code>{message.codeBlock}</code>
                </pre>
              ) : (
                <p>{message.content}</p>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant loading">
            <span className="typing-indicator">...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-controls">
        <select
          value={serviceType || ''}
          onChange={(e) => setServiceType(e.target.value as ServiceType)}
          className="service-selector"
        >
          <option value="">自动识别</option>
          <option value={ServiceType.API_MANAGEMENT}>API 管理</option>
          <option value={ServiceType.PLUGIN_DEVELOPMENT}>插件开发</option>
          <option value={ServiceType.SDK_MANAGEMENT}>SDK 管理</option>
          <option value={ServiceType.CODE_REVIEW}>代码审查</option>
        </select>

        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="输入您的问题..."
          rows={3}
          disabled={!isConnected || isLoading}
        />

        <button
          onClick={handleSend}
          disabled={!input.trim() || !isConnected || isLoading}
          className="send-button"
        >
          发送
        </button>
      </divendi>
    </div>
  );
};

// 样式
const styles = `
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.chat-header {
  padding: 16px;
  background: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ccc;
}

.status-indicator.connected {
  background: #4caf50;
}

.status-indicator.disconnected {
  background: #f44336;
}

.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.message {
  margin-bottom: 16px;
  padding: 12px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background: #e3f2fd;
  margin-left: auto;
}

.message.assistant {
  background: #f5f5f5;
}

.message-content pre {
  background: #f5f5f5;
  padding: 8px;
  border-radius: 4px;
  overflow-x: auto;
}

.chat-controls {
  padding: 16px;
  background: #f5f5f5;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 8px;
}

.service-selector {
  padding: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.chat-controls textarea {
  flex: 1;
  padding: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  resize: none;
}

.send-button {
  padding: 8px 24px;
  background: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.send-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
`;
```

### 4. 在应用中使用

```typescript
// src/App.tsx
import React from 'react';
import { Chat } from './components/Chat';

function App() {
  return (
    <div className="App">
      <Chat apiKey="your-api-key" />
    </div>
  );
}

export default App;
```

---

## 原生 JavaScript 集成

### 1. 基本集成

```javascript
// 直接使用 HTTP API
class XiaoyuanClient {
  constructor(apiKey, baseUrl = 'http://localhost:5000/api/xiaoyuan') {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
    this.sessionId = null;
  }

  async createSession(userId) {
    const response = await fetch(`${this.baseUrl}/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({ userId }),
    });

    const result = await response.json();
    if (result.success) {
      this.sessionId = result.data.id;
      return result.data;
    }
    throw new Error(result.error);
  }

  async sendMessage(content, serviceType) {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    const response = await fetch(`${this.baseUrl}/sessions/${this.sessionId}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        type: 'text',
        content,
        serviceType,
      }),
    });

    const result = await response.json();
    if (result.success) {
      return result.data;
    }
    throw new Error(result.error);
  }
}

// 使用示例
const client = new XiaoyuanClient('your-api-key');

// 创建会话
client.createSession('user-123').then(session => {
  console.log('Session created:', session.id);

  // 发送消息
  return client.sendMessage('帮我生成一个插件模板', 'plugin_development');
}).then(response => {
  console.log('Response:', response.content);
});
```

### 2. WebSocket 集成

```javascript
class XiaoyuanWebSocketClient {
  constructor(apiKey, wsUrl = 'ws://localhost:5000/ws/xiaoyuan') {
    this.apiKey = apiKey;
    this.wsUrl = `${wsUrl}?token=${apiKey}`;
    this.ws = null;
    this.messageHandlers = new Map();
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        resolve();
      };

      this.ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket closed');
      };
    });
  }

  send(sessionId, content, serviceType) {
    const message = {
      type: 'message',
      sessionId,
      payload: {
        type: 'text',
        content,
        serviceType,
      },
    };

    this.ws.send(JSON.stringify(message));
  }

  on(type, handler) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, []);
    }
    this.messageHandlers.get(type).push(handler);
  }

  handleMessage(message) {
    const handlers = this.messageHandlers.get(message.type) || [];
    handlers.forEach(handler => handler(message.payload));
  }

  disconnect() {
    this.ws?.close();
  }
}

// 使用示例
const client = new XiaoyuanWebSocketClient('your-api-key');

client.on('response', (response) => {
  console.log('Received response:', response.content);
});

client.on('notification', (notification) => {
  console.log('Received notification:', notification);
});

client.connect().then(() => {
  client.send('session-123', '帮我审查这段代码', 'code_review');
});
```

---

## Vue 3 + TypeScript 集成

### 1. 创建插件

```typescript
// src/plugins/xiaoyuan.ts
import { Plugin } from 'vue';
import { ref, reactive } from 'vue';
import { XiaoyuanAdapter } from '@xuanji-ai/xiaoyuan-adapter';

export const xiaoyuanPlugin: Plugin = {
  install(app) {
    const adapter = ref<XiaoyuanAdapter | null>(null);
    const isConnected = ref(false);
    const currentSession = ref<any>(null);

    const initialize = async (apiKey: string) => {
      adapter.value = new XiaoyuanAdapter({ apiKey });

      adapter.value.on('connected', () => {
        isConnected.value = true;
      });

      adapter.value.on('disconnected', () => {
        isConnected.value = false;
      });

      await adapter.value.connect();
      currentSession.value = await adapter.value.createSession('vue-user');
    };

    const sendMessage = async (content: string, serviceType?: string) => {
      if (!adapter.value || !currentSession.value) {
        throw new Error('Adapter not initialized');
      }

      return await adapter.value.handleMessage(currentSession.value.id, {
        type: 'text',
        role: 'user',
        content,
        timestamp: Date.now(),
        serviceType,
      });
    };

    app.provide('xiaoyuan', {
      adapter,
      isConnected,
      currentSession,
      initialize,
      sendMessage,
    });
  },
};

declare module '@vue/runtime-core' {
  export interface ComponentCustomProperties {
    $xiaoyuan: {
      adapter: typeof adapter;
      isConnected: typeof isConnected;
      currentSession: typeof currentSession;
      initialize: typeof initialize;
      sendMessage: typeof sendMessage;
    };
  }
}
```

### 2. 在组件中使用

```vue
<!-- src/components/XiaoyuanChat.vue -->
<template>
  <div class="chat-container">
    <div class="messages">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.role]"
      >
        {{ message.content }}
      </div>
    </div>

    <div class="input-area">
      <input v-model="input" @keyup.enter="handleSend" placeholder="输入消息..." />
      <button @click="handleSend" :disabled="!isConnected">发送</button>
    </div>
  </div>
endi>
</template>

<script setup lang="ts">
import { ref, inject, onMounted } from 'vue';
import type { Ref } from 'vue';

const xiaoyuan = inject<{
  isConnected: Ref<boolean>;
  initialize: (apiKey: string) => Promise<void>;
  sendMessage: (content: string, serviceType?: string) => Promise<any>;
}>('xiaoyuan');

const messages = ref<any[]>([]);
const input = ref('');

const isConnected = xiaoyuan?.isConnected || ref(false);

onMounted(async () => {
  await xiaoyuan?.initialize('your-api-key');
});

const handleSend = async () => {
  if (!input.value.trim()) return;

  try {
    const response = await xiaoyuan?.sendMessage(input.value);
    if (response) {
      messages.value.push(
        { role: 'user', content: input.value },
        { role: 'assistant', content: response.content }
      );
    }
    input.value = '';
  } catch (error) {
    console.error('Failed to send message:', error);
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 16px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 16px;
}

.message {
  padding: 8px 16px;
  margin: 8px 0;
  border-radius: 8px;
}

.message.user {
  background: #e3f2fd;
  margin-left: auto;
}

.message.assistant {
  background: #f5f5f5;
}

.input-area {
  display: flex;
  gap: 8px;
}

input {
  flex: 1;
  padding: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

button {
  padding: 8px 24px;
  background: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
```

---

## 使用 WebSocket 实时通信

### React + TypeScript 示例

```typescript
import { useEffect, useRef, useState } from 'react';

export const useXiaoyuanWebSocket = (apiKey: string) => {
  const wsRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:5000/ws/xiaoyuan?token=${apiKey}`);

    ws.onopen = () => {
      setIsConnected(true);
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log('Received:', message);

      if (message.type === 'response') {
        setMessages(prev => [...prev, message.payload]);
      } else if (message.type === 'notification') {
        console.log('Notification:', message.payload);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket closed');
    };

    wsRef.current = ws;

    return () => {
      ws.close();
    };
  }, [apiKey]);

  const sendMessage = (sessionId: string, content: string, serviceType?: string) => {
    if (!wsRef.current || !isConnected) {
      throw new Error('WebSocket not connected');
    }

    wsRef.current.send(JSON.stringify({
      type: 'message',
      sessionId,
      payload: {
        type: 'text',
        content,
        serviceType,
      },
    }));
  };

  return { isConnected, messages, sendMessage };
};
```

---

## 常见使用场景

### 场景 1: API 文档生成

```typescript
const generateApiDoc = async () => {
  const response = await sendMessage(
    '帮我生成 API 文档',
    'api_management'
  );

  if (response.type === 'code') {
    // 显示 Markdown 文档
    console.log(response.codeBlock);
  }
};
```

### 场景 2: 代码审查

```typescript
const reviewCode = async (code: string) => {
  const response = await sendMessage(
    '审查这段代码',
    'code_review',
    code
  );

  console.log('审查结果:', response.content);
};
```

### 场景 3: 创建插件

```typescript
const createPlugin = async (pluginName: string) => {
  const response = await sendMessage(
    `帮我创建一个名为 ${pluginName} 的插件`,
    'plugin_development'
  );

  console.log('插件模板:', response.content);
};
```

### 场景 4: SDK 集成指南

```typescript
const getSdkGuide = async (sdkName: string) => {
  const response = await sendMessage(
    `如何集成 ${sdkName} SDK`,
    'sdk_management'
  );

  console.log('集成指南:', response.content);
};
```

---

## 错误处理

```typescript
import { XiaoyuanAdapter } from '@xuanji-ai/xiaoyuan-adapter';

try {
  const adapter = new XiaoyuanAdapter({ apiKey: 'your-api-key' });
  await adapter.connect();
} catch (error) {
  if (error.message.includes('API key')) {
    console.error('API Key 无效');
  } else if (error.message.includes('connection')) {
    console.error('连接失败，请检查网络');
  } else {
    console.error('未知错误:', error);
  }
}
```

---

## 性能优化建议

1. **使用会话复用**: 不要为每次请求创建新会话
2. **消息限流**: 避免过于频繁的消息发送
3. **错误重试**: 实现指数退避重试机制
4. **缓存结果**: 缓存常用的 API 响应
5. **连接池**: 对于高并发场景，使用连接池管理

---

## 安全建议

1. **保护 API Key**: 不要在前端代码中硬编码 API Key
2. **使用 HTTPS**: 生产环境必须使用 HTTPS/WSS
3. **验证响应**: 验证所有从适配器收到的数据
4. **权限控制**: 根据用户角色限制功能访问
5. **日志监控**: 监控异常访问和错误日志

---

## 完整示例项目

示例项目结构：

```
xiaoyuan-react-example/
├── src/
│   ├── components/
│   │   ├── Chat.tsx
│   │   ├── CodeEditor.tsx
│   │   └── ApiViewer.tsx
│   ├── hooks/
│   │   └── useXiaoyuan.ts
│   ├── services/
│   │   └── xiaoyuan.service.ts
│   └── App.tsx
├── package.json
└── tsconfig.json
```

参考更多完整示例：
- [React 示例](https://github.com/xuanji-ai/xiaoyuan-react-example)
- [Vue 示例](https://github.com/xuanji-ai/xiaoyuan-vue-example)
- [原生 JS 示例](https://github.com/xuanji-ai/xiaoyuan-js-example)
