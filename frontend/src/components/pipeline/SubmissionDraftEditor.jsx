import React, { useEffect, useState } from 'react'
import { CheckCircle2, FilePenLine, Loader, Save, Send, ShieldCheck, Upload, X } from 'lucide-react'

const REQUIRED_FIELDS = [
  'provider_name',
  'provider_npi',
  'provider_phone',
  'service_date_requested',
  'insurance_id',
  'diagnosis_code',
  'procedure_description',
  'medical_necessity_letter',
]

const FIELD_LABELS = {
  provider_name: 'Provider Name',
  provider_npi: 'Provider NPI',
  provider_phone: 'Provider Phone',
  service_date_requested: 'Requested Service Date',
  insurance_id: 'Insurance Member ID',
  diagnosis_code: 'Diagnosis Code',
  procedure_description: 'Procedure Description',
  medical_necessity_letter: 'Justification Letter',
}

function isBlank(value) {
  return !String(value || '').trim()
}

function formatFailedTreatment(item) {
  if (typeof item === 'string') return item
  if (item && typeof item === 'object') {
    const treatment = String(item.treatment || '').trim()
    const outcome = String(item.outcome || '').trim()
    if (treatment && outcome) return `${treatment}: ${outcome}`
    return treatment || outcome || 'Treatment history documented'
  }
  return String(item || '').trim()
}

function buildDraft({ caseData, providerContext, submissionOutput, intelligenceOutput, insights }) {
  const filledForm = submissionOutput?.parsed_output?.filled_form || {}
  return {
    patient_name: caseData?.patient_name || '',
    insurance_plan: caseData?.insurance_plan || '',
    insurance_id: filledForm.insurance_id || caseData?.insurance_id || '',
    provider_name: filledForm.provider_name || providerContext?.provider_name || '',
    provider_npi: filledForm.provider_npi || providerContext?.provider_npi || '',
    provider_phone: filledForm.provider_phone || providerContext?.provider_phone || '',
    provider_fax: filledForm.provider_fax || providerContext?.provider_fax || '',
    provider_specialty: filledForm.provider_specialty || providerContext?.provider_specialty || '',
    facility_name: filledForm.facility_name || providerContext?.facility_name || '',
    service_date_requested: filledForm.service_date_requested || providerContext?.service_date_requested || '',
    service_location: filledForm.service_location || providerContext?.service_location || '',
    urgency: filledForm.urgency || providerContext?.urgency || '',
    diagnosis_code: filledForm.diagnosis_code_primary || filledForm.diagnosis_code || caseData?.diagnosis_code || '',
    diagnosis_description: filledForm.diagnosis_description || caseData?.diagnosis_description || '',
    cpt_code: filledForm.cpt_code || caseData?.treatment_cpt_code || '',
    procedure_description: filledForm.procedure_description || caseData?.proposed_treatment || '',
    clinical_summary: filledForm.clinical_summary || caseData?.clinical_notes || '',
    medical_necessity_letter:
      filledForm.medical_necessity_letter ||
      intelligenceOutput?.parsed_output?.medical_necessity_letter ||
      '',
    submission_method:
      submissionOutput?.parsed_output?.submission_method || 'Payer portal or fax per plan requirements',
    review_notes: (insights?.suggestions || []).join('\n'),
  }
}

function mergeStoredDraftWithFreshDraft(storedDraft, freshDraft) {
  const parsedStoredDraft = storedDraft && typeof storedDraft === 'object' ? storedDraft : {}
  return {
    ...freshDraft,
    ...parsedStoredDraft,
    medical_necessity_letter: freshDraft.medical_necessity_letter || parsedStoredDraft.medical_necessity_letter || '',
    clinical_summary: freshDraft.clinical_summary || parsedStoredDraft.clinical_summary || '',
    review_notes: freshDraft.review_notes || parsedStoredDraft.review_notes || '',
  }
}

function getMissingFields(draft) {
  return REQUIRED_FIELDS.filter((field) => isBlank(draft?.[field]))
}

