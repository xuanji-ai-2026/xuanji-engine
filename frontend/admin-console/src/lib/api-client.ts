import axios, { type AxiosInstance, type AxiosError } from 'axios'
import toast from 'react-hot-toast'
import type { ApiResponse } from '@/types'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: '/api',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private setupInterceptors(): void {
    // 请求拦截器
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // 响应拦截器
    this.client.interceptors.response.use(
      (response) => {
        return response.data
      },
      (error: AxiosError) => {
        const message = this.getErrorMessage(error)
        toast.error(message)

        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token')
          window.location.href = '/login'
        }

        return Promise.reject(error)
      }
    )
  }

  private getErrorMessage(error: AxiosError): string {
    if (error.response) {
      const data = error.response.data as { message?: string }
      return data?.message || '请求失败'
    }
    if (error.request) {
      return '网络错误，请检查连接'
    }
    return error.message || '未知错误'
  }

  async get<T>(url: string, params?: Record<string, unknown>): Promise<T> {
    return this.client.get(url, { params })
  }

  async post<T>(url: string, data?: unknown): Promise<T> {
    return this.client.post(url, data)
  }

  async put<T>(url: string, data?: unknown): Promise<T> {
    return this.client.put(url, data)
  }

  async patch<T>(url: string, data?: unknown): Promise<T> {
    return this.client.patch(url, data)
  }

  async delete<T>(url: string): Promise<T> {
    return this.client.delete(url)
  }
}

export const apiClient = new ApiClient()
