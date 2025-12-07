# 🏗️ Architektura Systemu "Scenariusze Jutra"

## Przegląd Architektury

System został zaprojektowany jako **silnik analityczno-decyzyjny**, a nie chatbot czy generator tekstu. Jego celem jest modelowanie mechaniki prowadzącej do przyszłości, a nie przewidywanie przyszłości.

## Warstwy Systemu

### 1. Data Ingestion Layer (`data_collector.py`)

**Odpowiedzialność**: Zbieranie i wstępne przetwarzanie danych

- Zbieranie danych z oficjalnych źródeł (ministerstwa, instytucje, think-tanki)
- Tagging źródeł (kraj, typ, język)
- Filtrowanie po dacie (po 31.12.2020)
- Ekstrakcja treści z RSS feeds i stron HTML
- Rate limiting i obsługa błędów

**Kluczowe klasy**:
- `DataCollector`: Główna klasa zbierająca dane
- `DataSource`: Reprezentacja pojedynczego źródła

### 2. Anti-Poisoning System (`anti_poisoning.py`)

**Odpowiedzialność**: Ochrona przed celowym zanieczyszczaniem danych

- Weryfikacja reputacji źródeł
- Wykrywanie anomalii w treści
- Weryfikacja krzyżowa (minimum 3 źródła potwierdzające fakt)
- Filtrowanie zanieczyszczonych danych
- Rejestr zaufanych domen

**Kluczowe klasy**:
- `AntiPoisoningSystem`: Główny system ochrony
- `SourceReputation`: Reputacja źródła
- `AnomalyDetection`: Wykryta anomalia

### 3. Knowledge Representation Layer (`knowledge_representation.py`)

**Odpowiedzialność**: Przekształcanie faktów w strukturę wiedzy

- Ekstrakcja konceptów z faktów (kraje, organizacje, wydarzenia, trendy)
- Budowa grafu wiedzy (NetworkX)
- Identyfikacja relacji między konceptami
- Wykrywanie konfliktów informacyjnych
- Obliczanie centralności konceptów

**Kluczowe klasy**:
- `KnowledgeGraph`: Graf wiedzy
- `KnowledgeExtractor`: Ekstraktor konceptów i relacji
- `Concept`: Reprezentacja konceptu
- `Relation`: Relacja między konceptami

### 4. Reasoning Engine (`reasoning_engine.py`)

**Odpowiedzialność**: Silnik wnioskowania z priorytetyzacją wag

- Rejestracja czynników sytuacyjnych z wagami
- Priorytetyzacja faktów na podstawie wag
- Budowa łańcuchów przyczynowo-skutkowych
- Symulacja przyszłych ścieżek rozwoju
- Wielowariantowe wnioskowanie
- Aktualizacja wag (ręczna korekta przez użytkownika)

**Kluczowe klasy**:
- `ReasoningEngine`: Główny silnik wnioskowania
- `WeightedFactor`: Czynnik z wagą
- `ReasoningPath`: Ścieżka rozumowania

### 5. Chain of Thought (`chain_of_thought.py`)

**Odpowiedzialność**: Śledzenie ścieżki rozumowania

- Rejestracja kroków analizy
- Budowa relacji przyczynowo-skutkowych
- Wykrywanie i rozwiązywanie konfliktów
- Wyjaśnialność (NIE surowy CoT, ale przejrzyste wyjaśnienia)
- Analiza wpływu czynników

**Kluczowe klasy**:
- `ChainOfThought`: Główna klasa zarządzająca CoT
- `ReasoningStep`: Pojedynczy krok rozumowania
- `CausalRelation`: Relacja przyczynowo-skutkowa

### 6. Scenario Generator (`scenario_generator.py`)

**Odpowiedzialność**: Generowanie scenariuszy

- Integracja z GQPA Core (Background IP)
- Generowanie 4 scenariuszy (12m+/-, 36m+/-)
- Chain of thought dla każdego scenariusza
- Poziom probabilizmu
- Pamięć 10 ostatnich promptów
- Generowanie raportu końcowego

**Kluczowe klasy**:
- `ScenarioGenerator`: Generator scenariuszy
- `Scenario`: Reprezentacja scenariusza
- `ScenarioInput`: Dane wejściowe do generowania

