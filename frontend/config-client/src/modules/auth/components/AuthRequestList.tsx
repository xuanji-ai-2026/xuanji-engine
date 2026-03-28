import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthRequestStore } from '@/stores/authRequestStore'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/Card'
import { StatusBadge } from '@/components/Badge'
import { PriorityBadge } from '@/components/Badge'
import { Select } from '@/components/Input'
import { cn, formatRelativeTime } from '@/utils'
import {
  Search,
  Filter,
  Plus,
  ShieldCheck,
  RefreshCw,
} from 'lucide-react'

export const AuthRequestList: React.FC = () => {
  const navigate = useNavigate()
  const {
    requests,
    loading,
    total,
    filters,
    pagination,
    fetchRequests,
    setFilters,
    setPagination,
  } = useAuthRequestStore()

  const [searchKeyword, setSearchKeyword] = useState('')

  useEffect(() => {
    fetchRequests()
  }, [fetchRequests])

  useEffect(() => {
    if (searchKeyword !== filters.keyword) {
      setFilters({ ...filters, keyword: searchKeyword })
    }
  }, [searchKeyword, filters, setFilters])

  const handleSearch = () => {
    setFilters({ ...filters, keyword: searchKeyword })
    fetchRequests()
  }

  const handleRefresh = () => {
    fetchRequests()
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-1">认证协助</h1>
          <p className="text-gray-600">管理和处理用户认证请求</p>
        </div>
        <Button
          variant="primary"
          icon={<RefreshCw className="w-4 h-4" />}
          onClick={handleRefresh}
          loading={loading}
        >
          刷新
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent padding="sm">
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex-1 min-w-[200px]">
              <Input
                placeholder="搜索请求ID、用户名、理由..."
                leftIcon={<Search className="w-4 h-4" />}
                value={searchKeyword}
                onChange={(e) => setSearchKeyword(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <Select
              options={[
                { label: '全部状态', value: '' },
                { label: '待处理', value: 'pending' },
                { label: '已批准', value: 'approved' },
                { label: '已拒绝', value: 'rejected' },
                { label: '处理中', value: 'processing' },
              ]}
              defaultValue=""
              onChange={(e) => {
                const status = e.target.value
                  ? [e.target.value]
                  : undefined
                setFilters({ ...filters, status })
              }}
            />
            <Select
              options={[
                { label: '全部优先级', value: '' },
                { label: '低', value: 'low' },
                { label: '中', value: 'medium' },
                { label: '高', value: 'high' },
                { label: '紧急', value: 'urgent' },
              ]}
              defaultValue=""
              onChange={(e) => {
                const priority = e.target.value
                  ? [e.target.value]
                  : undefined
                setFilters({ ...filters, priority })
              }}
            />
          </div>
        </CardContent>
      </Card>

      {/* Request List */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>
              认证请求 ({total})
            </CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-12">
              <RefreshCw className="w-8 h-8 text-xuanji-600 animate-spin mx-auto mb-4" />
              <p className="text-gray-600">加载中...</p>
            </div>
          ) : requests.length === 0 ? (
            <div className="text-center py-12">
              <ShieldCheck className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">暂无认证请求</p>
            </div>
          ) : (
            <div className="space-y-3">
              {requests.map((request) => (
                <div
                  key={request.id}
                  className={cn(
                    'flex items-start gap-4 p-4 border border-gray-200 rounded-lg hover:border-xuanji-300 hover:bg-xuanji-50 transition-all cursor-pointer',
                    request.priority === 'urgent' && 'border-l-4 border-l-red-500',
                  )}
                  onClick={() => navigate(`/auth/${request.id}`)}
                >
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 bg-xuanji-100 rounded-full flex items-center justify-center">
                      <ShieldCheck className="w-5 h-5 text-xuanji-600" />
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="text-sm font-medium text-gray-900">
                        {request.requesterName}
                      </h3>
                      <StatusBadge status={request.status} />
                      <PriorityBadge priority={request.priority} />
                    </div>
                    <p className="text-sm text-gray-600 mb-1">
                      {request.reason}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <span>类型: {request.requestType}</span>
                      <span>创建时间: {formatRelativeTime(request.createdAt)}</span>
                    </div>
                  </div>
                  <button className="flex-shrink-0 p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg">
                    →
                  </button>
                </div>
              ))}
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
                    fetchRequests()
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
                    fetchRequests()
                  }}
                >
                  下一页
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default AuthRequestList
