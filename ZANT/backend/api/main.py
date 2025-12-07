"""
FastAPI Backend dla ZANT
Główne endpointy API
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import os
import uuid
import logging
from datetime import datetime

from backend.models.accident import (
    AccidentReport, AccidentStatus, ReportAnalysis, AccidentCard
)
from backend.services.accident_assistant import AccidentAssistant
from backend.services.pdf_extractor import PDFExtractor
from backend.services.decision_engine import DecisionEngine
from backend.config import API_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ZANT API",
    description="ZUS Accident Notification Tool - API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicjalizacja serwisów
assistant = AccidentAssistant()
pdf_extractor = PDFExtractor()
decision_engine = DecisionEngine()

# Storage (w produkcji: baza danych)
reports_storage: Dict[str, AccidentReport] = {}
cards_storage: Dict[str, AccidentCard] = {}


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "ZANT API",
        "version": "1.0.0"
    }


@app.post("/api/report/analyze", response_model=Dict[str, Any])
async def analyze_report(report_data: Dict[str, Any]):
    """
    Analizuje zgłoszenie wypadku i wykrywa brakujące elementy
    """
    try:
        # Utwórz obiekt AccidentReport
        report_id = report_data.get("report_id", f"RPT-{uuid.uuid4().hex[:8]}")
        report = AccidentReport(
            report_id=report_id,
            data_wypadku=report_data.get("data_wypadku"),
            godzina_wypadku=report_data.get("godzina_wypadku"),
            miejsce_wypadku=report_data.get("miejsce_wypadku"),
            okolicznosci_wypadku=report_data.get("okolicznosci_wypadku"),
            przyczyna_wypadku=report_data.get("przyczyna_wypadku"),
            dane_poszkodowanego=report_data.get("dane_poszkodowanego"),
            rodzaj_dzialalnosci=report_data.get("rodzaj_dzialalnosci"),
            opis_urazu=report_data.get("opis_urazu"),
            status=AccidentStatus.DRAFT
        )
        
        # Zapisz w storage
        reports_storage[report_id] = report
        
        # Analizuj
        analysis = assistant.analyze_report(report)
        
        return {
            "report_id": report_id,
            "completeness_score": analysis.completeness_score,
            "missing_fields": [
                {
                    "field_name": mf.field_name,
                    "field_description": mf.field_description,
                    "priority": mf.priority,
                    "suggestion": mf.suggestion
                }
                for mf in analysis.missing_fields
            ],
            "suggestions": analysis.suggestions,
            "validation_errors": analysis.validation_errors,
            "confidence": analysis.confidence
        }
    
    except Exception as e:
        logger.error(f"Błąd podczas analizy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/report/submit", response_model=Dict[str, Any])
async def submit_report(report_data: Dict[str, Any]):
    """
    Zapisuje zgłoszenie wypadku
    """
    try:
        report_id = report_data.get("report_id", f"RPT-{uuid.uuid4().hex[:8]}")
        report = AccidentReport(
            report_id=report_id,
            **{k: v for k, v in report_data.items() if k != "report_id"}
        )
        report.status = AccidentStatus.SUBMITTED
        report.updated_at = datetime.now()
        
        reports_storage[report_id] = report
        
        return {
            "report_id": report_id,
            "status": "submitted",
            "message": "Zgłoszenie zostało zapisane"
        }
    
    except Exception as e:
        logger.error(f"Błąd podczas zapisywania: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/decision/analyze", response_model=Dict[str, Any])
async def analyze_decision(
    file: UploadFile = File(...),
    report_id: Optional[str] = None
):
    """
    Analizuje dokumentację PDF i rekomenduje decyzję
    """
    try:
        # Zapisz plik tymczasowo
        from backend.config import TEMP_UPLOADS_DIR
        file_path = os.path.join(TEMP_UPLOADS_DIR, f"{uuid.uuid4().hex}.pdf")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Ekstrahuj dane z PDF
        extraction = pdf_extractor.extract_from_pdf(file_path)
        
        # Jeśli nie podano report_id, utwórz nowy
        if not report_id:
            report_id = f"RPT-{uuid.uuid4().hex[:8]}"
        
        # Analizuj i rekomenduj decyzję
        card = decision_engine.analyze_and_recommend(extraction, report_id)
        
        # Zapisz kartę
        cards_storage[card.card_id] = card
        
        # Usuń plik tymczasowy
        try:
            os.remove(file_path)
        except:
            pass
        
        return {
            "card_id": card.card_id,
            "report_id": report_id,
            "decision": card.decision.value,
            "confidence": card.confidence,
            "reasoning": card.reasoning,
            "legal_basis": card.legal_basis,
            "risk_factors": card.risk_factors,
            "extracted_data": card.extracted_data
        }
    
    except Exception as e:
        logger.error(f"Błąd podczas analizy decyzji: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/report/{report_id}", response_model=Dict[str, Any])
async def get_report(report_id: str):
    """Pobiera zgłoszenie po ID"""
    if report_id not in reports_storage:
        raise HTTPException(status_code=404, detail="Zgłoszenie nie znalezione")
    
    return reports_storage[report_id].to_dict()


@app.get("/api/card/{card_id}", response_model=Dict[str, Any])
async def get_card(card_id: str):
    """Pobiera kartę wypadku po ID"""
    if card_id not in cards_storage:
        raise HTTPException(status_code=404, detail="Karta nie znaleziona")
    
    return cards_storage[card_id].to_dict()


@app.get("/api/reports", response_model=Dict[str, Any])
async def list_reports():
    """Lista wszystkich zgłoszeń"""
    return {
        "reports": [report.to_dict() for report in reports_storage.values()],
        "total": len(reports_storage)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=True
    )

