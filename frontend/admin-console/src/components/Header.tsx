import { useState } from 'react'
import { Bell, Search, User, LogOut, Settings, Sun, Moon } from 'lucide-react'
import { useAuthStore } from '@/stores/auth-store'
import { useThemeStore } from '@/stores/theme-store'
import { useAssistantStore } from '@/stores/assistant-store'
import { cn } from '@/utils'

export default function Header() {
  const { user, logout } = useAuthStore()
  const { theme, toggleTheme } = useThemeStore()
  const { alerts, toggleActive } = useAssistantStore()
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)

  return (
    <header className="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6">
      {/* Search */}
      <div className="flex-1 max-w-md">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="搜索..."
            className="w-full pl-10 pr-4 py-2 bg-gray-100 dark:bg-gray-700 border-0 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Right Actions */}
      <div className="flex items-center space-x-4">
        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          title={theme === 'light' ? '切换到深色模式' : '切换到浅色模式'}
        >
          {theme === 'light' ? (
            <Moon className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          ) : (
            <Sun className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          )}
        </button>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors relative"
          >
            <Bell className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            {alerts.length > 0 && (
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
            )}
          </button>

          {/* Notification Dropdown */}
          {showNotifications && (
            <NotificationDropdown onClose={() => setShowNotifications(false)} />
          )}
        </div>

        {/* User Menu */}
        <div className="relative">
          <button
            onClick={() => setShowUserMenu(!showUserMenu)}
            className="flex items-center space-x-3 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-white" />
            </div>
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              {user?.name}
            </span>
          </button>

          {/* User Dropdown */}
          {showUserMenu && (
            <UserDropdown
              user={user}
              onClose={() => setShowUserMenu(false)}
              onLogout={logout}
            />
          )}
        </div>
      </div>
    </header>
  )
}

function NotificationDropdown({ onClose }: { onClose: () => void }) {
  const { alerts, acknowledgeAlert, clearAlerts } = useAssistantStore()

  return (
    <div className="absolute right-0 top-full mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden z-50">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
          通知
        </h3>
        <button
          onClick={clearAlerts}
          className="text-xs text-blue-600 hover:text-blue-800"
        >
          清空
        </button>
      </div>

      <div className="max-h-96 overflow-y-auto scrollbar-thin">
        {alerts.length === 0 ? (
          <div className="p-8 text-center text-gray-500 dark:text-gray-400 text-sm">
            暂无通知
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className={cn(
                'p-4 border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer',
                alert.acknowledged && 'opacity-50'
              )}
              onClick={() => {
                acknowledgeAlert(alert.id)
              }}
            >
              <div className="flex items-start space-x-3">
                <div
                  className={cn(
                    'w-2 h-2 rounded-full mt-2',
                    alert.severity === 'critical' && 'bg-red-500',
                    alert.severity === 'high' && 'bg-orange-500',
                    alert.severity === 'medium' && 'bg-yellow-500',
                    alert.severity === 'low' && 'bg-blue-500'
                  )}
                />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {alert.title}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {alert.message}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

function UserDropdown({
  user,
  onClose,
  onLogout,
}: {
  user: any
  onClose: () => void
  onLogout: () => void
}) {
  const menuItems = [
    { icon: User, label: '个人资料', href: '/profile' },
    { icon: Settings, label: '设置', href: '/settings' },
  ]

  return (
    <div className="absolute right-0 top-full mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden z-50">
      <div className="p-3 border-b border-gray-200 dark:border-gray-700">
        <p className="text-sm font-medium text-gray-900 dark:text-white">
          {user?.name}
        </p>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
          {user?.email}
        </p>
      </div>

      <div className="py-1">
        {menuItems.map((item, index) => (
          <a
            key={index}
            href={item.href}
            className="flex items-center space-x-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <item.icon className="w-4 h-4" />
            <span>{item.label}</span>
          </a>
        ))}
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 py-1">
        <button
          onClick={() => {
            onLogout()
            onClose()
          }}
          className="flex items-center space-x-3 w-full px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700"
        >
          <LogOut className="w-4 h-4" />
          <span>退出登录</span>
        </button>
      </div>
    </div>
  )
}
