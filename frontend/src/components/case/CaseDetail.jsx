import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Play, User, FileText, Bot, History, AlertCircle, Loader } from 'lucide-react'
import { getCase } from '../../api'
import StatusTimeline from '../shared/StatusTimeline'
import PipelineStepOutput from '../pipeline/PipelineStepOutput'

const TABS = [
  { id: 'patient', label: 'Patient & Insurance', icon: User },
  { id: 'clinical', label: 'Clinical Data', icon: FileText },
  { id: 'outputs', label: 'Pipeline Outputs', icon: Bot },
  { id: 'history', label: 'Status History', icon: History },
]

export default function CaseDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('patient')

  useEffect(() => {
    const load = async () => {
      try {
        const res = await getCase(id)
        setData(res.data)
      } catch (e) {
        setError(e.response?.data?.detail || 'Failed to load case')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [id])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="bg-white border border-red-200 rounded-xl p-6 text-center shadow-sm">
          <AlertCircle className="w-8 h-8 text-red-500 mx-auto mb-2" />
          <p className="text-red-600">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="mt-4 inline-flex items-center justify-center rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
          >
            Back to Cases
          </button>
        </div>
      </div>
    )
  }

  const { case: c, provider_context, agent_outputs, status_history } = data

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start gap-3">
          <button
            onClick={() => navigate('/')}
            className="text-gray-500 hover:text-gray-900 transition-colors mt-1"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-semibold text-gray-900">{c.patient_name}</h1>
              <span className="text-gray-400 text-sm">#{c.id}</span>
            </div>
            <p className="text-gray-500 text-sm">
              {c.diagnosis_code && <span className="text-blue-600">{c.diagnosis_code} - </span>}
              {c.diagnosis_description}
            </p>
            <p className="text-gray-400 text-xs mt-0.5">
              {c.insurance_plan} · CPT {c.treatment_cpt_code}
            </p>
          </div>
        </div>
        <button
          onClick={() => navigate(`/cases/${id}/run`)}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl transition-colors font-medium text-sm shadow-sm"
        >
          <Play className="w-4 h-4" />
          Run Pipeline
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-4 mb-4 shadow-sm">
        <StatusTimeline currentStatus={c.status} />
      </div>

      <div className="flex gap-1 mb-4 bg-white border border-gray-200 rounded-xl p-1 shadow-sm">
        {TABS.map(({ id: tabId, label, icon: Icon }) => (
          <button
            key={tabId}
            onClick={() => setActiveTab(tabId)}
            className={`flex items-center gap-1.5 px-3 py-2 rounded text-sm transition-colors flex-1 justify-center ${
              activeTab === tabId ? 'bg-blue-50 text-blue-600' : 'text-gray-500 hover:text-gray-900'
            }`}
          >
            <Icon className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{label}</span>
          </button>
        ))}
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
        {activeTab === 'patient' && <PatientTab c={c} providerContext={provider_context} />}
        {activeTab === 'clinical' && <ClinicalTab c={c} />}
        {activeTab === 'outputs' && <OutputsTab outputs={agent_outputs} navigate={navigate} id={id} />}
        {activeTab === 'history' && <HistoryTab history={status_history} />}
      </div>
    </div>
  )
}

function Row({ label, value }) {
  return (
    <div className="flex gap-2">
      <span className="text-gray-500 text-sm w-40 flex-shrink-0">{label}</span>
      <span className="text-gray-900 text-sm">{value || '-'}</span>
    </div>
  )
}

