import { useState } from 'react'
import { Plus, Settings, Play, Pause } from 'lucide-react'
import type { DigitalHuman } from '@/types'

export default function DigitalHumanList() {
  const [digitalHumans, setDigitalHumans] = useState<DigitalHuman[]>([
    {
      id: '1',
      name: '客服助手',
      type: 'customer_service',
      model: 'gpt-4',
      status: 'active',
      capabilities: ['问答', '对话', '知识检索'],
      configuration: {},
      createdAt: '2024-01-15T00:00:00Z',
      updatedAt: '2024-03-20T00:00:00Z',
      usageStats: {
        totalSessions: 1523,
        avgResponseTime: 1.2,
        satisfaction: 4.5,
      },
    },
  ])

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            数字人管理
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            管理和配置 AI 数字员工
          </p>
        </div>
        <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
          <Plus className="w-4 h-4 mr-2" />
          创建数字人
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {digitalHumans.map((dh) => (
          <DigitalHumanCard key={dh.id} digitalHuman={dh} />
        ))}
      </div>
    </div>
  )
}

function DigitalHumanCard({ digitalHuman }: { digitalHuman: DigitalHuman }) {
  const typeLabels: Record<string, string> = {
    customer_service: '客服助手',
    assistant: '业务助手',
    expert: '专家顾问',
    custom: '自定义',
  }

  const statusColors: Record<string, string> = {
    active: 'bg-green-500',
    inactive: 'bg-gray-500',
    training: 'bg-yellow-500',
    maintenance: 'bg-red-500',
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {digitalHuman.name}
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {typeLabels[digitalHuman.type]}
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <div
            className={`w-2 h-2 rounded-full ${statusColors[digitalHuman.status]}`}
          />
          <span className="text-xs text-gray-500 dark:text-gray-400">
            {digitalHuman.status}
          </span>
        </div>
      </div>

      <div className="space-y-3 mb-4">
        <div className="flex justify-between text-sm">
          <span className="text-gray-600 dark:text-gray-400">模型</span>
          <span className="text-gray-900 dark:text-white font-medium">
            {digitalHuman.model}
          </span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-600 dark:text-gray-400">会话数</span>
          <span className="text-gray-900 dark:text-white font-medium">
            {digitalHuman.usageStats.totalSessions}
          </span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-600 dark:text-gray-400">满意度</span>
          <span className="text-gray-900 dark:text-white font-medium">
            {digitalHuman.usageStats.satisfaction.toFixed(1)}/5.0
          </span>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 mb-4">
        {digitalHuman.capabilities.slice(0, 3).map((cap, index) => (
          <span
            key={index}
            className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded"
          >
            {cap}
          </span>
        ))}
        {digitalHuman.capabilities.length > 3 && (
          <span className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded">
            +{digitalHuman.capabilities.length - 3}
          </span>
        )}
      </div>

      <div className="flex space-x-2">
        <button className="flex-1 flex items-center justify-center px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors">
          <Settings className="w-4 h-4 mr-1" />
          配置
        </button>
        {digitalHuman.status === 'active' ? (
          <button className="px-3 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 text-sm rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <Pause className="w-4 h-4" />
          </button>
        ) : (
          <button className="px-3 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 text-sm rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <Play className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  )
}
