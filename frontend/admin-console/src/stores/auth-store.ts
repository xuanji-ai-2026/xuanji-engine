import { create } from 'zustand'
import type { User, UserFilters, UserStats } from '@/types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  login: (user: User, token: string) => void
  logout: () => void
  updateUser: (user: Partial<User>) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  login: (user, token) => {
    localStorage.setItem('auth_token', token)
    set({ user, isAuthenticated: true })
  },
  logout: () => {
    localStorage.removeItem('auth_token')
    set({ user: null, isAuthenticated: false })
  },
  updateUser: (userData) =>
    set((state) => ({
      user: state.user ? { ...state.user, ...userData } : null,
    })),
}))
