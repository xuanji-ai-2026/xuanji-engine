import { create } from 'zustand'
import type { AssistantAlert, AssistantSuggestion } from '@/types'

interface AssistantState {
  alerts: AssistantAlert[]
  suggestions: AssistantSuggestion[]
  isActive: boolean
  addAlert: (alert: AssistantAlert) => void
  acknowledgeAlert: (id: string) => void
  clearAlerts: () => void
  addSuggestion: (suggestion: AssistantSuggestion) => void
  dismissSuggestion: (id: string) => void
  toggleActive: () => void
}

export const useAssistantStore = create<AssistantState>((set) => ({
  alerts: [],
  suggestions: [],
  isActive: true,
  addAlert: (alert) =>
    set((state) => ({
      alerts: [alert, ...state.alerts],
    })),
  acknowledgeAlert: (id) =>
    set((state) => ({
      alerts: state.alerts.map((alert) =>
        alert.id === id ? { ...alert, acknowledged: true } : alert
      ),
    })),
  clearAlerts: () => set({ alerts: [] }),
  addSuggestion: (suggestion) =>
    set((state) => ({
      suggestions: [suggestion, ...state.suggestions],
    })),
  dismissSuggestion: (id) =>
    set((state) => ({
      suggestions: state.suggestions.filter((s) => s.id !== id),
    })),
  toggleActive: () =>
    set((state) => ({ isActive: !state.isActive })),
}))
