import { DashboardStats } from '../types'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import './ChartsSection.css'

interface ChartsSectionProps {
  stats: DashboardStats
}

const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444']

export default function ChartsSection({ stats }: ChartsSectionProps) {
  // Przygotowanie danych dla wykresów
  const statusData = Object.entries(stats.cases_by_status).map(([name, value]) => ({
    name: name.replace('_', ' '),
    value
  }))

  const typeData = Object.entries(stats.cases_by_type).map(([name, value]) => ({
    name: name.replace('_', ' '),
    value
  }))

  const riskData = [
    { name: 'Niski', value: stats.cases_by_risk.niski },
    { name: 'Średni', value: stats.cases_by_risk.średni },
    { name: 'Wysoki', value: stats.cases_by_risk.wysoki },
    { name: 'Krytyczny', value: stats.cases_by_risk.krytyczny }
  ]

  return (
    <div className="charts-section">
      <div className="chart-card">
        <h3>Sprawy według statusu</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={statusData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-card">
        <h3>Sprawy według typu</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={typeData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8b5cf6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-card">
        <h3>Rozkład ryzyka</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={riskData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {riskData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

