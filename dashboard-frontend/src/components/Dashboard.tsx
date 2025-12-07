import { useState, useEffect } from 'react'
import { DashboardStats, SystemStatus } from '../types'
import Header from './Header'
import CriticalAlert from './CriticalAlert'
import ReadyDecision from './ReadyDecision'
import StatCards from './StatCards'
import CasesList from './CasesList'
import SystemStatusPanel from './SystemStatusPanel'
import { generateDecision } from '../services/api'
import './Dashboard.css'

interface DashboardProps {
  stats: DashboardStats | null
  systemStatus: SystemStatus | null
  onRefresh: () => void
}

export default function Dashboard({ stats, systemStatus, onRefresh }: DashboardProps) {
  const [refreshKey, setRefreshKey] = useState(0)
  const [generating, setGenerating] = useState(false)

  const handleRefresh = () => {
    onRefresh()
    setRefreshKey(prev => prev + 1)
  }

  const handleGenerateDecision = async (caseId: string) => {
    setGenerating(true)
    try {
      const decision = await generateDecision(caseId, 'pozytywna')
      alert(`✅ Decyzja wygenerowana!\n\nZgodność: ${Object.values(decision.compliance_checks).filter(Boolean).length}/${Object.keys(decision.compliance_checks).length}\n\nSprawdź szczegóły w konsoli.`)
      onRefresh()
    } catch (error) {
      console.error('Błąd generowania decyzji:', error)
      alert('Błąd generowania decyzji. Sprawdź konsolę.')
    } finally {
      setGenerating(false)
    }
  }

  if (!stats) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <p>Ładowanie danych...</p>
      </div>
    )
  }

  // Znajdź sprawę z gotową decyzją (symulacja)
  const readyCase = stats.summary.total_cases > 0 ? {
    caseId: 'SPR-2024-002',
    complianceScore: 96
  } : null

  return (
    <div className="dashboard">
      <Header onRefresh={handleRefresh} />
      
      <div className="dashboard-content">
        <div className="dashboard-main">
          {/* GŁÓWNA AKCJA: Krytyczny termin */}
          {stats.deadlines.critical.length > 0 && (
            <CriticalAlert 
              criticalDeadlines={stats.deadlines.critical}
              onAction={handleGenerateDecision}
            />
          )}

          {/* GOTOWA DECYZJA */}
          {readyCase && stats.summary.total_cases > 2 && (
            <ReadyDecision
              caseId={readyCase.caseId}
              complianceScore={readyCase.complianceScore}
              onView={() => alert('Szczegóły decyzji - funkcja w rozwoju')}
            />
          )}

          {/* UPROSZCZONE STATYSTYKI */}
          <div className="simple-stats">
            <div className="stat-item">
              <span className="stat-number">{stats.summary.total_cases}</span>
              <span className="stat-label">Spraw w systemie</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{stats.summary.critical_deadlines}</span>
              <span className="stat-label">Krytyczne terminy</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{stats.summary.total_analyses}</span>
              <span className="stat-label">Zakończone analizy</span>
            </div>
          </div>

          {/* LISTA SPRAW */}
          <CasesList key={refreshKey} />
        </div>
        
        <div className="dashboard-sidebar">
          <SystemStatusPanel status={systemStatus} />
        </div>
      </div>
    </div>
  )
}

