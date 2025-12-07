import { AlertTriangle, FileText, Clock } from 'lucide-react'
import { Deadline } from '../types'
import { format } from 'date-fns'
import pl from 'date-fns/locale/pl'
import './CriticalAlert.css'

interface CriticalAlertProps {
  criticalDeadlines: Deadline[]
  onAction: (caseId: string) => void
}

export default function CriticalAlert({ criticalDeadlines, onAction }: CriticalAlertProps) {
  if (criticalDeadlines.length === 0) {
    return null
  }

  const mostCritical = criticalDeadlines[0]

  return (
    <div className="critical-alert">
      <div className="alert-header">
        <AlertTriangle size={24} className="alert-icon" />
        <div className="alert-title">
          <h2>⚠️ KRYTYCZNY TERMIN</h2>
          <p>Ta sprawa za {mostCritical.days_left} dni złamie KPA</p>
        </div>
      </div>
      
      <div className="alert-content">
        <div className="alert-case">
          <FileText size={20} />
          <div>
            <strong>{mostCritical.case_id}</strong>
            <span className="case-type">{mostCritical.case_type.replace('_', ' ')}</span>
          </div>
        </div>
        
        <div className="alert-deadline">
          <Clock size={18} />
          <span>Termin: {format(new Date(mostCritical.deadline), 'dd MMMM yyyy', { locale: pl })}</span>
          <span className="days-left">({mostCritical.days_left} dni)</span>
        </div>
      </div>

      <div className="alert-actions">
        <button 
          className="btn-primary"
          onClick={() => onAction(mostCritical.case_id)}
        >
          📄 Przygotuj decyzję teraz
        </button>
        <button className="btn-secondary">
          📊 Zobacz szczegóły
        </button>
      </div>

      {criticalDeadlines.length > 1 && (
        <div className="alert-more">
          +{criticalDeadlines.length - 1} więcej krytycznych terminów
        </div>
      )}
    </div>
  )
}

