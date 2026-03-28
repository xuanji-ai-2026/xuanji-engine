/**
 * 小紫 - 用户端智能助手适配层
 * 核心适配器类
 */

import {
  Message,
  MessageType,
  Conversation,
  XiaopurpleConfig,
  ConnectionState,
  AdapterEvent,
  EventHandler,
  WSMessage,
  ApiResponse
} from '../types';

export class XiaopurpleAdapter {
  private config: XiaopurpleConfig;
  private connectionState: ConnectionState = ConnectionState.DISCONNECTED;
  private ws: WebSocket | null = null;
  private currentConversation: Conversation | null = null;
  private eventHandlers: Map<string, Set<EventHandler>> = new Map();
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;

  constructor(config: XiaopurpleConfig) {
    this.config = config;
    this.initializeConversation();
  }

  // ==================== 生命周期管理 ====================

  /**
   * 启动适配器
   */
  async start(): Promise<void> {
    this.log('info', '启动小紫适配器...');

    try {
      await this.connectWebSocket();
      this.connectionState = ConnectionState.CONNECTED;
      this.emit('adapter:started', { timestamp: Date.now() });
      this.log('info', '✅ 小紫适配器启动成功');
    } catch (error) {
      this.connectionState = ConnectionState.ERROR;
      this.log('error', `启动失败: ${error}`);
      throw error;
    }
  }

  /**
   * 停止适配器
   */
  async stop(): Promise<void> {
    this.log('info', '停止小紫适配器...');

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.connectionState = ConnectionState.DISCONNECTED;
    this.emit('adapter:stopped', { timestamp: Date.now() });
    this.log('info', '✅ 小紫适配器已停止');
  }

  /**
   * 重启适配器
   */
  async restart(): Promise<void> {
    await this.stop();
    await this.start();
  }

  // ==================== WebSocket 连接管理 ====================

