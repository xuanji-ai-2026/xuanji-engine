import { create } from 'zustand'
import type { ConfigRequest, SearchFilters, PaginatedResponse, PaginationParams, ProgressLog } from '@/types'

interface ConfigRequestState {
  requests: ConfigRequest[]
  currentRequest: ConfigRequest | null
  loading: boolean
  total: number
  filters: SearchFilters
  pagination: PaginationParams
  progressLogs: ProgressLog[]

  fetchRequests: () => Promise<void>
  fetchRequestById: (id: string) => Promise<void>
  createRequest: (request: Omit<ConfigRequest, 'id' | 'createdAt' | 'updatedAt'>) => Promise<void>
  updateRequest: (id: string, updates: Partial<ConfigRequest>) => Promise<void>
  deleteRequest: (id: string) => Promise<void>
  updateProgress: (id: string, progress: number, message: string) => Promise<void>
  fetchProgressLogs: (requestId: string) => Promise<void>
  setFilters: (filters: SearchFilters) => void
  setPagination: (pagination: Partial<PaginationParams>) => void
  clearCurrentRequest: () => void
}

export const useConfigRequestStore = create<ConfigRequestState>((set, get) => ({
  requests: [],
  currentRequest: null,
  loading: false,
  total: 0,
  filters: {},
  pagination: { page: 1, pageSize: 20 },
  progressLogs: [],

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

      const response = await fetch(`/api/config-requests?${queryParams}`)
      const data: PaginatedResponse<ConfigRequest> = await response.json()

      set({
        requests: data.items,
        total: data.total,
        loading: false,
      })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch config requests:', error)
    }
  },

  fetchRequestById: async (id: string) => {
    set({ loading: true })
    try {
      const response = await fetch(`/api/config-requests/${id}`)
      const data: ConfigRequest = await response.json()

      set({
        currentRequest: data,
        loading: false,
      })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch config request:', error)
    }
  },

  createRequest: async (request: Omit<ConfigRequest, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      const response = await fetch('/api/config-requests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      })

      if (response.ok) {
        await get().fetchRequests()
      }
    } catch (error) {
      console.error('Failed to create request:', error)
      throw error
    }
  },

  updateRequest: async (id: string, updates: Partial<ConfigRequest>) => {
    try {
      const response = await fetch(`/api/config-requests/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
      })

      if (response.ok) {
        await get().fetchRequests()
      }
    } catch (error) {
      console.error('Failed to update request:', error)
      throw error
    }
  },

  deleteRequest: async (id: string) => {
    try {
      const response = await fetch(`/api/config-requests/${id}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        await get().fetchRequests()
      }
    } catch (error) {
      console.error('Failed to delete request:', error)
      throw error
    }
  },

  updateProgress: async (id: string, progress: number, message: string) => {
    try {
      const response = await fetch(`/api/config-requests/${id}/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ progress, message }),
      })

      if (response.ok) {
        await get().fetchRequestById(id)
      }
    } catch (error) {
      console.error('Failed to update progress:', error)
      throw error
    }
  },

  fetchProgressLogs: async (requestId: string) => {
    try {
      const response = await fetch(`/api/config-requests/${requestId}/logs`)
      const data: ProgressLog[] = await response.json()

      set({ progressLogs: data })
    } catch (error) {
      console.error('Failed to fetch progress logs:', error)
    }
  },

  setFilters: (filters: SearchFilters) => {
    set({ filters, pagination: { ...get().pagination, page: 1 } })
  },

  setPagination: (pagination: Partial<PaginationParams>) => {
    set({ pagination: { ...get().pagination, ...pagination } })
  },

  clearCurrentRequest: () => {
    set({ currentRequest: null, progressLogs: [] })
  },
}))
