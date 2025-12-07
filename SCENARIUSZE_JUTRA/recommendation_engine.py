"""
Recommendation Engine - generuje rekomendacje strategiczne
Decyzje minimalizujące ryzyka i wzmacniające scenariusze pozytywne
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

from scenario_generator import Scenario
from reasoning_engine import ReasoningEngine
from knowledge_representation import KnowledgeGraph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Recommendation:
    """Pojedyncza rekomendacja strategiczna"""
    recommendation_id: str
    title: str
    description: str
    category: str  # 'political', 'economic', 'security', 'diplomatic', 'technological'
    priority: str  # 'high', 'medium', 'low'
    timeframe: str  # 'immediate', 'short_term', 'medium_term', 'long_term'
    target_scenario: str  # 'avoid_negative', 'pursue_positive', 'both'
    related_factors: List[str] = field(default_factory=list)
    expected_impact: str = ""
    implementation_steps: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)


class RecommendationEngine:
    """
    Silnik generujący rekomendacje strategiczne dla państwa Atlantis
    """
    
    def __init__(self, reasoning_engine: ReasoningEngine, knowledge_graph: KnowledgeGraph):
        self.reasoning_engine = reasoning_engine
        self.knowledge_graph = knowledge_graph
        self.recommendations: List[Recommendation] = []
    
    def generate_recommendations(
        self,
        scenarios: List[Scenario],
        atlantis_profile: Dict
    ) -> Dict[str, List[Recommendation]]:
        """
        Generuje rekomendacje na podstawie scenariuszy
        Zwraca słownik: {'avoid_negative': [...], 'pursue_positive': [...]}
        """
        logger.info("Generowanie rekomendacji strategicznych...")
        
        negative_scenarios = [s for s in scenarios if s.scenario_type == "negative"]
        positive_scenarios = [s for s in scenarios if s.scenario_type == "positive"]
        
        # Rekomendacje unikające scenariuszy negatywnych
        avoid_negative = self._generate_avoid_negative_recommendations(
            negative_scenarios,
            atlantis_profile
        )
        
        # Rekomendacje realizujące scenariusze pozytywne
        pursue_positive = self._generate_pursue_positive_recommendations(
            positive_scenarios,
            atlantis_profile
        )
        
        self.recommendations = avoid_negative + pursue_positive
        
        return {
            "avoid_negative": avoid_negative,
            "pursue_positive": pursue_positive
        }
    
    def _generate_avoid_negative_recommendations(
        self,
        negative_scenarios: List[Scenario],
        atlantis_profile: Dict
    ) -> List[Recommendation]:
        """Generuje rekomendacje unikające scenariuszy negatywnych"""
        recommendations = []
        
        # Analiza wspólnych zagrożeń z negatywnych scenariuszy
        common_threats = self._extract_common_threats(negative_scenarios)
        
        # Dla każdego zagrożenia generuj rekomendację
        for i, threat in enumerate(common_threats):
            rec = self._create_mitigation_recommendation(
                threat,
                f"mitigation_{i+1}",
                atlantis_profile
            )
            recommendations.append(rec)
        
        # Rekomendacje na podstawie kluczowych wydarzeń z negatywnych scenariuszy
        for scenario in negative_scenarios:
            for event in scenario.key_events[:3]:  # Top 3 wydarzenia
                rec = self._create_event_based_recommendation(
                    event,
                    scenario,
                    "avoid",
                    atlantis_profile
                )
                if rec:
                    recommendations.append(rec)
        
        # Sortowanie po priorytecie
        recommendations.sort(key=lambda r: self._priority_to_number(r.priority), reverse=True)
        
        return recommendations[:15]  # Top 15 rekomendacji
    
    def _generate_pursue_positive_recommendations(
        self,
        positive_scenarios: List[Scenario],
        atlantis_profile: Dict
    ) -> List[Recommendation]:
        """Generuje rekomendacje realizujące scenariusze pozytywne"""
        recommendations = []
        
        # Analiza wspólnych szans z pozytywnych scenariuszy
        common_opportunities = self._extract_common_opportunities(positive_scenarios)
        
        # Dla każdej szansy generuj rekomendację
        for i, opportunity in enumerate(common_opportunities):
            rec = self._create_opportunity_recommendation(
                opportunity,
                f"opportunity_{i+1}",
                atlantis_profile
            )
            recommendations.append(rec)
        
        # Rekomendacje na podstawie kluczowych wydarzeń z pozytywnych scenariuszy
        for scenario in positive_scenarios:
            for event in scenario.key_events[:3]:  # Top 3 wydarzenia
                rec = self._create_event_based_recommendation(
                    event,
                    scenario,
                    "pursue",
                    atlantis_profile
                )
                if rec:
                    recommendations.append(rec)
        
        # Sortowanie po priorytecie
        recommendations.sort(key=lambda r: self._priority_to_number(r.priority), reverse=True)
        
        return recommendations[:15]  # Top 15 rekomendacji
    
    def _extract_common_threats(self, scenarios: List[Scenario]) -> List[Dict[str, Any]]:
        """Ekstraktuje wspólne zagrożenia z negatywnych scenariuszy"""
        threats = []
        
        # Analiza kluczowych wydarzeń
        all_events = []
        for scenario in scenarios:
            all_events.extend(scenario.key_events)
        
        # Grupowanie podobnych wydarzeń (uproszczone)
        threat_keywords = ['kryzys', 'spadek', 'atak', 'embargo', 'konflikt', 'zagrożenie']
        
        for event in all_events:
            event_lower = event.lower()
            if any(kw in event_lower for kw in threat_keywords):
                threats.append({
                    "description": event,
                    "scenarios_count": sum(1 for s in scenarios if event in s.key_events),
                    "severity": "high" if any(kw in event_lower for kw in ['kryzys', 'atak', 'embargo']) else "medium"
                })
        
        # Usunięcie duplikatów i sortowanie
        unique_threats = []
        seen = set()
        for threat in threats:
            threat_key = threat["description"][:50]
            if threat_key not in seen:
                seen.add(threat_key)
                unique_threats.append(threat)
        
        unique_threats.sort(key=lambda t: t["scenarios_count"], reverse=True)
        
        return unique_threats[:10]
    
    def _extract_common_opportunities(self, scenarios: List[Scenario]) -> List[Dict[str, Any]]:
        """Ekstraktuje wspólne szanse z pozytywnych scenariuszy"""
        opportunities = []
        
        # Analiza kluczowych wydarzeń
        all_events = []
        for scenario in scenarios:
            all_events.extend(scenario.key_events)
        
        # Grupowanie podobnych wydarzeń
        opportunity_keywords = ['wzrost', 'rozwój', 'inwestycje', 'współpraca', 'sukces', 'szansa']
        
        for event in all_events:
            event_lower = event.lower()
            if any(kw in event_lower for kw in opportunity_keywords):
                opportunities.append({
                    "description": event,
                    "scenarios_count": sum(1 for s in scenarios if event in s.key_events),
                    "potential": "high" if any(kw in event_lower for kw in ['wzrost', 'inwestycje']) else "medium"
                })
        
        # Usunięcie duplikatów i sortowanie
        unique_opportunities = []
        seen = set()
        for opp in opportunities:
            opp_key = opp["description"][:50]
            if opp_key not in seen:
                seen.add(opp_key)
                unique_opportunities.append(opp)
        
        unique_opportunities.sort(key=lambda o: o["scenarios_count"], reverse=True)
        
        return unique_opportunities[:10]
    
    def _create_mitigation_recommendation(
        self,
        threat: Dict[str, Any],
        rec_id: str,
        atlantis_profile: Dict
    ) -> Recommendation:
        """Tworzy rekomendację minimalizującą zagrożenie"""
        
        # Określenie kategorii na podstawie zagrożenia
        threat_desc = threat["description"].lower()
        
        if any(kw in threat_desc for kw in ['gospodarczy', 'ekonomiczny', 'handel', 'rynki']):
            category = "economic"
        elif any(kw in threat_desc for kw in ['bezpieczeństwo', 'wojskowy', 'atak', 'obrona']):
            category = "security"
        elif any(kw in threat_desc for kw in ['polityczny', 'dyplomatyczny', 'relacje']):
            category = "diplomatic"
        else:
            category = "political"
        
        # Generowanie kroków implementacji
        implementation_steps = [
            f"Monitorowanie rozwoju sytuacji związanej z: {threat['description'][:100]}",
            "Przygotowanie planu awaryjnego na wypadek realizacji zagrożenia",
            "Budowa koalicji z kluczowymi partnerami (Niemcy, Francja, USA)",
            "Dywersyfikacja zależności w obszarze zagrożenia"
        ]
        
        return Recommendation(
            recommendation_id=rec_id,
            title=f"Minimalizacja ryzyka: {threat['description'][:80]}",
            description=f"Rekomendacja minimalizująca ryzyko realizacji zagrożenia: {threat['description']}",
            category=category,
            priority=threat.get("severity", "medium"),
            timeframe="immediate" if threat.get("severity") == "high" else "short_term",
            target_scenario="avoid_negative",
            expected_impact=f"Zmniejszenie prawdopodobieństwa realizacji negatywnego scenariusza o 20-30%",
            implementation_steps=implementation_steps,
            risks=["Opóźnienie w implementacji może zwiększyć ryzyko"]
        )
    
    def _create_opportunity_recommendation(
        self,
        opportunity: Dict[str, Any],
        rec_id: str,
        atlantis_profile: Dict
    ) -> Recommendation:
        """Tworzy rekomendację realizującą szansę"""
        
        # Określenie kategorii
        opp_desc = opportunity["description"].lower()
        
        if any(kw in opp_desc for kw in ['gospodarczy', 'ekonomiczny', 'handel', 'inwestycje']):
            category = "economic"
        elif any(kw in opp_desc for kw in ['technologiczny', 'ai', 'cyfrowy', 'ict']):
            category = "technological"
        elif any(kw in opp_desc for kw in ['energetyczny', 'oze', 'klimat']):
            category = "economic"  # Można dodać 'energy'
        else:
            category = "political"
        
        # Generowanie kroków implementacji
        implementation_steps = [
            f"Aktywne wsparcie rozwoju sytuacji: {opportunity['description'][:100]}",
            "Alokacja zasobów strategicznych do realizacji szansy",
            "Budowa partnerstw z kluczowymi aktorami",
            "Monitoring postępów i dostosowanie strategii"
        ]
        
        return Recommendation(
            recommendation_id=rec_id,
            title=f"Realizacja szansy: {opportunity['description'][:80]}",
            description=f"Rekomendacja realizująca szansę: {opportunity['description']}",
            category=category,
            priority=opportunity.get("potential", "medium"),
            timeframe="short_term",
            target_scenario="pursue_positive",
            expected_impact=f"Zwiększenie prawdopodobieństwa realizacji pozytywnego scenariusza o 25-35%",
            implementation_steps=implementation_steps,
            risks=["Niewystarczające zasoby mogą ograniczyć realizację"]
        )
    
    def _create_event_based_recommendation(
        self,
        event: str,
        scenario: Scenario,
        action_type: str,  # 'avoid' lub 'pursue'
        atlantis_profile: Dict
    ) -> Optional[Recommendation]:
        """Tworzy rekomendację na podstawie konkretnego wydarzenia ze scenariusza"""
        
        event_lower = event.lower()
        
        # Określenie kategorii i priorytetu
        if any(kw in event_lower for kw in ['kryzys', 'spadek', 'atak']):
            category = "security" if 'atak' in event_lower else "economic"
            priority = "high"
        elif any(kw in event_lower for kw in ['wzrost', 'rozwój', 'inwestycje']):
            category = "economic"
            priority = "medium"
        else:
            category = "political"
            priority = "low"
        
        if action_type == "avoid":
            title = f"Zapobieganie: {event[:80]}"
            description = f"Rekomendacja zapobiegająca negatywnemu wydarzeniu: {event}"
            target = "avoid_negative"
            impact = "Zmniejszenie ryzyka realizacji negatywnego wydarzenia"
        else:
            title = f"Wsparcie: {event[:80]}"
            description = f"Rekomendacja wspierająca pozytywne wydarzenie: {event}"
            target = "pursue_positive"
            impact = "Zwiększenie szansy realizacji pozytywnego wydarzenia"
        
        return Recommendation(
            recommendation_id=f"event_{scenario.timeframe_months}_{scenario.scenario_type}_{len(self.recommendations)}",
            title=title,
            description=description,
            category=category,
            priority=priority,
            timeframe="immediate" if scenario.timeframe_months <= 12 else "medium_term",
            target_scenario=target,
            related_factors=[f"scenario_{scenario.timeframe_months}m"],
            expected_impact=impact,
            implementation_steps=[
                f"Monitorowanie rozwoju: {event}",
                "Przygotowanie odpowiedzi strategicznej",
                "Koordynacja z partnerami"
            ]
        )
    
    def _priority_to_number(self, priority: str) -> int:
        """Konwersja priorytetu na liczbę dla sortowania"""
        mapping = {"high": 3, "medium": 2, "low": 1}
        return mapping.get(priority, 0)
    
    def format_recommendations_for_report(
        self,
        recommendations: Dict[str, List[Recommendation]]
    ) -> str:
        """Formatuje rekomendacje do raportu końcowego"""
        
        text_parts = []
        
        # Rekomendacje unikające negatywnych scenariuszy
        text_parts.append("### Jakie decyzje pomogą uniknąć scenariuszy negatywnych:\n")
        
        for i, rec in enumerate(recommendations.get("avoid_negative", [])[:10], 1):
            text_parts.append(f"#### {i}. {rec.title}")
            text_parts.append(f"{rec.description}")
            text_parts.append(f"**Kategoria:** {rec.category}")
            text_parts.append(f"**Priorytet:** {rec.priority}")
            text_parts.append(f"**Horyzont:** {rec.timeframe}")
            text_parts.append(f"**Oczekiwany wpływ:** {rec.expected_impact}")
            text_parts.append("**Kroki implementacji:**")
            for step in rec.implementation_steps:
                text_parts.append(f"- {step}")
            if rec.risks:
                text_parts.append("**Ryzyka:**")
                for risk in rec.risks:
                    text_parts.append(f"- {risk}")
            text_parts.append("")
        
        # Rekomendacje realizujące pozytywne scenariusze
        text_parts.append("### Jakie decyzje pomogą w zrealizowaniu scenariuszy pozytywnych:\n")
        
        for i, rec in enumerate(recommendations.get("pursue_positive", [])[:10], 1):
            text_parts.append(f"#### {i}. {rec.title}")
            text_parts.append(f"{rec.description}")
            text_parts.append(f"**Kategoria:** {rec.category}")
            text_parts.append(f"**Priorytet:** {rec.priority}")
            text_parts.append(f"**Horyzont:** {rec.timeframe}")
            text_parts.append(f"**Oczekiwany wpływ:** {rec.expected_impact}")
            text_parts.append("**Kroki implementacji:**")
            for step in rec.implementation_steps:
                text_parts.append(f"- {step}")
            if rec.risks:
                text_parts.append("**Ryzyka:**")
                for risk in rec.risks:
                    text_parts.append(f"- {risk}")
            text_parts.append("")
        
        return "\n".join(text_parts)

