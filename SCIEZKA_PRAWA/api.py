"""
Ścieżka Prawa (GQPA Legislative Navigator) - FastAPI Backend
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uvicorn

from config import API_CONFIG
from legislative_tracker import (
    LegislativeTracker, LegislativeDocument, LegislativeStatus
)
from plain_language_engine import PlainLanguageEngine
from impact_simulator import ImpactSimulator, ImpactType
from democratic_interface import (
    DemocraticInterface, Consultation, CitizenProfile
)
from transparency_hub import TransparencyHub

# Inicjalizacja FastAPI
app = FastAPI(
    title=API_CONFIG["title"],
    version=API_CONFIG["version"],
    description=API_CONFIG["description"]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji ograniczyć do konkretnych domen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicjalizacja modułów
tracker = LegislativeTracker()
plain_language = PlainLanguageEngine()
impact_simulator = ImpactSimulator()
democratic_interface = DemocraticInterface()
transparency_hub = TransparencyHub()


# ============================================================================
# MODELE PYDANTIC
# ============================================================================

class DocumentCreate(BaseModel):
    title: str
    description: str
    status: str = "prekonsultacje"
    dependencies: List[str] = []
    metadata: Dict[str, Any] = {}


class StatusUpdate(BaseModel):
    status: str
    stage: Optional[str] = None


class ConsultationCreate(BaseModel):
    title: str
    description: str
    start_date: str
    end_date: str
    document_id: str


class SimplifyRequest(BaseModel):
    text: str
    use_llm: bool = False


class ImpactAnalysisRequest(BaseModel):
    document_text: str
    impact_types: Optional[List[str]] = None


# ============================================================================
# ENDPOINTY - LEGISLATIVE TRACKER
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Ścieżka Prawa (GQPA Legislative Navigator)",
        "version": API_CONFIG["version"],
        "status": "running",
        "modules": [
            "Legislative Tracker",
            "Plain Language Engine",
            "Impact Simulator",
            "Democratic Interface",
            "Transparency Hub"
        ]
    }


@app.post("/api/documents", response_model=Dict[str, Any])
async def create_document(document: DocumentCreate):
    """Tworzy nowy dokument legislacyjny"""
    doc_id = f"doc_{datetime.now().timestamp()}"
    
    try:
        status = LegislativeStatus(document.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Nieprawidłowy status: {document.status}")
    
    doc = LegislativeDocument(
        id=doc_id,
        title=document.title,
        description=document.description,
        status=status,
        current_stage=document.status,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        dependencies=document.dependencies,
        metadata=document.metadata
    )
    
    if tracker.register_document(doc):
        return {"success": True, "document_id": doc_id, "document": doc.to_dict()}
    else:
        raise HTTPException(status_code=400, detail="Dokument już istnieje")


@app.get("/api/documents", response_model=List[Dict[str, Any]])
async def get_documents(status: Optional[str] = None):
    """Pobiera listę dokumentów"""
    if status:
        try:
            status_enum = LegislativeStatus(status)
            return tracker.get_all_documents(status_filter=status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Nieprawidłowy status: {status}")
    
    return tracker.get_all_documents()


@app.get("/api/documents/{document_id}", response_model=Dict[str, Any])
async def get_document(document_id: str):
    """Pobiera szczegóły dokumentu"""
    docs = tracker.get_all_documents()
    doc = next((d for d in docs if d["id"] == document_id), None)
    
    if not doc:
        raise HTTPException(status_code=404, detail="Dokument nie znaleziony")
    
    return doc


@app.put("/api/documents/{document_id}/status", response_model=Dict[str, Any])
async def update_status(document_id: str, update: StatusUpdate):
    """Aktualizuje status dokumentu"""
    try:
        status = LegislativeStatus(update.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Nieprawidłowy status: {update.status}")
    
    if tracker.update_status(document_id, status, update.stage):
        docs = tracker.get_all_documents()
        doc = next((d for d in docs if d["id"] == document_id), None)
        return {"success": True, "document": doc}
    else:
        raise HTTPException(status_code=404, detail="Dokument nie znaleziony")


@app.get("/api/documents/{document_id}/timeline", response_model=List[Dict[str, Any]])
async def get_timeline(document_id: str):
    """Pobiera oś czasu dokumentu"""
    timeline = tracker.get_document_timeline(document_id)
    if timeline is None:
        raise HTTPException(status_code=404, detail="Dokument nie znaleziony")
    return timeline


@app.get("/api/legislative-train", response_model=Dict[str, Any])
async def get_legislative_train():
    """Pobiera wizualizację Legislative Train"""
    return tracker.get_legislative_train()


@app.get("/api/documents/{document_id}/dependencies", response_model=Dict[str, Any])
async def get_dependencies(document_id: str):
    """Analizuje zależności dokumentu"""
    deps = tracker.analyze_dependencies(document_id)
    if not deps:
        raise HTTPException(status_code=404, detail="Dokument nie znaleziony")
    return deps


# ============================================================================
# ENDPOINTY - PLAIN LANGUAGE ENGINE
# ============================================================================

@app.post("/api/simplify", response_model=Dict[str, Any])
async def simplify_text(request: SimplifyRequest):
    """Upraszcza tekst urzędowy"""
    result = plain_language.simplify_text(request.text, request.use_llm)
    
    return {
        "original": result.original,
        "simplified": result.simplified,
        "complexity_score": result.complexity_score,
        "readability_score": result.readability_score,
        "changes": result.changes,
        "improvement": (1.0 - result.complexity_score) * 100
    }


@app.post("/api/simplify-document", response_model=Dict[str, Any])
async def simplify_document(document_text: str, sections: Optional[List[str]] = None):
    """Upraszcza cały dokument prawny"""
    result = plain_language.simplify_legal_document(document_text, sections)
    return result


@app.post("/api/summarize", response_model=Dict[str, Any])
async def summarize_text(text: str, max_length: int = 200):
    """Generuje streszczenie tekstu"""
    summary = plain_language.generate_summary(text, max_length)
    return {"summary": summary, "original_length": len(text), "summary_length": len(summary)}


# ============================================================================
# ENDPOINTY - IMPACT SIMULATOR
# ============================================================================

@app.post("/api/documents/{document_id}/impact-analysis", response_model=List[Dict[str, Any]])
async def analyze_impact(document_id: str, request: ImpactAnalysisRequest):
    """Analizuje wpływ regulacji"""
    impact_types = None
    if request.impact_types:
        impact_types = [ImpactType(t) for t in request.impact_types]
    
    analyses = impact_simulator.analyze_impact(
        document_id,
        request.document_text,
        impact_types
    )
    
    return [
        {
            "impact_type": a.impact_type.value,
            "severity": a.severity,
            "description": a.description,
            "affected_entities": a.affected_entities,
            "estimated_cost": a.estimated_cost,
            "time_horizon": a.time_horizon,
            "risks": a.risks,
            "opportunities": a.opportunities,
            "recommendations": a.recommendations
        }
        for a in analyses
    ]


@app.post("/api/documents/{document_id}/scenarios", response_model=List[Dict[str, Any]])
async def generate_scenarios(document_id: str):
    """Generuje scenariusze wpływu"""
    scenarios = impact_simulator.generate_scenarios(document_id)
    
    return [
        {
            "name": s.name,
            "probability": s.probability,
            "description": s.description,
            "key_indicators": s.key_indicators,
            "impacts": [
                {
                    "type": a.impact_type.value,
                    "severity": a.severity,
                    "description": a.description
                }
                for a in s.impacts
            ]
        }
        for s in scenarios
    ]


@app.get("/api/documents/{document_id}/impact-summary", response_model=Dict[str, Any])
async def get_impact_summary(document_id: str):
    """Pobiera podsumowanie analizy wpływu"""
    return impact_simulator.get_impact_summary(document_id)


# ============================================================================
# ENDPOINTY - DEMOCRATIC INTERFACE
# ============================================================================

@app.post("/api/consultations", response_model=Dict[str, Any])
async def create_consultation(consultation: ConsultationCreate):
    """Tworzy nowe konsultacje społeczne"""
    try:
        start_date = datetime.fromisoformat(consultation.start_date)
        end_date = datetime.fromisoformat(consultation.end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Nieprawidłowy format daty (użyj ISO format)")
    
    consult = Consultation(
        id=f"consult_{datetime.now().timestamp()}",
        title=consultation.title,
        description=consultation.description,
        start_date=start_date,
        end_date=end_date,
        document_id=consultation.document_id
    )
    
    if democratic_interface.register_consultation(consult):
        return {"success": True, "consultation_id": consult.id}
    else:
        raise HTTPException(status_code=400, detail="Konsultacje już istnieją")


@app.get("/api/consultations", response_model=List[Dict[str, Any]])
async def get_consultations(user_id: Optional[str] = None):
    """Pobiera aktywne konsultacje"""
    return democratic_interface.get_active_consultations(user_id)


@app.get("/api/consultations/upcoming", response_model=List[Dict[str, Any]])
async def get_upcoming_consultations(days_ahead: int = 30):
    """Pobiera nadchodzące konsultacje"""
    return democratic_interface.get_upcoming_consultations(days_ahead)


@app.post("/api/users/{user_id}/profile", response_model=Dict[str, Any])
async def create_user_profile(user_id: str, interests: List[str], language: str = "pl"):
    """Tworzy profil użytkownika"""
    profile = democratic_interface.create_user_profile(user_id, interests, language)
    return {
        "user_id": profile.user_id,
        "interests": profile.interests,
        "language_preference": profile.language_preference
    }


@app.get("/api/users/{user_id}/notifications", response_model=List[Dict[str, Any]])
async def get_notifications(user_id: str, unread_only: bool = False):
    """Pobiera powiadomienia użytkownika"""
    return democratic_interface.get_user_notifications(user_id, unread_only)


@app.get("/api/legislative-process-guide", response_model=Dict[str, Any])
async def get_process_guide():
    """Pobiera przewodnik po procesie legislacyjnym"""
    return democratic_interface.get_legislative_process_guide()


# ============================================================================
# ENDPOINTY - TRANSPARENCY HUB
# ============================================================================

@app.post("/api/documents/{document_id}/compliance", response_model=List[Dict[str, Any]])
async def check_compliance(document_id: str, policies: List[str]):
    """Sprawdza zgodność dokumentu z politykami"""
    reports = transparency_hub.check_compliance(document_id, policies)
    
    return [
        {
            "policy": r.policy_name,
            "status": r.status.value,
            "score": r.score,
            "findings": r.findings,
            "recommendations": r.recommendations
        }
        for r in reports
    ]


@app.get("/api/documents/{document_id}/transparency-report", response_model=Dict[str, Any])
async def get_transparency_report(document_id: str):
    """Generuje raport transparentności"""
    return transparency_hub.generate_transparency_report(document_id)


@app.post("/api/documents/{document_id}/osr-quality", response_model=Dict[str, Any])
async def assess_osr_quality(document_id: str, osr_text: str):
    """Ocenia jakość OSR"""
    return transparency_hub.get_osr_quality_assessment(document_id, osr_text)


# ============================================================================
# URUCHOMIENIE
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=True
    )

