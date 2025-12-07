import { DashboardStats } from '../types'
import { FileText, Clock, CheckCircle, AlertTriangle, TrendingUp } from 'lucide-react'
import './StatCards.css'

interface StatCardsProps {
  stats: DashboardStats
}

export default function StatCards({ stats }: StatCardsProps) {
  const cards = [
    {
      title: 'Łącznie spraw',
      value: stats.summary.total_cases,
      icon: FileText,
      color: 'blue',
      change: null
    },
    {
      title: 'Średni czas analizy',
      value: `${stats.summary.avg_analysis_time}s`,
      icon: Clock,
      color: 'purple',
      change: null
    },
    {
      title: 'Zakończone analizy',
      value: stats.summary.total_analyses,
      icon: CheckCircle,
      color: 'green',
      change: null
    },
    {
      title: 'Krytyczne terminy',
      value: stats.summary.critical_deadlines,
      icon: AlertTriangle,
      color: 'red',
      change: stats.summary.critical_deadlines > 0 ? 'wymaga uwagi' : null
    },
    {
      title: 'Średni czas decyzji',
      value: `${stats.summary.avg_decision_time}s`,
      icon: TrendingUp,
      color: 'orange',
      change: null
    }
  ]

  return (
    <div className="stat-cards">
      {cards.map((card, index) => {
        const Icon = card.icon
        return (
          <div key={index} className={`stat-card stat-card-${card.color}`}>
            <div className="stat-card-icon">
              <Icon size={24} />
            </div>
            <div className="stat-card-content">
              <p className="stat-card-title">{card.title}</p>
              <p className="stat-card-value">{card.value}</p>
              {card.change && (
                <p className="stat-card-change">{card.change}</p>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

