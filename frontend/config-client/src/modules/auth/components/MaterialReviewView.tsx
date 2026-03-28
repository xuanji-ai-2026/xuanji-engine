import React, { useEffect, useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Modal } from '@/components/Modal'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { CheckCircle, XCircle, FileText, Download, ZoomIn } from 'lucide-react'
import type { MaterialReview, AuthRequest } from '@/types'

export const MaterialReviewView: React.FC = () => {
  const [requests, setRequests] = useState<AuthRequest[]>([])
  const [reviews, setReviews] = useState<Record<string, MaterialReview[]>>({})
  const [loading, setLoading] = useState(false)
  const [selectedRequest, setSelectedRequest] = useState<AuthRequest | null>(null)
  const [isReviewModalOpen, setIsReviewModalOpen] = useState(false)
  const [previewMaterial, setPreviewMaterial] = useState<string | null>(null)

  useEffect(() => {
    fetchPendingRequests()
  }, [])

  const fetchPendingRequests = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/auth-requests/pending-review')
      const data: AuthRequest[] = await response.json()
      setRequests(data)
    } catch (error) {
      console.error('Failed to fetch pending requests:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchRequestReviews = async (requestId: string) => {
    try {
      const response = await fetch(`/api/auth-requests/${requestId}/materials`)
      const data: MaterialReview[] = await response.json()
      setReviews((prev) => ({ ...prev, [requestId]: data }))
    } catch (error) {
      console.error('Failed to fetch materials:', error)
    }
  }

  const handleOpenReview = async (request: AuthRequest) => {
    setSelectedRequest(request)
    await fetchRequestReviews(request.id)
    setIsReviewModalOpen(true)
  }

  const handleReviewMaterial = async (
    materialId: string,
    status: 'approved' | 'rejected',
    comment?: string
  ) => {
    if (!selectedRequest) return
    try {
      const response = await fetch(
        `/api/auth-requests/${selectedRequest.id}/materials/${materialId}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status, comment }),
        }
      )
      if (response.ok) {
        await fetchRequestReviews(selectedRequest.id)
      }
    } catch (error) {
      console.error('Failed to review material:', error)
    }
  }

  const handlePreview = (materialUrl: string) => {
    setPreviewMaterial(materialUrl)
  }

  const isAllApproved = (materials: MaterialReview[]) => {
    return materials.length > 0 && materials.every((m) => m.reviewStatus === 'approved')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">认证资料审核</h1>
        <p className="mt-1 text-sm text-gray-600">
          审核认证申请提交的资料文件
        </p>
      </div>

      {/* Requests List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {loading ? (
          <div className="col-span-2 py-12 text-center text-gray-500">
            加载中...
          </div>
        ) : requests.length === 0 ? (
          <div className="col-span-2 py-12 text-center text-gray-500">
            暂无待审核的资料
          </div>
        ) : (
          requests.map((request) => (
            <Card key={request.id} className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {request.requesterName}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    {request.requestType} - {request.reason}
                  </p>
                </div>
                <Badge variant={request.priority === 'urgent' ? 'danger' : 'warning'}>
                  {request.priority}
                </Badge>
              </div>
              <div className="flex items-center gap-2 mb-4">
                <FileText className="w-4 h-4 text-gray-500" />
                <span className="text-sm text-gray-600">
                  {request.attachments?.length || 0} 份资料待审核
                </span>
              </div>
              <Button
                size="sm"
                fullWidth
                onClick={() => handleOpenReview(request)}
              >
                开始审核
              </Button>
            </Card>
          ))
        )}
      </div>

      {/* Review Modal */}
      <Modal
        isOpen={isReviewModalOpen}
        onClose={() => setIsReviewModalOpen(false)}
        title="资料审核"
        size="lg"
        footer={
          <div className="flex items-center justify-between">
            <Button variant="ghost" onClick={() => setIsReviewModalOpen(false)}>
              关闭
            </Button>
            {selectedRequest && isAllApproved(reviews[selectedRequest.id] || []) && (
              <Button
                variant="primary"
                onClick={async () => {
                  try {
                    const response = await fetch(
                      `/api/auth-requests/${selectedRequest.id}/materials-complete`,
                      { method: 'POST' }
                    )
                    if (response.ok) {
                      setIsReviewModalOpen(false)
                      fetchPendingRequests()
                    }
                  } catch (error) {
                    console.error('Failed to complete review:', error)
                  }
                }}
              >
                完成审核
              </Button>
            )}
          </div>
        }
      >
        {selectedRequest && (
          <div className="space-y-6">
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">
                申请人信息
              </h4>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">姓名</span>
                  <span className="text-sm font-medium text-gray-900">
                    {selectedRequest.requesterName}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">请求类型</span>
                  <span className="text-sm text-gray-900">
                    {selectedRequest.requestType}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">创建时间</span>
                  <span className="text-sm text-gray-600">
                    {new Date(selectedRequest.createdAt).toLocaleString('zh-CN')}
                  </span>
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-3">
                资料文件
              </h4>
              <div className="space-y-3">
                {(reviews[selectedRequest.id] || []).map((material) => (
                  <div
                    key={material.id}
                    className="border border-gray-200 rounded-lg p-4"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <FileText className="w-5 h-5 text-gray-500" />
                          <span className="text-sm font-medium text-gray-900">
                            {material.materialType}
                          </span>
                          <Badge
                            variant={
                              material.reviewStatus === 'approved'
                                ? 'success'
                                : material.reviewStatus === 'rejected'
                                  ? 'danger'
                                  : 'warning'
                            }
                            size="sm"
                          >
                            {material.reviewStatus}
                          </Badge>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handlePreview(material.materialUrl)}
                          icon={<ZoomIn className="w-4 h-4" />}
                        />
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => window.open(material.materialUrl, '_blank')}
                          icon={<Download className="w-4 h-4" />}
                        />
                      </div>
                    </div>

                    {material.reviewStatus === 'pending' && (
                      <div className="flex items-center gap-2 mt-3 pt-3 border-t border-gray-100">
                        <Button
                          variant="primary"
                          size="sm"
                          onClick={() => handleReviewMaterial(material.id, 'approved')}
                          icon={<CheckCircle className="w-4 h-4" />}
                        >
                          通过
                        </Button>
                        <Button
                          variant="danger"
                          size="sm"
                          onClick={() => {
                            const comment = prompt('请输入驳回原因：')
                            if (comment) {
                              handleReviewMaterial(material.id, 'rejected', comment)
                            }
                          }}
                          icon={<XCircle className="w-4 h-4" />}
                        >
                          驳回
                        </Button>
                      </div>
                    )}

                    {material.reviewComment && (
                      <div className="mt-3 pt-3 border-t border-gray-100">
                        <p className="text-sm text-gray-600">
                          <span className="font-medium">审核意见：</span>
                          {material.reviewComment}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </Modal>

      {/* Preview Modal */}
      <Modal
        isOpen={previewMaterial !== null}
        onClose={() => setPreviewMaterial(null)}
        title="资料预览"
        size="xl"
        footer={
          <Button variant="ghost" onClick={() => setPreviewMaterial(null)}>
            关闭
          </Button>
        }
      >
        {previewMaterial && (
          <div className="flex justify-center">
            <img
              src={previewMaterial}
              alt="资料预览"
              className="max-w-full max-h-[60vh] object-contain"
            />
          </div>
        )}
      </Modal>
    </div>
  )
}

export default MaterialReviewView
