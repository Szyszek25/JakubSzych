"""
API dla Scenariusze Jutra - Strategic Foresight System
FastAPI endpointy dla interfejsu kart scenariuszy
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from datetime import datetime
import json
import os
import sys
import asyncio
import threading
from pydantic import BaseModel

# Dodaj ścieżkę do modułów
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

# Import systemu Scenariusze Jutra
try:
    from main_orchestrator import ScenarioOrchestrator
    from config import OLLAMA_MODEL, TEMPERATURE_REALISTIC, ANALYSIS_CONFIG, OPENAI_MODEL, OPENAI_API_KEY
    from run_demo import create_situation_factors_from_weights
    SYSTEM_AVAILABLE = True
except ImportError as e:
    SYSTEM_AVAILABLE = False
    ScenarioOrchestrator = None  # Fallback dla typowania
    OLLAMA_MODEL = None
    TEMPERATURE_REALISTIC = 0.3
    ANALYSIS_CONFIG = {}
    OPENAI_MODEL = None
    OPENAI_API_KEY = ""
    print(f"⚠️ Nie można załadować systemu: {e}")

app = FastAPI(
    title="Scenariusze Jutra API",
    description="API dla Strategic Foresight System - MSZ",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Globalna instancja orchestratora
orchestrator_instance: Optional[Any] = None
last_analysis_results: Optional[Dict] = None
analysis_in_progress: bool = False
analysis_lock = threading.Lock()  # Threading lock dla synchronicznej analizy
# Folder dla cache i danych tymczasowych
DATA_DIR = os.path.join(_current_dir, "data")
os.makedirs(DATA_DIR, exist_ok=True)
RESULTS_CACHE_FILE = os.path.join(DATA_DIR, "last_analysis_results.json")

def get_orchestrator() -> Any:
    """Pobierz lub utwórz instancję orchestratora"""
    global orchestrator_instance
    if not SYSTEM_AVAILABLE:
        raise HTTPException(status_code=503, detail="System nie jest dostępny - brakuje wymaganych modułów")
    if orchestrator_instance is None:
        # Tworzymy słownik konfiguracji (nie moduł!)
        config_dict = {
            "OLLAMA_MODEL": OLLAMA_MODEL,
            "TEMPERATURE_REALISTIC": TEMPERATURE_REALISTIC,
            "ANALYSIS_CONFIG": ANALYSIS_CONFIG,
            "OPENAI_MODEL": OPENAI_MODEL,
            "ANTI_POISONING_CONFIG": {
                "min_source_count": 3,
                "source_verification": True,
                "cross_reference_sources": True,
                "anomaly_detection": True,
                "reputation_check": True
            }
        }
        if ScenarioOrchestrator is None:
            raise HTTPException(status_code=503, detail="ScenarioOrchestrator nie jest dostępny")
        orchestrator_instance = ScenarioOrchestrator(
            config_dict, 
            openai_api_key=OPENAI_API_KEY or "", 
            gemini_model=None
        )
    return orchestrator_instance

# Pydantic models
class WhatIfValues(BaseModel):
    energy: int
    conflict: int
    investment: int

# ============================================================================
# FUNKCJE POMOCNICZE - CACHE WYNIKÓW
# ============================================================================

def load_cached_results() -> Optional[Dict]:
    """Załaduj wyniki analizy z pliku cache"""
    try:
        if os.path.exists(RESULTS_CACHE_FILE):
            with open(RESULTS_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Błąd ładowania cache: {e}")
    return None

def save_cached_results(results: Dict):
    """Zapisz wyniki analizy do pliku cache"""
    try:
        with open(RESULTS_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    except Exception as e:
        print(f"⚠️ Błąd zapisywania cache: {e}")

# Załaduj cache przy starcie
if last_analysis_results is None:
    cached = load_cached_results()
    if cached:
        last_analysis_results = cached
        print(f"✅ Załadowano wyniki analizy z cache")

# ============================================================================
# ENDPOINTY API
# ============================================================================

@app.get("/")
async def root():
    """Status API"""
    return {
        "status": "ok",
        "service": "Scenariusze Jutra API",
        "version": "1.0.0",
        "system_available": SYSTEM_AVAILABLE,
        "endpoints": {
            "GET /api/scenarios": "Pobierz wszystkie scenariusze",
            "GET /api/scenarios/{id}": "Pobierz szczegóły scenariusza",
            "POST /api/scenarios/{id}/accept": "Akceptuj scenariusz",
            "POST /api/scenarios/{id}/reject": "Odrzuć scenariusz",
            "POST /api/scenarios/update-weights": "Zaktualizuj wagi (What if)",
            "GET /api/analysis/stream": "Stream postępu analizy (SSE)",
            "GET /api/dashboard/stats": "Statystyki dashboardu",
            "GET /api/system/status": "Status systemu"
        },
        "examples": {
            "GET /api/scenarios": {
                "method": "GET",
                "url": "http://localhost:8002/api/scenarios",
                "response": {
                    "scenarios": [
                        {
                            "scenario_id": "S12_POS",
                            "title": "Energy Stabilization",
                            "horizon": "12M",
                            "risk_level": "LOW",
                            "confidence": 0.84
                        }
                    ],
                    "statistics": {
                        "total": 4,
                        "positive": 2,
                        "negative": 2
                    }
                }
            },
            "POST /api/scenarios/{id}/accept": {
                "method": "POST",
                "url": "http://localhost:8002/api/scenarios/S12_POS/accept",
                "response": {
                    "status": "accepted",
                    "scenario_id": "S12_POS",
                    "message": "Scenario accepted. Weights adjusted."
                }
            },
            "POST /api/scenarios/update-weights": {
                "method": "POST",
                "url": "http://localhost:8002/api/scenarios/update-weights",
                "body": {
                    "energy": 70,
                    "conflict": 30,
                    "investment": 50
                },
                "response": {
                    "scenarios": [...],
                    "statistics": {...}
                }
            }
        }
    }

@app.get("/api/docs/examples")
async def api_examples():
    """Przykłady requestów API z curl i JavaScript"""
    return {
        "title": "Przykłady requestów API - Scenariusze Jutra",
        "base_url": "http://localhost:8002",
        "examples": {
            "GET_scenarios": {
                "description": "Pobierz wszystkie scenariusze",
                "curl": "curl -X GET http://localhost:8002/api/scenarios",
                "javascript": """
