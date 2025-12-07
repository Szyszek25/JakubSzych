import { useState, useEffect } from 'react'
import { fetchCases, Case } from '../services/api'
import { format } from 'date-fns'
import pl from 'date-fns/locale/pl'
import { FileText, Calendar, Users, AlertCircle } from 'lucide-react'
import './CasesList.css'

export default function CasesList() {
  const [cases, setCases] = useState<Case[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadCases()
    // Odśwież co 5 sekund
    const interval = setInterval(loadCases, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadCases = async () => {
    try {
      const data = await fetchCases()
      setCases(data)
    } catch (error) {
      console.error('Błąd ładowania spraw:', error)
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'niski': return 'green'
      case 'średni': return 'yellow'
      case 'wysoki': return 'orange'
      case 'krytyczny': return 'red'
      default: return 'gray'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'zakończona': return 'success'
      case 'w_trakcie': return 'info'
      case 'oczekuje_decyzji': return 'warning'
      default: return 'default'
    }
  }

  if (loading) {
    return (
      <div className="cases-list-card">
        <p>Ładowanie spraw...</p>
      </div>
    )
  }

  return (
    <div className="cases-list-card">
      <div className="cases-list-header">
        <h3>Lista spraw</h3>
        <span className="cases-count">{cases.length} spraw</span>
      </div>
      
      <div className="cases-list">
        {cases.length === 0 ? (
          <p className="empty-state">Brak spraw w systemie</p>
        ) : (
          cases.map((caseItem) => (
            <div key={caseItem.case_id} className="case-item">
              <div className="case-header">
                <div className="case-id">
                  <FileText size={16} />
                  <span>{caseItem.case_id}</span>
                </div>
                <div className="case-badges">
                  <span className={`badge badge-${getStatusColor(caseItem.status)}`}>
                    {caseItem.status.replace('_', ' ')}
                  </span>
                  <span className={`badge badge-risk badge-${getRiskColor(caseItem.risk_level)}`}>
                    {caseItem.risk_level}
                  </span>
                </div>
              </div>
              
              <div className="case-body">
                <p className="case-type">{caseItem.type.replace('_', ' ')}</p>
                {caseItem.summary && (
                  <p className="case-summary">{caseItem.summary}</p>
                )}
              </div>
              
              <div className="case-footer">
                <div className="case-info">
                  <Users size={14} />
                  <span>{caseItem.parties.length} strony</span>
                </div>
                {caseItem.deadline && (
                  <div className="case-info">
                    <Calendar size={14} />
                    <span>
                      {format(new Date(caseItem.deadline), 'dd MMM yyyy', { locale: pl })}
                    </span>
                  </div>
                )}
                <div className="case-score">
                  Zgodność: {caseItem.compliance_score.toFixed(0)}%
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

