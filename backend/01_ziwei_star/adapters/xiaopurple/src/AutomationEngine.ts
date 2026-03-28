/**
 * 小紫 - 自动化操作引擎
 * 支持自动填写表单、自动导航、批量操作等自动化任务
 */

import {
  AutomationTask,
  AutomationStep
} from '../types';

export class AutomationEngine {
  private taskQueue: AutomationTask[] = [];
  private runningTasks: Map<string, AutomationTask> = new Map();
  private completedTasks: Map<string, AutomationTask> = new Map();
  private requireConfirmation: boolean = true;

  constructor(requireConfirmation: boolean = true) {
    this.requireConfirmation = requireConfirmation;
  }

  // ==================== 任务管理 ====================

  /**
   * 创建自动化任务
   */
  createTask(
    type: 'form_fill' | 'navigation' | 'batch_operation',
    name: string,
    steps: AutomationStep[]
  ): AutomationTask {
    const task: AutomationTask = {
      id: this.generateId(),
      type,
      name,
      status: 'pending',
      steps,
    };

    this.taskQueue.push(task);
    console.log(`[AutomationEngine] 创建任务: ${name}`, { taskId: task.id });

    return task;
  }

  /**
   * 执行任务
   */
  async executeTask(
    taskId: string,
    confirm: boolean = false
  ): Promise<AutomationTask> {
    // 检查任务是否存在
    let task = this.findTask(taskId);
    if (!task) {
      throw new Error(`未找到任务: ${taskId}`);
    }

    // 需要确认
    if (this.requireConfirmation && !confirm) {
      return {
        ...task,
        status: 'pending',
        error: '需要确认后才能执行'
      };
    }

    // 从队列中移除
    this.taskQueue = this.taskQueue.filter(t => t.id !== taskId);

    // 更新状态
    task.status = 'running';
    this.runningTasks.set(taskId, task);

    console.log(`[AutomationEngine] 开始执行任务: ${task.name}`);

    try {
      // 执行所有步骤
      const results = [];
      for (const step of task.steps) {
        const result = await this.executeStep(step);
        results.push(result);
      }

      // 任务完成
      task.status = 'completed';
      task.result = results;

      this.runningTasks.delete(taskId);
      this.completedTasks.set(taskId, task);

      console.log(`[AutomationEngine] 任务完成: ${task.name}`);

    } catch (error) {
      // 任务失败
      task.status = 'failed';
      task.error = error instanceof Error ? error.message : String(error);

      this.runningTasks.delete(taskId);
      this.completedTasks.set(taskId, task);

      console.error(`[AutomationEngine] 任务失败: ${task.name}`, error);
    }

    return task;
  }

  /**
   * 取消任务
   */
  cancelTask(taskId: string): boolean {
    // 检查正在运行的任务
    const runningTask = this.runningTasks.get(taskId);
    if (runningTask) {
      runningTask.status = 'failed';
      runningTask.error = '任务已取消';
      this.runningTasks.delete(taskId);
      console.log(`[AutomationEngine] 取消任务: ${taskId}`);
      return true;
    }

    // 检查队列中的任务
    const queueIndex = this.taskQueue.findIndex(t => t.id === taskId);
    if (queueIndex !== -1) {
      this.taskQueue.splice(queueIndex, 1);
      console.log(`[AutomationEngine] 从队列移除任务: ${taskId}`);
      return true;
    }

    return false;
  }

  // ==================== 步骤执行 ====================

  /**
   * 执行单个步骤
   */
  private async executeStep(step: AutomationStep): Promise<any> {
    console.log(`[AutomationEngine] 执行步骤: ${step.type}`);

    switch (step.type) {
      case 'navigation':
        return await this.executeNavigation(step);

      case 'form_fill':
        return await this.executeFormFill(step);

      case 'click':
        return await this.executeClick(step);

      case 'input':
        return await this.executeInput(step);

      case 'scroll':
        return await this.executeScroll(step);

      case 'wait':
        return await this.executeWait(step);

      default:
        throw new Error(`不支持的步骤类型: ${step.type}`);
    }
  }

  /**
   * 执行导航
   */
  private async executeNavigation(step: AutomationStep): Promise<any> {
    const url = step.value;
    console.log(`[AutomationEngine] 导航到: ${url}`);

    // 这里可以集成实际的导航逻辑
    // 例如使用 puppeteer 或 playwright

    return {
      stepId: step.id,
      type: 'navigation',
      success: true,
      url
    };
  }

  /**
   * 执行表单填写
   */
  private async executeFormFill(step: AutomationStep): Promise<any> {
    const formData = step.value;
    console.log(`[AutomationEngine] 填写表单:`, formData);

    // 这里可以集成实际的表单填写逻辑

    return {
      stepId: step.id,
      type: 'form_fill',
      success: true,
      fields: Object.keys(formData)
    };
  }

