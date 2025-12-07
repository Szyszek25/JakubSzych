import { useState, useEffect, useRef } from 'react'
import { useAnalysisStream } from '../hooks/useAnalysisStream'
import './AnalysisDashboard.css'

interface AnalysisStep {
  id: string
  label: string
  status: 'pending' | 'active' | 'completed'
  progress: number
}

interface Scenario {
  id: string
  type: 'positive' | 'negative'
  timeframe: 12 | 36
  title: string
  confidence: number
  impacts: {
    polityka: number
    gospodarka: number
    bezpieczeństwo: number
    społeczeństwo: number
  }
}

export default function AnalysisDashboard() {
  const { currentStep, scenarios: streamScenarios, isStreaming, error, startStream } = useAnalysisStream()
  const [dataStreams, setDataStreams] = useState<string[]>([])
  const [graphNodes, setGraphNodes] = useState<any[]>([])
  const [scenarios, setScenarios] = useState<Scenario[]>([])
  const [analysisProgress, setAnalysisProgress] = useState(0)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  // Mapuj kroki analizy na format UI
  const getAnalysisSteps = (): AnalysisStep[] => {
    if (!currentStep) {
      return [
        { id: 'ingest', label: 'Zbieranie danych', status: 'pending', progress: 0 },
        { id: 'correlate', label: 'Budowa łańcuchów przyczynowych', status: 'pending', progress: 0 },
        { id: 'simulate', label: 'Symulacja przyszłości', status: 'pending', progress: 0 },
        { id: 'generate', label: 'Generowanie scenariuszy', status: 'pending', progress: 0 }
      ]
    }

    const stepMap: Record<number, { id: string; label: string }> = {
      1: { id: 'ingest', label: 'Zbieranie danych' },
      2: { id: 'verify', label: 'Weryfikacja danych' },
      3: { id: 'analyze', label: 'Analiza danych' },
      4: { id: 'graph', label: 'Budowa grafu wiedzy' },
      5: { id: 'factors', label: 'Rejestracja czynników' },
      6: { id: 'prioritize', label: 'Priorytetyzacja faktów' },
      7: { id: 'correlate', label: 'Budowa łańcuchów przyczynowych' },
      8: { id: 'generate', label: 'Generowanie scenariuszy' },
      9: { id: 'recommend', label: 'Generowanie rekomendacji' },
      10: { id: 'complete', label: 'Zakończono' }
    }

    const currentStepInfo = stepMap[currentStep.step] || { id: 'unknown', label: currentStep.name }
    
    return [
      { id: 'ingest', label: 'Zbieranie danych', status: currentStep.step >= 1 ? 'completed' : 'pending', progress: currentStep.step >= 1 ? 100 : 0 },
      { id: 'correlate', label: 'Budowa łańcuchów przyczynowych', status: currentStep.step >= 7 ? 'completed' : currentStep.step === 7 ? 'active' : 'pending', progress: currentStep.step >= 7 ? 100 : currentStep.step === 7 ? currentStep.progress : 0 },
      { id: 'simulate', label: 'Symulacja przyszłości', status: currentStep.step >= 8 ? 'active' : 'pending', progress: currentStep.step >= 8 ? currentStep.progress : 0 },
      { id: 'generate', label: 'Generowanie scenariuszy', status: currentStep.step >= 8 ? 'active' : 'pending', progress: currentStep.step >= 8 ? currentStep.progress : 0 }
    ]
  }

  const analysisSteps = getAnalysisSteps()

  // Uruchom streaming przy montowaniu komponentu
  useEffect(() => {
    startStream()
  }, [startStream])

  // Aktualizuj postęp
  useEffect(() => {
    if (currentStep) {
      setAnalysisProgress(currentStep.progress)
    }
  }, [currentStep])

  // Aktualizuj scenariusze gdy są gotowe
  useEffect(() => {
    if (streamScenarios && streamScenarios.scenarios) {
      const mappedScenarios: Scenario[] = streamScenarios.scenarios.map((s: any) => ({
        id: s.scenario_id,
        title: s.title,
        horizon: s.horizon,
        risk_level: s.risk_level,
        confidence: s.confidence,
        drivers: s.drivers || [],
        recommendations: s.recommendations || [],
        explainability: s.explainability || { key_factors: [], logic_summary: '' },
        scenario_type: s.scenario_type,
        impacts: {
          gospodarka: 0.7,
          bezpieczeństwo: 0.6,
          społeczeństwo: 0.5
        }
      }))
      setScenarios(mappedScenarios)
    }
  }, [streamScenarios])

  // Symulacja strumieni danych
  useEffect(() => {
    const sources = [
      'media międzynarodowe',
      'raporty instytucjonalne',
      'dane ekonomiczne',
      'analizy think-tanków',
      'komunikaty dyplomatyczne'
    ]

    const interval = setInterval(() => {
      const randomSource = sources[Math.floor(Math.random() * sources.length)]
      setDataStreams(prev => [...prev.slice(-4), randomSource])
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  // Animacja grafu zależności
  useEffect(() => {
    if (!canvasRef.current) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    canvas.width = canvas.offsetWidth
    canvas.height = canvas.offsetHeight

    const nodes = [
      { id: 'factor_a', x: 100, y: 150, label: 'Procesory', weight: 30 },
      { id: 'factor_b', x: 300, y: 100, label: 'Motoryzacja', weight: 15 },
      { id: 'factor_c', x: 500, y: 150, label: 'PKB', weight: 15 },
      { id: 'factor_d', x: 200, y: 300, label: 'Ukraina', weight: 10 },
      { id: 'factor_e', x: 400, y: 300, label: 'Inwestycje', weight: 5 },
      { id: 'factor_f', x: 300, y: 250, label: 'OZE', weight: 25 }
    ]

    const connections = [
      { from: 'factor_a', to: 'factor_c', strength: 0.7 },
      { from: 'factor_b', to: 'factor_c', strength: 0.5 },
      { from: 'factor_d', to: 'factor_e', strength: 0.8 },
      { from: 'factor_f', to: 'factor_c', strength: 0.6 }
    ]

    let animationFrame = 0
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      // Rysuj połączenia
      connections.forEach((conn, idx) => {
        const fromNode = nodes.find(n => n.id === conn.from)
        const toNode = nodes.find(n => n.id === conn.to)
        if (!fromNode || !toNode) return

        const progress = Math.min(1, (animationFrame - idx * 30) / 60)
        if (progress > 0 && progress < 1) {
          const currentX = fromNode.x + (toNode.x - fromNode.x) * progress
          const currentY = fromNode.y + (toNode.y - fromNode.y) * progress

          ctx.strokeStyle = `rgba(255, 193, 7, ${0.3 + progress * 0.5})`
          ctx.lineWidth = conn.strength * 3
          ctx.beginPath()
          ctx.moveTo(fromNode.x, fromNode.y)
          ctx.lineTo(currentX, currentY)
          ctx.stroke()
        } else if (progress >= 1) {
          ctx.strokeStyle = `rgba(255, 193, 7, ${0.3 + conn.strength * 0.5})`
          ctx.lineWidth = conn.strength * 3
          ctx.beginPath()
          ctx.moveTo(fromNode.x, fromNode.y)
          ctx.lineTo(toNode.x, toNode.y)
          ctx.stroke()
        }
      })

      // Rysuj węzły
      nodes.forEach((node, idx) => {
        const appearProgress = Math.min(1, (animationFrame - idx * 20) / 40)
        if (appearProgress > 0) {
          ctx.fillStyle = `rgba(255, 193, 7, ${0.6 + appearProgress * 0.4})`
          ctx.beginPath()
          ctx.arc(node.x, node.y, 8 + appearProgress * 4, 0, Math.PI * 2)
          ctx.fill()

          // Etykieta
          ctx.fillStyle = 'rgba(255, 255, 255, 0.9)'
          ctx.font = '12px "Inter", sans-serif'
          ctx.textAlign = 'center'
          ctx.fillText(node.label, node.x, node.y - 15)
        }
      })

      animationFrame++
      requestAnimationFrame(animate)
    }

    animate()
  }, [])

  // Symulacja procesu analizy
  useEffect(() => {
    if (!isAnalyzing) return

    const interval = setInterval(() => {
      setAnalysisProgress(prev => {
        if (prev >= 100) {
          setIsAnalyzing(false)
          // Generuj scenariusze
          setTimeout(() => {
            setScenarios([
              {
                id: 'pos_12',
                type: 'positive',
                timeframe: 12,
                title: 'Scenariusz pozytywny - 12 miesięcy',
                confidence: 85,
                impacts: { polityka: 75, gospodarka: 80, bezpieczeństwo: 70, społeczeństwo: 75 }
              },
              {
                id: 'neg_12',
                type: 'negative',
                timeframe: 12,
                title: 'Scenariusz negatywny - 12 miesięcy',
                confidence: 75,
                impacts: { polityka: 60, gospodarka: 55, bezpieczeństwo: 65, społeczeństwo: 60 }
              },
              {
                id: 'pos_36',
                type: 'positive',
                timeframe: 36,
                title: 'Scenariusz pozytywny - 36 miesięcy',
                confidence: 70,
                impacts: { polityka: 70, gospodarka: 75, bezpieczeństwo: 65, społeczeństwo: 70 }
              },
              {
                id: 'neg_36',
                type: 'negative',
                timeframe: 36,
                title: 'Scenariusz negatywny - 36 miesięcy',
                confidence: 65,
                impacts: { polityka: 55, gospodarka: 50, bezpieczeństwo: 60, społeczeństwo: 55 }
              }
            ])
          }, 500)
          return 100
        }
        return prev + 0.5
      })
    }, 50)

    return () => clearInterval(interval)
  }, [isAnalyzing])

  return (
    <div className="analysis-dashboard">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Decision Intelligence for the Next Decade</h1>
          <p className="hero-subtitle">From data to policy-ready scenarios</p>
        </div>
        <div className="hero-background">
          <canvas ref={canvasRef} className="graph-canvas" />
        </div>
      </div>

      {/* Main Analysis Panel */}
      <div className="analysis-panel">
        <div className="panel-header">
          <h2>System Analysis</h2>
          <div className="timeframe-toggle">
            <button className={currentStep === 0 ? 'active' : ''}>12 months</button>
            <button className={currentStep === 1 ? 'active' : ''}>36 months</button>
          </div>
        </div>

        {/* Data Ingestion Animation */}
        <div className="data-ingestion">
          <h3>Data Ingestion</h3>
          <div className="data-streams">
            {dataStreams.map((source, idx) => (
              <div key={idx} className="data-stream">
                <div className="stream-line" />
                <span className="stream-label">{source}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Analysis Progress */}
        <div className="analysis-progress">
          <div className="progress-header">
            <span>{isStreaming ? 'Analiza w toku...' : currentStep?.status === 'completed' ? 'Analiza zakończona' : 'Oczekiwanie na analizę'}</span>
            <span className="progress-percent">{Math.round(analysisProgress)}%</span>
          </div>
          {error && (
            <div style={{ color: '#ef4444', fontSize: '0.875rem', marginTop: '0.5rem' }}>
              ⚠️ {error}
            </div>
          )}
          {currentStep && (
            <div style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
              {currentStep.name}
            </div>
          )}
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${analysisProgress}%` }}
            />
          </div>
          <div className="analysis-steps">
            {analysisSteps.map((step, idx) => (
              <div 
                key={step.id} 
                className={`analysis-step ${step.status}`}
                style={{ opacity: idx <= currentStep ? 1 : 0.3 }}
              >
                <div className="step-indicator">
                  {step.status === 'completed' ? '✓' : step.status === 'active' ? '⟳' : '○'}
                </div>
                <span>{step.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Scenarios */}
        {scenarios.length > 0 && (
          <div className="scenarios-section">
            <h3>Generated Scenarios</h3>
            <div className="scenarios-grid">
              {scenarios.map((scenario, idx) => (
                <div 
                  key={scenario.id} 
                  className={`scenario-card ${scenario.type}`}
                  style={{ 
                    animationDelay: `${idx * 0.2}s`,
                    animation: 'slideInUp 0.6s ease-out forwards'
                  }}
                >
                  <div className="scenario-header">
                    <span className="scenario-type">{scenario.type === 'positive' ? 'Positive' : 'Negative'}</span>
                    <span className="scenario-timeframe">{scenario.timeframe}m</span>
                  </div>
                  <h4>{scenario.title}</h4>
                  <div className="confidence-meter">
                    <span>Confidence</span>
                    <div className="confidence-bar">
                      <div 
                        className="confidence-fill" 
                        style={{ width: `${scenario.confidence}%` }}
                      />
                      <span className="confidence-value">{scenario.confidence}%</span>
                    </div>
                  </div>
                  <div className="impacts">
                    {Object.entries(scenario.impacts).map(([key, value]) => (
                      <div key={key} className="impact-item">
                        <span className="impact-label">{key}</span>
                        <div className="impact-bar">
                          <div 
                            className="impact-fill" 
                            style={{ width: `${value}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Sidebar - System Status */}
      <div className="system-sidebar">
        <div className="status-panel">
          <h3>System Status</h3>
          <div className="status-item">
            <span className="status-label">Factors analyzed</span>
            <span className="status-value">6</span>
          </div>
          <div className="status-item">
            <span className="status-label">Confidence level</span>
            <span className="status-value">High</span>
          </div>
          <div className="status-item">
            <span className="status-label">Last update</span>
            <span className="status-value">{new Date().toLocaleTimeString()}</span>
          </div>
        </div>

        <div className="terminal-panel">
          <div className="terminal-header">System Terminal</div>
          <div className="terminal-content">
            <div className="terminal-line">
              <span className="terminal-prompt">$</span>
              <span>System analyzing geopolitical factors...</span>
            </div>
            <div className="terminal-line">
              <span className="terminal-prompt">$</span>
              <span>Building causal dependency graph...</span>
            </div>
            <div className="terminal-line">
              <span className="terminal-prompt">$</span>
              <span className="terminal-success">✓ Scenarios generated</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

