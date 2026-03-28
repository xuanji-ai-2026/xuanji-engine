import React, { useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Input } from '@/components/Input'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { Download, Calendar, Filter, FileSpreadsheet, FileText } from 'lucide-react'
import type { ExportOptions } from '@/types'

export const AuthDataExport: React.FC = () => {
  const [format, setFormat] = useState<'csv' | 'excel' | 'json'>('excel')
  const [dateRange, setDateRange] = useState({ start: '', end: '' })
  const [selectedFields, setSelectedFields] = useState<string[]>([
    'id',
    'userId',
    'userName',
    'requestType',
    'status',
    'priority',
    'createdAt',
    'reviewedAt',
  ])
  const [loading, setLoading] = useState(false)

  const availableFields = [
    { key: 'id', label: '请求ID' },
    { key: 'userId', label: '用户ID' },
    { key: 'userName', label: '用户名' },
    { key: 'requestType', label: '请求类型' },
    { key: 'status', label: '状态' },
    { key: 'priority', label: '优先级' },
    { key: 'requesterName', label: '申请人' },
    { key: 'requesterPhone', label: '手机号' },
    { key: 'reason', label: '申请原因' },
    { key: 'createdAt', label: '创建时间' },
    { key: 'updatedAt', label: '更新时间' },
    { key: 'reviewedAt', label: '审核时间' },
    { key: 'reviewedBy', label: '审核人' },
    { key: 'reviewComment', label: '审核意见' },
  ]

  const handleToggleField = (field: string) => {
    setSelectedFields((prev) =>
      prev.includes(field) ? prev.filter((f) => f !== field) : [...prev, field]
    )
  }

  const handleExport = async () => {
    setLoading(true)
    try {
      const options: ExportOptions = {
        format,
        fields: selectedFields,
        dateRange: dateRange.start && dateRange.end ? dateRange : undefined,
      }

      const response = await fetch('/api/auth-requests/export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(options),
      })

      if (!response.ok) {
        throw new Error('导出失败')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `auth-requests-${new Date().toISOString().split('T')[0]}.${format === 'csv' ? 'csv' : format === 'json' ? 'json' : 'xlsx'}`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Export failed:', error)
      alert('导出失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  const getFormatIcon = () => {
    switch (format) {
      case 'excel':
        return <FileSpreadsheet className="w-5 h-5" />
      case 'csv':
        return <FileText className="w-5 h-5" />
      case 'json':
        return <FileText className="w-5 h-5" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">认证数据导出</h1>
        <p className="mt-1 text-sm text-gray-600">
          导出认证请求数据到本地文件
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Export Options */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            导出选项
          </h3>
          <div className="space-y-4">
            {/* Format Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                导出格式
              </label>
              <div className="grid grid-cols-3 gap-3">
                {(['excel', 'csv', 'json'] as const).map((fmt) => (
                  <button
                    key={fmt}
                    onClick={() => setFormat(fmt)}
                    className={cn(
                      'flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all',
                      format === fmt
                        ? 'border-xuanji-500 bg-xuanji-50'
                        : 'border-gray-200 hover:border-gray-300'
                    )}
                  >
                    <span className="mb-2 text-gray-600">
                      {fmt === 'excel' && <FileSpreadsheet className="w-6 h-6" />}
                      {fmt === 'csv' && <FileText className="w-6 h-6" />}
                      {fmt === 'json' && <FileText className="w-6 h-6" />}
                    </span>
                    <span className="text-sm font-medium text-gray-900 capitalize">
                      {fmt}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {/* Date Range */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                日期范围
              </label>
              <div className="flex items-center gap-2">
                <div className="flex-1">
                  <Input
                    type="date"
                    value={dateRange.start}
                    onChange={(value) => setDateRange({ ...dateRange, start: value })}
                    icon={<Calendar className="w-4 h-4" />}
                  />
                </div>
                <span className="text-gray-500">至</span>
                <div className="flex-1">
                  <Input
                    type="date"
                    value={dateRange.end}
                    onChange={(value) => setDateRange({ ...dateRange, end: value })}
                    icon={<Calendar className="w-4 h-4" />}
                  />
                </div>
              </div>
            </div>
          </div>
        </Card>

        {/* Field Selection */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            选择导出字段
          </h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-gray-600">
                已选择 {selectedFields.length} 个字段
              </span>
              <button
                onClick={() =>
                  setSelectedFields(
                    selectedFields.length === availableFields.length
                      ? []
                      : availableFields.map((f) => f.key)
                  )
                }
                className="text-sm text-xuanji-600 hover:text-xuanji-700"
              >
                {selectedFields.length === availableFields.length ? '全不选' : '全选'}
              </button>
            </div>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {availableFields.map((field) => (
                <label
                  key={field.key}
                  className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg cursor-pointer"
                >
                  <input
                    type="checkbox"
                    checked={selectedFields.includes(field.key)}
                    onChange={() => handleToggleField(field.key)}
                    className="w-4 h-4 rounded border-gray-300 text-xuanji-600 focus:ring-xuanji-500"
                  />
                  <span className="text-sm text-gray-900">{field.label}</span>
                </label>
              ))}
            </div>
          </div>
        </Card>
      </div>

      {/* Preview and Export */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          预览
        </h3>
        <div className="bg-gray-50 rounded-lg p-4 mb-4">
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
            {getFormatIcon()}
            <span>文件预览</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {selectedFields.map((field) => {
              const fieldInfo = availableFields.find((f) => f.key === field)
              return (
                <Badge key={field} variant="primary" size="sm">
                  {fieldInfo?.label}
                </Badge>
              )
            })}
          </div>
          {dateRange.start && dateRange.end && (
            <p className="text-sm text-gray-600 mt-3">
              时间范围: {dateRange.start} 至 {dateRange.end}
            </p>
          )}
        </div>
        <Button
          fullWidth
          variant="primary"
          onClick={handleExport}
          loading={loading}
          disabled={selectedFields.length === 0}
          icon={<Download className="w-4 h-4" />}
        >
          导出数据
        </Button>
      </Card>
    </div>
  )
}

export default AuthDataExport
