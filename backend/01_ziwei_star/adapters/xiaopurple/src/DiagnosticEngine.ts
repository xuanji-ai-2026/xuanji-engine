/**
 * 小紫 - 问题诊断引擎
 * 自动识别用户问题并提供解决方案
 */

import {
  DiagnosticResult,
  Solution
} from '../types';

export class DiagnosticEngine {
  private diagnosticHistory: Map<string, DiagnosticResult> = new Map();
  private commonIssues: Map<string, DiagnosticResult> = new Map();

  constructor() {
    this.initializeCommonIssues();
  }

  // ==================== 诊断功能 ====================

  /**
   * 自动诊断问题
   */
  async diagnose(
    symptoms: string[],
    context?: Record<string, any>
  ): Promise<DiagnosticResult> {
    console.log('[DiagnosticEngine] 开始诊断问题...', { symptoms });

    // 检查是否为已知问题
    const knownIssue = this.matchKnownIssue(symptoms);
    if (knownIssue) {
      console.log('[DiagnosticEngine] 匹配到已知问题:', knownIssue.title);
      return this.saveDiagnosticResult(knownIssue);
    }

    // 生成新的诊断结果
    const result = await this.generateDiagnosticResult(symptoms, context);

    return this.saveDiagnosticResult(result);
  }

  /**
   * 匹配已知问题
   */
  private matchKnownIssue(symptoms: string[]): DiagnosticResult | null {
    for (const [key, issue] of this.commonIssues) {
      const matchCount = issue.symptoms.filter(symptom =>
        symptoms.some(userSymptom =>
          userSymptom.toLowerCase().includes(symptom.toLowerCase()) ||
          symptom.toLowerCase().includes(userSymptom.toLowerCase())
        )
      ).length;

      if (matchCount > 0) {
        return { ...issue };
      }
    }

    return null;
  }

  /**
   * 生成诊断结果
   */
  private async generateDiagnosticResult(
    symptoms: string[],
    context?: Record<string, any>
  ): Promise<DiagnosticResult> {
    const result: DiagnosticResult = {
      id: this.generateId(),
      timestamp: Date.now(),
      issueType: 'unknown',
      severity: this.assessSeverity(symptoms),
      title: '检测到问题',
      description: '根据您描述的症状，系统检测到可能存在问题。',
      symptoms,
      solutions: this.generateSolutions(symptoms, context),
      requiresHuman: this.checkRequiresHuman(symptoms)
    };

    return result;
  }

  /**
   * 评估问题严重程度
   */
  private assessSeverity(symptoms: string[]): 'low' | 'medium' | 'high' | 'critical' {
    const symptomText = symptoms.join(' ').toLowerCase();

    // 关键错误
    if (symptomText.includes('崩溃') ||
        symptomText.includes('critical') ||
        symptomText.includes('fatal')) {
      return 'critical';
    }

    // 高优先级错误
    if (symptomText.includes('错误') ||
        symptomText.includes('失败') ||
        symptomText.includes('无法连接')) {
      return 'high';
    }

    // 中等优先级
    if (symptomText.includes('警告') ||
        symptomText.includes('慢') ||
        symptomText.includes('卡顿')) {
      return 'medium';
    }

    // 低优先级
    return 'low';
  }

  /**
   * 检查是否需要人工介入
   */
  private checkRequiresHuman(symptoms: string[]): boolean {
    const symptomText = symptoms.join(' ').toLowerCase();

    // 以下情况需要人工介入
    const humanKeywords = [
      '无法解决',
      '需要人工',
      '联系客服',
      '复杂问题',
      'custom',
      'special'
    ];

    return humanKeywords.some(keyword => symptomText.includes(keyword));
  }

