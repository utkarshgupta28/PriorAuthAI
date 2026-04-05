import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import CaseForm from './components/case/CaseForm'
import CaseDetail from './components/case/CaseDetail'
import PipelineView from './components/pipeline/PipelineView'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 text-gray-900">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/cases/new" element={<CaseForm />} />
          <Route path="/cases/:id" element={<CaseDetail />} />
          <Route path="/cases/:id/run" element={<PipelineView />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
