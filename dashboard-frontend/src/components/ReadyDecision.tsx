import { CheckCircle, FileText } from 'lucide-react'
import './ReadyDecision.css'

interface ReadyDecisionProps {
  caseId: string
  complianceScore: number
  onView: () => void
}

export default function ReadyDecision({ caseId, complianceScore, onView }: ReadyDecisionProps) {
  return (
    <div className="ready-decision">
      <div className="decision-header">
        <CheckCircle size={24} className="success-icon" />
        <div>
          <h3>✅ Projekt decyzji gotowy</h3>
          <p className="case-id">{caseId}</p>
        </div>
      </div>
      
      <div className="decision-score">
        <div className="score-circle">
          <span className="score-value">{complianceScore}%</span>
          <span className="score-label">zgodność</span>
        </div>
        <div className="score-details">
          <p>✓ Zgodność z KPA</p>
          <p>✓ Uzasadnienie prawne</p>
          <p>✓ Uzasadnienie faktyczne</p>
        </div>
      </div>

      <button className="btn-view" onClick={onView}>
        <FileText size={20} />
        Zobacz i zatwierdź decyzję
      </button>
    </div>
  )
}

