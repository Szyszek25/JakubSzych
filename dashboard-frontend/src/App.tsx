import { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import { DashboardStats, SystemStatus } from './types'
import { fetchDashboardStats, fetchSystemStatus } from './services/api'
import './App.css'

function App() {
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
      const [statsData, statusData] = await Promise.all([
        fetchDashboardStats(),
        fetchSystemStatus()
      ])
      setStats(statsData)
      setSystemStatus(statusData)
      setError(null)
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
        <p className="hint">Upewnij się, że backend API działa na porcie 8000</p>
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

  return (
    <div className="app">
      <Dashboard stats={stats} systemStatus={systemStatus} onRefresh={loadData} />
    </div>
  )
}

export default App

