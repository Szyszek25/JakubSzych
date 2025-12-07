"""
Explainability Layer - warstwa wyjaśnialności
NIE ujawnia surowego CoT, ale dostarcza przejrzyste wyjaśnienia dla użytkownika MSZ
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

from chain_of_thought import ChainOfThought
from reasoning_engine import ReasoningEngine, WeightedFactor
from knowledge_representation import KnowledgeGraph
from data_analyzer import AnalyzedFact

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Explanation:
    """Pojedyncze wyjaśnienie dla użytkownika"""
    title: str
    content: str
    supporting_data: Dict[str, Any] = None
    visualization_hint: Optional[str] = None


class ExplainabilityLayer:
    """
    Warstwa wyjaśnialności - tłumaczy mechanikę systemu użytkownikowi
    """
    
    def __init__(self, reasoning_engine: ReasoningEngine, knowledge_graph: KnowledgeGraph):
        self.reasoning_engine = reasoning_engine
        self.knowledge_graph = knowledge_graph
    
    def explain_key_factors(self) -> Explanation:
        """
        Wyjaśnia kluczowe czynniki i ich wagi
        """
        factors = self.reasoning_engine.weighted_factors
        
        # Sortowanie po wadze
        sorted_factors = sorted(
            factors.values(),
            key=lambda f: f.weight,
            reverse=True
        )
        
        content_parts = [
            "**Mechanika priorytetyzacji czynników:**",
            "",
            "System analizuje sytuację międzynarodową poprzez pryzmat 6 kluczowych czynników, "
            "każdy z przypisaną wagą istotności. Wagi określają, jak duży wpływ dany czynnik "
            "ma na finalne scenariusze.",
            "",
            "**Czynniki w kolejności ważności:**"
        ]
        
        for i, factor in enumerate(sorted_factors, 1):
            content_parts.append(
                f"{i}. **{factor.factor_id.upper()}** (waga: {factor.weight})"
            )
            content_parts.append(f"   - {factor.description}")
            content_parts.append(f"   - Kierunek wpływu: {factor.impact_direction}")
            content_parts.append(f"   - Horyzont czasowy: {factor.timeframe}")
            content_parts.append("")
        
        content_parts.append(
            "Użytkownik może ręcznie zmienić wagi, co automatycznie przeliczy scenariusze."
        )
        
        return Explanation(
            title="Kluczowe czynniki i ich wagi",
            content="\n".join(content_parts),
            supporting_data={
                "factors": [
                    {
                        "id": f.factor_id,
                        "weight": f.weight,
                        "description": f.description
                    }
                    for f in sorted_factors
                ]
            }
        )
    
    def explain_causal_relations(self) -> Explanation:
        """
        Wyjaśnia relacje przyczynowo-skutkowe
        """
        cot = self.reasoning_engine.chain_of_thought
        causal_relations = cot.causal_relations
        
        if not causal_relations:
            return Explanation(
                title="Relacje przyczynowo-skutkowe",
                content="Brak zidentyfikowanych relacji przyczynowo-skutkowych w analizie."
            )
        
        # Sortowanie po sile
        sorted_relations = sorted(causal_relations, key=lambda r: r.strength, reverse=True)
        
        content_parts = [
            "**Zidentyfikowane zależności przyczynowo-skutkowe:**",
            "",
            "System analizuje, jak poszczególne wydarzenia i trendy wpływają na siebie nawzajem "
            "oraz na sytuację państwa Atlantis. Poniżej przedstawiono kluczowe relacje:",
            ""
        ]
        
        for i, rel in enumerate(sorted_relations[:10], 1):  # Top 10
            content_parts.append(f"{i}. **{rel.cause}** → **{rel.effect}**")
            content_parts.append(f"   - Siła relacji: {rel.strength:.0%}")
            content_parts.append(f"   - Horyzont: {rel.timeframe}")
            content_parts.append(f"   - Wyjaśnienie: {rel.explanation}")
            content_parts.append(f"   - Fakty wspierające: {len(rel.supporting_facts)}")
            content_parts.append("")
        
        content_parts.append(
            "Te relacje stanowią podstawę dla generowanych scenariuszy. System symuluje różne "
            "ścieżki rozwoju sytuacji, uwzględniając te zależności."
        )
        
        return Explanation(
            title="Mechanika przyczynowo-skutkowa",
            content="\n".join(content_parts),
            supporting_data={
                "relations": [
                    {
                        "cause": r.cause,
                        "effect": r.effect,
                        "strength": r.strength,
                        "timeframe": r.timeframe
                    }
                    for r in sorted_relations[:10]
                ]
            },
            visualization_hint="graph"
        )
    
    def explain_data_to_conclusion_path(
        self,
        scenario_type: str,
        timeframe: int
    ) -> Explanation:
        """
        Wyjaśnia ścieżkę: dane → wniosek → rekomendacja
        """
        content_parts = [
            f"**Ścieżka rozumowania dla scenariusza {scenario_type} ({timeframe} miesięcy):**",
            "",
            "**Krok 1: Analiza faktów**",
            "- System analizuje zebrane dane z oficjalnych źródeł",
            "- Identyfikuje kluczowe informacje relewantne dla Atlantis",
            "- Ocenia wiarygodność i pewność każdego faktu",
            "",
            "**Krok 2: Priorytetyzacja**",
            "- Fakty są ważone zgodnie z wagami czynników sytuacyjnych",
            "- Czynniki o wyższej wadze mają większy wpływ na finalne scenariusze",
            "- System identyfikuje top 30-50 najważniejszych faktów",
            "",
            "**Krok 3: Wykrywanie korelacji**",
            "- System buduje graf wiedzy reprezentujący relacje między konceptami",
            "- Wykrywa zależności przyczynowo-skutkowe, czasowe i tematyczne",
            "- Rozwiązuje konflikty informacyjne",
            "",
            "**Krok 4: Wnioskowanie**",
            "- Na podstawie ważonych faktów i korelacji system buduje ścieżki rozumowania",
            "- Symuluje różne warianty rozwoju sytuacji",
            "- Oblicza prawdopodobieństwa różnych wydarzeń",
            "",
            "**Krok 5: Generowanie scenariusza**",
            f"- System generuje scenariusz {scenario_type} dla horyzontu {timeframe} miesięcy",
            "- Scenariusz uwzględnia mechanikę przyczynowo-skutkową",
            "- Zawiera kluczowe wydarzenia, prawdopodobieństwa i wpływy",
            "",
            "**Krok 6: Rekomendacje**",
            "- Na podstawie scenariusza system generuje rekomendacje strategiczne",
            "- Rekomendacje wskazują konkretne działania dla rządu Atlantis"
        ]
        
        return Explanation(
            title="Ścieżka: dane → wniosek → rekomendacja",
            content="\n".join(content_parts)
        )
    
    def explain_weight_impact(self, factor_id: str, old_weight: float, new_weight: float) -> Explanation:
        """
        Wyjaśnia wpływ zmiany wagi na wyniki
        """
        factor = self.reasoning_engine.weighted_factors.get(factor_id)
        
        if not factor:
            return Explanation(
                title="Wpływ zmiany wagi",
                content=f"Czynnik {factor_id} nie został znaleziony."
            )
        
        weight_change = new_weight - old_weight
        change_percent = (weight_change / old_weight * 100) if old_weight > 0 else 0
        
        content_parts = [
            f"**Wpływ zmiany wagi czynnika {factor_id.upper()}:**",
            "",
            f"- Stara waga: {old_weight}",
            f"- Nowa waga: {new_weight}",
            f"- Zmiana: {weight_change:+.1f} ({change_percent:+.1f}%)",
            "",
            "**Jak to wpływa na scenariusze:**",
            "",
            f"1. **Priorytetyzacja faktów**: Faktów związanych z tym czynnikiem będzie teraz "
            f"{'wyższy' if weight_change > 0 else 'niższy'} priorytet w analizie.",
            "",
            f"2. **Łańcuchy przyczynowe**: Relacje przyczynowo-skutkowe związane z tym czynnikiem "
            f"będą miały {'większą' if weight_change > 0 else 'mniejszą'} siłę.",
            "",
            f"3. **Scenariusze**: {factor.description[:100]} będzie miał "
            f"{'większy' if weight_change > 0 else 'mniejszy'} wpływ na finalne scenariusze.",
            "",
            "**Aby zobaczyć zmiany:**",
            "- System automatycznie przeliczy scenariusze z nowymi wagami",
            "- Porównaj nowe scenariusze z poprzednimi, aby zobaczyć różnice"
        ]
        
        return Explanation(
            title=f"Wpływ zmiany wagi {factor_id.upper()}",
            content="\n".join(content_parts),
            supporting_data={
                "factor_id": factor_id,
                "old_weight": old_weight,
                "new_weight": new_weight,
                "change": weight_change
            }
        )
    
    def generate_full_explanation(
        self,
        scenario_type: str,
        timeframe: int,
        top_facts: List[AnalyzedFact]
    ) -> Dict[str, Any]:
        """
        Generuje pełne wyjaśnienie dla użytkownika
        """
        explanations = {
            "key_factors": self.explain_key_factors(),
            "causal_relations": self.explain_causal_relations(),
            "reasoning_path": self.explain_data_to_conclusion_path(scenario_type, timeframe),
            "top_facts_used": self._explain_top_facts(top_facts),
            "weight_impact_analysis": self._explain_weight_impact_analysis()
        }
        
        return explanations
    
    def _explain_top_facts(self, top_facts: List[AnalyzedFact]) -> Explanation:
        """Wyjaśnia najważniejsze fakty użyte w analizie"""
        content_parts = [
            "**Najważniejsze fakty użyte w analizie:**",
            "",
            "Poniżej przedstawiono top 10 faktów, które miały największy wpływ na generowane scenariusze:",
            ""
        ]
        
        for i, fact in enumerate(top_facts[:10], 1):
            content_parts.append(f"{i}. **Relewantność: {fact.relevance_score:.0%}**")
            content_parts.append(f"   - {fact.content[:200]}...")
            content_parts.append(f"   - Źródło: {fact.source[:80]}...")
            content_parts.append(f"   - Pewność: {fact.confidence:.0%}")
            content_parts.append(f"   - Sentyment: {fact.sentiment}")
            content_parts.append("")
        
        return Explanation(
            title="Kluczowe fakty w analizie",
            content="\n".join(content_parts)
        )
    
    def _explain_weight_impact_analysis(self) -> Explanation:
        """Wyjaśnia analizę wpływu wag"""
        analysis = self.reasoning_engine.get_weight_impact_analysis()
        
        content_parts = [
            "**Analiza wpływu wag na wyniki:**",
            "",
            f"Łączna liczba czynników: {analysis['total_factors']}",
            "",
            "**Rozkład wpływu według kierunku:**",
            f"- Pozytywny: {analysis['impact_by_direction']['positive']}",
            f"- Negatywny: {analysis['impact_by_direction']['negative']}",
            f"- Neutralny: {analysis['impact_by_direction']['neutral']}",
            "",
            "**Rozkład wpływu według horyzontu czasowego:**",
            f"- Natychmiastowy: {analysis['impact_by_timeframe']['immediate']}",
            f"- Krótkoterminowy: {analysis['impact_by_timeframe']['short']}",
            f"- Średnioterminowy: {analysis['impact_by_timeframe']['medium']}",
            f"- Długoterminowy: {analysis['impact_by_timeframe']['long']}"
        ]
        
        return Explanation(
            title="Analiza wpływu wag",
            content="\n".join(content_parts),
            supporting_data=analysis
        )

