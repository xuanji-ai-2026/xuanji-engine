import { useState } from 'react'
import { Plus, Star, Download, Shield } from 'lucide-react'
import type { Plugin } from '@/types'

export default function PluginList() {
  const [plugins, setPlugins] = useState<Plugin[]>([
    {
      id: '1',
      name: 'CRM集成',
      version: '1.2.0',
      description: '与客户关系管理系统无缝集成',
      author: '官方',
      status: 'active',
      type: 'integration',
      config: {},
      metrics: {
        installs: 1234,
        rating: 4.5,
        reviews: 89,
      },
      createdAt: '2024-01-15T00:00:00Z',
      updatedAt: '2024-03-20T00:00:00Z',
    },
  ])

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            插件管理
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            管理和审核系统插件
          </p>
        </div>
        <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
          <Plus className="w-4 h-4 mr-2" />
          发布插件
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {plugins.map((plugin) => (
          <PluginCard key={plugin.id} plugin={plugin} />
        ))}
      </div>
    </div>
  )
}

function PluginCard({ plugin }: { plugin: Plugin }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
            {plugin.name}
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            v{plugin.version} · {plugin.author}
          </p>
        </div>
        <StatusBadge status={plugin.status} />
      </div>

      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
        {plugin.description}
      </p>

      <div className="flex items-center space-x-4 mb-4 text-sm">
        <div className="flex items-center">
          <Star className="w-4 h-4 text-yellow-500 mr-1" />
          <span className="text-gray-900 dark:text-white">
            {plugin.metrics.rating}
          </span>
        </div>
        <div className="flex items-center text-gray-600 dark:text-gray-400">
          <Download className="w-4 h-4 mr-1" />
          <span>{plugin.metrics.installs}</span>
        </div>
      </div>

      <div className="flex space-x-2">
        <button className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors">
          管理
        </button>
        <button className="px-3 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 text-sm rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
          审核
        </button>
      </div>
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const statusStyles: Record<string, string> = {
    active: 'bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400',
    inactive: 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400',
    reviewing: 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400',
    rejected: 'bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400',
  }

  const statusLabels: Record<string, string> = {
    active: '已启用',
    inactive: '未启用',
    reviewing: '审核中',
    rejected: '已拒绝',
  }

  return (
    <span
      className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${statusStyles[status] || statusStyles.inactive}`}
    >
      {statusLabels[status] || status}
    </span>
  )
}
