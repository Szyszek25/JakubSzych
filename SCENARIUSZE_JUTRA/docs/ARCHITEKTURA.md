# 🏗️ Architektura Scenariusze Jutra

## Przegląd Systemu

System **Scenariusze Jutra** to zaawansowany system analizy foresightowej dla MSZ, wykorzystujący architekturę GQPA (General Quantum Process Architecture) do generowania scenariuszy rozwojowych w perspektywie 12 i 36 miesięcy.

## Główne Komponenty

System składa się z **6 głównych modułów**:

1. **API Scenarios** - FastAPI endpointy dla interfejsu
2. **Scenario Generator** - Generator scenariuszy (GQPA Diamond)
3. **Local LLM Adapter** - Adapter dla lokalnych modeli LLM (Ollama)
4. **Scenario Analyzer** - Analiza i ocena scenariuszy
5. **Visualizer** - Wizualizacje GQPA Diamond
6. **Main Orchestrator** - Orkiestracja całego procesu

---

## Diagram Architektury

```
┌─────────────────────────────────────────────────────────┐
│              API SCENARIOS (FastAPI)                    │
│              Port: 8002                                 │
│              - /api/scenarios                           │
│              - /api/scenarios/{id}/accept                │
│              - /api/dashboard/stats                      │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Main         │ │          │ │             │
│ Orchestrator │ │ Scenario │ │ Local LLM   │
│              │ │ Generator│ │ Adapter      │
│ - Knowledge  │ │          │ │             │
│   Extraction │ │ - GQPA   │ │ - Ollama    │
│ - Reasoning  │ │   Diamond│ │ - OpenAI    │
│ - Analysis   │ │          │ │ - Gemini    │
└──────┬───────┘ └───┬───────┘ └───┬─────────┘
       │             │              │
       └─────────────┴──────────────┘
                     │
              ┌──────▼──────┐
              │  Analyzer   │
              │             │
              │ - Statistics│
              │ - Rankings  │
              └──────┬───────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Visualizer   │ │ Report    │ │ CSV Export  │
│              │ │ Generator │ │             │
│ - Radar      │ │           │ │ - CSV       │
│ - Heatmap    │ │ - MD      │ │ - JSON     │
│ - 3D Charts  │ │ - TXT     │ │             │
└──────────────┘ └───────────┘ └─────────────┘
```

---

## Szczegółowy Opis Modułów

### 1. API Scenarios (`api_scenarios.py`)

**FastAPI** endpointy dla interfejsu użytkownika:

- `GET /api/scenarios` - Pobierz wszystkie scenariusze
- `POST /api/scenarios/{id}/accept` - Zaakceptuj scenariusz
- `POST /api/scenarios/{id}/reject` - Odrzuć scenariusz
- `GET /api/dashboard/stats` - Statystyki dashboardu
- `POST /api/analyze` - Uruchom analizę z wagami

**Funkcje:**
- Cache wyników analizy
- Thread-safe analiza
- CORS dla frontendu
- Streaming responses

---

### 2. Main Orchestrator (`main_orchestrator.py`)

**Orkiestracja** całego procesu analizy:

**Komponenty:**
- **Knowledge Extractor** - Ekstrakcja wiedzy z danych
- **Data Analyzer** - Analiza danych geopolitycznych
- **Reasoning Engine** - Silnik wnioskowania GQPA
- **Recommendation Engine** - Generator rekomendacji

**Proces:**
1. Pobierz dane z zewnętrznych źródeł
2. Wyekstrahuj kluczowe fakty
3. Przeanalizuj dane używając GQPA
4. Wygeneruj scenariusze (12M, 36M)
5. Wygeneruj rekomendacje

---

### 3. Scenario Generator (`scenario_generator.py`)

**Generator scenariuszy** wykorzystujący GQPA Diamond:

**Funkcje:**
- Generowanie scenariuszy 12-miesięcznych
- Generowanie scenariuszy 36-miesięcznych
- Analiza prawdopodobieństw
- Identyfikacja kluczowych wydarzeń
- Ocena wpływu na państwo docelowe

**Metodologia:**
- Weighted factors analysis
- Causal chain reasoning
- Probability estimation
- Impact assessment

---

### 4. Local LLM Adapter (`local_llm_adapter.py`)

**Adapter** dla różnych modeli LLM:

