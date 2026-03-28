import { useState } from 'react'
import { useAssistantStore } from '@/stores/assistant-store'
import { Activity, AlertTriangle, Lightbulb } from 'lucide-react'

export default function Assistant() {
  const { alerts, suggestions, isActive, toggleActive } = useAssistantStore()

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">智能助手小灵</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            AI 助手，提供系统监控和决策建议
          </p>
        </div>
        <button
          onClick={toggleActive}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            isActive
              ? 'bg-green-600 hover:bg-green-700 text-white'
              : 'bg-gray-600 hover:bg-gray-700 text-white'
          }`}
        >
          {isActive ? '已启用' : '已禁用'}
        </button>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          icon={AlertTriangle}
          label="待处理告警"
          value={alerts.filter((a) => !a.acknowledged).length}
          color="red"
        />
        <StatCard
          icon={Lightbulb}
          label="优化建议"
          value={suggestions.length}
          color="yellow"
        />
        <StatCard
          icon={Activity}
          label="系统状态"
          value="正常"
          color="green"
        />
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            告警信息
          </h2>
          <div className="space-y-3">
            {alerts.slice(0, 5).map((alert) => (
              <AlertCard key={alert.id} alert={alert} />
            ))}
          </div>
        </div>
      )}

      {/* Suggestions */}
      {suggestions.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            优化建议
          </h2>
          <div className="space-y-3">
            {suggestions.slice(0, 3).map((suggestion) => (
              <SuggestionCard key={suggestion.id} suggestion={suggestion} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function StatCard({
  icon: Icon,
  label,
  value,
  color,
}: {
  icon: any
  label: string
  value: string | number
  color: string
}) {
  const colorClasses: Record<string, string> = {
    red: 'bg-red-100 dark:bg-red-900 text-red-600',
    yellow: 'bg-yellow-100 dark:bg-yellow-900 text-yellow-600',
    green: 'bg-green-100 dark:bg-green-900 text-green-600',
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
      <div className="flex items-center space-x-4">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{label}</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
        </div>
      </div>
    </div>
  )
}

function AlertCard({ alert }: { alert: any }) {
  return (
    <div className={`p-4 rounded-lg border ${
      alert.severity === 'critical'
        ? 'border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20'
        : alert.severity === 'high'
        ? 'border-orange-200 dark:border-orange-800 bg-orange-50 dark:bg-orange-900/20'
        : 'border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20'
    }`}>
      <div className="flex items-start justify-between">
        <div>
          <h4 className="font-medium text-gray-900 dark:text-white">{alert.title}</h4>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{alert.message}</p>
        </div>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          {new Date(alert.timestamp).toLocaleString('zh-CN')}
        </span>
      </div>
    </div>
  )
}

function SuggestionCard({ suggestion }: { suggestion: any }) {
  return (
    <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-700">
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-medium text-gray-900 dark:text-white">{suggestion.title}</h4>
        <span className="text-xs px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded">
          {suggestion.impact}
        </span>
      </div>
      <p className="text-sm text-gray-600 dark:text-gray-400">{suggestion.description}</p>
    </div>
  )
}
