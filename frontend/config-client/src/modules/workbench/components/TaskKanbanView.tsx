import React, { useEffect, useState } from 'react'
import { useWorkbenchStore } from '@/stores/workbenchStore'
import { Card } from '@/components/Card'
import { Button } from '@/components/Button'
import { Badge } from '@/components/Badge'
import { Input } from '@/components/Input'
import { Modal } from '@/components/Modal'
import { cn } from '@/utils'
import { Plus, Kanban, Calendar, Clock, User } from 'lucide-react'
import type { Task, KanbanColumn, TaskStatus } from '@/types'

export const TaskKanbanView: React.FC = () => {
  const { tasks, loading, fetchTasks, updateTask } = useWorkbenchStore()
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    type: 'custom' as const,
    priority: 'medium' as const,
    assignee: '',
    dueDate: '',
  })

  useEffect(() => {
    fetchTasks()
  }, [])

  const columns: KanbanColumn[] = [
    { id: 'todo', title: '待办', status: 'todo', taskIds: [], order: 1 },
    { id: 'in_progress', title: '进行中', status: 'in_progress', taskIds: [], order: 2 },
    { id: 'review', title: '审核中', status: 'review', taskIds: [], order: 3 },
    { id: 'completed', title: '已完成', status: 'completed', taskIds: [], order: 4 },
  ]

  const getTasksByStatus = (status: TaskStatus) => {
    return tasks.filter((task) => task.status === status)
  }

  const handleDragStart = (e: React.DragEvent, taskId: string) => {
    e.dataTransfer.setData('taskId', taskId)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = async (e: React.DragEvent, newStatus: TaskStatus) => {
    e.preventDefault()
    const taskId = e.dataTransfer.getData('taskId')
    if (taskId && newStatus) {
      await updateTask(taskId, { status: newStatus })
      await fetchTasks()
    }
  }

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          status: 'todo',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        }),
      })
      if (response.ok) {
        await fetchTasks()
        setIsModalOpen(false)
        setFormData({
          title: '',
          description: '',
          type: 'custom',
          priority: 'medium',
          assignee: '',
          dueDate: '',
        })
      }
    } catch (error) {
      console.error('Failed to create task:', error)
    }
  }

  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      low: 'bg-gray-500',
      medium: 'bg-blue-500',
      high: 'bg-orange-500',
      urgent: 'bg-red-500',
    }
    return colors[priority] || 'bg-gray-500'
  }

  const isOverdue = (task: Task) => {
    return task.dueDate && new Date(task.dueDate) < new Date() && task.status !== 'completed'
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">任务看板</h1>
          <p className="mt-1 text-sm text-gray-600">
            拖拽任务卡片来更改状态
          </p>
        </div>
        <Button onClick={() => setIsModalOpen(true)} icon={<Plus className="w-4 h-4" />}>
          创建任务
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 overflow-x-auto pb-4">
        {columns.map((column) => {
          const columnTasks = getTasksByStatus(column.status)
          return (
            <div
              key={column.id}
              className="flex-shrink-0 w-full"
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, column.status)}
            >
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <Kanban className="w-5 h-5 text-gray-600" />
                    <h3 className="font-semibold text-gray-900">{column.title}</h3>
                    <Badge size="sm">{columnTasks.length}</Badge>
                  </div>
                </div>

                <div className="space-y-3 min-h-[200px]">
                  {loading ? (
                    <div className="text-center text-gray-500 py-8">加载中...</div>
                  ) : columnTasks.length === 0 ? (
                    <div className="text-center text-gray-400 py-8 text-sm">
                      暂无任务
                    </div>
                  ) : (
                    columnTasks.map((task) => (
                      <div
                        key={task.id}
                        draggable
                        onDragStart={(e) => handleDragStart(e, task.id)}
                        className={cn(
                          'bg-white p-4 rounded-lg border-2 shadow-sm cursor-move hover:shadow-md transition-shadow',
                          isOverdue(task) ? 'border-red-300' : 'border-gray-200'
                        )}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <h4 className="font-medium text-gray-900 text-sm flex-1">
                            {task.title}
                          </h4>
                          <div
                            className={cn(
                              'w-2 h-2 rounded-full flex-shrink-0 ml-2',
                              getPriorityColor(task.priority)
                            )}
                          />
                        </div>

                        {task.description && (
                          <p className="text-xs text-gray-600 mb-3 line-clamp-2">
                            {task.description}
                          </p>
                        )}

                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            {task.dueDate && (
                              <div
                                className={cn(
                                  'flex items-center gap-1 text-xs',
                                  isOverdue(task) ? 'text-red-600' : 'text-gray-500'
                                )}
                              >
                                <Calendar className="w-3 h-3" />
                                {new Date(task.dueDate).toLocaleDateString('zh-CN')}
                              </div>
                            )}
                          </div>
                          {task.assigneeName && (
                            <div className="flex items-center gap-1">
                              <User className="w-3 h-3 text-gray-500" />
                              <span className="text-xs text-gray-600">
                                {task.assigneeName}
                              </span>
                            </div>
                          )}
                        </div>

                        {task.tags && task.tags.length > 0 && (
                          <div className="flex flex-wrap gap-1 mt-2">
                            {task.tags.map((tag, index) => (
                              <Badge key={index} size="sm" variant="primary">
                                {tag}
                              </Badge>
                            ))}
                          </div>
                        )}
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="创建任务"
        footer={
          <div className="flex items-center justify-end gap-3">
            <Button variant="ghost" onClick={() => setIsModalOpen(false)}>
              取消
            </Button>
            <Button onClick={handleCreateTask}>创建</Button>
          </div>
        }
      >
        <form onSubmit={handleCreateTask} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              标题
            </label>
            <Input
              value={formData.title}
              onChange={(value) => setFormData({ ...formData, title: value })}
              placeholder="输入任务标题"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              描述
            </label>
            <textarea
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              placeholder="输入任务描述"
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500 focus:border-transparent"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                优先级
              </label>
              <select
                value={formData.priority}
                onChange={(e) =>
                  setFormData({ ...formData, priority: e.target.value as any })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500"
              >
                <option value="low">低</option>
                <option value="medium">中</option>
                <option value="high">高</option>
                <option value="urgent">紧急</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                截止日期
              </label>
              <Input
                type="date"
                value={formData.dueDate}
                onChange={(value) => setFormData({ ...formData, dueDate: value })}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              指派给
            </label>
            <Input
              value={formData.assignee}
              onChange={(value) => setFormData({ ...formData, assignee: value })}
              placeholder="输入用户ID或用户名"
              icon={<User className="w-4 h-4" />}
            />
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default TaskKanbanView
