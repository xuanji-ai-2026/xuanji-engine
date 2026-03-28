import React, { useEffect, useState } from 'react'
import { Routes, Route, useNavigate, useParams } from 'react-router-dom'
import { useUserStore } from '@/stores/userStore'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/Card'
import { StatusBadge } from '@/components/Badge'
import { Select } from '@/components/Input'
import { Modal, ConfirmDialog } from '@/components/Modal'
import { cn, formatDate } from '@/utils'
import {
  Search,
  Plus,
  RefreshCw,
  Users,
  ArrowLeft,
  Edit,
  Trash2,
  MoreVertical,
  Shield,
  Key,
  Ban,
  Check,
} from 'lucide-react'

// User List Component
export const UserList: React.FC = () => {
  const navigate = useNavigate()
  const {
    users,
    loading,
    total,
    filters,
    pagination,
    fetchUsers,
    setFilters,
    setPagination,
  } = useUserStore()

  const [searchKeyword, setSearchKeyword] = useState('')
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false)
  const [selectedUser, setSelectedUser] = useState<string | null>(null)

  useEffect(() => {
    fetchUsers()
  }, [fetchUsers])

  const handleCreate = () => {
    navigate('/user/create')
  }

  const handleRefresh = () => {
    fetchUsers()
  }

  const handleDelete = (userId: string) => {
    setSelectedUser(userId)
    setDeleteConfirmOpen(true)
  }

  const confirmDelete = async () => {
    if (selectedUser) {
      try {
        // await deleteUser(selectedUser)
        fetchUsers()
      } catch (error) {
        console.error('Failed to delete user:', error)
      }
    }
    setDeleteConfirmOpen(false)
    setSelectedUser(null)
  }

  const roleLabels: Record<string, string> = {
    admin: '管理员',
    manager: '经理',
    operator: '操作员',
    viewer: '查看者',
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-1">用户管理</h1>
          <p className="text-gray-600">管理系统用户和权限</p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="secondary"
            icon={<RefreshCw className="w-4 h-4" />}
            onClick={handleRefresh}
            loading={loading}
          >
            刷新
          </Button>
          <Button
            variant="primary"
            icon={<Plus className="w-4 h-4" />}
            onClick={handleCreate}
          >
            添加用户
          </Button>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardContent padding="sm">
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex-1 min-w-[200px]">
              <Input
                placeholder="搜索用户名、邮箱、姓名..."
                leftIcon={<Search className="w-4 h-4" />}
                value={searchKeyword}
                onChange={(e) => setSearchKeyword(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && setFilters({ ...filters, keyword: searchKeyword })}
              />
            </div>
            <Select
              options={[
                { label: '全部状态', value: '' },
                { label: '活跃', value: 'active' },
                { label: '未激活', value: 'inactive' },
                { label: '已锁定', value: 'locked' },
                { label: '待审核', value: 'pending' },
              ]}
              defaultValue=""
              onChange={(e) => {
                const status = e.target.value ? [e.target.value] : undefined
                setFilters({ ...filters, status })
              }}
            />
          </div>
        </CardContent>
      </Card>

      {/* User List */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>用户列表 ({total})</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-12">
              <RefreshCw className="w-8 h-8 text-xuanji-600 animate-spin mx-auto mb-4" />
              <p className="text-gray-600">加载中...</p>
            </div>
          ) : users.length === 0 ? (
            <div className="text-center py-12">
              <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">暂无用户</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead>
                  <tr>
                    <th className="px-4 py-3">用户</th>
                    <th className="px-4 py-3">角色</th>
                    <th className="px-4 py-3">状态</th>
                    <th className="px-4 py-3">部门</th>
                    <th className="px-4 py-3">创建时间</th>
                    <th className="px-4 py-3">操作</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr
                      key={user.id}
                      className="border-b border-gray-200 hover:bg-gray-50 cursor-pointer"
                      onClick={() => navigate(`/user/${user.id}`)}
                    >
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 bg-xuanji-100 rounded-full flex items-center justify-center">
                            <span className="text-xs font-medium text-xuanji-700">
                              {user.realName?.[0] || user.username?.[0] || 'U'}
                            </span>
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">
                              {user.realName || user.username}
                            </p>
                            <p className="text-xs text-gray-500">{user.email}</p>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
                          {roleLabels[user.role] || user.role}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <StatusBadge status={user.status} />
                      </td>
                      <td className="px-4 py-3 text-gray-600">
                        {user.department || '-'}
                      </td>
                      <td className="px-4 py-3 text-gray-600">
                        {formatDate(user.createdAt, 'yyyy-MM-dd')}
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            icon={<Edit className="w-4 h-4" />}
                            onClick={(e) => {
                              e.stopPropagation()
                              navigate(`/user/${user.id}/edit`)
                            }}
                          />
                          <Button
                            variant="ghost"
                            size="sm"
                            icon={<Trash2 className="w-4 h-4" />}
                            onClick={(e) => {
                              e.stopPropagation()
                              handleDelete(user.id)
                            }}
                          />
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Pagination */}
          {total > 0 && (
            <div className="mt-4 flex items-center justify-between pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-600">
                显示 {((pagination.page - 1) * pagination.pageSize) + 1} -{' '}
                {Math.min(pagination.page * pagination.pageSize, total)} 共 {total} 条
              </p>
              <div className="flex gap-2">
                <Button
                  variant="secondary"
                  size="sm"
                  disabled={pagination.page === 1}
                  onClick={() => {
                    setPagination({ page: pagination.page - 1 })
                    fetchUsers()
                  }}
                >
                  上一页
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  disabled={pagination.page * pagination.pageSize >= total}
                  onClick={() => {
                    setPagination({ page: pagination.page + 1 })
                    fetchUsers()
                  }}
                >
                  下一页
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Delete Confirmation */}
      <ConfirmDialog
        isOpen={deleteConfirmOpen}
        onClose={() => setDeleteConfirmOpen(false)}
        onConfirm={confirmDelete}
        title="确认删除"
        message="确定要删除该用户吗？此操作不可恢复。"
        confirmText="删除"
        cancelText="取消"
        variant="danger"
      />
    </div>
  )
}

// User Detail Component
export const UserDetail: React.FC = () => {
  const navigate = useNavigate()
  const { id } = useParams<{ id: string }>()
  const { currentUser, loading, fetchUserById } = useUserStore()

  useEffect(() => {
    if (id) {
      fetchUserById(id)
    }
  }, [id, fetchUserById])

  const roleLabels: Record<string, string> = {
    admin: '管理员',
    manager: '经理',
    operator: '操作员',
    viewer: '查看者',
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-xuanji-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-600">加载中...</p>
        </div>
      </div>
    )
  }

  if (!currentUser) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">未找到该用户</p>
        <Button
          variant="secondary"
          className="mt-4"
          icon={<ArrowLeft className="w-4 h-4" />}
          onClick={() => navigate('/user')}
        >
          返回列表
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          icon={<ArrowLeft className="w-4 h-4" />}
          onClick={() => navigate('/user')}
        >
          返回
        </Button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-1">用户详情</h1>
          <p className="text-gray-600">{currentUser.id}</p>
        </div>
      </div>

      {/* User Info */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Card */}
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <div className="w-24 h-24 bg-xuanji-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl font-bold text-xuanji-700">
                  {currentUser.realName?.[0] || currentUser.username?.[0] || 'U'}
                </span>
              </div>
              <h2 className="text-xl font-semibold text-gray-900 mb-1">
                {currentUser.realName || currentUser.username}
              </h2>
              <p className="text-sm text-gray-500 mb-3">{currentUser.email}</p>
              <div className="flex justify-center gap-2 mb-4">
                <StatusBadge status={currentUser.status} />
                <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
                  {roleLabels[currentUser.role] || currentUser.role}
                </span>
              </div>
              <div className="flex justify-center gap-2">
                <Button
                  variant="secondary"
                  size="sm"
                  icon={<Edit className="w-4 h-4" />}
                  onClick={() => navigate(`/user/${currentUser.id}/edit`)}
                >
                  编辑
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  icon={<Key className="w-4 h-4" />}
                >
                  重置密码
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Details Card */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>详细信息</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600 mb-1">用户名</p>
                <p className="text-sm font-medium text-gray-900">
                  {currentUser.username}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">真实姓名</p>
                <p className="text-sm font-medium text-gray-900">
                  {currentUser.realName || '-'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">邮箱</p>
                <p className="text-sm font-medium text-gray-900">
                  {currentUser.email}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">手机号</p>
                <p className="text-sm font-medium text-gray-900">
                  {currentUser.phone || '-'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">部门</p>
                <p className="text-sm font-medium text-gray-900">
                  {currentUser.department || '-'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">职位</p>
                <p className="text-sm font-medium text-gray-900">
                  {currentUser.position || '-'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">创建时间</p>
                <p className="text-sm font-medium text-gray-900">
                  {formatDate(currentUser.createdAt)}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">最后登录</p>
                <p className="text-sm font-medium text-gray-900">
                  {currentUser.lastLoginAt
                    ? formatDate(currentUser.lastLoginAt)
                    : '从未登录'}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Actions Card */}
      <Card>
        <CardHeader>
          <CardTitle>用户操作</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            {currentUser.status === 'active' ? (
              <Button
                variant="danger"
                icon={<Ban className="w-4 h-4" />}
              >
                禁用账号
              </Button>
            ) : (
              <Button
                variant="primary"
                icon={<Check className="w-4 h-4" />}
              >
                激活账号
              </Button>
            )}
            <Button
              variant="secondary"
              icon={<Shield className="w-4 h-4" />}
            >
              修改角色
            </Button>
            <Button
              variant="secondary"
              icon={<Key className="w-4 h-4" />}
            >
              重置密码
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// User Create Component
export const UserCreate: React.FC = () => {
  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: 实现创建逻辑
    navigate('/user')
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          icon={<ArrowLeft className="w-4 h-4" />}
          onClick={() => navigate('/user')}
        >
          返回
        </Button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-1">添加用户</h1>
        </div>
      </div>

      <Card>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <p className="text-gray-600">表单内容待实现...</p>
            <div className="flex gap-3">
              <Button type="submit" variant="primary">
                提交
              </Button>
              <Button type="button" variant="secondary" onClick={() => navigate('/user')}>
                取消
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

// Main User Management Module
export const UserManagementModule: React.FC = () => {
  return (
    <Routes>
      <Route index element={<UserList />} />
      <Route path="create" element={<UserCreate />} />
      <Route path=":id" element={<UserDetail />} />
    </Routes>
  )
}

export default UserManagementModule
