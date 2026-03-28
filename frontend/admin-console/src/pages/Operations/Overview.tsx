import { useEffect, useState } from 'react'
import { Activity, AlertTriangle, Shield, TrendingUp, Users, DollarSign } from 'lucide-react'
import type { OperationMetrics } from '@/types'

export default function OperationsOverview() {
  const [metrics, setMetrics] = useState<OperationMetrics | null>(null)

  useEffect(() => {
    // 模拟数据
    setMetrics({
      system: {
        uptime: 99.9,
        cpu: 45,
        memory: 62,
        disk: 58,
      },
      performance: {
        avgResponseTime: 120,
        errorRate: 0.2,
        requestCount: 15234,
      },
      security: {
        threatsBlocked: 234,
        loginAttempts: 1205,
        securityScore: 95,
      },
      business: {
        activeUsers: 1847,
        revenue: 234500,
        conversionRate: 12.5,
        churnRate: 2.3,
      },
    })
  }, [])

  if (!metrics) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          运营管理
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          系统运营概览和关键指标
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={Users}
          label="活跃用户"
          value={metrics.business.activeUsers.toLocaleString()}
          trend="+12.5%"
          color="blue"
        />
        <StatCard
          icon={DollarSign}
          label="收入"
          value={`¥${metrics.business.revenue.toLocaleString()}`}
          trend="+8.2%"
          color="green"
        />
        <StatCard
          icon={Activity}
          label="请求数"
          value={metrics.performance.requestCount.toLocaleString()}
          trend="+15.3%"
          color="purple"
        />
        <StatCard
          icon={Shield}
          label="安全评分"
          value={metrics.security.securityScore}
          trend="-0.5%"
          color="orange"
        />
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Status */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <Activity className="w-5 h-5 mr-2 text-blue-600" />
            系统状态
          </h2>
          <div className="space-y-4">
            <MetricRow label="系统运行时间" value={`${metrics.system.uptime}%`} />
            <MetricRow label="CPU 使用率" value={`${metrics.system.cpu}%`} />
            <MetricRow label="内存使用率" value={`${metrics.system.memory}%`} />
            <MetricRow label="磁盘使用率" value={`${metrics.system.disk}%`} />
          </div>
        </div>

        {/* Security Metrics */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <Shield className="w-5 h-5 mr-2 text-green-600" />
            安全指标
          </h2>
          <div className="space-y-4">
            <MetricRow label="威胁拦截" value={metrics.security.threatsBlocked} />
            <MetricRow label="登录尝试" value={metrics.security.loginAttempts} />
            <MetricRow label="安全评分" value={metrics.security.securityScore} />
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          快捷操作
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <QuickAction href="/operations/maintenance" label="系统维护" icon={Activity} />
          <QuickAction href="/operations/security" label="安全设置" icon={Shield} />
          <QuickAction href="/operations/analytics" label="数据分析" icon={TrendingUp} />
          <QuickAction href="/operations/crm" label="客户管理" icon={Users} />
        </div>
      </div>
    </div>
  )
}

function StatCard({
  icon: Icon,
  label,
  value,
  trend,
  color,
}: {
  icon: any
  label: string
  value: string | number
  trend: string
  color: string
}) {
  const colorClasses: Record<string, string> = {
    blue: 'bg-blue-100 dark:bg-blue-900 text-blue-600',
    green: 'bg-green-100 dark:bg-green-900 text-green-600',
    purple: 'bg-purple-100 dark:bg-purple-900 text-purple-600',
    orange: 'bg-orange-100 dark:bg-orange-900 text-orange-600',
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
        <span className="text-sm text-green-600 font-medium">{trend}</span>
      </div>
      <h3 className="text-sm text-gray-600 dark:text-gray-400 mb-1">{label}</h3>
      <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
    </div>
  )
}

function MetricRow({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700 last:border-0">
      <span className="text-sm text-gray-600 dark:text-gray-400">{label}</span>
      <span className="text-sm font-medium text-gray-900 dark:text-white">{value}</span>
    </div>
  )
}

function QuickAction({
  href,
  label,
  icon: Icon,
}: {
  href: string
  label: string
  icon: any
}) {
  return (
    <a
      href={href}
      className="flex items-center space-x-3 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
    >
      <Icon className="w-5 h-5 text-gray-600 dark:text-gray-300" />
      <span className="text-sm font-medium text-gray-900 dark:text-white">{label}</span>
    </a>
  )
}
