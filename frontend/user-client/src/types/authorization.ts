// 工作人员相关类型
export interface Staff {
  id: string;
  userId: string;
  username: string;
  email: string;
  avatar?: string;
  role: string;
  permissions: string[];
  status: 'active' | 'inactive' | 'suspended';
  createdAt: string;
  updatedAt: string;
  lastLoginAt?: string;
}

// 添加工作人员请求
export interface AddStaffRequest {
  email: string;
  role: string;
  permissions: string[];
}

// 更新工作人员请求
export interface UpdateStaffRequest {
  role?: string;
  permissions?: string[];
  status?: 'active' | 'inactive' | 'suspended';
}

// 角色相关类型
export interface Role {
  id: string;
  name: string;
  displayName: string;
  description?: string;
  permissions: string[];
  isSystem: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface CreateRoleRequest {
  name: string;
  displayName: string;
  description?: string;
  permissions: string[];
}

export interface UpdateRoleRequest {
  displayName?: string;
  description?: string;
  permissions?: string[];
}

// 权限相关类型
export interface Permission {
  id: string;
  code: string;
  displayName: string;
  description?: string;
  module: string;
  resource: string;
  action: string;
}

// 权限模块
export type PermissionModule =
  | 'user'
  | 'staff'
  | 'permission'
  | 'role'
  | 'digital-human'
  | 'chat'
  | 'plugin'
  | 'billing'
  | 'config'
  | 'assistant';

// 权限操作
export type PermissionAction = 'read' | 'write' | 'delete' | 'manage';

export interface PermissionCheck {
  module: PermissionModule;
  resource: string;
  action: PermissionAction;
}