function DraftField({ label, value, onChange, rows = 1 }) {
  const className =
    'w-full rounded-xl border border-gray-200 bg-white px-3 py-2.5 text-sm text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100'

  return (
    <label className="block">
      <span className="mb-1.5 block text-xs font-medium uppercase tracking-[0.16em] text-gray-500">
        {label}
      </span>
      {rows > 1 ? (
        <textarea value={value} onChange={onChange} rows={rows} className={className} />
      ) : (
        <input value={value} onChange={onChange} className={className} />
      )}
    </label>
  )
}

export default function SubmissionDraftEditor({
  caseId,
  caseData,
  providerContext,
  policyOutput,
  submissionOutput,
  intelligenceOutput,
  insights,
  onSubmit,
  onDocumentsChange,
  submitting = false,
  submitLocked = false,
}) {
  const storageKey = `priorauth:draft:${caseId}`
  const [draft, setDraft] = useState(() =>
    buildDraft({ caseData, providerContext, submissionOutput, intelligenceOutput, insights }),
  )
  const [savedAt, setSavedAt] = useState(null)
  const [doctorApproved, setDoctorApproved] = useState(false)
  const [uploadedDocuments, setUploadedDocuments] = useState([])

  const failedTreatmentsRaw = intelligenceOutput?.parsed_output?.failed_treatments_documented
  const failedTreatments = Array.isArray(failedTreatmentsRaw)
    ? failedTreatmentsRaw.map(formatFailedTreatment).filter(Boolean)
    : []
  const guidelines = intelligenceOutput?.parsed_output?.guidelines_cited || []
  const payerCriteriaRaw = policyOutput?.parsed_output?.criteria_analysis
  const payerCriteria = (Array.isArray(payerCriteriaRaw) ? payerCriteriaRaw : [])
    .filter((item) => item?.criterion && item?.status && item.status !== 'Review Required')
    .slice(0, 3)

  useEffect(() => {
    const freshDraft = buildDraft({ caseData, providerContext, submissionOutput, intelligenceOutput, insights })
    const stored = window.localStorage.getItem(storageKey)
    if (stored) {
      try {
        setDraft(mergeStoredDraftWithFreshDraft(JSON.parse(stored), freshDraft))
        return
      } catch (_) {}
    }
    setDraft(freshDraft)
  }, [caseId, storageKey, caseData, providerContext, submissionOutput, intelligenceOutput, insights])

  const updateField = (field) => (event) => {
    const nextValue = event.target.value
    setDraft((current) => ({ ...current, [field]: nextValue }))
  }

  const handleSaveDraft = () => {
    window.localStorage.setItem(storageKey, JSON.stringify(draft))
    setSavedAt(new Date().toLocaleTimeString())
  }

  const handleDoctorApprovalChange = (event) => {
    if (!event.target.checked) {
      setDoctorApproved(false)
      return
    }

    if (missingFields.length > 0) {
      const missingLabels = missingFields.map((field) => FIELD_LABELS[field] || field)
      window.alert(`Fill these missing fields before doctor approval:\n\n${missingLabels.join('\n')}`)
      setDoctorApproved(false)
      return
    }

    setDoctorApproved(true)
  }

  const handleDocumentUpload = (event) => {
    const files = Array.from(event.target.files || []).map((file) => ({
      name: file.name,
      sizeLabel: `${Math.max(1, Math.round(file.size / 1024))} KB`,
    }))

    setUploadedDocuments((current) => {
      const nextFiles = [...current]
      files.forEach((file) => {
        if (!nextFiles.some((currentFile) => currentFile.name === file.name)) {
          nextFiles.push(file)
        }
      })
      onDocumentsChange?.(nextFiles)
      return nextFiles
    })

    event.target.value = ''
  }

  const handleRemoveDocument = (documentName) => {
    setUploadedDocuments((current) => {
      const nextFiles = current.filter((file) => file.name !== documentName)
      onDocumentsChange?.(nextFiles)
      return nextFiles
    })
  }

  const missingFields = getMissingFields(draft)
  const isReady = missingFields.length === 0
  const canSubmit = isReady && doctorApproved && !submitLocked && typeof onSubmit === 'function'

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <FilePenLine className="h-4 w-4 text-blue-600" />
            <h3 className="text-sm font-semibold uppercase tracking-[0.18em] text-gray-500">
              Submission Draft
            </h3>
          </div>
          <p className="mt-2 text-sm text-gray-500">
            Review and edit the application package before sending it to the insurance company.
          </p>
        </div>
        <div className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium ${
          isReady
            ? 'border-green-100 bg-green-50 text-green-700'
            : 'border-yellow-100 bg-yellow-50 text-yellow-700'
        }`}>
          <ShieldCheck className="h-3.5 w-3.5" />
          {isReady ? 'Application ready for submission' : `${missingFields.length} fields still need review`}
        </div>
      </div>

      {missingFields.length > 0 && (
        <div className="mt-4 rounded-xl border border-yellow-100 bg-yellow-50 p-3">
          <p className="text-sm font-medium text-yellow-800">Missing fields</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {missingFields.map((field) => (
              <span key={field} className="rounded-full border border-yellow-200 bg-white px-2 py-1 text-xs text-yellow-700">
                {field}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          onClick={handleSaveDraft}
          className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-3 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
        >
          <Save className="h-4 w-4" />
          Save Draft
        </button>
        {savedAt && <span className="self-center text-xs text-gray-500">Saved at {savedAt}</span>}
      </div>

      <div className="mt-4 rounded-xl border border-blue-100 bg-blue-50 p-4">
        <label className="flex items-start gap-3">
          <input
            type="checkbox"
            checked={doctorApproved}
            onChange={handleDoctorApprovalChange}
            className="mt-1 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <span>
            <span className="block text-sm font-medium text-gray-900">
              Doctor approval required before submission
            </span>
            <span className="mt-1 block text-sm text-gray-500">
              Confirm the application has been reviewed and approved by the requesting clinician before Agent 3 starts tracking.
            </span>
          </span>
        </label>

        <div className="mt-4 flex flex-wrap items-center gap-3">
          <button
            onClick={() => onSubmit?.(draft)}
            disabled={!canSubmit || submitting}
            className="inline-flex items-center gap-2 rounded-xl bg-green-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {submitting ? <Loader className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
            Submit To Insurance
          </button>
          <span className="text-sm text-gray-500">
            {submitLocked
              ? 'Submission already started for this review cycle.'
              : canSubmit
                ? 'Agent 3 will begin after submission.'
                : 'Complete required fields and confirm doctor approval to continue.'}
          </span>
        </div>
      </div>

      <div className="mt-5 grid gap-5">
        <div className="rounded-xl border border-gray-200 bg-gray-50 p-4">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-blue-600" />
            <p className="text-sm font-medium text-gray-900">Evidence Included In Review</p>
          </div>
          <p className="mt-1 text-sm text-gray-500">
            The justification letter is generated from the structured case record below, not on its own.
          </p>

          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-xs font-medium uppercase tracking-[0.16em] text-gray-500">Clinical Notes</p>
              <p className="mt-1 text-sm leading-relaxed text-gray-700">
                {caseData?.clinical_notes || 'No clinical notes available yet.'}
              </p>
            </div>
            <div>
              <p className="text-xs font-medium uppercase tracking-[0.16em] text-gray-500">Labs / Imaging / Findings</p>
              <p className="mt-1 text-sm leading-relaxed text-gray-700">
                {caseData?.lab_results || 'No supporting findings recorded yet.'}
              </p>
            </div>
            <div>
              <p className="text-xs font-medium uppercase tracking-[0.16em] text-gray-500">Prior Treatments Documented</p>
              {failedTreatments.length > 0 ? (
                <div className="mt-2 flex flex-wrap gap-2">
                  {failedTreatments.map((item) => (
                    <span
                      key={item}
                      className="rounded-full border border-gray-200 bg-white px-2 py-1 text-xs text-gray-700"
                    >
                      {item}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="mt-1 text-sm leading-relaxed text-gray-700">
                  No failed treatment history was extracted from the current chart note.
                </p>
              )}
            </div>
            <div>
              <p className="text-xs font-medium uppercase tracking-[0.16em] text-gray-500">Guidelines Cited</p>
              {guidelines.length > 0 ? (
                <div className="mt-2 flex flex-wrap gap-2">
                  {guidelines.map((item) => (
                    <span
                      key={`${item.organization}-${item.year}`}
                      className="rounded-full border border-gray-200 bg-white px-2 py-1 text-xs text-gray-700"
                    >
                      {item.organization} {item.year}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="mt-1 text-sm leading-relaxed text-gray-700">
                  No guideline citations were returned for this review yet.
                </p>
              )}
            </div>
          </div>

          {payerCriteria.length > 0 && (
            <div className="mt-4">
              <p className="text-xs font-medium uppercase tracking-[0.16em] text-gray-500">Payer Criteria Already Matched</p>
              <div className="mt-2 space-y-2">
                {payerCriteria.map((item) => (
                  <div key={item.criterion} className="rounded-xl border border-gray-200 bg-white px-3 py-2">
                    <p className="text-sm font-medium text-gray-900">{item.criterion}</p>
                    <p className="mt-1 text-sm text-gray-600">{item.evidence}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="rounded-xl border border-dashed border-gray-300 bg-gray-50 p-4">
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <Upload className="h-4 w-4 text-blue-600" />
                <p className="text-sm font-medium text-gray-900">Supporting Documents</p>
              </div>
              <p className="mt-1 text-sm text-gray-500">
                Optional for the demo. Add notes, imaging, labs, or other supporting records for review context.
              </p>
            </div>
            <label className="inline-flex cursor-pointer items-center gap-2 rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50">
              <Upload className="h-4 w-4 text-blue-600" />
              Upload Documents
              <input type="file" multiple className="hidden" onChange={handleDocumentUpload} />
            </label>
          </div>

          {uploadedDocuments.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {uploadedDocuments.map((file) => (
                <span
                  key={file.name}
                  className="inline-flex items-center gap-2 rounded-full border border-gray-200 bg-white px-3 py-1 text-xs text-gray-700"
                >
                  <span>{file.name} - {file.sizeLabel}</span>
                  <button
                    type="button"
                    onClick={() => handleRemoveDocument(file.name)}
                    className="text-gray-400 transition hover:text-red-500"
                    aria-label={`Remove ${file.name}`}
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <DraftField label="Provider Name" value={draft.provider_name} onChange={updateField('provider_name')} />
          <DraftField label="Provider NPI" value={draft.provider_npi} onChange={updateField('provider_npi')} />
          <DraftField label="Provider Phone" value={draft.provider_phone} onChange={updateField('provider_phone')} />
          <DraftField label="Requested Service Date" value={draft.service_date_requested} onChange={updateField('service_date_requested')} />
          <DraftField label="Facility Name" value={draft.facility_name} onChange={updateField('facility_name')} />
          <DraftField label="Submission Method" value={draft.submission_method} onChange={updateField('submission_method')} />
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <DraftField label="Insurance Member ID" value={draft.insurance_id} onChange={updateField('insurance_id')} />
          <DraftField label="Diagnosis Code" value={draft.diagnosis_code} onChange={updateField('diagnosis_code')} />
          <DraftField label="Diagnosis Description" value={draft.diagnosis_description} onChange={updateField('diagnosis_description')} />
          <DraftField label="Procedure Description" value={draft.procedure_description} onChange={updateField('procedure_description')} />
        </div>

        <DraftField label="Clinical Summary" value={draft.clinical_summary} onChange={updateField('clinical_summary')} rows={5} />
        <DraftField label="Justification Letter" value={draft.medical_necessity_letter} onChange={updateField('medical_necessity_letter')} rows={10} />
        <DraftField label="Review Notes" value={draft.review_notes} onChange={updateField('review_notes')} rows={4} />
      </div>

      {submissionOutput && (
        <div className="mt-5 rounded-xl border border-green-100 bg-green-50 p-4">
          <div className="flex items-center gap-2 text-sm font-medium text-green-700">
            <CheckCircle2 className="h-4 w-4" />
            Submission & tracking has started for this case.
          </div>
          <p className="mt-1 text-sm text-green-700">
            The latest tracker output is available in the pipeline view for this review cycle.
          </p>
        </div>
      )}
    </div>
  )
}
