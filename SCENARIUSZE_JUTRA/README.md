# 🌍 Scenariusze Jutra - System Analizy Foresightowej dla MSZ

## Opis

System analizy foresightowej dla Ministerstwa Spraw Zagranicznych RP, który wykorzystuje zaawansowane technologie NLP, analizy danych oraz modelowania scenariuszy do typowania prawdopodobnych wydarzeń i trendów w polityce międzynarodowej.

## Architektura Systemu

System składa się z następujących warstw:

### 1. Data Ingestion Layer
- **Moduł**: `data_collector.py`
- **Funkcja**: Zbieranie danych z oficjalnych źródeł (ministerstwa, instytucje międzynarodowe, think-tanki)
- **Funkcje**:
  - Tagging źródeł
  - Metadane czasu, kraju, tematu
  - Filtrowanie po dacie (po 31.12.2020)

### 2. Knowledge Representation Layer
- **Moduł**: `knowledge_representation.py`
- **Funkcja**: Przekształcanie faktów w koncepty i relacje
- **Funkcje**:
  - Fakty → Koncepty → Relacje
  - Graf przyczynowo-skutkowy (NetworkX)
  - Wykrywanie konfliktów informacyjnych

### 3. Reasoning Engine
- **Moduł**: `reasoning_engine.py`
- **Funkcja**: Silnik wnioskowania z priorytetyzacją wag
- **Funkcje**:
  - Priorytetyzacja faktów wg wag czynników
  - Wielowariantowe wnioskowanie
  - Symulacja przyszłych ścieżek
  - Budowa łańcuchów przyczynowo-skutkowych

### 4. Scenario Generator
- **Moduł**: `scenario_generator.py`
- **Funkcja**: Generowanie 4 scenariuszy (12m+/-, 36m+/-)
- **Funkcje**:
  - Integracja z GQPA Core (Background IP)
  - Generowanie scenariuszy z chain of thought
  - Poziom probabilizmu
  - Wyraźne różnice między wariantami

### 5. Explainability Layer
- **Moduł**: `explainability_layer.py`
- **Funkcja**: Wyjaśnianie mechaniki systemu użytkownikowi
- **Funkcje**:
  - Lista kluczowych czynników
  - Relacje przyczynowe
  - Wpływ wag na wynik
  - Przejście: dane → wniosek → rekomendacja
  - **NIE ujawnia surowego CoT**, ale przejrzyste wyjaśnienia

### 6. Recommendation Engine
- **Moduł**: `recommendation_engine.py`
- **Funkcja**: Generowanie rekomendacji strategicznych
- **Funkcje**:
  - Decyzje minimalizujące ryzyka (scenariusze negatywne)
  - Decyzje wzmacniające scenariusze pozytywne
  - Kategoryzacja (polityczne, ekonomiczne, bezpieczeństwo, dyplomatyczne, technologiczne)
  - Priorytetyzacja i kroki implementacji

### 7. Anti-Poisoning System
- **Moduł**: `anti_poisoning.py`
- **Funkcja**: Ochrona przed data poisoning
- **Funkcje**:
  - Weryfikacja źródeł
  - Wykrywanie anomalii
  - Weryfikacja krzyżowa (minimum 3 źródła)
  - Filtrowanie zanieczyszczonych danych

### 8. Chain of Thought
- **Moduł**: `chain_of_thought.py`
- **Funkcja**: Śledzenie ścieżki rozumowania
- **Funkcje**:
  - Rejestracja kroków analizy
  - Relacje przyczynowo-skutkowe
  - Rozwiązane konflikty
  - Wyjaśnialność (bez surowego CoT)

## Instalacja

```bash
# Zainstaluj zależności
pip install -r requirements.txt

# Skonfiguruj zmienne środowiskowe
# Utwórz plik .env z:
OPENAI_API_KEY=your_key_here
```

## Użycie

### Demo Flow

```bash
python run_demo.py
```

### Programowe użycie

