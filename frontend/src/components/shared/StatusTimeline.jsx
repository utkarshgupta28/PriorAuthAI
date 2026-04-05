import React from 'react'

const STEPS = [
  { key: 'intake', label: 'Intake' },
  { key: 'processing', label: 'Processing' },
  { key: 'analyzed', label: 'Analyzed' },
  { key: 'submitted', label: 'Submitted' },
  { key: 'approved', label: 'Approved' },
  { key: 'denied', label: 'Denied' },
]

const STATUS_ORDER = {
  intake: 0,
  processing: 1,
  analyzed: 2,
  error: 2,
  submitted: 3,
  approved: 4,
  denied: 4,
}

export default function StatusTimeline({ currentStatus }) {
  const currentIndex = STATUS_ORDER[currentStatus] ?? 0
  const isDenied = currentStatus === 'denied'

  return (
    <div className="flex items-center gap-0 overflow-x-auto py-2">
      {STEPS.map((step, i) => {
        const stepIndex = STATUS_ORDER[step.key] ?? i
        const isDone = stepIndex < currentIndex
        const isCurrent =
          step.key === currentStatus ||
          (step.key === 'analyzed' && currentStatus === 'error') ||
          (step.key === 'denied' && isDenied)

        let dotClass = 'w-4 h-4 rounded-full border-2 flex-shrink-0 '
        let labelClass = 'text-xs mt-1 text-center whitespace-nowrap '

        if (step.key === 'denied' && isDenied) {
          dotClass += 'bg-red-500 border-red-500'
          labelClass += 'text-red-500 font-medium'
        } else if (isCurrent) {
          dotClass += 'bg-blue-600 border-blue-600 animate-pulse'
          labelClass += 'text-blue-600 font-medium'
        } else if (isDone) {
          dotClass += 'bg-green-600 border-green-600'
          labelClass += 'text-green-600'
        } else {
          dotClass += 'border-gray-300 bg-white'
          labelClass += 'text-gray-400'
        }

        if (step.key === 'denied' && !isDenied) return null
        if (step.key === 'approved' && isDenied) return null

        return (
          <React.Fragment key={step.key}>
            {i > 0 && step.key !== 'denied' && (
              <div
                className={`h-px flex-1 min-w-[20px] ${
                  stepIndex <= currentIndex && !isDenied ? 'bg-green-600' : 'bg-gray-200'
                }`}
              />
            )}
            <div className="flex flex-col items-center">
              <div className={dotClass} />
              <span className={labelClass}>{step.label}</span>
            </div>
          </React.Fragment>
        )
      })}
    </div>
  )
}
