/**
 * 小紫 - 智能引导引擎
 * 提供新用户引导、功能发现、操作提示等功能
 */

import {
  GuideFlow,
  GuideStep,
  GuideState,
  GuideType,
  UserProfile
} from '../types';

export class GuideEngine {
  private guides: Map<string, GuideFlow> = new Map();
  private activeGuides: Map<string, GuideState> = new Map();
  private completedGuides: Set<string> = new Set();
  private userProfile: UserProfile | null = null;

  constructor() {
    this.registerDefaultGuides();
  }

  // ==================== 引导流程管理 ====================

  /**
   * 注册引导流程
   */
  registerGuide(guide: GuideFlow): void {
    this.guides.set(guide.id, guide);
    console.log(`[GuideEngine] 注册引导流程: ${guide.name}`);
  }

  /**
   * 开始引导流程
   */
  async startGuide(
    guideId: string,
    userId: string,
    skipPrerequisites = false
  ): Promise<GuideState | null> {
    const guide = this.guides.get(guideId);
    if (!guide) {
      console.error(`[GuideEngine] 未找到引导流程: ${guideId}`);
      return null;
    }

    // 检查前置条件
    if (!skipPrerequisites && guide.prerequisites) {
      const prerequisitesMet = guide.prerequisites.every(
        prereq => this.completedGuides.has(prereq)
      );
      if (!prerequisitesMet) {
        console.warn(`[GuideEngine] 前置条件未满足: ${guide.prerequisites}`);
        return null;
      }
    }

    // 创建引导状态
    const state: GuideState = {
      flowId: guideId,
      currentStepId: guide.steps[0].id,
      completedSteps: [],
      startTime: Date.now(),
      progress: 0
    };

    this.activeGuides.set(`${userId}:${guideId}`, state);
    console.log(`[GuideEngine] 开始引导流程: ${guide.name}`);

    return state;
  }

  /**
   * 获取当前步骤
   */
  getCurrentStep(userId: string, guideId: string): GuideStep | null {
    const state = this.activeGuides.get(`${userId}:${guideId}`);
    if (!state) return null;

    const guide = this.guides.get(guideId);
    if (!guide) return null;

    return guide.steps.find(step => step.id === state.currentStepId) || null;
  }

  /**
   * 完成当前步骤
   */
  async completeStep(userId: string, guideId: string): Promise<GuideStep | null> {
    const state = this.activeGuides.get(`${userId}:${guideId}`);
    if (!state) return null;

    const guide = this.guides.get(guideId);
    if (!guide) return null;

    const currentStepIndex = guide.steps.findIndex(
      step => step.id === state.currentStepId
    );
    if (currentStepIndex === -1) return null;

    // 标记当前步骤为已完成
    state.completedSteps.push(state.currentStepId);

    // 计算进度
    state.progress = Math.round(
      (state.completedSteps.length / guide.steps.length) * 100
    );

    // 获取下一步
    const nextStep = guide.steps[currentStepIndex + 1];

    if (nextStep) {
      state.currentStepId = nextStep.id;
    } else {
      // 完成整个引导流程
      this.completeGuide(userId, guideId);
      return null;
    }

    return nextStep;
  }

  /**
   * 跳过当前步骤
   */
  async skipStep(userId: string, guideId: string): Promise<GuideStep | null> {
    return this.completeStep(userId, guideId);
  }

  /**
   * 完成整个引导流程
   */
  async completeGuide(userId: string, guideId: string): Promise<void> {
    const state = this.activeGuides.get(`${userId}:${guideId}`);
    if (state) {
      this.completedGuides.add(guideId);
      this.activeGuides.delete(`${userId}:${guideId}`);
      console.log(`[GuideEngine] 完成引导流程: ${guideId}, 耗时: ${Date.now() - state.startTime}ms`);
    }
  }

  /**
   * 取消引导流程
   */
  cancelGuide(userId: string, guideId: string): void {
    this.activeGuides.delete(`${userId}:${guideId}`);
    console.log(`[GuideEngine] 取取消引导流程: ${guideId}`);
  }

  // ==================== 智能查询 ====================

  /**
   * 根据上下文推荐引导
   */
  recommendGuides(
    context: { userId: string; action?: string; features?: string[] }
  ): GuideFlow[] {
    const recommendations: GuideFlow[] = [];

    for (const [id, guide] of this.guides) {
      // 检查是否已完成
      if (this.completedGuides.has(id)) continue;

      // 检查是否正在进行中
      if (this.activeGuides.has(`${context.userId}:${id}`)) continue;

      // 根据上下文匹配
      if (this.shouldRecommenGuide(guide, context)) {
        recommendations.push(guide);
      }
    }

    return recommendations;
  }

  /**
   * 判断是否应该推荐该引导
   */
  private shouldRecommenGuide(guide: GuideFlow, context: any): boolean {
    // 新用户引导 - 只推荐给新用户
    if (guide.type === GuideType.NEW_ONBOARDING) {
      return context.isNewUser === true;
    }

    // 功能发现 - 根据用户行为推荐
    if (guide.type === GuideType.FEATURE_DISCOVERY) {
      if (context.features) {
        return guide.steps.some(step =>
          step.actions?.some(action =>
            context.features.includes(action.type)
          )
        );
      }
    }

    // 操作提示 - 根据当前操作推荐
    if (guide.type === GuideType.OPERATION_HINT) {
      return context.action && guide.description.includes(context.action);
    }

    return false;
  }