```python
from main_orchestrator import ScenarioOrchestrator, create_situation_factors_from_weights
from config import OPENAI_API_KEY, OPENAI_MODEL

# Konfiguracja
config = {
    "OPENAI_MODEL": OPENAI_MODEL,
    "TEMPERATURE_REALISTIC": 0.3,
    "ANALYSIS_CONFIG": {...}
}

# Inicjalizacja
orchestrator = ScenarioOrchestrator(config, OPENAI_API_KEY)

# Przygotowanie czynników
situation_factors = create_situation_factors_from_weights()

# Uruchomienie analizy
results = orchestrator.run_full_analysis(situation_factors, collect_data=True)

# Wyniki
scenarios = results["scenarios"]
recommendations = results["recommendations"]
report = results["report"]
```

## Czynniki Sytuacyjne (z wagami)

System analizuje 6 kluczowych czynników:

- **a)** Kryzys globalnej produkcji GPU (waga: 30)
- **b)** Załamanie rentowności europejskiej motoryzacji (waga: 15)
- **c)** Spadek PKB strefy euro (waga: 15)
- **d)** Sytuacja na Ukrainie (waga: 10)
- **e)** Inwestycje USA/UE w Ukrainie (waga: 5)
- **f)** Szok energetyczny: OZE + nadpodaż ropy (waga: 25)

**Użytkownik może ręcznie zmienić wagi**, co automatycznie przeliczy scenariusze.

## Format Wyjścia

System generuje raport tekstowy (2000-3000 słów) zawierający:

1. **Streszczenie danych** (≤250 słów)
2. **4 scenariusze**:
   - 12 miesięcy (pozytywny)
   - 12 miesięcy (negatywny)
   - 36 miesięcy (pozytywny)
   - 36 miesięcy (negatywny)
   
   Każdy scenariusz zawiera:
   - Opis
   - Kluczowe wydarzenia
   - Prawdopodobieństwa
   - Wpływy na różne obszary
   - Wyjaśnienie rozumowania (Chain of Thought)
   
3. **Rekomendacje**:
   - Unikanie scenariuszy negatywnych
   - Realizacja scenariuszy pozytywnych

## Bezpieczeństwo

- Brak ujawniania promptów (pamięć promptów tylko dla użytkownika MSZ)
- Możliwość pracy offline (kontenery)
- Odporność na data poisoning
- Licencje wyłącznie darmowe
- Python jako główny język

## Integracja z GQPA Core

System wykorzystuje **GQPA Core (Background IP)** jako bibliotekę zewnętrzną:
- Cognitive Agent dla kognitywnej analizy
- Enhanced Memory Nexus dla pamięci epizodycznej
- World Model dla symulacji przyszłości
- Gemini Cognitive Adapter dla interakcji z LLM

**Uwaga**: GQPA Core jest Background IP i nie podlega przeniesieniu praw.

## Skalowalność

System zaprojektowany z myślą o skalowaniu ×100:
- Wersja podstawowa: 50 mln słów
- Wersja rozszerzona: 5 mld słów (×100)
- Rozszerzenie parametrów geograficznych: do 50 krajów / 30 języków (×30)
- Rozszerzenie formatów: tekst → grafika, audio, wideo

## Struktura Plików

```
SCENARIUSZE_JUTRA/
├── config.py                    # Konfiguracja systemu
├── data_collector.py            # Zbieranie danych
├── data_analyzer.py              # Analiza danych NLP
├── knowledge_representation.py  # Graf wiedzy
├── reasoning_engine.py          # Silnik wnioskowania
├── scenario_generator.py         # Generator scenariuszy
├── recommendation_engine.py     # Generator rekomendacji
├── explainability_layer.py      # Warstwa wyjaśnialności
├── chain_of_thought.py          # Chain of Thought
├── anti_poisoning.py            # Ochrona przed data poisoning
├── main_orchestrator.py         # Główny orchestrator
├── run_demo.py                  # Demo flow
└── requirements.txt             # Zależności
```

## Licencja

System wykorzystuje wyłącznie licencje bezpłatne (Python, biblioteki open-source).

## Autorzy

System stworzony dla HackNation 2025 - wyzwanie "Scenariusze jutra" (MSZ).