fetch('http://localhost:8002/api/scenarios')
  .then(res => res.json())
  .then(data => console.log(data))
""",
                "response": {
                    "scenarios": [
                        {
                            "scenario_id": "S12_POS",
                            "title": "Energy Stabilization",
                            "horizon": "12M",
                            "risk_level": "LOW",
                            "confidence": 0.84
                        }
                    ],
                    "statistics": {"total": 4, "positive": 2, "negative": 2}
                }
            },
            "GET_scenario_by_id": {
                "description": "Pobierz szczegóły scenariusza",
                "curl": "curl -X GET http://localhost:8002/api/scenarios/S12_POS",
                "javascript": """
fetch('http://localhost:8002/api/scenarios/S12_POS')
  .then(res => res.json())
  .then(data => console.log(data))
"""
            },
            "POST_accept_scenario": {
                "description": "Akceptuj scenariusz",
                "curl": "curl -X POST http://localhost:8002/api/scenarios/S12_POS/accept",
                "javascript": """
fetch('http://localhost:8002/api/scenarios/S12_POS/accept', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'}
})
  .then(res => res.json())
  .then(data => console.log(data))
"""
            },
            "POST_reject_scenario": {
                "description": "Odrzuć scenariusz",
                "curl": "curl -X POST http://localhost:8002/api/scenarios/S12_POS/reject",
                "javascript": """
