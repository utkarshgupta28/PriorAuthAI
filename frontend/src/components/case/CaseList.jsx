import React from 'react'
import { useNavigate } from 'react-router-dom'
import { FileText, Loader, Trash2 } from 'lucide-react'

const STATUS_CONFIG = {
  intake: { label: 'Intake', color: 'bg-gray-100 text-gray-600 border border-gray-200' },
  processing: { label: 'Processing', color: 'bg-blue-50 text-blue-600 border border-blue-100' },
  analyzed: { label: 'Analyzed', color: 'bg-blue-50 text-blue-600 border border-blue-100' },
  submitted: { label: 'Submitted', color: 'bg-yellow-50 text-yellow-600 border border-yellow-100' },
  approved: { label: 'Approved', color: 'bg-green-50 text-green-600 border border-green-100' },
  denied: { label: 'Denied', color: 'bg-red-50 text-red-500 border border-red-100' },
  error: { label: 'Error', color: 'bg-red-50 text-red-500 border border-red-100' },
}

export default function CaseList({
  cases,
  onCaseSelect,
  onAppealRequest,
  highlightedCaseId,
  onDeleteCase,
  deletingCaseId,
}) {
  const navigate = useNavigate()

  const handleSelect = (id) => {
    if (onCaseSelect) {
      onCaseSelect(id)
      return
    }
    navigate(`/cases/${id}`)
  }

  const handleAppeal = (event, id) => {
    event.stopPropagation()
    if (onAppealRequest) {
      onAppealRequest(id)
      return
    }
    navigate(`/cases/${id}/run`)
  }

  const handleDelete = (event, id) => {
    event.stopPropagation()
    onDeleteCase?.(id)
  }

  if (!cases || cases.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <FileText className="w-12 h-12 mx-auto mb-3 opacity-30" />
        <p>No cases yet.</p>
      </div>
    )
  }

  return (
    <div className="grid gap-3">
      {cases.map((c) => {
        const statusConf = STATUS_CONFIG[c.status] || STATUS_CONFIG.intake
        const isHighlighted = c.id === highlightedCaseId
        return (
          <div
            key={c.id}
            onClick={() => handleSelect(c.id)}
            className={`rounded-xl border bg-white p-4 cursor-pointer shadow-sm transition hover:border-blue-200 hover:shadow-md ${
              isHighlighted ? 'border-blue-300 ring-2 ring-blue-100' : 'border-gray-200'
            }`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-gray-900 font-semibold truncate">{c.patient_name}</span>
                  <span className="text-gray-400 text-xs">#{c.id}</span>
                  {!c.is_demo_case && c.status === 'intake' && (
                    <span className="rounded-full border border-blue-100 bg-blue-50 px-2 py-0.5 text-[11px] font-medium text-blue-600">
                      New
                    </span>
                  )}
                </div>
                <div className="text-gray-500 text-sm truncate">
                  {c.diagnosis_code && (
                    <span className="text-blue-600 mr-1">{c.diagnosis_code}</span>
                  )}
                  {c.diagnosis_description}
                  {c.treatment_cpt_code && (
                    <span className="text-gray-400 ml-2">{'->'} CPT {c.treatment_cpt_code}</span>
                  )}
                </div>
                <div className="text-gray-400 text-xs mt-1 flex items-center gap-3">
                  <span>{c.insurance_plan}</span>
                  <span>{new Date(c.created_at).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                {c.status === 'denied' && (
                  <button
                    onClick={(event) => handleAppeal(event, c.id)}
                    className="rounded-full border border-red-100 bg-red-50 px-2.5 py-1 text-xs font-medium text-red-600 transition hover:bg-red-100"
                  >
                    Request Appeal
                  </button>
                )}
                <span
                  className={`px-2 py-0.5 rounded-full text-xs font-medium whitespace-nowrap ${statusConf.color}`}
                >
                  {statusConf.label}
                </span>
                {!c.is_demo_case && (
                  <button
                    onClick={(event) => handleDelete(event, c.id)}
                    disabled={deletingCaseId === c.id}
                    className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-red-100 bg-red-50 text-red-500 transition hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-60"
                    aria-label={`Delete case ${c.patient_name}`}
                    title="Delete case"
                  >
                    {deletingCaseId === c.id ? <Loader className="h-3.5 w-3.5 animate-spin" /> : <Trash2 className="h-3.5 w-3.5" />}
                  </button>
                )}
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
