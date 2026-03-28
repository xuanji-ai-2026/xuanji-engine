import React, { useEffect, useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Input } from '@/components/Input'
import { Modal } from '@/components/Modal'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { AlertCircle, CheckCircle, XCircle, Clock, FileText, Eye, Download } from 'lucide-react'
import type { Appeal, SearchFilters } from '@/types'

export const AppealManagement: React.FC = () => {
  const [appeals, setAppeals] = useState<Appeal[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedAppeal, setSelectedAppeal] = useState<Appeal | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [reviewComment, setReviewComment] = useState('')
  const [filters, setFilters] = useState<SearchFilters>({})

  useEffect(() => {
    fetchAppeals()
  }, [filters])

  const fetchAppeals = async () => {
    setLoading(true)
    try {
      const queryParams = new URLSearchParams({
        ...(filters.status && { status: filters.status.join(',') }),
      })

      const response = await fetch(`/api/auth-appeals?${queryParams}`)
      const data: Appeal[] = await response.json()
      setAppeals(data)
    } catch (error) {
      console.error('Failed to fetch appeals:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenReview = (appeal: Appeal) => {
    setSelectedAppeal(appeal)
    setIsModalOpen(true)
  }

  const handleApproveAppeal = async () => {
    if (!selectedAppeal) return
    try {
      const response = await fetch(`/api/auth-appeals/${selectedAppeal.id}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment: reviewComment }),
      })
      if (response.ok) {
        await fetchAppeals()
        handleCloseModal()
      }
    } catch (error) {
      console.error('Failed to approve appeal:', error)
    }
  }

  const handleRejectAppeal = async () => {
    if (!selectedAppeal) return
    try {
      const response = await fetch(`/api/auth-appeals/${selectedAppeal.id}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment: reviewComment }),
      })
      if (response.ok) {
        await fetchAppeals()
        handleCloseModal()
      }
    } catch (error) {
      console.error('Failed to reject appeal:', error)
    }
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setSelectedAppeal(null)
    setReviewComment('')
  }

  const getStatusBadge = (status: Appeal['status']) => {
    const variants: Record<string, 'primary' | 'success' | 'danger' | 'warning'> = {
      pending: 'warning',
      under_review: 'primary',
      approved: 'success',
      rejected: 'danger',
    }
    const labels: Record<string, string> = {
      pending: '待处理',
      under_review: '审核中',
      approved: '已通过',
      rejected: '已驳回',
    }
    return (
      <Badge variant={variants[status]} size="sm">
        {labels[status]}
      </Badge>
    )
  }

  const getStatusIcon = (status: Appeal['status']) => {
    switch (status) {
      case 'approved':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'rejected':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'under_review':
        return <Eye className="w-5 h-5 text-blue-500" />
      default:
        return <Clock className="w-5 h-5 text-yellow-500" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">申诉处理</h1>
          <p className="mt-1 text-sm text-gray-600">
            处理用户对认证结果的申诉
          </p>
        </div>
        <div className="flex items-center gap-2">
          {['pending', 'under_review'].map((status) => (
            <button
              key={status}
              onClick={() =>
                setFilters({
                  status: filters.status?.includes(status)
                    ? filters.status.filter((s) => s !== status)
                    : [...(filters.status || []), status],
                })
              }
              className={cn(
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                filters.status?.includes(status)
                  ? 'bg-xuanji-100 text-xuanji-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              )}
            >
              {status === 'pending' ? '待处理' : '审核中'}
            </button>
          ))}
        </div>
      </div>

      {/* Appeals List */}
      <div className="grid grid-cols-1 gap-4">
        {loading ? (
          <div className="py-12 text-center text-gray-500">加载中...</div>
        ) : appeals.length === 0 ? (
          <div className="py-12 text-center text-gray-500">暂无申诉记录</div>
        ) : (
          appeals.map((appeal) => (
            <Card key={appeal.id} className="p-6">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 mt-1">
                  {getStatusIcon(appeal.status)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {appeal.userName} 的申诉
                      </h3>
                      <p className="text-sm text-gray-600 mt-1">
                        请求ID: {appeal.requestId}
                      </p>
                    </div>
                    {getStatusBadge(appeal.status)}
                  </div>

                  <div className="bg-gray-50 rounded-lg p-4 mb-3">
                    <p className="text-sm font-medium text-gray-700 mb-2">
                      申诉原因
                    </p>
                    <p className="text-sm text-gray-900">{appeal.reason}</p>
                  </div>

                  {appeal.evidence && appeal.evidence.length > 0 && (
                    <div className="mb-3">
                      <p className="text-sm text-gray-600 mb-2">
                        申诉证据 ({appeal.evidence.length} 份)
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {appeal.evidence.map((evidence, index) => (
                          <a
                            key={index}
                            href={evidence}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 px-3 py-1.5 bg-gray-100 rounded-lg text-sm text-gray-700 hover:bg-gray-200"
                          >
                            <FileText className="w-4 h-4" />
                            证据 {index + 1}
                          </a>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="flex items-center justify-between">
                    <div className="text-sm text-gray-500">
                      <span>提交时间: {new Date(appeal.createdAt).toLocaleString('zh-CN')}</span>
                      {appeal.updatedAt !== appeal.createdAt && (
                        <span className="ml-4">
                          更新时间: {new Date(appeal.updatedAt).toLocaleString('zh-CN')}
                        </span>
                      )}
                    </div>
                    {appeal.status === 'pending' || appeal.status === 'under_review' ? (
                      <Button
                        variant="primary"
                        size="sm"
                        onClick={() => handleOpenReview(appeal)}
                        icon={<AlertCircle className="w-4 h-4" />}
                      >
                        处理申诉
                      </Button>
                    ) : appeal.reviewComment ? (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleOpenReview(appeal)}
                      >
                        查看详情
                      </Button>
                    ) : null}
                  </div>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>

      {/* Review Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title="处理申诉"
        size="lg"
        footer={
          <div className="flex items-center justify-between">
            <Button variant="ghost" onClick={handleCloseModal}>
              取消
            </Button>
            {selectedAppeal && (
              selectedAppeal.status === 'pending' || selectedAppeal.status === 'under_review'
            ) && (
              <div className="flex items-center gap-2">
                <Button
                  variant="danger"
                  onClick={handleRejectAppeal}
                  icon={<XCircle className="w-4 h-4" />}
                >
                  驳回申诉
                </Button>
                <Button
                  variant="primary"
                  onClick={handleApproveAppeal}
                  icon={<CheckCircle className="w-4 h-4" />}
                >
                  通过申诉
                </Button>
              </div>
            )}
          </div>
        }
      >
        {selectedAppeal && (
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">
                申诉信息
              </h4>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">申请人</span>
                  <span className="text-sm font-medium text-gray-900">
                    {selectedAppeal.userName}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">原始请求ID</span>
                  <span className="text-sm text-gray-900">
                    {selectedAppeal.requestId}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">当前状态</span>
                  {getStatusBadge(selectedAppeal.status)}
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">
                申诉原因
              </h4>
              <p className="text-sm text-gray-900 bg-gray-50 p-4 rounded-lg">
                {selectedAppeal.reason}
              </p>
            </div>

            {selectedAppeal.evidence && selectedAppeal.evidence.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">
                  申诉证据
                </h4>
                <div className="flex flex-wrap gap-2">
                  {selectedAppeal.evidence.map((evidence, index) => (
                    <a
                      key={index}
                      href={evidence}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-3 py-1.5 bg-gray-100 rounded-lg text-sm text-gray-700 hover:bg-gray-200"
                    >
                      <FileText className="w-4 h-4" />
                      证据 {index + 1}
                    </a>
                  ))}
                </div>
              </div>
            )}

            {selectedAppeal.reviewComment && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">
                  审核意见
                </h4>
                <p className="text-sm text-gray-900 bg-gray-50 p-4 rounded-lg">
                  {selectedAppeal.reviewComment}
                </p>
              </div>
            )}

            {(selectedAppeal.status === 'pending' || selectedAppeal.status === 'under_review') && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  处理意见
                </label>
                <textarea
                  value={reviewComment}
                  onChange={(e) => setReviewComment(e.target.value)}
                  placeholder="请输入处理意见..."
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500 focus:border-transparent"
                />
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  )
}

export default AppealManagement
