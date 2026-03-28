/**
 * 小紫 - 智能推荐引擎
 * 基于用户行为和上下文提供个性化推荐
 */

import {
  Recommendation,
  UserBehavior,
  UserProfile,
  RecommendationType
} from '../types';

export class RecommendationEngine {
  private userProfile: UserProfile | null = null;
  private behaviorHistory: UserBehavior[] = [];
  private recommendations: Map<string, Recommendation> = new Map();
  private dismissedRecommendations: Set<string> = new Set();
  private dismissedCount: number = 0;

  constructor() {
    this.initializeRecommendations();
  }

  // ==================== 用户画像管理 ====================

  /**
   * 设置用户画像
   */
  setUserProfile(profile: UserProfile): void {
    this.userProfile = profile;
    console.log(`[RecommendationEngine] 用户画像已设置: ${profile.userId}`);
  }

  /**
   * 获取用户画像
   */
  getUserProfile(): UserProfile | null {
    return this.userProfile;
  }

  // ==================== 行为追踪 ====================

  /**
   * 记录用户行为
   */
  async trackBehavior(
    action: string,
    context: Record<string, any>,
    features: string[] = []
  ): Promise<void> {
    const behavior: UserBehavior = {
      timestamp: Date.now(),
      action,
      context,
      features
    };

    this.behaviorHistory.push(behavior);
    console.log(`[RecommendationEngine] 记录行为: ${action}`, { features });

    // 触发推荐更新
    await this.updateRecommendations();
  }

  /**
   * 获取行为历史
   */
  getBehaviorHistory(limit?: number): UserBehavior[] {
    if (limit) {
      return this.behaviorHistory.slice(-limit);
    }
    return this.behaviorHistory;
  }

  /**
   * 清理过期行为记录
   */
  cleanExpiredBehaviors(retentionDays: number = 30): void {
    const cutoffTime = Date.now() - (retentionDays * 24 * 60 * 60 * 1000);
    this.behaviorHistory = this.behaviorHistory.filter(
      behavior => behavior.timestamp > cutoffTime
    );
    console.log(`[RecommendationEngine] 清理过期行为记录，保留最近 ${retentionDays} 天`);
  }

  // ==================== 推荐生成 ====================

  /**
   * 更新推荐列表
   */
  private async updateRecommendations(): Promise<void> {
    console.log('[RecommendationEngine] 开始更新推荐列表...');

    const recommendations = this.generateRecommendations();

    // 更新推荐列表
    this.recommendations.clear();
    recommendations.forEach(rec => {
      if (!this.dismissedRecommendations.has(rec.id)) {
        this.recommendations.set(rec.id, rec);
      }
    });

    console.log(`[RecommendationEngine] 推荐更新完成，共 ${recommendations.length} 条`);
  }

  /**
   * 生成推荐
   */
  private generateRecommendations(): Recommendation[] {
    const recommendations: Recommendation[] = [];

    // 分析用户行为模式
    const patterns = this.analyzeBehaviorPatterns();

    // 生成配置推荐
    recommendations.push(...this.generateConfigRecommendations(patterns));

    // 生成功能推荐
    recommendations.push(...this.generateFeatureRecommendations(patterns));

    // 生成最佳实践推荐
    recommendations.push(...this.generateBestPracticeRecommendations(patterns));

    // 生成优化建议
    recommendations.push(...this.generateOptimizationRecommendations(patterns));

    // 按优先级排序
    recommendations.sort((a, b) => b.priority - a.priority);

    return recommendations;
  }

  /**
   * 分析行为模式
   */
  private analyzeBehaviorPatterns(): Record<string, any> {
    const patterns: Record<string, any> = {
      mostCommonActions: {} as Record<string, number>,
      mostUsedFeatures: {} as Record<string, number>,
      timePatterns: {} as Record<string, number>,
      errorCount: 0,
      successCount: 0
    };

    this.behaviorHistory.forEach(behavior => {
      // 统计常用操作
      patterns.mostCommonActions[behavior.action] =
        (patterns.mostCommonActions[behavior.action] || 0) + 1;

      // 统计常用功能
      behavior.features.forEach(feature => {
        patterns.mostUsedFeatures[feature] =
          (patterns.mostUsedFeatures[feature] || 0) + 1;
      });

      // 时间模式
      const hour = new Date(behavior.timestamp).getHours();
      const timeSlot = hour < 12 ? 'morning' : hour < 18 ? 'afternoon' : 'evening';
      patterns.timePatterns[timeSlot] = (patterns.timePatterns[timeSlot] || 0) + 1;

      // 成功/失败统计
      if (behavior.context.success === false) {
        patterns.errorCount++;
      } else if (behavior.context.success === true) {
        patterns.successCount++;
      }
    });

    return patterns;
  }

