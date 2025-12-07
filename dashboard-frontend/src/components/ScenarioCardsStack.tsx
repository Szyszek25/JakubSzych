import { useState, useEffect, useRef } from 'react'
import { fetchScenarios, acceptScenario, rejectScenario, updateWeights, ScenariosData } from '../services/scenariosApi'
import { useAnalysisStream } from '../hooks/useAnalysisStream'
import './ScenarioCardsStack.css'

interface Scenario {
  id: string
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

interface ScenarioCardsStackProps {
  onScenarioChange?: (scenario: Scenario) => void
}

interface ScenarioResponse {
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

export default function ScenarioCardsStack({ onScenarioChange: _onScenarioChange }: ScenarioCardsStackProps) {
  const { currentStep, scenarios: streamScenarios, isStreaming, startStream } = useAnalysisStream()
  const [scenarios, setScenarios] = useState<Scenario[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isExpanded, setIsExpanded] = useState(false)
  const [whatIfValues, setWhatIfValues] = useState({
    energy: 50,
    conflict: 50,
    investment: 50
  })
  const [loading, setLoading] = useState(true)
  
  const cardRef = useRef<HTMLDivElement>(null)
  const startX = useRef(0)
  const currentX = useRef(0)
  const isDragging = useRef(false)

  useEffect(() => {
    // Uruchom streaming i załaduj scenariusze
    startStream()
    loadScenarios()
  }, [startStream])

  // Aktualizuj scenariusze gdy są gotowe ze streamu
  useEffect(() => {
    if (streamScenarios && streamScenarios.scenarios && streamScenarios.scenarios.length > 0) {
      const mappedScenarios: Scenario[] = streamScenarios.scenarios.map((s: ScenarioResponse) => ({
        id: s.scenario_id,
        title: s.title,
        horizon: s.horizon,
        risk_level: s.risk_level,
        confidence: s.confidence,
        drivers: s.drivers,
        recommendations: s.recommendations,
        explainability: s.explainability,
        scenario_type: s.scenario_type
      }))
      setScenarios(mappedScenarios)
      setLoading(false)
    }
  }, [streamScenarios])

  useEffect(() => {
    // Recalculate scenarios when "What if" sliders change
    if (scenarios.length > 0) {
      recalculateScenarios()
    }
  }, [whatIfValues])

  const loadScenarios = async () => {
    try {
      setLoading(true)
      const data: ScenariosData = await fetchScenarios()
      
      // Sprawdź czy analiza jest w toku
      if (data.status === 'analysis_in_progress') {
        setLoading(true)
        // Czekaj i spróbuj ponownie za 3 sekundy
        setTimeout(() => {
          loadScenarios()
        }, 3000)
        return
      }
      
      // Mapuj ScenarioResponse na Scenario
      const mappedScenarios: Scenario[] = (data.scenarios || []).map((s: ScenarioResponse) => ({
        id: s.scenario_id,
        title: s.title,
        horizon: s.horizon,
        risk_level: s.risk_level,
        confidence: s.confidence,
        drivers: s.drivers,
        recommendations: s.recommendations,
        explainability: s.explainability,
        scenario_type: s.scenario_type
      }))
      setScenarios(mappedScenarios)
      setCurrentIndex(0)
    } catch (error) {
      console.error('Błąd ładowania scenariuszy:', error)
    } finally {
      setLoading(false)
    }
  }

  const recalculateScenarios = async () => {
    try {
      const updated = await updateWeights(whatIfValues)
      // Mapuj ScenarioResponse na Scenario
      const mappedScenarios: Scenario[] = (updated.scenarios || []).map((s: ScenarioResponse) => ({
        id: s.scenario_id,
        title: s.title,
        horizon: s.horizon,
        risk_level: s.risk_level,
        confidence: s.confidence,
        drivers: s.drivers,
        recommendations: s.recommendations,
        explainability: s.explainability,
        scenario_type: s.scenario_type
      }))
      setScenarios(mappedScenarios)
    } catch (error) {
      console.error('Błąd przeliczania:', error)
    }
  }

  const handleSwipeStart = (e: React.TouchEvent | React.MouseEvent) => {
    const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX
    startX.current = clientX
    isDragging.current = true
  }

  const handleSwipeMove = (e: React.TouchEvent | React.MouseEvent) => {
    if (!isDragging.current) return
    const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX
    currentX.current = clientX - startX.current
    
    if (cardRef.current) {
      cardRef.current.style.transform = `translateX(${currentX.current}px) rotate(${currentX.current * 0.1}deg)`
      cardRef.current.style.opacity = `${1 - Math.abs(currentX.current) / 300}`
    }
  }

  const handleSwipeEnd = () => {
    if (!isDragging.current) return
    isDragging.current = false

    const threshold = 100
    if (Math.abs(currentX.current) > threshold) {
      if (currentX.current > 0) {
        handleAccept()
      } else {
        handleReject()
      }
    } else {
      // Reset position
      if (cardRef.current) {
        cardRef.current.style.transform = ''
        cardRef.current.style.opacity = ''
      }
    }
    currentX.current = 0
  }

  const handleAccept = async () => {
    if (scenarios.length === 0) return
    const scenario = scenarios[currentIndex]
    try {
      await acceptScenario(scenario.id)
      moveToNext()
    } catch (error) {
      console.error('Błąd akceptacji:', error)
    }
  }

  const handleReject = async () => {
    if (scenarios.length === 0) return
    const scenario = scenarios[currentIndex]
    try {
      await rejectScenario(scenario.id)
      moveToNext()
    } catch (error) {
      console.error('Błąd odrzucenia:', error)
    }
  }

  const moveToNext = () => {
    if (currentIndex < scenarios.length - 1) {
      setCurrentIndex(currentIndex + 1)
      setIsExpanded(false)
    } else {
      // All scenarios processed, reload
      loadScenarios()
    }
  }

  const handleCardTap = () => {
    setIsExpanded(!isExpanded)
  }

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'LOW': return '#10b981' // green
      case 'MEDIUM': return '#f59e0b' // amber
      case 'HIGH': return '#ef4444' // red
      default: return '#6b7280'
    }
  }

