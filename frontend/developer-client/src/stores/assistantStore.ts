import { create } from 'zustand';
import type {
  AssistantMessage,
  CodeGenerationResult,
  ErrorDiagnostic,
  OptimizationSuggestion,
} from '../types';
import { assistantService } from '../services/assistant';

interface AssistantState {
  messages: AssistantMessage[];
  codeResult: CodeGenerationResult | null;
  diagnostics: ErrorDiagnostic[];
  optimizations: OptimizationSuggestion[];
  loading: boolean;
  error: string | null;

  // Actions
  sendMessage: (message: string) => Promise<void>;
  generateCode: (description: string, language: string) => Promise<void>;
  diagnoseError: (error: string, code?: string, language?: string) => Promise<void>;
  getOptimizations: (code: string, language: string) => Promise<void>;
  clearMessages: () => void;
  clearError: () => void;
}

export const useAssistantStore = create<AssistantState>()((set, get) => ({
  messages: [],
  codeResult: null,
  diagnostics: [],
  optimizations: [],
  loading: false,
  error: null,

  sendMessage: async (message) => {
    set({ loading: true, error: null });
    try {
      const userMessage: AssistantMessage = {
        id: Date.now().toString(),
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      };
      set((state) => ({ messages: [...state.messages, userMessage] }));

      const response = await assistantService.sendMessage(message, get().messages);
      set((state) => ({ messages: [...state.messages, response.data], loading: false }));
    } catch (error: any) {
      set({ error: error.message, loading: false });
    }
  },

  generateCode: async (description, language) => {
    set({ loading: true, error: null });
    try {
      const response = await assistantService.generateCode({
        description,
        language,
      });
      set({ codeResult: response.data, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
    }
  },

  diagnoseError: async (error, code, language) => {
    set({ loading: true, error: null });
    try {
      const response = await assistantService.diagnoseError(error, code, language);
      set({ diagnostics: response.data, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
    }
  },

  getOptimizations: async (code, language) => {
    set({ loading: true, error: null });
    try {
      const response = await assistantService.getOptimizations(code, language);
      set({ optimizations: response.data, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
    }
  },

  clearMessages: () => set({ messages: [] }),
  clearError: () => set({ error: null }),
}));
