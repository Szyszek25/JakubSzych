"""
Modele danych dla systemu ZANT
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class AccidentStatus(Enum):
    """Status zgłoszenia wypadku"""
    DRAFT = "draft"  # W trakcie wypełniania
    SUBMITTED = "submitted"  # Zgłoszone
    UNDER_REVIEW = "under_review"  # W trakcie weryfikacji
    APPROVED = "approved"  # Uznane za wypadek
    REJECTED = "rejected"  # Nie uznane za wypadek


class DecisionRecommendation(Enum):
    """Rekomendacja decyzji"""
    RECOGNIZE = "recognize"  # Uznać za wypadek
    NOT_RECOGNIZE = "not_recognize"  # Nie uznać za wypadek
    NEEDS_REVIEW = "needs_review"  # Wymaga dodatkowej weryfikacji


@dataclass
class AccidentReport:
    """Model zgłoszenia wypadku"""
    report_id: str
    data_wypadku: Optional[str] = None
    godzina_wypadku: Optional[str] = None
    miejsce_wypadku: Optional[str] = None
    okolicznosci_wypadku: Optional[str] = None
    przyczyna_wypadku: Optional[str] = None
    dane_poszkodowanego: Optional[str] = None
    rodzaj_dzialalnosci: Optional[str] = None
    opis_urazu: Optional[str] = None
    status: AccidentStatus = AccidentStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Konwersja do słownika"""
        return {
            "report_id": self.report_id,
            "data_wypadku": self.data_wypadku,
            "godzina_wypadku": self.godzina_wypadku,
            "miejsce_wypadku": self.miejsce_wypadku,
            "okolicznosci_wypadku": self.okolicznosci_wypadku,
            "przyczyna_wypadku": self.przyczyna_wypadku,
            "dane_poszkodowanego": self.dane_poszkodowanego,
            "rodzaj_dzialalnosci": self.rodzaj_dzialalnosci,
            "opis_urazu": self.opis_urazu,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class MissingField:
    """Informacja o brakującym polu"""
    field_name: str
    field_description: str
    priority: str  # "high", "medium", "low"
    suggestion: Optional[str] = None


@dataclass
class ReportAnalysis:
    """Wynik analizy zgłoszenia"""
    report_id: str
    completeness_score: float  # 0.0 - 1.0
    missing_fields: List[MissingField]
    suggestions: List[str]
    validation_errors: List[str]
    confidence: float  # 0.0 - 1.0


@dataclass
class AccidentCard:
    """Karta wypadku (wynik analizy dokumentacji)"""
    card_id: str
    report_id: str
    decision: DecisionRecommendation
    confidence: float
    reasoning: str
    extracted_data: Dict[str, Any]
    legal_basis: List[str]
    risk_factors: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Konwersja do słownika"""
        return {
            "card_id": self.card_id,
            "report_id": self.report_id,
            "decision": self.decision.value,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "extracted_data": self.extracted_data,
            "legal_basis": self.legal_basis,
            "risk_factors": self.risk_factors,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class DocumentExtraction:
    """Wynik ekstrakcji danych z dokumentu PDF"""
    document_id: str
    text_content: str
    extracted_fields: Dict[str, Any]
    confidence: float
    processing_time: float
    ocr_used: bool


