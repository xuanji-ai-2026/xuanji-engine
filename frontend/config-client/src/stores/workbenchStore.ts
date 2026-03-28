import { create } from 'zustand'
import type { Task, SearchFilters, PaginatedResponse, PaginationParams, Notification, Statistics } from '@/types'

interface WorkbenchState {
  tasks: Task[]
  currentTask: Task | null
  notifications: Notification[]
  unreadCount: number
  statistics: Statistics | null
  loading: boolean
  total: number
  filters: SearchFilters
  pagination: PaginationParams

  fetchTasks: () => Promise<void>
  fetchTaskById: (id: string) => Promise<void>
  createTask: (task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => Promise<void>
  updateTask: (id: string, updates: Partial<Task>) => Promise<void>
  deleteTask: (id: string) => Promise<void>
  completeTask: (id: string) => Promise<void>
  fetchNotifications: () => Promise<void>
  markNotificationAsRead: (id: string) => Promise<void>
  markAllNotificationsAsRead: () => Promise<void>
  fetchStatistics: () => Promise<void>
  setFilters: (filters: SearchFilters) => void
  setPagination: (pagination: Partial<PaginationParams>) => void
  clearCurrentTask: () => void
}

export const useWorkbenchStore = create<WorkbenchState>((set, get) => ({
  tasks: [],
  currentTask: null,
  notifications: [],
  unreadCount: 0,
  statistics: null,
  loading: false,
  total: 0,
  filters: {},
  pagination: { page: 1, pageSize: 20 },

  fetchTasks: async () => {
    set({ loading: true })
    try {
      const { filters, pagination } = get()
      const queryParams = new URLSearchParams({
        page: pagination.page.toString(),
        pageSize: pagination.pageSize.toString(),
        ...(filters.keyword && { keyword: filters.keyword }),
        ...(filters.status?.length && { status: filters.status.join(',') }),
        ...(filters.priority?.length && { priority: filters.priority.join(',') }),
      })

      const response = await fetch(`/api/tasks?${queryParams}`)
      const data: PaginatedResponse<Task> = await response.json()

      set({
        tasks: data.items,
        total: data.total,
        loading: false,
      })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch tasks:', error)
    }
  },

  fetchTaskById: async (id: string) => {
    set({ loading: true })
    try {
      const response = await fetch(`/api/tasks/${id}`)
      const data: Task = await response.json()

      set({
        currentTask: data,
        loading: false,
      })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch task:', error)
    }
  },

  createTask: async (task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(task),
      })

      if (response.ok) {
        await get().fetchTasks()
      }
    } catch (error) {
      console.error('Failed to create task:', error)
      throw error
    }
  },

  updateTask: async (id: string, updates: Partial<Task>) => {
    try {
      const response = await fetch(`/api/tasks/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
      })

      if (response.ok) {
        await get().fetchTasks()
      }
    } catch (error) {
      console.error('Failed to update task:', error)
      throw error
    }
  },

  deleteTask: async (id: string) => {
    try {
      const response = await fetch(`/api/tasks/${id}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        await get().fetchTasks()
      }
    } catch (error) {
      console.error('Failed to delete task:', error)
      throw error
    }
  },

  completeTask: async (id: string) => {
    try {
      const response = await fetch(`/api/tasks/${id}/complete`, {
        method: 'POST',
      })

      if (response.ok) {
        await get().fetchTasks()
      }
    } catch (error) {
      console.error('Failed to complete task:', error)
      throw error
    }
  },

  fetchNotifications: async () => {
    try {
      const response = await fetch('/api/notifications')
      const data: Notification[] = await response.json()

      set({
        notifications: data,
        unreadCount: data.filter((n) => !n.read).length,
      })
    } catch (error) {
      console.error('Failed to fetch notifications:', error)
    }
  },

  markNotificationAsRead: async (id: string) => {
    try {
      const response = await fetch(`/api/notifications/${id}/read`, {
        method: 'POST',
      })

      if (response.ok) {
        await get().fetchNotifications()
      }
    } catch (error) {
      console.error('Failed to mark notification as read:', error)
    }
  },

  markAllNotificationsAsRead: async () => {
    try {
      const response = await fetch('/api/notifications/read-all', {
        method: 'POST',
      })

      if (response.ok) {
        await get().fetchNotifications()
      }
    } catch (error) {
      console.error('Failed to mark all notifications as read:', error)
    }
  },

  fetchStatistics: async () => {
    try {
      const response = await fetch('/api/statistics')
      const data: Statistics = await response.json()

      set({ statistics: data })
    } catch (error) {
      console.error('Failed to fetch statistics:', error)
    }
  },

  setFilters: (filters: SearchFilters) => {
    set({ filters, pagination: { ...get().pagination, page: 1 } })
  },

  setPagination: (pagination: Partial<PaginationParams>) => {
    set({ pagination: { ...get().pagination, ...pagination } })
  },

  clearCurrentTask: () => {
    set({ currentTask: null })
  },
}))