  /**
   * 执行点击
   */
  private async executeClick(step: AutomationStep): Promise<any> {
    const selector = step.selector;
    console.log(`[AutomationEngine] 点击元素: ${selector}`);

    // 这里可以集成实际的点击逻辑

    return {
      stepId: step.id,
      type: 'click',
      success: true,
      selector
    };
  }

  /**
   * 执行输入
   */
  private async executeInput(step: AutomationStep): Promise<any> {
    const selector = step.selector;
    const value = step.value;
    console.log(`[AutomationEngine] 输入内容: ${selector} = ${value}`);

    // 这里可以集成实际的输入逻辑

    return {
      stepId: step.id,
      type: 'input',
      success: true,
      selector,
      value
    };
  }

  /**
   * 执行滚动
   */
  private async executeScroll(step: AutomationStep): Promise<any> {
    const scrollY = step.value;
    console.log(`[AutomationEngine] 滚动到: ${scrollY}`);

    // 这里可以集成实际的滚动逻辑

    return {
      stepId: step.id,
      type: 'scroll',
      success: true,
      scrollY
    };
  }

  /**
   * 执行等待
   */
  private async executeWait(step: AutomationStep): Promise<any> {
    const duration = step.value || 1000;
    console.log(`[AutomationEngine] 等待: ${duration}ms`);

    await new Promise(resolve => setTimeout(resolve, duration));

    return {
      stepId: step.id,
      type: 'wait',
      success: true,
      duration
    };
  }

  // ==================== 批量操作 ====================

  /**
   * 创建批量操作任务
   */
  createBatchTask(
    name: string,
    operations: Array<{
      type: string;
      data: any;
    }>
  ): AutomationTask {
    const steps: AutomationStep[] = operations.map((op, index) => ({
      id: `batch_step_${index}`,
      type: op.type,
      value: op.data
    }));

    return this.createTask('batch_operation', name, steps);
  }

  /**
   * 批量导航
   */
  createBatchNavigationTask(urls: string[]): AutomationTask {
    const steps: AutomationStep[] = urls.map((url, index) => ({
      id: `nav_step_${index}`,
      type: 'navigation',
      value: url
    }));

    return this.createTask('batch_operation', '批量导航', steps);
  }

  /**
   * 批量表单填写
   */
  createBatchFormFillTask(forms: Array<{ selector: string; data: any }>): AutomationTask {
    const steps: AutomationStep[] = forms.flatMap((form, formIndex) => {
      return Object.entries(form.data).map(([key, value], fieldIndex) => ({
({
        id: `form_${formIndex}_field_${fieldIndex}`,
        type: 'input',
        selector: `${form.selector} [name="${key}"]`,
        value
      }));
    });

    return this.createTask('batch_operation', '批量表单填写', steps);
  }

  // ==================== 任务查询 ====================

  /**
   * 查找任务
   */
  private findTask(taskId: string): AutomationTask | undefined {
    return (
      this.taskQueue.find(t => t.id === taskId) ||
      this.runningTasks.get(taskId) ||
      this.completedTasks.get(taskId)
    );
  }

  /**
   * 获取任务
   */
  getTask(taskId: string): AutomationTask | null {
    return this.findTask(taskId) || null;
  }

  /**
   * 获取所有任务
   */
  getAllTasks(): {
    pending: AutomationTask[];
    running: AutomationTask[];
    completed: AutomationTask[];
  } {
    return {
      pending: [...this.taskQueue],
      running: Array.from(this.runningTasks.values()),
      completed: Array.from(this.completedTasks.values())
    };
  }

  /**
   * 获取任务状态
   */
  getTaskStatus(taskId: string): 'pending' | 'running' | 'completed' | 'failed' | null {
    const task = this.findTask(taskId);
    return task ? task.status : null;
  }

  // ==================== 配置管理 ====================

  /**
   * 设置是否需要确认
   */
  setRequireConfirmation(require: boolean): void {
    this.requireConfirmation = require;
    console.log(`[AutomationEngine] 设置确认要求: ${require}`);
  }

  /**
   * 清空已完成任务
   */
  clearCompletedTasks(): void {
    this.completedTasks.clear();
    console.log('[AutomationEngine] 清空已完成任务');
  }

  /**
   * 清空所有任务
   */
  clearAllTasks(): void {
    this.taskQueue = [];
    this.runningTasks.clear();
    this.completedTasks.clear();
    console.log('[AutomationEngine] 清空所有任务');
  }

  // ==================== 辅助方法 ====================

  /**
   * 生成唯一 ID
   */
  private generateId(): string {
    return `auto_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    pendingTasks: number;
    runningTasks: number;
    completedTasks: number;
    totalSteps: number;
  } {
    const runningTasks = Array.from(this.runningTasks.values());
    const completedTasks = Array.from(this.completedTasks.values());

    return {
      pendingTasks: this.taskQueue.length,
      runningTasks: runningTasks.length,
      completedTasks: completedTasks.length,
      totalSteps: [
        ...this.taskQueue,
        ...runningTasks,
        ...completedTasks
      ].reduce((sum, task) => sum + task.steps.length, 0)
    };
  }
}
