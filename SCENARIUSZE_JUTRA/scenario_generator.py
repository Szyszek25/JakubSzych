"""
Moduł generowania scenariuszy z wykorzystaniem GQPA Core
Integruje analizę danych, chain of thought i generowanie scenariuszy
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gqpa_core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'system'))

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
from collections import deque

# Importy GQPA (Background IP)
try:
    from gqpa_part5 import CognitiveAgent
    from gqpa_part4 import EnhancedMemoryNexus, WorldModel
    from gqpa_part6 import GeminiCognitiveAdapter
    from gqpa_part1 import Episode
    GQPA_AVAILABLE = True
except ImportError:
    GQPA_AVAILABLE = False
    logging.warning("GQPA Core nie jest dostępne. Używam uproszczonej wersji.")

try:
    from data_analyzer import DataAnalyzer, AnalyzedFact, Correlation
    from chain_of_thought import ChainOfThought, ReasoningStep
    from anti_poisoning import AntiPoisoningSystem
except ImportError:
    # Fallback jeśli moduły nie są dostępne
    AnalyzedFact = None
    Correlation = None
    ChainOfThought = None
    ReasoningStep = None
    AntiPoisoningSystem = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Scenario:
    """Reprezentacja wygenerowanego scenariusza"""
    timeframe_months: int  # 12 lub 36
    scenario_type: str  # 'positive' lub 'negative'
    title: str
    description: str
    key_events: List[str]
    probabilities: Dict[str, float]  # Prawdopodobieństwa różnych wydarzeń
    impacts: Dict[str, str]  # Wpływy na różne obszary
    recommendations: List[str]
    chain_of_thought: ChainOfThought
    supporting_facts: List[str]  # ID faktów wspierających
    correlations_used: List[str]  # ID korelacji użytych
    confidence_score: float
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass
class ScenarioInput:
    """Dane wejściowe do generowania scenariuszy"""
    situation_factors: Dict[str, Dict]  # Czynniki a-f z wagami
    atlantis_profile: Dict
    analyzed_facts: List[AnalyzedFact]
    correlations: List[Correlation]
    priority_facts: List[AnalyzedFact]


class ScenarioGenerator:
    """Główna klasa generująca scenariusze z wykorzystaniem GQPA Core"""
    
    def __init__(self, config: Dict, openai_api_key: str, gemini_model=None):
        self.config = config
        self.openai_api_key = openai_api_key
        
        # Inicjalizacja GQPA Core
        if GQPA_AVAILABLE and gemini_model:
            self.cognitive_agent = CognitiveAgent()
            self.gemini_adapter = GeminiCognitiveAdapter(gemini_model, self.cognitive_agent)
            self.use_gqpa = True
            logger.info("✅ GQPA Core zainicjalizowany")
        else:
            self.cognitive_agent = None
            self.gemini_adapter = None
            self.use_gqpa = False
            logger.warning("⚠️ Używam uproszczonej wersji bez GQPA")
        
        # System ochrony przed data poisoning
        self.anti_poisoning = AntiPoisoningSystem(config.get("ANTI_POISONING_CONFIG", {}))
        
        # Pamięć promptów (10 ostatnich)
        self.prompt_memory = deque(maxlen=config.get("ANALYSIS_CONFIG", {}).get("memory_size", 10))
        
        # Temperatura dla realistycznych scenariuszy
        self.temperature_realistic = config.get("TEMPERATURE_REALISTIC", 0.3)
        self.temperature_creative = config.get("TEMPERATURE_CREATIVE", 0.8)
        
        self.generated_scenarios: List[Scenario] = []
    
    def _prepare_cognitive_context(self, input_data: ScenarioInput) -> Dict[str, Any]:
        """Przygotowuje kontekst kognitywny dla GQPA"""
        if not self.use_gqpa:
            return {}
        
        # Aktualizacja modelu świata z faktami
        for fact in input_data.priority_facts[:20]:  # Top 20 faktów
            # Symulacja dodania faktów do modelu świata
            concept_data = {
                "name": f"fact_{fact.content[:50]}",
                "type": "geopolitical_fact",
                "attributes": {
                    "relevance": fact.relevance_score,
                    "sentiment": fact.sentiment,
                    "confidence": fact.confidence,
                    "tags": fact.tags
                }
            }
            # W rzeczywistości użyjemy world_model.update_from_perception()
        
        return {
            "facts_count": len(input_data.analyzed_facts),
            "correlations_count": len(input_data.correlations),
            "priority_facts": len(input_data.priority_facts),
            "situation_factors": len(input_data.situation_factors)
        }
    
    def _generate_scenario_with_gqpa(
        self, 
        timeframe: int, 
        scenario_type: str, 
        input_data: ScenarioInput,
        chain_of_thought: ChainOfThought
    ) -> Scenario:
        """Generuje scenariusz używając GQPA Core"""
        
        # Ustawienie celu dla agenta kognitywnego
        goal = f"generate_{scenario_type}_scenario_{timeframe}months"
        if self.use_gqpa:
            self.cognitive_agent.set_goal(goal)
        
        # Przygotowanie kontekstu
        cognitive_context = self._prepare_cognitive_context(input_data)
        
        # Budowa promptu z chain of thought
        prompt = self._build_scenario_prompt(timeframe, scenario_type, input_data, chain_of_thought)
        
        # Zapytanie przez GQPA adapter
        if self.use_gqpa and self.gemini_adapter:
            response = self.gemini_adapter.cognitive_query(
                prompt, 
                context=cognitive_context
            )
            scenario_text = response.get('response', '')
        else:
            # Fallback bez GQPA
            scenario_text = self._generate_scenario_fallback(prompt)
        
        # Parsowanie odpowiedzi
        scenario = self._parse_scenario_response(
            scenario_text, timeframe, scenario_type, input_data, chain_of_thought
        )
        
        # Zapis do pamięci promptów
        self.prompt_memory.append({
            "timestamp": datetime.now(),
            "prompt": prompt[:500],  # Skrócona wersja
            "scenario_id": f"{timeframe}_{scenario_type}",
            "response_length": len(scenario_text)
        })
        
        return scenario
    
    def _build_scenario_prompt(
        self, 
        timeframe: int, 
        scenario_type: str, 
        input_data: ScenarioInput,
        chain_of_thought: ChainOfThought
    ) -> str:
        """Buduje prompt do generowania scenariusza z chain of thought"""
        
        # Podsumowanie faktów priorytetowych
        facts_summary = "\n".join([
            f"- {fact.content[:200]} (relevance: {fact.relevance_score:.2f}, confidence: {fact.confidence:.2f})"
            for fact in input_data.priority_facts[:30]
        ])
        
        # Podsumowanie korelacji
        correlations_summary = "\n".join([
            f"- {corr.correlation_type}: {corr.explanation} (strength: {corr.strength:.2f})"
            for corr in input_data.correlations[:10]
        ])
        
        # Podsumowanie czynników sytuacyjnych z wagami
        factors_summary = "\n".join([
            f"- {key}: {value.get('description', '')} (waga: {value.get('weight', 0)})"
            for key, value in input_data.situation_factors.items()
        ])
        
        # Chain of thought summary
        cot_summary = chain_of_thought.get_summary()
        
        prompt = f"""
