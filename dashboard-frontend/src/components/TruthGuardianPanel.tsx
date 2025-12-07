import { Shield, CheckCircle, XCircle, AlertTriangle } from 'lucide-react'
import './TruthGuardianPanel.css'

interface TruthGuardianPanelProps {
  stats: {
    total_verifications: number
    fake_detected: number
    verified: number
  }
}

export default function TruthGuardianPanel({ stats }: TruthGuardianPanelProps) {
  const verificationRate = stats.total_verifications > 0
    ? ((stats.verified / stats.total_verifications) * 100).toFixed(1)
    : '0'

  const fakeRate = stats.total_verifications > 0
    ? ((stats.fake_detected / stats.total_verifications) * 100).toFixed(1)
    : '0'

  return (
    <div className="truth-guardian-panel">
      <div className="panel-header">
        <Shield size={20} />
        <h3>Truth Guardian (COI)</h3>
      </div>
      
      <div className="guardian-stats">
        <div className="guardian-stat">
          <div className="stat-icon verified">
            <CheckCircle size={24} />
          </div>
          <div className="stat-info">
            <p className="stat-value">{stats.verified}</p>
            <p className="stat-label">Zweryfikowane</p>
            <p className="stat-percent">{verificationRate}%</p>
          </div>
        </div>

        <div className="guardian-stat">
          <div className="stat-icon fake">
            <XCircle size={24} />
          </div>
          <div className="stat-info">
            <p className="stat-value">{stats.fake_detected}</p>
            <p className="stat-label">Wykryte fake</p>
            <p className="stat-percent">{fakeRate}%</p>
          </div>
        </div>

        <div className="guardian-stat">
          <div className="stat-icon total">
            <AlertTriangle size={24} />
          </div>
          <div className="stat-info">
            <p className="stat-value">{stats.total_verifications}</p>
            <p className="stat-label">Łącznie weryfikacji</p>
          </div>
        </div>
      </div>

      <div className="guardian-description">
        <p>System immunologiczny kognitywny do wykrywania dezinformacji w dokumentach administracyjnych.</p>
      </div>
    </div>
  )
}

