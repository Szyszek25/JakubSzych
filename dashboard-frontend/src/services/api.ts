import axios from 'axios'
import { DashboardStats, SystemStatus, Case, Deadline } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const fetchDashboardStats = async (): Promise<DashboardStats> => {
  const response = await api.get('/api/dashboard/stats')
  return response.data
}

export const fetchSystemStatus = async (): Promise<SystemStatus> => {
  const response = await api.get('/api/system/status')
  return response.data
}

export const fetchCases = async (): Promise<Case[]> => {
  const response = await api.get('/api/cases')
  return response.data.cases
}

export const fetchCaseDetail = async (caseId: string) => {
  const response = await api.get(`/api/cases/${caseId}`)
  return response.data
}

export const fetchDeadlines = async (daysAhead: number = 30): Promise<Deadline[]> => {
  const response = await api.get(`/api/deadlines?days_ahead=${daysAhead}`)
  return response.data.deadlines
}

export const fetchPerformanceMetrics = async () => {
  const response = await api.get('/api/performance')
  return response.data
}

export const analyzeCase = async (caseId: string) => {
  const response = await api.post(`/api/cases/${caseId}/analyze`)
  return response.data
}

export const generateDecision = async (caseId: string, decisionType: string = 'pozytywna') => {
  const response = await api.post(`/api/cases/${caseId}/generate-decision?decision_type=${decisionType}`)
  return response.data
}

export const initDemoData = async () => {
  const response = await api.post('/api/demo/init')
  return response.data
}

export default api

