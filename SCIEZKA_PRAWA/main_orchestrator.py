"""
GQPA Legislative Navigator - Main Orchestrator
Koordynuje wszystkie moduły systemu
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from legislative_tracker import LegislativeTracker, LegislativeDocument, LegislativeStatus
from plain_language_engine import PlainLanguageEngine
from impact_simulator import ImpactSimulator, ImpactType
from democratic_interface import DemocraticInterface, Consultation
from transparency_hub import TransparencyHub


class GQPALegislativeOrchestrator:
    """
    Główny orchestrator systemu GQPA Legislative Navigator
    Koordynuje pracę wszystkich modułów
    """
    
    def __init__(self):
        self.tracker = LegislativeTracker()
        self.plain_language = PlainLanguageEngine()
        self.impact_simulator = ImpactSimulator()
        self.democratic_interface = DemocraticInterface()
        self.transparency_hub = TransparencyHub()
        
    def process_new_document(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Przetwarza nowy dokument legislacyjny przez wszystkie moduły
        
        Args:
            document_data: Dane dokumentu (title, description, text, etc.)
        """
        # 1. Zarejestruj dokument w trackerze
        doc_id = f"doc_{datetime.now().timestamp()}"
        doc = LegislativeDocument(
            id=doc_id,
            title=document_data.get("title", ""),
            description=document_data.get("description", ""),
            status=LegislativeStatus.PREKONSULTACJE,
            current_stage="prekonsultacje",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata=document_data.get("metadata", {})
        )
        
        self.tracker.register_document(doc)
        
        # 2. Uprość język (jeśli podano tekst)
        simplified = None
        if "text" in document_data:
            simplified = self.plain_language.simplify_legal_document(document_data["text"])
        
        # 3. Analiza wpływu
        impact_analyses = []
        if "text" in document_data:
            impact_analyses = self.impact_simulator.analyze_impact(
                doc_id,
                document_data["text"]
            )
            
            # Generuj scenariusze
            scenarios = self.impact_simulator.generate_scenarios(doc_id, impact_analyses)
        
        # 4. Sprawdź zgodność z politykami
        compliance_reports = []
        policies = document_data.get("policies_to_check", ["RODO", "DSA", "WCAG"])
        compliance_reports = self.transparency_hub.check_compliance(doc_id, policies)
        
        # 5. Utwórz konsultacje społeczne (jeśli wymagane)
        consultation = None
        if document_data.get("create_consultation", False):
            consultation = Consultation(
                id=f"consult_{datetime.now().timestamp()}",
                title=f"Konsultacje: {doc.title}",
                description=doc.description,
                start_date=datetime.now(),
                end_date=datetime.now(),  # W rzeczywistości ustawić odpowiedni termin
                document_id=doc_id
            )
            self.democratic_interface.register_consultation(consultation)
        
        return {
            "document_id": doc_id,
            "document": doc.to_dict(),
            "simplified": simplified,
            "impact_analyses": [
                {
                    "type": a.impact_type.value,
                    "severity": a.severity,
                    "description": a.description
                }
                for a in impact_analyses
            ],
            "scenarios": [
                {
                    "name": s.name,
                    "probability": s.probability,
                    "description": s.description
                }
                for s in scenarios
            ] if "text" in document_data else [],
            "compliance": [
                {
                    "policy": r.policy_name,
                    "status": r.status.value,
                    "score": r.score
                }
                for r in compliance_reports
            ],
            "consultation": {
                "id": consultation.id,
                "title": consultation.title
            } if consultation else None
        }
    
    def get_comprehensive_report(self, document_id: str) -> Dict[str, Any]:
        """
        Generuje kompleksowy raport dla dokumentu
        Zawiera informacje ze wszystkich modułów
        """
        # Pobierz dokument
        docs = self.tracker.get_all_documents()
        doc = next((d for d in docs if d["id"] == document_id), None)
        
        if not doc:
            return {"error": "Dokument nie znaleziony"}
        
        # Oś czasu
        timeline = self.tracker.get_document_timeline(document_id)
        
        # Zależności
        dependencies = self.tracker.analyze_dependencies(document_id)
        
        # Analiza wpływu
        impact_summary = self.impact_simulator.get_impact_summary(document_id)
        scenarios = self.impact_simulator.generate_scenarios(document_id)
        
        # Raport transparentności
        transparency_report = self.transparency_hub.generate_transparency_report(document_id)
        
        # Konsultacje społeczne
        consultations = [
            c for c in self.democratic_interface.consultations.values()
            if c.document_id == document_id
        ]
        
        return {
            "document": doc,
            "timeline": timeline,
            "dependencies": dependencies,
            "impact_analysis": impact_summary,
            "scenarios": [
                {
                    "name": s.name,
                    "probability": s.probability,
                    "description": s.description,
                    "key_indicators": s.key_indicators
                }
                for s in scenarios
            ],
            "transparency": transparency_report,
            "consultations": [
                {
                    "id": c.id,
                    "title": c.title,
                    "status": c.status,
                    "end_date": c.end_date.isoformat()
                }
                for c in consultations
            ],
            "generated_at": datetime.now().isoformat()
        }
    
    def update_document_status(self, document_id: str, new_status: str,
                              stage: Optional[str] = None) -> Dict[str, Any]:
        """
        Aktualizuje status dokumentu i wyzwala odpowiednie akcje
        """
        try:
            status = LegislativeStatus(new_status)
        except ValueError:
            return {"error": f"Nieprawidłowy status: {new_status}"}
        
        # Aktualizuj status
        success = self.tracker.update_status(document_id, status, stage)
        
        if not success:
            return {"error": "Dokument nie znaleziony"}
        
        # Jeśli dokument przeszedł do konsultacji społecznych, utwórz powiadomienia
        if status == LegislativeStatus.KONSULTACJE_SPOLECZNE:
            consultations = [
                c for c in self.democratic_interface.consultations.values()
                if c.document_id == document_id
            ]
            
            # Jeśli nie ma konsultacji, można je utworzyć automatycznie
            if not consultations:
                # W rzeczywistości tutaj byłaby logika tworzenia konsultacji
                pass
        
        # Pobierz zaktualizowany dokument
        docs = self.tracker.get_all_documents()
        doc = next((d for d in docs if d["id"] == document_id), None)
        
        return {
            "success": True,
            "document": doc,
            "status_changed_to": new_status
        }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Generuje dane dla dashboardu
        Zawiera statystyki ze wszystkich modułów
        """
        # Statystyki dokumentów
        all_docs = self.tracker.get_all_documents()
        docs_by_status = {}
        for doc in all_docs:
            status = doc["status"]
            docs_by_status[status] = docs_by_status.get(status, 0) + 1
        
        # Legislative Train
        train = self.tracker.get_legislative_train()
        
        # Aktywne konsultacje
        active_consultations = self.democratic_interface.get_active_consultations()
        
        # Statystyki analizy wpływu
        total_analyses = sum(len(analyses) for analyses in self.impact_simulator.analyses.values())
        
        return {
            "documents": {
                "total": len(all_docs),
                "by_status": docs_by_status
            },
            "legislative_train": train,
            "consultations": {
                "active": len(active_consultations),
                "total": len(self.democratic_interface.consultations)
            },
            "impact_analyses": {
                "total": total_analyses,
                "documents_analyzed": len(self.impact_simulator.analyses)
            },
            "generated_at": datetime.now().isoformat()
        }


# Singleton instance
orchestrator = GQPALegislativeOrchestrator()

