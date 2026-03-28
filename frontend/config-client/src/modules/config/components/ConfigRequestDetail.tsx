import React from 'react'
import { useParams } from 'react-router-dom'

const ConfigRequestDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">配置请求详情</h1>
      <p className="text-gray-600">请求ID: {id}</p>
      <p className="text-gray-600 mt-4">功能开发中</p>
    </div>
  )
}

export default ConfigRequestDetail
