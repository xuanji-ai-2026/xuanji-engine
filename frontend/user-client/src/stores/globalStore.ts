import { create } from 'zustand';
import type { Notification } from '@/types';

interface GlobalState {
  notifications: Notification[];
  isOnline: boolean;
  isLoading: boolean;

  addNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void;
  removeNotification: (id: string) => void;
  markAsRead: (id: string) => void;
  clearNotifications: () => void;
  setOnlineStatus: (isOnline: boolean) => void;
  setLoading: (isLoading: boolean) => void;
}

export const useGlobalStore = create<GlobalState>((set) => ({
  notifications: [],
  isOnline: true,
  isLoading: false,

  addNotification: (notification) => {
    const newNotification: Notification = {
      ...notification,
      id: `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      read: false,
    };
    set((state) => ({
      notifications: [newNotification, ...state.notifications],
    }));

    // Auto-remove after 5 seconds for success messages
    if (notification.type === 'success') {
      setTimeout(() => {
        set((state) => ({
          notifications: state.notifications.filter((n) => n.id !== newNotification.id),
        }));
      }, 5000);
    }
  },

  removeNotification: (id) => {
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    }));
  },

  markAsRead: (id) => {
    set((state) => ({
      notifications: state.notifications.map((n) =>
        n.id === id ? { ...n, read: true } : n
      ),
    }));
  },

  clearNotifications: () => {
    set({ notifications: [] });
  },

  setOnlineStatus: (isOnline) => {
    set({ isOnline });
  },

  setLoading: (isLoading) => {
    set({ isLoading });
  },
}));
