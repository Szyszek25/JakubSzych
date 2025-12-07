import { RefreshCw, Database } from 'lucide-react'
import { initDemoData } from '../services/api'
import { useState } from 'react'
import './Header.css'

interface HeaderProps {
  onRefresh: () => void
}

export default function Header({ onRefresh }: HeaderProps) {
  const [loading, setLoading] = useState(false)

  const handleInitDemo = async () => {
    setLoading(true)
    try {
      const result = await initDemoData()
      // Odśwież dane po dodaniu demo
      setTimeout(() => {
        onRefresh()
        setLoading(false)
        if (result.cases_added) {
          alert(`✅ Dodano ${result.cases_added} spraw demo!`)
        } else if (result.skipped) {
          alert(`ℹ️ Dane demo już istnieją (${result.existing_cases} spraw)`)
        }
      }, 1000)
    } catch (error: any) {
      console.error('Błąd inicjalizacji danych demo:', error)
      setLoading(false)
      const errorMsg = error?.response?.data?.detail || error?.message || 'Nieznany błąd'
      alert(`❌ Błąd: ${errorMsg}\n\nUpewnij się że backend działa na porcie 8002`)
    }
  }

  return (
    <header className="dashboard-header">
      <div className="header-content">
        <div className="header-title">
          <h1>🏛️ Asystent AI dla Administracji</h1>
          <p className="subtitle">Pilnuje terminów i przygotowuje decyzje bez błędów proceduralnych</p>
        </div>
        <div className="header-actions">
          <button 
            className="demo-btn" 
            onClick={handleInitDemo} 
            disabled={loading}
            title="Dodaj przykładowe dane demo"
          >
            <Database size={18} />
            {loading ? 'Dodawanie...' : 'Dane Demo'}
          </button>
          <button className="refresh-btn" onClick={onRefresh} title="Odśwież dane">
            <RefreshCw size={20} />
            Odśwież
          </button>
        </div>
      </div>
    </header>
  )
}

