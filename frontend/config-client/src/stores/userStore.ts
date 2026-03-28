import { create } from 'zustand'
import type { User, SearchFilters, PaginatedResponse, PaginationParams } from '@/types'

interface UserManagementState {
  users: User[]
  currentUser: User | null
  loading: boolean
  total: number
  filters: SearchFilters
  pagination: PaginationParams

  fetchUsers: () => Promise<void>
  fetchUserById: (id: string) => Promise<void>
  createUser: (user: Omit<User, 'id' | 'createdAt'>) => Promise<void>
  updateUser: (id: string, updates: Partial<User>) => Promise<void>
  deleteUser: (id: string) => Promise<void>
  activateUser: (id: string) => Promise<void>
  deactivateUser: (id: string) => Promise<void>
  resetPassword: (id: string, newPassword: string) => Promise<void>
  setFilters: (filters: SearchFilters) => void
  setPagination: (pagination: Partial<PaginationParams>) => void
  clearCurrentUser: () => void
}

export const useUserStore = create<UserManagementState>((set, get) => ({
  users: [],
  currentUser: null,
  loading: false,
  total: 0,
  filters: {},
  pagination: { page: 1, pageSize: 20 },

  fetchUsers: async () => {
    set({ loading: true })
    try {
      const { filters, pagination } = get()
      const queryParams = new URLSearchParams({
        page: pagination.page.toString(),
        pageSize: pagination.pageSize.toString(),
        ...(filters.keyword && { keyword: filters.keyword }),
        ...(filters.status?.length && { status: filters.status.join(',') }),
        ...(filters.department && { department: filters.department }),
      })

      const response = await fetch(`/api/users?${queryParams}`)
      const data: PaginatedResponse<User> = await response.json()

      set({
        users: data.items,
        total: data.total,
        loading: false,
      })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch users:', error)
    }
  },

  fetchUserById: async (id: string) => {
    set({ loading: true })
    try {
      const response = await fetch(`/api/users/${id}`)
      const data: User = await response.json()

      set({
        currentUser: data,
        loading: false,
      })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch user:', error)
    }
  },

  createUser: async (user: Omit<User, 'id' | 'createdAt'>) => {
    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user),
      })

      if (response.ok) {
        await get().fetchUsers()
      }
    } catch (error) {
      console.error('Failed to create user:', error)
      throw error
    }
  },

  updateUser: async (id: string, updates: Partial<User>) => {
    try {
      const response = await fetch(`/api/users/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
      })

      if (response.ok) {
        await get().fetchUsers()
        if (get().currentUser?.id === id) {
          await get().fetchUserById(id)
        }
      }
    } catch (error) {
      console.error('Failed to update user:', error)
      throw error
    }
  },

  deleteUser: async (id: string) => {
    try {
      const response = await fetch(`/api/users/${id}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        await get().fetchUsers()
        if (get().currentUser?.id === id) {
          set({ currentUser: null })
        }
      }
    } catch (error) {
      console.error('Failed to delete user:', error)
      throw error
    }
  },

  activateUser: async (id: string) => {
    try {
      const response = await fetch(`/api/users/${id}/activate`, {
        method: 'POST',
      })

      if (response.ok) {
        await get().fetchUsers()
      }
    } catch (error) {
      console.error('Failed to activate user:', error)
      throw error
    }
  },

  deactivateUser: async (id: string) => {
    try {
      const response = await fetch(`/api/users/${id}/deactivate`, {
        method: 'POST',
      })

      if (response.ok) {
        await get().fetchUsers()
      }
    } catch (error) {
      console.error('Failed to deactivate user:', error)
      throw error
    }
  },

  resetPassword: async (id: string, newPassword: string) => {
    try {
      const response = await fetch(`/api/users/${id}/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: newPassword }),
      })

      if (!response.ok) {
        throw new Error('Failed to reset password')
      }
    } catch (error) {
      console.error('Failed to reset password:', error)
      throw error
    }
  },

  setFilters: (filters: SearchFilters) => {
    set({ filters, pagination: { ...get().pagination, page: 1 } })
  },

  setPagination: (pagination: Partial<PaginationParams>) => {
    set({ pagination: { ...get().pagination, ...pagination } })
  },

  clearCurrentUser: () => {
    set({ currentUser: null })
  },
}))
