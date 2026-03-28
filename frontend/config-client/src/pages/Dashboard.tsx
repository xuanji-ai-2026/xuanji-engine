import React, { useEffect } from 'react'
import { useWorkbenchStore } from '@/stores/workbenchStore'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/Card'
import { Badge } from '@/components/Badge'
import { cn, formatRelativeTime } from '@/utils'
import {
  Users,
  ShieldCheck,
  Settings,
  LayoutList,
  CheckCircle,
  Clock,
  AlertTriangle,
  TrendingUp,
} from 'lucide-react'

interface StatCardProps {
  title: string
  value: number | string
  icon: React.ReactNode
  trend?: {
    value: number
    isPositive: boolean
  }
  color: 'blue' | 'green' | 'yellow' | 'red' | 'purple'
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon,
  trend,
  color,
}) => {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    yellow: 'bg-yellow-50 text-yellow-600',
    red: 'bg-red-50 text-red-600',
    purple: 'bg-purple-50 text-purple-600',
  }

  return (
    <Card>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {trend && (
            <p
              className={cn(
                'text-xs mt-1',
                trend.isPositive ? 'text-green-600' : 'text-red-600',
              )}
            >
              {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
            </p>
          )}
        </div>
        <div className={cn('p-3 rounded-lg', colorClasses[color])}>
          {icon}
        </div>
      </div>
    </Card>
  )
}

export const Dashboard: React.FC = () => {
  const { statistics, notifications, fetchStatistics, fetchNotifications } =
    useWorkbenchStore()

  useEffect(() => {
    fetchStatistics()
    fetchNotifications()
  }, [fetchStatistics, fetchNotifications])

  const recentNotifications = notifications.slice(0, 5)

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-1">工作台</h1>
        <p className="text-gray-600">欢迎回来，这是系统概览</p>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="总用户数"
          value={statistics?.totalUsers || 0}
          icon={<Users className="w-6 h-6" />}
          trend={{ value: 12, isPositive: true }}
          color="blue"
        />
        <StatCard
          title="待处理认证请求"
          value={statistics?.pendingAuthRequests || 0}
          icon={<ShieldCheck className="w-6 h-6" />}
          color="yellow"
        />
        <StatCard
          title="待处理配置请求"
          value={statistics?.pendingConfigRequests || 0}
          icon={<Settings className="w-6 h-6" />}
          color="purple"
        />
        <StatCard
          title="已完成任务"
          value={statistics?.completedTasks || 0}
          icon={<CheckCircle className="w-6 h-6" />}
          trend={{ value: 8, isPositive: true }}
          color="green"
        />
      </div>

      {/* Additional Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <StatCard
          title="进行中任务"
          value={statistics?.inProgressTasks || 0}
          icon={<Clock className="w-6 h-6" />}
          color="blue"
        />
        <StatCard
          title="逾期任务"
          value={statistics?.overdueTasks || 0}
          icon={<AlertTriangle className="w-6 h-6" />}
          color="red"
        />
        <StatCard
          title="系统健康状态"
          value={
            statistics?.systemHealth === 'healthy'
              ? '正常'
              : statistics?.systemHealth === 'warning'
              ? '警告'
              : '异常'
          }
          icon={<TrendingUp className="w-6 h-6" />}
          color={
            statistics?.systemHealth === 'healthy'
              ? 'green'
              : statistics?.systemHealth === 'warning'
              ? 'yellow'
              : 'red'
          }
        />
      </div>

      {/* Recent Notifications */}
      <Card>
        <CardHeader>
          <CardTitle>最近通知</CardTitle>
        </CardHeader>
        <CardContent>
          {recentNotifications.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              暂无通知
            </div>
          ) : (
            <div className="space-y-3">
              {recentNotifications.map((notification) => (
                <div
                  key={notification.id}
                  className={cn(
                    'flex items-start gap-3 p-3 rounded-lg transition-colors',
                    notification.read ? 'bg-gray-50' : 'bg-xuanji-50',
                  )}
                >
                  <div className="flex-shrink-0 mt-0.5">
                    {!notification.read && (
                      <div className="w-2 h-2 bg-xuanji-600 rounded-full" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">
                      {notification.title}
                    </p>
                    <p className="text-sm text-gray-600 mt-0.5">
                      {notification.message}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {formatRelativeTime(notification.createdAt)}
                    </p>
                  </div>
                  <Badge
                    variant={
                      notification.priority === 'urgent'
                        ? 'danger'
                        : notification.priority === 'high'
                        ? 'warning'
                        : 'info'
                    }
                    size="sm"
                  >
                    {notification.priority}
                  </Badge>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>快捷操作</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button className="p-4 border border-gray-200 rounded-lg hover:border-xuanji-300 hover:bg-xuanji-50 transition-all text-left">
              <ShieldCheck className="w-6 h-6 text-xuanji-600 mb-2" />
              <p className="text-sm font-medium text-gray-900">处理认证请求</p>
            </button>
            <button className="p-4 border border-gray-200 rounded-lg hover:border-xuanji-300 hover:bg-xuanji-50 transition-all text-left">
              <Settings className="w-6 h-6 text-xuanji-600 mb-2" />
              <p className="text-sm font-medium text-gray-900">处理配置请求</p>
            </button>
            <button className="p-4 border border-gray-200 rounded-lg hover:border-xuanji-300 hover:bg-xuanji-50 transition-all text-left">
              <LayoutList className="w-6 h-6 text-xuanji-600 mb-2" />
              <p className="text-sm font-medium text-gray-900">创建新任务</p>
            </button>
            <button className="p-4 border border-gray-200 rounded-lg hover:border-xuanji-300 hover:bg-xuanji-50 transition-all text-left">
              <Users className="w-6 h-6 text-xuanji-600 mb-2" />
              <p className="text-sm font-medium text-gray-900">添加用户</p>
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
