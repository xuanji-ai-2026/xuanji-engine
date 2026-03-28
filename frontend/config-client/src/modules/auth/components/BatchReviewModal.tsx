import React from 'react'

interface BatchReviewModalProps {
  isOpen: boolean
  onClose: () => void
  onRequestIds: string[]
}

const BatchReviewModal: React.FC<BatchReviewModalProps> = ({
  isOpen,
  onClose,
  onRequestIds
}) => {
  if (!isOpen) return null

  const handleReview = (action: 'approve' | 'reject') => {
    console.log(`批量${action === 'approve' ? '通过' : '拒绝'}`, onRequestIds)
    // TODO: 实现批量审核逻辑
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">批量审核</h2>
        <p className="text-gray-600 mb-4">
          已选择 {onRequestIds.length} 个请求
        </p>
        <div className="flex justify-end gap-3">
          <button
            onClick={() => handleReview('reject')}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            批量拒绝
          </button>
          <button
            onClick={() => handleReview('approve')}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            批量通过
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  )
}

export default BatchReviewModal
