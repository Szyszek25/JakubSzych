"""
🌍 HAMA DIAMOND MODULE: GEOPOLITICAL FORECASTER (MSZ CHALLENGE)

Rozszerzenie dla zadania "Scenariusze Jutra"

Gotowe do wklejenia w Google Colab po uruchomieniu części 1-7

UWAGA: Ten moduł wymaga wcześniejszego uruchomienia części 1-7,
które definiują klasy: ComplexDynamicEnvironment, SensoryData, 
ModalityType, EnhancedCognitiveAgent, GeminiCognitiveAdapter, Concept
"""

import networkx as nx
import json
import time
from typing import List, Dict, Any
from tqdm.notebook import tqdm

# Type hints dla klas zdefiniowanych w poprzednich częściach
# (będą dostępne w runtime po uruchomieniu części 1-7)
try:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        # Te importy są tylko dla type checker, nie są wykonywane w runtime
        pass
except ImportError:
    pass

# ============================================================================
# 1. ŚRODOWISKO GEOPOLITYCZNE (Zastępuje ComplexDynamicEnvironment)
# ============================================================================

class GeopoliticalEnvironment(ComplexDynamicEnvironment):  # type: ignore[name-defined]
    def __init__(self):
        super().__init__()
        # Symulowany strumień danych (w produkcji podpinamy tu API newsowe/RSS)
        self.news_feed = [
            {"type": "conflict", "region": "Eastern Europe", "intensity": 0.8, "actors": ["Country_A", "Country_B"]},
            {"type": "economic", "region": "Asia", "trend": "growth_slowdown", "impact": 0.6},
            {"type": "cyber", "region": "Global", "target": "infrastructure", "severity": 0.9},
            {"type": "climate", "region": "South America", "event": "drought", "impact": 0.7},
            {"type": "diplomacy", "region": "Middle East", "event": "treaty_signed", "impact": 0.5}
        ]
        self.current_index = 0

    def generate_sensory_data(self) -> List[Any]:  # type: ignore[valid-type]
        """Konwertuje newsy na dane sensoryczne agenta"""
        data = []
       
        # Pobierz newsa
        if self.current_index < len(self.news_feed):
            news = self.news_feed[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.news_feed)
           
            # Traktujemy newsy jako modalność JĘZYKOWĄ i WIZJĘ (metaforycznie)
            # SensoryData i ModalityType są zdefiniowane w hama_part1.py
            data.append(SensoryData(  # type: ignore[name-defined]
                modality=ModalityType.LANGUAGE,  # type: ignore[name-defined]
                data=news,
                timestamp=time.time(),
                intensity=news.get('intensity', news.get('impact', 0.5)),
                source="intelligence_feed"
            ))
           
        return data

# ============================================================================
# 2. SYMULATOR SCENARIUSZY (Rozszerzenie WorldModel)
# ============================================================================

