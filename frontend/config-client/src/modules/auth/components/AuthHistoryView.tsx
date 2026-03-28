import React, { useEffect, useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Badge } from '@/components/Badge'
import { Input } from '@/components/Input'
import { cn } from '@/utils'
import { Search, Filter, Download, Clock, CheckCircle, XCircle, RotateCcw } from 'lucide-react'
import type { AuthHistory, SearchFilters } from '@/types'

export const AuthHistoryView: React.FC = () => {
  const [history, setHistory] = useState<AuthHistory[]>([])
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState<SearchFilters>({})
  const [searchKeyword, setSearchKeyword] = useState('')

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    setLoading(true)
    try {
      const queryParams = new URLSearchParams({
        ...(filters.keyword && { keyword: filters.keyword }),
        ...(filters.dateRange?.start && {
          startDate: filters.dateRange.start,
        }),
        ...(filters.dateRange?.end && { endDate: filters.dateRange.end }),
      })

      const response = await fetch(`/api/auth-history?${queryParams}`)
      const data: AuthHistory[] = await response.json()
      setHistory(data)
    } catch (error) {
      console.error('Failed to fetch auth history:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = () => {
    setFilters({ ...filters, keyword: searchKeyword })
    fetchHistory()
  }

  const handleExport = async () => {
    try {
      const response = await fetch('/api/auth-history/export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filters }),
      })
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `auth-history-${new Date().toISOString().split('T')[0]}.xlsx`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Export failed:', error)
    }
  }

  const getActionIcon = (action: AuthHistory['action']) => {
    switch (action) {
      case 'approved':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'rejected':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'processing':
        return <Clock className="w-5 h-5 text-blue-500" />
      default:
        return <RotateCcw className="w-5 h-5 text-gray-500" />
    }
  }

  const getActionLabel = (action: AuthHistory['action']) => {
    const labels: Record<AuthHistory['action'], string> = {
      created: '创建',
      approved: '通过',
      rejected: '驳回',
      processing: '处理中',
      cancelled: '取消',
    }
    return labels[action]
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, 'primary' | 'success' | 'danger' | 'warning'> = {
      pending: 'warning',
      approved: 'success',
      rejected: 'danger',
      processing: 'primary',
    }
    return (
      <Badge variant={variants[status] || 'primary'} size="sm">
        {status}
      </Badge>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">认证历史记录</h1>
          <p className="mt-1 text-sm text-gray-600">
            查看所有认证请求的处理历史
          </p>
        </div>
        <Button onClick={handleExport} icon={<Download className="w-4 h-4" />}>
          导出数据
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <Input
              placeholder="搜索用户、请求类型..."
              value={searchKeyword}
              onChange={setSearchKeyword}
              icon={<Search className="w-4 h-4" />}
            />
          </div>
          <Button onClick={handleSearch}>搜索</Button>
        </div>
      </Card>

      {/* History List */}
      <Card>
        {loading ? (
          <div className="py-12 text-center text-gray-500">加载中...</div>
        ) : history.length === 0 ? (
          <div className="py-12 text-center text-gray-500">暂无历史记录</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    请求ID
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    用户
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    操作
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    状态
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    操作人
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    时间
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    备注
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {history.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-900">
                      {item.requestId}
                    </td>
                    <td className="px-4 py-3">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {item.userName}
                        </div>
                        <div className="text-xs text-gray-500">{item.userId}</div>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        {getActionIcon(item.action)}
                        <span className="text-sm text-gray-900">
                          {getActionLabel(item.action)}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      {getStatusBadge(item.status)}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900">
                      {item.actionByName}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {new Date(item.actionAt).toLocaleString('zh-CN')}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {item.comment || '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  )
}

export default AuthHistoryView
