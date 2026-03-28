import { create } from 'zustand'
import type { AuthRequest, SearchFilters, PaginatedResponse, PaginationParams } from '@/types'

interface AuthRequestState {
  requests: AuthRequest[]
  currentRequest: AuthRequest | null
  loading: boolean
  total: number
  filters: SearchFilters
  pagination: PaginationParams

  fetchRequests: () => Promise<void>
  fetchRequestById: (id: string) => Promise<void>
  approveRequest: (id: string, comment?: string) => Promise<void>
  rejectRequest: (id: string, comment?: string) => Promise<void>
  setFilters: (filters: SearchFilters) => void
  setPagination: (pagination: Partial<PaginationParams>) => void
  clearCurrentRequest: () => void
}

export const useAuthRequestStore = create<AuthRequestState>((set, get) => ({
  requests: [],
  currentRequest: null,
  loading: false,
  total: 0,
  filters: {},
  pagination: { page: 1, pageSize: 20 },

  fetchRequests: async () => {
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

      const response = await fetch(`/api/auth-requests?${queryParams}`)
      const data: PaginatedResponse<AuthRequest> = await response.json()

      set({
        requests: data.items,
        total: data.total,
        loading: false,
      })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch auth requests:', error)
    }
  },

  fetchRequestById: async (id: string) => {
    set({ loading: true })
    try {
      const response = await fetch(`/api/auth-requests/${id}`)
      const data: AuthRequest = await response.json()

      set({
        currentRequest: data,
        loading: false,
      })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch auth request:', error)
    }
  },

  approveRequest: async (id: string, comment?: string) => {
    try {
      const response = await fetch(`/api/auth-requests/${id}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment }),
      })

      if (response.ok) {
        await get().fetchRequests()
      }
    } catch (error) {
      console.error('Failed to approve request:', error)
      throw error
    }
  },

  rejectRequest: async (id: string, comment?: string) => {
    try {
      const response = await fetch(`/api/auth-requests/${id}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment }),
      })

      if (response.ok) {
        await get().fetchRequests()
      }
    } catch (error) {
      console.error('Failed to reject request:', error)
      throw error
    }
  },

  setFilters: (filters: SearchFilters) => {
    set({ filters, pagination: { ...get().pagination, page: 1 } })
  },

  setPagination: (pagination: Partial<PaginationParams>) => {
    set({ pagination: { ...get().pagination, ...pagination } })
  },

  clearCurrentRequest: () => {
    set({ currentRequest: null })
  },
}))