class ScenarioSimulator:
    def __init__(self, agent):
        self.agent = agent
        self.knowledge_graph = nx.DiGraph()
       
    def build_graph_from_memory(self):
        """Buduje graf relacji z pamięci semantycznej i modelu świata"""
        self.knowledge_graph.clear()
       
        # Dodaj obiekty (kraje, aktorzy)
        for name, concept in self.agent.world_model.objects.items():
            self.knowledge_graph.add_node(name, type="actor", activation=concept.activation)
           
            # Dodaj relacje
            for rel_type, targets in concept.relations.items():
                for target in targets:
                    self.knowledge_graph.add_edge(name, target, relation=rel_type)
                   
    def simulate_timeline(self, horizon_months=6) -> str:
        """
        Symuluje przyszłość używając Gemini jako silnika wnioskowania,
        ale uziemionego w stanie wewnętrznym agenta (HAMA2)
        """
        print(f"\n🔮 Symulacja horyzontu czasowego: {horizon_months} miesięcy...")
       
        # Pobierz stan chaosu - jeśli wysoki, przewiduj bardziej radykalne scenariusze
        chaos = self.agent.emergent_integrator.get_integration_status()['emergent_metrics']['chaos_level']
       
        # Pobierz ostatnie elementy z pamięci roboczej
        recent_memory = [item.content for item in self.agent.workspace.working_memory[:5]]
       
        prompt = f"""
        Jesteś zaawansowanym systemem analitycznym MSZ.

        STAN WEWNĘTRZNY SYSTEMU:

        - Poziom niepewności (Chaos): {chaos:.2f} (0.0 = stabilnie, 1.0 = kryzys totalny)
        - Znane podmioty i relacje: {list(self.agent.world_model.objects.keys())}
        - Ostatnie wydarzenia w pamięci roboczej: {recent_memory}

        ZADANIE:

        Wygeneruj 3 scenariusze na najbliższe {horizon_months} miesięcy.

        1. Scenariusz Bazowy (Najbardziej prawdopodobny)
        2. Scenariusz Optymistyczny (Deeskalacja)
        3. Scenariusz "Czarny Łabędź" (Mało prawdopodobny, ale krytyczny - bazuj na poziomie chaosu)

        Format JSON (zwróć TYLKO JSON, bez dodatkowego tekstu):

        [
            {{"name": "Scenariusz Bazowy", "probability": 0.0-1.0, "description": "...", "key_indicators": ["..."]}},
            {{"name": "Scenariusz Optymistyczny", "probability": 0.0-1.0, "description": "...", "key_indicators": ["..."]}},
            {{"name": "Czarny Łabędź", "probability": 0.0-1.0, "description": "...", "key_indicators": ["..."]}}
        ]

        Jeśli poziom chaosu jest wysoki ({chaos:.2f}), scenariusz "Czarny Łabędź" powinien być bardziej radykalny i niebezpieczny.
        """

        # Używamy adaptera Gemini z HAMA Diamond
        response = self.agent.adapter.cognitive_query(prompt)
        
        # Wyciągnij JSON z odpowiedzi (może zawierać markdown)
        response_text = response.get('response', '')
        
        # Spróbuj wyciągnąć JSON z odpowiedzi
        try:
            # Usuń markdown code blocks jeśli są
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            # Parsuj JSON
            scenarios = json.loads(response_text)
            return json.dumps(scenarios, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            # Jeśli nie udało się sparsować, zwróć surową odpowiedź
            return response_text

# ============================================================================
# 3. AGENT MSZ (Konfiguracja)
# ============================================================================

def setup_msz_agent():
    print("\n🕵️ INICJALIZACJA AGENTA MSZ 'FUTURE-SIGHT'...")
   
    # 1. Podmiana środowiska
    # EnhancedCognitiveAgent jest zdefiniowany w hama_part5.py
    agent = EnhancedCognitiveAgent()  # type: ignore[name-defined]
    agent.environment = GeopoliticalEnvironment()
   
    # 2. Podpięcie adaptera
    # GeminiCognitiveAdapter i gemini_model są zdefiniowane w hama_part6.py i hama_part1.py
    adapter = GeminiCognitiveAdapter(gemini_model, agent)  # type: ignore[name-defined]
    agent.adapter = adapter  # Hack: przypisujemy adapter do agenta dla łatwego dostępu
   
    # 3. Dodanie symulatora
    agent.scenario_simulator = ScenarioSimulator(agent)
   
    # 4. Ustawienie celu
    agent.set_goal("analyze global stability trends and predict threats")
   
    return agent

# ============================================================================
# 4. URUCHOMIENIE DEMO
# ============================================================================

def run_msz_demo():
    # Setup
    msz_agent = setup_msz_agent()
   
    print("\n📥 Pobieranie danych wywiadowczych (Cykle kognitywne)...")
   
    # Wykonaj cykle, aby "przeczytać" newsy i zbudować model świata
    for _ in tqdm(range(6), desc="Analiza raportów"):
        msz_agent.cognitive_cycle()
       
        # Wymuś konceptualizację newsów (uproszczone mapowanie)
        # W prawdziwym rozwiązaniu tu byłby parser NLP wyciągający encje
        last_memory = msz_agent.workspace.working_memory[0] if msz_agent.workspace.working_memory else None
        if last_memory and isinstance(last_memory.content, dict):
            data = last_memory.content.get('data', {})
            if isinstance(data, dict) and 'region' in data:
                # Tworzymy koncept w modelu świata
                # Concept jest zdefiniowany w hama_part1.py
                concept = Concept(  # type: ignore[name-defined]
                    name=f"{data['region']}_{data.get('type', 'event')}",
                    properties=data,
                    relations={"involved": data.get('actors', [])},
                    activation=0.9
                )
                msz_agent.world_model.update_from_perception([concept])

    # Budowa grafu wiedzy
    msz_agent.scenario_simulator.build_graph_from_memory()
    print(f"✅ Zbudowano graf wiedzy: {len(msz_agent.world_model.objects)} węzłów")
   
    # Generowanie raportu
    print("\n📊 GENEROWANIE RAPORTU 'SCENARIUSZE JUTRA'...")
    scenarios_json = msz_agent.scenario_simulator.simulate_timeline(horizon_months=12)
   
    print("\n" + "="*70)
    print("RAPORT DLA MINISTERSTWA SPRAW ZAGRANICZNYCH")
    print("="*70)
    print(scenarios_json)
   
    # Analiza metryk chaosu
    metrics = msz_agent.emergent_integrator.get_integration_status()['emergent_metrics']
    print(f"\n⚠️ Wskaźnik niestabilności globalnej (System Chaos): {metrics['chaos_level']:.4f}")
    if metrics['chaos_level'] > 0.3:
        print("   ALARM: Wykryto wysoką dynamikę zmian - zalecana zwiększona czujność.")
    else:
        print("   STATUS: Sytuacja stabilna.")
    
    return msz_agent, scenarios_json

print("✅ Moduł Geopolityczny HAMA Diamond zdefiniowany")
print("\n" + "="*70)
print("CZĘŚĆ 8 ZAKOŃCZONA - Moduł Geopolityczny gotowy")
print("="*70)
print("\n💡 Aby uruchomić demo, wykonaj w następnej komórce:")
print("   run_msz_demo()")
print("\n📝 UWAGA: Upewnij się, że uruchomiłeś wszystkie części 1-7 przed tym modułem!")

# ============================================================================
# URUCHOMIENIE DEMO (odkomentuj poniższą linię, aby uruchomić)
# ============================================================================

# run_msz_demo()

