// 工具函数

// 格式化日期
export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 格式化时间
export function formatTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 格式化日期时间
export function formatDateTime(date: Date | string): string {
  return formatDate(date) + ' ' + formatTime(date)
}

// 格式化数字
export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

// 格式化字节
export function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 随机ID
export function randomId(): string {
  return Math.random().toString(36).substring(2, 15)
}

// 延迟函数
export function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

// 防抖函数
export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | null = null
  return function(...args: Parameters<T>) {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func.apply(this, args), wait)
  }
}

// 节流函数
export function throttle<T extends (...args: unknown[]) => unknown>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean
  return function(...args: Parameters<T>) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

// 深拷贝
export function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj))
}

// 判断对象是否为空
export function isEmpty(obj: unknown): boolean {
  if (obj === null || obj === undefined) return true
  if (typeof obj === 'string') return obj.length === 0
  if (Array.isArray(obj)) return obj.length === 0
  if (typeof obj === 'object') return Object.keys(obj).length === 0
  return false
}

// 首字母大写
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1)
}

// 随机颜色
export function randomColor(): string {
  const colors = [
    '#667eea', '#764ba2', '#06b6d4', '#8b5cf6', 
    '#a855f7', '#c084fc', '#d946ef', '#f97316'
  ]
  return colors[Math.floor(Math.random() * colors.length)]
}

// 获取URL参数
export function getUrlParam(key: string): string | null {
  const params = new URLSearchParams(window.location.search)
  return params.get(key)
}

// 设置URL参数
export function setUrlParam(key: string, value: string): void {
  const params = new URLSearchParams(window.location.search)
  params.set(key, value)
  window.history.pushState({}, '', '?' + params.toString())
}

// 复制到剪贴板
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    return false
  }
}

// 下载文件
export function downloadFile(content: string, filename: string, type: string = 'text/plain'): void {
  const blob = new Blob([content], { type })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

// 本地存储
export const storage = {
  get: (key: string): unknown => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : null
    } catch {
      return null
    }
  },
  set: (key: string, value: unknown): void => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (e) {
      console.error('Storage error:', e)
    }
  },
  remove: (key: string): void => {
    localStorage.removeItem(key)
  },
  clear: (): void => {
    localStorage.clear()
  }
}
