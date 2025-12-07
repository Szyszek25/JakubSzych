import { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import AnalysisDashboard from './components/AnalysisDashboard'
import ScenarioCardsStack from './components/ScenarioCardsStack'
import { DashboardStats, SystemStatus } from './types'
import { fetchDashboardStats, fetchSystemStatus } from './services/api'
import './App.css'

function App() {
  const [viewMode, setViewMode] = useState<'analysis' | 'dashboard' | 'scenarios'>('scenarios')
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 30000) // Odśwież co 30 sekund
    return () => clearInterval(interval)
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const [statsData, statusData] = await Promise.all([
        fetchDashboardStats().catch(err => {
          console.warn('Błąd pobierania stats:', err)
          return null
        }),
        fetchSystemStatus().catch(err => {
          console.warn('Błąd pobierania status:', err)
          return null
        })
      ])
      
      // Ustaw dane tylko jeśli zostały pobrane
      if (statsData) setStats(statsData)
      if (statusData) setSystemStatus(statusData)
      
      // Jeśli oba requesty się nie powiodły, ustaw błąd
      if (!statsData && !statusData) {
        setError('Nie można połączyć się z backendem API')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd ładowania danych')
      console.error('Błąd ładowania:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading && !stats) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Ładowanie dashboardu...</p>
        <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '1rem' }}>
          Łączenie z backendem API...
        </p>
      </div>
    )
  }

  if (error && !stats) {
    return (
      <div className="error-container">
        <h2>❌ Błąd połączenia</h2>
        <p>{error}</p>
        <button onClick={loadData}>Spróbuj ponownie</button>
        <p className="hint">Upewnij się, że backend API działa na porcie 8002</p>
        <p className="hint" style={{ marginTop: '0.5rem' }}>
          Sprawdź konsolę przeglądarki (F12) dla szczegółów błędu
        </p>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="error-container">
        <h2>⚠️ Brak danych</h2>
        <p>Nie udało się załadować danych z API</p>
        <button onClick={loadData}>Spróbuj ponownie</button>
      </div>
    )
  }

  // Toggle między widokami
  if (viewMode === 'scenarios') {
    return (
      <div className="app">
        <div style={{ position: 'fixed', top: '1rem', right: '1rem', zIndex: 1000, display: 'flex', gap: '0.5rem' }}>
          <button 
            onClick={() => setViewMode('dashboard')}
            style={{
              padding: '0.5rem 1rem',
              background: 'rgba(255, 193, 7, 0.2)',
              border: '1px solid rgba(255, 193, 7, 0.5)',
              color: '#ffc107',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '0.875rem'
            }}
          >
            Dashboard
          </button>
          <button 
            onClick={() => setViewMode('analysis')}
            style={{
              padding: '0.5rem 1rem',
              background: 'rgba(255, 193, 7, 0.2)',
              border: '1px solid rgba(255, 193, 7, 0.5)',
              color: '#ffc107',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '0.875rem'
            }}
          >
            Analysis
          </button>
        </div>
        <ScenarioCardsStack />
      </div>
    )
  }

  if (viewMode === 'analysis') {
    return (
      <div className="app">
        <div style={{ position: 'fixed', top: '1rem', right: '1rem', zIndex: 1000, display: 'flex', gap: '0.5rem' }}>
          <button 
            onClick={() => setViewMode('scenarios')}
            style={{
              padding: '0.5rem 1rem',
              background: 'rgba(255, 193, 7, 0.2)',
              border: '1px solid rgba(255, 193, 7, 0.5)',
              color: '#ffc107',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '0.875rem'
            }}
          >
            Scenarios
          </button>
          <button 
            onClick={() => setViewMode('dashboard')}
            style={{
              padding: '0.5rem 1rem',
              background: 'rgba(255, 193, 7, 0.2)',
              border: '1px solid rgba(255, 193, 7, 0.5)',
              color: '#ffc107',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '0.875rem'
            }}
          >
            Dashboard
          </button>
        </div>
        <AnalysisDashboard />
      </div>
    )
  }

  return (
    <div className="app">
      <div style={{ position: 'fixed', top: '1rem', right: '1rem', zIndex: 1000, display: 'flex', gap: '0.5rem' }}>
        <button 
          onClick={() => setViewMode('scenarios')}
          style={{
            padding: '0.5rem 1rem',
            background: 'rgba(255, 193, 7, 0.2)',
            border: '1px solid rgba(255, 193, 7, 0.5)',
            color: '#ffc107',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '0.875rem'
          }}
        >
          Scenarios
        </button>
        <button 
          onClick={() => setViewMode('analysis')}
          style={{
            padding: '0.5rem 1rem',
            background: 'rgba(255, 193, 7, 0.2)',
            border: '1px solid rgba(255, 193, 7, 0.5)',
            color: '#ffc107',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '0.875rem'
          }}
        >
          Analysis
        </button>
      </div>
      <Dashboard stats={stats} systemStatus={systemStatus} onRefresh={loadData} />
    </div>
  )
}

export default App

