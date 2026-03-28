# 小紫 - React 前端集成示例

本文档展示如何在 React 18.3.1 + TypeScript 项目中集成小紫适配层。

## 1. 安装依赖

```bash
npm install react@18.3.1 typescript@5.x
```

## 2. 创建适配层上下文

```typescript
// src/contexts/XiaopxurpleContext.tsx
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {
  XiaopurpleAdapter,
  GuideEngine,
  RecommendationEngine,
  DiagnosticEngine,
  AutomationEngine,
  defaultConfig,
  Message,
  Recommendation,
  DiagnosticResult
} from '../../../backend/01_ziwei_star/adapters/xiaopurple/src';

interface XiaopurpleContextType {
  // 适配器
  adapter: XiaopurpleAdapter | null;
  isConnected: boolean;

  // 引擎
  guideEngine: GuideEngine;
  recommendationEngine: RecommendationEngine;
  diagnosticEngine: DiagnosticEngine;
  automationEngine: AutomationEngine;

  // 消息
  messages: Message[];
  sendMessage: (message: Message) => Promise<void>;

  // 推荐
  recommendations: Recommendation[];

  // 加载状态
  loading: boolean;
  error: string | null;
}

const XiaopurpleContext = createContext<XiaopurpleContextType | undefined>(undefined);

export const XiaopurpleProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [adapter, setAdapter] = useState<XiaopurpleAdapter | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 初始化引擎
  const guideEngine = new GuideEngine();
  const recommendationEngine = new RecommendationEngine();
  const diagnosticEngine = new DiagnosticEngine();
  const automationEngine = new AutomationEngine(true);

  // 初始化适配器
  useEffect(() => {
    const init = async () => {
      try {
        setLoading(true);
        setError(null);

        // 创建适配器
        const newAdapter = new XiaopurpleAdapter(defaultConfig);

        // 监听消息
        newAdapter.on('message:received', (event) => {
          setMessages(prev => [...prev, event.data.message]);
        });

        newAdapter.on('ws:connected', () => {
          setIsConnected(true);
        });

        newAdapter.on('ws:disconnected', () => {
          setIsConnected(false);
        });

        newAdapter.on('ws:error', (event) => {
          setError(event.data.error?.toString() || '连接错误');
        });

        // 启动适配器
        await newAdapter.start();

        setAdapter(newAdapter);

        // 初始化推荐
        const recs = recommendationEngine.getRecommendations(5);
        setRecommendations(recs);

      } catch (err) {
        setError(err instanceof Error ? err.message : '初始化失败');
      } finally {
        setLoading(false);
      }
    };

    init();

    return () => {
      adapter?.stop();
    };
  }, []);

  // 发送消息
  const sendMessage = async (message: Message) => {
    if (!adapter) {
      throw new Error('适配器未初始化');
    }

    await adapter.sendMessage(message);
    setMessages(prev => [...prev, message]);

    // 追踪行为
    await recommendationEngine.trackBehavior('send_message', {
      messageType: message.type
    });

    // 更新推荐
    const recs = recommendationEngine.getRecommendations(5);
    setRecommendations(recs);
  };

  const value: XiaopurpleContextType = {
    adapter,
    isConnected,
    guideEngine,
    recommendationEngine,
    diagnosticEngine,
    automationEngine,
    messages,
    sendMessage,
    recommendations,
    loading,
    error
  };

  return (
    <XiaopurpleContext.Provider value={value}>
      {children}
    </XiaopurpleContext.Provider>
  );
};

export const useXiaopurple = () => {
  const context = useContext(XiaopurpleContext);
  if (!context) {
    throw new Error('useXiaopurple 必须在 XiaopurpleProvider 内部使用');
  }
  return context;
};
```

## 3. 聊天组件

```typescript
// src/components/ChatWidget.tsx
import React, { useState, useRef, useEffect } from 'react';
import { useXiaopurple } from '../contexts/XiaopurpleContext';
import { MessageType, MessageRole, VoiceMessage, ImageMessage } from '../../../backend/01_ziwei_star/adapters/xiaopurple/src';

interface ChatMessage {
  id: string;
  role: string;
  content: string;
  type: MessageType;
}

export const ChatWidget: React.FC = () => {
  const { sendMessage, messages, isConnected } = useXiaopurple();
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!input.trim() || !isConnected) return;

    try {
      await sendMessage({
        id: generateId(),
        type: MessageType.TEXT,
        role: MessageRole.USER,
        content: input,
        timestamp: Date.now()
      });

      setInput('');
    } catch (error) {
      console.error('发送失败:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const startVoiceInput = () => {
    setIsRecording(true);
    // TODO: 集成语音录制逻辑
  };

  const stopVoiceInput = async () => {
    setIsRecording(false);
    // TODO: 发送语音消息
  };

  return (
    <div className="chat-widget">
      <div className="chat-header">
        <h3>💜 小紫助手</h3>
        <div className="connection-status">
          <span className={isConnected ? 'connected' : 'disconnected'}>
            {isConnected ? '● 已连接' : '● 未连接'}
          </span>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <div className="input-wrapper">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="输入消息..."
            rows={3}
            disabled={!isConnected}
          />
          <button
            className="voice-button"
            onClick={isRecording ? stopVoiceInput : startVoiceInput}
            disabled={!isConnected}
          >
            {isRecording ? '⏹️' : '🎤'}
          </button>
          <button
            className="send-button"
            onClick={handleSend}
            disabled={!input.trim() || !isConnected}
          >
            发送
          </button>
        </div>
      </div>
    </div>
  );
};

const MessageBubble: React.FC<{ message: ChatMessage }> = ({ message }) => {
  const isUser = message.role === MessageRole.USER;

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-content">
        {message.type === MessageType.TEXT && (
          <p>{message.content}</p>
        )}
        {message.type === MessageType.VOICE && (
          <div className="voice-message">
            🔊 语音消息
          </div>
        )}
        {message.type === MessageType.IMAGE && (
          <div className="image-message">
            🖼️ 图片消息
          </div>
        )}
      </div>
      <div className="message-meta">
        <span className="timestamp">
          {new Date(message.timestamp).toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
};

function generateId(): string {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};
```

