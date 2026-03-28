import type { DigitalHuman } from '@/types'

export default function DigitalHumanDetail() {
  const [digitalHuman] = useState<DigitalHuman>({
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
  })

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">数字人详情</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">查看数字人详细信息</p>
      </div>
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          {digitalHuman.name}
        </h2>
        <div className="space-y-4">
          <div>
            <label className="text-sm text-gray-600 dark:text-gray-400">类型</label>
            <p className="text-gray-900 dark:text-white">{digitalHuman.type}</p>
          </div>
          <div>
            <label className="text-sm text-gray-600 dark:text-gray-400">模型</label>
            <p className="text-gray-900 dark:text-white">{digitalHuman.model}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

function useState<T>(initial: T): [T, any] {
  const [value] = React.useState(initial)
  return [value, () => {}]
}
