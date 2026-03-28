import React from 'react'
import { useParams } from 'react-router-dom'

const AuthRequestReview: React.FC = () => {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">审核认证请求</h1>
      <p className="text-gray-600">请求ID: {id}</p>
      <p className="text-gray-600 mt-4">功能开发中</p>
    </div>
  )
}

export default AuthRequestReview