**Obsługiwane modele:**
- **Ollama** (lokalne modele)
- **OpenAI** (GPT-4, GPT-3.5)
- **Google Gemini** (Gemini Pro)

**Funkcje:**
- Unified interface
- Fallback mechanisms
- Error handling
- Token management

---

### 5. Scenario Analyzer (`analyze_scenarios.py`)

**Analiza** wygenerowanych scenariuszy:

**Funkcje:**
- Statystyki scenariuszy
- Analiza prawdopodobieństw
- Ranking scenariuszy
- Eksport do CSV
- Generowanie raportów

**Metryki:**
- GQPA Diamond Index
- Prawdopodobieństwo
- Wpływ (pozytywny/negatywny)
- Ryzyko/Szansa

---

### 6. Visualizer (`visualizer_hama.py`)

**Wizualizacje** GQPA Diamond:

**Typy wykresów:**
- **GQPA Diamond Radar** - Profil scenariuszy
- **Heatmap Prawdopodobieństw** - Mapa prawdopodobieństw
- **Mapa Ryzyka/Szans** - Wizualizacja ryzyka
- **Porównanie Horyzontów** - 12M vs 36M
- **Wykres 3D Timeline** - Wymiar czasowy

**Technologie:**
- Plotly (interaktywne wykresy)
- HTML export
- Responsive design

---

## Przepływ Danych

```
Użytkownik (Frontend)
    ↓
API Scenarios (FastAPI)
    ↓
Main Orchestrator
    ↓
┌─────────────────────────┐
│ Knowledge Extractor     │ → Dane zewnętrzne
│ Data Analyzer           │ → Analiza danych
│ Reasoning Engine        │ → Wnioskowanie GQPA
│ Recommendation Engine   │ → Rekomendacje
└─────────────────────────┘
    ↓
Scenario Generator
    ↓
Scenario Analyzer
    ↓
Visualizer
    ↓
Outputs (CSV, MD, HTML)
```

---

## Integracja z GQPA Diamond

System wykorzystuje **GQPA Diamond** jako silnik kognitywny:

1. **Knowledge Extraction** - Ekstrakcja wiedzy z danych
2. **Causal Reasoning** - Wnioskowanie przyczynowo-skutkowe
3. **Multi-factor Analysis** - Analiza wielowymiarowa
4. **Probability Estimation** - Estymacja prawdopodobieństw
5. **Impact Assessment** - Ocena wpływu

---

## Bezpieczeństwo i Weryfikacja

**Anti-Poisoning Config:**
- Minimum 3 źródła danych
- Weryfikacja źródeł
- Cross-reference sources
- Anomaly detection
- Reputation check

---

## Skalowalność

- **Thread-safe** analiza
- **Cache** wyników
- **Async** API endpoints
- **Modular** architecture
- **Extensible** design

---

## Technologie

- **Backend**: Python 3.9+, FastAPI, GQPA Diamond
- **LLM**: Ollama, OpenAI, Google Gemini
- **Visualization**: Plotly
- **Frontend**: React, TypeScript, Vite
- **Data**: JSON, CSV, Markdown

---

## Porty i Endpointy

- **Backend API**: `http://localhost:8002`
- **API Docs**: `http://localhost:8002/docs`
- **Frontend**: `http://localhost:5173`

---

## Struktura Folderów

```
SCENARIUSZE_JUTRA/
├── api_scenarios.py          # FastAPI endpoints
├── main_orchestrator.py      # Main orchestrator
├── scenario_generator.py     # Scenario generator
├── local_llm_adapter.py      # LLM adapter
├── analyze_scenarios.py      # Scenario analyzer
├── visualizer_hama.py        # Visualizations
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── docs/                     # Documentation
│   ├── ARCHITEKTURA.md       # This file
│   ├── METODOLOGIA.md        # Methodology
│   └── ZRODLA_DANYCH.md      # Data sources
├── prezentacja/              # Presentations
│   ├── prezentacja.md        # Main presentation
│   └── scenariusz_filmu.md   # Demo scenario
└── outputs/                  # Generated outputs
    ├── analiza_scenariuszy.csv
    ├── raport_analiza_scenariuszy.md
    └── wykresy/              # Charts
```

---

## Wnioski

System **Scenariusze Jutra** to kompleksowe rozwiązanie do analizy foresightowej, wykorzystujące zaawansowane technologie AI i architekturę GQPA do generowania wiarygodnych scenariuszy rozwojowych dla MSZ.

