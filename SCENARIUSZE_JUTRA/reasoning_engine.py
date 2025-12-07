"""
Reasoning Engine - silnik wnioskowania z priorytetyzacją wag
Wielowariantowe wnioskowanie i symulacja przyszłych ścieżek
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import logging
from datetime import datetime

from data_analyzer import AnalyzedFact, Correlation
from knowledge_representation import KnowledgeGraph, Concept, Relation
from chain_of_thought import ChainOfThought, ReasoningStep, ReasoningStepType, CausalRelation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WeightedFactor:
    """Czynnik z wagą"""
    factor_id: str
    description: str
    weight: float
    impact_direction: str  # 'positive', 'negative', 'neutral'
    timeframe: str  # 'immediate', 'short', 'medium', 'long'
    related_facts: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)


@dataclass
class ReasoningPath:
    """Ścieżka rozumowania prowadząca do wniosku"""
    path_id: str
    factors_sequence: List[str]  # Kolejność zastosowanych czynników
    causal_chain: List[CausalRelation]
    conclusion: str
    confidence: float
    probability: float


class ReasoningEngine:
    """
    Silnik wnioskowania z priorytetyzacją wag
    """
    
    def __init__(self, config: Dict, atlantis_profile: Dict):
        self.config = config
        self.atlantis_profile = atlantis_profile
        self.weighted_factors: Dict[str, WeightedFactor] = {}
        self.reasoning_paths: List[ReasoningPath] = []
        self.chain_of_thought = ChainOfThought(initial_goal="reasoning_for_scenarios")
    
    def register_situation_factors(self, factors: Dict[str, Dict]):
        """
        Rejestruje czynniki sytuacyjne z wagami
        factors: {'a': {'description': '...', 'weight': 30}, ...}
        """
        for factor_id, factor_data in factors.items():
            weight = factor_data.get('weight', 0)
            description = factor_data.get('description', '')
            
            # Określenie kierunku wpływu
            impact_direction = self._determine_impact_direction(description)
            
            # Określenie horyzontu czasowego
            timeframe = self._extract_timeframe(description)
            
            self.weighted_factors[factor_id] = WeightedFactor(
                factor_id=factor_id,
                description=description,
                weight=weight,
                impact_direction=impact_direction,
                timeframe=timeframe,
                related_facts=[],
                related_concepts=[]
            )
            
            # Rejestracja w chain of thought
            self.chain_of_thought.register_key_factor(
                factor_id,
                weight,
                impact_direction
            )
        
        logger.info(f"Zarejestrowano {len(self.weighted_factors)} czynników z wagami")
    
    def _determine_impact_direction(self, description: str) -> str:
        """Określa kierunek wpływu na podstawie opisu"""
        desc_lower = description.lower()
        
        negative_keywords = ['kryzys', 'spadek', 'załamanie', 'utrata', 'embargo', 'atak', 'zagrożenie']
        positive_keywords = ['wzrost', 'rozwój', 'sukces', 'zwiększenie', 'inwestycje', 'odbudowa']
        
        if any(kw in desc_lower for kw in negative_keywords):
            return 'negative'
        elif any(kw in desc_lower for kw in positive_keywords):
            return 'positive'
        
        return 'neutral'
    
    def _extract_timeframe(self, description: str) -> str:
        """Ekstraktuje horyzont czasowy z opisu"""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ['natychmiast', 'obecnie', 'teraz']):
            return 'immediate'
        elif any(word in desc_lower for word in ['krótkoterminowy', 'miesiące', 'tygodnie']):
            return 'short'
        elif any(word in desc_lower for word in ['średnioterminowy', 'rok', 'lata']):
            return 'medium'
        elif any(word in desc_lower for word in ['długoterminowy', 'przyszłość', 'dekada']):
            return 'long'
        
        return 'medium'
    
    def prioritize_facts(
        self, 
        facts: List[AnalyzedFact], 
        knowledge_graph: KnowledgeGraph
    ) -> List[AnalyzedFact]:
        """
        Priorytetyzuje fakty na podstawie wag czynników
        """
        logger.info(f"Priorytetyzacja {len(facts)} faktów...")
        
        # Obliczenie score dla każdego faktu
        for fact in facts:
            priority_score = 0.0
            
            # 1. Relewantność bazowa
            priority_score += fact.relevance_score * 0.3
            
            # 2. Pewność źródła
            priority_score += fact.confidence * 0.2
            
            # 3. Związek z ważonymi czynnikami
            for factor_id, factor in self.weighted_factors.items():
                # Sprawdzenie czy fakt dotyczy tego czynnika
                if self._fact_matches_factor(fact, factor):
                    # Mnożenie przez wagę (znormalizowaną)
                    normalized_weight = factor.weight / 100.0  # Wagi są 5-30, normalizacja do 0-1
                    priority_score += normalized_weight * 0.4
                    
                    # Zapisanie powiązania
                    if fact.content not in factor.related_facts:
                        factor.related_facts.append(fact.content[:100])  # Skrócona wersja
            
            # 4. Centralność w grafie wiedzy
            if knowledge_graph:
                for concept_name in knowledge_graph.fact_to_concepts.get(fact.content[:50], []):
                    importance = knowledge_graph.get_concept_importance(concept_name)
                    priority_score += importance * 0.1
            
            # Aktualizacja score (można dodać pole do AnalyzedFact)
            fact.relevance_score = min(priority_score, 1.0)
        
        # Sortowanie po priorytecie
        prioritized = sorted(facts, key=lambda f: f.relevance_score, reverse=True)
        
        # Rejestracja w chain of thought
        self.chain_of_thought.add_step(ReasoningStep(
            step_type=ReasoningStepType.PRIORITIZATION,
            content=f"Priorytetyzacja {len(facts)} faktów na podstawie wag czynników",
            facts_used=[f.content[:50] for f in prioritized[:20]],
            weights_applied={fid: f.weight for fid, f in self.weighted_factors.items()},
            confidence=0.8
        ))
        
        return prioritized
    
    def _fact_matches_factor(self, fact: AnalyzedFact, factor: WeightedFactor) -> bool:
        """Sprawdza czy fakt dotyczy danego czynnika"""
        fact_lower = fact.content.lower()
        desc_lower = factor.description.lower()
        
        # Ekstrakcja kluczowych słów z opisu czynnika
        key_words = set(desc_lower.split())
        # Usunięcie słów pomocniczych
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        key_words = {w for w in key_words if w not in stop_words and len(w) > 3}
        
        # Sprawdzenie czy któreś słowo kluczowe występuje w fakcie
        return any(word in fact_lower for word in key_words)
    
    def build_causal_chains(
        self,
        knowledge_graph: KnowledgeGraph,
        target_concept: str = "Atlantis"
    ) -> List[CausalRelation]:
        """
        Buduje łańcuchy przyczynowo-skutkowe prowadzące do Atlantis
        """
        logger.info("Budowanie łańcuchów przyczynowo-skutkowych...")
        
        causal_relations = []
        
        # Dla każdego ważonego czynnika
        for factor_id, factor in self.weighted_factors.items():
            # Znajdź koncepty związane z czynnikiem
            related_concepts = factor.related_concepts
            
            if not related_concepts and knowledge_graph:
                # Próba znalezienia konceptów w grafie
                for concept_name, concept in knowledge_graph.concepts.items():
                    if self._concept_matches_factor(concept, factor):
                        related_concepts.append(concept_name)
            
            # Dla każdego powiązanego konceptu, znajdź ścieżkę do Atlantis
            for source_concept in related_concepts:
                if source_concept == target_concept:
                    continue
                
                paths = knowledge_graph.find_causal_paths(source_concept, target_concept)
                
                for path in paths:
                    # Budowa relacji przyczynowej dla całej ścieżki
                    if len(path) >= 2:
                        # Relacja bezpośrednia (pierwszy → ostatni)
                        causal_relations.append(CausalRelation(
                            cause=path[0],
                            effect=target_concept,
                            strength=factor.weight / 100.0,  # Normalizacja wagi
                            timeframe=factor.timeframe,
                            explanation=f"Czynnik {factor_id} ({factor.description[:100]}) prowadzi przez {len(path)-1} kroków do {target_concept}",
                            supporting_facts=factor.related_facts
                        ))
        
        # Rejestracja w chain of thought
        for rel in causal_relations:
            self.chain_of_thought.add_causal_relation(rel)
        
        self.chain_of_thought.add_step(ReasoningStep(
            step_type=ReasoningStepType.CAUSAL_INFERENCE,
            content=f"Zbudowano {len(causal_relations)} łańcuchów przyczynowo-skutkowych",
            correlations_used=[],
            confidence=0.75
        ))
        
        return causal_relations
    
    def _concept_matches_factor(self, concept: Concept, factor: WeightedFactor) -> bool:
        """Sprawdza czy koncept pasuje do czynnika"""
        concept_attrs = str(concept.attributes).lower()
        desc_lower = factor.description.lower()
        
        # Proste dopasowanie słów kluczowych
        key_words = set(desc_lower.split())
        key_words = {w for w in key_words if len(w) > 3}
        
        return any(word in concept_attrs or word in concept.name.lower() for word in key_words)
    
    def simulate_future_paths(
        self,
        timeframe_months: int,
        scenario_type: str,
        knowledge_graph: KnowledgeGraph,
        top_facts: List[AnalyzedFact]
    ) -> List[ReasoningPath]:
        """
        Symuluje przyszłe ścieżki rozwoju sytuacji
        """
        logger.info(f"Symulacja ścieżek dla {timeframe_months}m, typ: {scenario_type}")
        
        reasoning_paths = []
        
        # Grupowanie czynników po horyzoncie czasowym
        immediate_factors = [f for f in self.weighted_factors.values() if f.timeframe == 'immediate']
        short_factors = [f for f in self.weighted_factors.values() if f.timeframe == 'short']
        medium_factors = [f for f in self.weighted_factors.values() if f.timeframe == 'medium']
        long_factors = [f for f in self.weighted_factors.values() if f.timeframe == 'long']
        
        # Wybór odpowiednich czynników dla horyzontu czasowego
        if timeframe_months <= 12:
            relevant_factors = immediate_factors + short_factors
        else:
            relevant_factors = medium_factors + long_factors
        
        # Filtrowanie po typie scenariusza
        if scenario_type == 'positive':
            relevant_factors = [f for f in relevant_factors if f.impact_direction != 'negative']
        else:
            relevant_factors = [f for f in relevant_factors if f.impact_direction != 'positive']
        
        # Sortowanie po wadze
        relevant_factors.sort(key=lambda f: f.weight, reverse=True)
        
        # Generowanie ścieżek rozumowania
        for i, factor in enumerate(relevant_factors[:5]):  # Top 5 czynników
            # Budowa łańcucha przyczynowego dla tego czynnika
            causal_chain = []
            
            if knowledge_graph:
                # Znajdź ścieżki w grafie
                for concept_name in factor.related_concepts:
                    paths = knowledge_graph.find_causal_paths(concept_name, "Atlantis")
                    for path in paths:
                        # Konwersja na CausalRelation
                        if len(path) >= 2:
                            causal_chain.append(CausalRelation(
                                cause=path[0],
                                effect="Atlantis",
                                strength=factor.weight / 100.0,
                                timeframe=factor.timeframe,
                                explanation=f"Ścieżka przez {len(path)-1} kroków",
                                supporting_facts=factor.related_facts
                            ))
            
            # Obliczenie prawdopodobieństwa i pewności
            probability = self._calculate_path_probability(factor, scenario_type, timeframe_months)
            confidence = min(0.9, factor.weight / 100.0 * 1.2)
            
            # Wniosek
            conclusion = self._generate_conclusion(factor, scenario_type, timeframe_months)
            
            reasoning_path = ReasoningPath(
                path_id=f"path_{i+1}",
                factors_sequence=[factor.factor_id],
                causal_chain=causal_chain,
                conclusion=conclusion,
                confidence=confidence,
                probability=probability
            )
            
            reasoning_paths.append(reasoning_path)
        
        self.reasoning_paths = reasoning_paths
        
        # Rejestracja w chain of thought
        self.chain_of_thought.add_step(ReasoningStep(
            step_type=ReasoningStepType.SCENARIO_GENERATION,
            content=f"Symulacja {len(reasoning_paths)} ścieżek dla scenariusza {scenario_type}",
            facts_used=[],
            correlations_used=[],
            confidence=sum(p.confidence for p in reasoning_paths) / len(reasoning_paths) if reasoning_paths else 0.5
        ))
        
        return reasoning_paths
    
    def _calculate_path_probability(
        self, 
        factor: WeightedFactor, 
        scenario_type: str, 
        timeframe_months: int
    ) -> float:
        """Oblicza prawdopodobieństwo realizacji ścieżki"""
        base_prob = factor.weight / 100.0
        
        # Korekta dla typu scenariusza
        if scenario_type == 'positive' and factor.impact_direction == 'positive':
            base_prob *= 1.2
        elif scenario_type == 'negative' and factor.impact_direction == 'negative':
            base_prob *= 1.2
        else:
            base_prob *= 0.8
        
        # Korekta dla horyzontu czasowego
        if timeframe_months <= 12 and factor.timeframe in ['immediate', 'short']:
            base_prob *= 1.1
        elif timeframe_months > 12 and factor.timeframe in ['medium', 'long']:
            base_prob *= 1.1
        
        return min(base_prob, 0.95)
    
    def _generate_conclusion(
        self, 
        factor: WeightedFactor, 
        scenario_type: str, 
        timeframe_months: int
    ) -> str:
        """Generuje wniosek na podstawie czynnika"""
        direction = "pozytywny" if scenario_type == 'positive' else "negatywny"
        return f"Czynnik {factor.factor_id} ({factor.description[:100]}) prowadzi do {direction} scenariusza w horyzoncie {timeframe_months} miesięcy"
    
    def update_weights(self, new_weights: Dict[str, float]):
        """
        Aktualizuje wagi czynników (umożliwia ręczną korektę przez użytkownika)
        """
        for factor_id, new_weight in new_weights.items():
            if factor_id in self.weighted_factors:
                old_weight = self.weighted_factors[factor_id].weight
                self.weighted_factors[factor_id].weight = new_weight
                
                logger.info(f"Zaktualizowano wagę {factor_id}: {old_weight} → {new_weight}")
                
                # Rejestracja w chain of thought
                self.chain_of_thought.add_step(ReasoningStep(
                    step_type=ReasoningStepType.WEIGHT_APPLICATION,
                    content=f"Ręczna korekta wagi czynnika {factor_id}",
                    weights_applied={factor_id: new_weight},
                    confidence=1.0
                ))
    
    def get_weight_impact_analysis(self) -> Dict[str, Any]:
        """Analiza wpływu wag na wyniki"""
        analysis = {
            "total_factors": len(self.weighted_factors),
            "weight_distribution": {},
            "impact_by_direction": {"positive": 0, "negative": 0, "neutral": 0},
            "impact_by_timeframe": {"immediate": 0, "short": 0, "medium": 0, "long": 0}
        }
        
        for factor_id, factor in self.weighted_factors.items():
            analysis["weight_distribution"][factor_id] = factor.weight
            analysis["impact_by_direction"][factor.impact_direction] += factor.weight
            analysis["impact_by_timeframe"][factor.timeframe] += factor.weight
        
        return analysis

