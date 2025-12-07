"""
GQPA Transparency Hub
Centrum transparentności dla administracji
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class ComplianceStatus(Enum):
    """Status zgodności"""
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"


@dataclass
class ComplianceReport:
    """Raport zgodności"""
    document_id: str
    policy_name: str
    status: ComplianceStatus
    score: float  # 0.0 - 1.0
    findings: List[str]
    recommendations: List[str]
    checked_at: datetime = field(default_factory=datetime.now)


@dataclass
class DelayAnalysis:
    """Analiza opóźnień"""
    document_id: str
    stage: str
    expected_duration: int  # dni
    actual_duration: int  # dni
    delay_days: int
    delay_reason: Optional[str] = None
    impact: str = "low"  # low, medium, high


@dataclass
class DocumentRelationship:
    """Relacja między dokumentami"""
    source_id: str
    target_id: str
    relationship_type: str  # depends_on, related_to, conflicts_with, replaces
    strength: float  # 0.0 - 1.0
    description: Optional[str] = None


class TransparencyHub:
    """
    Centrum transparentności
    Zapewnia wgląd w procesy legislacyjne dla administracji
    """
    
    def __init__(self):
        self.compliance_reports: Dict[str, List[ComplianceReport]] = {}  # document_id -> reports
        self.delay_analyses: Dict[str, List[DelayAnalysis]] = {}  # document_id -> analyses
        self.relationships: List[DocumentRelationship] = []
        
    def check_compliance(self, document_id: str, 
                        policies: List[str]) -> List[ComplianceReport]:
        """
        Sprawdza zgodność dokumentu z politykami
        
        Args:
            document_id: ID dokumentu
            policies: Lista polityk do sprawdzenia (np. ["RODO", "DSA", "WCAG"])
        """
        reports = []
        
        for policy in policies:
            report = self._check_single_policy(document_id, policy)
            reports.append(report)
        
        # Zapisz raporty
        if document_id not in self.compliance_reports:
            self.compliance_reports[document_id] = []
        self.compliance_reports[document_id].extend(reports)
        
        return reports
    
    def _check_single_policy(self, document_id: str, policy: str) -> ComplianceReport:
        """
        Sprawdza zgodność z pojedynczą polityką
        W pełnej implementacji używa GQPA do analizy
        """
        # Uproszczona wersja - w pełnej implementacji użyjemy GQPA CognitiveAgent
        
        # Symulacja sprawdzenia
        if policy.upper() in ["RODO", "GDPR"]:
            # Sprawdź zgodność z RODO
            score = 0.85  # Przykładowy wynik
            status = ComplianceStatus.COMPLIANT if score > 0.8 else ComplianceStatus.PARTIAL
            findings = [
                "Dokument zawiera wymagane informacje o przetwarzaniu danych",
                "Zidentyfikowano wszystkie kategorie danych osobowych"
            ]
            recommendations = []
            if score < 0.9:
                recommendations.append("Rozważyć dodanie dodatkowych informacji o prawach osób")
        
        elif policy.upper() in ["DSA", "DIGITAL_SERVICES_ACT"]:
            # Sprawdź zgodność z DSA
            score = 0.75
            status = ComplianceStatus.PARTIAL if score > 0.7 else ComplianceStatus.NON_COMPLIANT
            findings = [
                "Dokument częściowo uwzględnia wymagania DSA",
                "Wymagane dodatkowe sekcje dotyczące bezpieczeństwa cyfrowego"
            ]
            recommendations = [
                "Dodać sekcję o mechanizmach raportowania",
                "Uwzględnić wymagania dotyczące transparentności algorytmów"
            ]
        
        elif policy.upper() in ["WCAG", "ACCESSIBILITY"]:
            # Sprawdź zgodność z dostępnością
            score = 0.90
            status = ComplianceStatus.COMPLIANT
            findings = [
                "Dokument spełnia wymagania WCAG AA",
                "Zapewniono wsparcie dla czytników ekranu"
            ]
            recommendations = []
        
        else:
            # Domyślna polityka
            score = 0.70
            status = ComplianceStatus.PARTIAL
            findings = [f"Sprawdzono zgodność z polityką: {policy}"]
            recommendations = ["Wymagana szczegółowa analiza"]
        
        return ComplianceReport(
            document_id=document_id,
            policy_name=policy,
            status=status,
            score=score,
            findings=findings,
            recommendations=recommendations
        )
    
    def analyze_delays(self, document_id: str, 
                     stage_durations: Dict[str, int]) -> List[DelayAnalysis]:
        """
        Analizuje opóźnienia w procesie legislacyjnym
        
        Args:
            document_id: ID dokumentu
            stage_durations: Słownik {stage: actual_duration_days}
        """
        analyses = []
        
        # Oczekiwane czasy trwania etapów (w dniach)
        expected_durations = {
            "prekonsultacje": 30,
            "konsultacje_spoleczne": 45,
            "projekt_rzadowy": 60,
            "rada_ministrow": 14,
            "sejm_pierwsze_czytanie": 30,
            "sejm_drugie_czytanie": 14,
            "sejm_trzecie_czytanie": 7,
            "senat": 30,
            "podpis_prezydenta": 21,
            "opublikowanie": 14
        }
        
        for stage, actual_duration in stage_durations.items():
            expected_duration = expected_durations.get(stage, 30)
            delay_days = max(0, actual_duration - expected_duration)
            
            if delay_days > 0:
                # Określ wpływ opóźnienia
                if delay_days <= 7:
                    impact = "low"
                elif delay_days <= 30:
                    impact = "medium"
                else:
                    impact = "high"
                
                analysis = DelayAnalysis(
                    document_id=document_id,
                    stage=stage,
                    expected_duration=expected_duration,
                    actual_duration=actual_duration,
                    delay_days=delay_days,
                    impact=impact
                )
                analyses.append(analysis)
        
        # Zapisz analizy
        if document_id not in self.delay_analyses:
            self.delay_analyses[document_id] = []
        self.delay_analyses[document_id].extend(analyses)
        
        return analyses
    
    def analyze_relationships(self, document_id: str,
                              all_documents: List[Dict[str, Any]]) -> List[DocumentRelationship]:
        """
        Analizuje relacje między dokumentami
        Wykorzystuje GQPA do wykrywania zależności
        """
        relationships = []
        
        # Znajdź dokument docelowy
        target_doc = next((d for d in all_documents if d.get("id") == document_id), None)
        if not target_doc:
            return relationships
        
        target_text = (target_doc.get("title", "") + " " + target_doc.get("description", "")).lower()
        
        # Sprawdź relacje z innymi dokumentami
        for doc in all_documents:
            if doc.get("id") == document_id:
                continue
            
            doc_text = (doc.get("title", "") + " " + doc.get("description", "")).lower()
            
            # Wykryj wspólne słowa kluczowe
            target_words = set(target_text.split())
            doc_words = set(doc_text.split())
            common_words = target_words.intersection(doc_words)
            
            if len(common_words) >= 3:  # Próg podobieństwa
                # Określ typ relacji
                relationship_type = "related_to"
                strength = min(1.0, len(common_words) / 10)
                
                # Sprawdź czy są wzmianki o zależnościach
                if any(word in target_text for word in ["zależy", "wymaga", "potrzebuje"]):
                    relationship_type = "depends_on"
                    strength = min(1.0, strength + 0.2)
                
                if any(word in target_text for word in ["zastępuje", "uchyla", "anuluje"]):
                    relationship_type = "replaces"
                    strength = min(1.0, strength + 0.3)
                
                relationship = DocumentRelationship(
                    source_id=document_id,
                    target_id=doc.get("id"),
                    relationship_type=relationship_type,
                    strength=strength,
                    description=f"Wykryto {len(common_words)} wspólnych słów kluczowych"
                )
                relationships.append(relationship)
        
        # Zapisz relacje
        self.relationships.extend(relationships)
        
        return relationships
    
    def generate_transparency_report(self, document_id: str) -> Dict[str, Any]:
        """Generuje raport transparentności dla dokumentu"""
        compliance_reports = self.compliance_reports.get(document_id, [])
        delay_analyses = self.delay_analyses.get(document_id, [])
        relationships = [r for r in self.relationships if r.source_id == document_id]
        
        # Oblicz ogólny wskaźnik transparentności
        compliance_score = sum(r.score for r in compliance_reports) / len(compliance_reports) if compliance_reports else 0.0
        
        # Analiza opóźnień
        total_delays = sum(a.delay_days for a in delay_analyses)
        avg_delay = total_delays / len(delay_analyses) if delay_analyses else 0
        
        # Liczba relacji
        relationship_count = len(relationships)
        
        # Ogólny wskaźnik transparentności (0.0 - 1.0)
        transparency_score = (
            compliance_score * 0.5 +
            (1.0 - min(1.0, avg_delay / 100)) * 0.3 +  # Im mniej opóźnień, tym lepiej
            min(1.0, relationship_count / 10) * 0.2  # Im więcej relacji wykrytych, tym lepiej
        )
        
        return {
            "document_id": document_id,
            "transparency_score": transparency_score,
            "compliance": {
                "reports_count": len(compliance_reports),
                "average_score": compliance_score,
                "status": "compliant" if compliance_score > 0.8 else "partial" if compliance_score > 0.6 else "non_compliant",
                "reports": [
                    {
                        "policy": r.policy_name,
                        "status": r.status.value,
                        "score": r.score,
                        "findings": r.findings,
                        "recommendations": r.recommendations
                    }
                    for r in compliance_reports
                ]
            },
            "delays": {
                "analyses_count": len(delay_analyses),
                "total_delay_days": total_delays,
                "average_delay": avg_delay,
                "analyses": [
                    {
                        "stage": a.stage,
                        "expected_duration": a.expected_duration,
                        "actual_duration": a.actual_duration,
                        "delay_days": a.delay_days,
                        "impact": a.impact
                    }
                    for a in delay_analyses
                ]
            },
            "relationships": {
                "count": relationship_count,
                "relationships": [
                    {
                        "target_id": r.target_id,
                        "type": r.relationship_type,
                        "strength": r.strength,
                        "description": r.description
                    }
                    for r in relationships
                ]
            },
            "generated_at": datetime.now().isoformat()
        }
    
    def get_osr_quality_assessment(self, document_id: str, osr_text: str) -> Dict[str, Any]:
        """
        Ocenia jakość OSR (Ocena Skutków Regulacji)
        Wykorzystuje GQPA do analizy kompletności i jakości
        """
        # Uproszczona wersja - w pełnej implementacji użyjemy GQPA
        
        # Sprawdź obecność wymaganych sekcji OSR
        required_sections = [
            "cel regulacji",
            "analiza problemu",
            "opcje regulacyjne",
            "analiza skutków",
            "konsultacje",
            "monitoring"
        ]
        
        osr_lower = osr_text.lower()
        found_sections = [section for section in required_sections if section in osr_lower]
        
        completeness = len(found_sections) / len(required_sections)
        
        # Sprawdź długość OSR (wymagane minimum ~5000 znaków)
        length_score = min(1.0, len(osr_text) / 5000)
        
        # Ogólna ocena jakości
        quality_score = (completeness * 0.6 + length_score * 0.4)
        
        return {
            "document_id": document_id,
            "quality_score": quality_score,
            "completeness": completeness,
            "found_sections": found_sections,
            "missing_sections": [s for s in required_sections if s not in found_sections],
            "length": len(osr_text),
            "recommendations": [
                f"Dodać sekcję: {section}" 
                for section in required_sections 
                if section not in found_sections
            ] if completeness < 1.0 else ["OSR jest kompletne"]
        }

