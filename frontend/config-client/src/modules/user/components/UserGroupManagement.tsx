import React, { useEffect, useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Input } from '@/components/Input'
import { Modal } from '@/components/Modal'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { Plus, Users, Edit, Trash2, Search } from 'lucide-react'
import type { UserGroup, User } from '@/types'

export const UserGroupManagement: React.FC = () => {
  const [groups, setGroups] = useState<UserGroup[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingGroup, setEditingGroup] = useState<UserGroup | null>(null)
  const [searchKeyword, setSearchKeyword] = useState('')
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    userIds: [] as string[],
  })

  useEffect(() => {
    fetchGroups()
    fetchUsers()
  }, [])

  const fetchGroups = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/user-groups')
      const data: UserGroup[] = await response.json()
      setGroups(data)
    } catch (error) {
      console.error('Failed to fetch groups:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchUsers = async () => {
    try {
      const response = await fetch('/api/users')
      const data: User[] = await response.json()
      setUsers(data)
    } catch (error) {
      console.error('Failed to fetch users:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const url = editingGroup
        ? `/api/user-groups/${editingGroup.id}`
        : '/api/user-groups'
      const method = editingGroup ? 'PUT' : 'POST'

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        await fetchGroups()
        handleCloseModal()
      }
    } catch (error) {
      console.error('Failed to save group:', error)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除此用户组吗？')) return
    try {
      const response = await fetch(`/api/user-groups/${id}`, {
        method: 'DELETE',
      })
      if (response.ok) {
        await fetchGroups()
      }
    } catch (error) {
      console.error('Failed to delete group:', error)
    }
  }

  const handleEdit = (group: UserGroup) => {
    setEditingGroup(group)
    setFormData({
      name: group.name,
      description: group.description || '',
      userIds: group.userIds,
    })
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setEditingGroup(null)
    setFormData({ name: '', description: '', userIds: [] })
  }

  const toggleUserSelection = (userId: string) => {
    setFormData((prev) => ({
      ...prev,
      userIds: prev.userIds.includes(userId)
        ? prev.userIds.filter((id) => id !== userId)
        : [...prev.userIds, userId],
    }))
  }

  const filteredUsers = searchKeyword
    ? users.filter(
        (user) =>
          user.username.toLowerCase().includes(searchKeyword.toLowerCase()) ||
          user.email.toLowerCase().includes(searchKeyword.toLowerCase()) ||
          user.realName.toLowerCase().includes(searchKeyword.toLowerCase())
      )
    : users

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">用户分组管理</h1>
          <p className="mt-1 text-sm text-gray-600">
            管理用户分组和成员
          </p>
        </div>
        <Button onClick={() => setIsModalOpen(true)} icon={<Plus className="w-4 h-4" />}>
          创建分组
        </Button>
      </div>

      <Card className="p-6">
        {loading ? (
          <div className="py-12 text-center text-gray-500">加载中...</div>
        ) : groups.length === 0 ? (
          <div className="py-12 text-center text-gray-500">暂无用户分组</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {groups.map((group) => (
              <div
                key={group.id}
                className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-xuanji-100 rounded-lg">
                      <Users className="w-5 h-5 text-xuanji-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">
                        {group.name}
                      </h3>
                      <Badge size="sm" className="mt-1">
                        {group.userIds.length} 成员
                      </Badge>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleEdit(group)}
                      icon={<Edit className="w-4 h-4" />}
                    />
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(group.id)}
                      icon={<Trash2 className="w-4 h-4" />}
                    />
                  </div>
                </div>

                {group.description && (
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                    {group.description}
                  </p>
                )}

                <div className="text-xs text-gray-500">
                  创建时间: {new Date(group.createdAt).toLocaleDateString('zh-CN')}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingGroup ? '编辑分组' : '创建分组'}
        size="lg"
        actions={
          <div className="flex items-center justify-end gap-3">
            <Button variant="ghost" onClick={handleCloseModal}>
              取消
            </Button>
            <Button onClick={handleSubmit}>保存</Button>
          </div>
        }
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              分组名称
            </label>
            <Input
              value={formData.name}
              onChange={(value) => setFormData({ ...formData, name: value })}
              placeholder="输入分组名称"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              描述
            </label>
            <textarea
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              placeholder="输入分组描述（可选）"
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              选择成员
            </label>
            <div className="mb-3">
              <Input
                placeholder="搜索用户..."
                value={searchKeyword}
                onChange={(e) => setSearchKeyword(e.target.value)}
                icon={<Search className="w-4 h-4" />}
              />
            </div>
            <div className="border border-gray-200 rounded-lg max-h-64 overflow-y-auto">
              {filteredUsers.length === 0 ? (
                <div className="p-4 text-center text-gray-500">
                  没有找到用户
                </div>
              ) : (
                filteredUsers.map((user) => (
                  <label
                    key={user.id}
                    className="flex items-center gap-3 p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                  >
                    <input
                      type="checkbox"
                      checked={formData.userIds.includes(user.id)}
                      onChange={() => toggleUserSelection(user.id)}
                      className="w-4 h-4 rounded border-gray-300 text-xuanji-600 focus:ring-xuanji-500"
                    />
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-medium text-gray-900">
                          {user.realName || user.username}
                        </span>
                        <Badge size="sm" variant={user.status === 'active' ? 'success' : 'warning'}>
                          {user.status}
                        </Badge>
                      </div>
                      <div className="text-xs text-gray-600 mt-0.5">
                        {user.email}
                      </div>
                    </div>
                  </label>
                ))
              )}
            </div>
            <div className="mt-2 text-sm text-gray-600">
              已选择 {formData.userIds.length} 位用户
            </div>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default UserGroupManagement