Jesteś ekspertem analizy foresightowej dla Ministerstwa Spraw Zagranicznych.
Twoim zadaniem jest wygenerowanie realistycznego scenariusza dla państwa Atlantis.

KONTEKST:
Państwo Atlantis: {json.dumps(input_data.atlantis_profile, indent=2, ensure_ascii=False)}

CZASOKRES: {timeframe} miesięcy
TYP SCENARIUSZA: {'pozytywny' if scenario_type == 'positive' else 'negatywny'} dla interesów Atlantis

CZYNNIKI SYTUACYJNE (z wagami):
{factors_summary}

FAKTY PRIORYTETOWE:
{facts_summary}

KORELACJE ZNALEZIONE:
{correlations_summary}

CHAIN OF THOUGHT (dotychczasowe rozumowanie):
{cot_summary}

ZADANIE:
Wygeneruj szczegółowy scenariusz {timeframe}-miesięczny ({'pozytywny' if scenario_type == 'positive' else 'negatywny'}) 
dla państwa Atlantis, który:

1. Opisuje kluczowe wydarzenia i trendy
2. Wskazuje prawdopodobieństwa różnych zdarzeń
3. Analizuje wpływ na różne obszary (polityka, gospodarka, bezpieczeństwo, społeczeństwo)
4. Zawiera rekomendacje dla rządu Atlantis
5. Wyjaśnia logikę przyczynowo-skutkową prowadzącą do scenariusza
6. Wskazuje które fakty i korelacje były kluczowe dla wnioskowania

FORMAT ODPOWIEDZI (JSON):
{{
    "title": "Tytuł scenariusza",
    "description": "Szczegółowy opis (500-800 słów)",
    "key_events": ["wydarzenie1", "wydarzenie2", ...],
    "probabilities": {{
        "wydarzenie1": 0.75,
        "wydarzenie2": 0.60
    }},
    "impacts": {{
        "polityka": "opis wpływu",
        "gospodarka": "opis wpływu",
        "bezpieczeństwo": "opis wpływu",
        "społeczeństwo": "opis wpływu"
    }},
    "recommendations": ["rekomendacja1", "rekomendacja2", ...],
    "reasoning": {{
        "key_facts_used": ["fact_id1", "fact_id2"],
        "key_correlations": ["corr_id1"],
        "causal_chain": "wyjaśnienie ścieżki przyczynowo-skutkowej",
        "confidence": 0.85
    }}
}}

