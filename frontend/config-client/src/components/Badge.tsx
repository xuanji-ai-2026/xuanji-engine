import React from 'react'
import { cn } from '@/utils'

type BadgeVariant = 'success' | 'warning' | 'danger' | 'info' | 'gray'

interface BadgeProps {
  variant?: BadgeVariant
  size?: 'sm' | 'md'
  className?: string
  children: React.ReactNode
}

export const Badge: React.FC<BadgeProps> = ({
  variant = 'gray',
  size = 'md',
  className,
  children,
}) => {
  const variants: Record<BadgeVariant, string> = {
    success: 'bg-green-100 text-green-800 border-green-200',
    warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    danger: 'bg-red-100 text-red-800 border-red-200',
    info: 'bg-blue-100 text-blue-800 border-blue-200',
    gray: 'bg-gray-100 text-gray-800 border-gray-200',
  }

  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-0.5 text-sm',
  }

  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full border font-medium',
        variants[variant],
        sizes[size],
        className,
      )}
    >
      {children}
    </span>
  )
}

interface StatusBadgeProps {
  status: 'pending' | 'approved' | 'rejected' | 'processing' | 'active' | 'inactive' | 'locked' | 'todo' | 'in_progress' | 'review' | 'completed' | 'cancelled'
  className?: string
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, className }) => {
  const statusConfig: Record<
    string,
    { variant: BadgeVariant; label: string }
  > = {
    pending: { variant: 'warning', label: '待处理' },
    approved: { variant: 'success', label: '已批准' },
    rejected: { variant: 'danger', label: '已拒绝' },
    processing: { variant: 'info', label: '处理中' },
    active: { variant: 'success', label: '活跃' },
    inactive: { variant: 'gray', label: '未激活' },
    locked: { variant: 'danger', label: '已锁定' },
    todo: { variant: 'gray', label: '待办' },
    in_progress: { variant: 'info', label: '进行中' },
    review: { variant: 'warning', label: '审核中' },
    completed: { variant: 'success', label: '已完成' },
    cancelled: { variant: 'danger', label: '已取消' },
  }

  const config = statusConfig[status] || { variant: 'gray', label: status }

  return (
    <Badge variant={config.variant} className={className}>
      {config.label}
    </Badge>
  )
}

interface PriorityBadgeProps {
  priority: 'low' | 'medium' | 'high' | 'urgent'
  className?: string
}

export const PriorityBadge: React.FC<PriorityBadgeProps> = ({ priority, className }) => {
  const priorityConfig: Record<
    string,
    { variant: BadgeVariant; label: string }
  > = {
    low: { variant: 'gray', label: '低' },
    medium: { variant: 'info', label: '中' },
    high: { variant: 'warning', label: '高' },
    urgent: { variant: 'danger', label: '紧急' },
  }

  const config = priorityConfig[priority] || { variant: 'gray', label: priority }

  return (
    <Badge variant={config.variant} className={className}>
      {config.label}
    </Badge>
  )
}