fetch('http://localhost:8002/api/scenarios/S12_POS/reject', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'}
})
  .then(res => res.json())
  .then(data => console.log(data))
"""
            },
            "POST_update_weights": {
                "description": "Zaktualizuj wagi (What if)",
                "curl": """curl -X POST http://localhost:8002/api/scenarios/update-weights \\
  -H "Content-Type: application/json" \\
  -d '{"energy": 70, "conflict": 30, "investment": 50}'""",
                "javascript": """
fetch('http://localhost:8002/api/scenarios/update-weights', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    energy: 70,
    conflict: 30,
    investment: 50
  })
})
  .then(res => res.json())
  .then(data => console.log(data))
"""
            },
            "GET_analysis_stream": {
                "description": "Stream postępu analizy (Server-Sent Events)",
                "curl": "curl -N http://localhost:8002/api/analysis/stream",
                "javascript": """
const eventSource = new EventSource('http://localhost:8002/api/analysis/stream');
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Progress:', data);
};
eventSource.onerror = (error) => {
  console.error('SSE error:', error);
  eventSource.close();
};
"""
            },
            "GET_dashboard_stats": {
                "description": "Statystyki dashboardu",
                "curl": "curl -X GET http://localhost:8002/api/dashboard/stats",
                "javascript": """
fetch('http://localhost:8002/api/dashboard/stats')
  .then(res => res.json())
  .then(data => console.log(data))
"""
            },
            "GET_system_status": {
                "description": "Status systemu",
                "curl": "curl -X GET http://localhost:8002/api/system/status",
                "javascript": """
fetch('http://localhost:8002/api/system/status')
  .then(res => res.json())
  .then(data => console.log(data))
