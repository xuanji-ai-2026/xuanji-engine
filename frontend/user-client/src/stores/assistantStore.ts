import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { AssistantMessage, GuideStep, Recommendation } from '@/types';
import assistantService from '@/services/assistant';

interface AssistantState {
  messages: AssistantMessage[];
  guideSteps: GuideStep[];
  currentStep: number;
  isGuideCompleted: boolean;
  isGuideStarted: boolean;
  recommendations: Recommendation[];
  isVoiceEnabled: boolean;
  voiceLanguage: string;
  isTyping: boolean;
  error: string | null;

  sendMessage: (message: string) => Promise<void>;
  fetchMessages: () => Promise<void>;
  clearHistory: () => Promise<void>;
  startGuide: () => Promise<void>;
  nextGuideStep: () => void;
  previousGuideStep: () => void;
  completeGuide: () => Promise<void>;
  skipGuide: () => Promise<void>;
  fetchRecommendations: () => Promise<void>;
  dismissRecommendation: (id: string) => Promise<void>;
  toggleVoice: () => Promise<void>;
  clearError: () => void;
  clearMessages: () => void;
}

export const useAssistantStore = create<AssistantState>()(
  persist(
    (set, get) => ({
      messages: [],
      guideSteps: [],
      currentStep: 0,
      isGuideCompleted: false,
      isGuideStarted: false,
      recommendations: [],
      isVoiceEnabled: false,
      voiceLanguage: 'zh-CN',
      isTyping: false,
      error: null,

      sendMessage: async (message) => {
        set({ isTyping: true, error: null });

        // Add user message
        const userMessage: AssistantMessage = {
          id: `user-${Date.now()}`,
          role: 'user',
          content: message,
          timestamp: new Date().toISOString(),
          type: 'text',
        };

        set((state) => ({
          messages: [...state.messages, userMessage],
        }));

        try {
          const response = await assistantService.sendMessage(message);
          set((state) => ({
            messages: [...state.messages, response],
            isTyping: false,
          }));
        } catch (error) {
          set({
            isTyping: false,
            error: error instanceof Error ? error.message : '发送消息失败',
          });
          throw error;
        }
      },

      fetchMessages: async () => {
        try {
          const messages = await assistantService.getMessages(20);
          set({ messages });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : '获取消息失败',
          });
        }
      },

      clearHistory: async () => {
        try {
          await assistantService.clearHistory();
          set({ messages: [] });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : '清除历史失败',
          });
        }
      },

      startGuide: async () => {
        try {
          const guide = await assistantService.startOnboarding();
          const steps = await assistantService.getGuideSteps(guide.id);
          set({
            guideSteps: steps,
            currentStep: 0,
            isGuideStarted: true,
            isGuideCompleted: false,
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : '启动引导失败',
          });
        }
      },

      nextGuideStep: () => {
        const { currentStep, guideSteps } = get();
        if (currentStep < guideSteps.length - 1) {
          set({ currentStep: currentStep + 1 });
        }
      },

      previousGuideStep: () => {
        const { currentStep } = get();
        if (currentStep > 0) {
          set({ currentStep: currentStep - 1 });
        }
      },

      completeGuide: async () => {
        try {
          await assistantService.completeOnboarding();
          set({
            isGuideCompleted: true,
            currentStep: 0,
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : '完成引导失败',
          });
        }
      },

      skipGuide: async () => {
        try {
          await assistantService.skipOnboarding();
          set({
            isGuideCompleted: true,
            currentStep: 0,
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : '跳过引导失败',
          });
        }
      },

      fetchRecommendations: async () => {
        try {
          const recommendations = await assistantService.getRecommendations();
          set({ recommendations });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : '获取推荐失败',
          });
        }
      },

      dismissRecommendation: async (id) => {
        try {
          await assistantService.dismissRecommendation(id);
          set((state) => ({
            recommendations: state.recommendations.filter((r) => r.id !== id),
          }));
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : '忽略推荐失败',
          });
        }
      },

      toggleVoice: async () => {
        const { isVoiceEnabled } = get();
        try {
          if (isVoiceEnabled) {
            await assistantService.disableVoiceInput();
            set({ isVoiceEnabled: false });
          } else {
            await assistantService.enableVoiceInput('zh-CN');
            set({ isVoiceEnabled: true });
          }
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : '切换语音失败',
          });
        }
      },

      clearError: () => set({ error: null }),

      clearMessages: () => set({ messages: [] }),
    }),
    {
      name: 'assistant-storage',
      partialize: (state) => ({
        isGuideCompleted: state.isGuideCompleted,
        isVoiceEnabled: state.isVoiceEnabled,
        voiceLanguage: state.voiceLanguage,
      }),
    }
  )
);
