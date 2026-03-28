import { Outlet } from 'react-router-dom'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'
import { useUIStore } from '@/stores/ui-store'

export default function MainLayout() {
  const { config } = useUIStore()

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <Sidebar
        collapsed={config.sidebar.collapsed}
        width={config.sidebar.width}
        position={config.sidebar.position}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {config.header.visible && <Header />}

        <main className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900 scrollbar-thin">
          <div className="container mx-auto px-4 py-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