  // ==================== 配置推荐 ====================

  private generateConfigRecommendations(patterns: any): Recommendation[] {
    const recommendations: Recommendation[] = [];

    // 检测频繁错误操作
    if (patterns.errorCount > 3) {
      recommendations.push({
        id: 'config_error_handling',
        type: RecommendationType.CONFIGURATION,
        title: '启用错误处理增强模式',
        description: '检测到您近期遇到较多操作错误，建议启用错误处理增强模式以提供更详细的错误信息和解决方案。',
        priority: 80,
        confidence: 0.85,
        actions: [
          {
            type: 'apply',
            label: '启用增强模式',
            payload: {
              config: { errorHandling: 'enhanced' }
            }
          },
          {
            type: 'dismiss',
            label: '暂不启用',
            payload: {}
          }
        ]
      });
    }

    // 检测特定功能高频使用
    const mostUsedFeature = Object.entries(patterns.mostUsedFeatures)
      .sort((a, b) => b[1] - a[1])[0];

    if (mostUsedFeature && mostUsedFeature[1] as number > 5) {
      recommendations.push({
        id: 'config_feature_optimization',
        type: RecommendationType.CONFIGURATION,
        title: `优化 ${mostUsedFeature[0]} 功能配置`,
        description: `您频繁使用 ${mostUsedFeature[0]} 功能，建议优化相关配置以提升性能。`,
        priority: 60,
        confidence: 0.75,
        actions: [
          {
            type: 'apply',
            label: '应用优化',
            payload: {
              feature: mostUsedFeature[0],
              optimization: true
            }
          },
          {
            type: 'snooze',
            label: '稍后提醒',
            payload: { delay: 3600000 } // 1小时
          }
        ]
      });
    }

    return recommendations;
  }

  // ==================== 功能推荐 ====================

  private generateFeatureRecommendations(patterns: any): Recommendation[] {
    const recommendations: Recommendation[] = [];

    // 根据已用功能推荐相关功能
    const usedFeatures = Object.keys(patterns.mostUsedFeatures);

    if (!usedFeatures.includes('voice_input') && this.userProfile?.skillLevel === 'beginner') {
      recommendations.push({
        id: 'feature_voice_input',
        type: RecommendationType.FEATURE,
        title: '尝试语音输入',
        description: '语音输入可以更快速地表达您的想法，特别适合移动场景使用。',
        priority: 50,
        confidence: 0.6,
        actions: [
          {
            type: 'apply',
            label: '开始使用',
            payload: { action: 'enable_voice_input' }
          }
        ]
      });
    }

    if (!usedFeatures.includes('shortcut') && patterns.successCount > 10) {
      recommendations.push({
        id: 'feature_shortcuts',
        type: RecommendationType.FEATURE,
        title: '学习快捷操作',
        description: '您已经熟悉基本操作，可以尝试使用快捷键来提升效率。',
        priority: 55,
        confidence: 0.7,
        actions: [
          {
            type: 'apply',
            label: '查看快捷键',
            payload: { action: 'show_shortcuts' }
          }
        ]
      });
    }

    return recommendations;
  }

  // ==================== 最佳实践推荐 ====================

  private generateBestPracticeRecommendations(patterns: any): Recommendation[] {
    const recommendations: Recommendation[] = [];

    // 检测是否在合适时间工作
    const timePatterns = patterns.timePatterns;
    const totalActions = this.behaviorHistory.length;

    if (totalActions > 10) {
      const eveningRatio = (timePatterns.evening || 0) / totalActions;

      if (eveningRatio > 0.6) {
        recommendations.push({
          id: 'practice_evening' as any,
          type: RecommendationType.BEST_PRACTICE,
          title: '健康工作提醒',
          description: '您经常在晚上使用系统，建议合理安排时间，保护视力健康。',
          priority: 40,
          confidence: 0.65,
          actions: [
            {
              type: 'dismiss',
              label: '知道了',
              payload: {}
            }
          ]
        });
      }
    }

    return recommendations;
  }