  /**
   * 检查引导跳过条件
   */
  checkSkipCondition(condition: string, context: Record<string, any>): boolean {
    if (!condition) return false;

    try {
      // 安全的条件评估
      const keys = Object.keys(context);
      const values = Object.values(context);
      const func = new Function(...keys, `return ${condition}`);
      return func(...values);
    } catch (error) {
      console.error(`[GuideEngine] 条件评估失败: ${condition}`, error);
      return false;
    }
  }

  // ==================== 用户画像 ====================

  /**
   * 设置用户画像
   */
  setUserProfile(profile: UserProfile): void {
    this.userProfile = profile;
    console.log(`[GuideEngine] 设置用户画像: ${profile.skillLevel}`);
  }

  /**
   * 根据用户技能级别调整引导内容
   */
  adjustContentForSkillLevel(
    content: string,
    skillLevel?: 'beginner' | 'intermediate' | 'advanced'
  ): string {
    const level = skillLevel || this.userProfile?.skillLevel || 'beginner';

    switch (level) {
      case 'beginner':
        // 添加更详细的解释
        if (!content.includes('提示：') && !content.includes('说明：')) {
          content = `${content}\n\n💡 提示：这是一个基础操作，跟着步骤完成即可。`;
        }
        break;
      case 'intermediate':
        // 添加进阶提示
        if (!content.includes('进阶：')) {
          content = `${content}\n\n🔧 进阶：您可以在完成后尝试更多高级配置。`;
        }
        break;
      case 'advanced':
        // 保持简洁
        content = content.replace(/💡.*提示：.*/g, '');
        break;
    }

    return content;
  }

  // ==================== 默认引导流程 ====================

  /**
   * 注册默认引导流程
   */
  private registerDefaultGuides(): void {
    // 新用户引导流程
    this.registerGuide({
      id: 'new_user_onboarding',
      name: '新用户入门引导',
      description: '帮助新用户快速了解紫微元灵的基本功能',
      type: GuideType.NEW_ONBOARDING,
      steps: [
        {
          id: 'welcome',
          title: '欢迎使用紫微元灵',
          content: '欢迎来到紫微元灵！我是小紫，您的智能助手。让我带您快速了解这里的功能。',
          type: GuideType.NEW_ONBOARDING,
          order: 1,
          actionable: true,
          actions: [
            {
              id: 'start_tour',
              label: '开始体验',
              type: 'navigation',
              payload: { route: '/dashboard' }
            }
          ],
          nextStepId: 'basic_chat'
        },
        {
          id: 'basic_chat',
          title: '基础对话功能',
          content: '您可以通过对话的方式与紫微元灵交互，无论是文本还是语音，我都能理解您的需求。',
          type: GuideType.NEW_ONBOARDING,
          order: 2,
          actionable: true,
          actions: [
            {
              id: 'try_chat',
              label: '尝试对话',
              type: 'navigation',
              payload: { route: '/chat' }
            }
          ],
          nextStepId: 'features_discovery'
        },
        {
          id: 'features_discovery',
          title: '探索功能',
          content: '紫微元灵提供了丰富的功能模块，包括智能推荐、自动化操作、问题诊断等。',
          type: GuideType.NEW_ONBOARDING,
          order: 3,
          actionable: true,
          actions: [
            {
              id: 'explore_features',
              label: '探索功能',
              type: 'navigation',
              payload: { route: '/features' }
            }
          ],
          nextStepId: 'complete'
        },
        {
          id: 'complete',
          title: '引导完成',
          content: '恭喜您完成了新手引导！现在您可以自由探索紫微元灵的各项功能了。',
          type: GuideType.NEW_ONBOARDING,
          order: 4
        }
      ]
    });

    // 功能发现引导 - 配置优化
    this.registerGuide({
      id: 'config_optimization',
      name: '配置优化建议',
      description: '帮助用户优化系统配置以获得更好的性能',
      type: GuideType.FEATURE_DISCOVERY,
      steps: [
        {
          id: 'check_config',
          title: '检查当前配置',
          content: '我发现您的配置有优化空间，让我为您检查一下...',
          type: GuideType.FEATURE_DISCOVERY,
          order: 1,
          nextStepId: 'apply_recommendations'
        },
        {
          id: 'apply_recommendations',
          title: '应用优化建议',
          content: '建议启用自动缓存和懒加载以提升性能。是否立即应用？',
          type: GuideType.FEATURE_DISCOVERY,
          order: 2,
          actionable: true,
          actions: [
            {
              id: 'apply_config',
              label: '应用配置',
              type: 'api_call',
              payload: { action: 'update_config', settings: { cache: true, lazyLoad: true } }
            }
          ]
        }
      ]
    });

    console.log('[GuideEngine] 默认引导流程注册完成');
  }

  // ==================== 状态查询 ====================

  /**
   * 获取引导统计
   */
  getStats(): {
    totalGuides: number;
    activeGuides: number;
    completedGuides: number;
  } {
    return {
      totalGuides: this.guides.size,
      activeGuides: this.activeGuides.size,
      completedGuides: this.completedGuides.size
    };
  }

  /**
   * 检查引导是否完成
   */
  isGuideCompleted(guideId: string): boolean {
    return this.completedGuides.has(guideId);
  }

  /**
   * 检查引导是否活跃
   */
  isGuideActive(userId: string, guideId: string): boolean {
    return this.activeGuides.has(`${userId}:${guideId}`);
  }
}
