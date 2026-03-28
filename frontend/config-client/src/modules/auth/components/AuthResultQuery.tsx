import React, { useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Input } from '@/components/Input'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { Search, FileText, CheckCircle, XCircle, Clock } from 'lucide-react'
import type { AuthRequest } from '@/types'

export const AuthResultQuery: React.FC = () => {
  const [queryType, setQueryType] = useState<'request_id' | 'phone' | 'email'>('request_id')
  const [queryValue, setQueryValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AuthRequest | null>(null)
  const [error, setError] = useState('')

  const handleQuery = async () => {
    if (!queryValue.trim()) {
      setError('请输入查询值')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const queryParams = new URLSearchParams({
        type: queryType,
        value: queryValue.trim(),
      })

      const response = await fetch(`/api/auth-requests/query?${queryParams}`)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || '查询失败')
      }

      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : '查询失败，请检查输入信息')
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, 'success' | 'danger' | 'warning' | 'primary'> = {
      approved: 'success',
      rejected: 'danger',
      pending: 'warning',
      processing: 'primary',
    }
    const labels: Record<string, string> = {
      approved: '已通过',
      rejected: '已驳回',
      pending: '待处理',
      processing: '处理中',
    }
    return (
      <Badge variant={variants[status] || 'primary'} size="md">
        {labels[status] || status}
      </Badge>
    )
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'approved':
        return <CheckCircle className="w-12 h-12 text-green-500" />
      case 'rejected':
        return <XCircle className="w-12 h-12 text-red-500" />
      case 'pending':
      case 'processing':
        return <Clock className="w-12 h-12 text-blue-500" />
      default:
        return <FileText className="w-12 h-12 text-gray-500" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">认证结果查询</h1>
        <p className="mt-1 text-sm text-gray-600">
          查询认证申请的处理结果和进度
        </p>
      </div>

      {/* Query Form */}
      <Card className="p-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              查询方式
            </label>
            <div className="flex gap-4">
              <button
                onClick={() => setQueryType('request_id')}
                className={cn(
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  queryType === 'request_id'
                    ? 'bg-xuanji-100 text-xuanji-700'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                )}
              >
                请求ID
              </button>
              <button
                onClick={() => setQueryType('phone')}
                className={cn(
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  queryType === 'phone'
                    ? 'bg-xuanji-100 text-xuanji-700'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                )}
              >
                手机号码
              </button>
              <button
                onClick={() => setQueryType('email')}
                className={cn(
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  queryType === 'email'
                    ? 'bg-xuanji-100 text-xuanji-700'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                )}
              >
                邮箱地址
              </button>
            </div>
          </div>

          <div className="flex gap-3">
            <Input
              placeholder={
                queryType === 'request_id'
                  ? '请输入请求ID'
                  : queryType === 'phone'
                    ? '请输入手机号码'
                    : '请输入邮箱地址'
              }
              value={queryValue}
              onChange={setQueryValue}
              icon={<Search className="w-4 h-4" />}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleQuery()
                }
              }}
            />
            <Button onClick={handleQuery} loading={loading}>
              查询
            </Button>
          </div>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}
        </div>
      </Card>

      {/* Result */}
      {result && (
        <Card className="p-6">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                认证申请详情
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                请求ID: {result.id}
              </p>
            </div>
            {getStatusBadge(result.status)}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Status Icon */}
            <div className="flex flex-col items-center justify-center p-6 bg-gray-50 rounded-lg">
              {getStatusIcon(result.status)}
              <p className="mt-4 text-sm font-medium text-gray-900">
                {result.status === 'approved' && '认证通过'}
                {result.status === 'rejected' && '认证失败'}
                {result.status === 'pending' && '待处理'}
                {result.status === 'processing' && '处理中'}
              </p>
            </div>

            {/* Details */}
            <div className="lg:col-span-2 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500 mb-1">申请人</p>
                  <p className="text-sm font-medium text-gray-900">
                    {result.requesterName}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">申请类型</p>
                  <p className="text-sm text-gray-900">
                    {result.requestType}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">手机号码</p>
                  <p className="text-sm text-gray-900">
                    {result.requesterPhone || '-'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">优先级</p>
                  <Badge size="sm">{result.priority}</Badge>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">申请时间</p>
                  <p className="text-sm text-gray-900">
                    {new Date(result.createdAt).toLocaleString('zh-CN')}
                  </p>
                </div>
                {result.reviewedAt && (
                  <div>
                    <p className="text-sm text-gray-500 mb-1">审核时间</p>
                    <p className="text-sm text-gray-900">
                      {new Date(result.reviewedAt).toLocaleString('zh-CN')}
                    </p>
                  </div>
                )}
              </div>

              <div>
                <p className="text-sm text-gray-500 mb-1">申请原因</p>
                <p className="text-sm text-gray-900 bg-gray-50 p-3 rounded-lg">
                  {result.reason}
                </p>
              </div>

              {result.reviewComment && (
                <div>
                  <p className="text-sm text-gray-500 mb-1">审核意见</p>
                  <p className="text-sm text-gray-900 bg-gray-50 p-3 rounded-lg">
                    {result.reviewComment}
                  </p>
                </div>
              )}

              {result.attachments && result.attachments.length > 0 && (
                <div>
                  <p className="text-sm text-gray-500 mb-2">附件</p>
                  <div className="flex flex-wrap gap-2">
                    {result.attachments.map((attachment, index) => (
                      <a
                        key={index}
                        href={attachment}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 px-3 py-1.5 bg-gray-100 rounded-lg text-sm text-gray-700 hover:bg-gray-200"
                      >
                        <FileText className="w-4 h-4" />
                        附件 {index + 1}
                      </a>
                    ))}
                  </div>
                </div>
              )}

              {result.status === 'rejected' && (
                <div className="mt-4">
                  <Button variant="primary" size="sm" onClick={() => {
                    // TODO: 打开申诉页面
                    alert('申诉功能开发中')
                  }}>
                    申请申诉
                  </Button>
                </div>
              )}
            </div>
          </div>
        </Card>
      )}
    </div>
  )
}

export default AuthResultQuery
