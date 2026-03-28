import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, Notification, ThemeConfig } from '../types';

interface AppState {
  user: User | null;
  notifications: Notification[];
  theme: ThemeConfig;
  sidebarOpen: boolean;

  // Actions
  setUser: (user: User | null) => void;
  addNotification: (notification: Omit<Notification, 'id' | 'createdAt'>) => void;
  markNotificationRead: (id: string) => void;
  clearNotifications: () => void;
  setTheme: (theme: Partial<ThemeConfig>) => void;
  toggleSidebar: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      user: null,
      notifications: [],
      theme: {
        mode: 'light',
        primaryColor: '#0ea5e9',
      },
      sidebarOpen: true,

      setUser: (user) => set({ user }),

      addNotification: (notification) =>
        set((state) => ({
          notifications: [
            {
              ...notification,
              id: Date.now().toString(),
              createdAt: new Date().toISOString(),
            },
            ...state.notifications,
          ],
        })),

      markNotificationRead: (id) =>
        set((state) => ({
          notifications: state.notifications.map((n) =>
            n.id === id ? { ...n, read: true } : n
          ),
        })),

      clearNotifications: () => set({ notifications: [] }),

      setTheme: (theme) =>
        set((state) => ({
          theme: { ...state.theme, ...theme },
        })),

      toggleSidebar: () =>
        set((state) => ({ sidebarOpen: !state.sidebarOpen })),
    }),
    {
      name: 'app-storage',
    }
  )
);
