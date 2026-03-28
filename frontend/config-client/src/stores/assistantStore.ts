import { create } from 'zustand'
import type { Conversation, AssistantMessage } from '@/types'

interface AssistantState {
  conversations: Conversation[]
  currentConversation: Conversation | null
  loading: boolean
  sending: boolean

  fetchConversations: () => Promise<void>
  fetchConversationById: (id: string) => Promise<void>
  createConversation: (title: string) => Promise<void>
  deleteConversation: (id: string) => Promise<void>
  sendMessage: (conversationId: string, content: string, attachments?: string[]) => Promise<void>
  setCurrentConversation: (conversation: Conversation | null) => void
  clearCurrentConversation: () => void
}

export const useAssistantStore = create<AssistantState>((set, get) => ({
  conversations: [],
  currentConversation: null,
  loading: false,
  sending: false,

  fetchConversations: async () => {
    set({ loading: true })
    try {
      const response = await fetch('/api/assistant/conversations')
      const data: Conversation[] = await response.json()

      set({
        conversations: data,
        loading: false,
      })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch conversations:', error)
    }
  },

  fetchConversationById: async (id: string) => {
    set({ loading: true })
    try {
      const response = await fetch(`/api/assistant/conversations/${id}`)
      const data: Conversation = await response.json()

      set({
        currentConversation: data,
        loading: false,
      })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch conversation:', error)
    }
  },

  createConversation: async (title: string) => {
    try {
      const response = await fetch('/api/assistant/conversations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      })

      if (response.ok) {
        const data: Conversation = await response.json()
        set({ currentConversation: data })
        await get().fetchConversations()
      }
    } catch (error) {
      console.error('Failed to create conversation:', error)
      throw error
    }
  },

  deleteConversation: async (id: string) => {
    try {
      const response = await fetch(`/api/assistant/conversations/${id}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        await get().fetchConversations()
        if (get().currentConversation?.id === id) {
          set({ currentConversation: null })
        }
      }
    } catch (error) {
      console.error('Failed to delete conversation:', error)
      throw error
    }
  },

  sendMessage: async (conversationId: string, content: string, attachments?: string[]) => {
    set({ sending: true })
    try {
      const response = await fetch(`/api/assistant/conversations/${conversationId}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, attachments }),
      })

      if (response.ok) {
        const data: AssistantMessage = await response.json()

        // 添加用户消息到当前对话
        set((state) => ({
          currentConversation: state.currentConversation
            ? {
                ...state.currentConversation,
                messages: [...state.currentConversation.messages, data],
              }
            : null,
          sending: false,
        }))

        // 模拟AI响应（实际应该从后端流式获取）
        setTimeout(async () => {
          const aiResponse: AssistantMessage = {
            id: `msg_${Date.now()}`,
            role: 'assistant',
            content: '我已收到您的消息，正在分析...',
            timestamp: new Date().toISOString(),
          }

          set((state) => ({
            currentConversation: state.currentConversation
              ? {
                  ...state.currentConversation,
                  messages: [...state.currentConversation.messages, aiResponse],
                }
              : null,
          }))
        }, 1000)
      } else {
        set({ sending: false })
      }
    } catch (error) {
      set({ sending: false })
      console.error('Failed to send message:', error)
      throw error
    }
  },

  setCurrentConversation: (conversation: Conversation | null) => {
    set({ currentConversation: conversation })
  },

  clearCurrentConversation: () => {
    set({ currentConversation: null })
  },
}))
