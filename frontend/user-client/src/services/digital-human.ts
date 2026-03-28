import apiService from './api';
import type {
  DigitalHuman,
  CreateDigitalHumanRequest,
  UpdateDigitalHumanRequest,
  DigitalHumanTemplate,
  PaginationRequest,
  PaginationResponse,
} from '@/types';

class DigitalHumanService {
  // 数字人管理

  // 获取数字人列表
  async getDigitalHumanList(
    params: PaginationRequest
  ): Promise<PaginationResponse<DigitalHuman>> {
    const response = await apiService.get<PaginationResponse<DigitalHuman>>(
      '/digital-humans',
      { params }
    );
    return response.data as PaginationResponse<DigitalHuman>;
  }

  // 获取单个数字人
  async getDigitalHuman(id: string): Promise<DigitalHuman> {
    const response = await apiService.get<DigitalHuman>(`/digital-humans/${id}`);
    return response.data as DigitalHuman;
  }

  // 创建数字人
  async createDigitalHuman(data: CreateDigitalHumanRequest): Promise<DigitalHuman> {
    const response = await apiService.post<DigitalHuman>('/digital-humans', data);
    return response.data as DigitalHuman;
  }

  // 更新数字人
  async updateDigitalHuman(
    id: string,
    data: UpdateDigitalHumanRequest
  ): Promise<DigitalHuman> {
    const response = await apiService.patch<DigitalHuman>(
      `/digital-humans/${id}`,
      data
    );
    return response.data as DigitalHuman;
  }

  // 删除数字人
  async deleteDigitalHuman(id: string): Promise<void> {
    await apiService.delete(`/digital-humans/${id}`);
  }

  // 启动数字人
  async startDigitalHuman(id: string): Promise<void> {
    await apiService.post(`/digital-humans/${id}/start`);
  }

  // 停止数字人
  async stopDigitalHuman(id: string): Promise<void> {
    await apiService.post(`/digital-humans/${id}/stop`);
  }

  // 克隆数字人
  async cloneDigitalHuman(id: string, name: string): Promise<DigitalHuman> {
    const response = await apiService.post<DigitalHuman>(
      `/digital-humans/${id}/clone`,
      { name }
    );
    return response.data as DigitalHuman;
  }

  // 数字人模板

  // 获取模板列表
  async getTemplateList(params?: PaginationRequest): Promise<PaginationResponse<DigitalHumanTemplate>> {
    const response = await apiService.get<PaginationResponse<DigitalHumanTemplate>>(
      '/digital-humans/templates',
      { params }
    );
    return response.data as PaginationResponse<DigitalHumanTemplate>;
  }

  // 获取单个模板
  async getTemplate(id: string): Promise<DigitalHumanTemplate> {
    const response = await apiService.get<DigitalHumanTemplate>(
      `/digital-humans/templates/${id}`
    );
    return response.data as DigitalHumanTemplate;
  }

  // 使用模板创建数字人
  async createFromTemplate(
    templateId: string,
    name: string
  ): Promise<DigitalHuman> {
    const response = await apiService.post<DigitalHuman>(
      `/digital-humans/templates/${templateId}/create`,
      { name }
    );
    return response.data as DigitalHuman;
  }

  // 上传数字人头像
  async uploadAvatar(file: File, onProgress?: (progress: number) => void): Promise<string> {
    const response = await apiService.upload<{ url: string }>(
      '/digital-humans/upload-avatar',
      file,
      onProgress
    );
    return (response.data as { url: string }).url;
  }
}

export const digitalHumanService = new DigitalHumanService();
export default digitalHumanService;