### 7. Explainability Layer (`explainability_layer.py`)

**Odpowiedzialność**: Wyjaśnianie mechaniki systemu użytkownikowi

- Wyjaśnienie kluczowych czynników i wag
- Wyjaśnienie relacji przyczynowo-skutkowych
- Ścieżka: dane → wniosek → rekomendacja
- Wpływ zmian wag na wyniki
- **NIE ujawnia surowego CoT**, ale przejrzyste wyjaśnienia

**Kluczowe klasy**:
- `ExplainabilityLayer`: Warstwa wyjaśnialności
- `Explanation`: Pojedyncze wyjaśnienie

### 8. Recommendation Engine (`recommendation_engine.py`)

**Odpowiedzialność**: Generowanie rekomendacji strategicznych

- Rekomendacje unikające scenariuszy negatywnych
- Rekomendacje realizujące scenariusze pozytywne
- Kategoryzacja (polityczne, ekonomiczne, bezpieczeństwo, dyplomatyczne, technologiczne)
- Priorytetyzacja (high, medium, low)
- Kroki implementacji
- Analiza ryzyk

**Kluczowe klasy**:
- `RecommendationEngine`: Generator rekomendacji
- `Recommendation`: Pojedyncza rekomendacja

### 9. Main Orchestrator (`main_orchestrator.py`)

**Odpowiedzialność**: Koordynacja wszystkich modułów

- Inicjalizacja wszystkich komponentów
- Koordynacja przepływu danych między modułami
- Uruchomienie pełnej analizy
- Zarządzanie pamięcią promptów
- Aktualizacja wag i przeliczanie scenariuszy

**Kluczowe klasy**:
- `ScenarioOrchestrator`: Główny orchestrator

## Przepływ Danych

```
1. Data Collection
   ↓
2. Anti-Poisoning Filtering
   ↓
3. Data Analysis (NLP)
   ↓
4. Knowledge Graph Construction
   ↓
5. Factor Registration (with weights)
   ↓
6. Fact Prioritization
   ↓
7. Causal Chain Building
   ↓
8. Scenario Generation (4 scenarios)
   ↓
9. Recommendation Generation
   ↓
10. Report Generation
```

## Integracja z GQPA Core

System wykorzystuje **GQPA Core (Background IP)** jako bibliotekę zewnętrzną:

- `CognitiveAgent`: Kognitywna analiza
- `EnhancedMemoryNexus`: Pamięć epizodyczna
- `WorldModel`: Model świata i symulacja
- `GeminiCognitiveAdapter`: Interakcja z LLM

**Uwaga**: GQPA Core jest Background IP i nie podlega przeniesieniu praw w ramach hackathonu.

## Bezpieczeństwo

- **Brak ujawniania promptów**: Pamięć promptów dostępna tylko dla użytkownika MSZ
- **Ochrona przed data poisoning**: Weryfikacja źródeł, wykrywanie anomalii
- **Możliwość pracy offline**: Kontenery z danymi
- **Licencje bezpłatne**: Wszystkie biblioteki open-source

## Skalowalność

System zaprojektowany z myślą o skalowaniu ×100:

- **Wersja podstawowa**: 50 mln słów
- **Wersja rozszerzona**: 5 mld słów (×100)
- **Parametry geograficzne**: do 50 krajów / 30 języków (×30)
- **Formaty danych**: tekst → grafika, audio, wideo

## Wyjaśnialność

System **NIE ujawnia surowego Chain of Thought**, ale dostarcza:

1. **Lista kluczowych czynników** z wagami
2. **Relacje przyczynowo-skutkowe** z wyjaśnieniami
3. **Mechanika priorytetyzacji** faktów
4. **Ścieżka rozumowania**: dane → wniosek → rekomendacja
5. **Wpływ wag** na finalne scenariusze

## Testowanie

```bash
# Demo flow
python run_demo.py

# Programowe użycie
python -c "from main_orchestrator import *; ..."
```

## Rozszerzenia (Przyszłość)

- Backcasting (prognozowanie wsteczne)
- Analiza danych graficznych, audio, wideo
- Rozszerzenie do 50 krajów / 30 języków
- Analiza do 5 mld słów
- Praca na danych zamkniętych (kontenery)

