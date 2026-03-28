import { useEffect, useState } from 'react'
import { useAuthStore } from '@/stores/auth-store'
import type { User } from '@/types'

export function useAuth() {
  const { user, isAuthenticated, login, logout, updateUser } = useAuthStore()

  return {
    user,
    isAuthenticated,
    login,
    logout,
    updateUser,
  }
}

export function usePermission(user?: User) {
  const currentUser = useAuthStore((state) => state.user)
  const userData = user || currentUser

  const hasRole = (roles: string[]) => {
    if (!userData) return false
    return roles.includes(userData.role)
  }

  const isAdmin = hasRole(['admin'])
  const isManager = hasRole(['admin', 'manager'])
  const canEdit = isAdmin || isManager

  return {
    isAdmin,
    isManager,
    canEdit,
    hasRole,
  }
}

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(error)
    }
  }

  return [storedValue, setValue] as const
}

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}

export function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  })

  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      })
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return size
}

export function useBreakpoint() {
  const { width } = useWindowSize()

  return {
    isMobile: width < 640,
    isTablet: width >= 640 && width < 1024,
    isDesktop: width >= 1024,
  }
}
