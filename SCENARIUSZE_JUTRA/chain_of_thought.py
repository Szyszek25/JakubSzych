"""
Moduł Chain of Thought - śledzenie ścieżki rozumowania
Dostarcza wyjaśnialność bez ujawniania surowego CoT
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class ReasoningStepType(Enum):
    """Typy kroków rozumowania"""
    FACT_ANALYSIS = "fact_analysis"
    CORRELATION_DETECTION = "correlation_detection"
    WEIGHT_APPLICATION = "weight_application"
    CAUSAL_INFERENCE = "causal_inference"
    SCENARIO_GENERATION = "scenario_generation"
    CONFLICT_RESOLUTION = "conflict_resolution"
    PRIORITIZATION = "prioritization"


@dataclass
class ReasoningStep:
    """Pojedynczy krok w łańcuchu rozumowania"""
    step_type: ReasoningStepType
    content: str
    facts_used: List[str] = field(default_factory=list)
    correlations_used: List[str] = field(default_factory=list)
    weights_applied: Dict[str, float] = field(default_factory=dict)
    confidence: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)
    causal_chain: Optional[str] = None
    impact_analysis: Optional[Dict[str, Any]] = None


@dataclass
class CausalRelation:
    """Relacja przyczynowo-skutkowa"""
    cause: str
    effect: str
    strength: float  # 0.0-1.0
    timeframe: str  # "short", "medium", "long"
    explanation: str
    supporting_facts: List[str] = field(default_factory=list)


class ChainOfThought:
    """
    Zarządza łańcuchem rozumowania z wyjaśnialnością
    NIE ujawnia surowego CoT, ale dostarcza przejrzyste wyjaśnienia
    """
    
    def __init__(self, initial_goal: str = ""):
        self.initial_goal = initial_goal
        self.steps: List[ReasoningStep] = []
        self.causal_relations: List[CausalRelation] = []
        self.key_factors: Dict[str, float] = {}  # Czynniki z wagami
        self.conflicts_detected: List[Dict] = []
        self.confidence_trajectory: List[float] = []
    
    def add_step(self, step: ReasoningStep):
        """Dodaje krok do łańcucha rozumowania"""
        self.steps.append(step)
        self.confidence_trajectory.append(step.confidence)
    
    def add_causal_relation(self, relation: CausalRelation):
        """Dodaje relację przyczynowo-skutkową"""
        self.causal_relations.append(relation)
    
    def register_key_factor(self, factor_name: str, weight: float, impact: str):
        """Rejestruje kluczowy czynnik z wagą i wpływem"""
        self.key_factors[factor_name] = {
            "weight": weight,
            "impact": impact,
            "used_in_steps": len([s for s in self.steps if factor_name in str(s.content)])
        }
    
    def detect_conflict(self, fact1_id: str, fact2_id: str, conflict_type: str, resolution: str):
        """Rejestruje wykryty konflikt i jego rozwiązanie"""
        self.conflicts_detected.append({
            "fact1": fact1_id,
            "fact2": fact2_id,
            "type": conflict_type,
            "resolution": resolution,
            "timestamp": datetime.now()
        })
    
    def get_summary(self) -> str:
        """Zwraca skrócone podsumowanie (dla promptów)"""
        if not self.steps:
            return "Brak dotychczasowych kroków rozumowania."
        
        summary = f"Cel: {self.initial_goal}\n"
        summary += f"Liczba kroków: {len(self.steps)}\n"
        summary += f"Kluczowe czynniki: {len(self.key_factors)}\n"
        summary += f"Relacje przyczynowe: {len(self.causal_relations)}\n"
        summary += f"Konflikty wykryte: {len(self.conflicts_detected)}\n"
        
        return summary
    
    def get_detailed_explanation(self) -> str:
        """
        Zwraca szczegółowe wyjaśnienie rozumowania
        NIE surowy CoT, ale przejrzyste wyjaśnienie dla użytkownika MSZ
        """
        explanation = []
        
        # 1. Kluczowe czynniki i ich wagi
        if self.key_factors:
            explanation.append("**Kluczowe czynniki uwzględnione w analizie:**")
            for factor, data in sorted(
                self.key_factors.items(), 
                key=lambda x: x[1]["weight"], 
                reverse=True
            ):
                explanation.append(
                    f"- {factor}: waga {data['weight']}, "
                    f"wpływ: {data['impact']}, "
                    f"użyty w {data['used_in_steps']} krokach analizy"
                )
            explanation.append("")
        
        # 2. Relacje przyczynowo-skutkowe
        if self.causal_relations:
            explanation.append("**Zidentyfikowane zależności przyczynowo-skutkowe:**")
            for rel in sorted(self.causal_relations, key=lambda x: x.strength, reverse=True)[:10]:
                explanation.append(
                    f"- {rel.cause} → {rel.effect} "
                    f"(siła: {rel.strength:.0%}, "
                    f"horyzont: {rel.timeframe}, "
                    f"fakty wspierające: {len(rel.supporting_facts)})"
                )
                if rel.explanation:
                    explanation.append(f"  Wyjaśnienie: {rel.explanation}")
            explanation.append("")
        
        # 3. Mechanika priorytetyzacji
        if self.steps:
            weight_steps = [s for s in self.steps if s.step_type == ReasoningStepType.WEIGHT_APPLICATION]
            if weight_steps:
                explanation.append("**Mechanika priorytetyzacji faktów:**")
                for step in weight_steps[:5]:
                    explanation.append(f"- {step.content}")
                    if step.weights_applied:
                        explanation.append(f"  Zastosowane wagi: {step.weights_applied}")
                explanation.append("")
        
        # 4. Rozwiązane konflikty
        if self.conflicts_detected:
            explanation.append("**Wykryte i rozwiązane konflikty informacyjne:**")
            for conflict in self.conflicts_detected[:5]:
                explanation.append(
                    f"- Konflikt typu {conflict['type']} między faktami "
                    f"{conflict['fact1']} i {conflict['fact2']}"
                )
                explanation.append(f"  Rozwiązanie: {conflict['resolution']}")
            explanation.append("")
        
        # 5. Ścieżka od danych do wniosków
        explanation.append("**Ścieżka rozumowania:**")
        explanation.append("1. Analiza faktów → identyfikacja kluczowych informacji")
        explanation.append("2. Wykrywanie korelacji → budowa grafu zależności")
        explanation.append("3. Aplikacja wag → priorytetyzacja czynników")
        explanation.append("4. Wnioskowanie przyczynowe → symulacja ścieżek")
        explanation.append("5. Generowanie scenariuszy → warianty przyszłości")
        
        # 6. Pewność analizy
        if self.confidence_trajectory:
            avg_confidence = sum(self.confidence_trajectory) / len(self.confidence_trajectory)
            explanation.append("")
            explanation.append(f"**Pewność analizy:** {avg_confidence:.0%}")
            explanation.append(f"(na podstawie {len(self.confidence_trajectory)} kroków analizy)")
        
        return "\n".join(explanation)
    
    def get_factor_impact_analysis(self) -> Dict[str, Any]:
        """Analiza wpływu poszczególnych czynników"""
        impact_analysis = {}
        
        for factor, data in self.key_factors.items():
            impact_analysis[factor] = {
                "weight": data["weight"],
                "usage_count": data["used_in_steps"],
                "related_causal_relations": len([
                    r for r in self.causal_relations 
                    if factor.lower() in r.cause.lower() or factor.lower() in r.effect.lower()
                ]),
                "impact_description": data["impact"]
            }
        
        return impact_analysis
    
    def export_for_explainability(self) -> Dict[str, Any]:
        """Eksportuje dane do warstwy wyjaśnialności (bez surowego CoT)"""
        return {
            "key_factors": self.key_factors,
            "causal_relations": [
                {
                    "cause": r.cause,
                    "effect": r.effect,
                    "strength": r.strength,
                    "timeframe": r.timeframe,
                    "explanation": r.explanation
                }
                for r in self.causal_relations
            ],
            "conflicts_resolved": len(self.conflicts_detected),
            "reasoning_path": "fakty → korelacje → wagi → wnioskowanie → scenariusze",
            "confidence": sum(self.confidence_trajectory) / len(self.confidence_trajectory) if self.confidence_trajectory else 0.5
        }

