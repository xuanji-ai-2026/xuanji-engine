import React, { useEffect, useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Input } from '@/components/Input'
import { Modal } from '@/components/Modal'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { Plus, Edit, Trash2, Search } from 'lucide-react'
import type { RejectReason } from '@/types'

export const RejectReasonManagement: React.FC = () => {
  const [reasons, setReasons] = useState<RejectReason[]>([])
  const [loading, setLoading] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingReason, setEditingReason] = useState<RejectReason | null>(null)
  const [formData, setFormData] = useState({
    code: '',
    reason: '',
    category: '',
    isActive: true,
  })

  useEffect(() => {
    fetchReasons()
  }, [])

  const fetchReasons = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/reject-reasons')
      const data: RejectReason[] = await response.json()
      setReasons(data)
    } catch (error) {
      console.error('Failed to fetch reject reasons:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const url = editingReason
        ? `/api/reject-reasons/${editingReason.id}`
        : '/api/reject-reasons'
      const method = editingReason ? 'PUT' : 'POST'

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        await fetchReasons()
        handleCloseModal()
      }
    } catch (error) {
      console.error('Failed to save reason:', error)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除此驳回原因吗？')) return
    try {
      const response = await fetch(`/api/reject-reasons/${id}`, {
        method: 'DELETE',
      })
      if (response.ok) {
        await fetchReasons()
      }
    } catch (error) {
      console.error('Failed to delete reason:', error)
    }
  }

  const handleEdit = (reason: RejectReason) => {
    setEditingReason(reason)
    setFormData({
      code: reason.code,
      reason: reason.reason,
      category: reason.category,
      isActive: reason.isActive,
    })
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setEditingReason(null)
    setFormData({ code: '', reason: '', category: '', isActive: true })
  }

  const handleToggleStatus = async (id: string, isActive: boolean) => {
    try {
      const response = await fetch(`/api/reject-reasons/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ isActive }),
      })
      if (response.ok) {
        await fetchReasons()
      }
    } catch (error) {
      console.error('Failed to update reason status:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">驳回原因管理</h1>
          <p className="mt-1 text-sm text-gray-600">
            管理认证申请的驳回原因选项
          </p>
        </div>
        <Button onClick={() => setIsModalOpen(true)} icon={<Plus className="w-4 h-4" />}>
          添加原因
        </Button>
      </div>

      {/* List */}
      <Card>
        {loading ? (
          <div className="py-12 text-center text-gray-500">加载中...</div>
        ) : reasons.length === 0 ? (
          <div className="py-12 text-center text-gray-500">暂无驳回原因</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    编码
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    原因
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    分类
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    状态
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    创建时间
                  </th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                    操作
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {reasons.map((reason) => (
                  <tr key={reason.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <code className="text-sm text-gray-900 bg-gray-100 px-2 py-1 rounded">
                        {reason.code}
                      </code>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900">
                      {reason.reason}
                    </td>
                    <td className="px-4 py-3">
                      <Badge size="sm">{reason.category}</Badge>
                    </td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() =>
                          handleToggleStatus(reason.id, !reason.isActive)
                        }
                        className={cn(
                          'px-2 py-1 text-xs rounded-full font-medium',
                          reason.isActive
                            ? 'bg-green-100 text-green-700'
                            : 'bg-gray-100 text-gray-500'
                        )}
                      >
                        {reason.isActive ? '启用' : '禁用'}
                      </button>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {new Date(reason.createdAt).toLocaleString('zh-CN')}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEdit(reason)}
                          icon={<Edit className="w-4 h-4" />}
                        />
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDelete(reason.id)}
                          icon={<Trash2 className="w-4 h-4" />}
                        />
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      {/* Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingReason ? '编辑驳回原因' : '添加驳回原因'}
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
              编码
            </label>
            <Input
              value={formData.code}
              onChange={(value) =>
                setFormData({ ...formData, code: value })
              }
              placeholder="例如：INVALID_ID_CARD"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              原因
            </label>
            <Input
              value={formData.reason}
              onChange={(value) =>
                setFormData({ ...formData, reason: value })
              }
              placeholder="例如：身份证信息无效"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              分类
            </label>
            <Input
              value={formData.category}
              onChange={(value) =>
                setFormData({ ...formData, category: value })
              }
              placeholder="例如：资料问题"
              required
            />
          </div>
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="isActive"
              checked={formData.isActive}
              onChange={(e) =>
                setFormData({ ...formData, isActive: e.target.checked })
              }
              className="w-4 h-4 rounded border-gray-300 text-xuanji-600 focus:ring-xuanji-500"
            />
            <label htmlFor="isActive" className="text-sm text-gray-700">
              启用
            </label>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default RejectReasonManagement
