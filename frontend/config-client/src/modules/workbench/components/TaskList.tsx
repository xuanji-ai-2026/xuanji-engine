import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useWorkbenchStore } from '@/stores/workbenchStore'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/Card'
import { StatusBadge } from '@/components/Badge'
import { PriorityBadge } from '@/components/Badge'
import { Select } from '@/components/Input'
import { cn, formatRelativeTime } from '@/utils'
import { Search, Plus, LayoutList, RefreshCw, CheckCircle } from 'lucide-react'

export const TaskList: React.FC = () => {
  const navigate = useNavigate()
  const {
    tasks,
    loading,
    total,
    filters,
    pagination,
    fetchTasks,
    setFilters,
    setPagination,
  } = useWorkbenchStore()

  const [searchKeyword, setSearchKeyword] = useState('')

  useEffect(() => {
    fetchTasks()
  }, [fetchTasks])

  const handleCreate = () => {
    navigate('/workbench/create')
  }

  const handleRefresh = () => {
    fetchTasks()
  }

  const statusLabels: Record<string, string> = {
    todo: '待办',
    in_progress: '进行中',
    review: '审核中',
    completed: '已完成',
    cancelled: '已取消',
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-1">任务管理</h1>
          <p className="text-gray-600">管理所有工作任务</p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="secondary"
            icon={<RefreshCw className="w-4 h-4" />}
            onClick={handleRefresh}
            loading={loading}
          >
            刷新
          </Button>
          <Button
            variant="primary"
            icon={<Plus className="w-4 h-4" />}
            onClick={handleCreate}
          >
            新建任务
          </Button>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardContent padding="sm">
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex-1 min-w-[200px]">
              <Input
                placeholder="搜索任务标题、描述..."
                leftIcon={<Search className="w-4 h-4" />}
                value={searchKeyword}
                onChange={(e) => setSearchKeyword(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && setFilters({ ...filters, keyword: searchKeyword })}
              />
            </div>
            <Select
              options={[
                { label: '全部状态', value: '' },
                { label: '待办', value: 'todo' },
                { label: '进行中', value: 'in_progress' },
                { label: '审核中', value: 'review' },
                { label: '已完成', value: 'completed' },
                { label: '已取消', value: 'cancelled' },
              ]}
              defaultValue=""
              onChange={(e) => {
                const status = e.target.value ? [e.target.value] : undefined
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
                const priority = e.target.value ? [e.target.value] : undefined
                setFilters({ ...filters, priority })
              }}
            />
          </div>
        </CardContent>
      </Card>

      {/* Task List */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>任务列表 ({total})</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-12">
              <RefreshCw className="w-8 h-8 text-xuanji-600 animate-spin mx-auto mb-4" />
              <p className="text-gray-600">加载中...</p>
            </div>
          ) : tasks.length === 0 ? (
            <div className="text-center py-12">
              <LayoutList className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">暂无任务</p>
            </div>
          ) : (
            <div className="space-y-3">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className={cn(
                    'flex items-start gap-4 p-4 border border-gray-200 rounded-lg hover:border-xuanji-300 hover:bg-xuanji-50 transition-all cursor-pointer',
                    task.priority === 'urgent' && 'border-l-4 border-l-red-500',
                    task.status === 'completed' && 'opacity-60',
                  )}
                  onClick={() => navigate(`/workbench/${task.id}`)}
                >
                  <div className="flex-shrink-0">
                    <div className={cn(
                      'w-10 h-10 rounded-full flex items-center justify-center',
                      task.status === 'completed' ? 'bg-green-100' : 'bg-xuanji-100'
                    )}>
                      {task.status === 'completed' ? (
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      ) : (
                        <LayoutList className="w-5 h-5 text-xuanji-600" />
                      )}
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <h3 className="text-sm font-medium text-gray-900">
                        {task.title}
                      </h3>
                      <StatusBadge status={task.status} />
                      <PriorityBadge priority={task.priority} />
                    </div>
                    <p className="text-sm text-gray-600 mb-2 line-clamp-2">
                      {task.description}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <span>创建人: {task.createdBy}</span>
                      {task.assigneeName && <span>负责人: {task.assigneeName}</span>}
                      {task.dueDate && <span>截止: {formatRelativeTime(task.dueDate)}</span>}
                      <span>创建时间: {formatRelativeTime(task.createdAt)}</span>
                    </div>
                    {task.tags && task.tags.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {task.tags.map((tag, index) => (
                          <span
                            key={index}
                            className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
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
                    fetchTasks()
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
                    fetchTasks()
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

export const TaskDetail: React.FC = () => {
  const navigate = useNavigate()
  const { id } = useParams<{ id: string }>()

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          icon={<ArrowLeft className="w-4 h-4" />}
          onClick={() => navigate('/workbench')}
        >
          返回
        </Button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-1">任务详情</h1>
        </div>
      </div>

      <Card>
        <CardContent>
          <p className="text-gray-600">任务详情待实现... (ID: {id})</p>
        </CardContent>
      </Card>
    </div>
  )
}

export const TaskCreate: React.FC = () => {
  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    navigate('/workbench')
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          icon={<ArrowLeft className="w-4 h-4" />}
          onClick={() => navigate('/workbench')}
        >
          返回
        </Button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-1">新建任务</h1>
        </div>
      </div>

      <Card>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <p className="text-gray-600">表单内容待实现...</p>
            <div className="flex gap-3">
              <Button type="submit" variant="primary">
                提交
              </Button>
              <Button type="button" variant="secondary" onClick={() => navigate('/workbench')}>
                取消
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default TaskList
