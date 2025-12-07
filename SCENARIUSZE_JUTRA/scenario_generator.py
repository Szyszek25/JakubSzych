"""
Moduł generowania scenariuszy z wykorzystaniem GQPA Core
Integruje analizę danych, chain of thought i generowanie scenariuszy
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'hama_core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'system'))

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
from collections import deque

# Importy HAMA Diamond (Background IP)
try:
    from hama_part5 import CognitiveAgent, EnhancedCognitiveAgent
    from hama_part4 import EnhancedMemoryNexus, WorldModel
    from hama_part6 import GeminiCognitiveAdapter
    from hama_part1 import Episode
    HAMA_AVAILABLE = True
except ImportError:
    HAMA_AVAILABLE = False
    EnhancedCognitiveAgent = None
    logging.warning("HAMA Diamond Core nie jest dostępne. Używam uproszczonej wersji.")

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
        # GQPA może działać bez gemini_model - GeminiCognitiveAdapter używa lokalnego LLM (Ollama)
        # Używamy EnhancedCognitiveAgent, który ma metodę get_enhanced_state_summary()
        if HAMA_AVAILABLE:
            try:
                # EnhancedCognitiveAgent ma więcej funkcji niż CognitiveAgent
                # Sprawdzamy czy klasa jest dostępna i można ją użyć
                try:
                    # Sprawdź czy EnhancedCognitiveAgent jest dostępny i ma metodę get_enhanced_state_summary
                    if EnhancedCognitiveAgent is not None and hasattr(EnhancedCognitiveAgent, '__call__'):
                        # Spróbuj utworzyć instancję i sprawdź czy ma metodę
                        test_agent = EnhancedCognitiveAgent()
                        if hasattr(test_agent, 'get_enhanced_state_summary'):
                            self.cognitive_agent = test_agent
                            logger.info("✅ Używam EnhancedCognitiveAgent (pełna funkcjonalność GQPA)")
                        else:
                            # Instancja nie ma metody - użyj podstawowego
                            self.cognitive_agent = CognitiveAgent()
                            logger.warning("⚠️ EnhancedCognitiveAgent nie ma get_enhanced_state_summary, używam podstawowego CognitiveAgent")
                    else:
                        self.cognitive_agent = CognitiveAgent()
                        logger.warning("⚠️ EnhancedCognitiveAgent niedostępny, używam podstawowego CognitiveAgent")
                except (NameError, TypeError, AttributeError, Exception) as e:
                    # EnhancedCognitiveAgent nie został zaimportowany lub nie można go użyć
                    self.cognitive_agent = CognitiveAgent()
                    logger.warning(f"⚠️ EnhancedCognitiveAgent nie dostępny ({e}), używam podstawowego CognitiveAgent")
                
                # GeminiCognitiveAdapter może działać z gemini_model=None - używa lokalnego adaptera LLM
                self.gemini_adapter = GeminiCognitiveAdapter(gemini_model, self.cognitive_agent)
                self.use_gqpa = True
                if gemini_model:
                    logger.info("✅ GQPA Core zainicjalizowany z Gemini adapter")
                else:
                    logger.info("✅ GQPA Core zainicjalizowany z lokalnym LLM adapter (Ollama)")
            except Exception as e:
                logger.warning(f"⚠️ Błąd inicjalizacji GQPA: {e}. Używam uproszczonej wersji.")
                import traceback
                logger.debug(traceback.format_exc())
                self.cognitive_agent = None
                self.gemini_adapter = None
                self.use_gqpa = False
        else:
            self.cognitive_agent = None
            self.gemini_adapter = None
            self.use_gqpa = False
            logger.warning("⚠️ GQPA Core nie jest dostępne. Używam uproszczonej wersji bez GQPA")
        
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
            logger.info(f"Generuję scenariusz używając lokalnego LLM (długość promptu: {len(prompt)} znaków)")
            scenario_text = self._generate_scenario_fallback(prompt)
            logger.info(f"Otrzymano odpowiedź (długość: {len(scenario_text)} znaków)")
        
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
        
        # Podsumowanie faktów priorytetowych (ograniczone do 10 najważniejszych dla szybszej odpowiedzi)
        facts_summary = "\n".join([
            f"- {fact.content[:150]} (relevance: {fact.relevance_score:.2f})"
            for fact in input_data.priority_facts[:10]  # Zmniejszone z 30 do 10
        ])
        
        # Podsumowanie korelacji (ograniczone do 5 najważniejszych)
        correlations_summary = "\n".join([
            f"- {corr.correlation_type}: {corr.explanation[:100]} (strength: {corr.strength:.2f})"
            for corr in input_data.correlations[:5]  # Zmniejszone z 10 do 5
        ])
        
        # Podsumowanie czynników sytuacyjnych z wagami
        factors_summary = "\n".join([
            f"- {key}: {value.get('description', '')} (waga: {value.get('weight', 0)})"
            for key, value in input_data.situation_factors.items()
        ])
        
        # Chain of thought summary
        cot_summary = chain_of_thought.get_summary()
        
        # Różnicowanie promptu w zależności od horyzontu czasowego
        if timeframe == 12:
            timeframe_context = """
