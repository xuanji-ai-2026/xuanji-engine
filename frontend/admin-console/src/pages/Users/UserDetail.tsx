import { useState } from 'react'
import type { User } from '@/types'

export default function UserDetail() {
  const [user] = useState<User>({
    id: '1',
    name: '张三',
    email: 'zhangsan@example.com',
    role: 'admin',
    status: 'active',
    createdAt: '2024-01-15T00:00:00Z',
    lastLoginAt: '2024-03-20T10:30:00Z',
  })

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">用户详情</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">查看用户详细信息</p>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
        <div className="grid grid-cols-2 gap-6">
          <div>
            <label className="text-sm text-gray-600 dark:text-gray-400">姓名</label>
            <p className="text-lg font-medium text-gray-900 dark:text-white mt-1">{user.name}</p>
          </div>
          <div>
            <label className="text-sm text-gray-600 dark:text-gray-400">邮箱</label>
            <p className="text-lg font-medium text-gray-900 dark:text-white mt-1">{user.email}</p>
          </div>
          <div>
            <label className="text-sm text-gray-600 dark:text-gray-400">角色</label>
            <p className="text-lg font-medium text-gray-900 dark:text-white mt-1">{user.role}</p>
          </div>
          <div>
            <label className="text-sm text-gray-600 dark:text-gray-400">状态</label>
            <p className="text-lg font-medium text-gray-900 dark:text-white mt-1">{user.status}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
