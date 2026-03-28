import apiService from './api';
import type {
  Staff,
  AddStaffRequest,
  UpdateStaffRequest,
  Role,
  CreateRoleRequest,
  UpdateRoleRequest,
  Permission,
  PaginationRequest,
  PaginationResponse,
} from '@/types';

class AuthorizationService {
  // 工作人员管理

  // 获取工作人员列表
  async getStaffList(
    params: PaginationRequest
  ): Promise<PaginationResponse<Staff>> {
    const response = await apiService.get<PaginationResponse<Staff>>(
      '/authorization/staff',
      { params }
    );
    return response.data as PaginationResponse<Staff>;
  }

  // 添加工作人员
  async addStaff(data: AddStaffRequest): Promise<Staff> {
    const response = await apiService.post<Staff>('/authorization/staff', data);
    return response.data as Staff;
  }

  // 更新工作人员
  async updateStaff(id: string, data: UpdateStaffRequest): Promise<Staff> {
    const response = await apiService.patch<Staff>(
      `/authorization/staff/${id}`,
      data
    );
    return response.data as Staff;
  }

  // 删除工作人员
  async deleteStaff(id: string): Promise<void> {
    await apiService.delete(`/authorization/staff/${id}`);
  }

  // 角色管理

  // 获取角色列表
  async getRoleList(
    params?: PaginationRequest
  ): Promise<PaginationResponse<Role>> {
    const response = await apiService.get<PaginationResponse<Role>>(
      '/authorization/roles',
      { params }
    );
    return response.data as PaginationResponse<Role>;
  }

  // 获取单个角色
  async getRole(id: string): Promise<Role> {
    const response = await apiService.get<Role>(`/authorization/roles/${id}`);
    return response.data as Role;
  }

  // 创建角色
  async createRole(data: CreateRoleRequest): Promise<Role> {
    const response = await apiService.post<Role>('/authorization/roles', data);
    return response.data as Role;
  }

  // 更新角色
  async updateRole(id: string, data: UpdateRoleRequest): Promise<Role> {
    const response = await apiService.patch<Role>(
      `/authorization/roles/${id}`,
      data
    );
    return response.data as Role;
  }

  // 删除角色
  async deleteRole(id: string): Promise<void> {
    await apiService.delete(`/authorization/roles/${id}`);
  }

  // 权限管理

  // 获取权限列表
  async getPermissionList(): Promise<Permission[]> {
    const response = await apiService.get<Permission[]>('/authorization/permissions');
    return response.data as Permission[];
  }

  // 检查权限
  async checkPermission(module: string, resource: string, action: string): Promise<boolean> {
    const response = await apiService.post<{ allowed: boolean }>('/authorization/check', {
      module,
      resource,
      action,
    });
    return (response.data as { allowed: boolean }).allowed;
  }

  // 获取用户权限
  async getUserPermissions(userId: string): Promise<string[]> {
    const response = await apiService.get<string[]>(`/authorization/users/${userId}/permissions`);
    return response.data as string[];
  }
}

export const authorizationService = new AuthorizationService();
export default authorizationService;
