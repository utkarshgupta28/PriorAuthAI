import React, { useState } from 'react'
import { TrendingUp, AlertTriangle, Lightbulb, CheckCircle, ShieldCheck, ChevronDown, ChevronRight, FileText } from 'lucide-react'

function ApprovalBar({ probability }) {
  const pct = Math.max(0, Math.min(100, probability ?? 50))
  const color = pct >= 75 ? 'bg-green-600' : pct >= 50 ? 'bg-yellow-500' : 'bg-red-500'
  const textColor = pct >= 75 ? 'text-green-600' : pct >= 50 ? 'text-yellow-500' : 'text-red-500'
  const label = pct >= 75
    ? 'High Approval Likelihood'
    : pct >= 50
      ? 'Moderate Approval Likelihood'
      : 'Low Approval Likelihood'

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <span className="text-gray-900 text-sm font-medium">Approval Probability</span>
        <div className="flex items-center gap-2">
          <span className={`text-2xl font-bold ${textColor}`}>{pct}%</span>
          <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${
            pct >= 75
              ? 'bg-green-50 text-green-600 border-green-100'
              : pct >= 50
                ? 'bg-yellow-50 text-yellow-600 border-yellow-100'
                : 'bg-red-50 text-red-500 border-red-100'
          }`}>
            {label}
          </span>
        </div>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
        <div className={`h-3 rounded-full transition-all duration-700 ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

function StrengthScore({ score }) {
  const s = Math.max(1, Math.min(10, score ?? 5))
  const dots = Array.from({ length: 10 }, (_, i) => i < s)
  const color = s >= 7 ? 'bg-green-600' : s >= 5 ? 'bg-yellow-500' : 'bg-red-500'

  return (
    <div className="flex items-center gap-3">
      <span className="text-gray-500 text-xs">Case Strength</span>
      <div className="flex gap-1">
        {dots.map((filled, i) => (
          <div key={i} className={`w-2.5 h-2.5 rounded-full ${filled ? color : 'bg-gray-200'}`} />
        ))}
      </div>
      <span className="text-gray-700 text-xs font-medium">Case Strength: {s}/10</span>
    </div>
  )
}

function normalizeInsightLabel(label) {
  const text = String(label || '').trim()
  if (!text) return ''
  const lower = text.toLowerCase()
  if (
    lower.includes('documentation') ||
    lower.includes('document') ||
    lower.includes('chart note') ||
    lower.includes('attached')
  ) {
    return ''
  }
  return text
}

function canonicalizeLabel(label) {
  return String(label || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
}

function dedupeSuggestions(riskFlags, suggestions) {
  const riskKeys = new Set(
    riskFlags
      .map(normalizeInsightLabel)
      .filter(Boolean)
      .map(canonicalizeLabel),
  )

  return suggestions.filter((suggestion) => {
    const normalized = normalizeInsightLabel(suggestion)
    if (!normalized) return false
    return !riskKeys.has(canonicalizeLabel(normalized))
  })
}

function distributeDelta(totalDelta, count) {
  if (!count) return []
  const base = Math.trunc(totalDelta / count)
  let remainder = totalDelta - base * count
  return Array.from({ length: count }, () => {
    if (remainder === 0) return base
    const adjustment = remainder > 0 ? 1 : -1
    remainder -= adjustment
    return base + adjustment
  })
}

function buildScoreBreakdown(probability, score, riskFlags, suggestions) {
  const pct = Math.max(0, Math.min(100, probability ?? 50))
  const totalDelta = pct - 50
  const positiveCandidates = []
  const negativeCandidates = []

  if ((score ?? 0) >= 7) positiveCandidates.push('Strong clinical profile')
  if (pct >= 65) positiveCandidates.push('Clinical evidence supports approval')
  if (pct >= 60) positiveCandidates.push('Treatment history supports medical necessity')

  riskFlags
    .map(normalizeInsightLabel)
    .filter(Boolean)
    .forEach((label) => {
      if (!negativeCandidates.includes(label)) negativeCandidates.push(label)
    })

  suggestions
    .map(normalizeInsightLabel)
    .filter(Boolean)
    .forEach((label) => {
      if (!negativeCandidates.includes(label)) negativeCandidates.push(label)
    })

  const selectedLabels = totalDelta >= 0
    ? positiveCandidates.slice(0, 3)
    : negativeCandidates.slice(0, 3)

  if (selectedLabels.length === 0) {
    selectedLabels.push(totalDelta >= 0 ? 'Overall case profile' : 'Clinical review risk remains')
  }

  const deltas = distributeDelta(totalDelta, selectedLabels.length)
  return selectedLabels.map((label, index) => ({
    label,
    delta: deltas[index],
  }))
}

function buildStrengthJustification(score, riskFlags, suggestions) {
  const s = score ?? 5
  const riskDriver = riskFlags.find(Boolean)
  const suggestionDriver = suggestions.find(Boolean)

  if (s >= 9) {
    return 'Case strength is very high because the record is well-supported across severity, prior treatment history, and payer-facing clinical evidence.'
  }
  if (s >= 7) {
    return 'Case strength is strong because the record shows good clinical support, with only limited remaining review risk.'
  }
  if (s >= 5) {
    if (riskDriver) {
      return `Case strength is moderate because the record is partly supportable, but ${riskDriver.charAt(0).toLowerCase()}${riskDriver.slice(1)}`
    }
    if (suggestionDriver) {
      return `Case strength is moderate because the case is supportable, but it would improve if you ${suggestionDriver.charAt(0).toLowerCase()}${suggestionDriver.slice(1)}`
    }
    return 'Case strength is moderate because the case has some support, but the payer rationale is not yet strong enough to be high confidence.'
  }
  if (riskDriver) {
    return `Case strength is low because ${riskDriver.charAt(0).toLowerCase()}${riskDriver.slice(1)}`
  }
  return 'Case strength is low because the submission package still lacks enough high-confidence support for approval.'
}

function truncateSentence(text) {
  const value = String(text || '').trim()
  if (!value) return ''
  return value.length > 180 ? `${value.slice(0, 177).trimEnd()}...` : value
}

function buildEvidenceItems(insights, evidenceContext, documentCount) {
  const items = []
  const failedTreatments = insights?.failed_treatments_documented || []
  const guidelines = insights?.guidelines_cited || []
  const policyCriteria = evidenceContext?.policyCriteria || []

  if (failedTreatments.length > 0) {
    items.push({
      label: 'Prior treatment history',
      value: failedTreatments.slice(0, 3).join('; '),
    })
  }

  if (evidenceContext?.clinicalNotes) {
    items.push({
      label: 'Clinical history',
      value: truncateSentence(evidenceContext.clinicalNotes),
    })
  }

  if (evidenceContext?.labResults) {
    items.push({
      label: 'Objective findings',
      value: truncateSentence(evidenceContext.labResults),
    })
  }

  if (policyCriteria.length > 0) {
    const emphasizedCriteria = policyCriteria
      .filter((item) => item?.criterion && item?.status && item.status !== 'Review Required')
      .slice(0, 2)
      .map((item) => `${item.criterion} (${item.status})`)

    if (emphasizedCriteria.length > 0) {
      items.push({
        label: 'Payer criteria review',
        value: emphasizedCriteria.join('; '),
      })
    }
  }

  if (guidelines.length > 0) {
    items.push({
      label: 'Guideline support',
      value: guidelines
        .slice(0, 3)
        .map((item) => `${item.organization} ${item.year}`)
        .join(', '),
    })
  }

  if (documentCount > 0) {
    items.push({
      label: 'Additional uploaded records',
      value: `${documentCount} supporting document${documentCount === 1 ? '' : 's'} added for review context`,
    })
  }

  return items.slice(0, 5)
}

export default function CaseInsightsPanel({ insights, evidenceContext = null, documentCount = 0 }) {
  if (!insights) return null
  const [showApprovalInfo, setShowApprovalInfo] = useState(false)
  const [showStrengthInfo, setShowStrengthInfo] = useState(false)

  const {
    approval_probability,
    risk_flags = [],
    suggestions = [],
    strength_score,
    evidence_summary,
    approval_reasoning,
    failed_treatments_documented = [],
    guidelines_cited = [],
  } = insights
  const filteredSuggestions = dedupeSuggestions(risk_flags, suggestions)
  const scoreBreakdown = buildScoreBreakdown(
    approval_probability,
    strength_score,
    risk_flags,
    filteredSuggestions,
  )
  const approvalJustification =
    approval_probability >= 70
      ? 'Approval is higher because the documented history and clinical evidence appear to align with payer expectations.'
      : approval_probability >= 50
        ? 'Approval remains moderate because there is meaningful clinical support, but the case still has review risk.'
        : 'Approval is lower because the current record still shows material review risk or payer-evidence gaps.'
  const strengthJustification = buildStrengthJustification(
    strength_score,
    risk_flags,
    filteredSuggestions,
  )
  const evidenceItems = buildEvidenceItems(
    {
      ...insights,
      failed_treatments_documented,
      guidelines_cited,
    },
    evidenceContext,
    documentCount,
  )

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 space-y-5 shadow-sm">
      <div className="flex items-center gap-2">
        <TrendingUp className="w-4 h-4 text-blue-600" />
        <h3 className="text-gray-900 font-semibold text-sm">Case Insights</h3>
        <span className="ml-auto text-xs text-gray-500 bg-gray-50 px-2 py-0.5 rounded-full border border-gray-200">
          Live
        </span>
      </div>

      <div>
        <button
          onClick={() => setShowApprovalInfo((current) => !current)}
          className="w-full text-left"
        >
          <div className="flex items-start gap-2">
            {showApprovalInfo ? (
              <ChevronDown className="mt-1 h-4 w-4 flex-shrink-0 text-gray-400" />
            ) : (
              <ChevronRight className="mt-1 h-4 w-4 flex-shrink-0 text-gray-400" />
            )}
            <div className="flex-1">
              <ApprovalBar probability={approval_probability} />
            </div>
          </div>
        </button>
        {showApprovalInfo && (
          <p className="mt-2 pl-6 text-sm text-gray-700 leading-relaxed">{approvalJustification}</p>
        )}
      </div>

      {strength_score != null && (
        <div>
          <button
            onClick={() => setShowStrengthInfo((current) => !current)}
            className="w-full text-left"
          >
            <div className="flex items-center gap-2">
              {showStrengthInfo ? (
                <ChevronDown className="h-4 w-4 flex-shrink-0 text-gray-400" />
              ) : (
                <ChevronRight className="h-4 w-4 flex-shrink-0 text-gray-400" />
              )}
              <div className="flex-1">
                <StrengthScore score={strength_score} />
              </div>
            </div>
          </button>
          {showStrengthInfo && (
            <p className="mt-2 pl-6 text-sm text-gray-600 leading-relaxed">{strengthJustification}</p>
          )}
        </div>
      )}

      {(approval_reasoning || evidence_summary) && (
        <div className="rounded-xl border border-blue-100 bg-blue-50 p-4">
          <div className="mb-2 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-blue-600" />
            <span className="text-xs font-semibold uppercase tracking-[0.18em] text-gray-500">
              Why This Score
            </span>
          </div>
          {approval_reasoning && (
            <p className="text-sm text-gray-700 leading-relaxed">{approval_reasoning}</p>
          )}
          {evidence_summary && (
            <p className={`text-sm text-gray-700 leading-relaxed ${approval_reasoning ? 'mt-2' : ''}`}>
              {evidence_summary}
            </p>
          )}
        </div>
      )}

      {evidenceItems.length > 0 && (
        <div className="rounded-xl border border-gray-200 bg-white p-4">
          <div className="mb-3 flex items-center gap-2">
            <FileText className="w-4 h-4 text-blue-600" />
            <span className="text-xs font-semibold uppercase tracking-[0.18em] text-gray-500">
              Evidence Used
            </span>
          </div>
          <div className="space-y-3">
            {evidenceItems.map((item) => (
              <div key={item.label}>
                <p className="text-xs font-semibold uppercase tracking-[0.14em] text-gray-500">
                  {item.label}
                </p>
                <p className="mt-1 text-sm leading-relaxed text-gray-700">{item.value}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="rounded-xl border border-gray-200 bg-gray-50 p-4">
        <div className="mb-3 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-blue-600" />
          <span className="text-xs font-semibold uppercase tracking-[0.18em] text-gray-500">
            Score Breakdown
          </span>
        </div>
        <div className="space-y-2">
          {scoreBreakdown.map((item, index) => (
            <div key={`${item.label}-${index}`} className="flex items-center justify-between gap-3 text-sm">
              <span className="text-gray-700">{item.label}</span>
              <span className={item.delta > 0 ? 'text-green-600 font-medium' : 'text-red-500 font-medium'}>
                {item.delta > 0 ? `+${item.delta}%` : `${item.delta}%`}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div>
        <div className="flex items-center gap-1.5 mb-2">
          <AlertTriangle className="w-3.5 h-3.5 text-yellow-500" />
          <span className="text-gray-500 text-xs font-semibold uppercase tracking-[0.18em]">
            Risk Flags ({risk_flags.length})
          </span>
        </div>
        {risk_flags.length === 0 ? (
          <div className="flex items-center gap-2 text-green-600 text-sm">
            <CheckCircle className="w-4 h-4" />
            <span>No risk flags identified</span>
          </div>
        ) : (
          <ul className="space-y-1.5">
            {risk_flags.map((flag, i) => (
              <li key={i} className="flex items-start gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-yellow-500 mt-1.5 flex-shrink-0" />
                <span className="text-gray-700 text-sm leading-relaxed">{flag}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {filteredSuggestions.length > 0 && (
        <div>
          <div className="flex items-center gap-1.5 mb-2">
            <Lightbulb className="w-3.5 h-3.5 text-blue-600" />
            <span className="text-gray-500 text-xs font-semibold uppercase tracking-[0.18em]">
              Improvement Suggestions
            </span>
          </div>
          <ul className="space-y-1.5">
            {filteredSuggestions.map((suggestion, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-blue-600 text-xs font-bold mt-0.5 flex-shrink-0">{i + 1}.</span>
                <span className="text-gray-700 text-sm leading-relaxed">{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="rounded-xl border border-yellow-100 bg-yellow-50 px-3 py-2 text-sm text-yellow-700">
        Doctor review required before submission.
      </div>
    </div>
  )
}
