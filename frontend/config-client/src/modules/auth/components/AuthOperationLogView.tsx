import React, { useEffect, useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Input } from '@/components/Input'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { Search, Clock, User, Activity, Filter } from 'lucide-react'
import type { AuthOperationLog } from '@/types'

export const AuthOperationLogView: React.FC = () => {
  const [logs, setLogs] = useState<AuthOperationLog[]>([])
  const [loading, setLoading] = useState(false)
  const [keyword, setKeyword] = useState('')
  const [selectedOperation, setSelectedOperation] = useState<string>('')
  const [selectedUser, setSelectedUser] = useState<string>('')

  useEffect(() => {
    fetchLogs()
  }, [keyword, selectedOperation, selectedUser])

  const fetchLogs = async () => {
    setLoading(true)
    try {
      const queryParams = new URLSearchParams({
        ...(keyword && { keyword }),
        ...(selectedOperation && { operation: selectedOperation }),
        ...(selectedUser && { user: selectedUser }),
      })

      const response = await fetch(`/api/auth-logs?${queryParams}`)
      const data: AuthOperationLog[] = await response.json()
      setLogs(data)
    } catch (error) {
      console.error('Failed to fetch logs:', error)
    } finally {
      setLoading(false)
    }
  }

  const operations = ['created', 'approved', 'rejected', 'processing', 'cancelled', 'viewed']

  const getOperationBadge = (operation: string) => {
    const variants: Record<string, 'primary' | 'success' | 'danger' | 'warning'> = {
      created: 'primary',
      approved: 'success',
      rejected: 'danger',
      processing: 'warning',
      cancelled: 'danger',
      viewed: 'primary',
    }
    const labels: Record<string, string> = {
      created: '创建',
      approved: '通过',
      rejected: '驳回',
      processing: '处理',
      cancelled: '取消',
      viewed: '查看',
    }
    return (
      <Badge variant={variants[operation] || 'primary'} size="sm">
        {labels[operation] || operation}
      </Badge>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">认证操作日志</h1>
        <p className="mt-1 text-sm text-gray-600">
          查看所有认证相关操作的记录
        </p>
      </div>

      {/* Filters */}
      <Card className="p-6">
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <Input
              placeholder="搜索日志..."
              value={keyword}
              onChange={setKeyword}
              icon={<Search className="w-4 h-4" />}
            />
          </div>
          <select
            value={selectedOperation}
            onChange={(e) => setSelectedOperation(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-xuanji-500 focus:border-transparent"
          >
            <option value="">所有操作</option>
            {operations.map((op) => (
              <option key={op} value={op}>
                {op}
              </option>
            ))}
          </select>
        </div>
      </Card>

      {/* Logs List */}
      <Card>
        {loading ? (
          <div className="py-12 text-center text-gray-500">加载中...</div>
        ) : logs.length === 0 ? (
          <div className="py-12 text-center text-gray-500">暂无操作日志</div>
        ) : (
          <div className="divide-y divide-gray-200">
            {logs.map((log) => (
              <div key={log.id} className="p-4 hover:bg-gray-50">
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 mt-1">
                    <div className="p-2 bg-xuanji-100 rounded-lg">
                      <Activity className="w-4 h-4 text-xuanji-600" />
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          {getOperationBadge(log.operation)}
                          <span className="text-sm font-medium text-gray-900">
                            {log.userName}
                          </span>
                          <span className="text-gray-300">|</span>
                          <span className="text-sm text-gray-500">
                            请求ID: {log.requestId}
                          </span>
                        </div>
                      </div>
                      <div className="text-sm text-gray-500">
                        <Clock className="w-3 h-3 inline mr-1" />
                        {new Date(log.createdAt).toLocaleString('zh-CN')}
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4 text-gray-500" />
                        <span className="text-gray-600">用户ID:</span>
                        <span className="text-gray-900 font-mono text-xs">
                          {log.userId}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-gray-600">IP:</span>
                        <span className="text-gray-900 font-mono text-xs">
                          {log.ip}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 truncate">
                        <span className="text-gray-600">User Agent:</span>
                        <span className="text-gray-500 truncate">
                          {log.userAgent}
                        </span>
                      </div>
                    </div>

                    {Object.keys(log.details).length > 0 && (
                      <details className="mt-3">
                        <summary className="text-sm text-xuanji-600 cursor-pointer hover:text-xuanji-700">
                          查看详细信息
                        </summary>
                        <div className="mt-2 p-3 bg-gray-50 rounded-lg">
                          <pre className="text-xs text-gray-700 overflow-x-auto">
                            {JSON.stringify(log.details, null, 2)}
                          </pre>
                        </div>
                      </details>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}

export default AuthOperationLogView
