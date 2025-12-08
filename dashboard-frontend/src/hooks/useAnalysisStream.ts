import { useState, useEffect, useRef } from 'react'

interface AnalysisStep {
  step: number
  name: string
  progress: number
  status: 'running' | 'completed' | 'error' | 'pending'
  error?: string
}

interface ScenariosReady {
  type: 'scenarios_ready'
  data: any
}

type StreamEvent = AnalysisStep | ScenariosReady

export function useAnalysisStream() {
  const [currentStep, setCurrentStep] = useState<AnalysisStep | null>(null)
  const [scenarios, setScenarios] = useState<any>(null)
  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const eventSourceRef = useRef<EventSource | null>(null)

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002'

  const startStream = () => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
    }

    setIsStreaming(true)
    setError(null)
    setCurrentStep(null)
    setScenarios(null)

    const eventSource = new EventSource(`${API_BASE_URL}/api/analysis/stream`)
    eventSourceRef.current = eventSource

    eventSource.onmessage = (event) => {
      try {
        const data: StreamEvent = JSON.parse(event.data)
        
        if ('type' in data && data.type === 'scenarios_ready') {
          setScenarios(data.data)
          setIsStreaming(false)
        } else if ('step' in data) {
          setCurrentStep(data as AnalysisStep)
          if (data.status === 'completed' || data.status === 'error') {
            setIsStreaming(false)
            if (data.status === 'error') {
              setError(data.error || 'Błąd podczas analizy')
            }
          }
        }
      } catch (err) {
        console.error('Błąd parsowania danych ze streamu:', err)
        setError('Błąd parsowania danych')
        setIsStreaming(false)
      }
    }

    eventSource.onerror = (err) => {
      console.error('Błąd połączenia SSE:', err)
      setError('Błąd połączenia z serwerem')
      setIsStreaming(false)
      eventSource.close()
    }
  }

  const stopStream = () => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
      eventSourceRef.current = null
    }
    setIsStreaming(false)
  }

  useEffect(() => {
    return () => {
      stopStream()
    }
  }, [])

  return {
    currentStep,
    scenarios,
    isStreaming,
    error,
    startStream,
    stopStream
  }
}


