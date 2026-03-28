import React, { useEffect } from 'react'
import { Routes, Route, useNavigate } from 'react-router-dom'
import { useAuthRequestStore } from '@/stores/authRequestStore'
import AuthRequestList from './components/AuthRequestList'
import AuthRequestDetail from './components/AuthRequestDetail'
import AuthRequestReview from './components/AuthRequestReview'
import BatchReviewModal from './components/BatchReviewModal'
import AuthHistoryView from './components/AuthHistoryView'
import AuthStatisticsView from './components/AuthStatisticsView'
import RejectReasonManagement from './components/RejectReasonManagement'
import MaterialReviewView from './components/MaterialReviewView'
import AuthResultQuery from './components/AuthResultQuery'
import AppealManagement from './components/AppealManagement'
import AuthDataExport from './components/AuthDataExport'
import AuthReportGenerator from './components/AuthReportGenerator'
import AuthOperationLogView from './components/AuthOperationLogView'
import AuthTagManagement from './components/AuthTagManagement'

export const AuthAssistModule: React.FC = () => {
  const navigate = useNavigate()

  return (
    <Routes>
      <Route index element={<AuthRequestList />} />
      <Route path=":id" element={<AuthRequestDetail />} />
      <Route path=":id/review" element={<AuthRequestReview />} />
      <Route path="batch" element={<AuthRequestList />} />
      <Route path="history" element={<AuthHistoryView />} />
      <Route path="statistics" element={<AuthStatisticsView />} />
      <Route path="reject-reasons" element={<RejectReasonManagement />} />
      <Route path="material-review" element={<MaterialReviewView />} />
      <Route path="query" element={<AuthResultQuery />} />
      <Route path="appeals" element={<AppealManagement />} />
      <Route path="export" element={<AuthDataExport />} />
      <Route path="reports" element={<AuthReportGenerator />} />
      <Route path="logs" element={<AuthOperationLogView />} />
      <Route path="tags" element={<AuthTagManagement />} />
    </Routes>
  )
}

export default AuthAssistModule