  if (loading || isStreaming) {
    return (
      <div className="scenarios-loading">
        <div className="loading-spinner"></div>
        <p>{isStreaming ? 'Analiza w toku...' : 'Ładowanie scenariuszy...'}</p>
        {currentStep && (
          <div style={{ marginTop: '1rem', textAlign: 'center' }}>
            <div style={{ 
              fontSize: '0.875rem', 
              color: 'rgba(255, 255, 255, 0.7)',
              marginBottom: '0.5rem'
            }}>
              {currentStep.name}
            </div>
            <div style={{
              width: '300px',
              height: '4px',
              background: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '2px',
              margin: '0 auto',
              overflow: 'hidden'
            }}>
              <div style={{
                width: `${currentStep.progress}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #ffc107, #ff9800)',
                transition: 'width 0.3s ease',
                borderRadius: '2px'
              }} />
            </div>
            <div style={{
              fontSize: '0.75rem',
              color: 'rgba(255, 255, 255, 0.5)',
              marginTop: '0.5rem'
            }}>
              {currentStep.progress}%
            </div>
          </div>
        )}
      </div>
    )
  }

  if (scenarios.length === 0) {
    return (
      <div className="scenarios-empty">
        <p>Brak dostępnych scenariuszy</p>
        <button onClick={loadScenarios}>Załaduj ponownie</button>
      </div>
    )
  }

  const currentScenario = scenarios[currentIndex]

  return (
    <div className="scenarios-container">
      {/* Header */}
      <div className="scenarios-header">
        <div>
          <h1>Scenariusze Jutra</h1>
          <p className="subtitle">Decision support for long-term international policy</p>
        </div>
        <div className="status-indicator">
          <span className="status-dot"></span>
          Explainability enabled • Anti-data-poisoning active
        </div>
      </div>

      {/* Card Stack */}
      <div className="cards-stack-container">
        <div
          ref={cardRef}
          className={`scenario-card ${isExpanded ? 'expanded' : ''}`}
          onClick={handleCardTap}
          onTouchStart={handleSwipeStart}
          onTouchMove={handleSwipeMove}
          onTouchEnd={handleSwipeEnd}
          onMouseDown={handleSwipeStart}
          onMouseMove={handleSwipeMove}
          onMouseUp={handleSwipeEnd}
          onMouseLeave={handleSwipeEnd}
        >
          <div className="card-header">
            <div className="card-badges">
              <span className="horizon-badge">{currentScenario.horizon}</span>
              <span 
                className="risk-badge"
                style={{ backgroundColor: getRiskColor(currentScenario.risk_level) }}
              >
                {currentScenario.risk_level}
              </span>
            </div>
            <div className="confidence-score">
              Confidence: {Math.round(currentScenario.confidence * 100)}%
            </div>
          </div>

          <h2 className="card-title">{currentScenario.title}</h2>

          {!isExpanded ? (
            <>
              <div className="card-drivers">
                <h3>Key Drivers:</h3>
                <ul>
                  {currentScenario.drivers.map((driver, idx) => (
                    <li key={idx}>{driver}</li>
                  ))}
                </ul>
              </div>

              <div className="card-hint">
                Swipe RIGHT to accept • Swipe LEFT to reject • Tap to expand
              </div>
            </>
          ) : (
            <div className="card-details">
              <div className="explainability-section">
                <h3>Key Factors</h3>
                <div className="factors-list">
                  {currentScenario.explainability.key_factors.map((factor, idx) => (
                    <div key={idx} className="factor-item">
                      <span className="factor-name">{factor.factor}</span>
                      <div className="factor-weight">
                        <div 
                          className="weight-bar"
                          style={{ width: `${factor.weight * 100}%` }}
                        ></div>
                        <span>{Math.round(factor.weight * 100)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="logic-summary">
                <h3>Reasoning</h3>
                <p>{currentScenario.explainability.logic_summary}</p>
              </div>

              <div className="recommendations-section">
                <h3>Recommendations</h3>
                <ul>
                  {currentScenario.recommendations.map((rec, idx) => (
                    <li key={idx}>{rec}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>

        {/* Stack indicators */}
        <div className="stack-indicators">
          {scenarios.slice(currentIndex, currentIndex + 3).map((_, idx) => (
            <div 
              key={idx} 
              className={`stack-dot ${idx === 0 ? 'active' : ''}`}
            ></div>
          ))}
        </div>
      </div>

      {/* What If Panel */}
      <div className="what-if-panel">
        <h3>What If Analysis</h3>
        <div className="sliders-container">
          <div className="slider-group">
            <label>Energy Market Instability</label>
            <input
              type="range"
              min="0"
              max="100"
              value={whatIfValues.energy}
              onChange={(e) => setWhatIfValues({...whatIfValues, energy: parseInt(e.target.value)})}
              className="what-if-slider"
            />
            <span className="slider-value">{whatIfValues.energy}%</span>
          </div>

          <div className="slider-group">
            <label>Geopolitical Conflict Escalation</label>
            <input
              type="range"
              min="0"
              max="100"
              value={whatIfValues.conflict}
              onChange={(e) => setWhatIfValues({...whatIfValues, conflict: parseInt(e.target.value)})}
              className="what-if-slider"
            />
            <span className="slider-value">{whatIfValues.conflict}%</span>
          </div>

          <div className="slider-group">
            <label>Foreign Investment Flow</label>
            <input
              type="range"
              min="0"
              max="100"
              value={whatIfValues.investment}
              onChange={(e) => setWhatIfValues({...whatIfValues, investment: parseInt(e.target.value)})}
              className="what-if-slider"
            />
            <span className="slider-value">{whatIfValues.investment}%</span>
          </div>
        </div>
      </div>

      {/* Recommendations Panel */}
      <div className="recommendations-panel">
        <h3>Strategic Recommendations</h3>
        <div className="recommendation-cards">
          {currentScenario.recommendations.map((rec, idx) => (
            <div 
              key={idx} 
              className="recommendation-card"
              onClick={() => {
                // Animate impact on scenario
                if (cardRef.current) {
                  cardRef.current.classList.add('impact-animation')
                  setTimeout(() => {
                    cardRef.current?.classList.remove('impact-animation')
                  }, 1000)
                }
              }}
            >
              {rec}
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="scenarios-footer">
        <p>Human-in-the-loop • Scenario-based modeling • Explainable AI reasoning</p>
      </div>
    </div>
  )
}

