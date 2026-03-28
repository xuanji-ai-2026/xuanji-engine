import { Outlet } from 'react-router-dom';
import Sidebar from '@/components/layout/Sidebar';
import Header from '@/components/layout/Header';
import { useThemeStore } from '@/stores';
import { getEffectiveTheme } from '@/stores/themeStore';
import { useEffect } from 'react';

const MainLayout = () => {
  const { theme, sidebarCollapsed } = useThemeStore();

  useEffect(() => {
    const effectiveTheme = getEffectiveTheme(theme);
    if (effectiveTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div
        className={`flex flex-1 flex-col transition-all duration-300 ${
          sidebarCollapsed ? 'ml-20' : 'ml-64'
        }`}
      >
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
