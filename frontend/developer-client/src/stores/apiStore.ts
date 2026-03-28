import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { ApiKey, CallStatistics, CallTrend, ApiDocument, DebugRequest } from '../types';
import { apiService } from '../services/api';

interface ApiState {
  apiKeys: ApiKey[];
  statistics: CallStatistics | null;
  trends: CallTrend[];
  documents: ApiDocument[];
  currentDocument: ApiDocument | null;
  debugHistory: DebugRequest[];
  loading: boolean;
  error: string | null;

  // Actions
  fetchApiKeys: () => Promise<void>;
  createApiKey: (data: { name: string; permissions: string[] }) => Promise<void>;
  updateApiKey: (id: string, data: Partial<ApiKey>) => Promise<void>;
  deleteApiKey: (id: string) => Promise<void>;
  revokeApiKey: (id: string) => Promise<void>;
  fetchStatistics: (period: string) => Promise<void>;
  fetchTrends: (period: string) => Promise<void>;
  fetchDocuments: () => Promise<void>;
  fetchDocument: (id: string) => Promise<void>;
  sendDebugRequest: (data: any) => Promise<void>;
  fetchDebugHistory: () => Promise<void>;
  clearError: () => void;
}

export const useApiStore = create<ApiState>()(
  persist(
    (set, get) => ({
      apiKeys: [],
      statistics: null,
      trends: [],
      documents: [],
      currentDocument: null,
      debugHistory: [],
      loading: false,
      error: null,

      fetchApiKeys: async () => {
        set({ loading: true, error: null });
        try {
          const response = await apiService.getApiKeys({ page: 1, pageSize: 100 });
          set({ apiKeys: response.data.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      createApiKey: async (data) => {
        set({ loading: true, error: null });
        try {
          await apiService.createApiKey(data);
          await get().fetchApiKeys();
          set({ loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      updateApiKey: async (id, data) => {
        set({ loading: true, error: null });
        try {
          await apiService.updateApiKey(id, data);
          await get().fetchApiKeys();
          set({ loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      deleteApiKey: async (id) => {
        set({ loading: true, error: null });
        try {
          await apiService.deleteApiKey(id);
          set((state) => ({ apiKeys: state.apiKeys.filter((k) => k.id !== id), loading: false }));
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      revokeApiKey: async (id) => {
        set({ loading: true, error: null });
        try {
          await apiService.revokeApiKey(id);
          await get().fetchApiKeys();
          set({ loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      fetchStatistics: async (period) => {
        set({ loading: true, error: null });
        try {
          const response = await apiService.getStatistics(period);
          set({ statistics: response.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      fetchTrends: async (period) => {
        set({ loading: true, error: null });
        try {
          const response = await apiService.getCallTrends(period);
          set({ trends: response.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      fetchDocuments: async () => {
        set({ loading: true, error: null });
        try {
          const response = await apiService.getApiDocuments();
          set({ documents: response.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      fetchDocument: async (id) => {
        set({ loading: true, error: null });
        try {
          const response = await apiService.getApiDocument(id);
          set({ currentDocument: response.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      sendDebugRequest: async (data) => {
        set({ loading: true, error: null });
        try {
          const response = await apiService.sendDebugRequest(data);
          set((state) => ({
            debugHistory: [response.data, ...state.debugHistory],
            loading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      fetchDebugHistory: async () => {
        set({ loading: true, error: null });
        try {
          const response = await apiService.getDebugHistory({ page: 1, pageSize: 50 });
          set({ debugHistory: response.data.data, loading: false });
        } catch (error: any) {
          set({ error: error.message, loading: false });
        }
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'api-storage',
      partialize: (state) => ({
        apiKeys: state.apiKeys,
        debugHistory: state.debugHistory,
      }),
    }
  )
);
