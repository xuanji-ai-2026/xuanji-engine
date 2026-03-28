import axios from 'axios';
import type {
  AssistantMessage,
  CodeGenerationRequest,
  CodeGenerationResult,
  ErrorDiagnostic,
  OptimizationSuggestion,
  ApiResponse,
} from '../types';

class AssistantService {
  private client = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
    timeout: 60000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // ============================================
  // 聊天对话
  // ============================================

  async sendMessage(message: string, history: AssistantMessage[]): Promise<ApiResponse<AssistantMessage>> {
    const response = await this.client.post('/assistant/chat', { message, history });
    return response.data;
  }

  // ============================================
  // 代码生成
  // ============================================

  async generateCode(request: CodeGenerationRequest): Promise<ApiResponse<CodeGenerationResult>> {
    const response = await this.client.post('/assistant/code/generate', request);
    return response.data;
  }

  async explainCode(code: string, language: string): Promise<ApiResponse<{ explanation: string }>> {
    const response = await this.client.post('/assistant/code/explain', { code, language });
    return response.data;
  }

  async refactorCode(code: string, language: string): Promise<ApiResponse<{ code: string; explanation: string }>> {
    const response = await this.client.post('/assistant/code/refactor', { code, language });
    return response.data;
  }

  async optimizeCode(code: string, language: string): Promise<ApiResponse<{ code: string; explanation: string }>> {
    const response = await this.client.post('/assistant/code/optimize', { code, language });
    return response.data;
  }

  // ============================================
  // 错误诊断
  // ============================================

  async diagnoseError(error: string, code?: string, language?: string): Promise<ApiResponse<ErrorDiagnostic[]>> {
    const response = await this.client.post('/assistant/error/diagnose', { error, code, language });
    return response.data;
  }

  async getFixSuggestion(diagnosticId: string): Promise<ApiResponse<{ suggestion: string; code: string }>> {
    const response = await this.client.get(`/assistant/error/${diagnosticId}/fix`);
    return response.data;
  }

  // ============================================
  // 优化建议
  // ============================================

  async getOptimizations(code: string, language: string): Promise<ApiResponse<OptimizationSuggestion[]>> {
    const response = await this.client.post('/assistant/optimize', { code, language });
    return response.data;
  }

  async getBestPractices(language: string): Promise<ApiResponse<{ title: string; description: string; code: string }[]>> {
    const response = await this.client.get('/assistant/best-practices', { params: { language } });
    return response.data;
  }
}

export const assistantService = new AssistantService();
