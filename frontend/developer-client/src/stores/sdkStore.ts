import { create } from 'zustand';
import type { Sdk } from '../types';
import { sdkService } from '../services/sdk';

interface SdkState {
  sdks: Sdk[];
  currentSdk: Sdk | null;
  loading: boolean;
  error: string | null;

  // Actions
  fetchSdks: () => Promise<void>;
  fetchSdk: (id: string) => Promise<void>;
  downloadSdk: (id: string) => Promise<void>;
  clearError: () => void;
}

export const useSdkStore = create<SdkState>()((set, get) => ({
  sdks: [],
  currentSdk: null,
  loading: false,
  error: null,

  fetchSdks: async () => {
    set({ loading: true, error: null });
    try {
      const response = await sdkService.getSdks();
      set({ sdks: response.data, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
    }
  },

  fetchSdk: async (id) => {
    set({ loading: true, error: null });
    try {
      const response = await sdkService.getSdk(id);
      set({ currentSdk: response.data, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
    }
  },

  downloadSdk: async (id) => {
    set({ loading: true, error: null });
    try {
      const blob = await sdkService.downloadSdk(id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `sdk-${id}.zip`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      set({ loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
    }
  },

  clearError: () => set({ error: null }),
}));
