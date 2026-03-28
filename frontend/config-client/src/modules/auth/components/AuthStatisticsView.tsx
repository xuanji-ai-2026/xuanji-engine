import React, { useEffect, useState } from 'react'
import { Card } from '@/components/Card'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import {
  TrendingUp,
  TrendingDown,
  CheckCircle,
  XCircle,
  Clock,
  AlertCircle,
} from 'lucide-react'
import type { AuthStatistics } from '@/types'

export const AuthStatisticsView: React.FC = () => {
  const [statistics, setStatistics] = useState<AuthStatistics | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchStatistics()
  }, [])

  const fetchStatistics = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/auth-statistics')
      const data: AuthStatistics = await response.json()
      setStatistics(data)
    } catch (error) {
      console.error('Failed to fetch statistics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading || !statistics) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-gray-500">加载统计数据...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">认证统计分析</h1>
        <p className="mt-1 text-sm text-gray-600">
          认证请求的整体数据和趋势分析
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">总请求数</p>
              <p className="mt-2 text-3xl font-bold text-gray-900">
                {statistics.totalRequests}
              </p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <AlertCircle className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">待处理</p>
              <p className="mt-2 text-3xl font-bold text-yellow-600">
                {statistics.pendingRequests}
              </p>
            </div>
            <div className="p-3 bg-yellow-100 rounded-lg">
              <Clock className="w-6 h-6 text-yellow-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">已通过</p>
              <p className="mt-2 text-3xl font-bold text-green-600">
                {statistics.approvedRequests}
              </p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">已驳回</p>
              <p className="mt-2 text-3xl font-bold text-red-600">
                {statistics.rejectedRequests}
              </p>
            </div>
            <div className="p-3 bg-red-100 rounded-lg">
              <XCircle className="w-6 h-6 text-red-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            关键指标
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">通过率</span>
              <span className="text-lg font-semibold text-gray-900">
                {statistics.approvalRate.toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-green-600 h-2 rounded-full"
                style={{ width: `${statistics.approvalRate}%` }}
              />
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="text-sm text-gray-600">平均处理时间</span>
              <div className="flex items-center gap-2">
                <TrendingDown className="w-4 h-4 text-green-500" />
                <span className="text-lg font-semibold text-gray-900">
                  {statistics.averageProcessingTime} 分钟
                </span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">处理中</span>
              <span className="text-lg font-semibold text-blue-600">
                {statistics.processingRequests}
              </span>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            按请求类型分布
          </h3>
          <div className="space-y-3">
            {Object.entries(statistics.requestsByType).map(
              ([type, count]) => {
                const percentage =
                  (count / statistics.totalRequests) * 100
                const colors: Record<string, string> = {
                  login: 'bg-blue-500',
                  password_reset: 'bg-purple-500',
                  privilege_upgrade: 'bg-orange-500',
                  account_recovery: 'bg-red-500',
                  two_factor_enable: 'bg-green-500',
                }
                const labels: Record<string, string> = {
                  login: '登录认证',
                  password_reset: '密码重置',
                  privilege_upgrade: '权限升级',
                  account_recovery: '账号恢复',
                  two_factor_enable: '双因素认证',
                }
                return (
                  <div key={type}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm text-gray-900">
                        {labels[type] || type}
                      </span>
                      <span className="text-sm text-gray-600">
                        {count} ({percentage.toFixed(1)}%)
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={cn('h-2 rounded-full', colors[type] || 'bg-gray-500')}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                )
              }
            )}
          </div>
        </Card>
      </div>

      {/* Priority and Trend */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            按优先级分布
          </h3>
          <div className="space-y-3">
            {Object.entries(statistics.requestsByPriority).map(
              ([priority, count]) => {
                const percentage =
                  (count / statistics.totalRequests) * 100
                const colors: Record<string, string> = {
                  low: 'bg-gray-400',
                  medium: 'bg-blue-500',
                  high: 'bg-orange-500',
                  urgent: 'bg-red-500',
                }
                const labels: Record<string, string> = {
                  low: '低',
                  medium: '中',
                  high: '高',
                  urgent: '紧急',
                }
                return (
                  <div key={priority}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm text-gray-900">
                        {labels[priority] || priority}
                      </span>
                      <span className="text-sm text-gray-600">
                        {count} ({percentage.toFixed(1)}%)
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={cn('h-2 rounded-full', colors[priority] || 'bg-gray-500')}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                )
              }
            )}
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            月度趋势
          </h3>
          <div className="space-y-3">
            {statistics.monthlyTrend.map((item, index) => {
              const maxCount = Math.max(
                ...statistics.monthlyTrend.map((t) => t.count)
              )
              const percentage = (item.count / maxCount) * 100
              return (
                <div key={index}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-gray-900">{item.month}</span>
                    <div className="flex items-center gap-1">
                      {index > 0 &&
                      item.count > statistics.monthlyTrend[index - 1].count ? (
                        <TrendingUp className="w-4 h-4 text-green-500" />
                      ) : (
                        <TrendingDown className="w-4 h-4 text-red-500" />
                      )}
                      <span className="text-sm text-gray-600">{item.count}</span>
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-xuanji-600 h-2 rounded-full"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </Card>
      </div>
    </div>
  )
}

export default AuthStatisticsView
