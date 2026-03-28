import apiService from './api';
import type {
  SmartConfigSession,
  ConfigMessage,
  SmartConfigRequest,
  SmartConfigResponse,
  ConfigHistory,
  ConfigTemplate,
  PaginationRequest,
  PaginationResponse,
} from '@/types';

class SmartConfigService {
  // 智能配置会话管理

  // 创建配置会话
  async createSession(configType: string): Promise<SmartConfigSession> {
    const response = await apiService.post<SmartConfigSession>('/smart-config/sessions', {
      configType,
    });
    return response.data as SmartConfigSession;
  }

  // 获取会话详情
  async getSession(id: string): Promise<SmartConfigSession> {
    const response = await apiService.get<SmartConfigSession>(`/smart-config/sessions/${id}`);
    return response.data as SmartConfigSession;
  }

  // 发送消息
  async sendMessage(data: SmartConfigRequest): Promise<SmartConfigResponse> {
    const response = await apiService.post<SmartConfigResponse>('/smart-config/chat', data);
    return response.data as SmartConfigResponse;
  }

  // 流式对话
  async sendMessageStream(
    data: SmartConfigRequest,
    onChunk: (chunk: string) => void,
    onComplete: (response: SmartConfigResponse) => void,
    onError: (error: Error) => void
  ): Promise<void> {
    const token = localStorage.getItem('xuanji_token');
    const response = await fetch('/api/smart-config/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let fullContent = '';

    if (!reader) {
      throw new Error('Response body is null');
    }

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          onComplete({
            message: fullContent,
            action: 'continue',
          });
          break;
        }

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.content) {
                fullContent += data.content;
                onChunk(data.content);
              }
            } catch {
              // Ignore invalid JSON
            }
          }
        }
      }
    } catch (error) {
      onError(error as Error);
    }
  }

  // 获取会话消息历史
  async getSessionMessages(
    sessionId: string,
    params?: PaginationRequest
  ): Promise<PaginationResponse<ConfigMessage>> {
    const response = await apiService.get<PaginationResponse<ConfigMessage>>(
      `/smart-config/sessions/${sessionId}/messages`,
      { params }
    );
    return response.data as PaginationResponse<ConfigMessage>;
  }

  // 应用配置
  async applyConfig(sessionId: string): Promise<void> {
    await apiService.post(`/smart-config/sessions/${sessionId}/apply`);
  }

  // 取消会话
  async cancelSession(sessionId: string): Promise<void> {
    await apiService.delete(`/smart-config/sessions/${sessionId}`);
  }

  // 配置历史

  // 获取配置历史
  async getConfigHistory(params?: PaginationRequest): Promise<PaginationResponse<ConfigHistory>> {
    const response = await apiService.get<PaginationResponse<ConfigHistory>>(
      '/smart-config/history',
      { params }
    );
    return response.data as PaginationResponse<ConfigHistory>;
  }

  // 获取单个配置历史
  async getConfigHistoryItem(id: string): Promise<ConfigHistory> {
    const response = await apiService.get<ConfigHistory>(`/smart-config/history/${id}`);
    return response.data as ConfigHistory;
  }

  // 恢复配置
  async restoreConfig(historyId: string): Promise<void> {
    await apiService.post(`/smart-config/history/${historyId}/restore`);
  }

  // 配置模板

  // 获取模板列表
  async getTemplates(params?: PaginationRequest): Promise<PaginationResponse<ConfigTemplate>> {
    const response = await apiService.get<PaginationResponse<ConfigTemplate>>(
      '/smart-config/templates',
      { params }
    );
    return response.data as PaginationResponse<ConfigTemplate>;
  }

  // 获取单个模板
  async getTemplate(id: string): Promise<ConfigTemplate> {
    const response = await apiService.get<ConfigTemplate>(`/smart-config/templates/${id}`);
    return response.data as ConfigTemplate;
  }

  // 使用模板
  async useTemplate(templateId: string, sessionId: string): Promise<void> {
    await apiService.post(`/smart-config/templates/${templateId}/use`, {
      sessionId,
    });
  }

  // 获取建议
  async getSuggestions(context: string): Promise<string[]> {
    const response = await apiService.post<string[]>('/smart-config/suggestions', {
      context,
    });
    return response.data as string[];
  }
}

export const smartConfigService = new SmartConfigService();
export default smartConfigService;
