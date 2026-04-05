import React, { useState } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'

const AGENT_ICONS = {
  'Policy & Requirements Engine': 'PE',
  'Case Intelligence Engine': 'CI',
  'Submission & Tracker': 'ST',
  'Policy Analyst': 'PE',
  'Medical Necessity Specialist': 'MN',
  'Form Completion Specialist': 'FC',
  'Fraud & Compliance Auditor': 'FA',
  'Appeals & Tracking Specialist': 'AT',
}

function renderValue(val, depth = 0) {
  if (val === null || val === undefined) return <span className="text-gray-400">-</span>
  if (typeof val === 'boolean') return <span className={val ? 'text-green-600' : 'text-red-500'}>{val ? 'Yes' : 'No'}</span>
  if (typeof val === 'number') return <span className="text-blue-600">{val}</span>
  if (typeof val === 'string') {
    if (val.length > 200) {
      return (
        <details className="inline">
          <summary className="cursor-pointer text-gray-500 hover:text-gray-900 text-xs">
            {val.slice(0, 80)}... [expand]
          </summary>
          <pre className="whitespace-pre-wrap text-gray-700 mt-1">{val}</pre>
        </details>
      )
    }
    return <span className="text-gray-700">{val}</span>
  }
  if (Array.isArray(val)) {
    if (val.length === 0) return <span className="text-gray-400">[]</span>
    return (
      <ul className="space-y-1 mt-1">
        {val.map((item, i) => (
          <li key={i} className="flex gap-2">
            <span className="text-gray-300 text-xs mt-0.5">•</span>
            <div>{renderValue(item, depth + 1)}</div>
          </li>
        ))}
      </ul>
    )
  }
  if (typeof val === 'object') {
    return (
      <div className={depth > 0 ? 'pl-3 border-l border-gray-200 mt-1' : 'mt-1'}>
        {Object.entries(val).map(([k, v]) => (
          <div key={k} className="mb-1">
            <span className="text-gray-500 text-xs font-medium capitalize">
              {k.replace(/_/g, ' ')}:{' '}
            </span>
            {renderValue(v, depth + 1)}
          </div>
        ))}
      </div>
    )
  }
  return <span className="text-gray-700">{String(val)}</span>
}

export default function PipelineStepOutput({ agentName, outputData, isExpanded: defaultExpanded = false }) {
  const [expanded, setExpanded] = useState(defaultExpanded)

  const icon = AGENT_ICONS[agentName] || 'AI'
  const parsed = outputData?.parsed || outputData || {}
  const hasParseError = parsed?.parse_error

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-50 text-xs font-semibold text-blue-600">
            {icon}
          </div>
          <div className="text-left">
            <div className="text-gray-900 font-medium text-sm">{agentName}</div>
            {!expanded && (
              <div className="text-gray-500 text-xs">
                {hasParseError ? 'Raw output available' : `${Object.keys(parsed).length} fields`}
              </div>
            )}
          </div>
        </div>
        {expanded ? (
          <ChevronDown className="w-4 h-4 text-gray-400" />
        ) : (
          <ChevronRight className="w-4 h-4 text-gray-400" />
        )}
      </button>

      {expanded && (
        <div className="px-4 pb-4 border-t border-gray-200 pt-3">
          {hasParseError ? (
            <div>
              <p className="text-yellow-600 text-xs mb-2">Raw output (JSON parsing failed):</p>
              <pre className="text-gray-700 text-xs whitespace-pre-wrap font-mono bg-gray-50 p-3 rounded-xl overflow-x-auto max-h-96 border border-gray-200">
                {outputData?.raw || String(outputData)}
              </pre>
            </div>
          ) : (
            <div className="text-sm space-y-2">
              {renderValue(parsed)}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
