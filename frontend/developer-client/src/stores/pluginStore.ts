import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  Plugin,
  PluginConfig,
  PluginTestResult,
  PluginTemplate,
  PluginLogEntry,
  CodeSnippet,
} from '../types';
import { pluginService } from '../services/plugin';

interface PluginState {
  plugins: Plugin[];
  currentPlugin: Plugin | null;
  templates: PluginTemplate[];
  snippets: CodeSnippet[];
  testResults: PluginTestResult[];
  logs: PluginLogEntry[];
  loading: boolean;
  error: string | null;

  // Actions
  fetchPlugins: () => Promise<void>;
  fetchPlugin: (id: string) => Promise<void>;
  createPlugin: (data: Partial<Plugin>) => Promise<void>;
  updatePlugin: (id: string, data: Partial<Plugin>) => Promise<void>;
  deletePlugin: (id: string) => Promise<void>;
  submitForReview: (id: string) => Promise<void>;
  fetchTemplates: () => Promise<void>;
  fetchSnippets: () => Promise<void>;
  createSnippet: (data: Partial<CodeSnippet>) => Promise<void>;
  runTest: (pluginId: string, testType: string) => Promise<void>;
  fetchLogs: (pluginId: string) => Promise<void>;
  clearError: () => void;
}

export const usePluginStore = create<PluginState>()(
  persist(
    (set, get) => ({
      plugins: [],
      currentPlugin: null,
      templates: [],
      snippets: [],
      testResults: [],
      logs: [],
      loading: false,
      error: null,

      fetchPlugins: async () => {
        set({ loading: true, error: null });
        try {
          const response = await pluginService.getPlugins({ page: 1, pageSize: 100 });
          set({ plugins: response.data.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      fetchPlugin: async (id) => {
        set({ loading: true, error: null });
        try {
          const response = await pluginService.getPlugin(id);
          set({ currentPlugin: response.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      createPlugin: async (data) => {
        set({ loading: true, error: null });
        try {
          await pluginService.createPlugin(data);
          await get().fetchPlugins();
          set({ loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      updatePlugin: async (id, data) => {
        set({ loading: true, error: null });
        try {
          await pluginService.updatePlugin(id, data);
          await get().fetchPlugins();
          set({ loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      deletePlugin: async (id) => {
        set({ loading: true, error: null });
        try {
          await pluginService.deletePlugin(id);
          set((state) => ({ plugins: state.plugins.filter((p) => p.id !== id), loading: false }));
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      submitForReview: async (id) => {
        set({ loading: true, error: null });
        try {
          await pluginService.submitForReview(id);
          await get().fetchPlugins();
          set({ loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      fetchTemplates: async () => {
        set({ loading: true, error: null });
        try {
          const response = await pluginService.getTemplates();
          set({ templates: response.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      fetchSnippets: async () => {
        set({ loading: true, error: null });
        try {
          const response = await pluginService.getCodeSnippets();
          set({ snippets: response.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      createSnippet: async (data) => {
        set({ loading: true, error: null });
        try {
          await pluginService.createCodeSnippet(data);
          await get().fetchSnippets();
          set({ loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      runTest: async (pluginId, testType) => {
        set({ loading: true, error: null });
        try {
          const response = await pluginService.runTest(pluginId, testType as any);
          set((state) => ({
            testResults: [response.data, ...state.testResults],
            loading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      fetchLogs: async (pluginId) => {
        set({ loading: true, error: null });
        try {
          const response = await pluginService.getPluginLogs(pluginId);
          set({ logs: response.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'plugin-storage',
      partialize: (state) => ({
        templates: state.templates,
        snippets: state.snippets,
      }),
    }
  )
);
