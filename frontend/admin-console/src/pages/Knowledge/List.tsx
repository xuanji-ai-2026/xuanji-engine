import { useState } from 'react'
import { Plus, Upload, FileText, Database, Globe, Link as LinkIcon } from 'lucide-react'
import type { KnowledgeSource } from '@/types'

export default function KnowledgeList() {
  const [sources, setSources] = useState<KnowledgeSource[]>([
    {
      id: '1',
      name: '产品文档',
      type: 'document',
      status: 'active',
      config: {},
      stats: {
        documents: 156,
        size: 25600000,
        lastSyncAt: new Date().toISOString(),
      },
      createdAt: '2024-01-15T00:00:00Z',
      updatedAt: '2024-03-20T00:00:00Z',
    },
  ])

  const typeIcons: Record<string, any> = {
    document: FileText,
    database: Database,
    api: LinkIcon,
    website: Globe,
    custom: Upload,
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            知识源管理
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            管理和配置知识数据源
          </p>
        </div>
        <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
          <Plus className="w-4 h-4 mr-2" />
          添加知识源
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sources.map((source) => {
          const Icon = typeIcons[source.type] || FileText
          return (
            <div
              key={source.id}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                  <Icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
                <StatusBadge status={source.status} />
              </div>

              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {source.name}
              </h3>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">文档数</span>
                  <span className="text-gray-900 dark:text-white font-medium">
                    {source.stats.documents}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">大小</span>
                  <span className="text-gray-900 dark:text-white font-medium">
                    {(source.stats.size / 1024 / 1024).toFixed(2)} MB
                  </span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 flex space-x-2">
                <button className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors">
                  配置
                </button>
                <button className="px-3 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 text-sm rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  同步
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const statusStyles: Record<string, string> = {
    active: 'bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400',
    syncing: 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400',
    error: 'bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400',
    inactive: 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400',
  }

  const statusLabels: Record<string, string> = {
    active: '活跃',
    syncing: '同步中',
    error: '错误',
    inactive: '未激活',
  }

  return (
    <span
      className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${statusStyles[status] || statusStyles.inactive}`}
    >
      {statusLabels[status] || status}
    </span>
  )
}