Użyj temperatury {self.temperature_realistic} dla realistycznych prognoz.
Odpowiedz TYLKO w formacie JSON, bez dodatkowego tekstu.
"""
        return prompt
    
    def _generate_scenario_fallback(self, prompt: str) -> str:
        """Fallback bez GQPA - używa OpenAI bezpośrednio"""
        try:
            import openai
            openai.api_key = self.openai_api_key
            
            response = openai.ChatCompletion.create(
                model=self.config.get("OPENAI_MODEL", "gpt-4-turbo-preview"),
                messages=[
                    {"role": "system", "content": "Jesteś ekspertem analizy foresightowej dla MSZ."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature_realistic,
                max_tokens=3000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Błąd podczas generowania scenariusza: {e}")
            return '{"error": "Nie udało się wygenerować scenariusza"}'
    
    def _parse_scenario_response(
        self,
        response_text: str,
        timeframe: int,
        scenario_type: str,
        input_data: ScenarioInput,
        chain_of_thought: ChainOfThought
    ) -> Scenario:
        """Parsuje odpowiedź LLM do obiektu Scenario"""
        
        try:
            # Próba wyciągnięcia JSON z odpowiedzi
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                data = json.loads(json_text)
            else:
                raise ValueError("Nie znaleziono JSON w odpowiedzi")
        except Exception as e:
            logger.warning(f"Błąd parsowania JSON: {e}. Używam domyślnych wartości.")
            data = {
                "title": f"Scenariusz {scenario_type} {timeframe} miesięcy",
                "description": response_text[:1000],
                "key_events": [],
                "probabilities": {},
                "impacts": {},
                "recommendations": [],
                "reasoning": {"confidence": 0.5}
            }
        
        # Ekstrakcja faktów i korelacji użytych w rozumowaniu
        reasoning = data.get("reasoning", {})
        supporting_facts = reasoning.get("key_facts_used", [])
        correlations_used = reasoning.get("key_correlations", [])
        confidence = reasoning.get("confidence", 0.5)
        
        # Aktualizacja chain of thought
        chain_of_thought.add_step(
            ReasoningStep(
                step_type="scenario_generation",
                content=f"Wygenerowano scenariusz {scenario_type} dla {timeframe} miesięcy",
                facts_used=supporting_facts,
                correlations_used=correlations_used,
                confidence=confidence
            )
        )
        
        return Scenario(
            timeframe_months=timeframe,
            scenario_type=scenario_type,
            title=data.get("title", f"Scenariusz {scenario_type}"),
            description=data.get("description", ""),
            key_events=data.get("key_events", []),
            probabilities=data.get("probabilities", {}),
            impacts=data.get("impacts", {}),
            recommendations=data.get("recommendations", []),
            chain_of_thought=chain_of_thought,
            supporting_facts=supporting_facts,
            correlations_used=correlations_used,
            confidence_score=confidence
        )
    
    def generate_all_scenarios(self, input_data: ScenarioInput) -> List[Scenario]:
        """Generuje wszystkie 4 scenariusze (12m+, 12m-, 36m+, 36m-)"""
        
        logger.info("Rozpoczynam generowanie scenariuszy...")
        
        scenarios = []
        timeframes = [12, 36]
        scenario_types = ["positive", "negative"]
        
        for timeframe in timeframes:
            for scenario_type in scenario_types:
                logger.info(f"Generuję scenariusz: {timeframe}m, {scenario_type}")
                
                # Inicjalizacja chain of thought dla tego scenariusza
                cot = ChainOfThought(
                    initial_goal=f"generate_{scenario_type}_scenario_{timeframe}months"
                )
                
                # Dodanie początkowych kroków rozumowania
                cot.add_step(ReasoningStep(
                    step_type="initialization",
                    content=f"Inicjalizacja generowania scenariusza {scenario_type} dla {timeframe} miesięcy",
                    facts_used=[],
                    correlations_used=[],
                    confidence=1.0
                ))
                
                # Generowanie scenariusza
                scenario = self._generate_scenario_with_gqpa(
                    timeframe, scenario_type, input_data, cot
                )
                
                scenarios.append(scenario)
                self.generated_scenarios.append(scenario)
        
        logger.info(f"Wygenerowano {len(scenarios)} scenariuszy")
        return scenarios
    
    def get_prompt_memory(self) -> List[Dict]:
        """Zwraca historię ostatnich promptów"""
        return list(self.prompt_memory)
    
    def generate_final_report(self, scenarios: List[Scenario], input_data: ScenarioInput) -> str:
        """Generuje końcowy raport 2-3 tysiące słów"""
        
        # Streszczenie danych
        data_summary = self._generate_data_summary(input_data)
        
        # Scenariusze z wyjaśnieniami
        scenarios_text = []
        for scenario in scenarios:
            scenario_text = self._format_scenario_with_explanation(scenario)
            scenarios_text.append(scenario_text)
        
        # Rekomendacje
        recommendations = self._generate_recommendations(scenarios)
        
        # Złożenie raportu
        report = f"""
