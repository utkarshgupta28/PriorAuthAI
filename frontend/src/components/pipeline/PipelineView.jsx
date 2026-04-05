import React, { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  AlertCircle,
  ArrowLeft,
  Award,
  CheckCircle,
  ChevronDown,
  ChevronRight,
  Clock3,
  DollarSign,
  Loader,
  Play,
  Sparkles,
  TrendingUp,
  XCircle,
} from 'lucide-react'
import {
  getCase,
  getCaseInsights,
  getCaseOutputs,
  runPipeline,
  simulateApproval,
  simulateDenial,
  submitApplication,
} from '../../api'
import CaseInsightsPanel from '../insights/CaseInsightsPanel'
import SubmissionDraftEditor from './SubmissionDraftEditor'

const AGENTS = [
  {
    key: 'policy_engine',
    name: 'Policy Review',
    icon: 'PE',
    description: 'Reviewing payer criteria, prior auth requirements, and documentation rules...',
  },
  {
    key: 'case_intelligence',
    name: 'Clinical Review',
    icon: 'CI',
    description: 'Summarizing medical necessity, clinical support, and approval outlook...',
  },
  {
    key: 'submission_tracker',
    name: 'Submission Tracking',
    icon: 'ST',
    description: 'Starting submission follow-up after physician approval...',
  },
]

const FOLLOW_UP_SCENARIOS = {
  insurance_silent: {
    label: 'Insurance No Reply',
    description: 'The payer stays silent and the system keeps escalating on schedule.',
  },
  doctor_no_action: {
    label: 'Insurance Replied, Doctor No Action',
    description: 'The payer responded, but the doctor has not acted on the requested next step.',
  },
}

function formatAudience(audience) {
  return audience === 'doctor' ? 'Doctor' : 'Insurance'
}

function getFollowUpStatus(day, simulatedDay) {
  if (simulatedDay > day) return 'overdue'
  if (simulatedDay === day) return 'due'
  return 'scheduled'
}

function getFollowUpStatusClasses(status) {
  if (status === 'completed') return 'border-green-200 bg-green-50 text-green-700'
  if (status === 'due') return 'border-yellow-200 bg-yellow-50 text-yellow-800'
  if (status === 'overdue') return 'border-red-200 bg-red-50 text-red-700'
  return 'border-gray-200 bg-white text-gray-700'
}

