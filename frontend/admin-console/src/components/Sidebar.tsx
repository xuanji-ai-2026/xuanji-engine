import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  Users,
  Bot,
  Database,
  Puzzle,
  Activity,
  Settings as SettingsIcon,
  Bell,
  Zap,
  ChevronRight,
  ChevronLeft,
  X,
} from 'lucide-react'
import { useUIStore } from '@/stores/ui-store'
import { useBreakpoint } from '@/hooks'
import { cn } from '@/utils'

interface NavItem {
  title: string
  href: string
  icon: any
  badge?: number
}

const navItems: NavItem[] = [
  { title: '仪表板', href: '/dashboard', icon: LayoutDashboard },
  { title: '系统初始化', href: '/system-init', icon: Zap },
  { title: '用户管理', href: '/users', icon: Users },
  { title: '数字人', href: '/digital-humans', icon: Bot },
  { title: '知识源', href: '/knowledge', icon: Database },
  { title: '插件', href: '/plugins', icon: Puzzle },
  { title: '运营管理', href: '/operations', icon: Activity },
  { title: 'UI配置', href: '/settings', icon: SettingsIcon },
  { title: '更新中心', href: '/updates', icon: Bell },
]

interface SidebarProps {
  collapsed: boolean
  width: number
  position: 'left' | 'right'
}

export default function Sidebar({ collapsed, width, position }: SidebarProps) {
  const { isMobile } = useBreakpoint()
  const { toggleSidebar } = useUIStore()
  const location = useLocation()
  const [mobileOpen, setMobileOpen] = useState(false)

  if (position === 'right') {
    return null
  }

  return (
    <>
      {/* Mobile Backdrop */}
      {mobileOpen && isMobile && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed lg:static inset-y-0 z-50 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 transition-all duration-300',
          isMobile
            ? mobileOpen
              ? 'translate-x-0'
              : '-translate-x-full'
            : 'translate-x-0',
          collapsed ? 'w-16' : `w-${width}`
        )}
        style={{
          width: isMobile ? '256px' : collapsed ? '64px' : `${width}px`,
        }}
      >
        {/* Logo */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200 dark:border-gray-700">
          {!collapsed && (
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <span className="text-lg font-bold text-gray-900 dark:text-white">
                玄玑引擎
              </span>
            </div>
          )}
          {collapsed && (
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mx-auto">
              <Bot className="w-5 h-5 text-white" />
            </div>
          )}
          {isMobile && (
            <button
              onClick={() => setMobileOpen(false)}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
            >
              <X className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </button>
          )}
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-1 overflow-y-auto scrollbar-thin">
          {navItems.map((item) => (
            <NavItem
              key={item.href}
              item={item}
              collapsed={collapsed}
              isActive={location.pathname === item.href}
            />
          ))}
        </nav>

        {/* Toggle Button */}
        {!isMobile && (
          <div className="absolute bottom-4 left-0 right-0 flex justify-center">
            <button
              onClick={toggleSidebar}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
            >
              {collapsed ? (
                <ChevronRight className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              ) : (
                <ChevronLeft className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              )}
            </button>
          </div>
        )}
      </aside>

      {/* Mobile Toggle */}
      {isMobile && (
        <button
          onClick={() => setMobileOpen(true)}
          className="lg:hidden fixed bottom-4 right-4 p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg z-50"
        >
          <Menu className="w-6 h-6" />
        </button>
      )}
    </>
  )
}

function NavItem({
  item,
  collapsed,
  isActive,
}: {
  item: NavItem
  collapsed: boolean
  isActive: boolean
}) {
  const { isMobile } = useBreakpoint()

  return (
    <Link
      to={item.href}
      className={cn(
        'flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors',
        isActive
          ? 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400'
          : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
      )}
      onClick={() => isMobile && setMobileOpen(false)}
    >
      <item.icon className="w-5 h-5 flex-shrink-0" />
      {!collapsed && (
        <>
          <span className="font-medium">{item.title}</span>
          {item.badge && (
            <span className="ml-auto bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
              {item.badge}
            </span>
          )}
        </>
      )}
    </Link>
  )
}

function Menu({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M4 6h16M4 12h16M4 18h16"
      />
    </svg>
  )
}
