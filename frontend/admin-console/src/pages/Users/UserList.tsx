import { useState } from 'react'
import { Plus, Search, Filter, Download } from 'lucide-react'
import type { User, UserFilters, Pagination } from '@/types'

export default function UserList() {
  const [users, setUsers] = useState<User[]>([
    {
      id: '1',
      name: '张三',
      email: 'zhangsan@example.com',
      role: 'admin',
      status: 'active',
      createdAt: '2024-01-15T00:00:00Z',
      lastLoginAt: '2024-03-20T10:30:00Z',
    },
    {
      id: '2',
      name: '李四',
      email: 'lisi@example.com',
      role: 'user',
      status: 'active',
      createdAt: '2024-02-10T00:00:00Z',
      lastLoginAt: '2024-03-19T15:45:00Z',
    },
  ])

  const [filters, setFilters] = useState<UserFilters>({})
  const [pagination, setPagination] = useState<Pagination>({
    page: 1,
    pageSize: 10,
    total: 2,
  })

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            用户管理
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            管理系统中的所有用户
          </p>
        </div>
        <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
          <Plus className="w-4 h-4 mr-2" />
          添加用户
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="搜索用户..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
              value={filters.keyword || ''}
              onChange={(e) =>
                setFilters({ ...filters, keyword: e.target.value })
              }
            />
          </div>
          <select
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
            value={filters.role || ''}
            onChange={(e) => setFilters({ ...filters, role: e.target.value })}
          >
            <option value="">所有角色</option>
            <option value="admin">管理员</option>
            <option value="user">用户</option>
            <option value="manager">经理</option>
            <option value="viewer">访客</option>
          </select>
          <select
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
            value={filters.status || ''}
            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
          >
            <option value="">所有状态</option>
            <option value="active">活跃</option>
            <option value="inactive">未激活</option>
            <option value="pending">待审核</option>
            <option value="suspended">已禁用</option>
          </select>
          <button className="flex items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <Filter className="w-4 h-4 mr-2" />
            高级筛选
          </button>
        </div>
      </div>

      {/* User Table */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  用户
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  角色
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  状态
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  创建时间
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  最后登录
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  操作
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {users.map((user) => (
                <tr
                  key={user.id}
                  className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  <td className="px-6 py-4">
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        {user.name}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {user.email}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex px-2 py-1 text-xs font-medium rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400">
                      {user.role}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <StatusBadge status={user.status} />
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {new Date(user.createdAt).toLocaleDateString('zh-CN')}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {user.lastLoginAt
                      ? new Date(user.lastLoginAt).toLocaleString('zh-CN')
                      : '-'}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end space-x-2">
                      <button className="text-blue-600 hover:text-blue-800 text-sm">
                        查看
                      </button>
                      <button className="text-gray-600 hover:text-gray-800 text-sm">
                        编辑
                      </button>
                      <button className="text-red-600 hover:text-red-800 text-sm">
                        删除
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <div className="text-sm text-gray-500 dark:text-gray-400">
            共 {pagination.total} 条记录
          </div>
          <div className="flex space-x-2">
            <button className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm dark:text-gray-300 disabled:opacity-50">
              上一页
            </button>
            <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm">
              1
            </button>
            <button className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm dark:text-gray-300">
              下一页
            </button>
          </div>
        </div>
      </div>

      {/* Export Button */}
      <div className="flex justify-end">
        <button className="flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
          <Download className="w-4 h-4 mr-2" />
          导出数据
        </button>
      </div>
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const statusStyles: Record<string, string> = {
    active: 'bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400',
    inactive:
      'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400',
    pending: 'bg-yellow-100 dark:bg-yellow-900 text-yellow-600 dark:text-yellow-400',
    suspended: 'bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400',
  }

  const statusLabels: Record<string, string> = {
    active: '活跃',
    inactive: '未激活',
    pending: '待审核',
    suspended: '已禁用',
  }

  return (
    <span
      className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${statusStyles[status] || statusStyles.inactive}`}
    >
      {statusLabels[status] || status}
    </span>
  )
}
