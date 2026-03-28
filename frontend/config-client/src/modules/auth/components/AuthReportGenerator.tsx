import React, { useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Input } from '@/components/Input'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { Calendar, FileText, BarChart, PieChart, LineChart } from 'lucide-react'
import type { ReportParams } from '@/types'

export const AuthReportGenerator: React.FC = () => {
  const [reportType, setReportType] = useState<'summary' | 'detailed' | 'trend' | 'analysis'>('summary')
  const [dateRange, setDateRange] = useState({ start: '', end: '' })
  const [format, setFormat] = useState<'pdf' | 'excel' | 'csv'>('pdf')
  const [loading, setLoading] = useState(false)

  const reportTypes = [
    {
      id: 'summary' as const,
      name: '汇总报表',
      description: '认证请求的整体统计数据',
      icon: <BarChart className="w-6 h-6" />,
    },
    {
      id: 'detailed' as const,
      name: '详细报表',
      description: '每条认证请求的详细信息',
      icon: <FileText className="w-6 h-6" />,
    },
    {
      id: 'trend' as const,
      name: '趋势报表',
      description: '认证请求的时间趋势分析',
      icon: <LineChart className="w-6 h-6" />,
    },
    {
      id: 'analysis' as const,
      name: '分析报表',
      description: '深入的数据分析和洞察',
      icon: <PieChart className="w-6 h-6" />,
    },
  ]

  const handleGenerate = async () => {
    if (!dateRange.start || !dateRange.end) {
      alert('请选择日期范围')
      return
    }

    setLoading(true)
    try {
      const params: ReportParams = {
        type: reportType,
        startDate: dateRange.start,
        endDate: dateRange.end,
        format,
      }

      const response = await fetch('/api/auth-reports/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
      })

      if (!response.ok) {
        throw new Error('生成报表失败')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `auth-report-${reportType}-${new Date().toISOString().split('T')[0]}.${format === 'csv' ? 'csv' : format === 'excel' ? 'xlsx' : 'pdf'}`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Failed to generate report:', error)
      alert('生成报表失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  const handlePreview = async () => {
    if (!dateRange.start || !dateRange.end) {
      alert('请选择日期范围')
      return
    }

    try {
      const params = new URLSearchParams({
        type: reportType,
        startDate: dateRange.start,
        endDate: dateRange.end,
      })

      window.open(`/api/auth-reports/preview?${params}`, '_blank')
    } catch (error) {
      console.error('Failed to preview report:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">认证报表生成</h1>
        <p className="mt-1 text-sm text-gray-600">
          生成各类认证统计报表
        </p>
      </div>

      {/* Report Type Selection */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          选择报表类型
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {reportTypes.map((type) => (
            <button
              key={type.id}
              onClick={() => setReportType(type.id)}
              className={cn(
                'p-4 rounded-lg border-2 transition-all text-left',
                reportType === type.id
                  ? 'border-xuanji-500 bg-xuanji-50'
                  : 'border-gray-200 hover:border-gray-300'
              )}
            >
              <div className="flex items-center gap-3 mb-2">
                <div
                  className={cn(
                    'p-2 rounded-lg',
                    reportType === type.id ? 'bg-xuanji-100 text-xuanji-600' : 'bg-gray-100 text-gray-600'
                  )}
                >
                  {type.icon}
                </div>
                <span className="font-medium text-gray-900">{type.name}</span>
              </div>
              <p className="text-sm text-gray-600">{type.description}</p>
            </button>
          ))}
        </div>
      </Card>

      {/* Date Range and Format */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            日期范围
          </h3>
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <Input
                  type="date"
                  label="开始日期"
                  value={dateRange.start}
                  onChange={(value) => setDateRange({ ...dateRange, start: value })}
                  icon={<Calendar className="w-4 h-4" />}
                />
              </div>
              <span className="text-gray-500 mt-6">至</span>
              <div className="flex-1">
                <Input
                  type="date"
                  label="结束日期"
                  value={dateRange.end}
                  onChange={(value) => setDateRange({ ...dateRange, end: value })}
                  icon={<Calendar className="w-4 h-4" />}
                />
              </div>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-blue-700">
                💡 提示：日期范围最大支持365天
              </p>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            导出格式
          </h3>
          <div className="space-y-3">
            {(['pdf', 'excel', 'csv'] as const).map((fmt) => (
              <label
                key={fmt}
                className={cn(
                  'flex items-center gap-3 p-4 rounded-lg border-2 cursor-pointer transition-all',
                  format === fmt
                    ? 'border-xuanji-500 bg-xuanji-50'
                    : 'border-gray-200 hover:border-gray-300'
                )}
              >
                <input
                  type="radio"
                  name="format"
                  value={fmt}
                  checked={format === fmt}
                  onChange={(e) => setFormat(e.target.value as 'pdf' | 'excel' | 'csv')}
                  className="w-4 h-4 text-xuanji-600"
                />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 capitalize">
                    {fmt.toUpperCase()}
                  </p>
                  <p className="text-xs text-gray-600">
                    {fmt === 'pdf' && '适合打印和分享'}
                    {fmt === 'excel' && '适合进一步分析'}
                    {fmt === 'csv' && '适合数据导入'}
                  </p>
                </div>
              </label>
            ))}
          </div>
        </Card>
      </div>

      {/* Preview and Generate */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          报表预览
        </h3>
        <div className="bg-gray-50 rounded-lg p-6 mb-4">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h4 className="text-lg font-medium text-gray-900">
                {reportTypes.find((t) => t.id === reportType)?.name}
              </h4>
              {dateRange.start && dateRange.end && (
                <p className="text-sm text-gray-600 mt-1">
                  {dateRange.start} 至 {dateRange.end}
                </p>
              )}
            </div>
            <Badge variant="primary" size="md">
              {format.toUpperCase()}
            </Badge>
          </div>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="p-4 bg-white rounded-lg">
              <p className="text-2xl font-bold text-xuanji-600">
                {reportType === 'summary' ? '12' : reportType === 'detailed' ? '156' : reportType === 'trend' ? '6' : '8'}
              </p>
              <p className="text-sm text-gray-600 mt-1">数据点</p>
            </div>
            <div className="p-4 bg-white rounded-lg">
              <p className="text-2xl font-bold text-green-600">
                {reportType === 'summary' ? '92%' : reportType === 'detailed' ? '100%' : reportType === 'trend' ? '+15%' : '85%'}
              </p>
              <p className="text-sm text-gray-600 mt-1">准确率</p>
            </div>
            <div className="p-4 bg-white rounded-lg">
              <p className="text-2xl font-bold text-blue-600">
                {reportType === 'summary' ? '1.2s' : reportType === 'detailed' ? '3.5s' : reportType === 'trend' ? '2.1s' : '2.8s'}
              </p>
              <p className="text-sm text-gray-600 mt-1">预计耗时</p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="secondary"
            onClick={handlePreview}
            disabled={!dateRange.start || !dateRange.end}
            icon={<FileText className="w-4 h-4" />}
          >
            预览报表
          </Button>
          <Button
            variant="primary"
            onClick={handleGenerate}
            loading={loading}
            disabled={!dateRange.start || !dateRange.end}
            icon={<BarChart className="w-4 h-4" />}
          >
            生成报表
          </Button>
        </div>
      </Card>
    </div>
  )
}

export default AuthReportGenerator
