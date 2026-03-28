import apiService from './api';
import type {
  AssistantMessage,
  AssistantContext,
  AssistantAction,
  GuideStep,
  OnboardingGuide,
  Recommendation,
} from '@/types';

class AssistantService {
  // 对话管理

  // 发送消息
  async sendMessage(message: string): Promise<AssistantMessage> {
    const response = await apiService.post<AssistantMessage>('/assistant/message', {
      message,
    });
    return response.data as AssistantMessage;
  }

  // 获取对话历史
  async getMessages(limit: number = 20): Promise<AssistantMessage[]> {
    const response = await apiService.get<AssistantMessage[]>('/assistant/messages', {
      params: { limit },
    });
    return response.data as AssistantMessage[];
  }

  // 清除对话历史
  async clearHistory(): Promise<void> {
    await apiService.delete('/assistant/messages');
  }

  // 上下文管理

  // 获取当前上下文
  async getContext(): Promise<AssistantContext> {
    const response = await apiService.get<AssistantContext>('/assistant/context');
    return response.data as AssistantContext;
  }

  // 更新上下文
  async updateContext(context: Partial<AssistantContext>): Promise<void> {
    await apiService.patch('/assistant/context', context);
  }

  // 动作执行

  // 执行动作
  async executeAction(action: AssistantAction): Promise<void> {
    await apiService.post('/assistant/execute', action);
  }

  // 获取推荐动作
  async getRecommendedActions(): Promise<AssistantAction[]> {
    const response = await apiService.get<AssistantAction[]>('/assistant/recommendations');
    return response.data as AssistantAction[];
  }

  // 引导管理

  // 获取引导步骤
  async getGuideSteps(guideId: string): Promise<GuideStep[]> {
    const response = await apiService.get<GuideStep[]>(`/assistant/guides/${guideId}/steps`);
    return response.data as GuideStep[];
  }

  // 开始新手引导
  async startOnboarding(): Promise<OnboardingGuide> {
    const response = await apiService.post<OnboardingGuide>('/assistant/onboarding/start');
    return response.data as OnboardingGuide;
  }

  // 更新引导进度
  async updateOnboardingProgress(step: number): Promise<OnboardingGuide> {
    const response = await apiService.patch<OnboardingGuide>('/assistant/onboarding/progress', {
      step,
    });
    return response.data as OnboardingGuide;
  }

  // 完成新手引导
  async completeOnboarding(): Promise<void> {
    await apiService.post('/assistant/onboarding/complete');
  }

  // 跳过新手引导
  async skipOnboarding(): Promise<void> {
    await apiService.post('/assistant/onboarding/skip');
  }

  // 推荐管理

  // 获取推荐列表
  async getRecommendations(): Promise<Recommendation[]> {
    const response = await apiService.get<Recommendation[]>('/assistant/recommendations');
    return response.data as Recommendation[];
  }

  // 忽略推荐
  async dismissRecommendation(id: string): Promise<void> {
    await apiService.post(`/assistant/recommendations/${id}/dismiss`);
  }

  // 快捷操作

  // 快速创建数字人
  async quickCreateDigitalHuman(): Promise<string> {
    const response = await apiService.post<{ url: string }>('/assistant/quick-create-digital-human');
    return (response.data as { url: string }).url;
  }

  // 快速开始对话
  async quickStartChat(digitalHumanId: string): Promise<string> {
    const response = await apiService.post<{ url: string }>('/assistant/quick-start-chat', {
      digitalHumanId,
    });
    return (response.data as { url: string }).url;
  }

  // 语音交互

  // 启用语音输入
  async enableVoiceInput(language: string = 'zh-CN'): Promise<void> {
    await apiService.post('/assistant/voice/enable', { language });
  }

  // 禁用语音输入
  async disableVoiceInput(): Promise<void> {
    await apiService.post('/assistant/voice/disable');
  }

  // 获取语音配置
  async getVoiceConfig(): Promise<{ enabled: boolean; language: string }> {
    const response = await apiService.get('/assistant/voice/config');
    return response.data as { enabled: boolean; language: string };
  }
}

export const assistantService = new AssistantService();
export default assistantService;
