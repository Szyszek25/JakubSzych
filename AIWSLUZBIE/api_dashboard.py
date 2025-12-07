"""
🚀 API Dashboard dla Asystenta AI - Backend
FastAPI endpointy dla dashboardu React
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import os
import sys
from pydantic import BaseModel

# Dodaj ścieżkę do system/
_current_dir = os.path.dirname(os.path.abspath(__file__))
_system_dir = os.path.join(os.path.dirname(_current_dir), 'system')
if _system_dir not in sys.path:
    sys.path.insert(0, _system_dir)

# Import asystenta
try:
    from asystent_ai_gqpa_integrated import (
        HAMAAdministrativeAssistant,
        GeminiCognitiveAdapter,
        AdministrativeCase,
        create_demo_assistant
    )
    ASSISTANT_AVAILABLE = True
except ImportError as e:
    ASSISTANT_AVAILABLE = False
    print(f"⚠️ Nie można załadować asystenta: {e}")

app = FastAPI(
    title="Asystent AI Dashboard API",
    description="API dla dashboardu Asystenta AI dla Administracji",
    version="1.0.0"
)

# CORS - pozwól na połączenia z React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Globalna instancja asystenta
assistant_instance: Optional[HAMAAdministrativeAssistant] = None

def get_assistant() -> HAMAAdministrativeAssistant:
    """Pobierz lub utwórz instancję asystenta"""
    global assistant_instance
    if assistant_instance is None:
        if ASSISTANT_AVAILABLE:
            adapter = GeminiCognitiveAdapter(None, use_local_model=True)
            assistant_instance = HAMAAdministrativeAssistant(adapter)
        else:
            raise HTTPException(status_code=503, detail="Asystent nie jest dostępny")
    return assistant_instance

# ============================================================================
# MODELE PYDANTIC
# ============================================================================

class CaseCreate(BaseModel):
    case_id: str
    case_type: str
    documents: List[Dict[str, Any]]
    parties: List[str]
    status: str
    deadline: Optional[str] = None

class CaseSummary(BaseModel):
    case_id: str
    type: str
    status: str
    parties: List[str]
    deadline: Optional[str]
    summary: Optional[str]
    risk_assessment: Optional[Dict]
    legal_issues: List[str]
    compliance_score: float
    created_at: str
    updated_at: str

# ============================================================================
# ENDPOINTY API
# ============================================================================

@app.get("/")
async def root():
    """Status API"""
    return {
        "status": "ok",
        "service": "Asystent AI Dashboard API",
        "version": "1.0.0",
        "assistant_available": ASSISTANT_AVAILABLE
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        assistant = get_assistant()
        return {
            "status": "healthy",
            "assistant_loaded": assistant is not None,
            "hama_info": assistant.hama_info if assistant else None,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Główne statystyki dashboardu"""
    try:
        assistant = get_assistant()
        
        # Statystyki spraw
        total_cases = len(assistant.cases)
        cases_by_status = {}
        cases_by_type = {}
        cases_by_risk = {"niski": 0, "średni": 0, "wysoki": 0, "krytyczny": 0}
        
        for case in assistant.cases.values():
            # Status
            status = case.status
            cases_by_status[status] = cases_by_status.get(status, 0) + 1
            
            # Typ
            case_type = case.case_type
            cases_by_type[case_type] = cases_by_type.get(case_type, 0) + 1
            
            # Ryzyko
            if case.risk_assessment:
                risk_level = case.risk_assessment.get("level", "średni")
                cases_by_risk[risk_level] = cases_by_risk.get(risk_level, 0) + 1
        
        # Metryki wydajności
        metrics = assistant.get_performance_metrics()
        
        # Terminy
        upcoming_deadlines = assistant.check_deadlines(days_ahead=30)
        critical_deadlines = [d for d in upcoming_deadlines if d.get('priority') == 'krytyczny']
        
        # Truth Guardian stats
        truth_guardian_stats = {
            "total_verifications": getattr(assistant.cognitive_agent.environment, 'post_id', 0) if hasattr(assistant.cognitive_agent, 'environment') and hasattr(assistant.cognitive_agent.environment, 'post_id') else 0,
            "fake_detected": 0,  # TODO: track this
            "verified": 0
        }
        
        return {
            "summary": {
                "total_cases": total_cases,
                "total_analyses": metrics.get('total_analyses', 0),
                "avg_analysis_time": round(metrics.get('avg_analysis_time', 0), 2),
                "avg_decision_time": round(metrics.get('avg_decision_generation_time', 0), 2),
                "upcoming_deadlines": len(upcoming_deadlines),
                "critical_deadlines": len(critical_deadlines)
            },
            "cases_by_status": cases_by_status,
            "cases_by_type": cases_by_type,
            "cases_by_risk": cases_by_risk,
            "performance_metrics": metrics,
            "deadlines": {
                "upcoming": upcoming_deadlines[:10],  # Top 10
                "critical": critical_deadlines
            },
            "truth_guardian": truth_guardian_stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania statystyk: {str(e)}")

@app.get("/api/cases")
async def get_cases():
    """Lista wszystkich spraw"""
    try:
        assistant = get_assistant()
        cases_list = []
        
        for case_id, case in assistant.cases.items():
            cases_list.append({
                "case_id": case.case_id,
                "type": case.case_type,
                "status": case.status,
                "parties": case.parties,
                "deadline": case.deadline.isoformat() if case.deadline else None,
                "summary": case.summary[:200] if case.summary else None,
                "risk_level": case.risk_assessment.get("level") if case.risk_assessment else "średni",
                "compliance_score": case.compliance_score,
                "created_at": case.created_at.isoformat(),
                "updated_at": case.updated_at.isoformat()
            })
        
        return {
            "cases": cases_list,
            "total": len(cases_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania spraw: {str(e)}")

@app.get("/api/cases/{case_id}")
async def get_case_detail(case_id: str):
    """Szczegóły konkretnej sprawy"""
    try:
        assistant = get_assistant()
        summary = assistant.get_case_summary(case_id)
        
        if not summary:
            raise HTTPException(status_code=404, detail=f"Sprawa {case_id} nie istnieje")
        
        return summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania sprawy: {str(e)}")

@app.post("/api/cases")
async def create_case(case_data: CaseCreate):
    """Utworzenie nowej sprawy"""
    try:
        assistant = get_assistant()
        
        deadline = None
        if case_data.deadline:
            deadline = datetime.fromisoformat(case_data.deadline)
        
        case = AdministrativeCase(
            case_id=case_data.case_id,
            case_type=case_data.case_type,
            documents=case_data.documents,
            parties=case_data.parties,
            status=case_data.status,
            deadline=deadline
        )
        
        success = assistant.add_case(case)
        
        if success:
            return {
                "success": True,
                "case_id": case.case_id,
                "message": f"Sprawa {case.case_id} została dodana"
            }
        else:
            raise HTTPException(status_code=400, detail="Nie udało się dodać sprawy")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd tworzenia sprawy: {str(e)}")

@app.post("/api/cases/{case_id}/analyze")
async def analyze_case(case_id: str):
    """Analiza sprawy"""
    try:
        assistant = get_assistant()
        analysis = assistant.analyze_case(case_id)
        
        if "error" in analysis:
            raise HTTPException(status_code=404, detail=analysis["error"])
        
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd analizy sprawy: {str(e)}")

@app.post("/api/cases/{case_id}/generate-decision")
async def generate_decision(case_id: str, decision_type: str = "pozytywna"):
    """Generowanie projektu decyzji"""
    try:
        assistant = get_assistant()
        draft = assistant.generate_decision_draft(case_id, decision_type)
        
        return {
            "case_id": draft.case_id,
            "decision_type": draft.decision_type,
            "factual_justification": draft.factual_justification,
            "legal_justification": draft.legal_justification,
            "decision_text": draft.decision_text,
            "legal_references": draft.legal_references,
            "compliance_checks": draft.compliance_checks,
            "generated_at": draft.generated_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd generowania decyzji: {str(e)}")

@app.get("/api/performance")
async def get_performance_metrics():
    """Metryki wydajności"""
    try:
        assistant = get_assistant()
        metrics = assistant.get_performance_metrics()
        
        # Dodatkowe metryki
        total_cases = len(assistant.cases)
        cases_with_decisions = sum(1 for c in assistant.cases.values() if c.decision_proposal)
        
        return {
            **metrics,
            "total_cases": total_cases,
            "cases_with_decisions": cases_with_decisions,
            "decision_rate": round(cases_with_decisions / total_cases * 100, 2) if total_cases > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania metryk: {str(e)}")

@app.get("/api/deadlines")
async def get_deadlines(days_ahead: int = 30):
    """Lista zbliżających się terminów"""
    try:
        assistant = get_assistant()
        deadlines = assistant.check_deadlines(days_ahead=days_ahead)
        
        return {
            "deadlines": deadlines,
            "total": len(deadlines),
            "days_ahead": days_ahead
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania terminów: {str(e)}")

@app.get("/api/audit-log")
async def get_audit_log(limit: int = 50):
    """Audit log"""
    try:
        assistant = get_assistant()
        log = assistant.export_audit_log()
        
        return {
            "log": log[-limit:],  # Ostatnie N wpisów
            "total": len(log)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania audit log: {str(e)}")

@app.post("/api/demo/init")
async def init_demo_data():
    """Inicjalizacja danych demo - dodaje przykładowe sprawy"""
    try:
        assistant = get_assistant()
        
        # Sprawdź czy już są dane
        if len(assistant.cases) > 0:
            return {
                "message": "Dane demo już istnieją",
                "existing_cases": len(assistant.cases),
                "skipped": True
            }
        
        # Przykładowe sprawy
        demo_cases = [
            AdministrativeCase(
                case_id="SPR-2024-001",
                case_type="kwalifikacja_zawodowa",
                documents=[
                    {
                        "type": "wniosek",
                        "content": "Wniosek o nadanie kwalifikacji przewodnika turystycznego. Wnioskodawca: Jan Kowalski, posiada dyplom ukończenia studiów turystycznych na Uniwersytecie Warszawskim."
                    },
                    {
                        "type": "dyplom",
                        "content": "Dyplom ukończenia studiów wyższych - kierunek: Turystyka i Rekreacja, Uniwersytet Warszawski, rok 2020."
                    }
                ],
                parties=["Jan Kowalski", "Departament Turystyki MSiT"],
                status="w_trakcie",
                deadline=datetime.now() + timedelta(days=15)
            ),
            AdministrativeCase(
                case_id="SPR-2024-002",
                case_type="kategoria_hotelu",
                documents=[
                    {
                        "type": "wniosek",
                        "content": "Wniosek o nadanie kategorii hotelowi 'Grand Hotel' w Warszawie. Obiekt posiada 150 pokoi, restaurację, centrum fitness."
                    },
                    {
                        "type": "dokumentacja_techniczna",
                        "content": "Dokumentacja techniczna obiektu, standardy pokoi, wyposażenie, certyfikaty bezpieczeństwa."
                    }
                ],
                parties=["Grand Hotel Sp. z o.o.", "Departament Turystyki MSiT"],
                status="oczekuje_decyzji",
                deadline=datetime.now() + timedelta(days=5)
            ),
            AdministrativeCase(
                case_id="SPR-2024-003",
                case_type="zakaz_dzialalnosci",
                documents=[
                    {
                        "type": "wniosek",
                        "content": "Wniosek o zakaz prowadzenia działalności gospodarczej w zakresie usług turystycznych. Podstawa: wielokrotne naruszenia przepisów."
                    },
                    {
                        "type": "dokumentacja_naruszen",
                        "content": "Protokoły kontroli, dokumentacja naruszeń przepisów ustawy o usługach turystycznych."
                    }
                ],
                parties=["ABC Biuro Podróży", "Departament Turystyki MSiT"],
                status="w_trakcie",
                deadline=datetime.now() + timedelta(days=45)
            ),
            AdministrativeCase(
                case_id="SPR-2024-004",
                case_type="kwalifikacja_zawodowa",
                documents=[
                    {
                        "type": "wniosek",
                        "content": "Wniosek o nadanie kwalifikacji pilota wycieczek. Wnioskodawca: Anna Nowak, posiada certyfikat ukończenia kursu pilotażu."
                    }
                ],
                parties=["Anna Nowak", "Departament Turystyki MSiT"],
                status="nowa",
                deadline=datetime.now() + timedelta(days=25)
            ),
            AdministrativeCase(
                case_id="SPR-2024-005",
                case_type="kategoria_hotelu",
                documents=[
                    {
                        "type": "wniosek",
                        "content": "Wniosek o podwyższenie kategorii hotelu 'Seaside Resort' w Gdańsku z 3 do 4 gwiazdek."
                    }
                ],
                parties=["Seaside Resort Sp. z o.o.", "Departament Turystyki MSiT"],
                status="zakończona",
                deadline=datetime.now() - timedelta(days=10)
            )
        ]
        
        # Dodaj sprawy
        added = 0
        for case in demo_cases:
            if assistant.add_case(case):
                added += 1
        
        return {
            "message": f"Dodano {added} przykładowych spraw",
            "cases_added": added,
            "total_cases": len(assistant.cases)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd inicjalizacji danych demo: {str(e)}")

@app.get("/api/system/status")
async def get_system_status():
    """Status systemu"""
    try:
        assistant = get_assistant()
        
        # Status Gemini
        gemini_status = "unknown"
        if hasattr(assistant.adapter, 'local_adapter') and assistant.adapter.local_adapter:
            gemini_status = "available" if assistant.adapter.local_adapter.is_available() else "unavailable"
        
        return {
            "hama": {
                "available": assistant.hama_info is not None,
                "info": assistant.hama_info
            },
            "gemini": {
                "status": gemini_status,
                "using_api": assistant.adapter.use_local_model,
                "available": assistant.adapter.gemini is not None or (assistant.adapter.local_adapter and assistant.adapter.local_adapter.is_available())
            },
            "guardrails": {
                "enabled": True,
                "audit_log_size": len(assistant.guardrails.audit_log)
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania statusu: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Uruchamianie API Dashboard...")
    print("📡 API dostępne na: http://localhost:8000")
    print("📚 Dokumentacja: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