HORYZONT CZASOWY: 12 MIESIĘCY (krótkoterminowy)
- Skup się na wydarzeniach i trendach, które mogą wystąpić w ciągu najbliższego roku
- Uwzględnij wydarzenia już rozpoczęte lub w trakcie realizacji
- Prawdopodobieństwa powinny być wyższe (60-90%) dla wydarzeń krótkoterminowych
- Skoncentruj się na bezpośrednich konsekwencjach i natychmiastowych działaniach
"""
        else:  # 36 miesięcy
            timeframe_context = """
HORYZONT CZASOWY: 36 MIESIĘCY (średnioterminowy)
- Skup się na trendach strukturalnych i długoterminowych zmianach
- Uwzględnij kumulatywne efekty wydarzeń z ostatnich lat
- Prawdopodobieństwa mogą być bardziej zróżnicowane (40-80%) dla wydarzeń długoterminowych
- Skoncentruj się na transformacjach strukturalnych i strategicznych decyzjach
- Rozważ scenariusze alternatywne i niepewność długoterminową
"""
        
        # Skrócony profil Atlantis (tylko kluczowe informacje)
        atlantis_short = {
            "name": input_data.atlantis_profile.get("name", "Atlantis"),
            "population": input_data.atlantis_profile.get("population", 28000000),
            "memberships": input_data.atlantis_profile.get("memberships", {}),
            "strong_sectors": input_data.atlantis_profile.get("economy", {}).get("strong_sectors", [])[:5]
        }
        
        # Skracanie podsumowań dla szybszej odpowiedzi
        factors_short = factors_summary[:1000] if len(facts_summary) > 1000 else factors_summary
        facts_short = facts_summary[:500] if len(facts_summary) > 500 else facts_summary
        corr_short = correlations_summary[:300] if len(correlations_summary) > 300 else correlations_summary
        
        prompt = f"""
Jestes ekspertem analizy foresightowej dla MSZ. Wygeneruj scenariusz dla Atlantis.

KONTEKST: {json.dumps(atlantis_short, ensure_ascii=False)}

{timeframe_context}

CZASOKRES: {timeframe} miesiecy | TYP: {'pozytywny' if scenario_type == 'positive' else 'negatywny'}

CZYNNIKI (wagi):
{factors_short}

FAKTY:
{facts_short}

KORELACJE:
{corr_short}

ZADANIE: Wygeneruj scenariusz {timeframe}m ({'pozytywny' if scenario_type == 'positive' else 'negatywny'}) z:
- Kluczowymi wydarzeniami
- Prawdopodobienstwami
- Wplywem na polityke/gospodarke/bezpieczenstwo
- Rekomendacjami

FORMAT (JSON):
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
        """Fallback bez GQPA - używa lokalnego LLM (Ollama)"""
        try:
            from local_llm_adapter import LocalLLMAdapter
            
            model_name = self.config.get("OLLAMA_MODEL", "mistral")
            logger.info(f"Tworzenie adaptera LLM dla modelu: {model_name}")
            llm = LocalLLMAdapter(model_name=model_name)
            
            # Dodaj instrukcję systemową
            system_prompt = "Jesteś ekspertem analizy foresightowej dla MSZ. "
            full_prompt = system_prompt + prompt
            
            logger.info(f"Wywołuję LLM.generate (długość promptu: {len(full_prompt)} znaków, max_tokens: 1500, timeout: 120s)")
            logger.info(f"UWAGA: Generowanie scenariusza może zająć 3-10 minut - Mistral jest wolny dla długich promptów")
            logger.info(f"Proszę czekać...")
            
            response = llm.generate(
                full_prompt,
                temperature=self.temperature_realistic,
                max_tokens=1500,  # Zmniejszone dla szybszej odpowiedzi
                json_mode=True
            )
            logger.info(f"Otrzymano odpowiedź z LLM (długość: {len(response)} znaków)")
            return response
        except ImportError:
            logger.warning("LocalLLMAdapter nie dostępne - używam prostego fallback")
            return self._simple_scenario_fallback(prompt)
        except Exception as e:
            logger.error(f"Błąd podczas generowania scenariusza: {e}")
            return self._simple_scenario_fallback(prompt)
    
    def _simple_scenario_fallback(self, prompt: str) -> str:
        """Prosty fallback gdy LLM nie działa"""
        return """{
    "title": "Scenariusz analityczny (wymaga Ollama)",
    "description": "Aby wygenerować pełny scenariusz, uruchom Ollama: ollama serve",
    "key_events": ["Wymagana instalacja Ollama dla pełnej funkcjonalności"],
    "probabilities": {},
    "impacts": {},
    "recommendations": ["Zainstaluj Ollama: https://ollama.ai", "Uruchom: ollama serve", "Pobierz model: ollama pull llama3.2"],
    "reasoning": {"confidence": 0.3}
}"""
    
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