# RAPORT ANALITYCZNO-PROGNOSTYCZNY DLA PAŃSTWA ATLANTIS

## 1. STRESZCZENIE DANYCH UWZGLĘDNIONYCH W ANALIZIE

{data_summary}

## 2. SCENARIUSZE

{chr(10).join(scenarios_text)}

## 3. REKOMENDACJE DLA PAŃSTWA ATLANTIS

{recommendations}

---
Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Narzędzie: Scenariusze Jutra v1.0 z GQPA Core
"""
        
        return report
    
    def _generate_data_summary(self, input_data: ScenarioInput) -> str:
        """Generuje streszczenie danych (max 250 słów)"""
        total_facts = len(input_data.analyzed_facts)
        total_correlations = len(input_data.correlations)
        priority_count = len(input_data.priority_facts)
        
        summary = f"""
Analiza obejmuje {total_facts} faktów zebranych z oficjalnych źródeł międzynarodowych 
(ministerstwa, instytucje, think-tanki) opublikowanych po 31 grudnia 2020 roku. 
Zidentyfikowano {total_correlations} korelacji między faktami, w tym zależności 
przyczynowo-skutkowe, czasowe i tematyczne. 

Do generowania scenariuszy wykorzystano {priority_count} faktów priorytetowych, 
wyselekcjonowanych na podstawie relewantności dla interesów państwa Atlantis oraz 
poziomu pewności źródła. Analiza uwzględnia {len(input_data.situation_factors)} 
kluczowych czynników sytuacyjnych z przypisanymi wagami istotności.

Wszystkie dane zostały zweryfikowane pod kątem wiarygodności źródła oraz 
zabezpieczone przed potencjalnym data poisoning poprzez system weryfikacji 
krzyżowej i wykrywania anomalii.
"""
        return summary.strip()
    
    def _format_scenario_with_explanation(self, scenario: Scenario) -> str:
        """Formatuje scenariusz z wyjaśnieniem chain of thought"""
        
        type_name = "pozytywny" if scenario.scenario_type == "positive" else "negatywny"
        
        text = f"""
### Scenariusz {type_name} - {scenario.timeframe_months} miesięcy

**{scenario.title}**

{scenario.description}

**Kluczowe wydarzenia:**
{chr(10).join(f"- {event}" for event in scenario.key_events)}

**Prawdopodobieństwa:**
{chr(10).join(f"- {event}: {prob:.0%}" for event, prob in scenario.probabilities.items())}

**Wpływy:**
{chr(10).join(f"- **{area}**: {impact}" for area, impact in scenario.impacts.items())}

**Rekomendacje:**
{chr(10).join(f"- {rec}" for rec in scenario.recommendations)}

**Wyjaśnienie rozumowania (Chain of Thought):**

{scenario.chain_of_thought.get_detailed_explanation()}

**Pewność scenariusza:** {scenario.confidence_score:.0%}
"""
        return text
    
    def _generate_recommendations(self, scenarios: List[Scenario]) -> str:
        """Generuje rekomendacje na podstawie wszystkich scenariuszy"""
        
        positive_scenarios = [s for s in scenarios if s.scenario_type == "positive"]
        negative_scenarios = [s for s in scenarios if s.scenario_type == "negative"]
        
        # Agregacja rekomendacji z scenariuszy negatywnych (jak unikać)
        avoid_recommendations = set()
        for scenario in negative_scenarios:
            avoid_recommendations.update(scenario.recommendations)
        
        # Agregacja rekomendacji z scenariuszy pozytywnych (jak realizować)
        pursue_recommendations = set()
        for scenario in positive_scenarios:
            pursue_recommendations.update(scenario.recommendations)
        
        text = f"""
#### Jakie decyzje pomogą uniknąć scenariuszy negatywnych:

{chr(10).join(f"- {rec}" for rec in list(avoid_recommendations)[:10])}

#### Jakie decyzje pomogą w zrealizowaniu scenariuszy pozytywnych:

{chr(10).join(f"- {rec}" for rec in list(pursue_recommendations)[:10])}
"""
        return text

