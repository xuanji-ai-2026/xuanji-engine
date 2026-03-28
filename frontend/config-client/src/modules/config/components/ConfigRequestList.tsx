import React, { useEffect, useState } from 'react'

const ConfigRequestList: React.FC = () => {
  const [requests] = useState([])

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">配置请求列表</h1>
      <p className="text-gray-600">共 {requests.length} 个请求</p>
      <p className="text-gray-600 mt-4">功能开发中</p>
    </div>
  )
}

export default ConfigRequestList