  /**
   * 连接 WebSocket
   */
  private async connectWebSocket(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.connectionState = ConnectionState.CONNECTING;
        this.log('info', `连接 WebSocket: ${this.config.wsEndpoint}`);

        const ws = new WebSocket(this.config.wsEndpoint);

        ws.onopen = () => {
          this.log('info', '✅ WebSocket 连接成功');
          this.connectionState = ConnectionState.CONNECTED;
          this.reconnectAttempts = 0;
          this.emit('ws:connected', {});
          this.startHeartbeat();
          resolve();
        };

        ws.onmessage = (event) => {
          this.handleWSMessage(event.data);
        };

        ws.onerror = (error) => {
          this.log('error', 'WebSocket 错误', error);
          this.connectionState = ConnectionState.ERROR;
          this.emit('ws:error', { error });
          reject(error);
        };

        ws.onclose = () => {
          this.log('warn', 'WebSocket 连接关闭');
          this.connectionState = ConnectionState.DISCONNECTED;
          this.emit('ws:disconnected', {});

          // 自动重连
          if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
            this.log('info', `${delay}ms 后尝试重连 (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            setTimeout(() => this.connectWebSocket(), delay);
          }
        };

        this.ws = ws;
      } catch (error) {
        this.log('error', 'WebSocket 连接失败', error);
        reject(error);
      }
    });
  }

  /**
   * 发送 WebSocket 消息
   */
  private sendWSMessage(message: WSMessage): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket 未连接');
    }

    const payload = JSON.stringify(message);
    this.ws.send(payload);
    this.log('debug', '发送 WS 消息', message);
  }

  /**
   * 处理 WebSocket 消息
   */
  private handleWSMessage(data: string): void {
    try {
      const message: WSMessage = JSON.parse(data);
      this.log('debug', '收到 WS 消息', message);

      switch (message.type) {
        case 'message':
          this.handleIncomingMessage(message.payload);
          break;
        case 'heartbeat':
          this.emit('heartbeat:received', {});
          break;
        case 'close':
          this.emit('ws:close_requested', {});
          break;
        case 'error':
          this.emit('ws:error_received', message.payload);
          break;
      }
    } catch (error) {
      this.log('error', '处理 WS 消息失败', error);
    }
  }

  /**
   * 启动心跳
   */
  private startHeartbeat(): void {
    const interval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.sendWSMessage({
          type: 'heartbeat',
          payload: { timestamp: Date.now() }
        });
      } else {
        clearInterval(interval);
      }
    }, 30000);  // 每 30 秒发送一次心跳
  }

  // ==================== 消息处理 ====================

  /**
   * 发送消息到核心
   */
  async sendMessage(message: Message): Promise<void> {
    if (!this.currentConversation) {
      throw new Error('未初始化对话会话');
    }

    // 添加消息到历史
    this.currentConversation.messages.push(message);
    this.currentConversation.updatedAt = Date.now();

    this.log('info', `发送消息: ${message.type}`, { role: message.role });

    // 发送到核心
    this.sendWSMessage({
      type: 'message',
      payload: {
        conversationId: this.currentConversation.id,
        message: message
      }
    });

    this.emit('message:sent', { message });
  }

  /**
   * 处理来自核心的消息
   */
  private handleIncomingMessage(payload: any): void {
    const message: Message = payload.message;

    if (this.currentConversation) {
      this.currentConversation.messages.push(message);
      this.currentConversation.updatedAt = Date.now();
    }

    this.emit('message:received', { message });
  }

  /**
   * 获取对话历史
   */
  getConversationHistory(): Message[] {
    return this.currentConversation?.messages || [];
  }

  /**
   * 清空对话历史
   */
  clearHistory(): void {
    if (this.currentConversation) {
      this.currentConversation.messages = [];
      this.currentConversation.updatedAt = Date.now();
      this.log('info', '对话历史已清空');
      this.emit('history:cleared', {});
    }
  }

  // ==================== 事件系统 ====================

  /**
   * 监听事件
   */
  on(eventType: string, handler: EventHandler): void {
    if (!this.eventHandlers.has(eventType)) {
      this.eventHandlers.set(eventType, new Set());
    }
    this.eventHandlers.get(eventType)!.add(handler);
  }

  /**
   * 取消监听事件
   */
  off(eventType: string, handler: EventHandler): void {
    const handlers = this.eventHandlers.get(eventType);
    if (handlers) {
      handlers.delete(handler);
    }
  }

  /**
   * 触发事件
   */
  private emit(eventType: string, data: any): void {
    const handlers = this.eventHandlers.get(eventType);
    if (handlers) {
      const event: AdapterEvent = {
        type: eventType,
        data,
        timestamp: Date.now()
      };
      handlers.forEach(handler => handler(event));
    }
  }

  // ==================== 状态管理 ====================

  /**
   * 获取连接状态
   */
  getConnectionState(): ConnectionState {
    return this.connectionState;
  }

  /**
   * 获取当前对话会话
   */
  getCurrentConversation(): Conversation | null {
    return this.currentConversation;
  }

  /**
   * 更新对话状态
   */
  updateConversationState(state: Record<string, any>): void {
    if (this.currentConversation) {
      this.currentConversation.state = {
        ...this.currentConversation.state,
        ...state
      };
      this.emit('conversation:state_updated', { state });
    }
  }

  // ==================== 私有方法 ====================

  /**
   * 初始化对话会话
   */
  private initializeConversation(): void {
    this.currentConversation = {
      id: this.generateId(),
      userId: 'unknown',
      sessionId: this.generateId(),
      messages: [],
      state: {},
      createdAt: Date.now(),
      updatedAt: Date.now()
    };
  }

  /**
   * 生成唯一 ID
   */
  private generateId(): string {
    return `xp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 日志输出
   */
  private log(level: string, message: string, ...args: any[]): void {
    if (!this.config.logging.enableConsole) return;

    const levels = ['debug', 'info', 'warn', 'error'];
    const configLevelIndex = levels.indexOf(this.config.logging.level);
    const currentLevelIndex = levels.indexOf(level);

    if (currentLevelIndex >= configLevelIndex) {
      const prefix = `[小紫][${level.toUpperCase()}]`;
      console[level === 'error' ? 'error' : level === 'warn' ? 'warn' : 'log'](prefix, message, ...args);
    }
  }

  // ==================== 健康检查 ====================

  /**
   * 健康检查
   */
  healthCheck(): { healthy: boolean; details: Record<string, any> } {
    return {
      healthy: this.connectionState === ConnectionState.CONNECTED,
      details: {
        connectionState: this.connectionState,
        wsConnected: this.ws?.readyState === WebSocket.OPEN,
        conversationId: this.currentConversation?.id,
        messageCount: this.currentConversation?.messages.length || 0,
        uptime: Date.now() - (this.currentConversation?.createdAt || Date.now())
      }
    };
  }
}
