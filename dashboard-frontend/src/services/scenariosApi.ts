import axios from 'axios'
import { Scenario } from '../types'

// Domyślnie używa portu 8002 (nowy projekt Scenariusze Jutra)
// Możesz zmienić port ustawiając VITE_API_URL w pliku .env
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface ScenarioResponse {
  scenario_id: string
  title: string
  horizon: '12M' | '36M'
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH'
  confidence: number
  drivers: string[]
  recommendations: string[]
  explainability: {
    key_factors: Array<{ factor: string; weight: number }>
    logic_summary: string
  }
  scenario_type: 'positive' | 'negative'
}

export interface ScenariosData {
  scenarios: ScenarioResponse[]
  statistics: {
    total: number
    positive: number
    negative: number
  }
  status?: 'analysis_in_progress' | 'no_data' | 'ready'
  message?: string
}

export interface WhatIfValues {
  energy: number
  conflict: number
  investment: number
}

// Fetch all scenarios
export const fetchScenarios = async (): Promise<ScenariosData> => {
  const response = await api.get('/api/scenarios')
  return response.data
}

// Accept a scenario (swipe right)
export const acceptScenario = async (scenarioId: string) => {
  const response = await api.post(`/api/scenarios/${scenarioId}/accept`)
  return response.data
}

// Reject a scenario (swipe left)
export const rejectScenario = async (scenarioId: string) => {
  const response = await api.post(`/api/scenarios/${scenarioId}/reject`)
  return response.data
}

// Update weights based on "What if" sliders
export const updateWeights = async (values: WhatIfValues): Promise<ScenariosData> => {
  const response = await api.post('/api/scenarios/update-weights', values)
  return response.data
}

// Get scenario details
export const getScenarioDetails = async (scenarioId: string): Promise<ScenarioResponse> => {
  const response = await api.get(`/api/scenarios/${scenarioId}`)
  return response.data
}

export default api

