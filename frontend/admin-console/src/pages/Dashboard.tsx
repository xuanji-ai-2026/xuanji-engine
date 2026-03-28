import { useEffect, useState } from 'react'
import {
  Users,
  Bot,
  Database,
  Puzzle,
  Activity,
  Settings,
  Zap,
  Bell,
} from 'lucide-react'
import type { OperationMetrics } from '@/types'

export default function Dashboard() {
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

  const statCards = [
    {
      title: '总用户数',
      value: metrics?.business.activeUsers || 0,
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100 dark:bg-blue-900',
    },
    {
      title: '数字人数量',
      value: 156,
      icon: Bot,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100 dark:bg-purple-900',
    },
    {
      title: '知识源',
      value: 89,
      icon: Database,
      color: 'text-green-600',
      bgColor: 'bg-green-100 dark:bg-green-900',
    },
    {
      title: '插件数',
      value: 234,
      icon: Puzzle,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100 dark:bg-orange-900',
    },
  ]

  if (!metrics) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          仪表板
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          欢迎回到玄玑引擎管理控制台
        </p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => (
          <div
            key={index}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 transition-transform hover:scale-105 animate-slide-in"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {card.title}
                </p>
                <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
                  {card.value.toLocaleString()}
                </p>
              </div>
              <div
                className={`p-3 rounded-lg ${card.bgColor} ${card.color}`}
              >
                <card.icon className="w-6 h-6" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Metrics */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            系统指标
          </h2>
          <div className="space-y-4">
            <MetricBar
              label="CPU 使用率"
              value={metrics.system.cpu}
              color="bg-blue-500"
            />
            <MetricBar
              label="内存使用率"
              value={metrics.system.memory}
              color="bg-green-500"
            />
            <MetricBar
              label="磁盘使用率"
              value={metrics.system.disk}
              color="bg-purple-500"
            />
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            性能指标
          </h2>
          <div className="space-y-4">
            <MetricCard
              icon={Activity}
              label="平均响应时间"
              value={`${metrics.performance.avgResponseTime}ms`}
            />
            <MetricCard
              icon={Zap}
              label="错误率"
              value={`${metrics.performance.errorRate}%`}
            />
            <MetricCard
              icon={Bell}
              label="请求数量"
              value={metrics.performance.requestCount.toLocaleString()}
            />
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          快捷操作
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <QuickActionButton
            icon={Users}
            label="添加用户"
            href="/users"
            color="bg-blue-500"
          />
          <QuickActionButton
            icon={Bot}
            label="创建数字人"
            href="/digital-humans"
            color="bg-purple-500"
          />
          <QuickActionButton
            icon={Database}
            label="导入知识"
            href="/knowledge"
            color="bg-green-500"
          />
          <QuickActionButton
            icon={Settings}
            label="系统设置"
            href="/settings"
            color="bg-orange-500"
          />
        </div>
      </div>
    </div>
  )
}

function MetricBar({
  label,
  value,
  color,
}: {
  label: string
  value: number
  color: string
}) {
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="text-gray-600 dark:text-gray-400">{label}</span>
        <span className="text-gray-900 dark:text-white font-medium">
          {value}%
        </span>
      </div>
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
        <div
          className={`${color} h-2 rounded-full transition-all duration-500`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  )
}

function MetricCard({
  icon: Icon,
  label,
  value,
}: {
  icon: any
  label: string
  value: string
}) {
  return (
    <div className="flex items-center space-x-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
      <Icon className="w-5 h-5 text-gray-600 dark:text-gray-300" />
      <div className="flex-1">
        <p className="text-sm text-gray-600 dark:text-gray-400">{label}</p>
        <p className="text-lg font-semibold text-gray-900 dark:text-white">
          {value}
        </p>
      </div>
    </div>
  )
}

function QuickActionButton({
  icon: Icon,
  label,
  href,
  color,
}: {
  icon: any
  label: string
  href: string
  color: string
}) {
  return (
    <a
      href={href}
      className="flex flex-col items-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
    >
      <Icon className={`w-8 h-8 mb-2 ${color} text-white`} />
      <span className="text-sm font-medium text-gray-900 dark:text-white">
        {label}
      </span>
    </a>
  )
}
