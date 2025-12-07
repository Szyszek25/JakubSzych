import { Deadline } from '../types'
import { format } from 'date-fns'
import pl from 'date-fns/locale/pl'
import { Calendar, AlertTriangle } from 'lucide-react'
import './DeadlinesPanel.css'

interface DeadlinesPanelProps {
  deadlines: {
    upcoming: Deadline[]
    critical: Deadline[]
  }
}

export default function DeadlinesPanel({ deadlines }: DeadlinesPanelProps) {
  const critical = deadlines.critical.slice(0, 5)
  const upcoming = deadlines.upcoming.slice(0, 5)

  return (
    <div className="deadlines-panel">
      <h3>Zbliżające się terminy</h3>
      
      {critical.length > 0 && (
        <div className="deadlines-section">
          <div className="section-header critical">
            <AlertTriangle size={16} />
            <span>Krytyczne ({critical.length})</span>
          </div>
          <div className="deadlines-list">
            {critical.map((deadline) => (
              <div key={deadline.case_id} className="deadline-item critical">
                <div className="deadline-case">{deadline.case_id}</div>
                <div className="deadline-date">
                  {format(new Date(deadline.deadline), 'dd MMM yyyy', { locale: pl })}
                </div>
                <div className="deadline-days">{deadline.days_left} dni</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {upcoming.length > 0 && (
        <div className="deadlines-section">
          <div className="section-header">
            <Calendar size={16} />
            <span>Nadchodzące ({upcoming.length})</span>
          </div>
          <div className="deadlines-list">
            {upcoming.map((deadline) => (
              <div key={deadline.case_id} className="deadline-item">
                <div className="deadline-case">{deadline.case_id}</div>
                <div className="deadline-date">
                  {format(new Date(deadline.deadline), 'dd MMM yyyy', { locale: pl })}
                </div>
                <div className="deadline-days">{deadline.days_left} dni</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {critical.length === 0 && upcoming.length === 0 && (
        <p className="empty-deadlines">Brak zbliżających się terminów</p>
      )}
    </div>
  )
}