## 4. 推荐组件

```typescript
// src/components/RecommendationPanel.tsx
import React from 'react';
import { useXiaopurple } from '../contexts/XiaopurpleContext';
import { Recommendation } from '../../../backend/01_ziwei_star/adapters/xiaopurple/src';

export const RecommendationPanel: React.FC = () => {
  const { recommendations, recommendationEngine } = useXiaopurple();

  const handleApply = async (rec: Recommendation) => {
    try {
      await recommendationEngine.applyRecommendation(rec.id, rec.actions?.[0]?.payload);
      // 触发重新获取推荐
    } catch (error) {
      console.error('应用推荐失败:', error);
    }
  };

  const handleDismiss = async (rec: Recommendation) => {
    await recommendationEngine.dismissRecommendation(rec.id);
  };

  if (recommendations.length === 0) {
    return (
      <div className="recommendation-panel">
        <p>暂无推荐</p>
      </div>
    );
  }

  return (
    <div className="recommendation-panel">
      <h3>💡 智能推荐</h3>
      {recommendations.map((rec) => (
        <RecommendationCard
          key={rec.id}
          recommendation={rec}
          onApply={() => handleApply(rec)}
          onDismiss={() => handleDismiss(rec)}
        />
      ))}
    </div>
  );
};

interface RecommendationCardProps {
  recommendation: Recommendation;
  onApply: () => void;
  onDismiss: () => void;
}

const RecommendationCard: React.FC<RecommendationCardProps> = ({
  recommendation,
  onApply,
  onDismiss
}) => {
  return (
    <div className="recommendation-card">
      <div className="card-header">
        <h4>{recommendation.title}</h4>
        <span className="confidence">
          置信度: {Math.round(recommendation.confidence * 100)}%
        </span>
      </div>
      <p className="description">{recommendation.description}</p>
      <div className="card-actions">
        {recommendation.actions?.map((action, index) => (
          <button
            key={index}
            className={`action-btn ${action.type}`}
            onClick={onApply}
          >
            {action.label}
          </button>
        ))}
        <button className="dismiss-btn" onClick={onDismiss}>
          驳回
        </button>
      </div>
    </div>
  );
};
```

## 5. 诊断组件

```typescript
// src/components/DiagnosticPanel.tsx
import React, { useState } from 'react';
import { useXiaopurple } from '../contexts/XiaopurpleContext';

export const DiagnosticPanel: React.FC = () => {
  const { diagnosticEngine } = useXiaopurple();
  const [symptoms, setSymptoms] = useState('');
  const [diagnosing, setDiagnosing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleDiagnose = async () => {
    if (!symptoms.trim()) return;

    setDiagnosing(true);
    try {
      const diagnosisResult = await diagnosticEngine.diagnose([
        symptoms
      ]);
      setResult(diagnosisResult);
    } catch (error) {
      console.error('诊断失败:', error);
    } finally {
      setDiagnosing(false);
    }
  };

  const handleExecuteSolution = async (solutionId: string) => {
    if (!result) return;

    try {
      const executionResult = await diagnosticEngine.executeSolution(
        result.id,
        solutionId
      );
      console.log('执行结果:', executionResult);
    } catch (error) {
      console.error('执行解决方案失败:', error);
    }
  };

  return (
    <div className="diagnostic-panel">
      <h3>🔧 问题诊断</h3>

      <div className="diagnosis-form">
        <textarea
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
          placeholder="描述问题症状..."
          rows={3}
        />
        <button
          className="diagnose-btn"
          onClick={handleDiagnose}
          disabled={diagnosing || !symptoms.trim()}
        >
          {diagnosing ? '诊断中...' : '开始诊断'}
        </button>
      </div>

      {result && (
        <div className="diagnosis-result">
          <div className="result-header">
            <h4>{result.title}</h4>
            <span className={`severity ${result.severity}`}>
              {result.severity}
            </span>
          </div>
          <p className="description">{result.description}</p>

          {result.solutions.length > 0 && (
            <div className="solutions">
              <h5>解决方案</h5>
              {result.solutions.map((solution: any) => (
                <SolutionCard
                  key={solution.id}
                  solution={solution}
                  onExecute={() => handleExecuteSolution(solution.id)}
                />
              ))}
            </div>
          )}

          {result.requiresHuman && (
            <div className="human-support">
              <p>此问题需要人工支持</p>
              <button className="contact-btn">
                联系技术支持
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

interface SolutionCardProps {
  solution: any;
  onExecute: () => void;
}

const SolutionCard: React.FC<SolutionCardProps> = ({ solution, onExecute }) => {
  return (
    <div className="solution-card">
      <h5>{solution.title}</h5>
      <p>{solution.description}</p>
      <ol className="steps">
        {solution.steps.map((step: string, index: number) => (
          <li key={index}>{step}</li>
        ))}
      </ol>
      <div className="solution-actions">
        {solution.autoFix && (
          <button className="auto-fix-btn" onClick={onExecute}>
            🤖 自动修复
          </button>
        )}
        <span className="estimated-time">
          预计: {solution.estimatedTime}秒
        </span>
      </div>
    </div>
  );
};
```

