"""
GQPA Legislative Tracker
Moduł śledzenia procesów legislacyjnych
"""

import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from config import LEGISLATIVE_STATUSES


class LegislativeStatus(Enum):
    """Statusy procesu legislacyjnego"""
    PREKONSULTACJE = "prekonsultacje"
    KONSULTACJE_SPOLECZNE = "konsultacje_spoleczne"
    PROJEKT_RZADOWY = "projekt_rzadowy"
    RADA_MINISTROW = "rada_ministrow"
    SEJM_PIERWSZE_CZYTANIE = "sejm_pierwsze_czytanie"
    SEJM_DRUGIE_CZYTANIE = "sejm_drugie_czytanie"
    SEJM_TRZECIE_CZYTANIE = "sejm_trzecie_czytanie"
    SENAT = "senat"
    PODPIS_PREZYDENTA = "podpis_prezydenta"
    OPUBLIKOWANIE = "opublikowanie"
    WEJSCIE_W_ZYCIE = "wejscie_w_zycie"


@dataclass
class LegislativeDocument:
    """Reprezentacja dokumentu legislacyjnego"""
    id: str
    title: str
    description: str
    status: LegislativeStatus
    current_stage: str
    created_at: datetime
    updated_at: datetime
    version: int = 1
    dependencies: List[str] = field(default_factory=list)
    related_documents: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Konwersja do słownika"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "current_stage": self.current_stage,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version,
            "dependencies": self.dependencies,
            "related_documents": self.related_documents,
            "metadata": self.metadata
        }


@dataclass
class LegislativeEvent:
    """Wydarzenie w procesie legislacyjnym"""
    document_id: str
    event_type: str
    timestamp: datetime
    description: str
    actor: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class LegislativeTracker:
    """
    Główny moduł śledzenia legislacji
    Wykorzystuje GQPA do analizy i prognozowania
    """
    
    def __init__(self):
        self.documents: Dict[str, LegislativeDocument] = {}
        self.events: List[LegislativeEvent] = []
        self.dependency_graph: Dict[str, List[str]] = {}
        
    def register_document(self, document: LegislativeDocument) -> bool:
        """Rejestracja nowego dokumentu legislacyjnego"""
        if document.id in self.documents:
            return False
        
        self.documents[document.id] = document
        self.dependency_graph[document.id] = document.dependencies.copy()
        
        # Zarejestruj wydarzenie
        event = LegislativeEvent(
            document_id=document.id,
            event_type="document_registered",
            timestamp=datetime.now(),
            description=f"Dokument '{document.title}' został zarejestrowany"
        )
        self.events.append(event)
        
        return True
    
    def update_status(self, document_id: str, new_status: LegislativeStatus, 
                     stage: Optional[str] = None) -> bool:
        """Aktualizacja statusu dokumentu"""
        if document_id not in self.documents:
            return False
        
        doc = self.documents[document_id]
        old_status = doc.status
        doc.status = new_status
        doc.updated_at = datetime.now()
        
        if stage:
            doc.current_stage = stage
        
        # Zarejestruj wydarzenie
        event = LegislativeEvent(
            document_id=document_id,
            event_type="status_changed",
            timestamp=datetime.now(),
            description=f"Status zmieniony z {old_status.value} na {new_status.value}",
            metadata={"old_status": old_status.value, "new_status": new_status.value}
        )
        self.events.append(event)
        
        return True
    
    def get_document_timeline(self, document_id: str) -> List[Dict[str, Any]]:
        """Pobranie osi czasu dla dokumentu"""
        if document_id not in self.documents:
            return []
        
        timeline = []
        doc = self.documents[document_id]
        
        # Dodaj wydarzenia związane z dokumentem
        doc_events = [e for e in self.events if e.document_id == document_id]
        doc_events.sort(key=lambda x: x.timestamp)
        
        for event in doc_events:
            timeline.append({
                "timestamp": event.timestamp.isoformat(),
                "event_type": event.event_type,
                "description": event.description,
                "actor": event.actor,
                "metadata": event.metadata
            })
        
        return timeline
    
    def get_legislative_train(self) -> Dict[str, Any]:
        """
        Generuje wizualizację 'Legislative Train' (jak Legislative Train Schedule)
        Każdy pociąg = priorytet polityczny, wagony = projekty legislacyjne
        """
        trains = {}
        
        # Grupuj dokumenty według priorytetów (z metadanych)
        for doc_id, doc in self.documents.items():
            priority = doc.metadata.get("priority", "other")
            
            if priority not in trains:
                trains[priority] = {
                    "priority": priority,
                    "name": doc.metadata.get("priority_name", priority),
                    "wagons": []
                }
            
            # Status jako pozycja na trasie (0.0 - 1.0)
            status_index = LEGISLATIVE_STATUSES.index(doc.status.value) if doc.status.value in LEGISLATIVE_STATUSES else 0
            progress = status_index / (len(LEGISLATIVE_STATUSES) - 1) if len(LEGISLATIVE_STATUSES) > 1 else 0.0
            
            trains[priority]["wagons"].append({
                "id": doc_id,
                "title": doc.title,
                "status": doc.status.value,
                "progress": progress,
                "current_stage": doc.current_stage,
                "version": doc.version
            })
        
        return {
            "trains": list(trains.values()),
            "total_documents": len(self.documents),
            "generated_at": datetime.now().isoformat()
        }
    
    def analyze_dependencies(self, document_id: str) -> Dict[str, Any]:
        """Analiza zależności między dokumentami"""
        if document_id not in self.documents:
            return {}
        
        doc = self.documents[document_id]
        
        # Znajdź dokumenty zależne
        dependent_docs = []
        for other_id, other_doc in self.documents.items():
            if document_id in other_doc.dependencies:
                dependent_docs.append({
                    "id": other_id,
                    "title": other_doc.title,
                    "status": other_doc.status.value
                })
        
        # Znajdź dokumenty powiązane
        related_docs = []
        for related_id in doc.related_documents:
            if related_id in self.documents:
                related_docs.append({
                    "id": related_id,
                    "title": self.documents[related_id].title,
                    "status": self.documents[related_id].status.value
                })
        
        return {
            "document_id": document_id,
            "dependencies": [
                {
                    "id": dep_id,
                    "title": self.documents[dep_id].title,
                    "status": self.documents[dep_id].status.value
                }
                for dep_id in doc.dependencies if dep_id in self.documents
            ],
            "dependent_documents": dependent_docs,
            "related_documents": related_docs,
            "dependency_count": len(doc.dependencies),
            "impact_score": len(dependent_docs) * 0.1  # Prosty wskaźnik wpływu
        }
    
    def get_all_documents(self, status_filter: Optional[LegislativeStatus] = None) -> List[Dict[str, Any]]:
        """Pobranie wszystkich dokumentów z opcjonalnym filtrem statusu"""
        docs = list(self.documents.values())
        
        if status_filter:
            docs = [d for d in docs if d.status == status_filter]
        
        return [doc.to_dict() for doc in docs]
    
    def search_documents(self, query: str) -> List[Dict[str, Any]]:
        """Wyszukiwanie dokumentów po tytule i opisie"""
        query_lower = query.lower()
        results = []
        
        for doc in self.documents.values():
            if (query_lower in doc.title.lower() or 
                query_lower in doc.description.lower()):
                results.append(doc.to_dict())
        
        return results