function PatientTab({ c, providerContext }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <h4 className="text-gray-500 text-xs font-semibold uppercase tracking-[0.18em] mb-3">Patient</h4>
        <div className="space-y-2">
          <Row label="Full Name" value={c.patient_name} />
          <Row label="Date of Birth" value={c.patient_dob} />
          <Row label="Patient ID" value={c.patient_id} />
        </div>
      </div>
      <div>
        <h4 className="text-gray-500 text-xs font-semibold uppercase tracking-[0.18em] mb-3">Insurance</h4>
        <div className="space-y-2">
          <Row label="Plan" value={c.insurance_plan} />
          <Row label="Member ID" value={c.insurance_id} />
        </div>
      </div>
      {providerContext && (
        <div className="md:col-span-2">
          <h4 className="text-gray-500 text-xs font-semibold uppercase tracking-[0.18em] mb-3">Requesting Provider</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Row label="Provider Name" value={providerContext.provider_name} />
              <Row label="NPI" value={providerContext.provider_npi} />
              <Row label="Phone" value={providerContext.provider_phone} />
              <Row label="Fax" value={providerContext.provider_fax} />
            </div>
            <div className="space-y-2">
              <Row label="Specialty" value={providerContext.provider_specialty} />
              <Row label="Facility" value={providerContext.facility_name} />
              <Row label="Service Date" value={providerContext.service_date_requested} />
              <Row label="Place of Service" value={providerContext.service_location} />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function ClinicalTab({ c }) {
  return (
    <div className="space-y-4">
      <div>
        <h4 className="text-gray-500 text-xs font-semibold uppercase tracking-[0.18em] mb-2">Diagnosis & Treatment</h4>
        <div className="space-y-2">
          <Row label="ICD-10 Code" value={c.diagnosis_code} />
          <Row label="Diagnosis" value={c.diagnosis_description} />
          <Row label="Proposed Treatment" value={c.proposed_treatment} />
          <Row label="CPT Code" value={c.treatment_cpt_code} />
        </div>
      </div>
      {c.clinical_notes && (
        <div>
          <h4 className="text-gray-500 text-xs font-semibold uppercase tracking-[0.18em] mb-2">Clinical Notes</h4>
          <div className="bg-gray-50 rounded-xl p-3 text-gray-700 text-sm leading-relaxed border border-gray-200">
            {c.clinical_notes}
          </div>
        </div>
      )}
      {c.lab_results && (
        <div>
          <h4 className="text-gray-500 text-xs font-semibold uppercase tracking-[0.18em] mb-2">Lab Results</h4>
          <div className="bg-gray-50 rounded-xl p-3 text-gray-700 text-sm leading-relaxed border border-gray-200">
            {c.lab_results}
          </div>
        </div>
      )}
    </div>
  )
}

function OutputsTab({ outputs, navigate, id }) {
  if (!outputs || outputs.length === 0) {
    return (
      <div className="text-center py-8">
        <Bot className="w-10 h-10 text-gray-300 mx-auto mb-3" />
        <p className="text-gray-500 mb-3">No pipeline outputs yet.</p>
        <button
          onClick={() => navigate(`/cases/${id}/run`)}
          className="text-blue-600 hover:underline text-sm"
        >
          Run the pipeline to analyze this case
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {outputs.map((o, i) => (
        <PipelineStepOutput key={o.id || i} agentName={o.agent_name} outputData={o.output_data} />
      ))}
    </div>
  )
}

function HistoryTab({ history }) {
  if (!history || history.length === 0) {
    return <p className="text-gray-500 text-sm">No status history available.</p>
  }

  return (
    <div className="space-y-2">
      {[...history].reverse().map((h, i) => (
        <div key={h.id || i} className="flex items-start gap-3 py-2 border-b border-gray-100 last:border-0">
          <div className="w-2 h-2 rounded-full bg-blue-600 mt-1.5 flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 text-sm">
              {h.old_status && (
                <>
                  <span className="text-gray-400">{h.old_status}</span>
                  <span className="text-gray-300">{'->'}</span>
                </>
              )}
              <span className="text-gray-900 font-medium">{h.new_status}</span>
            </div>
            {h.notes && <p className="text-gray-500 text-xs mt-0.5">{h.notes}</p>}
            <p className="text-gray-400 text-xs mt-0.5">
              {new Date(h.created_at).toLocaleString()}
            </p>
          </div>
        </div>
      ))}
    </div>
  )
}

