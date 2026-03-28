import { create } from 'zustand';
import type { Chat, ChatMessage, ChatStreamResponse } from '@/types';
import chatService from '@/services/chat';

interface ChatState {
  chats: Chat[];
  currentChat: Chat | null;
  messages: ChatMessage[];
  isLoading: boolean;
  isLoadingMessages: boolean;
  isSending: boolean;
  error: string | null;

  fetchChats: () => Promise<void>;
  fetchMessages: (chatId: string) => Promise<void>;
  createChat: (digitalHumanId: string, title?: string) => Promise<void>;
  selectChat: (chat: Chat | null) => void;
  sendMessage: (content: string, attachments?: any[]) => Promise<void>;
  sendStreamMessage: (
    content: string,
    onChunk: (chunk: string) => void,
    onComplete: () => void,
    onError: (error: Error) => void
  ) => Promise<void>;
  deleteChat: (chatId: string) => Promise<void>;
  updateChatTitle: (chatId: string, title: string) => Promise<void>;
  clearMessages: () => void;
  clearError: () => void;
}

export const useChatStore = create<ChatState>((set, _get) => ({
  chats: [],
  currentChat: null,
  messages: [],
  isLoading: false,
  isLoadingMessages: false,
  isSending: false,
  error: null,

  fetchChats: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await chatService.getChatList({
        page: 1,
        pageSize: 50,
      });
      set({
        chats: response.items,
        isLoading: false,
      });
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : '获取对话列表失败',
      });
      throw error;
    }
  },

  fetchMessages: async (chatId) => {
    set({ isLoadingMessages: true, error: null });
    try {
      const response = await chatService.getMessages(chatId);
      set({
        messages: response.items,
        isLoadingMessages: false,
      });
    } catch (error) {
      set({
        isLoadingMessages: false,
        error: error instanceof Error ? error.message : '获取消息失败',
      });
      throw error;
    }
  },

  createChat: async (digitalHumanId, title) => {
    set({ isLoading: true, error: null });
    try {
      const newChat = await chatService.createChat(digitalHumanId, title);
      set((state) => ({
        chats: [newChat, ...state.chats],
        currentChat: newChat,
        messages: [],
        isLoading: false,
      }));
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : '创建对话失败',
      });
      throw error;
    }
  },

  selectChat: (chat) => {
    set({ currentChat: chat, messages: [] });
  },

  sendMessage: async (content, attachments) => {
    const { currentChat } = _get();
    if (!currentChat) return;

    set({ isSending: true, error: null });

    // Add user message immediately
    const userMessage: ChatMessage = {
      id: `temp-${Date.now()}`,
      chatId: currentChat.id,
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
      attachments,
    };

    set((state) => ({
      messages: [...state.messages, userMessage],
    }));

    try {
      const assistantMessage = await chatService.sendMessage(
        currentChat.id,
        { content, attachments, stream: false }
      );
      set((state) => ({
        messages: [...state.messages, assistantMessage],
        isSending: false,
      }));
    } catch (error) {
      set({
        isSending: false,
        error: error instanceof Error ? error.message : '发送消息失败',
      });
      throw error;
    }
  },

  sendStreamMessage: async (content, onChunk, onComplete, onError) => {
    const { currentChat } = _get();
    if (!currentChat) return;

    set({ isSending: true, error: null });

    // Add user message immediately
    const userMessage: ChatMessage = {
      id: `temp-${Date.now()}`,
      chatId: currentChat.id,
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    set((state) => ({
      messages: [...state.messages, userMessage],
    }));

    // Create assistant message placeholder
    const assistantMessageId = `stream-${Date.now()}`;
    const assistantMessage: ChatMessage = {
      id: assistantMessageId,
      chatId: currentChat.id,
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString(),
    };

    set((state) => ({
      messages: [...state.messages, assistantMessage],
    }));

    try {
      let fullContent = '';
      await chatService.sendMessageStream(
        currentChat.id,
        { content, stream: true },
        (response: ChatStreamResponse) => {
          if (response.delta) {
            fullContent += response.delta;
            onChunk(response.delta);
          }
          set((state) => ({
            messages: state.messages.map((msg) =>
              msg.id === assistantMessageId
                ? { ...msg, content: fullContent }
                : msg
            ),
          }));
        },
        () => {
          set({ isSending: false });
          onComplete();
        },
        (error: Error) => {
          set({ isSending: false, error: error.message });
          onError(error);
        }
      );
    } catch (error) {
      set({
        isSending: false,
        error: error instanceof Error ? error.message : '发送消息失败',
      });
      onError(error instanceof Error ? error : new Error('发送消息失败'));
    }
  },

  deleteChat: async (chatId) => {
    set({ isLoading: true, error: null });
    try {
      await chatService.deleteChat(chatId);
      set((state) => ({
        chats: state.chats.filter((chat) => chat.id !== chatId),
        currentChat: state.currentChat?.id === chatId ? null : state.currentChat,
        messages: state.currentChat?.id === chatId ? [] : state.messages,
        isLoading: false,
      }));
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : '删除对话失败',
      });
      throw error;
    }
  },

  updateChatTitle: async (chatId, title) => {
    try {
      const updatedChat = await chatService.updateChatTitle(chatId, title);
      set((state) => ({
        chats: state.chats.map((chat) =>
          chat.id === chatId ? updatedChat : chat
        ),
        currentChat: state.currentChat?.id === chatId
          ? updatedChat
          : state.currentChat,
      }));
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '更新标题失败',
      });
      throw error;
    }
  },

  clearMessages: () => set({ messages: [] }),

  clearError: () => set({ error: null }),
}));
