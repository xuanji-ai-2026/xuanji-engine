import React, { useEffect, useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Input } from '@/components/Input'
import { Modal } from '@/components/Modal'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { Plus, Copy, Edit, Trash2, FileCode } from 'lucide-react'
import type { ConfigTemplate } from '@/types'

export const ConfigTemplateManagement: React.FC = () => {
  const [templates, setTemplates] = useState<ConfigTemplate[]>([])
  const [loading, setLoading] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingTemplate, setEditingTemplate] = useState<ConfigTemplate | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    configType: 'system_config' as any,
    templateData: {} as Record<string, unknown>,
    isActive: true,
  })

  const configTypes = [
    'system_config',
    'network_config',
    'security_config',
    'service_config',
    'database_config',
    'api_config',
    'feature_config',
    'custom_config',
  ]

  useEffect(() => {
    fetchTemplates()
  }, [])

  const fetchTemplates = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/config-templates')
      const data: ConfigTemplate[] = await response.json()
      setTemplates(data)
    } catch (error) {
      console.error('Failed to fetch templates:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const url = editingTemplate
        ? `/api/config-templates/${editingTemplate.id}`
        : '/api/config-templates'
      const method = editingTemplate ? 'PUT' : 'POST'

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        await fetchTemplates()
        handleCloseModal()
      }
    } catch (error) {
      console.error('Failed to save template:', error)
    }
  }

  const handleDuplicate = async (template: ConfigTemplate) => {
    const response = await fetch('/api/config-templates', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...template,
        name: `${template.name} (副本)`,
        id: undefined,
        createdAt: undefined,
      }),
    })
    if (response.ok) {
      await fetchTemplates()
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除此模板吗？')) return
    try {
      const response = await fetch(`/api/config-templates/${id}`, {
        method: 'DELETE',
      })
      if (response.ok) {
        await fetchTemplates()
      }
    } catch (error) {
      console.error('Failed to delete template:', error)
    }
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setEditingTemplate(null)
    setFormData({
      name: '',
      description: '',
      configType: 'system_config',
      templateData: {},
      isActive: true,
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">配置模板管理</h1>
          <p className="mt-1 text-sm text-gray-600">
            管理配置请求的模板
          </p>
        </div>
        <Button onClick={() => setIsModalOpen(true)} icon={<Plus className="w-4 h-4" />}>
          添加模板
        </Button>
      </div>

      <Card className="p-6">
        {loading ? (
          <div className="py-12 text-center text-gray-500">加载中...</div>
        ) : templates.length === 0 ? (
          <div className="py-12 text-center text-gray-500">暂无模板</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {templates.map((template) => (
              <div
                key={template.id}
                className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <div className="p-2 bg-xuanji-100 rounded-lg">
                      <FileCode className="w-4 h-4 text-xuanji-600" />
                    </div>
                    <div>
                      <span className="font-medium text-gray-900 block">
                        {template.name}
                      </span>
                      <span className="text-xs text-gray-500">
                        v{template.version}
                      </span>
                    </div>
                  </div>
                  <Badge size="sm" variant={template.isActive ? 'success' : 'warning'}>
                    {template.isActive ? '启用' : '禁用'}
                  </Badge>
                </div>

                <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                  {template.description}
                </p>

                <div className="flex items-center gap-2 mb-3">
                  <Badge size="sm">{template.configType}</Badge>
                </div>

                <div className="flex items-center justify-between">
                  <div className="text-xs text-gray-500">
                    {Object.keys(template.templateData).length} 个配置项
                  </div>
                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDuplicate(template)}
                      icon={<Copy className="w-4 h-4" />}
                    />
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(template.id)}
                      icon={<Trash2 className="w-4 h-4" />}
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
        title={editingTemplate ? '编辑模板' : '添加模板'}
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
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                模板名称
              </label>
              <Input
                value={formData.name}
                onChange={(value) => setFormData({ ...formData, name: value })}
                placeholder="输入模板名称"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                配置类型
              </label>
              <select
                value={formData.configType}
                onChange={(e) => setFormData({ ...formData, configType: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500"
                required
              >
                {configTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              描述
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="描述模板的用途..."
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              模板数据 (JSON)
            </label>
            <textarea
              value={JSON.stringify(formData.templateData, null, 2)}
              onChange={(e) => {
                try {
                  setFormData({ ...formData, templateData: JSON.parse(e.target.value) })
                } catch {
                  // Invalid JSON, ignore
                }
              }}
              rows={8}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500 focus:border-transparent font-mono text-sm"
            />
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="isActive"
              checked={formData.isActive}
              onChange={(e) => setFormData({ ...formData, isActive: e.target.checked })}
              className="w-4 h-4 rounded border-gray-300 text-xuanji-600 focus:ring-xuanji-500"
            />
            <label htmlFor="isActive" className="text-sm text-gray-700">
              启用模板
            </label>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default ConfigTemplateManagement