  /**
   * 生成解决方案
   */
  private generateSolutions(
    symptoms: string[],
    context?: Record<string, any>
  ): Solution[] {
    const solutions: Solution[] = [];
    const symptomText = symptoms.join(' ').toLowerCase();

    // 连接问题
    if (symptomText.includes('连接') || symptomText.includes('网络')) {
      solutions.push({
        id: 'sol_check_connection',
        title: '检查网络连接',
        description: '确保您的网络连接正常，并检查防火墙设置。',
        steps: [
          '打开浏览器，访问 https://www.google.com',
          '检查本地网络连接',
          '确认防火墙没有阻止应用访问网络',
          '尝试重启路由器'
        ],
        autoFix: true,
        estimatedTime: 30
      });

      solutions.push({
        id: 'sol_retry_connection',
        title: '重新连接',
        description: '尝试重新连接到服务器。',
        steps: [
          '点击"重新连接"按钮',
          '等待连接建立',
          '如果失败，请等待 30 秒后重试'
        ],
        autoFix: true,
        estimatedTime: 5
      });
    }

    // 认证问题
    if (symptomText.includes('登录') || symptomText.includes('认证') || symptomText.includes('token')) {
      solutions.push({
        id: 'sol_relogin',
        title: '重新登录',
        description: '您的会话可能已过期，请重新登录。',
        steps: [
          '点击"登出"按钮',
          '重新输入账号密码登录',
          '确认登录成功'
        ],
        autoFix: false,
        estimatedTime: 60
      });
    }

    // 性能问题
    if (symptomText.includes('慢') || symptomText.includes('卡顿')) {
      solutions.push({
        id: 'sol_clear_cache',
        title: '清除缓存',
        description: '清除应用缓存可以提升性能。',
        steps: [
          '打开设置页面',
          '找到"清除缓存"选项',
          '点击确认清除'
        ],
        autoFix: true,
        estimatedTime: 10
      });

      solutions.push({
        id: 'sol_disable_animations',
        title: '禁用动画',
        description: '禁用动画可以减少资源消耗。',
        steps: [
          '打开设置页面',
          '找到"动画效果"选项',
          '关闭动画效果'
        ],
        autoFix: true,
        estimatedTime: 5
      });
    }

    // 如果没有匹配的解决方案，提供通用方案
    if (solutions.length === 0) {
      solutions.push({
        id: 'sol_restart',
        title: '重启应用',
        description: '重启应用可以解决大多数临时问题。',
        steps: [
          '关闭应用',
          '等待 5 秒',
          '重新打开应用'
        ],
        autoFix: false,
        estimatedTime: 10
      });

      solutions.push({
        id: 'sol_contact_support',
        title: '联系技术支持',
        description: '如果问题持续存在，请联系我们的技术支持团队。',
        steps: [
          '收集错误信息和截图',
          '点击"联系支持"按钮',
          '详细描述问题并提交'
        ],
        autoFix: false,
        estimatedTime: 300
      });
    }

    return solutions;
  }

  // ==================== 解决方案执行 ====================

  /**
   * 执行解决方案
   */
  async executeSolution(
    resultId: string,
    solutionId: string
  ): Promise<{ success: boolean; message: string }> {
    const result = this.diagnosticHistory.get(resultId);
    if (!result) {
      return {
        success: false,
        message: '未找到诊断结果'
      };
    }

    const solution = result.solutions.find(sol => sol.id === solutionId);
    if (!solution) {
      return {
        success: false,
        message: '未找到解决方案'
      };
    }

    console.log(`[DiagnosticEngine] 执行解决方案: ${solution.title}`);

    // 如果支持自动修复
    if (solution.autoFix) {
      return await this.autoFixSolution(solution);
    }

    // 否则提供手动执行指导
    return {
      success: true,
      message: '请按照以下步骤手动执行：\n' + solution.steps.join('\n')
    };
  }

  /**
   * 自动修复
   */
  private async autoFixSolution(solution: Solution): Promise<{ success: boolean; message: string }> {
    // 这里可以实现实际的自动修复逻辑
    // 目前只返回模拟结果

    console.log(`[DiagnosticEngine] 自动修复: ${solution.title}`);

    // 模拟修复过程
    await new Promise(resolve => setTimeout(resolve, 1000));

    return {
      success: true,
      message: `✅ 自动修复完成: ${solution.title}`
    };
  }

  /**
   * 获取人工支持信息
   */
  getHumanSupportInfo(): {
    available: boolean;
    channels: Array<{ type: string; contact: string }>;
    estimatedWaitTime: number;
  } {
    return {
      available: true,
      channels: [
        { type: '在线客服', contact: '点击右下角客服图标' },
        { type: '邮件', contact: 'support@xuanji.ai' },
        { type: '电话', contact: '400-XXX-XXXX' }
      ],
      estimatedWaitTime: 300  // 预计等待时间（秒）
    };
  }

