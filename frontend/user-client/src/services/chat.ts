import apiService from './api';
import type {
  Chat,
  ChatMessage,
  SendMessageRequest,
  ChatStreamResponse,
  PaginationRequest,
  PaginationResponse,
} from '@/types';

class ChatService {
  // 对话管理

  // 获取对话列表
  async getChatList(
    params: PaginationRequest
  ): Promise<PaginationResponse<Chat>> {
    const response = await apiService.get<PaginationResponse<Chat>>(
      '/chats',
      { params }
    );
    return response.data as PaginationResponse<Chat>;
  }

  // 获取单个对话
  async getChat(id: string): Promise<Chat> {
    const response = await apiService.get<Chat>(`/chats/${id}`);
    return response.data as Chat;
  }

  // 创建对话
  async createChat(digitalHumanId: string, title?: string): Promise<Chat> {
    const response = await apiService.post<Chat>('/chats', {
      digitalHumanId,
      title,
    });
    return response.data as Chat;
  }

  // 更新对话标题
  async updateChatTitle(id: string, title: string): Promise<Chat> {
    const response = await apiService.patch<Chat>(`/chats/${id}`, { title });
    return response.data as Chat;
  }

  // 删除对话
  async deleteChat(id: string): Promise<void> {
    await apiService.delete(`/chats/${id}`);
  }

  // 归档对话
  async archiveChat(id: string): Promise<void> {
    await apiService.post(`/chats/${id}/archive`);
  }

  // 消息管理

  // 获取消息列表
  async getMessages(
    chatId: string,
    params?: PaginationRequest
  ): Promise<PaginationResponse<ChatMessage>> {
    const response = await apiService.get<PaginationResponse<ChatMessage>>(
      `/chats/${chatId}/messages`,
      { params }
    );
    return response.data as PaginationResponse<ChatMessage>;
  }

  // 发送消息
  async sendMessage(
    chatId: string,
    data: SendMessageRequest
  ): Promise<ChatMessage> {
    const response = await apiService.post<ChatMessage>(
      `/chats/${chatId}/messages`,
      data
    );
    return response.data as ChatMessage;
  }

  // 发送流式消息
  async sendMessageStream(
    chatId: string,
    data: SendMessageRequest,
    onChunk: (chunk: ChatStreamResponse) => void,
    onComplete: () => void,
    onError: (error: Error) => void
  ): Promise<void> {
    const token = localStorage.getItem('xuanji_token');
    const response = await fetch(`/api/chats/${chatId}/messages/stream`, {
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

    if (!reader) {
      throw new Error('Response body is null');
    }

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          onComplete();
          break;
        }

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              onChunk(data);
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

  // 删除消息
  async deleteMessage(chatId: string, messageId: string): Promise<void> {
    await apiService.delete(`/chats/${chatId}/messages/${messageId}`);
  }

  // 语音输入
  async uploadAudioFile(file: File): Promise<{ text: string }> {
    const response = await apiService.upload<{ text: string }>(
      '/chats/upload-audio',
      file
    );
    return response.data as { text: string };
  }

  // 文字转语音
  async textToSpeech(text: string, voiceId: string): Promise<{ audioUrl: string }> {
    const response = await apiService.post<{ audioUrl: string }>('/chats/tts', {
      text,
      voiceId,
    });
    return response.data as { audioUrl: string };
  }
}

export const chatService = new ChatService();
export default chatService;
