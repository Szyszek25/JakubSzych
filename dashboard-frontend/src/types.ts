export interface DashboardStats {
  summary: {
    total_cases: number
    total_analyses: number
    avg_analysis_time: number
    avg_decision_time: number
    upcoming_deadlines: number
    critical_deadlines: number
  }
  cases_by_status: Record<string, number>
  cases_by_type: Record<string, number>
  cases_by_risk: {
    niski: number
    średni: number
    wysoki: number
    krytyczny: number
  }
  performance_metrics: {
    total_cases: number
    total_analyses: number
    avg_analysis_time: number
    avg_decision_generation_time: number
  }
  deadlines: {
    upcoming: Deadline[]
    critical: Deadline[]
  }
  truth_guardian: {
    total_verifications: number
    fake_detected: number
    verified: number
  }
  timestamp: string
}

export interface Deadline {
  case_id: string
  case_type: string
  deadline: string
  days_left: number
  priority: string
  status: string
}

export interface SystemStatus {
  gqpa: {
    available: boolean
    info: {
      name: string
      version: string
      status: string
    } | null
  }
  ollama: {
    status: string
    using_local: boolean
  }
  gemini: {
    available: boolean
    using_api: boolean
  }
  guardrails: {
    enabled: boolean
    audit_log_size: number
  }
  timestamp: string
}

export interface Case {
  case_id: string
  type: string
  status: string
  parties: string[]
  deadline: string | null
  summary: string | null
  risk_level: string
  compliance_score: number
  created_at: string
  updated_at: string
}

