/**
 * 小元 - 开发者端智能助手适配层
 * 核心适配器类
 */

import { EventEmitter } from 'events';
import {
  XiaoyuanConfig,
  Message,
  Session,
  SessionContext,
  ServiceType,
  TextMessage,
  CodeMessage,
  MessageType,
  MessageRole,
  ConnectionStatus,
  ApiResponse,
  AdapterEvent,
} from './types';
import { createConfig } from './config';
import { ApiManagementService } from './services/api-management.service';
import { PluginDevelopmentService } from './services/plugin-development.service';
import { SdkManagementService } from './services/sdk-management.service';
import { CodeReviewService } from './services/code-review.service';

/**
 * 小元适配器主类
 */
export class XiaoyuanAdapter extends EventEmitter {
  private config: XiaoyuanConfig;
  private sessions: Map<string, Session> = new Map();
  private logger: any;
  private status: ConnectionStatus = ConnectionStatus.DISCONNECTED;

  // 服务实例
  private apiManagementService?: ApiManagementService;
  private pluginDevelopmentService?: PluginDevelopmentService;
  private sdkManagementService?: SdkManagementService;
  private codeReviewService?: CodeReviewService;

  // WebSocket 连接
  private ws?: WebSocket;
  private reconnectTimer?: NodeJS.Timeout;
  private heartbeatTimer?: NodeJS.Timeout;

  constructor(config?: Partial<XiaoyuanConfig>) {
    super();
    this.config = createConfig(config);
    this.initializeLogger();
    this.initializeServices();
    this.logger.info('Xiaoyuan adapter initialized');
  }

  /**
   * 初始化日志系统
   */
  private initializeLogger(): void {
    const levels = ['debug', 'info', 'warn', 'error'];
    this.logger = {
      level: this.config.logging.level,
      debug: (...args: any[]) => {
        if (this.shouldLog('debug')) console.debug('[Xiaoyuan]', ...args);
      },
      info: (...args: any[]) => {
        if (this.shouldLog('info')) console.info('[Xiaoyuan]', ...args);
      },
      warn: (...args: any[]) => {
        if (this.shouldLog('warn')) console.warn('[Xiaoyuan]', ...args);
      },
      error: (...args: any[]) => {
        if (this.shouldLog('error')) console.error('[Xiaoyuan]', ...args);
      },
    };
  }

  /**
   * 检查是否应该记录日志
   */
  private shouldLog(level: string): boolean {
    if (!this.config.logging.enableConsole) return false;
    const levels = ['debug', 'info', 'warn', 'error'];
    return levels.indexOf(level) >= levels.indexOf(this.config.logging.level);
  }

  /**
   * 初始化服务
   */
  private initializeServices(): void {
    if (this.config.services.apiManagement.enabled) {
      this.apiManagementService = new ApiManagementService(this.config, this.logger);
      this.logger.info('API Management service initialized');
    }

    if (this.config.services.pluginDevelopment.enabled) {
      this.pluginDevelopmentService = new PluginDevelopmentService(this.config, this.logger);
      this.logger.info('Plugin Development service initialized');
    }

    if (this.config.services.sdkManagement.enabled) {
      this.sdkManagementService = new SdkManagementService(this.config, this.logger);
      if (this.config.services.sdkManagement.autoNotify) {
        this.sdkManagementService.startUpdateCheck();
      }
      this.logger.info('SDK Management service initialized');
    }

    if (this.config.services.codeReview.enabled) {
      this.codeReviewService = new CodeReviewService(this.config, this.logger);
      this.logger.info('Code Review service initialized');
    }
  }

  /**
   * 连接到核心服务
   */
  async connect(): Promise<void> {
    this.logger.info('Connecting to Xuanji core service...');

    try {
      // 建立 WebSocket 连接
      this.ws = new WebSocket(this.config.wsEndpoint);

      this.ws.onopen = () => {
        this.status = ConnectionStatus.CONNECTED;
        this.logger.info('Connected to Xuanji core service');
        this.startHeartbeat();
        this.emit('connected', { status: this.status });
      };

      this.ws.onmessage = (event) => {
        this.handleCoreMessage(event.data);
      };

      this.ws.onerror = (error) => {
        this.logger.error('WebSocket error:', error);
        this.status = ConnectionStatus.ERROR;
        this.emit('error', error);
      };

      this.ws.onclose = () => {
        this.status = ConnectionStatus.DISCONNECTED;
        this.logger.warn('Disconnected from Xuanji core service');
        this.stopHeartbeat();
        this.emit('disconnected');
        this.scheduleReconnect();
      };

    } catch (error) {
      this.logger.error('Connection failed:', error);
      this.status = ConnectionStatus.ERROR;
      throw error;
    }
  }

