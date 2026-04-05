import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Save, Loader, Zap } from 'lucide-react'
import { createCase, getDemoPresets } from '../../api'

const INSURANCE_PLANS = [
  'Aetna PPO Gold',
  'UnitedHealthcare Choice Plus',
  'Cigna Open Access Plus',
  'Blue Cross Blue Shield PPO',
  'Medicare Advantage (Humana Gold Plus)',
  'Other',
]

export default function CaseForm() {
  const navigate = useNavigate()
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [demoPresets, setDemoPresets] = useState([])
  const [form, setForm] = useState({
    patient_name: '',
    patient_dob: '',
    patient_id: '',
    insurance_plan: '',
    insurance_id: '',
    diagnosis_code: '',
    diagnosis_description: '',
    proposed_treatment: '',
    treatment_cpt_code: '',
    clinical_notes: '',
    lab_results: '',
  })

  useEffect(() => {
    const loadDemoPresets = async () => {
      try {
        const res = await getDemoPresets()
        setDemoPresets(res.data || [])
      } catch (_) {
        setDemoPresets([])
      }
    }

    loadDemoPresets()
  }, [])

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.patient_name.trim()) {
      setError('Patient name is required')
      return
    }
    setSubmitting(true)
    setError(null)
    try {
      const res = await createCase(form)
      navigate(`/?created=${res.data.id}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create case')
      setSubmitting(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex items-center gap-3 mb-6">
        <button
          onClick={() => navigate('/')}
          className="text-gray-500 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">New Prior Authorization Case</h1>
          <p className="text-gray-500 text-sm">Capture patient, payer, and clinical details for review.</p>
        </div>
      </div>

      <div className="mb-4 bg-white border border-gray-200 rounded-xl p-4 shadow-sm">
        <div className="flex items-center gap-2 flex-wrap">
          <Zap className="w-3.5 h-3.5 text-blue-600 flex-shrink-0" />
          <span className="text-gray-500 text-xs font-medium">Quick-fill demo case:</span>
          {demoPresets.map((preset) => (
            <button
              key={preset.key}
              type="button"
              onClick={() => setForm((f) => ({ ...f, ...(preset.data || {}) }))}
              className="px-3 py-1 text-xs bg-gray-50 hover:bg-blue-50 text-gray-700 rounded-lg border border-gray-200 transition-colors"
            >
              {preset.label}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded-xl p-3 text-red-600 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <Section title="Patient Information">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Field label="Full Name" required>
              <input type="text" value={form.patient_name} onChange={set('patient_name')} placeholder="e.g. Maria Rodriguez" className={inputClass} required />
            </Field>
            <Field label="Date of Birth">
              <input type="date" value={form.patient_dob} onChange={set('patient_dob')} className={inputClass} />
            </Field>
            <Field label="Patient ID">
              <input type="text" value={form.patient_id} onChange={set('patient_id')} placeholder="e.g. MR-20240315" className={inputClass} />
            </Field>
          </div>
        </Section>

        <Section title="Insurance Information">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Field label="Insurance Plan">
              <select value={form.insurance_plan} onChange={set('insurance_plan')} className={inputClass}>
                <option value="">Select plan...</option>
                {INSURANCE_PLANS.map((p) => (
                  <option key={p} value={p}>{p}</option>
                ))}
              </select>
            </Field>
            <Field label="Member ID">
              <input type="text" value={form.insurance_id} onChange={set('insurance_id')} placeholder="e.g. AET-889921034" className={inputClass} />
            </Field>
          </div>
        </Section>

        <Section title="Diagnosis & Treatment">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Field label="ICD-10 Diagnosis Code">
              <input type="text" value={form.diagnosis_code} onChange={set('diagnosis_code')} placeholder="e.g. M17.11" className={inputClass} />
            </Field>
            <Field label="Diagnosis Description">
              <input type="text" value={form.diagnosis_description} onChange={set('diagnosis_description')} placeholder="e.g. Primary osteoarthritis, right knee" className={inputClass} />
            </Field>
            <Field label="Proposed Treatment">
              <input type="text" value={form.proposed_treatment} onChange={set('proposed_treatment')} placeholder="e.g. Total Knee Arthroplasty" className={inputClass} />
            </Field>
            <Field label="CPT Code">
              <input type="text" value={form.treatment_cpt_code} onChange={set('treatment_cpt_code')} placeholder="e.g. 27447" className={inputClass} />
            </Field>
          </div>
        </Section>

        <Section title="Clinical Documentation">
          <div className="space-y-4">
            <Field label="Clinical Notes">
              <textarea value={form.clinical_notes} onChange={set('clinical_notes')} rows={5} placeholder="Patient history, failed treatments, exam findings, imaging results..." className={inputClass} />
            </Field>
            <Field label="Lab Results">
              <textarea value={form.lab_results} onChange={set('lab_results')} rows={3} placeholder="Recent lab values, pathology results, imaging reports..." className={inputClass} />
            </Field>
          </div>
        </Section>

        <div className="flex justify-end gap-3 pt-2">
          <button
            type="button"
            onClick={() => navigate('/')}
            className="px-4 py-2 rounded-xl border border-gray-200 text-gray-600 hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white px-5 py-2 rounded-xl transition-colors font-medium shadow-sm"
          >
            {submitting ? <Loader className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
            {submitting ? 'Creating...' : 'Create Case'}
          </button>
        </div>
      </form>
    </div>
  )
}

const inputClass =
  'w-full bg-white border border-gray-200 rounded-xl px-3 py-2.5 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-colors text-sm'

function Section({ title, children }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
      <h3 className="text-gray-900 font-semibold text-sm mb-4 uppercase tracking-[0.18em]">{title}</h3>
      {children}
    </div>
  )
}

function Field({ label, required, children }) {
  return (
    <div>
      <label className="block text-gray-500 text-xs mb-1.5">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      {children}
    </div>
  )
}
