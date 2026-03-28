import React, { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Key,
  Puzzle,
  Package,
  MessageSquare,
  Settings,
  Bell,
  Menu,
  X,
  User,
} from 'lucide-react';
import { Button } from './Button';
import { useAppStore } from '../stores/appStore';
import { cn } from '../utils';

const navItems = [
  { path: '/api', icon: Key, label: 'API管理' },
  { path: '/plugin', icon: Puzzle, label: '插件开发' },
  { path: '/sdk', icon: Package, label: 'SDK管理' },
  { path: '/assistant', icon: MessageSquare, label: '智能助手' },
  { path: '/settings', icon: Settings, label: '设置' },
];

export const Layout: React.FC = () => {
  const location = useLocation();
  const { sidebarOpen, toggleSidebar } = useAppStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-14 items-center px-4">
          <button
            onClick={toggleSidebar}
            className="mr-4 rounded-lg p-2 hover:bg-muted lg:hidden"
          >
            <Menu className="h-5 w-5" />
          </button>

          <Link to="/" className="flex items-center space-x-2">
            <LayoutDashboard className="h-6 w-6 text-primary" />
            <span className="text-lg font-bold">玄玑引擎</span>
          </Link>

          <div className="ml-auto flex items-center space-x-2">
            <Button variant="ghost" size="sm" icon={<Bell className="h-4 w-4" />} />
            <Button variant="ghost" size="sm" icon={<User className="h-4 w-4" />} />
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside
          className={cn(
            'fixed left-0 top-14 z-30 h-[calc(100vh-3.5rem)] w-64 border-r bg-background transition-transform',
            sidebarOpen ? 'translate-x-0' : '-translate-x-full',
            'lg:translate-x-0',
            !sidebarOpen && 'lg:w-0 lg:overflow-hidden'
          )}
        >
          <nav className="space-y-1 p-4">
            {navItems.map((item) => {
              const isActive = location.pathname.startsWith(item.path);
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={cn(
                    'flex items-center space-x-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                  )}
                >
                  <item.icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </aside>

        {/* Main Content */}
        <main className={cn('flex-1', sidebarOpen ? 'lg:ml-64' : 'lg:ml-0')}>
          <div className="container mx-auto p-4 lg:p-8">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};
