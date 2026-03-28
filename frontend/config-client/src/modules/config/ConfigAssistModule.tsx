import React, { useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import ConfigRequestList from './components/ConfigRequestList'
import ConfigRequestDetail from './components/ConfigRequestDetail'
import ConfigRequestCreate from './components/ConfigRequestCreate'
import ConfigRequestEdit from './components/ConfigRequestEdit'

export const ConfigAssistModule: React.FC = () => {
  return (
    <Routes>
      <Route index element={<ConfigRequestList />} />
      <Route path="create" element={<ConfigRequestCreate />} />
      <Route path=":id" element={<ConfigRequestDetail />} />
      <Route path=":id/edit" element={<ConfigRequestEdit />} />
    </Routes>
  )
}

export default ConfigAssistModule