function ActionResultCard({ actionResult }) {
  if (!actionResult) return null

  if (actionResult.type === 'approval') {
    return (
      <div className="rounded-xl border border-green-100 bg-green-50 p-4 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <Award className="w-5 h-5 text-green-600" />
          <span className="text-green-600 font-semibold">Authorization Approved</span>
          <span className="ml-auto text-green-700 font-mono text-sm">{actionResult.data.auth_number}</span>
        </div>
        <p className="text-gray-600 text-sm">Valid for {actionResult.data.valid_for}</p>
      </div>
    )
  }

  return (
    <div className="rounded-xl border border-red-100 bg-red-50 p-4 shadow-sm">
      <div className="flex items-center gap-2 mb-2">
        <XCircle className="w-5 h-5 text-red-500" />
        <span className="text-red-500 font-semibold">Authorization Denied</span>
      </div>
      <p className="text-gray-700 text-sm mb-3">{actionResult.data.denial_reason}</p>
      {actionResult.data.denial_reasons?.length > 0 && (
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-900">Denial drivers</p>
          <div className="mt-2 space-y-2">
            {actionResult.data.denial_reasons.map((reason) => (
              <p key={reason} className="text-sm text-gray-700">
                {reason}
              </p>
            ))}
          </div>
        </div>
      )}
      {actionResult.data.improvement_suggestions?.length > 0 && (
        <div className="mb-1">
          <p className="text-sm font-medium text-gray-900">How to improve the case</p>
          <div className="mt-2 space-y-2">
            {actionResult.data.improvement_suggestions.map((suggestion) => (
              <p key={suggestion} className="text-sm text-gray-700">
                {suggestion}
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function buildScenarioItem(item, simulatedDay, scenarioMode) {
  const baseStatus = getFollowUpStatus(item.day, simulatedDay)

  if (scenarioMode === 'insurance_silent') {
    return {
      ...item,
      status: baseStatus,
      outcome:
        item.audience === 'insurance' && simulatedDay >= item.day
          ? 'No payer response received yet.'
          : item.audience === 'doctor' && simulatedDay >= item.day
            ? 'Doctor reminder sent while waiting on payer response.'
            : '',
    }
  }

  if (item.audience === 'insurance') {
    if (item.day === 7 && simulatedDay >= 7) {
      return {
        ...item,
        status: 'completed',
        action: 'Payer response received',
        activityLabel: 'Message received from Insurance',
        message:
          'The payer acknowledged the packet and requested physician clarification on medical necessity despite the attached supporting records.',
        outcome: 'Insurance responded and is waiting on doctor action.',
      }
    }

    if (simulatedDay >= item.day) {
      return {
        ...item,
        status: 'scheduled',
        outcome: 'No additional payer outreach needed until the doctor responds.',
      }
    }
  }

  if (item.audience === 'doctor') {
    if (simulatedDay >= item.day) {
      const messageByDay = {
        7: 'Please review the payer request for physician clarification and confirm whether you want to send an addendum.',
        14: 'The payer is still waiting on the physician response. Please approve or update the clarification note.',
        21: 'The case is stalled because the physician response is still pending. Escalation planning is recommended.',
      }
      return {
        ...item,
        status: baseStatus,
        activityLabel: 'Message sent to Doctor',
        message: messageByDay[item.day] || item.message,
        outcome: 'Doctor action still pending.',
      }
    }
  }

  return {
    ...item,
    status: baseStatus,
    activityLabel: item.audience === 'insurance' ? 'Message sent to Insurance' : 'Message sent to Doctor',
    outcome: '',
  }
}

function FollowUpTimeline({ schedule, simulatedDay, scenarioMode, onScenarioChange, onAdvanceWeek, onReset }) {
  if (!schedule?.length) return null
  const scenario = FOLLOW_UP_SCENARIOS[scenarioMode] || FOLLOW_UP_SCENARIOS.insurance_silent
  const sentItems = schedule
    .map((item) => buildScenarioItem(item, simulatedDay, scenarioMode))
    .filter((item) => simulatedDay >= item.day)
    .sort((a, b) => a.day - b.day)

  const [collapsed, setCollapsed] = useState(false)

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <button
            onClick={() => setCollapsed((current) => !current)}
            className="flex items-center gap-2 text-sm font-semibold uppercase tracking-[0.18em] text-gray-500"
          >
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
            Follow-Up Automation
          </button>
          <p className="mt-1 text-sm text-gray-500">
            Simulate weekly outreach to both the insurance company and the doctor.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={onAdvanceWeek}
            className="rounded-xl border border-gray-200 px-3 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
          >
            Advance 7 Days
          </button>
          {simulatedDay > 0 && (
            <button
              onClick={onReset}
              className="rounded-xl border border-gray-200 px-3 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
            >
              Reset Demo
            </button>
          )}
        </div>
      </div>

      {!collapsed && (
        <>
          <div className="mt-3 flex flex-wrap gap-2">
            {Object.entries(FOLLOW_UP_SCENARIOS).map(([key, value]) => (
              <button
                key={key}
                onClick={() => onScenarioChange(key)}
                className={`rounded-xl border px-3 py-2 text-sm font-medium transition ${
                  scenarioMode === key
                    ? 'border-blue-600 bg-blue-50 text-blue-700'
                    : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                }`}
              >
                {value.label}
              </button>
            ))}
          </div>
          <p className="mt-2 text-sm text-gray-500">{scenario.description}</p>
          <p className="mt-3 text-sm text-blue-600">Demo day: {simulatedDay}</p>

          {sentItems.length === 0 ? (
            <div className="mt-4 rounded-xl border border-gray-200 bg-gray-50 p-4 text-sm text-gray-500">
              No follow-up messages have been sent yet. Advance 7 days to trigger the first outreach.
            </div>
          ) : (
            <div className="mt-4 space-y-3">
              {sentItems.map((item, index) => (
                <div
                  key={`${item.day}-${item.audience || 'insurance'}-${item.action}-${index}`}
                  className={`rounded-xl border p-3 ${getFollowUpStatusClasses(item.status === 'scheduled' ? 'completed' : item.status)}`}
                >
                  <div className="flex items-center justify-between gap-3">
                    <p className="text-sm font-medium text-gray-900">
                      Day {item.day}: {item.activityLabel || `Message sent to ${formatAudience(item.audience)}`}
                    </p>
                    <span className="rounded-full border border-current/20 px-2 py-1 text-xs font-medium">
                      Sent
                    </span>
                  </div>
                  <p className="mt-1 text-sm text-gray-600">{item.contact_method}</p>
                  {item.message && (
                    <p className="mt-2 text-sm text-gray-700">{item.message}</p>
                  )}
                  {item.outcome && (
                    <p className="mt-2 text-sm font-medium text-gray-700">{item.outcome}</p>
                  )}
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

function mapAgentKey(agentName) {
  if (agentName === 'Policy Review' || agentName === 'Policy & Requirements Engine') return 'policy_engine'
  if (agentName === 'Clinical Review' || agentName === 'Case Intelligence Engine') return 'case_intelligence'
  if (agentName === 'Submission Tracking' || agentName === 'Submission & Tracker') return 'submission_tracker'
  return null
}

function AgentCard({ agent, status }) {
  const [expanded, setExpanded] = useState(false)
  const s = status || {}
  const parsed = s.output?.parsed_output || {}
  const hasOutput = s.status === 'complete' && Object.keys(parsed).length > 0
  const hasError = parsed?.error || parsed?.parse_error

  const stateIcon =
    s.status === 'complete' ? <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0" /> :
    s.status === 'running' ? <Loader className="w-4 h-4 text-blue-600 animate-spin flex-shrink-0" /> :
    s.status === 'error' ? <XCircle className="w-4 h-4 text-red-500 flex-shrink-0" /> :
    <div className="w-4 h-4 rounded-full border-2 border-gray-300 flex-shrink-0" />

  return (
    <div className="overflow-hidden border-b border-gray-200 last:border-b-0">
      <div
        className={`flex items-center gap-3 px-4 py-4 ${hasOutput ? 'cursor-pointer hover:bg-gray-50' : ''}`}
        onClick={() => hasOutput && setExpanded(!expanded)}
      >
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-50 text-xs font-semibold text-blue-600">
          {agent.icon}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-gray-900 font-medium text-sm">{agent.name}</span>
            {s.status === 'running' && s.elapsed != null && (
              <span className="text-blue-600 text-xs">{s.elapsed}s</span>
            )}
          </div>
          <p className="text-gray-500 text-xs mt-0.5 truncate">
            {s.status === 'running' ? agent.description :
             s.status === 'complete' ? (hasError ? 'Completed with warnings' : 'Analysis complete') :
             s.status === 'error' ? 'Failed' :
             s.status === 'locked' ? 'Waiting for doctor approval and submission' :
             'Waiting...'}
          </p>
        </div>
        {stateIcon}
        {hasOutput && (
          expanded
            ? <ChevronDown className="w-4 h-4 text-gray-400 flex-shrink-0" />
            : <ChevronRight className="w-4 h-4 text-gray-400 flex-shrink-0" />
        )}
      </div>

      {expanded && hasOutput && (
        <div className="border-t border-gray-200 px-4 py-3 bg-gray-50">
          <AgentOutputDisplay agentName={agent.name} parsed={parsed} />
        </div>
      )}
    </div>
  )
}

function AgentOutputDisplay({ agentName, parsed }) {
  if (parsed?.parse_error) {
    return (
      <p className="text-yellow-600 text-xs">
        Raw output - JSON parsing failed. Check terminal for details.
      </p>
    )
  }

  if (agentName === 'Policy Review' || agentName === 'Policy & Requirements Engine') {
    return (
      <div className="space-y-3">
        <div className="flex items-center gap-4 text-xs">
          <span className="text-gray-500">
            Prior Auth Required:{' '}
            <span className={parsed.requires_prior_auth ? 'text-yellow-600 font-medium' : 'text-green-600 font-medium'}>
              {parsed.requires_prior_auth ? 'YES' : 'NO'}
            </span>
          </span>
          <span className="text-gray-500">
            Decision Time: <span className="text-gray-900">{parsed.standard_decision_timeframe}</span>
          </span>
          <span className="text-gray-500">
            Approval Likelihood:{' '}
            <span className={
              parsed.approval_likelihood === 'High' ? 'text-green-600 font-medium' :
              parsed.approval_likelihood === 'Medium' ? 'text-yellow-600 font-medium' :
              'text-red-500 font-medium'
            }>
              {parsed.approval_likelihood === 'Medium' ? 'Moderate Approval Likelihood' : parsed.approval_likelihood}
            </span>
          </span>
        </div>
      </div>
    )
  }

  if (agentName === 'Clinical Review' || agentName === 'Case Intelligence Engine') {
    return (
      <div className="space-y-3">
        {parsed.evidence_summary && (
          <p className="text-gray-700 text-xs leading-relaxed">{parsed.evidence_summary}</p>
        )}
        {parsed.medical_necessity_letter && (
          <details className="text-xs">
            <summary className="text-blue-600 cursor-pointer hover:text-blue-700">
              View medical necessity letter
            </summary>
            <pre className="mt-2 text-gray-700 whitespace-pre-wrap font-sans leading-relaxed bg-white p-3 rounded-xl text-xs max-h-60 overflow-y-auto border border-gray-200">
              {parsed.medical_necessity_letter}
            </pre>
          </details>
        )}
      </div>
    )
  }

  if (agentName === 'Submission Tracking' || agentName === 'Submission & Tracker') {
    const pct = parsed.completion_percentage ?? 0
    const followUpSchedule = parsed.follow_up_schedule || []
    return (
      <div className="space-y-3">
        <div className="flex items-center gap-4 text-xs">
          <span className="text-gray-500">
            Form Completion:{' '}
            <span className={`font-medium ${pct >= 80 ? 'text-green-600' : pct >= 50 ? 'text-yellow-600' : 'text-red-500'}`}>
              {pct}%
            </span>
          </span>
          <span className="text-gray-500">
            Ready to Submit:{' '}
            <span className={parsed.ready_to_submit ? 'text-green-600 font-medium' : 'text-yellow-600 font-medium'}>
              {parsed.ready_to_submit ? 'YES' : 'NO'}
            </span>
          </span>
        </div>
        {followUpSchedule.length > 0 && (
          <div className="rounded-xl border border-gray-200 bg-white p-3">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-gray-500">
              Automated Follow-Up
            </p>
            <div className="mt-2 space-y-2">
              {followUpSchedule.map((item) => (
                <div key={`${item.day}-${item.action}`} className="text-xs text-gray-600">
                  <span className="font-medium text-gray-900">Day {item.day}:</span> {item.action}
                  {item.contact_method ? ` for ${formatAudience(item.audience)} via ${item.contact_method}` : ''}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  return null
}

function MetricTile({ icon, label, value, sub, valueClass }) {
  return (
    <div className="bg-white rounded-xl p-4 border border-gray-200 flex flex-col gap-1 shadow-sm">
      <div className="flex items-center gap-2 text-gray-500 text-xs">{icon}{label}</div>
      <div className={`text-xl font-semibold ${valueClass || 'text-gray-900'}`}>{value}</div>
      {sub && <div className="text-gray-400 text-xs">{sub}</div>}
    </div>
  )
}

function ModeBadge({ mode }) {
  const isFallback = mode === 'fallback'
  return (
    <div className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium ${
      isFallback
        ? 'border-yellow-100 bg-yellow-50 text-yellow-700'
        : 'border-green-100 bg-green-50 text-green-700'
    }`}>
      <span className={`h-2 w-2 rounded-full ${isFallback ? 'bg-yellow-500' : 'bg-green-600'}`} />
      {isFallback ? 'Fallback Mode (Offline Intelligence)' : 'AI Mode'}
    </div>
  )
}

function buildOutputs(outputs) {
  return (outputs || []).map((output) => ({
    agent_key: output.agent_key || mapAgentKey(output.agent_name),
    agent_name: output.agent_name,
    parsed_output: output.parsed_output || output.output_data?.parsed || {},
    raw_output: output.raw_output || output.output_data?.raw || '',
  })).filter((output) => output.agent_key)
}

function buildAgentStatuses(outputs, caseStatus) {
  const statuses = {}
  AGENTS.forEach((agent) => {
    const matchingOutput = outputs.find((output) => output.agent_key === agent.key)
    if (matchingOutput) {
      statuses[agent.key] = {
        status: matchingOutput.parsed_output?.error ? 'error' : 'complete',
        elapsed: null,
        output: matchingOutput,
      }
      return
    }
    if (agent.key === 'submission_tracker' && caseStatus === 'analyzed') {
      statuses[agent.key] = { status: 'locked', elapsed: null, output: null }
      return
    }
    statuses[agent.key] = { status: 'pending', elapsed: null, output: null }
  })
  return statuses
}

function buildLiveInsights(intelligenceOutput, persistedInsights) {
  const parsed = intelligenceOutput?.parsed_output
  if (parsed && Object.keys(parsed).length > 0) {
    return {
      approval_probability: parsed.approval_probability ?? persistedInsights?.approval_probability ?? 50,
      risk_flags: parsed.risk_flags || persistedInsights?.risk_flags || [],
      suggestions: parsed.suggestions || persistedInsights?.suggestions || [],
      strength_score: parsed.strength_score ?? persistedInsights?.strength_score ?? 5,
      evidence_summary: parsed.evidence_summary || persistedInsights?.evidence_summary || '',
      approval_reasoning: parsed.approval_likelihood_reasoning || persistedInsights?.approval_reasoning || '',
      failed_treatments_documented: parsed.failed_treatments_documented || [],
      guidelines_cited: parsed.guidelines_cited || [],
    }
  }
  return persistedInsights
}

export default function PipelineView() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [caseData, setCaseData] = useState(null)
  const [providerContext, setProviderContext] = useState(null)
  const [existingOutputs, setExistingOutputs] = useState([])
  const [runResult, setRunResult] = useState(null)
  const [agentStatuses, setAgentStatuses] = useState({})
  const [running, setRunning] = useState(false)
  const [submittingApplication, setSubmittingApplication] = useState(false)
  const [error, setError] = useState(null)
  const [actionResult, setActionResult] = useState(null)
  const [insights, setInsights] = useState(null)
  const [mode, setMode] = useState('ai')
  const [simulatedDay, setSimulatedDay] = useState(0)
  const [followUpScenarioMode, setFollowUpScenarioMode] = useState('insurance_silent')
  const [uploadedDocuments, setUploadedDocuments] = useState([])
  const pollRef = useRef(null)
  const elapsedRef = useRef(null)

  useEffect(() => {
    getCase(id).then((res) => {
      const outputs = buildOutputs(res.data.agent_outputs || [])
      setCaseData(res.data.case)
      setProviderContext(res.data.provider_context || null)
      setExistingOutputs(outputs)
      setAgentStatuses(buildAgentStatuses(outputs, res.data.case?.status))
    }).catch((e) => {
      setError(e.response?.data?.detail || 'Failed to load case')
    })

    getCaseInsights(id).then((res) => setInsights(res.data)).catch(() => {})

    return () => {
      if (pollRef.current) clearInterval(pollRef.current)
      if (elapsedRef.current) clearInterval(elapsedRef.current)
    }
  }, [id])

  const clearTimers = () => {
    if (pollRef.current) clearInterval(pollRef.current)
    if (elapsedRef.current) clearInterval(elapsedRef.current)
  }

  const startPipeline = async () => {
    setRunning(true)
    setError(null)
    setRunResult(null)
    setActionResult(null)
    setInsights(null)
    setMode('ai')
    setSimulatedDay(0)
    setFollowUpScenarioMode('insurance_silent')
    setAgentStatuses({
      policy_engine: { status: 'running', elapsed: 0, output: null },
      case_intelligence: { status: 'pending', elapsed: null, output: null },
      submission_tracker: { status: 'locked', elapsed: null, output: null },
    })

    elapsedRef.current = setInterval(() => {
      setAgentStatuses((prev) => {
        const updated = { ...prev }
        for (const key of Object.keys(updated)) {
          if (updated[key]?.status === 'running') {
            updated[key] = { ...updated[key], elapsed: (updated[key].elapsed || 0) + 1 }
          }
        }
        return updated
      })
    }, 1000)

    let knownCount = 0
    pollRef.current = setInterval(async () => {
      try {
        const res = await getCaseOutputs(id)
        const outputs = buildOutputs(res.data || [])
        const reviewOutputs = outputs.filter((output) => output.agent_key !== 'submission_tracker')
        if (reviewOutputs.length > knownCount) {
          knownCount = reviewOutputs.length
          setAgentStatuses((prev) => {
            const next = { ...prev }
            reviewOutputs.forEach((output) => {
              next[output.agent_key] = {
                status: output.parsed_output?.error ? 'error' : 'complete',
                elapsed: null,
                output,
              }
            })
            if (reviewOutputs.length === 1) {
              next.case_intelligence = { status: 'running', elapsed: 0, output: null }
            }
            if (reviewOutputs.length >= 2) {
              next.submission_tracker = { status: 'locked', elapsed: null, output: null }
            }
            return next
          })
        }
      } catch (_) {}
    }, 3000)

    try {
      const res = await runPipeline(id, false, '')
      const result = res.data
      clearTimers()

      const outputs = buildOutputs(result.task_outputs || [])
      setMode(result.mode || (result.fallback_mode ? 'fallback' : 'ai'))
      setRunResult({ ...result, task_outputs: outputs })
      setExistingOutputs(outputs)
      setAgentStatuses(buildAgentStatuses(outputs, result.new_status))
      setCaseData((current) => current ? { ...current, status: result.new_status } : current)

      try {
        const insightsRes = await getCaseInsights(id)
        setInsights(insightsRes.data)
      } catch (_) {}
    } catch (e) {
      clearTimers()
      setError(e.response?.data?.detail || e.message || 'Pipeline failed')
      setAgentStatuses((prev) => ({
        ...prev,
        policy_engine: { ...prev.policy_engine, status: 'error', elapsed: null },
        case_intelligence: { ...prev.case_intelligence, status: prev.case_intelligence?.status === 'complete' ? 'complete' : 'error', elapsed: null },
      }))
    } finally {
      setRunning(false)
    }
  }

  const handleSubmitApplication = async (draft) => {
    setSubmittingApplication(true)
    setError(null)
    setActionResult(null)
    setSimulatedDay(0)
    setFollowUpScenarioMode('insurance_silent')
    setAgentStatuses((prev) => ({
      ...prev,
      submission_tracker: { status: 'running', elapsed: 0, output: null },
    }))

    elapsedRef.current = setInterval(() => {
      setAgentStatuses((prev) => ({
        ...prev,
        submission_tracker: prev.submission_tracker?.status === 'running'
          ? { ...prev.submission_tracker, elapsed: (prev.submission_tracker.elapsed || 0) + 1 }
          : prev.submission_tracker,
      }))
    }, 1000)

    pollRef.current = setInterval(async () => {
      try {
        const res = await getCaseOutputs(id)
        const outputs = buildOutputs(res.data || [])
        const trackerOutput = outputs.find((output) => output.agent_key === 'submission_tracker')
        if (trackerOutput) {
          setAgentStatuses((prev) => ({
            ...prev,
            submission_tracker: {
              status: trackerOutput.parsed_output?.error ? 'error' : 'complete',
              elapsed: null,
              output: trackerOutput,
            },
          }))
        }
      } catch (_) {}
    }, 3000)

    try {
      const res = await submitApplication(id, draft)
      const result = res.data
      clearTimers()

      const outputs = buildOutputs(result.task_outputs || [])
      setMode(result.mode || (result.fallback_mode ? 'fallback' : 'ai'))
      setRunResult({ ...result, task_outputs: outputs })
      setExistingOutputs(outputs)
      setAgentStatuses(buildAgentStatuses(outputs, result.new_status))
      setCaseData((current) => current ? { ...current, status: result.new_status } : current)
    } catch (e) {
      clearTimers()
      setAgentStatuses((prev) => ({
        ...prev,
        submission_tracker: { ...prev.submission_tracker, status: 'error', elapsed: null },
      }))
      setError(e.response?.data?.detail || e.message || 'Submission failed')
    } finally {
      setSubmittingApplication(false)
    }
  }

  const handleDeny = async () => {
    try {
      const res = await simulateDenial(id)
      setActionResult({ type: 'denial', data: res.data })
    } catch (_) {
      setError('Failed to simulate denial')
    }
  }

  const handleApprove = async () => {
    try {
      const res = await simulateApproval(id)
      setActionResult({ type: 'approval', data: res.data })
    } catch (_) {
      setError('Failed to simulate approval')
    }
  }

  const taskOutputs = runResult?.task_outputs?.length ? runResult.task_outputs : existingOutputs
  const approvalLikelihood = taskOutputs
    .find((output) => output.agent_key === 'policy_engine')
    ?.parsed_output?.approval_likelihood?.toUpperCase()
  const policyOutput = taskOutputs.find((output) => output.agent_key === 'policy_engine')
  const caseIntelligenceOutput = taskOutputs.find((output) => output.agent_key === 'case_intelligence')
  const submissionTrackerOutput = taskOutputs.find((output) => output.agent_key === 'submission_tracker')
  const liveInsights = buildLiveInsights(caseIntelligenceOutput, insights)
  const evidenceContext = {
    clinicalNotes: caseData?.clinical_notes || '',
    labResults: caseData?.lab_results || '',
    policyCriteria: policyOutput?.parsed_output?.criteria_analysis || [],
  }
  const followUpSchedule =
    submissionTrackerOutput?.parsed_output?.follow_up_schedule ||
    actionResult?.data?.follow_up_schedule ||
    []

  const formatTime = (seconds) => {
    if (seconds == null) return '-'
    return seconds < 60 ? `${seconds}s` : `${Math.floor(seconds / 60)}m ${seconds % 60}s`
  }

  if (error && !caseData) {
    return (
      <div className="flex min-h-screen items-center justify-center px-4">
        <div className="w-full max-w-md rounded-xl border border-red-200 bg-white p-6 text-center shadow-sm">
          <AlertCircle className="mx-auto mb-3 h-8 w-8 text-red-500" />
          <p className="text-sm text-red-600">{error}</p>
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

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-start gap-3">
          <button
            onClick={() => navigate(`/cases/${id}`)}
            className="text-gray-500 hover:text-gray-900 transition-colors mt-1"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">3-Agent Pipeline</h1>
            {caseData && (
              <p className="text-gray-500 text-sm mt-0.5">
                {caseData.patient_name}
                {caseData.diagnosis_code && <span className="text-blue-600 ml-2">{caseData.diagnosis_code}</span>}
                <span className="text-gray-400 ml-2">CPT {caseData.treatment_cpt_code}</span>
              </p>
            )}
          </div>
        </div>
        <ModeBadge mode={mode} />
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-4 mb-6 shadow-sm">
        <div className="flex items-center justify-between gap-4 flex-wrap">
          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-sm font-semibold uppercase tracking-[0.18em] text-gray-500">
                Review Workflow
              </span>
              <span className="rounded-full border border-blue-100 bg-blue-50 px-2.5 py-1 text-xs font-medium text-blue-700">
                Policy Review + Clinical Review
              </span>
            </div>
            <p className="text-gray-500 text-sm mt-2">
              Submission tracking begins after physician approval.
            </p>
          </div>
          <button
            onClick={startPipeline}
            disabled={running || submittingApplication}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed text-white px-5 py-2 rounded-xl font-medium text-sm transition-colors shadow-sm"
          >
            {running ? <><Loader className="w-4 h-4 animate-spin" /> Running...</> : <><Play className="w-4 h-4" /> Run Clinical Review</>}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded-xl p-3 flex items-center gap-2 text-red-600 text-sm">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          {error}
        </div>
      )}

      {followUpSchedule.length > 0 && (
        <div className="mb-6">
          <FollowUpTimeline
            schedule={followUpSchedule}
            simulatedDay={simulatedDay}
            scenarioMode={followUpScenarioMode}
            onScenarioChange={setFollowUpScenarioMode}
            onAdvanceWeek={() => setSimulatedDay((current) => current + 7)}
            onReset={() => setSimulatedDay(0)}
          />
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <div className="space-y-6">
          <div className="rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden">
            <div className="flex items-center justify-between border-b border-gray-200 px-4 py-3">
              <div>
                <h2 className="text-sm font-semibold uppercase tracking-[0.18em] text-gray-500">
                  Pipeline Progress
                </h2>
                <p className="mt-1 text-sm text-gray-500">
                  Review the case, confirm physician approval, then start submission follow-up.
                </p>
              </div>
            </div>
            <div>
              {AGENTS.map((agent) => (
                <AgentCard key={agent.key} agent={agent} status={agentStatuses[agent.key]} />
              ))}
            </div>
          </div>

          {liveInsights ? (
            <CaseInsightsPanel
              insights={liveInsights}
              evidenceContext={evidenceContext}
              documentCount={uploadedDocuments.length}
            />
          ) : (
            <div className="rounded-xl border border-gray-200 bg-white p-5 text-sm text-gray-500 shadow-sm">
              Run the clinical review to generate approval probability, risks, and improvement guidance.
            </div>
          )}

          <div className="rounded-xl border border-gray-200 bg-white p-4 text-sm text-gray-600 shadow-sm">
            Physician approval is required before submission tracking can begin.
          </div>
        </div>

        <div className="lg:col-span-2 space-y-6">
          {actionResult && (
            <ActionResultCard actionResult={actionResult} />
          )}

          {caseIntelligenceOutput ? (
            <SubmissionDraftEditor
              caseId={id}
              caseData={caseData}
              providerContext={providerContext}
              policyOutput={policyOutput}
              submissionOutput={submissionTrackerOutput}
              intelligenceOutput={caseIntelligenceOutput}
              insights={liveInsights}
              onDocumentsChange={setUploadedDocuments}
              onSubmit={handleSubmitApplication}
              submitting={submittingApplication}
              submitLocked={running || caseData?.status === 'submitted'}
            />
          ) : (
            <div className="rounded-xl border border-gray-200 bg-white p-8 shadow-sm">
              <h2 className="text-sm font-semibold uppercase tracking-[0.18em] text-gray-500">Application Review</h2>
              <p className="mt-3 text-sm text-gray-500">
                Run the review to generate the justification letter and open the editable application package.
              </p>
            </div>
          )}

          {(runResult || existingOutputs.length > 0) && (
            <>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <MetricTile icon={<Clock3 className="w-3.5 h-3.5" />} label="AI Time" value={formatTime(runResult?.elapsed_seconds)} sub="Current stage runtime" />
                <MetricTile icon={<Sparkles className="w-3.5 h-3.5" />} label="Time Saved" value={runResult?.time_saved_percent != null ? `${runResult.time_saved_percent}%` : '-'} sub="vs manual process" valueClass="text-green-600" />
                <MetricTile icon={<DollarSign className="w-3.5 h-3.5" />} label="AI Cost" value={`~$${runResult?.estimated_cost_ai ?? '-'}`} sub="Estimated stage cost" />
                <MetricTile
                  icon={<TrendingUp className="w-3.5 h-3.5" />}
                  label="Approval Likelihood"
                  value={approvalLikelihood === 'MEDIUM' ? 'Moderate Approval Likelihood' : (approvalLikelihood || '-')}
                  valueClass={approvalLikelihood === 'HIGH' ? 'text-green-600' : approvalLikelihood === 'MEDIUM' ? 'text-yellow-600' : 'text-red-500'}
                  sub="Policy Engine estimate"
                />
              </div>

              {!actionResult && (
                <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm">
                  <p className="text-gray-900 text-sm mb-3 font-medium">Actions</p>
                  <div className="flex gap-3 flex-wrap">
                    <button onClick={handleApprove} className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl text-sm font-medium transition-colors">
                      <Award className="w-4 h-4" /> Simulate Approval
                    </button>
                    <button onClick={handleDeny} className="flex items-center gap-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-xl text-sm font-medium transition-colors">
                      <XCircle className="w-4 h-4" /> Simulate Denial
                    </button>
                  </div>
                </div>
              )}

            </>
          )}
        </div>
      </div>
    </div>
  )
}
