/**
 * 小微适配层 - 用户管理协助
 * 版本: v1.0.0
 * 描述: 用户信息查询、用户配置建议、批量用户操作
 */

import {
  XiaoweiConfig,
  MessageType,
  Message,
  BaseResponse,
  UserQueryParams,
  UserInfo,
  UserConfigureParams,
  BatchUserOperation,
  Pagination,
  Sort
} from '../types';
import { ConfigAdapter } from './ConfigAdapter';

export class UserHelper {
  private configAdapter: ConfigAdapter;

  constructor(configAdapter: ConfigAdapter) {
    this.configAdapter = configAdapter;
  }

  /**
   * 查询用户信息
   */
  async queryUsers(params: UserQueryParams): Promise<BaseResponse<{
    users: UserInfo[];
    total: number;
    page: number;
    pageSize: number;
  }>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.USER_QUERY,
      payload: params,
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<any>>(message);
  }

  /**
   * 根据用户 ID 获取用户信息
   */
  async getUserById(userId: string): Promise<BaseResponse<UserInfo>> {
    return this.queryUsers({
      filters: { username: userId } as any,
      pagination: { page: 1, pageSize: 1 }
    }).then(response => {
      if (response.data && response.data.users.length > 0) {
        return {
          status: response.status,
          data: response.data.users[0],
          timestamp: response.timestamp
        } as BaseResponse<UserInfo>;
      }
      return {
        status: 'error',
        error: 'User not found',
        timestamp: Date.now()
      };
    });
  }

  /**
   * 搜索用户
   */
  async searchUsers(query: string, filters?: {
    role?: string;
    department?: string;
    status?: 'active' | ' 'inactive' | 'suspended';
  }): Promise<BaseResponse<UserInfo[]>> {
    const params: UserQueryParams = {
      filters: {
        username: `*${query}*`,
        ...filters
      },
      pagination: { page: 1, pageSize: 20 }
    };

    return this.queryUsers(params).then(response => ({
      status: response.status,
      data: response.data?.users || [],
      timestamp: response.timestamp
    }));
  }

  /**
   * 配置用户
   */
  async configureUser(params: UserConfigureParams): Promise<BaseResponse<UserInfo>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.USER_CONFIGURE,
      payload: params,
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<UserInfo>>(message);
  }

  /**
   * 批量用户操作
   */
  async batchUserOperations(operations: BatchUserOperation[]): Promise<BaseResponse<{
    successful: number;
    failed: number;
    errors: Array<{ operation: BatchUserOperation; error: string }>;
  }>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.USER_BATCH,
      payload: { operations },
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<any>>(message);
  }

  /**
   * 创建用户
   */
  async createUser(userData: Partial<UserInfo> & { password?: string }): Promise<BaseResponse<UserInfo>> {
    return this.batchUserOperations([{
      type: 'create',
      userData
    }]).then(response => {
      if (response.data?.successful === 1) {
        return {
          status: 'success',
          data: userData as UserInfo,
          timestamp: response.timestamp
        };
      }
      return {
        status: 'error',
        error: response.data?.errors?.[0]?.error || 'Failed to create user',
        timestamp: response.timestamp
      };
    });
  }

  /**
   * 更新用户
   */
  async updateUser(userId: string, updates: Partial<UserInfo>): Promise<BaseResponse<UserInfo>> {
    return this.configureUser({
      userId,
      updates
    });
  }

  /**
   * 删除用户
   */
  async deleteUser(userId: string): Promise<BaseResponse<{ success: boolean }>> {
    return this.batchUserOperations([{
      type: 'delete',
      userId
    }]).then(response => ({
      status: response.data?.successful === 1 ? 'success' : 'error',
      data: { success: response.data?.successful === 1 },
      error: response.data?.errors?.[0]?.error,
      timestamp: response.timestamp
    }));
  }

  /**
   * 激活用户
   */
  async activateUser(userId: string): Promise<BaseResponse<{ success: boolean }>> {
    return this.batchUserOperations([{
      type: 'activate',
      userId
    }]).then(response => ({
      status: response.data?.successful === 1 ? 'success' : 'error',
      data: { success: response.data?.successful === 1 },
      error: response.data?.errors?.[0]?.error,
      timestamp: response.timestamp
    }));
  }

  /**
   * 停用用户
   */
  async deactivateUser(userId: string): Promise<BaseResponse<{ success: boolean }>> {
    return this.batchUserOperations([{
      type: 'deactivate',
      userId
    }]).then(response => ({
      status: response.data?.successful === 1 ? 'success' : 'error',
      data: { success: response.data?.successful === 1 },
      error: response.data?.errors?.[0]?.error,
      timestamp: response.timestamp
    }));
  }

  /**
   * 批量激活用户
   */
  async batchActivate(filter: {
    role?: string;
    department?: string;
    status?: 'inactive' | 'suspended';
  }): Promise<BaseResponse<{ activated: number }>> {
    return this.batchUserOperations([{
      type: 'activate',
      filter
    }]).then(response => ({
      status: 'success',
      data: { activated: response.data?.successful || 0 },
      timestamp: response.timestamp
    }));
  }

  /**
   * 获取用户统计信息
   */
  async getUserStatistics(): Promise<BaseResponse<{
    total: number;
    active: number;
    inactive: number;
    suspended: number;
    byRole: Record<string, number>;
    byDepartment: Record<string, number>;
  }>> {
    const message: Message = {
      id: this.generateMessageId(),
      type: MessageType.USER_QUERY,
      payload: { action: 'statistics' },
      timestamp: Date.now()
    };

    return this.configAdapter['sendMessage']<BaseResponse<any>>(message);
  }

  /**
   * 生成消息 ID
   */
  private generateMessageId(): string {
    return `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

export default UserHelper;
