import { Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { LoginPage } from './pages/LoginPage'
import { Dashboard } from './pages/Dashboard'

// 模块路由
import { AuthAssistModule } from './modules/auth/AuthAssistModule'
import { ConfigAssistModule } from './modules/config/ConfigAssistModule'
import { WorkbenchModule } from './modules/workbench/WorkbenchModule'
import AssistantModule from './modules/assistant/AssistantModule'
import { UserManagementModule } from './modules/user/UserManagementModule'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="auth/*" element={<AuthAssistModule />} />
        <Route path="config/*" element={<ConfigAssistModule />} />
        <Route path="workbench/*" element={<WorkbenchModule />} />
        <Route path="assistant/*" element={<AssistantModule />} />
        <Route path="user/*" element={<UserManagementModule />} />
      </Route>
    </Routes>
  )
}

export default App
