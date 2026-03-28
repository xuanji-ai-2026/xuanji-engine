import React, { useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import TaskList from './components/TaskList'
import TaskDetail from './components/TaskDetail'
import TaskCreate from './components/TaskCreate'

export const WorkbenchModule: React.FC = () => {
  return (
    <Routes>
      <Route index element={<TaskList />} />
      <Route path="create" element={<TaskCreate />} />
      <Route path=":id" element={<TaskDetail />} />
    </Routes>
  )
}

export default WorkbenchModule
