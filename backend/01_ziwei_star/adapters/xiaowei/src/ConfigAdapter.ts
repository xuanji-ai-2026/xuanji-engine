/**
 * 小微适配层 - 配置协助接口适配器
 * 版本: v1.0.0
 * 描述: 实现与紫微元灵核心的配置消息通信，支持配置项查询、修改、验证
 */

import {
  XiaoweiConfig,
  MessageType,
  Message,
  BaseResponse,
  ConfigQueryParams,
  ConfigModifyParams,
  ConfigItem,
  ValidationResult,
  ConfigValidationError,
  BatchConfigOperation,
  WebSocketEvents
} from '../types';

export class ConfigAdapter {
  private config: XiaoweiConfig;
  private ws: WebSocket | null = null;
  private messageHandlers: Map<string, (response: BaseResponse) => void> = new Map();
  private events: WebSocketEvents = {};
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  constructor(config: XiaoweiConfig) {
    this.config = config;
  }

  /**
   * 连接到紫微元灵核心
   */
  async connect(events?: WebSocketEvents): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.events = events || {};
        
        this.ws = new WebSocket(this.config.coreWsUrl);

        this.ws.onopen = () => {
          this.log('Connected to Ziwei Core');
          this.reconnectAttempts = 0;
          this.events.onConnect?.({ connected: true });
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: Message = JSON.parse(event.data);
            this.log(`Received message: ${message.type}`);
            this.events.onMessage?.(message);
            this.handleMessage(message);
          } catch (error) {
            this.error('Failed to parse message', error);
          }
        };

        this.ws.onerror = (error) => {
          this.error('WebSocket error', error);
          this.events.onError?.(error as Error);
        };

        this.ws.onclose = () => {
          this.log('Disconnected from Ziwei Core');
          this.events.onDisconnect?.({ connected: false });
          this.reconnect();
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * 断开连接
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.messageHandlers.clear();
  }

  /**
   * 查询配置项
   */
  async queryConfig(params: ConfigQueryParams): Promise<BaseResponse<ConfigItem[]>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.CONFIG_QUERY,
      payload: params,
      timestamp: Date.now()
    };

    return this.sendMessage<BaseResponse<ConfigItem[]>>(message);
  }

  /**
   * 修改配置项
   */
  async modifyConfig(params: ConfigModifyParams): Promise<BaseResponse<{ success: boolean; updated: string[] }>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.CONFIG_MODIFY,
      payload: params,
      timestamp: Date.now()
    };

    return this.sendMessage<BaseResponse<{ success: boolean; updated: string[] }>>(message);
  }

  /**
   * 验证配置
   */
  async validateConfig(configs: Record<string, any>): Promise<BaseResponse<ValidationResult>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.CONFIG_VALIDATE,
      payload: { configs },
      timestamp: Date.now()
    };

    return this.sendMessage<BaseResponse<ValidationResult>>(message);
  }

  /**
   * 批量配置操作
   */
  async batchConfig(operations: BatchConfigOperation[]): Promise<BaseResponse<any>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.CONFIG_BATCH,
      payload: { operations },
      timestamp: Date.now()
    };

    return this.sendMessage<BaseResponse<any>>(message);
  }

  /**
   * 发送消息并等待响应
   */
  private async sendMessage<T>(message: Message): Promise<T> {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.messageHandlers.delete(message.id);
        reject(new Error(`Message timeout: ${message.id}`));
      }, this.config.timeout);

      this.messageHandlers.set(message.id, (response: BaseResponse) => {
        clearTimeout(timeout);
        
        if (response.status === 'success') {
          resolve(response as T);
        } else {
          reject(new Error(response.error || 'Unknown error'));
        }
      });

      try {
        this.ws?.send(JSON.stringify(message));
        this.log(`Sent message: ${message.type}`);
      } catch (error) {
        clearTimeout(timeout);
        this.messageHandlers.delete(message.id);
        reject(error);
      }
    });
  }

  /**
   * 处理接收到的消息
   */
  private handleMessage(message: Message): void {
    const handler = this.messageHandlers.get(message.id);
    if (handler) {
      handler(message.payload);
      this.messageHandlers.delete(message.id);
    }
  }

  /**
   * 重连逻辑
   */
  private reconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      this.error('Max reconnect attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

    this.log(`Reconnecting in ${delay}ms...`);
    setTimeout(() => {
      this.connect(this.events).catch((error) => {
        this.error('Reconnect failed', error);
      });
    }, delay);
  }

  /**
   * 生成消息 ID
   */
  private generateMessageId(): string {
    return `${this.config.adapterId}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 日志输出
   */
  private log(message: string, ...args: any[]): void {
    if (this.config.logLevel === 'debug') {
      console.log(`[Xiaowei ConfigAdapter] ${message}`, ...args);
    }
  }

  /**
   * 错误日志
   */
  private error(message: string, ...args: any[]): void {
    console.error(`[Xiaowei ConfigAdapter ERROR] ${message}`, ...args);
  }
}

export default ConfigAdapter;
