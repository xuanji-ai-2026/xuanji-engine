import React, { useEffect, useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Input } from '@/components/Input'
import { Modal } from '@/components/Modal'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { Plus, Book, Search, Edit, Trash2, FileText, Tag } from 'lucide-react'
import type { KnowledgeEntry } from '@/types'

export const KnowledgeBase: React.FC = () => {
  const [entries, setEntries] = useState<KnowledgeEntry[]>([])
  const [loading, setLoading] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingEntry, setEditingEntry] = useState<KnowledgeEntry | null>(null)
  const [searchKeyword, setSearchKeyword] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    category: '',
    tags: [] as string[],
  })

  const categories = [
    '认证流程',
    '配置管理',
    '系统使用',
    '常见问题',
    '操作指南',
    '故障排除',
  ]

  useEffect(() => {
    fetchEntries()
  }, [searchKeyword, selectedCategory])

  const fetchEntries = async () => {
    setLoading(true)
    try {
      const queryParams = new URLSearchParams({
        ...(searchKeyword && { keyword: searchKeyword }),
        ...(selectedCategory && { category: selectedCategory }),
      })

      const response = await fetch(`/api/knowledge?${queryParams}`)
      const data: KnowledgeEntry[] = await response.json()
      setEntries(data)
    } catch (error) {
      console.error('Failed to fetch knowledge entries:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const url = editingEntry
        ? `/api/knowledge/${editingEntry.id}`
        : '/api/knowledge'
      const method = editingEntry ? 'PUT' : 'POST'

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        await fetchEntries()
        handleCloseModal()
      }
    } catch (error) {
      console.error('Failed to save entry:', error)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除此知识条目吗？')) return
    try {
      const response = await fetch(`/api/knowledge/${id}`, {
        method: 'DELETE',
      })
      if (response.ok) {
        await fetchEntries()
      }
    } catch (error) {
      console.error('Failed to delete entry:', error)
    }
  }

  const handleEdit = (entry: KnowledgeEntry) => {
    setEditingEntry(entry)
    setFormData({
      title: entry.title,
      content: entry.content,
      category: entry.category,
      tags: entry.tags,
    })
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setEditingEntry(null)
    setFormData({ title: '', content: '', category: '', tags: [] })
  }

  const addTag = (tag: string) => {
    if (tag && !formData.tags.includes(tag)) {
      setFormData({ ...formData, tags: [...formData.tags, tag] })
    }
  }

  const removeTag = (tag: string) => {
    setFormData({ ...formData, tags: formData.tags.filter((t) => t !== tag) })
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">知识库管理</h1>
          <p className="mt-1 text-sm text-gray-600">
            管理智能助手的知识库内容
          </p>
        </div>
        <Button onClick={() => setIsModalOpen(true)} icon={<Plus className="w-4 h-4" />}>
          添加知识
        </Button>
      </div>

      <Card className="p-6">
        <div className="flex items-center gap-4 mb-6">
          <div className="flex-1">
            <Input
              placeholder="搜索知识库..."
              value={searchKeyword}
              onChange={setSearchKeyword}
              icon={<Search className="w-4 h-4" />}
            />
          </div>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500"
          >
            <option value="">所有分类</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>

        {loading ? (
          <div className="py-12 text-center text-gray-500">加载中...</div>
        ) : entries.length === 0 ? (
          <div className="py-12 text-center text-gray-500">暂无知识条目</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {entries.map((entry) => (
              <div
                key={entry.id}
                className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
              >
                <div className="flex items-start gap-3 mb-3">
                  <div className="p-2 bg-xuanji-100 rounded-lg flex-shrink-0">
                    <Book className="w-5 h-5 text-xuanji-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-900 truncate">
                      {entry.title}
                    </h3>
                    <Badge size="sm" className="mt-1">
                      {entry.category}
                    </Badge>
                  </div>
                </div>

                <p className="text-sm text-gray-600 mb-3 line-clamp-3">
                  {entry.content}
                </p>

                {entry.tags && entry.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-3">
                    {entry.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center gap-1 px-2 py-0.5 bg-gray-100 text-gray-700 text-xs rounded-full"
                      >
                        <Tag className="w-3 h-3" />
                        {tag}
                      </span>
                    ))}
                  </div>
                )}

                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>
                    {new Date(entry.createdAt).toLocaleDateString('zh-CN')}
                  </span>
                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleEdit(entry)}
                      icon={<Edit className="w-3 h-3" />}
                    />
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(entry.id)}
                      icon={<Trash2 className="w-3 h-3" />}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingEntry ? '编辑知识' : '添加知识'}
        size="lg"
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
              标题
            </label>
            <Input
              value={formData.title}
              onChange={(value) => setFormData({ ...formData, title: value })}
              placeholder="输入知识标题"
              required
              icon={<FileText className="w-4 h-4" />}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              分类
            </label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500"
              required
            >
              <option value="">选择分类</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              内容
            </label>
            <textarea
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
              placeholder="输入详细内容，支持Markdown格式"
              rows={8}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              标签
            </label>
            <div className="flex gap-2 mb-2">
              <Input
                value={formData.tags.join(', ')}
                onChange={(value) => {
                  const tags = value.split(',').map((t) => t.trim()).filter(Boolean)
                  setFormData({ ...formData, tags })
                }}
                placeholder="输入标签，用逗号分隔"
              />
            </div>
            <div className="flex flex-wrap gap-2">
              {formData.tags.map((tag, index) => (
                <Badge key={index} size="sm">
                  {tag}
                  <button
                    type="button"
                    onClick={() => removeTag(tag)}
                    className="ml-1 text-red-500 hover:text-red-600"
                  >
                    ×
                  </button>
                </Badge>
              ))}
            </div>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default KnowledgeBase
