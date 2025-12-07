import { SystemStatus } from '../types'
import { CheckCircle, Shield, Database } from 'lucide-react'
import './SystemStatusPanel.css'

interface SystemStatusPanelProps {
  status: SystemStatus | null
}

export default function SystemStatusPanel({ status }: SystemStatusPanelProps) {
  if (!status) {
    return (
      <div className="status-panel">
        <p>Ładowanie statusu...</p>
      </div>
    )
  }

  const statusItems = [
    {
      label: 'GQPA Core',
      value: status.gqpa.available ? 'Dostępny' : 'Niedostępny',
      icon: Database,
      status: status.gqpa.available ? 'success' : 'error',
      details: status.gqpa.info ? `${status.gqpa.info.name} v${status.gqpa.info.version}` : null
    },
    {
      label: 'Ollama (Lokalny)',
      value: status.ollama.status === 'available' ? 'Dostępny' : 'Niedostępny',
      icon: CheckCircle,
      status: status.ollama.status === 'available' ? 'success' : 'error',
      details: status.ollama.using_local ? 'Używany lokalny model open-source' : 'API mode'
    },
    {
      label: 'Guardrails',
      value: status.guardrails.enabled ? 'Aktywne' : 'Nieaktywne',
      icon: Shield,
      status: status.guardrails.enabled ? 'success' : 'error',
      details: `${status.guardrails.audit_log_size} wpisów w logu`
    }
  ]

  return (
    <div className="status-panel">
      <h3>Status systemu</h3>
      <div className="status-list">
        {statusItems.map((item, index) => {
          const Icon = item.icon
          return (
            <div key={index} className={`status-item status-${item.status}`}>
              <div className="status-icon">
                <Icon size={18} />
              </div>
              <div className="status-content">
                <p className="status-label">{item.label}</p>
                <p className="status-value">{item.value}</p>
                {item.details && (
                  <p className="status-details">{item.details}</p>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

