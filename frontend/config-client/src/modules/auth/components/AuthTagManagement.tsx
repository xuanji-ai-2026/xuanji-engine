import React, { useEffect, useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Input } from '@/components/Input'
import { Modal } from '@/components/Modal'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { Plus, Edit, Trash2, Tag, Hash } from 'lucide-react'
import type { AuthTag } from '@/types'

export const AuthTagManagement: React.FC = () => {
  const [tags, setTags] = useState<AuthTag[]>([])
  const [loading, setLoading] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingTag, setEditingTag] = useState<AuthTag | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    color: '#3B82F6',
    description: '',
  })

  const colorOptions = [
    '#EF4444', // red
    '#F97316', // orange
    '#F59E0B', // amber
    '#EAB308', // yellow
    '#84CC16', // lime
    '#22C55E', // green
    '#10B981', // emerald
    '#14B8A6', // teal
    '#06B6D4', // cyan
    '#0EA5E9', // sky
    '#3B82F6', // blue
    '#6366F1', // indigo
    '#8B5CF6', // violet
    '#A855F7', // purple
    '#D946EF', // fuchsia
    '#EC4899', // pink
  ]

  useEffect(() => {
    fetchTags()
  }, [])

  const fetchTags = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/auth-tags')
      const data: AuthTag[] = await response.json()
      setTags(data)
    } catch (error) {
      console.error('Failed to fetch tags:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const url = editingTag
        ? `/api/auth-tags/${editingTag.id}`
        : '/api/auth-tags'
      const method = editingTag ? 'PUT' : 'POST'

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        await fetchTags()
        handleCloseModal()
      }
    } catch (error) {
      console.error('Failed to save tag:', error)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除此标签吗？')) return
    try {
      const response = await fetch(`/api/auth-tags/${id}`, {
        method: 'DELETE',
      })
      if (response.ok) {
        await fetchTags()
      }
    } catch (error) {
      console.error('Failed to delete tag:', error)
    }
  }

  const handleEdit = (tag: AuthTag) => {
    setEditingTag(tag)
    setFormData({
      name: tag.name,
      color: tag.color,
      description: tag.description || '',
    })
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setEditingTag(null)
    setFormData({ name: '', color: '#3B82F6', description: '' })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">认证标签管理</h1>
          <p className="mt-1 text-sm text-gray-600">
            管理用于标记认证申请的标签
          </p>
        </div>
        <Button onClick={() => setIsModalOpen(true)} icon={<Plus className="w-4 h-4" />}>
          添加标签
        </Button>
      </div>

      {/* Tags List */}
      <Card className="p-6">
        {loading ? (
          <div className="py-12 text-center text-gray-500">加载中...</div>
        ) : tags.length === 0 ? (
          <div className="py-12 text-center text-gray-500">暂无标签</div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {tags.map((tag) => (
              <div
                key={tag.id}
                className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: tag.color }}
                    />
                    <span className="font-medium text-gray-900">{tag.name}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleEdit(tag)}
                      icon={<Edit className="w-4 h-4" />}
                    />
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(tag.id)}
                      icon={<Trash2 className="w-4 h-4" />}
                    />
                  </div>
                </div>
                {tag.description && (
                  <p className="text-sm text-gray-600 mb-2">{tag.description}</p>
                )}
                <div className="flex items-center gap-2">
                  <Badge size="sm">{tag.name}</Badge>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingTag ? '编辑标签' : '添加标签'}
        footer={
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
              标签名称
            </label>
            <Input
              value={formData.name}
              onChange={(value) => setFormData({ ...formData, name: value })}
              placeholder="例如：紧急、VIP、需要补充资料"
              required
              icon={<Tag className="w-4 h-4" />}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              标签颜色
            </label>
            <div className="grid grid-cols-8 gap-2">
              {colorOptions.map((color) => (
                <button
                  key={color}
                  type="button"
                  onClick={() => setFormData({ ...formData, color })}
                  className={cn(
                    'w-8 h-8 rounded-full border-2 transition-all',
                    formData.color === color
                      ? 'border-gray-900 scale-110'
                      : 'border-transparent hover:scale-105'
                  )}
                  style={{ backgroundColor: color }}
                />
              ))}
            </div>
            <div className="mt-3 flex items-center gap-2">
              <span className="text-sm text-gray-600">当前选择:</span>
              <div
                className="w-6 h-6 rounded-full"
                style={{ backgroundColor: formData.color }}
              />
              <span className="text-sm font-mono text-gray-900">
                {formData.color}
              </span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              描述（可选）
            </label>
            <textarea
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              placeholder="描述此标签的用途..."
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500 focus:border-transparent"
            />
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default AuthTagManagement
