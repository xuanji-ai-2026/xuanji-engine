import { Link } from 'react-router-dom'
import { Sparkles, User, Shield } from 'lucide-react'

export default function SystemInit() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          系统初始化
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          完成初始配置以启动玄玑引擎
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <InitCard
          title="一键创世"
          description="初始化系统核心配置，创建管理员账户"
          icon={Sparkles}
          href="/system-init/creator"
          status="pending"
        />
        <InitCard
          title="创始人绑定"
          description="绑定创始人账户，授予最高权限"
          icon={User}
          href="/system-init/creator"
          status="pending"
        />
        <InitCard
          title="隐身激活"
          description="启用隐身模式，隐藏系统标识"
          icon={Shield}
          href="/system-init/stealth"
          status="pending"
        />
      </div>
    </div>
  )
}

function InitCard({
  title,
  description,
  icon: Icon,
  href,
  status,
}: {
  title: string
  description: string
  icon: any
  href: string
  status: 'completed' | 'pending' | 'in-progress'
}) {
  const statusColors = {
    completed: 'bg-green-500',
    pending: 'bg-gray-500',
    'in-progress': 'bg-blue-500',
  }

  return (
    <Link
      to={href}
      className="block bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow"
    >
      <div className="flex items-start justify-between mb-4">
        <div className={`p-3 rounded-lg ${statusColors[status]} text-white`}>
          <Icon className="w-6 h-6" />
        </div>
        <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
          {status === 'completed'
            ? '已完成'
            : status === 'in-progress'
            ? '进行中'
            : '待处理'}
        </span>
      </div>
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        {title}
      </h3>
      <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
    </Link>
  )
}