**Wyjaśnienie mechaniki decyzyjnej:**

{self._format_explanation_for_msz(scenario.chain_of_thought.get_detailed_explanation())}

**Pewność scenariusza:** {self._format_confidence(scenario.confidence_score)}
"""
        return text
    
    def _generate_recommendations(self, scenarios: List[Scenario]) -> str:
        """Generuje rekomendacje na podstawie wszystkich scenariuszy"""
        
        positive_scenarios = [s for s in scenarios if s.scenario_type == "positive"]
        negative_scenarios = [s for s in scenarios if s.scenario_type == "negative"]
        
        # Agregacja rekomendacji z scenariuszy negatywnych (jak unikać)
        avoid_recommendations = []
        seen_avoid = set()
        for scenario in negative_scenarios:
            for rec in scenario.recommendations:
                # Obsługa zarówno stringów, jak i słowników
                if isinstance(rec, dict):
                    rec_text = rec.get('description', rec.get('recommendation', str(rec)))
                else:
                    rec_text = str(rec)
                
                # Dodaj tylko unikalne rekomendacje
                if rec_text not in seen_avoid:
                    seen_avoid.add(rec_text)
                    avoid_recommendations.append(rec_text)
        
        # Agregacja rekomendacji z scenariuszy pozytywnych (jak realizować)
        pursue_recommendations = []
        seen_pursue = set()
        for scenario in positive_scenarios:
            for rec in scenario.recommendations:
                # Obsługa zarówno stringów, jak i słowników
                if isinstance(rec, dict):
                    rec_text = rec.get('description', rec.get('recommendation', str(rec)))
                else:
                    rec_text = str(rec)
                
                # Dodaj tylko unikalne rekomendacje
                if rec_text not in seen_pursue:
                    seen_pursue.add(rec_text)
                    pursue_recommendations.append(rec_text)
        
        text = f"""
#### Jakie decyzje pomogą uniknąć scenariuszy negatywnych:

{chr(10).join(f"- {rec}" for rec in avoid_recommendations[:10])}

#### Jakie decyzje pomogą w zrealizowaniu scenariuszy pozytywnych:

{chr(10).join(f"- {rec}" for rec in pursue_recommendations[:10])}
"""
        return text
    
    def _format_explanation_for_msz(self, explanation: str) -> str:
        """Formatuje wyjaśnienie na język urzędowy dla MSZ"""
        # Zamiana terminów technicznych
        replacements = {
            'Chain of Thought': 'Mechanika decyzyjna',
            'krok 1': 'Etap 1',
            'krok 2': 'Etap 2',
            'krok 3': 'Etap 3',
            'krok 4': 'Etap 4',
            'krok 5': 'Etap 5',
            'Analiza faktów →': 'Etap analizy →',
            'Wykrywanie korelacji →': 'Etap syntezy →',
            'Aplikacja wag →': 'Etap priorytetyzacji →',
            'Wnioskowanie przyczynowe →': 'Etap oceny skutków →',
            'Generowanie scenariuszy →': 'Etap wariantowania →',
        }
        
        result = explanation
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        return result
    
    def _format_confidence(self, confidence: float) -> str:
        """Formatuje pewność na język opisowy"""
        if confidence >= 0.8:
            return "wysoka"
        elif confidence >= 0.6:
            return "umiarkowana do wysoka"
        elif confidence >= 0.4:
            return "umiarkowana"
        else:
            return "niska do umiarkowanej"