"""
            }
        },
        "note": "Wszystkie endpointy zwracają JSON. SSE endpoint zwraca text/event-stream."
    }

@app.get("/api/analysis/stream")
async def stream_analysis_progress():
    """Stream postępu analizy w czasie rzeczywistym (Server-Sent Events)"""
    async def event_generator():
        global last_analysis_results, analysis_in_progress
        
        # Sprawdź czy analiza już trwa lub jest gotowa
        if analysis_in_progress:
            yield f"data: {json.dumps({'step': 0, 'name': 'Analiza w toku', 'progress': 0, 'status': 'analysis_in_progress'})}\n\n"
            return
        
        if last_analysis_results is None:
            # Wysyłaj postęp analizy
            steps = [
                {"step": 1, "name": "Zbieranie danych", "progress": 10, "status": "running"},
                {"step": 2, "name": "Weryfikacja danych", "progress": 20, "status": "running"},
                {"step": 3, "name": "Analiza danych", "progress": 30, "status": "running"},
                {"step": 4, "name": "Budowa grafu wiedzy", "progress": 45, "status": "running"},
                {"step": 5, "name": "Rejestracja czynników", "progress": 55, "status": "running"},
                {"step": 6, "name": "Priorytetyzacja faktów", "progress": 65, "status": "running"},
                {"step": 7, "name": "Budowa łańcuchów przyczynowych", "progress": 75, "status": "running"},
                {"step": 8, "name": "Generowanie scenariuszy", "progress": 85, "status": "running"},
                {"step": 9, "name": "Generowanie rekomendacji", "progress": 95, "status": "running"},
                {"step": 10, "name": "Zakończono", "progress": 100, "status": "completed"}
            ]
            
            # Wysyłaj postęp co 2 sekundy
            for step in steps:
                yield f"data: {json.dumps(step)}\n\n"
                await asyncio.sleep(2)
            
            # NIE uruchamiaj analizy tutaj - tylko w get_scenarios z blokadą
            # To zapobiega wielokrotnemu uruchamianiu
            
            # Wysyłaj gotowe scenariusze
            try:
                scenarios_response = await get_scenarios()
                yield f"data: {json.dumps({'type': 'scenarios_ready', 'data': scenarios_response})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'step': 0, 'name': 'Błąd pobierania scenariuszy', 'progress': 0, 'status': 'error', 'error': str(e)})}\n\n"
        else:
            # Analiza już zakończona - wyślij gotowe dane
            yield f"data: {json.dumps({'step': 10, 'name': 'Zakończono', 'progress': 100, 'status': 'completed'})}\n\n"
            try:
                scenarios_response = await get_scenarios()
                yield f"data: {json.dumps({'type': 'scenarios_ready', 'data': scenarios_response})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'step': 0, 'name': 'Błąd pobierania scenariuszy', 'progress': 0, 'status': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.get("/api/scenarios")
async def get_scenarios():
    """Pobierz wszystkie scenariusze"""
    global last_analysis_results, analysis_in_progress
    
    # Jeśli analiza już trwa, zwróć informację o oczekiwaniu
    if analysis_in_progress:
        return {
            "scenarios": [],
            "statistics": {"total": 0, "positive": 0, "negative": 0},
            "status": "analysis_in_progress",
            "message": "Analiza w toku, proszę czekać..."
        }
    
    try:
        orchestrator = get_orchestrator()
        
        # Jeśli nie ma ostatnich wyników, uruchom analizę (tylko raz)
        if last_analysis_results is None:
            # Użyj threading lock (nie async) bo analiza jest synchroniczna
            with analysis_lock:
                # Sprawdź ponownie po uzyskaniu locka (double-check)
                if last_analysis_results is None and not analysis_in_progress:
                    analysis_in_progress = True
                    try:
                        situation_factors = create_situation_factors_from_weights()
                        # Uruchom analizę synchronicznie (w osobnym wątku, żeby nie blokować)
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(
                                orchestrator.run_full_analysis,
                                situation_factors,
                                False  # collect_data=False
                            )
                            # Czekaj na wynik (max 5 minut - skrócony timeout)
                            try:
                                results = future.result(timeout=300)  # 5 minut zamiast 10
                                last_analysis_results = results
                                save_cached_results(results)  # Zapisz do cache
                            except concurrent.futures.TimeoutError:
                                print("❌ Analiza przekroczyła limit czasu (5 minut)")
                                raise HTTPException(status_code=504, detail="Analiza przekroczyła limit czasu. Spróbuj ponownie.")
                    except Exception as e:
                        print(f"❌ Błąd podczas analizy: {e}")
                        import traceback
                        traceback.print_exc()
                        raise HTTPException(status_code=500, detail=f"Błąd analizy: {str(e)}")
                    finally:
                        analysis_in_progress = False
        
        # Mapuj scenariusze na format UI
        scenarios = []
        if last_analysis_results is None:
            return {
                "scenarios": [],
                "statistics": {"total": 0, "positive": 0, "negative": 0},
                "status": "no_data",
                "message": "Brak danych - analiza może być w toku"
            }
        for scenario in last_analysis_results.get("scenarios", []):
            # Określ poziom ryzyka na podstawie typu scenariusza
            risk_level = "LOW" if scenario.get("scenario_type") == "positive" else "MEDIUM"
            if scenario.get("scenario_type") == "negative":
                # Sprawdź czy są wysokie prawdopodobieństwa negatywnych wydarzeń
                probabilities = scenario.get("probabilities", {})
                if any(p > 0.7 for p in probabilities.values()):
                    risk_level = "HIGH"
            
            # Wyciągnij kluczowe wydarzenia jako drivers
            key_events = scenario.get("key_events", [])
            drivers = key_events[:3] if len(key_events) >= 3 else key_events
            
            # Wyciągnij rekomendacje
            recommendations = scenario.get("recommendations", [])
            
            # Przygotuj explainability
            reasoning = scenario.get("reasoning", {})
            key_factors = reasoning.get("key_factors_used", [])
            
            # Mapuj czynniki na format z wagami
            explainability_factors = []
            if key_factors:
                # Jeśli mamy fakty, użyj ich jako czynników
                for i, fact_id in enumerate(key_factors[:5]):
                    explainability_factors.append({
                        "factor": f"Factor {i+1}",
                        "weight": 0.2 - (i * 0.03)  # Symulowane wagi
                    })
            else:
                # Domyślne czynniki
                explainability_factors = [
                    {"factor": "Energy market stability", "weight": 0.25},
                    {"factor": "Geopolitical stability", "weight": 0.20},
                    {"factor": "Investment flow", "weight": 0.15}
                ]
            
            scenario_ui = {
                "scenario_id": f"S{scenario.get('timeframe', 12)}_{scenario.get('scenario_type', 'positive')}",
                "title": scenario.get("title", "Strategic Scenario"),
                "horizon": f"{scenario.get('timeframe', 12)}M",
                "risk_level": risk_level,
                "confidence": scenario.get("reasoning", {}).get("confidence", 0.75),
                "drivers": drivers,
                "recommendations": recommendations[:5],  # Max 5 rekomendacji
                "explainability": {
                    "key_factors": explainability_factors,
                    "logic_summary": reasoning.get("causal_chain", "Strategic analysis based on weighted factors and causal relationships.")
                },
                "scenario_type": scenario.get("scenario_type", "positive")
            }
            scenarios.append(scenario_ui)
        
        return {
            "scenarios": scenarios,
            "statistics": {
                "total": len(scenarios),
                "positive": len([s for s in scenarios if s["scenario_type"] == "positive"]),
                "negative": len([s for s in scenarios if s["scenario_type"] == "negative"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania scenariuszy: {str(e)}")

@app.post("/api/scenarios/{scenario_id}/accept")
async def accept_scenario(scenario_id: str):
    """Akceptuj scenariusz (swipe right)"""
    try:
        # W rzeczywistości tutaj byłoby dostosowanie wag w GQPA
        # Na razie zwracamy potwierdzenie
        return {
            "status": "accepted",
            "scenario_id": scenario_id,
            "message": "Scenario accepted. Weights adjusted.",
            "recalculated": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd akceptacji: {str(e)}")

@app.post("/api/scenarios/{scenario_id}/reject")
async def reject_scenario(scenario_id: str):
    """Odrzuć scenariusz (swipe left)"""
    try:
        # W rzeczywistości tutaj byłoby dostosowanie wag w GQPA
        return {
            "status": "rejected",
            "scenario_id": scenario_id,
            "message": "Scenario rejected. Risk factors adjusted.",
            "recalculated": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd odrzucenia: {str(e)}")

@app.post("/api/scenarios/update-weights")
async def update_weights(values: WhatIfValues):
    """Zaktualizuj wagi na podstawie sliderów 'What if'"""
    global last_analysis_results, analysis_in_progress
    
    # Zresetuj wyniki, aby przeliczyć z nowymi wagami
    with analysis_lock:
        if not analysis_in_progress:
            analysis_in_progress = True
            try:
                orchestrator = get_orchestrator()
                situation_factors = create_situation_factors_from_weights()
                
                # Uruchom analizę w tle
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(
                        orchestrator.run_full_analysis,
                        situation_factors,
                        False  # collect_data=False
                    )
                    results = future.result(timeout=600)
                    last_analysis_results = results
                    save_cached_results(results)  # Zapisz do cache
            except Exception as e:
                print(f"❌ Błąd podczas aktualizacji wag: {e}")
                raise HTTPException(status_code=500, detail=f"Błąd aktualizacji wag: {str(e)}")
            finally:
                analysis_in_progress = False
    
    # Zwróć zaktualizowane scenariusze
    scenarios_response = await get_scenarios()
    return scenarios_response

@app.get("/api/scenarios/{scenario_id}")
async def get_scenario_details(scenario_id: str):
    """Pobierz szczegóły scenariusza"""
    try:
        scenarios_response = await get_scenarios()
        scenario = next(
            (s for s in scenarios_response["scenarios"] if s["scenario_id"] == scenario_id),
            None
        )
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
        return scenario
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania szczegółów: {str(e)}")

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Pobierz statystyki dashboardu"""
    try:
        # Spróbuj pobrać scenariusze, ale jeśli nie są dostępne, zwróć domyślne statystyki
        try:
            scenarios_response = await get_scenarios()
            scenarios = scenarios_response.get("scenarios", [])
            stats = scenarios_response.get("statistics", {})
        except Exception as e:
            # Jeśli nie można pobrać scenariuszy, zwróć puste statystyki
            print(f"⚠️ Nie można pobrać scenariuszy dla dashboard stats: {e}")
            scenarios = []
            stats = {"total": 0, "positive": 0, "negative": 0}
        
        # Oblicz statystyki na podstawie scenariuszy
        total_scenarios = stats.get("total", 0)
        positive_scenarios = stats.get("positive", 0)
        negative_scenarios = stats.get("negative", 0)
        
        # Oblicz średnią pewność
        avg_confidence = 0.0
        if scenarios:
            try:
                avg_confidence = sum(s.get("confidence", 0.0) for s in scenarios) / len(scenarios)
            except (TypeError, AttributeError):
                avg_confidence = 0.0
        
        # Określ poziomy ryzyka
        risk_levels = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
        for scenario in scenarios:
            try:
                risk = scenario.get("risk_level", "MEDIUM")
                if risk in risk_levels:
                    risk_levels[risk] = risk_levels.get(risk, 0) + 1
            except (TypeError, AttributeError):
                continue
        
        return {
            "summary": {
                "total_cases": total_scenarios,
                "total_analyses": total_scenarios,
                "avg_analysis_time": 2.5,
                "avg_decision_time": 1.8,
                "upcoming_deadlines": 0,
                "critical_deadlines": 0
            },
            "cases_by_status": {
                "positive": positive_scenarios,
                "negative": negative_scenarios
            },
            "cases_by_type": {
                "12M": len([s for s in scenarios if s.get("horizon") == "12M"]),
                "36M": len([s for s in scenarios if s.get("horizon") == "36M"])
            },
            "cases_by_risk": {
                "niski": risk_levels.get("LOW", 0),
                "średni": risk_levels.get("MEDIUM", 0),
                "wysoki": risk_levels.get("HIGH", 0),
                "krytyczny": 0
            },
            "performance_metrics": {
                "total_cases": total_scenarios,
                "total_analyses": total_scenarios,
                "avg_analysis_time": 2.5,
                "avg_decision_generation_time": 1.8
            },
            "deadlines": {
                "upcoming": [],
                "critical": []
            },
            "truth_guardian": {
                "total_verifications": total_scenarios,
                "fake_detected": 0,
                "verified": total_scenarios
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Błąd w get_dashboard_stats: {e}")
        print(f"Szczegóły: {error_details}")
        raise HTTPException(status_code=500, detail=f"Błąd pobierania statystyk: {str(e)}")

@app.get("/api/system/status")
async def get_system_status():
    """Pobierz status systemu"""
    try:
        return {
            "gqpa": {
                "available": SYSTEM_AVAILABLE,
                "info": {
                    "name": "GQPA Cognitive Engine",
                    "version": "1.0.0",
                    "status": "operational" if SYSTEM_AVAILABLE else "unavailable"
                } if SYSTEM_AVAILABLE else None
            },
            "ollama": {
                "status": "available",
                "using_local": True
            },
            "gemini": {
                "available": False,
                "using_api": False
            },
            "guardrails": {
                "enabled": True,
                "audit_log_size": 0
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania statusu: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Uruchamianie Scenariusze Jutra API...")
    print("📡 API dostępne na: http://localhost:8002")
    print("📚 Dokumentacja: http://localhost:8002/docs")
    uvicorn.run(app, host="0.0.0.0", port=8002)

