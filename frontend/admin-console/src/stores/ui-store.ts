import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { UIConfig } from '@/types'

interface UIState {
  config: UIConfig
  updateConfig: (config: Partial<UIConfig>) => void
  toggleSidebar: () => void
  setHeaderVisible: (visible: boolean) => void
}

const defaultConfig: UIConfig = {
  sidebar: {
    collapsed: false,
    width: 256,
    position: 'left',
  },
  header: {
    height: 64,
    visible: true,
  },
  animations: {
    enabled: true,
    duration: 300,
  },
}

export const useUIStore = create<UIState>()(
  persist(
    (set, get) => ({
      config: defaultConfig,
      updateConfig: (newConfig) =>
        set((state) => ({
          config: { ...state.config, ...newConfig },
        })),
      toggleSidebar: () =>
        set((state) => ({
          config: {
            ...state.config,
            sidebar: {
              ...state.config.sidebar,
              collapsed: !state.config.sidebar.collapsed,
            },
          },
        })),
      setHeaderVisible: (visible) =>
        set((state) => ({
          config: {
            ...state.config,
            header: { ...state.config.header, visible },
          },
        })),
    }),
    {
      name: 'ui-storage',
    }
  )
)
