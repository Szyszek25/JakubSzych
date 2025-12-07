"""
Główny orchestrator systemu Scenariusze Jutra
Koordynuje wszystkie moduły i dostarcza interfejs użytkownika
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gqpa_core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'system'))

from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import logging
from collections import deque

from config import (
    ATLANTIS_PROFILE, SCENARIO_WEIGHTS, ANALYSIS_CONFIG,
    TEMPERATURE_REALISTIC, OPENAI_API_KEY, OPENAI_MODEL
)

from data_collector import DataCollector, DataSource
from data_analyzer import DataAnalyzer, AnalyzedFact, Correlation
from knowledge_representation import KnowledgeGraph, KnowledgeExtractor
from reasoning_engine import ReasoningEngine
from scenario_generator import ScenarioGenerator, ScenarioInput, Scenario
from recommendation_engine import RecommendationEngine
from explainability_layer import ExplainabilityLayer
from anti_poisoning import AntiPoisoningSystem
from chain_of_thought import ChainOfThought

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScenarioOrchestrator:
    """
    Główny orchestrator systemu analizy foresightowej
    """
    
    def __init__(self, config: Dict, openai_api_key: str, gemini_model=None):
        self.config = config
        self.openai_api_key = openai_api_key
        self.gemini_model = gemini_model
        
        # Inicjalizacja modułów
        logger.info("Inicjalizacja modułów systemu...")
        
        # 1. Data Ingestion Layer
        self.data_collector = DataCollector(config)
        self.anti_poisoning = AntiPoisoningSystem(config.get("ANTI_POISONING_CONFIG", {}))
        
        # 2. Knowledge Representation Layer
        self.knowledge_graph = KnowledgeGraph()
        self.knowledge_extractor = KnowledgeExtractor(ATLANTIS_PROFILE)
        
        # 3. Reasoning Engine
        self.reasoning_engine = ReasoningEngine(config, ATLANTIS_PROFILE)
        
        # 4. Scenario Generator
        self.scenario_generator = ScenarioGenerator(config, openai_api_key, gemini_model)
        
        # 5. Recommendation Engine
        self.recommendation_engine = RecommendationEngine(
            self.reasoning_engine,
            self.knowledge_graph
        )
        
        # 6. Explainability Layer
        self.explainability = ExplainabilityLayer(
            self.reasoning_engine,
            self.knowledge_graph
        )
        
        # Pamięć promptów (10 ostatnich)
        self.prompt_memory = deque(maxlen=ANALYSIS_CONFIG.get("memory_size", 10))
        
        logger.info("✅ Wszystkie moduły zainicjalizowane")
    
    def run_full_analysis(
        self,
        situation_factors: Dict[str, Dict],
        collect_data: bool = True
    ) -> Dict[str, Any]:
        """
        Uruchamia pełną analizę: zbieranie danych → analiza → scenariusze → rekomendacje
        """
        logger.info("=" * 80)
        logger.info("ROZPOCZĘCIE PEŁNEJ ANALIZY FORESIGHTOWEJ")
        logger.info("=" * 80)
        
        # KROK 1: Zbieranie danych
        if collect_data:
            logger.info("\n[KROK 1] Zbieranie danych ze źródeł...")
            data_sources = self.data_collector.collect_all_data()
            logger.info(f"Zebrano {len(data_sources)} źródeł danych")
        else:
            # Użycie przykładowych danych (dla demo)
            data_sources = self._get_demo_data()
            logger.info(f"Używam danych demo: {len(data_sources)} źródeł")
        
        # KROK 2: Ochrona przed data poisoning
        logger.info("\n[KROK 2] Weryfikacja danych i ochrona przed data poisoning...")
        clean_data, poisoned_data = self.anti_poisoning.filter_poisoned_data([
            {
                "id": f"source_{i}",
                "source": s.url,
                "content": s.content,
                "date": str(s.date) if s.date else "unknown"
            }
            for i, s in enumerate(data_sources)
        ])
        logger.info(f"Zweryfikowano: {len(clean_data)} czystych, {len(poisoned_data)} zanieczyszczonych")
        
        # KROK 3: Analiza danych
        logger.info("\n[KROK 3] Analiza danych...")
        data_analyzer = DataAnalyzer(self.config, self.openai_api_key)
        analyzed_facts = data_analyzer.analyze_data(clean_data, ATLANTIS_PROFILE)
        correlations = data_analyzer.find_correlations()
        logger.info(f"Przeanalizowano {len(analyzed_facts)} faktów, znaleziono {len(correlations)} korelacji")
        
        # KROK 4: Budowa grafu wiedzy
        logger.info("\n[KROK 4] Budowa grafu wiedzy...")
        concepts = self.knowledge_extractor.extract_concepts_from_facts([
            {
                "id": f"fact_{i}",
                "content": f.content,
                "entities": f.entities,
                "tags": f.tags
            }
            for i, f in enumerate(analyzed_facts)
        ])
        
        for concept in concepts:
            self.knowledge_graph.add_concept(concept)
            # Linkowanie faktów do konceptów
            for fact in analyzed_facts:
                if any(entity in concept.name for entity in fact.entities):
                    self.knowledge_graph.link_fact_to_concept(fact.content[:50], concept.name)
        
        relations = self.knowledge_extractor.extract_relations_from_facts([
            {
                "id": f"fact_{i}",
                "content": f.content,
                "entities": f.entities
            }
            for i, f in enumerate(analyzed_facts)
        ], concepts)
        
        for relation in relations:
            self.knowledge_graph.add_relation(relation)
        
        logger.info(f"Zbudowano graf: {len(concepts)} konceptów, {len(relations)} relacji")
        
        # KROK 5: Rejestracja czynników sytuacyjnych
        logger.info("\n[KROK 5] Rejestracja czynników sytuacyjnych z wagami...")
        self.reasoning_engine.register_situation_factors(situation_factors)
        
        # KROK 6: Priorytetyzacja faktów
        logger.info("\n[KROK 6] Priorytetyzacja faktów na podstawie wag...")
        priority_facts = self.reasoning_engine.prioritize_facts(
            analyzed_facts,
            self.knowledge_graph
        )
        logger.info(f"Wyselekcjonowano {len(priority_facts[:50])} faktów priorytetowych")
        
        # KROK 7: Budowa łańcuchów przyczynowo-skutkowych
        logger.info("\n[KROK 7] Budowa łańcuchów przyczynowo-skutkowych...")
        causal_chains = self.reasoning_engine.build_causal_chains(self.knowledge_graph)
        logger.info(f"Zbudowano {len(causal_chains)} łańcuchów przyczynowo-skutkowych")
        
        # KROK 8: Generowanie scenariuszy
        logger.info("\n[KROK 8] Generowanie scenariuszy...")
        scenario_input = ScenarioInput(
            situation_factors=situation_factors,
            atlantis_profile=ATLANTIS_PROFILE,
            analyzed_facts=analyzed_facts,
            correlations=correlations,
            priority_facts=priority_facts[:50]
        )
        
        scenarios = self.scenario_generator.generate_all_scenarios(scenario_input)
        logger.info(f"Wygenerowano {len(scenarios)} scenariuszy")
        
        # KROK 9: Generowanie rekomendacji
        logger.info("\n[KROK 9] Generowanie rekomendacji strategicznych...")
        recommendations = self.recommendation_engine.generate_recommendations(
            scenarios,
            ATLANTIS_PROFILE
        )
        logger.info(f"Wygenerowano {len(recommendations['avoid_negative'])} rekomendacji unikających negatywnych scenariuszy")
        logger.info(f"Wygenerowano {len(recommendations['pursue_positive'])} rekomendacji realizujących pozytywne scenariusze")
        
        # KROK 10: Generowanie raportu końcowego
        logger.info("\n[KROK 10] Generowanie raportu końcowego...")
        final_report = self.scenario_generator.generate_final_report(scenarios, scenario_input)
        
        # Dodanie rekomendacji do raportu
        recommendations_text = self.recommendation_engine.format_recommendations_for_report(recommendations)
        final_report += "\n\n" + recommendations_text
        
        logger.info("\n" + "=" * 80)
        logger.info("ANALIZA ZAKOŃCZONA POMYŚLNIE")
        logger.info("=" * 80)
        
        return {
            "scenarios": scenarios,
            "recommendations": recommendations,
            "report": final_report,
            "statistics": {
                "data_sources": len(data_sources),
                "analyzed_facts": len(analyzed_facts),
                "correlations": len(correlations),
                "concepts": len(concepts),
                "relations": len(relations),
                "causal_chains": len(causal_chains)
            },
            "explainability": self._generate_explainability_summary(scenarios[0] if scenarios else None)
        }
    
    def _get_demo_data(self) -> List[DataSource]:
        """Zwraca przykładowe dane dla demo (gdy nie ma dostępu do zbierania danych)"""
        from data_collector import DataSource
        
        demo_sources = [
            DataSource(
                url="https://example.com/demo1",
                title="Demo Source 1",
                content="Przykładowa treść źródła danych dotycząca sytuacji międzynarodowej.",
                date=datetime.now(),
                source_type="institution",
                language="en"
            )
        ]
        
        return demo_sources
    
    def _generate_explainability_summary(self, sample_scenario: Optional[Scenario]) -> Dict[str, Any]:
        """Generuje podsumowanie wyjaśnialności"""
        if not sample_scenario:
            return {}
        
        explanations = self.explainability.generate_full_explanation(
            sample_scenario.scenario_type,
            sample_scenario.timeframe_months,
            []  # Top facts - można dodać
        )
        
        return {
            "key_factors": explanations["key_factors"].content,
            "causal_relations": explanations["causal_relations"].content,
            "reasoning_path": explanations["reasoning_path"].content
        }
    
    def update_weights_and_recalculate(
        self,
        new_weights: Dict[str, float],
        current_scenarios: List[Scenario]
    ) -> Dict[str, Any]:
        """
        Aktualizuje wagi i przelicza scenariusze
        """
        logger.info("Aktualizacja wag i przeliczanie scenariuszy...")
        
        # Aktualizacja wag
        self.reasoning_engine.update_weights(new_weights)
        
        # Wyjaśnienie wpływu zmian
        impact_explanations = {}
        for factor_id, new_weight in new_weights.items():
            old_weight = self.reasoning_engine.weighted_factors.get(factor_id, {}).weight if hasattr(self.reasoning_engine.weighted_factors.get(factor_id), 'weight') else 0
            explanation = self.explainability.explain_weight_impact(
                factor_id,
                old_weight,
                new_weight
            )
            impact_explanations[factor_id] = explanation.content
        
        return {
            "weights_updated": new_weights,
            "impact_explanations": impact_explanations,
            "message": "Wagi zaktualizowane. Uruchom ponownie analizę, aby zobaczyć nowe scenariusze."
        }
    
    def get_prompt_memory(self) -> List[Dict]:
        """Zwraca historię ostatnich promptów"""
        return list(self.prompt_memory)


def create_situation_factors_from_weights() -> Dict[str, Dict]:
    """
    Tworzy słownik czynników sytuacyjnych na podstawie wag z config
    """
    factors = {
        "a": {
            "description": "Wskutek zaistniałej przed miesiącem katastrofy naturalnej wiodący światowy producent procesorów graficznych stracił 60% zdolności produkcyjnych; odbudowa mocy produkcyjnych poprzez inwestycje w filie zlokalizowane na obszarach nieobjętych katastrofą potrwa do końca roku 2028",
            "weight": SCENARIO_WEIGHTS["a"]
        },
        "b": {
            "description": "Przemysł motoryzacyjny w Europie bardzo wolno przestawia się na produkcję samochodów elektrycznych; rynek europejski zalewają tanie samochody elektryczne z Azji Wschodniej; europejski przemysł motoryzacyjny będzie miał w roku 2025 zyski na poziomie 30% średnich rocznych zysków z lat 2020-2024",
            "weight": SCENARIO_WEIGHTS["b"]
        },
        "c": {
            "description": "PKB krajów strefy euro w roku 2025 spadnie średnio o 1,5% w stosunku do roku 2024",
            "weight": SCENARIO_WEIGHTS["c"]
        },
        "d": {
            "description": "Na wschodzie Ukrainy trwa słaby rozejm; Rosja kontroluje dwie główne elektrownie ukraińskie, które pracują na potrzeby konsumentów rosyjskich; gospodarka ukraińska rozwija się w tempie 4% PKB, głównie dzięki inwestycjom w przemysł zbrojeniowy i odbudowę infrastruktury",
            "weight": SCENARIO_WEIGHTS["d"]
        },
        "e": {
            "description": "Inwestycje amerykańskie w Ukrainie kierowane są do przemysłu wydobywczego (surowce krytyczne); roczne inwestycje UE w Ukrainie są na poziomie 3% ukraińskiego PKB i utrzymają się na takim poziomie do roku 2029",
            "weight": SCENARIO_WEIGHTS["e"]
        },
        "f": {
            "description": "Mamy gwałtowny wzrost udziału energii z OZE w miksie energetycznym krajów UE oraz Chin od początku roku 2028; w połowie roku 2023 średniej wielkości kraj południowoamerykański odkrył ogromne i łatwe do eksploatacji złoża ropy naftowej i gazu ziemnego dorównujące wielkością złożom Arabii Saudyjskiej i Kataru, co przełoży się pod koniec roku 2027 na nadpodaż tych paliw na światowe rynki; wzrost podaży energii z OZE oraz nadpodaż paliw węglowodorowych przekładają się na znaczny spadek cen ropy: do poziomu 30-35 USD za baryłkę; będzie to miało wpływ na budżet Rosji oraz (w mniejszym stopniu) innych krajów producentów ropy i paliw ropopochodnych",
            "weight": SCENARIO_WEIGHTS["f"]
        }
    }
    
    return factors


if __name__ == "__main__":
    # Demo flow
    logger.info("🚀 Uruchamianie systemu Scenariusze Jutra...")
    
    # Konfiguracja
    config = {
        "OPENAI_MODEL": OPENAI_MODEL,
        "TEMPERATURE_REALISTIC": TEMPERATURE_REALISTIC,
        "ANALYSIS_CONFIG": ANALYSIS_CONFIG,
        "ANTI_POISONING_CONFIG": {
            "min_source_count": 3,
            "source_verification": True,
            "cross_reference_sources": True
        }
    }
    
    # Inicjalizacja orchestratora
    orchestrator = ScenarioOrchestrator(config, OPENAI_API_KEY, gemini_model=None)
    
    # Przygotowanie czynników sytuacyjnych
    situation_factors = create_situation_factors_from_weights()
    
    # Uruchomienie analizy (bez zbierania danych - demo)
    results = orchestrator.run_full_analysis(situation_factors, collect_data=False)
    
    # Zapisanie raportu
    report_file = f"raport_atlantis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(results["report"])
    
    logger.info(f"\n✅ Raport zapisany do: {report_file}")
    logger.info(f"📊 Statystyki: {results['statistics']}")