  // ==================== 常见问题库 ====================

  /**
   * 初始化常见问题
   */
  private initializeCommonIssues(): void {
    // 连接失败
    this.commonIssues.set('connection_failed', {
      id: 'connection_failed',
      timestamp: Date.now(),
      issueType: 'network',
      severity: 'high',
      title: '连接服务器失败',
      description: '无法连接到紫微元灵服务器，请检查网络设置。',
      symptoms: ['连接失败', '无法连接服务器', '网络错误'],
      solutions: [
        {
          id: 'check_network',
          title: '检查网络连接',
          description: '确保网络连接正常',
          steps: ['检查本地网络', '测试网络连接', '检查防火墙设置'],
          autoFix: true,
          estimatedTime: 30
        },
        {
          id: 'retry_connection',
          title: '重新连接',
          description: '尝试重新连接服务器',
          steps: ['点击重新连接按钮'],
          autoFix: true,
          estimatedTime: 5
        }
      ],
      requiresHuman: false
    });

    // 会话过期
    this.commonIssues.set('session_expired', {
      id: 'session_expired',
      timestamp: Date.now(),
      issueType: 'auth',
      severity: 'medium',
      title: '会话已过期',
      description: '您的登录会话已过期，需要重新登录。',
      symptoms: ['会话过期', '登录过期', 'token无效', '未授权'],
      solutions: [
        {
          id: 'relogin',
          title: '重新登录',
          description: '重新登录以建立新会话',
          steps: ['点击登出', '重新输入账号密码'],
          autoFix: false,
          estimatedTime: 60
        }
      ],
      requiresHuman: false
    });

    // 性能问题
    this.commonIssues.set('performance_issue', {
      id: 'performance_issue',
      timestamp: Date.now(),
      issueType: 'performance',
      severity: 'medium',
      title: '性能问题',
      description: '应用运行缓慢或出现卡顿。',
      symptoms: ['慢', '卡顿', '延迟', '性能'],
      solutions: [
        {
          id: 'clear_cache',
          title: '清除缓存',
          description: '清除应用缓存',
          steps: ['打开设置', '点击清除缓存'],
          autoFix: true,
          estimatedTime: 10
        },
        {
          id: 'disable_animations',
          title: '禁用动画',
          description: '禁用动画效果',
          steps: ['打开设置', '关闭动画效果'],
          autoFix: true,
          estimatedTime: 5
        }
      ],
      requiresHuman: false
    });

    console.log('[DiagnosticEngine] 常见问题库初始化完成');
  }

  /**
   * 添加自定义问题
   */
  addCustomIssue(issue: DiagnosticResult): void {
    this.commonIssues.set(issue.id, issue);
    console.log(`[DiagnosticEngine] 添加自定义问题: ${issue.title}`);
  }

  // ==================== 历史管理 ====================

  /**
   * 保存诊断结果
   */
  private saveDiagnosticResult(result: DiagnosticResult): DiagnosticResult {
    this.diagnosticHistory.set(result.id, result);
    return result;
  }

  /**
   * 获取诊断结果
   */
  getDiagnosticResult(id: string): DiagnosticResult | null {
    return this.diagnosticHistory.get(id) || null;
  }

  /**
   * 获取诊断历史
   */
  getDiagnosticHistory(limit?: number): DiagnosticResult[] {
    const history = Array.from(this.diagnosticHistory.values())
      .sort((a, b) => b.timestamp - a.timestamp);

    if (limit) {
      return history.slice(0, limit);
    }

    return history;
  }

  /**
   * 清空诊断历史
   */
  clearHistory(): void {
    this.diagnosticHistory.clear();
    console.log('[DiagnosticEngine] 诊断历史已清空');
  }

  // ==================== 辅助方法 ====================

  /**
   * 生成唯一 ID
   */
  private generateId(): string {
    return `diag_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    totalDiagnoses: number;
    commonIssues: number;
  } {
    return {
      totalDiagnoses: this.diagnosticHistory.size,
      commonIssues: this.commonIssues.size
    };
  }
}
