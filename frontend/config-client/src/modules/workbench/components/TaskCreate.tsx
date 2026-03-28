import React, { useState } from 'react'

const TaskCreate: React.FC = () => {
  const [taskName, setTaskName] = useState('')
  const [description, setDescription] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('创建任务:', { taskName, description })
    // TODO: 实现任务创建逻辑
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">创建任务</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">任务名称</label>
          <input
            type="text"
            value={taskName}
            onChange={(e) => setTaskName(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            placeholder="请输入任务名称"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">任务描述</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            placeholder="请输入任务描述"
            rows={4}
          />
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          创建任务
        </button>
      </form>
    </div>
  )
}

export default TaskCreate
