import React, { useState } from 'react'
import { useParams } from 'react-router-dom'

const ConfigRequestEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const [requestType, setRequestType] = useState('digital_human')
  const [description, setDescription] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('编辑配置请求:', { id, requestType, description })
    // TODO: 实现配置请求编辑逻辑
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">编辑配置请求</h1>
      <p className="text-gray-600 mb-4">请求ID: {id}</p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">请求类型</label>
          <select
            value={requestType}
            onChange={(e) => setRequestType(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
          >
            <option value="digital_human">数字人配置</option>
            <option value="knowledge_base">知识库配置</option>
            <option value="plugin">插件配置</option>
            <option value="other">其他</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">详细描述</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            placeholder="请详细描述配置需求"
            rows={6}
          />
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 mr-2"
        >
          保存更改
        </button>
        <button
          type="button"
          className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
        >
          取消
        </button>
      </form>
    </div>
  )
}

export default ConfigRequestEdit
