"""
GQPA Impact Simulator
Moduł analizy skutków regulacji
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from config import IMPACT_TYPES


class ImpactType(Enum):
    """Typy analizy wpływu"""
    FINANSOWY = "finansowy"
    SPOLECZNY = "spoleczny"
    TECHNOLOGICZNY = "technologiczny"
    OPERACYJNY = "operacyjny"
    PRAWNY = "prawny"
    EKONOMICZNY = "ekonomiczny"


@dataclass
class ImpactAnalysis:
    """Analiza wpływu regulacji"""
    document_id: str
    impact_type: ImpactType
    severity: float  # 0.0 - 1.0 (niski - wysoki)
    description: str
    affected_entities: List[str]  # Kto jest dotknięty
    estimated_cost: Optional[float] = None  # Szacowany koszt (jeśli dotyczy)
    time_horizon: str = "krotkoterminowy"  # krotkoterminowy, srednioterminowy, dlugoterminowy
    risks: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImpactScenario:
    """Scenariusz wpływu regulacji"""
    name: str
    probability: float  # 0.0 - 1.0
    impacts: List[ImpactAnalysis]
    description: str
    key_indicators: List[str]


class ImpactSimulator:
    """
    Symulator wpływu regulacji
    Wykorzystuje GQPA do modelowania skutków decyzji
    """
    
    def __init__(self):
        self.analyses: Dict[str, List[ImpactAnalysis]] = {}  # document_id -> analyses
        self.scenarios: Dict[str, List[ImpactScenario]] = {}  # document_id -> scenarios
        
    def analyze_impact(self, document_id: str, document_text: str,
                       impact_types: Optional[List[ImpactType]] = None) -> List[ImpactAnalysis]:
        """
        Analizuje wpływ regulacji
        
        Args:
            document_id: ID dokumentu
            document_text: Tekst dokumentu
            impact_types: Typy analizy do wykonania (jeśli None, wszystkie)
        """
        if impact_types is None:
            impact_types = [ImpactType(t) for t in IMPACT_TYPES]
        
        analyses = []
        
        for impact_type in impact_types:
            analysis = self._analyze_single_impact(document_id, document_text, impact_type)
            analyses.append(analysis)
        
        # Zapisz analizy
        if document_id not in self.analyses:
            self.analyses[document_id] = []
        self.analyses[document_id].extend(analyses)
        
        return analyses
    
    def _analyze_single_impact(self, document_id: str, document_text: str,
                               impact_type: ImpactType) -> ImpactAnalysis:
        """
        Analizuje pojedynczy typ wpływu
        W pełnej implementacji używa GQPA do głębokiej analizy semantycznej
        """
        # Uproszczona analiza oparta na słowach kluczowych
        # W pełnej wersji użyjemy GQPA CognitiveAgent do analizy
        
        text_lower = document_text.lower()
        
        # Wykrywanie słów kluczowych dla różnych typów wpływu
        keywords_map = {
            ImpactType.FINANSOWY: ["koszt", "wydatek", "budżet", "finansowanie", "środki", "kwota"],
            ImpactType.SPOLECZNY: ["obywatel", "społeczeństwo", "grupa", "osoba", "prawo", "dostęp"],
            ImpactType.TECHNOLOGICZNY: ["system", "technologia", "cyfryzacja", "platforma", "aplikacja"],
            ImpactType.OPERACYJNY: ["procedura", "proces", "działanie", "realizacja", "wdrożenie"],
            ImpactType.PRAWNY: ["przepis", "ustawa", "rozporządzenie", "art.", "paragraf"],
            ImpactType.EKONOMICZNY: ["gospodarka", "rynek", "przedsiębiorstwo", "inwestycja", "wzrost"]
        }
        
        keywords = keywords_map.get(impact_type, [])
        matches = sum(1 for keyword in keywords if keyword in text_lower)
        
        # Oblicz severity na podstawie liczby dopasowań
        severity = min(1.0, matches / max(1, len(keywords)) * 0.5 + 0.3)
        
        # Wygeneruj opis (w pełnej wersji użyjemy LLM)
        description = self._generate_impact_description(document_text, impact_type, severity)
        
        # Wykryj dotknięte podmioty (uproszczone)
        affected_entities = self._detect_affected_entities(document_text, impact_type)
        
        # Szacuj koszt (jeśli dotyczy)
        estimated_cost = None
        if impact_type == ImpactType.FINANSOWY:
            estimated_cost = self._estimate_cost(document_text)
        
        # Wykryj ryzyka i możliwości
        risks = self._detect_risks(document_text, impact_type)
        opportunities = self._detect_opportunities(document_text, impact_type)
        
        # Generuj rekomendacje
        recommendations = self._generate_recommendations(impact_type, severity, risks)
        
        # Określ horyzont czasowy
        time_horizon = self._determine_time_horizon(document_text)
        
        return ImpactAnalysis(
            document_id=document_id,
            impact_type=impact_type,
            severity=severity,
            description=description,
            affected_entities=affected_entities,
            estimated_cost=estimated_cost,
            time_horizon=time_horizon,
            risks=risks,
            opportunities=opportunities,
            recommendations=recommendations
        )
    
    def _generate_impact_description(self, text: str, impact_type: ImpactType, 
                                     severity: float) -> str:
        """Generuje opis wpływu"""
        # Uproszczona wersja - w pełnej implementacji użyjemy GQPA LLM
        descriptions = {
            ImpactType.FINANSOWY: f"Regulacja ma {'wysoki' if severity > 0.7 else 'średni' if severity > 0.4 else 'niski'} wpływ finansowy.",
            ImpactType.SPOLECZNY: f"Regulacja wpływa na {'dużą' if severity > 0.7 else 'średnią' if severity > 0.4 else 'małą'} grupę społeczną.",
            ImpactType.TECHNOLOGICZNY: f"Regulacja wymaga {'znacznych' if severity > 0.7 else 'umiarkowanych' if severity > 0.4 else 'minimalnych'} zmian technologicznych.",
            ImpactType.OPERACYJNY: f"Regulacja wpływa na {'znaczące' if severity > 0.7 else 'umiarkowane' if severity > 0.4 else 'minimalne'} zmiany operacyjne.",
            ImpactType.PRAWNY: f"Regulacja wprowadza {'istotne' if severity > 0.7 else 'średnie' if severity > 0.4 else 'drobne'} zmiany prawne.",
            ImpactType.EKONOMICZNY: f"Regulacja ma {'znaczący' if severity > 0.7 else 'umiarkowany' if severity > 0.4 else 'minimalny'} wpływ ekonomiczny."
        }
        
        return descriptions.get(impact_type, "Analiza wpływu wymaga szczegółowego przeglądu.")
    
    def _detect_affected_entities(self, text: str, impact_type: ImpactType) -> List[str]:
        """Wykrywa dotknięte podmioty"""
        # Uproszczona wersja - w pełnej implementacji użyjemy NER (Named Entity Recognition)
        entities = []
        
        entity_patterns = {
            "ministerstwo": r"ministerstw[ao]\s+\w+",
            "urząd": r"urzą[d]\s+\w+",
            "organ": r"organ\s+\w+",
            "jednostka": r"jednostk[ai]\s+\w+"
        }
        
        import re
        for entity_type, pattern in entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities.extend(matches[:3])  # Maksymalnie 3 na typ
        
        return list(set(entities))[:10]  # Unikalne, maksymalnie 10
    
    def _estimate_cost(self, text: str) -> Optional[float]:
        """Szacuje koszt (uproszczone)"""
        import re
        # Szukaj wzmianek o kwotach
        cost_patterns = [
            r"(\d+)\s*(mln|milion|tys|tysiąc)\s*(zł|PLN)",
            r"kwot[ay]\s+(\d+)",
            r"(\d+)\s*(mln|milion)"
        ]
        
        for pattern in cost_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Uproszczone - zwróć pierwszą znalezioną wartość
                # W pełnej wersji potrzebna lepsza ekstrakcja
                return 1000000.0  # Placeholder
        
        return None
    
    def _detect_risks(self, text: str, impact_type: ImpactType) -> List[str]:
        """Wykrywa ryzyka"""
        # Uproszczona wersja - w pełnej implementacji użyjemy GQPA do analizy
        risks = []
        text_lower = text.lower()
        
        risk_indicators = ["ryzyko", "zagrożenie", "niebezpieczeństwo", "problem", "utrudnienie"]
        if any(indicator in text_lower for indicator in risk_indicators):
            risks.append("Wykryto potencjalne ryzyka w regulacji")
        
        return risks
    
    def _detect_opportunities(self, text: str, impact_type: ImpactType) -> List[str]:
        """Wykrywa możliwości"""
        opportunities = []
        text_lower = text.lower()
        
        opportunity_indicators = ["możliwość", "szansa", "korzyść", "poprawa", "rozwój"]
        if any(indicator in text_lower for indicator in opportunity_indicators):
            opportunities.append("Wykryto potencjalne możliwości w regulacji")
        
        return opportunities
    
    def _generate_recommendations(self, impact_type: ImpactType, severity: float,
                                 risks: List[str]) -> List[str]:
        """Generuje rekomendacje"""
        recommendations = []
        
        if severity > 0.7:
            recommendations.append("Zalecana szczegółowa analiza przed wdrożeniem")
            recommendations.append("Rozważenie fazowego wdrożenia")
        
        if risks:
            recommendations.append("Wymagane opracowanie planu zarządzania ryzykiem")
        
        return recommendations
    
    def _determine_time_horizon(self, text: str) -> str:
        """Określa horyzont czasowy"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["natychmiast", "od razu", "niezwłocznie"]):
            return "krotkoterminowy"
        elif any(word in text_lower for word in ["roku", "latach", "okresie"]):
            return "dlugoterminowy"
        else:
            return "srednioterminowy"
    
    def generate_scenarios(self, document_id: str, 
                          analyses: Optional[List[ImpactAnalysis]] = None) -> List[ImpactScenario]:
        """
        Generuje scenariusze wpływu regulacji
        Wykorzystuje GQPA do symulacji różnych wariantów
        """
        if analyses is None:
            analyses = self.analyses.get(document_id, [])
        
        if not analyses:
            return []
        
        scenarios = []
        
        # Scenariusz bazowy (najbardziej prawdopodobny)
        baseline = ImpactScenario(
            name="Scenariusz Bazowy",
            probability=0.6,
            impacts=analyses,
            description="Najbardziej prawdopodobny scenariusz wpływu regulacji",
            key_indicators=["Średni wpływ na wszystkie obszary", "Standardowe wdrożenie"]
        )
        scenarios.append(baseline)
        
        # Scenariusz optymistyczny
        optimistic_impacts = [
            ImpactAnalysis(
                document_id=a.document_id,
                impact_type=a.impact_type,
                severity=max(0.0, a.severity - 0.2),  # Niższy wpływ
                description=f"Optymistyczna wersja: {a.description}",
                affected_entities=a.affected_entities,
                estimated_cost=a.estimated_cost * 0.8 if a.estimated_cost else None,
                time_horizon=a.time_horizon,
                risks=[],
                opportunities=a.opportunities + ["Dodatkowe korzyści z optymalizacji"],
                recommendations=a.recommendations
            )
            for a in analyses
        ]
        
        optimistic = ImpactScenario(
            name="Scenariusz Optymistyczny",
            probability=0.25,
            impacts=optimistic_impacts,
            description="Scenariusz z niższym wpływem i większymi korzyściami",
            key_indicators=["Niższe koszty", "Szybsze wdrożenie", "Więcej korzyści"]
        )
        scenarios.append(optimistic)
        
        # Scenariusz pesymistyczny (czarny łabędź)
        pessimistic_impacts = [
            ImpactAnalysis(
                document_id=a.document_id,
                impact_type=a.impact_type,
                severity=min(1.0, a.severity + 0.3),  # Wyższy wpływ
                description=f"Pesymistyczna wersja: {a.description}",
                affected_entities=a.affected_entities,
                estimated_cost=a.estimated_cost * 1.5 if a.estimated_cost else None,
                time_horizon=a.time_horizon,
                risks=a.risks + ["Nieoczekiwane komplikacje", "Opóźnienia wdrożenia"],
                opportunities=[],
                recommendations=a.recommendations + ["Wymagane dodatkowe środki bezpieczeństwa"]
            )
            for a in analyses
        ]
        
        pessimistic = ImpactScenario(
            name="Scenariusz Pesymistyczny (Czarny Łabędź)",
            probability=0.15,
            impacts=pessimistic_impacts,
            description="Scenariusz z wyższym wpływem i większymi ryzykami",
            key_indicators=["Wyższe koszty", "Dłuższe wdrożenie", "Więcej ryzyk"]
        )
        scenarios.append(pessimistic)
        
        # Zapisz scenariusze
        if document_id not in self.scenarios:
            self.scenarios[document_id] = []
        self.scenarios[document_id] = scenarios
        
        return scenarios
    
    def get_impact_summary(self, document_id: str) -> Dict[str, Any]:
        """Pobiera podsumowanie analizy wpływu"""
        analyses = self.analyses.get(document_id, [])
        scenarios = self.scenarios.get(document_id, [])
        
        if not analyses:
            return {
                "document_id": document_id,
                "status": "no_analysis",
                "message": "Brak analizy wpływu dla tego dokumentu"
            }
        
        # Oblicz średnią severity
        avg_severity = sum(a.severity for a in analyses) / len(analyses) if analyses else 0.0
        
        # Znajdź najwyższy wpływ
        max_impact = max(analyses, key=lambda x: x.severity) if analyses else None
        
        # Oblicz całkowity szacowany koszt
        total_cost = sum(a.estimated_cost for a in analyses if a.estimated_cost)
        
        return {
            "document_id": document_id,
            "status": "analyzed",
            "total_analyses": len(analyses),
            "average_severity": avg_severity,
            "max_impact": {
                "type": max_impact.impact_type.value if max_impact else None,
                "severity": max_impact.severity if max_impact else 0.0,
                "description": max_impact.description if max_impact else None
            },
            "total_estimated_cost": total_cost if total_cost > 0 else None,
            "scenarios_count": len(scenarios),
            "generated_at": datetime.now().isoformat()
        }

