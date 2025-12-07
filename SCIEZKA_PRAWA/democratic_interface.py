"""
GQPA Democratic Interface
Interfejs dla obywateli do śledzenia konsultacji społecznych
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class NotificationType(Enum):
    """Typy powiadomień"""
    NEW_CONSULTATION = "new_consultation"
    DEADLINE_APPROACHING = "deadline_approaching"
    STATUS_CHANGED = "status_changed"
    DOCUMENT_UPDATED = "document_updated"
    IMPACT_ANALYSIS_READY = "impact_analysis_ready"


@dataclass
class Consultation:
    """Konsultacje społeczne"""
    id: str
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    document_id: str
    status: str = "active"  # active, closed, upcoming
    participants_count: int = 0
    submissions_count: int = 0
    simplified_description: Optional[str] = None
    plain_language_summary: Optional[str] = None


@dataclass
class CitizenNotification:
    """Powiadomienie dla obywatela"""
    id: str
    type: NotificationType
    title: str
    message: str
    document_id: Optional[str] = None
    consultation_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    read: bool = False
    priority: str = "normal"  # low, normal, high, urgent


@dataclass
class CitizenProfile:
    """Profil obywatela"""
    user_id: str
    interests: List[str]  # Obszary zainteresowań
    notification_preferences: Dict[str, bool]
    subscribed_documents: List[str] = field(default_factory=list)
    language_preference: str = "pl"
    accessibility_needs: List[str] = field(default_factory=list)


class DemocraticInterface:
    """
    Interfejs demokratyczny dla obywateli
    Umożliwia śledzenie konsultacji i zrozumienie procesów legislacyjnych
    """
    
    def __init__(self):
        self.consultations: Dict[str, Consultation] = {}
        self.notifications: Dict[str, List[CitizenNotification]] = {}  # user_id -> notifications
        self.profiles: Dict[str, CitizenProfile] = {}
        
    def register_consultation(self, consultation: Consultation) -> bool:
        """Rejestracja nowych konsultacji społecznych"""
        if consultation.id in self.consultations:
            return False
        
        self.consultations[consultation.id] = consultation
        
        # Wyślij powiadomienia do zainteresowanych użytkowników
        self._notify_new_consultation(consultation)
        
        return True
    
    def _notify_new_consultation(self, consultation: Consultation):
        """Wysyła powiadomienia o nowych konsultacjach"""
        for user_id, profile in self.profiles.items():
            # Sprawdź czy użytkownik jest zainteresowany
            if self._is_user_interested(profile, consultation):
                notification = CitizenNotification(
                    id=f"notif_{datetime.now().timestamp()}",
                    type=NotificationType.NEW_CONSULTATION,
                    title=f"Nowe konsultacje: {consultation.title}",
                    message=f"Rozpoczęły się konsultacje społeczne. Termin: {consultation.end_date.strftime('%Y-%m-%d')}",
                    consultation_id=consultation.id,
                    document_id=consultation.document_id,
                    priority="high"
                )
                
                if user_id not in self.notifications:
                    self.notifications[user_id] = []
                self.notifications[user_id].append(notification)
    
    def _is_user_interested(self, profile: CitizenProfile, consultation: Consultation) -> bool:
        """Sprawdza czy użytkownik jest zainteresowany konsultacjami"""
        # Sprawdź czy dokument jest w subskrypcjach
        if consultation.document_id in profile.subscribed_documents:
            return True
        
        # Sprawdź czy tematyka pasuje do zainteresowań
        consultation_lower = (consultation.title + " " + consultation.description).lower()
        for interest in profile.interests:
            if interest.lower() in consultation_lower:
                return True
        
        return False
    
    def get_active_consultations(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Pobiera aktywne konsultacje"""
        now = datetime.now()
        active = [
            c for c in self.consultations.values()
            if c.start_date <= now <= c.end_date and c.status == "active"
        ]
        
        # Jeśli podano user_id, filtruj według zainteresowań
        if user_id and user_id in self.profiles:
            profile = self.profiles[user_id]
            active = [c for c in active if self._is_user_interested(profile, c)]
        
        return [self._consultation_to_dict(c) for c in active]
    
    def get_upcoming_consultations(self, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """Pobiera nadchodzące konsultacje"""
        now = datetime.now()
        future = now + timedelta(days=days_ahead)
        
        upcoming = [
            c for c in self.consultations.values()
            if c.start_date > now and c.start_date <= future
        ]
        
        return [self._consultation_to_dict(c) for c in upcoming]
    
    def _consultation_to_dict(self, consultation: Consultation) -> Dict[str, Any]:
        """Konwersja konsultacji do słownika"""
        return {
            "id": consultation.id,
            "title": consultation.title,
            "description": consultation.description,
            "simplified_description": consultation.simplified_description,
            "plain_language_summary": consultation.plain_language_summary,
            "start_date": consultation.start_date.isoformat(),
            "end_date": consultation.end_date.isoformat(),
            "document_id": consultation.document_id,
            "status": consultation.status,
            "participants_count": consultation.participants_count,
            "submissions_count": consultation.submissions_count,
            "days_remaining": (consultation.end_date - datetime.now()).days if consultation.end_date > datetime.now() else 0
        }
    
    def subscribe_to_document(self, user_id: str, document_id: str) -> bool:
        """Subskrypcja użytkownika do dokumentu"""
        if user_id not in self.profiles:
            return False
        
        if document_id not in self.profiles[user_id].subscribed_documents:
            self.profiles[user_id].subscribed_documents.append(document_id)
        
        return True
    
    def unsubscribe_from_document(self, user_id: str, document_id: str) -> bool:
        """Anulowanie subskrypcji"""
        if user_id not in self.profiles:
            return False
        
        if document_id in self.profiles[user_id].subscribed_documents:
            self.profiles[user_id].subscribed_documents.remove(document_id)
        
        return True
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Pobiera powiadomienia użytkownika"""
        if user_id not in self.notifications:
            return []
        
        notifications = self.notifications[user_id]
        
        if unread_only:
            notifications = [n for n in notifications if not n.read]
        
        # Sortuj według priorytetu i czasu
        notifications.sort(key=lambda n: (
            {"urgent": 0, "high": 1, "normal": 2, "low": 3}.get(n.priority, 2),
            n.timestamp
        ))
        
        return [self._notification_to_dict(n) for n in notifications]
    
    def _notification_to_dict(self, notification: CitizenNotification) -> Dict[str, Any]:
        """Konwersja powiadomienia do słownika"""
        return {
            "id": notification.id,
            "type": notification.type.value,
            "title": notification.title,
            "message": notification.message,
            "document_id": notification.document_id,
            "consultation_id": notification.consultation_id,
            "timestamp": notification.timestamp.isoformat(),
            "read": notification.read,
            "priority": notification.priority
        }
    
    def mark_notification_read(self, user_id: str, notification_id: str) -> bool:
        """Oznacza powiadomienie jako przeczytane"""
        if user_id not in self.notifications:
            return False
        
        for notification in self.notifications[user_id]:
            if notification.id == notification_id:
                notification.read = True
                return True
        
        return False
    
    def create_user_profile(self, user_id: str, interests: List[str],
                           language_preference: str = "pl") -> CitizenProfile:
        """Tworzy profil użytkownika"""
        profile = CitizenProfile(
            user_id=user_id,
            interests=interests,
            notification_preferences={
                "new_consultation": True,
                "deadline_approaching": True,
                "status_changed": True,
                "document_updated": False
            },
            language_preference=language_preference
        )
        
        self.profiles[user_id] = profile
        self.notifications[user_id] = []
        
        return profile
    
    def get_document_explanation(self, document_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generuje wyjaśnienie dokumentu dla obywatela
        Wykorzystuje Plain Language Engine
        """
        # W pełnej implementacji integruje się z PlainLanguageEngine
        return {
            "document_id": document_id,
            "simple_explanation": "Ten dokument reguluje...",
            "key_points": [
                "Punkt 1: ...",
                "Punkt 2: ...",
                "Punkt 3: ..."
            ],
            "what_you_can_do": [
                "Możesz wziąć udział w konsultacjach społecznych",
                "Możesz zgłosić swoje uwagi",
                "Możesz śledzić postęp prac"
            ],
            "deadlines": [],
            "related_consultations": []
        }
    
    def get_legislative_process_guide(self) -> Dict[str, Any]:
        """Zwraca przewodnik po procesie legislacyjnym"""
        return {
            "stages": [
                {
                    "name": "Prekonsultacje",
                    "description": "Wczesne konsultacje przed przygotowaniem projektu",
                    "duration": "2-4 tygodnie",
                    "what_happens": "Zbieranie wstępnych opinii od interesariuszy"
                },
                {
                    "name": "Konsultacje społeczne",
                    "description": "Publiczne konsultacje projektu",
                    "duration": "3-6 tygodni",
                    "what_happens": "Obywatele mogą zgłaszać uwagi do projektu"
                },
                {
                    "name": "Projekt rządowy",
                    "description": "Projekt przygotowany przez rząd",
                    "duration": "Zależnie od złożoności",
                    "what_happens": "Projekt trafia do Rady Ministrów"
                },
                {
                    "name": "Sejm",
                    "description": "Proces legislacyjny w Sejmie",
                    "duration": "Kilka miesięcy",
                    "what_happens": "Trzy czytania projektu w Sejmie"
                },
                {
                    "name": "Senat",
                    "description": "Proces w Senacie",
                    "duration": "1-2 miesiące",
                    "what_happens": "Senat może wprowadzić poprawki"
                },
                {
                    "name": "Podpis Prezydenta",
                    "description": "Podpisanie ustawy przez Prezydenta",
                    "duration": "21 dni",
                    "what_happens": "Prezydent podpisuje lub zawetuje ustawę"
                },
                {
                    "name": "Wejście w życie",
                    "description": "Ustawa wchodzi w życie",
                    "duration": "Zazwyczaj 14-30 dni po publikacji",
                    "what_happens": "Ustawa staje się obowiązującym prawem"
                }
            ],
            "how_to_participate": [
                "Śledź konsultacje społeczne na tej platformie",
                "Zgłaszaj swoje uwagi w terminie",
                "Bądź na bieżąco z postępem prac",
                "Korzystaj z uproszczonych wyjaśnień dokumentów"
            ]
        }

