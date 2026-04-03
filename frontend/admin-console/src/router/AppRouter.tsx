import { RouterProvider, Route, createBrowserRouter, Navigate, createRoutesFromElements } from 'react-router-dom'
import MainLayout from '@/layouts/MainLayout'
import Dashboard from '@/pages/Dashboard'

// 系统初始化
import SystemInit from '@/pages/SystemInit'
import CreatorBinding from '@/pages/SystemInit/CreatorBinding'
import StealthActivation from '@/pages/SystemInit/StealthActivation'

// 用户管理
import UserList from '@/pages/Users/UserList'
import UserDetail from '@/pages/Users/UserDetail'
import UserAuth from '@/pages/Users/UserAuth'
import UserStatus from '@/pages/Users/UserStatus'
import UserSearch from '@/pages/Users/UserSearch'

// 数字人管理
import DigitalHumanList from '@/pages/DigitalHumans/List'
import DigitalHumanDetail from '@/pages/DigitalHumans/Detail'
import DigitalHumanConfig from '@/pages/DigitalHumans/Config'
import DigitalHumanStats from '@/pages/DigitalHumans/Stats'

// 知识源管理
import KnowledgeList from '@/pages/Knowledge/List'
import KnowledgeConfig from '@/pages/Knowledge/Config'
import KnowledgeStats from '@/pages/Knowledge/Stats'

// 插件管理
import PluginList from '@/pages/Plugins/List'
import PluginReview from '@/pages/Plugins/Review'
import PluginStats from '@/pages/Plugins/Stats'
import PluginManage from '@/pages/Plugins/Manage'

// 运营管理
import Overview from '@/pages/Operations/Overview'
import Maintenance from '@/pages/Operations/Maintenance'
import Security from '@/pages/Operations/Security'
import Analytics from '@/pages/Operations/Analytics'
import CRM from '@/pages/Operations/CRM'
import Marketing from '@/pages/Operations/Marketing'
import Finance from '@/pages/Operations/Finance'

// UI配置
import UISettings from '@/pages/Settings/UISettings'
import LogoSettings from '@/pages/Settings/LogoSettings'
import ThemeSettings from '@/pages/Settings/ThemeSettings'
import LayoutSettings from '@/pages/Settings/LayoutSettings'
import AnimationSettings from '@/pages/Settings/AnimationSettings'

// 更新管理
import UpdateCenter from '@/pages/Updates/UpdateCenter'
import VersionHistory from '@/pages/Updates/VersionHistory'
import Announcements from '@/pages/Updates/Announcements'
import PluginRecommendations from '@/pages/Updates/PluginRecommendations'

// 智能助手小灵
import Assistant from '@/pages/Assistant/Assistant'
import SystemMonitor from '@/pages/Assistant/SystemMonitor'
import Alerts from '@/pages/Assistant/Alerts'
import DecisionSupport from '@/pages/Assistant/DecisionSupport'

// 登录页面
import Login from '@/pages/Login'

// ✅ 修复：使用createRoutesFromElements正确创建路由
const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      {/* 登录页面 */}
      <Route path="/login" element={<Login />} />

      {/* 主布局 */}
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />

        {/* 仪表板 */}
        <Route path="dashboard" element={<Dashboard />} />

        {/* 系统初始化 */}
        <Route path="system-init">
          <Route index element={<SystemInit />} />
          <Route path="creator" element={<CreatorBinding />} />
          <Route path="stealth" element={<StealthActivation />} />
        </Route>

        {/* 用户管理 */}
        <Route path="users">
          <Route index element={<UserList />} />
          <Route path=":id" element={<UserDetail />} />
          <Route path="auth" element={<UserAuth />} />
          <Route path="status" element={<UserStatus />} />
          <Route path="search" element={<UserSearch />} />
        </Route>

        {/* 数字人管理 */}
        <Route path="digital-humans">
          <Route index element={<DigitalHumanList />} />
          <Route path=":id" element={<DigitalHumanDetail />} />
          <Route path="config" element={<DigitalHumanConfig />} />
          <Route path="stats" element={<DigitalHumanStats />} />
        </Route>

        {/* 知识源管理 */}
        <Route path="knowledge">
          <Route index element={<KnowledgeList />} />
          <Route path="config" element={<KnowledgeConfig />} />
          <Route path="stats" element={<KnowledgeStats />} />
        </Route>

        {/* 插件管理 */}
        <Route path="plugins">
          <Route index element={<PluginList />} />
          <Route path="review" element={<PluginReview />} />
          <Route path="stats" element={<PluginStats />} />
          <Route path="manage" element={<PluginManage />} />
        </Route>

        {/* 运营管理 */}
        <Route path="operations">
          <Route index element={<Overview />} />
          <Route path="maintenance" element={<Maintenance />} />
          <Route path="security" element={<Security />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="crm" element={<CRM />} />
          <Route path="marketing" element={<Marketing />} />
          <Route path="finance" element={<Finance />} />
        </Route>

        {/* UI配置 */}
        <Route path="settings">
          <Route index element={<UISettings />} />
          <Route path="logo" element={<LogoSettings />} />
          <Route path="theme" element={<ThemeSettings />} />
          <Route path="layout" element={<LayoutSettings />} />
          <Route path="animation" element={<AnimationSettings />} />
        </Route>

        {/* 更新管理 */}
        <Route path="updates">
          <Route index element={<UpdateCenter />} />
          <Route path="history" element={<VersionHistory />} />
          <Route path="announcements" element={<Announcements />} />
          <Route path="recommendations" element={<PluginRecommendations />} />
        </Route>

        {/* 智能助手 */}
        <Route path="assistant">
          <Route index element={<Assistant />} />
          <Route path="monitor" element={<SystemMonitor />} />
          <Route path="alerts" element={<Alerts />} />
          <Route path="support" element={<DecisionSupport />} />
        </Route>
      </Route>
    </>
  )
)

export default function AppRouter() {
  return <RouterProvider router={router} />
}
