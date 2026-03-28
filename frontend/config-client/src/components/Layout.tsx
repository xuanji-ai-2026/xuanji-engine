import React, { useState } from 'react'
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { Button } from './Button'
import { Badge } from './Badge'
import { cn } from '@/utils'
import {
  LayoutDashboard,
  ShieldCheck,
  Settings,
  LayoutList,
  MessageSquare,
  Users,
  Bell,
  LogOut,
  Menu,
  X,
  ChevronRight,
} from 'lucide-react'

interface NavItem {
  label: string
  path: string
  icon: React.ReactNode
  badge?: number
}

const navItems: NavItem[] = [
  { label: '工作台', path: '/', icon: <LayoutDashboard className="w-5 h-5" /> },
  { label: '认证协助', path: '/auth', icon: <ShieldCheck className="w-5 h-5" /> },
  { label: '配置协助', path: '/config', icon: <Settings className="w-5 h-5" /> },
  { label: '任务管理', path: '/workbench', icon: <LayoutList className="w-5 h-5" /> },
  { label: '智能助手', path: '/assistant', icon: <MessageSquare className="w-5 h-5" /> },
  { label: '用户管理', path: '/user', icon: <Users className="w-5 h-5" /> },
]

export const Layout: React.FC = () => {
  const { user, logout } = useAuthStore()
  const location = useLocation()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [notificationOpen, setNotificationOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const isActivePath = (path: string): boolean => {
    if (path === '/') {
      return location.pathname === '/'
    }
    return location.pathname.startsWith(path)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile Header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 z-30 bg-white border-b border-gray-200">
        <div className="flex items-center justify-between px-4 py-3">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            <Menu className="w-6 h-6" />
          </button>
          <h1 className="text-lg font-semibold text-xuanji-600">玄玑引擎配置端</h1>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleLogout}
            icon={<LogOut className="w-4 h-4" />}
          />
        </div>
      </header>

      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed top-0 left-0 bottom-0 z-40 w-64 bg-white border-r border-gray-200 transition-transform duration-300 lg:translate-x-0 lg:static lg:z-auto',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
            <h1 className="text-xl font-bold text-xuanji-600">玄玑引擎配置端</h1>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setSidebarOpen(false)}
                className={cn(
                  'flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                  isActivePath(item.path)
                    ? 'bg-xuanji-50 text-xuanji-700'
                    : 'text-gray-700 hover:bg-gray-100',
                )}
              >
                <div className="flex items-center gap-3">
                  {item.icon}
                  <span>{item.label}</span>
                </div>
                {item.badge && item.badge > 0 && (
                  <Badge variant="danger" size="sm">
                    {item.badge}
                  </Badge>
                )}
              </Link>
            ))}
          </nav>

          {/* User Info */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center gap-3">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-xuanji-100 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-xuanji-700">
                    {user?.realName?.[0] || user?.username?.[0] || 'U'}
                  </span>
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user?.realName || user?.username}
                </p>
                <p className="text-xs text-gray-500 truncate">{user?.email}</p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLogout}
                icon={<LogOut className="w-4 h-4" />}
              />
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="lg:ml-64 pt-16 lg:pt-0 min-h-screen">
        {/* Top Bar */}
        <header className="sticky top-0 lg:top-0 z-20 bg-white border-b border-gray-200">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <span>首页</span>
              <ChevronRight className="w-4 h-4" />
              <span className="font-medium text-gray-900">
                {navItems.find((item) => isActivePath(item.path))?.label || '未知'}
              </span>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setNotificationOpen(!notificationOpen)}
                className="relative p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
              >
                <Bell className="w-5 h-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
              </button>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
