/**
 * 小微适配层 - 工作台协助
 * 版本: v1.0.0
 * 描述: 工作台流程引导、快速操作建议、批量配置管理
 */

import {
  XiaoweiConfig,
  MessageType,
  Message,
  BaseResponse,
  WorkbenchGuide,
  WorkbenchSuggestion,
  BatchConfigOperation
} from '../types';
import { ConfigAdapter } from './ConfigAdapter';

export class WorkbenchHelper {
  private configAdapter: ConfigAdapter;

  constructor(configAdapter: ConfigAdapter) {
    this.configAdapter = configAdapter;
  }

  /**
   * 获取工作台引导流程
   * @param taskType 任务类型（setup, configure, deploy, etc.）
   */
  async getGuide(taskType: string): Promise<BaseResponse<WorkbenchGuide>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.WORKBENCH_GUIDE,
      payload: { taskType },
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<WorkbenchGuide>>(message);
  }

  /**
   * 获取快速操作建议
   * @param context 当前上下文信息
   */
  async getSuggestions(context: {
    currentPage?: string;
    userRole?: string;
    recentActions?: string[];
    configChanges?: string[];
  }): Promise<BaseResponse<WorkbenchSuggestion[]>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.WORKBENCH_SUGGEST,
      payload: { context },
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<WorkbenchSuggestion[]>>(message);
  }

  /**
   * 获取工作台流程状态
   * @param flowId 流程 ID
   */
  async getFlowStatus(flowId: string): Promise<BaseResponse<any>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.WORKBENCH_FLOW,
      payload: { flowId, action: 'status' },
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<any>>(message);
  }

  /**
   * 开始工作台流程
   * @param flowType 流程类型
   * @param params 流程参数
   */
  async startFlow(flowType: string, params?: Record<string, any>): Promise<BaseResponse<{ flowId: string }>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.WORKBENCH_FLOW,
      payload: { action: 'start', flowType, params },
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<{ flowId: string }>>(message);
  }

  /**
   * 执行批量配置管理
   * @param operations 批量操作
   */
  async batchManageConfigs(operations: BatchConfigOperation[]): Promise<BaseResponse<any>> {
    return this.configAdapter.batchConfig(operations);
  }

  /**
   * 获取工作台概览
   */
  async getOverview(): Promise<BaseResponse<{
    totalConfigs: number;
    activeUsers: number;
    systemStatus: string;
    pendingTasks: number;
    recentActivity: any[];
  }>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.WORKBENCH_FLOW,
      payload: { action: 'overview' },
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<any>>(message);
  }

  /**
   * 搜索配置项
   * @param query 搜索关键词
   * @param filters 过滤条件
   */
  async searchConfigs(
    query: string,
    filters?: {
      group?: string;
      type?: string;
      modifiedSince?: Date;
    }
  ): Promise<BaseResponse<any>> {
    return this.configAdapter.queryConfig({
      keys: [`*${query}*`],
      group: filters?.group,
      includeDefault: true
    });
  }

  /**
   * 导出配置
   * @param format 导出格式
   * @param filters 过滤条件
   */
  async exportConfigs(
    format: 'json' | 'yaml' | 'env',
    filters?: Record<string, any>
  ): Promise<BaseResponse<{ data: string; filename: string }>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.CONFIG_BATCH,
      payload: { action: 'export', format, filters },
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<{ data: string; filename: string }>>(message);
  }

  /**
   * 导入配置
   * @param data 配置数据
   * @param format 导入格式
   * @param validate 是否验证
   */
  async importConfigs(
    data: string,
    format: 'json' | 'yaml' | 'env',
    validate: boolean = true
  ): Promise<BaseResponse<{ imported: number; errors: string[] }>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.CONFIG_BATCH,
      payload: { action: 'import', data, format, validate },
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<{ imported: number; errors: string[] }>>(message);
  }

  /**
   * 生成消息 ID
   */
  private generateMessageId(): string {
    return `workbench-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

export default WorkbenchHelper;