## 6. 主应用组件

```typescript
// src/App.tsx
import React from 'react';
import { XiaopurpleProvider } from './contexts/XiaopurpleContext';
import { ChatWidget } from './components/ChatWidget';
import { RecommendationPanel } from './components/RecommendationPanel';
import { DiagnosticPanel } from './components/DiagnosticPanel';

const AppContent: React.FC = () => {
  const { loading, error, isConnected } = useXiaopurple();

  if (loading) {
    return (
      <div className="loading-screen">
        <h2>正在初始化小紫...</h2>
        <div className="spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-screen">
        <h2>❌ 初始化失败</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>
          重试
        </button>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>紫微元灵 - 用户端</h1>
        <div className="status-indicator">
          {isConnected ? '🟢 在线' : '🔴 离线'}
        </div>
      </header>

      <main className="app-main">
        <div className="main-content">
          <ChatWidget />
        </div>

        <aside className="sidebar">
          <RecommendationPanel />
          <DiagnosticPanel />
        </aside>
      </main>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <XiaopurpleProvider>
      <AppContent />
    </XiaopurpleProvider>
  );
};
```

## 7. 样式示例

```css
/* src/App.css */
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f5f5f5;
}

.app-header {
  background: #6b46c1;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.sidebar {
  width: 400px;
  background: white;
  border-left: 1px solid #e0e0e0;
  padding: 1.5rem;
  overflow-y: auto;
}

/* 聊天组件 */
.chat-widget {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.message-bubble {
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 12px;
  max-width: 70%;
}

.message-bubble.user {
  background: #6b46c1;
  color: white;
  margin-left: auto;
}

.message-bubble.assistant {
  background: #f0f0f0;
  margin-right: auto;
}

.chat-input {
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
}

.input-wrapper {
  display: flex;
  gap: 0.5rem;
}

.input-wrapper textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  resize: none;
  font-family: inherit;
}

.send-button {
  background: #6b46c1;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
}

.send-button:hover {
  background: #553c9a;
}

.send-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* 推荐面板 */
.recommendation-panel {
  margin-bottom: 2rem;
}

.recommendation-card {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.recommendation-card h4 {
  margin: 0 0 0.5rem 0;
  color: #856404;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.action-btn.apply {
  background: #28a745;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.dismiss-btn {
  background: transparent;
  border: 1px solid #dc3545;
  color: #dc3545;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

/* 诊断面板 */
.diagnostic-panel {
  margin-bottom: 2rem;
}

.diagnosis-form {
  margin-bottom: 1rem;
}

.diagnosis-form textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  resize: none;
}

.diagnose-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
}

.diagnose-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* 加载和错误状态 */
.loading-screen,
.error-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #6b46c1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

## 8. 入口文件

```typescript
// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './App.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

## 使用流程

1. 在应用根组件包裹 `XiaopurpleProvider`
2. 在需要使用小紫功能的组件中使用 `useXiaopurple` Hook
3. 通过 `sendMessage` 发送消息
4. 监听 `messages` 数组更新来显示收到的消息
5. 使用 `recommendationEngine` 获取和管理推荐
6. 使用 `diagnosticEngine` 进行问题诊断

## 注意事项

1. 确保适配层编译后的文件在正确的路径
2. WebSocket 端点需要根据实际部署配置
3. 语音录制和图片上传需要额外的浏览器 API 支持
4. 建议在生产环境中添加错误监控和日志

## 性能优化建议

1. 使用 React.memo 避免不必要的重渲染
2. 对长消息列表使用虚拟滚动
3. 对推荐和诊断结果使用缓存
4. 使用 useMemo 和 useCallback 优化计算
