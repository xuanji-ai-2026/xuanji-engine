import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { HomePage } from './pages/common/HomePage';
import { NotFoundPage } from './pages/common/NotFoundPage';
import { ApiPage } from './pages/api/ApiPage';
import { PluginPage } from './pages/plugin/PluginPage';
import { SdkPage } from './pages/sdk/SdkPage';
import { AssistantPage } from './pages/assistant/AssistantPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="api" element={<ApiPage />} />
          <Route path="plugin" element={<PluginPage />} />
          <Route path="sdk" element={<SdkPage />} />
          <Route path="assistant" element={<AssistantPage />} />
          <Route path="404" element={<NotFoundPage />} />
          <Route path="*" element={<Navigate to="/404" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};
