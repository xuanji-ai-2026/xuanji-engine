import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Language } from '@/types';

interface ThemeState {
  theme: 'light' | 'dark' | 'auto';
  language: Language;
  fontSize: 'small' | 'medium' | 'large';
  sidebarCollapsed: boolean;

  setTheme: (theme: 'light' | 'dark' | 'auto') => void;
  setLanguage: (language: Language) => void;
  setFontSize: (size: 'small' | 'medium' | 'large') => void;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set) => ({
      theme: 'light',
      language: 'zh-CN',
      fontSize: 'medium',
      sidebarCollapsed: false,

      setTheme: (theme) => set({ theme }),

      setLanguage: (language) => set({ language }),

      setFontSize: (fontSize) => set({ fontSize }),

      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

      setSidebarCollapsed: (sidebarCollapsed) => set({ sidebarCollapsed }),
    }),
    {
      name: 'theme-storage',
    }
  )
);

// Get effective theme (considering 'auto' setting)
export function getEffectiveTheme(theme: 'light' | 'dark' | 'auto'): 'light' | 'dark' {
  if (theme === 'auto') {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  return theme;
}
