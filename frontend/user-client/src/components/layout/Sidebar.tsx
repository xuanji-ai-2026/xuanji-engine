import { NavLink } from 'react-router-dom';
import {
  Home,
  Users,
  Shield,
  Cpu,
  Bot,
  MessageSquare,
  Puzzle,
  CreditCard,
  Sparkles,
  Settings,
  Menu,
} from 'lucide-react';
import { useThemeStore } from '@/stores';
import { cn } from '@/utils';
import Button from '@/components/common/Button';

const navigation = [
  { name: '仪表盘', href: '/dashboard', icon: Home },
  { name: '工作人员', href: '/staff', icon: Users },
  { name: '权限管理', href: '/permissions', icon: Shield },
  { name: '智能配置', href: '/smart-config', icon: Cpu },
  { name: '自动生成', href: '/auto-generate', icon: Bot },
  { name: '对话', href: '/chat', icon: MessageSquare },
  { name: '插件市场', href: '/plugin-market', icon: Puzzle },
  { name: '计费中心', href: '/account', icon: CreditCard },
  { name: '小紫助手', href: '/assistant', icon: Sparkles },
];

const Sidebar = () => {
  const { sidebarCollapsed, setSidebarCollapsed } = useThemeStore();

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 z-40 h-screen bg-white border-r border-gray-200 transition-all duration-300',
        sidebarCollapsed ? 'w-20' : 'w-64'
      )}
    >
      {/* Logo */}
      <div className="flex h-16 items-center justify-center border-b border-gray-200">
        {sidebarCollapsed ? (
          <div className="text-2xl font-bold text-primary-600">玄</div>
        ) : (
          <div className="text-xl font-bold text-gray-900">玄玑引擎</div>
        )}
      </div>

      {/* Toggle Button */}
      <div className="flex justify-center p-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={setSidebarCollapsed}
          className="w-full"
        >
          <Menu className="h-4 w-4" />
        </Button>
      </div>

      {/* Navigation */}
      <nav className="space-y-1 p-2">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              cn(
                'flex items-center rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-gray-700 hover:bg-gray-50',
                sidebarCollapsed ? 'justify-center' : 'justify-start'
              )
            }
          >
            <item.icon className={cn('h-5 w-5', !sidebarCollapsed && 'mr-3')} />
            {!sidebarCollapsed && <span>{item.name}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Bottom Navigation */}
      <nav className="absolute bottom-0 left-0 right-0 border-t border-gray-200 p-2">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            cn(
              'flex items-center rounded-lg px-3 py-2 text-sm font-medium transition-colors',
              isActive
                ? 'bg-primary-50 text-primary-700'
                : 'text-gray-700 hover:bg-gray-50',
              sidebarCollapsed ? 'justify-center' : 'justify-start'
            )
          }
        >
          <Settings className={cn('h-5 w-5', !sidebarCollapsed && 'mr-3')} />
          {!sidebarCollapsed && <span>设置</span>}
        </NavLink>
      </nav>
    </aside>
  );
};

export default Sidebar;