  /**
   * 断开连接
   */
  async disconnect(): Promise<void> {
    this.logger.info('Disconnecting from Xuanji core service...');

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = undefined;
    }

    this.stopHeartbeat();

    if (this.ws) {
      this.ws.close();
      this.ws = undefined;
    }

    if (this.sdkManagementService) {
      this.sdkManagementService.stopUpdateCheck();
    }

    this.status = ConnectionStatus.DISCONNECTED;
    this.logger.info('Disconnected');
  }

  /**
   * 重新连接调度
   */
  private scheduleReconnect(): void {
    if (this.reconnectTimer) return;

    this.reconnectTimer = setTimeout(async () => {
      this.reconnectTimer = undefined;
      try {
        await this.connect();
      } catch (error) {
        this.logger.error('Reconnect failed:', error);
      }
    }, 5000); // 5秒后重连
  }

  /**
   * 启动心跳
   */
  private startHeartbeat(): void {
    this.stopHeartbeat();
    this.heartbeatTimer = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'heartbeat' }));
      }
    }, 30000); // 30秒心跳
  }

  /**
   * 停止心跳
   */
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = undefined;
    }
  }

  /**
   * 处理核心消息
   */
  private handleCoreMessage(data: string): void {
    try {
      const message = JSON.parse(data);
      this.logger.debug('Received message from core:', message.type);

      // 根据消息类型处理
      switch (message.type) {
        case 'message':
          this.handleCoreResponse(message.payload);
          break;
        case 'notification':
          this.handleNotification(message.payload);
          break;
        default:
          this.emit('message', message);
      }
    } catch (error) {
      this.logger.error('Failed to handle core message:', error);
    }
  }

  /**
   * 处理核心响应
   */
  private handleCoreResponse(payload: any): void {
    this.emit('response', payload);
  }

  /**
   * 处理通知
   */
  private handleNotification(payload: any): void {
    this.logger.debug('Notification:', payload);
    this.emit('notification', payload);
  }

  /**
   * 发送消息到核心
   */
  private sendToCore(type: string, payload: any): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error('Not connected to core service');
    }

    const message = {
      type,
      payload,
      timestamp: Date.now(),
    };

    this.ws.send(JSON.stringify(message));
  }

  /**
   * 创建会话
   */
  async createSession(userId: string): Promise<Session> {
    const session: Session = {
      id: this.generateId(),
      userId,
      messages: [],
      context: {},
      state: {
        status: ConnectionStatus.CONNECTED,
        lastActivity: Date.now(),
      },
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };

    this.sessions.set(session.id, session);
    this.logger.info(`Session created: ${session.id}`);

    return session;
  }

  /**
   * 获取会话
   */
  getSession(sessionId: string): Session | undefined {
    return this.sessions.get(sessionId);
  }

  /**
   * 处理用户消息
   */
  async handleMessage(sessionId: string, message: TextMessage | CodeMessage): Promise<Message> {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error(`Session not found: ${sessionId}`);
    }

    // 添加用户消息到会话
    session.messages.push(message);
    session.state.lastActivity = Date.now();
    session.updatedAt = Date.now();

    // 处理消息
    let response: Message;

    try {
      // 根据服务类型路由到相应的服务
      if (message.serviceType) {
        response = await this.routeToService(message.serviceType, message, session);
      } else {
        // 如果没有指定服务类型，自动识别
        const serviceType = this.detectServiceType(message.content);
        response = await this.routeToService(serviceType, message, session);
      }

      // 添加响应到会话
      session.messages.push(response);
      session.updatedAt = Date.now();

      return response;

    } catch (error: any) {
      this.logger.error('Failed to handle message:', error);

      const errorMessage: Message = {
        id: this.generateId(),
        type: MessageType.ERROR,
        role: MessageRole.ASSISTANT,
        timestamp: Date.now(),
        content: error.message || '处理消息时发生错误',
      };

      session.messages.push(errorMessage);
      return errorMessage;
    }
  }

  /**
   * 自动检测服务类型
   */
  private detectServiceType(content: string): ServiceType {
    const lowerContent = content.toLowerCase();

    // API 管理相关关键词
    if (/api|endpoint|接口|rest|http/i.test(lowerContent)) {
      return ServiceType.API_MANAGEMENT;
    }

    // 插件开发相关关键词
    if (/plugin|插件|模板|template|开发/i.test(lowerContent)) {
      return ServiceType.PLUGIN_DEVELOPMENT;
    }

    // SDK 管理相关关键词
    if (/sdk|version|update|版本|更新/i.test(lowerContent)) {
      return ServiceType.SDK_MANAGEMENT;
    }

    // 代码审查相关关键词
    if (/review|审查|检查|bug|漏洞|vulnerability|安全/i.test(lowerContent)) {
      return ServiceType.CODE_REVIEW;
    }

    // 默认返回 API 管理服务
    return ServiceType.API_MANAGEMENT;
  }

  /**
   * 路由到指定服务
   */
  private async routeToService(
    serviceType: ServiceType,
    message: TextMessage | CodeMessage,
    session: Session
  ): Promise<Message) {
    switch (serviceType) {
      case ServiceType.API_MANAGEMENT:
        return this.handleApiManagement(message, session);

      case ServiceType.PLUGIN_DEVELOPMENT:
        return this.handlePluginDevelopment(message, session);

      case ServiceType.SDK_MANAGEMENT:
        return this.handleSdkManagement(message, session);

      case ServiceType.CODE_REVIEW:
        return this.handleCodeReview(message, session);

      default:
        throw new Error(`Unknown service type: ${serviceType}`);
    }
  }

  /**
   * 处理 API 管理服务
   */
  private async handleApiManagement(message: TextMessage | CodeMessage, session: Session): Promise<Message> {
    if (!this.apiManagementService) {
      throw new Error('API Management service is not enabled');
    }

    const content = message.content.toLowerCase();

    // 获取所有 API 端点
    if (content.includes('list') || content.includes('获取') && content.includes('api')) {
      const endpoints = await this.apiManagementService.getAllEndpoints();
      return this.createTextMessage(`找到 ${endpoints.length} 个 API 端点`);
    }

    // 生成 API 文档
    if (content.includes('document') || content.includes('文档')) {
      const doc = await this.apiManagementService.generateDocumentation('markdown');
      return this.createCodeMessage('API 文档', 'markdown', doc);
    }

    // 默认响应
    return this.createTextMessage(
      '我可以帮您管理 API 端点、生成文档和执行测试。您可以问我：\n' +
      '- 列出所有 API 端点\n' +
      '- 生成 API 文档\n' +
      '- 测试 API 端点\n' +
      '- 创建新的 API 端点'
    );
  }

  /**
   * 处理插件开发服务
   */
  private async handlePluginDevelopment(message: TextMessage | CodeMessage, session: Session): Promise<Message> {
    if (!this.pluginDevelopmentService) {
      throw new Error('Plugin Development service is not enabled');
    }

    const content = message.content.toLowerCase();

    // 列出插件模板
    if (content.includes('template') || content.includes('模板')) {
      const templates = await this.pluginDevelopmentService.getAllTemplates();
      const templateNames = templates.map(t => `- ${t.name}: ${t.description}`).join('\n');
      return this.createTextMessage(`可用插件模板：\n${templateNames}`);
    }

    // 默认响应
    return this.createTextMessage(
      '我可以帮您开发插件。您可以问我：\n' +
      '- 列出可用的插件模板\n' +
      '- 创建新的插件项目\n' +
      '- 生成插件 API 对接指南\n' +
      '- 生成插件测试用例'
    );
  }

  /**
   * 处理 SDK 管理服务
   */
  private async handleSdkManagement(message: TextMessage | CodeMessage, session: Session): Promise<Message> {
    if (!this.sdkManagementService) {
      throw new Error('SDK Management service is not enabled');
    }

    const content = message.content.toLowerCase();

    // 列出所有 SDK
    if (content.includes('list') || content.includes('list') && content.includes('sdk')) {
      const sdks = await this.sdkManagementService.getAllSdks();
      const sdkList = sdks.map(s => `- ${s.name}: 当前版本 ${s.currentVersion}，最新版本 ${s.latestVersion}`).join('\n');
      return this.createTextMessage(`可用的 SDK：\n${sdkList}`);
    }

    // 检查更新
    if (content.includes('update') || content.includes('更新')) {
      const updates: string[] = [];
      for (const [name] of Object.entries({ javascript: '', python: '', typescript: '' })) {
        const update = await this.sdkManagementService.checkUpdates(name);
        if (update) {
          updates.push(`${name}: ${update.fromVersion} → ${update.toVersion}`);
        }
      }

      if (updates.length > 0) {
        return this.createTextMessage(`可用更新：\n${updates.join('\n')}`);
      } else {
        return this.createTextMessage('所有 SDK 都是最新版本');
      }
    }

    // 默认响应
    return this.createTextMessage(
      '我可以帮您管理 SDK。您可以问我：\n' +
      '- 列出所有 SDK\n' +
      '- 检查 SDK 更新\n' +
      '- 获取 SDK 集成指南\n' +
      '- 查看 SDK 版本历史'
    );
  }

  /**
   * 处理代码审查服务
   */
  private async handleCodeReview(message: TextMessage | CodeMessage, session: Session): Promise<Message> {
    if (!this.codeReviewService) {
      throw new Error('Code Review service is not enabled');
    }

    const content = message.content.toLowerCase();

    // 如果消息包含代码，执行审查
    if (message.type === MessageType.CODE) {
      const result = await this.codeReviewService.reviewCode({
        code: message.codeBlock || message.content,
        language: message.language,
        filePath: session.context.codeReviewContext?.code && 'in-memory',
      });

      return this.createTextMessage(
        `代码审查结果：\n` +
        `总体评分: ${result.overallScore}/100\n` +
        `发现 ${result.issues.length} 个问题\n` +
        `${result.summary}\n\n` +
        `建议：\n${result.suggestions.map(s => `- ${s.title}: ${s.description}`).join('\n')}`
      );
    }

    // 扫描安全漏洞
    if (content.includes('security') || content.includes('安全')) {
      if (session.context.codeReviewContext?.code) {
        const vulnerabilities = await this.codeReviewService.scanSecurityVulnerabilities(
          session.context.codeReviewContext.code,
          session.context.codeReviewContext.language
        );

        if (vulnerabilities.length > 0) {
          return this.createTextMessage(
            `发现 ${vulnerabilities.length} 个安全漏洞：\n` +
            vulnerabilities.map(v => `- [${v.severity}] ${v.title}: ${v.description}`).join('\n')
          );
        } else {
          return this.createTextMessage('未发现明显的安全漏洞');
        }
      }
    }

    // 默认响应
    return this.createTextMessage(
      '我可以帮您进行代码审查。您可以：\n' +
      '- 提交代码进行审查\n' +
      '- 扫描安全漏洞\n' +
      '- 获取代码质量建议\n' +
      '- 查看所有审查规则'
    );
  }

  /**
   * 创建文本消息
   */
  private createTextMessage(content: string, serviceType?: ServiceType): TextMessage {
    return {
      id: this.generateId(),
      type: MessageType.TEXT,
      role: MessageRole.ASSISTANT,
      content,
      timestamp: Date.now(),
      serviceType,
    };
  }

  /**
   * 创建代码消息
   */
  private createCodeMessage(title: string, language: string, codeBlock: string): CodeMessage {
    return {
      id: this.generateId(),
      type: MessageType.CODE,
      role: MessageRole.ASSISTANT,
      content: title,
      language,
      codeBlock,
      timestamp: Date.now(),
    };
  }

  /**
   * 生成唯一 ID
   */
  private generateId(): string {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 获取 API 管理服务
   */
  getApiManagementService(): ApiManagementService | undefined {
    return this.apiManagementService;
  }

  /**
   * 获取插件开发服务
   */
  getPluginDevelopmentService(): PluginDevelopmentService | undefined {
    return this.pluginDevelopmentService;
  }

  /**
   * 获取 SDK 管理服务
   */
  getSdkManagementService(): SdkManagementService | undefined {
    return this.sdkManagementService;
  }

  /**
   * 获取代码审查服务
   */
  getCodeReviewService(): CodeReviewService | undefined {
    return this.codeReviewService;
  }

  /**
   * 获取连接状态
   */
  getStatus(): ConnectionStatus {
    return this.status;
  }

  /**
   * 获取配置
   */
  getConfig(): XiaoyuanConfig {
    return { ...this.config };
  }

  /**
   * 更新配置
   */
  async updateConfig(updates: Partial<XiaoyuanConfig>): Promise<void> {
    this.config = { ...this.config, ...updates };
    this.logger.info('Configuration updated');
  }

  /**
   * 健康检查
   */
  async healthCheck(): Promise<boolean> {
    try {
      // 检查 WebSocket 连接
      if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
        return false;
      }

      // 检查服务状态
      if (this.apiManagementService && !this.apiManagementService) {
        return false;
      }

      return true;
    } catch (error) {
      this.logger.error('Health check failed:', error);
      return false;
    }
  }
}

/**
 * 导出
 */
export default XiaoyuanAdapter;
