import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';

// Layouts
import MainLayout from '@/layouts/MainLayout';
import AuthLayout from '@/layouts/AuthLayout';

// Pages - Auth
import LoginPage from '@/pages/auth/LoginPage';
import RegisterPage from '@/pages/auth/RegisterPage';
import ForgotPasswordPage from '@/pages/auth/ForgotPasswordPage';
import ResetPasswordPage from '@/pages/auth/ResetPasswordPage';

// Pages - Main
import DashboardPage from '@/pages/dashboard/DashboardPage';
import ProfilePage from '@/pages/user/ProfilePage';
import SettingsPage from '@/pages/user/SettingsPage';

// Pages - Authorization
import StaffPage from '@/pages/authorization/StaffPage';
import PermissionsPage from '@/pages/authorization/PermissionsPage';
import RolesPage from '@/pages/authorization/RolesPage';

// Pages - Smart Config
import SmartConfigPage from '@/pages/smart-config/SmartConfigPage';
import ConfigHistoryPage from '@/pages/smart-config/ConfigHistoryPage';

// Pages - Auto Generation
import AutoGeneratePage from '@/pages/auto-generate/AutoGeneratePage';
import PersonalityConfigPage from '@/pages/auto-generate/PersonalityConfigPage';
import EmotionConfigPage from '@/pages/auto-generate/EmotionConfigPage';
import PluginConfigPage from '@/pages/auto-generate/PluginConfigPage';
import KnowledgeConfigPage from '@/pages/auto-generate/KnowledgeConfigPage';

// Pages - Digital Human
import DigitalHumanListPage from '@/pages/digital-human/DigitalHumanListPage';
import DigitalHumanCreatePage from '@/pages/digital-human/DigitalHumanCreatePage';
import DigitalHumanDetailPage from '@/pages/digital-human/DigitalHumanDetailPage';

// Pages - Chat
import ChatPage from '@/pages/chat/ChatPage';
import ChatHistoryPage from '@/pages/chat/ChatHistoryPage';

// Pages - Plugin Market
import PluginMarketPage from '@/pages/plugin-market/PluginMarketPage';
import MyPluginsPage from '@/pages/plugin-market/MyPluginsPage';

// Pages - Billing
import AccountPage from '@/pages/billing/AccountPage';
import RechargePage from '@/pages/billing/RechargePage';
import BillsPage from '@/pages/billing/BillsPage';
import InvoicePage from '@/pages/billing/InvoicePage';

// Pages - Assistant
import AssistantPage from '@/pages/assistant/AssistantPage';

// Components
import ProtectedRoute from '@/components/auth/ProtectedRoute';

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return (
    <Routes>
      {/* Auth Routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />
      </Route>

      {/* Main Routes */}
      <Route
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/settings" element={<SettingsPage />} />

        {/* Authorization */}
        <Route path="/staff" element={<StaffPage />} />
        <Route path="/permissions" element={<PermissionsPage />} />
        <Route path="/roles" element={<RolesPage />} />

        {/* Smart Config */}
        <Route path="/smart-config" element={<SmartConfigPage />} />
        <Route path="/config-history" element={<ConfigHistoryPage />} />

        {/* Auto Generation */}
        <Route path="/auto-generate" element={<AutoGeneratePage />} />
        <Route path="/personality" element={<PersonalityConfigPage />} />
        <Route path="/emotion" element={<EmotionConfigPage />} />
        <Route path="/plugin-config" element={<PluginConfigPage />} />
        <Route path="/knowledge" element={<KnowledgeConfigPage />} />

        {/* Digital Human */}
        <Route path="/digital-humans" element={<DigitalHumanListPage />} />
        <Route path="/digital-humans/create" element={<DigitalHumanCreatePage />} />
        <Route path="/digital-humans/:id" element={<DigitalHumanDetailPage />} />

        {/* Chat */}
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/chat/history" element={<ChatHistoryPage />} />

        {/* Plugin Market */}
        <Route path="/plugin-market" element={<PluginMarketPage />} />
        <Route path="/my-plugins" element={<MyPluginsPage />} />

        {/* Billing */}
        <Route path="/account" element={<AccountPage />} />
        <Route path="/recharge" element={<RechargePage />} />
        <Route path="/bills" element={<BillsPage />} />
        <Route path="/invoices" element={<InvoicePage />} />

        {/* Assistant */}
        <Route path="/assistant" element={<AssistantPage />} />
      </Route>

      {/* Catch all */}
      <Route
        path="*"
        element={
          <Navigate to={isAuthenticated ? '/dashboard' : '/login'} replace />
        }
      />
    </Routes>
  );
}

export default App;