  // ==================== 优化建议 ====================

  private generateOptimizationRecommendations(patterns: any): Recommendation[] {
    const recommendations: Recommendation[] = [];

    // 检测行为频率
    const totalActions = this.behaviorHistory.length;

    if (totalActions > 20) {
      recommendations.push({
        id: 'optimization_batch',
        type: RecommendationType.OPTIMIZATION,
        title: '启用批量操作',
        description: '检测到您有大量相似操作，建议使用批量操作功能来提升效率。',
        priority: 70,
        confidence: 0.8,
        actions: [
          {
            type: 'apply',
            label: '查看批量操作',
            payload: { action: 'show_batch_operations' }
          },
          {
            type: 'dismiss',
            label: '暂不需要',
            payload: {}
          }
        ]
      });
    }

    return recommendations;
  }

  // ==================== 推荐管理 ====================

  /**
   * 获取推荐列表
   */
  getRecommendations(maxCount?: number): Recommendation[] {
    let recommendations = Array.from(this.recommendations.values());

    // 过滤过期的推荐
    const now = Date.now();
    recommendations = recommendations.filter(rec => {
      if (rec.expiresAt && rec.expiresAt < now) {
        this.recommendations.delete(rec.id);
        return false;
      }
      return true;
    });

    // 按优先级和置信度排序
    recommendations.sort((a, b) => {
      if (a.priority !== b.priority) return b.priority - a.priority;
      return b.confidence - a.confidence;
    });

    // 限制数量
    if (maxCount) {
      recommendations = recommendations.slice(0, maxCount);
    }

    return recommendations;
  }

  /**
   * 获取特定类型的推荐
   */
  getRecommendationsByType(type: RecommendationType): Recommendation[] {
    return this.getRecommendations().filter(rec => rec.type === type);
  }

  /**
   * 驳回推荐
   */
  async dismissRecommendation(recommendationId: string): Promise<void> {
    this.recommendations.delete(recommendationId);
    this.dismissedRecommendations.add(recommendationId);
    this.dismissedCount++;

    console.log(`[RecommendationEngine] 驳回推荐: ${recommendationId}`);

    // 记录驳回行为
    await this.trackBehavior('dismiss_recommendation', {
      recommendationId
    });
  }

  /**
   * 应用推荐
   */
  async applyRecommendation(
    recommendationId: string,
    actionPayload?: any
  ): Promise<boolean> {
    const recommendation = this.recommendations.get(recommendationId);
    if (!recommendation) {
      console.error(`[RecommendationEngine] 未找到推荐: ${recommendationId}`);
      return false;
    }

    console.log(`[RecommendationEngine] 应用推荐: ${recommendation.title}`);

    // 记录应用行为
    await this.trackBehavior('apply_recommendation', {
      recommendationId,
      payload: actionPayload
    });

    // 从列表中移除
    this.recommendations.delete(recommendationId);

    return true;
  }

  // ==================== 初始化推荐 ====================

  /**
   * 初始化默认推荐
   */
  private initializeRecommendations(): void {
    console.log('[RecommendationEngine] 初始化推荐引擎...');
  }

  // ==================== 统计信息 ====================

  /**
   * 获取统计信息
   */
  getStats(): {
    totalRecommendations: number;
    dismissedRecommendations: number;
    behaviorCount: number;
  } {
    return {
      totalRecommendations: this.recommendations.size,
      dismissedRecommendations: this.dismissedRecommendations.size,
      behaviorCount: this.behaviorHistory.length
    };
  }

  /**
   * 重置推荐状态
   */
  reset(): void {
    this.recommendations.clear();
    this.dismissedRecommendations.clear();
    this.behaviorHistory = [];
    this.dismissedCount = 0;
    console.log('[RecommendationEngine] 推荐状态已重置');
  }
}
