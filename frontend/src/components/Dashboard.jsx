import React, { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Plus, Activity, CheckCircle, Clock3, FileText, TrendingUp, AlertCircle } from 'lucide-react'
import { deleteCase, getCases, getMetrics } from '../api'
import CaseList from './case/CaseList'

export default function Dashboard() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [cases, setCases] = useState([])
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [deletingCaseId, setDeletingCaseId] = useState(null)
  const [error, setError] = useState(null)
  const [activeFilter, setActiveFilter] = useState('total')
  const createdCaseId = Number(searchParams.get('created')) || null

  useEffect(() => {
    const load = async () => {
      try {
        const [casesRes, metricsRes] = await Promise.all([getCases(), getMetrics()])
        setCases(casesRes.data)
        setMetrics(metricsRes.data)
      } catch (e) {
        setError('Failed to connect to backend. Is the server running on port 8000?')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mx-auto mb-3" />
          <p className="text-gray-500">Loading PriorAuth AI...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="bg-white border border-red-200 rounded-xl p-6 max-w-md text-center shadow-sm">
          <AlertCircle className="w-8 h-8 text-red-500 mx-auto mb-2" />
          <p className="text-red-600">{error}</p>
          <p className="text-gray-500 text-sm mt-2">`cd backend && uvicorn main:app --reload --port 8000`</p>
        </div>
      </div>
    )
  }

  const realCases = cases.filter((item) => !item.is_demo_case)

  const filterCases = (items, filter) => {
    if (filter === 'in_progress') {
      return items.filter((item) => ['intake', 'processing'].includes(item.status))
    }
    if (filter === 'analyzed') {
      return items.filter((item) => item.status === 'analyzed')
    }
    if (filter === 'approved') {
      return items.filter((item) => item.status === 'approved')
    }
    if (filter === 'denied') {
      return items.filter((item) => item.status === 'denied')
    }
    return items
  }

  const visibleCases = filterCases(realCases, activeFilter)
  const listTitle = {
    total: 'Prior Authorization Cases',
    in_progress: 'In Progress Cases',
    analyzed: 'Analyzed Cases',
    approved: 'Approved Cases',
    denied: 'Denied Cases',
  }[activeFilter] || 'Prior Authorization Cases'

  const refreshDashboard = async () => {
    const [casesRes, metricsRes] = await Promise.all([getCases(), getMetrics()])
    setCases(casesRes.data)
    setMetrics(metricsRes.data)
  }

  const handleDeleteCase = async (caseId) => {
    const targetCase = cases.find((item) => item.id === caseId)
    const caseLabel = targetCase?.patient_name || `Case #${caseId}`
    if (!window.confirm(`Delete ${caseLabel}? This will remove the case and its review history.`)) {
      return
    }

    try {
      setDeletingCaseId(caseId)
      await deleteCase(caseId)
      await refreshDashboard()
    } catch (_) {
      window.alert('Unable to delete the case right now. Please try again.')
    } finally {
      setDeletingCaseId(null)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8 rounded-3xl border border-blue-100 bg-white/90 shadow-sm overflow-hidden">
        <div className="flex flex-col gap-6 px-6 py-7 md:flex-row md:items-end md:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-xs font-medium text-blue-600">
              <Activity className="h-3.5 w-3.5" />
              Clinical decision support
            </div>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight text-gray-900">
              PriorAuth AI
            </h1>
            <p className="mt-2 max-w-2xl text-sm text-gray-500">
              Healthcare prior authorization workflow for case intake, AI analysis, and submission readiness.
            </p>
          </div>
          <button
            onClick={() => navigate('/cases/new')}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm transition hover:bg-blue-700"
          >
            <Plus className="w-4 h-4" />
            New Case
          </button>
        </div>
      </div>

      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold uppercase tracking-[0.18em] text-gray-500">
          Operations Overview
        </h2>
      </div>

      {metrics && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          <MetricCard
            icon={<FileText className="w-5 h-5 text-blue-600" />}
            label="Total Cases"
            value={metrics.total_cases}
            accent="text-blue-600"
            active={activeFilter === 'total'}
            onClick={() => setActiveFilter('total')}
          />
          <MetricCard
            icon={<Clock3 className="w-5 h-5 text-yellow-500" />}
            label="In Progress"
            value={metrics.in_progress + metrics.intake}
            accent="text-yellow-500"
            active={activeFilter === 'in_progress'}
            onClick={() => setActiveFilter('in_progress')}
          />
          <MetricCard
            icon={<TrendingUp className="w-5 h-5 text-blue-600" />}
            label="Analyzed"
            value={metrics.analyzed ?? 0}
            accent="text-blue-600"
            active={activeFilter === 'analyzed'}
            onClick={() => setActiveFilter('analyzed')}
          />
          <MetricCard
            icon={<CheckCircle className="w-5 h-5 text-green-600" />}
            label="Approved"
            value={metrics.approved}
            accent="text-green-600"
            active={activeFilter === 'approved'}
            onClick={() => setActiveFilter('approved')}
          />
          <MetricCard
            icon={<AlertCircle className="w-5 h-5 text-red-500" />}
            label="Denied"
            value={metrics.denied}
            accent="text-red-500"
            active={activeFilter === 'denied'}
            onClick={() => setActiveFilter('denied')}
          />
        </div>
      )}

      <div>
        <h2 className="text-gray-900 font-semibold mb-3 text-sm uppercase tracking-[0.18em]">
          {listTitle} ({visibleCases.length})
        </h2>
        {visibleCases.length === 0 ? (
          <div className="rounded-2xl border border-gray-200 bg-white py-12 text-center text-gray-500 shadow-sm">
            <FileText className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p>No cases match this view.</p>
            <button
              onClick={() => setActiveFilter('total')}
              className="mt-3 text-blue-600 hover:underline text-sm"
            >
              Show all cases
            </button>
          </div>
        ) : (
          <CaseList
            cases={visibleCases}
            onCaseSelect={(caseId) => navigate(`/cases/${caseId}`)}
            onAppealRequest={(caseId) => navigate(`/cases/${caseId}/run`)}
            highlightedCaseId={createdCaseId}
            onDeleteCase={handleDeleteCase}
            deletingCaseId={deletingCaseId}
          />
        )}
      </div>
    </div>
  )
}

function MetricCard({ icon, label, value, accent, active = false, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-xl border bg-white p-4 text-left shadow-sm transition hover:border-blue-200 hover:shadow-md ${
        active ? 'border-blue-200 ring-2 ring-blue-100' : 'border-gray-200'
      }`}
    >
      <div className="flex items-center gap-2 mb-1">
        {icon}
        <span className="text-gray-500 text-xs">{label}</span>
      </div>
      <div className={`text-2xl font-semibold ${accent}`}>{value}</div>
    </button>
  )
}
