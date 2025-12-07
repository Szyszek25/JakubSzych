# 🏗️ Architektura Ścieżka Prawa (GQPA Legislative Navigator)

## Przegląd Systemu

System **Ścieżka Prawa (GQPA Legislative Navigator)** to kompleksowe rozwiązanie wykorzystujące architekturę GQPA (General Quantum Process Architecture) do monitorowania, analizy i prognozowania procesów legislacyjnych w administracji publicznej.

## Główne Komponenty

System składa się z **6 głównych modułów**:

1. **Legislative Tracker** - Śledzenie zmian prawnych od prekonsultacji do wejścia w życie
2. **Plain Language Engine** - Automatyczne upraszczanie języka urzędowego
3. **Impact Simulator** - Analiza skutków regulacji (finansowe, społeczne, operacyjne)
4. **Democratic Interface** - Interfejs dla obywateli do śledzenia konsultacji społecznych
5. **Transparency Hub** - Centrum transparentności dla administracji
6. **Main Orchestrator** - Orkiestracja wszystkich modułów

---

## Diagram Architektury

```
┌─────────────────────────────────────────────────────────┐
│         API (FastAPI) - Port: 8003                     │
│         - /api/documents                                │
│         - /api/analyze                                   │
│         - /api/consultations                            │
│         - /api/compliance                               │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Legislative  │ │ Plain    │ │ Impact      │
│ Tracker      │ │ Language │ │ Simulator   │
│              │ │ Engine   │ │             │
│ - Register   │ │ - Simplify│ │ - Analyze  │
│ - Track      │ │ - Translate│ │ - Forecast │
│ - Status     │ │ - Improve │ │ - Scenarios│
│ - Events     │ │   Readability│ │ - Impact  │
└──────┬───────┘ └───┬───────┘ └───┬─────────┘
       │             │              │
       └─────────────┴──────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Democratic   │ │ Transparency│ │ Main      │
│ Interface    │ │ Hub         │ │ Orchestrator│
│              │ │             │ │            │
│ - Consult    │ │ - Compliance│ │ - Coordinate│
│ - Feedback   │ │ - Reports  │ │ - Process │
│ - Profile    │ │ - Relations│ │ - Integrate│
└──────────────┘ └────────────┘ └────────────┘
```

---

## Szczegółowy Opis Modułów

### 1. Legislative Tracker (`legislative_tracker.py`)

**Śledzenie dokumentów legislacyjnych** przez wszystkie etapy procesu legislacyjnego.

**Statusy legislacyjne:**
1. `prekonsultacje` - Faza przedkonsultacyjna
2. `konsultacje_spoleczne` - Konsultacje społeczne
3. `projekt_rzadowy` - Projekt rządowy
4. `rada_ministrow` - Rada Ministrów
5. `sejm_pierwsze_czytanie` - Sejm - pierwsze czytanie
6. `sejm_drugie_czytanie` - Sejm - drugie czytanie
7. `sejm_trzecie_czytanie` - Sejm - trzecie czytanie
8. `senat` - Senat
9. `podpis_prezydenta` - Podpis Prezydenta
10. `opublikowanie` - Opublikowanie w Dzienniku Ustaw
11. `wejscie_w_zycie` - Wejście w życie

**Klasy:**
- `LegislativeDocument` - Reprezentacja dokumentu
- `LegislativeEvent` - Wydarzenie w procesie legislacyjnym
- `LegislativeTracker` - Główna klasa tracker'a

**Funkcje:**
- Rejestracja nowych dokumentów
- Aktualizacja statusu
- Śledzenie wydarzeń
- Historia zmian
- Zależności między dokumentami

---

### 2. Plain Language Engine (`plain_language_engine.py`)

**Automatyczne upraszczanie języka urzędowego** do języka zrozumiałego dla obywateli.

**Funkcje:**
- **Skracanie zdań** - Maksymalna długość: 20 słów
- **Usuwanie żargonu** - Zastępowanie terminów technicznych
- **Aktywna forma** - Zamiast strony biernej
- **Uproszczenie liczb** - Czytelne formatowanie
- **Strukturyzacja** - Podział na sekcje i akapity

**Klasy:**
- `SimplifiedText` - Uproszczony tekst z metadanymi
- `PlainLanguageEngine` - Główna klasa silnika

**Metryki:**
- **Readability Score** - Wskaźnik czytelności (0-100)
- **Sentence Length** - Średnia długość zdań
- **Word Complexity** - Złożoność słów

**Konfiguracja:**
- `max_sentence_length`: 20 słów
- `max_word_length`: 12 znaków
- `avoid_jargon`: True
- `use_active_voice`: True
- `simplify_numbers`: True

---

### 3. Impact Simulator (`impact_simulator.py`)

**Analiza skutków regulacji** w różnych wymiarach.

**Typy analizy wpływu:**
1. **Finansowy** - Koszty i przychody
2. **Społeczny** - Wpływ na społeczeństwo
3. **Technologiczny** - Wymagania techniczne
4. **Operacyjny** - Wpływ na procesy
5. **Prawny** - Zgodność z prawem
6. **Ekonomiczny** - Wpływ na gospodarkę

**Klasy:**
- `ImpactType` - Enum typów wpływu
- `ImpactAnalysis` - Analiza wpływu
- `ImpactSimulator` - Główna klasa symulatora

**Funkcje:**
- Analiza wpływu dla każdego typu
- Generowanie scenariuszy
- Prognozowanie skutków
- Ocena ryzyka
- Rekomendacje

**Metodologia:**
- Analiza tekstu dokumentu
- Identyfikacja kluczowych obszarów
- Estymacja wpływu (niski/średni/wysoki)
- Generowanie scenariuszy (optymistyczny/realistyczny/pesymistyczny)

---

### 4. Democratic Interface (`democratic_interface.py`)

**Interfejs dla obywateli** do śledzenia i uczestnictwa w konsultacjach społecznych.

**Funkcje:**
- **Śledzenie konsultacji** - Lista aktywnych konsultacji
- **Składanie uwag** - Formularz uwag
- **Feedback** - Opinie i komentarze
- **Profil obywatela** - Personalizacja

**Klasy:**
- `Consultation` - Konsultacja społeczna
- `CitizenProfile` - Profil obywatela
- `DemocraticInterface` - Główna klasa interfejsu

**Funkcjonalności:**
- Rejestracja w konsultacjach
- Przeglądanie dokumentów
- Składanie uwag online
- Śledzenie statusu uwag
- Powiadomienia o zmianach

---

### 5. Transparency Hub (`transparency_hub.py`)

**Centrum transparentności** dla administracji.

**Funkcje:**
- **Compliance Checking** - Sprawdzanie zgodności z politykami
- **Relacje między dokumentami** - Mapowanie zależności
- **Raporty** - Generowanie raportów zgodności
- **Metadane** - Zarządzanie metadanymi

**Klasy:**
- `ComplianceStatus` - Status zgodności
- `ComplianceReport` - Raport zgodności
- `DocumentRelationship` - Relacja między dokumentami
- `TransparencyHub` - Główna klasa hub'a

**Polityki zgodności:**
- **RODO** - Ochrona danych osobowych
- **DSA** - Digital Services Act
- **WCAG** - Web Content Accessibility Guidelines
- **Custom policies** - Własne polityki

**Funkcjonalności:**
- Automatyczne sprawdzanie zgodności
- Generowanie raportów
- Mapowanie relacji
- Tracking zmian

---

### 6. Main Orchestrator (`main_orchestrator.py`)

**Orkiestracja wszystkich modułów** systemu.

**Klasa:**
- `GQPALegislativeOrchestrator` - Główny orchestrator

**Proces przetwarzania dokumentu:**

1. **Rejestracja** - Dokument rejestrowany w Legislative Tracker
2. **Uproszczenie** - Plain Language Engine upraszcza tekst
3. **Analiza wpływu** - Impact Simulator analizuje skutki
4. **Compliance** - Transparency Hub sprawdza zgodność
5. **Konsultacje** - Democratic Interface tworzy konsultacje (jeśli wymagane)

**Funkcje:**
- `process_new_document()` - Przetwarzanie nowego dokumentu
- Koordynacja między modułami
- Zarządzanie przepływem danych
- Obsługa błędów

---

## Przepływ Danych

```
Nowy Dokument
    ↓
Main Orchestrator
    ↓
┌─────────────────────────┐
│ Legislative Tracker     │ → Rejestracja
│ Plain Language Engine   │ → Uproszczenie
│ Impact Simulator        │ → Analiza wpływu
│ Transparency Hub        │ → Compliance
│ Democratic Interface    │ → Konsultacje
└─────────────────────────┘
    ↓
Raporty i Dokumentacja
    ↓
API Response (JSON)
```

---

## Integracja z GQPA

System wykorzystuje **GQPA Core** jako silnik analityczny:

1. **Cognitive Processing** - Przetwarzanie kognitywne
2. **Reasoning** - Wnioskowanie
3. **Memory Management** - Zarządzanie pamięcią
4. **Decision Making** - Podejmowanie decyzji

**Konfiguracja GQPA:**
- `cognitive_cycles`: 10
- `memory_size`: 1000
- `impact_analysis_depth`: 5
- `scenario_horizon_months`: 12

---

## Bezpieczeństwo

**Security Config:**
- `rodo_compliant`: True
- `data_encryption`: True
- `access_logging`: True
- `rate_limiting`: True

**Compliance:**
- RODO - Ochrona danych osobowych
- DSA - Digital Services Act
- WCAG - Accessibility

---

## Technologie

- **Backend**: Python 3.9+, FastAPI, GQPA Core
- **LLM**: Ollama, OpenAI, Google Gemini (dla Plain Language)
- **Frontend**: React, TypeScript (opcjonalnie)
- **Data**: JSON, HTML, PDF, DOCX

---

## Porty i Endpointy

- **Backend API**: `http://localhost:8003`
- **API Docs**: `http://localhost:8003/docs`

**Główne endpointy:**
- `GET /api/documents` - Lista dokumentów
- `POST /api/documents` - Utwórz dokument
- `GET /api/documents/{id}` - Szczegóły dokumentu
- `POST /api/documents/{id}/status` - Aktualizuj status
- `POST /api/documents/{id}/simplify` - Uprość język
- `POST /api/documents/{id}/analyze` - Analiza wpływu
- `GET /api/consultations` - Lista konsultacji
- `POST /api/consultations/{id}/feedback` - Składanie uwag
- `GET /api/compliance/{id}` - Raport zgodności

---

## Struktura Folderów

```
SCIEZKA_PRAWA/
├── api.py                        # FastAPI endpoints
├── main_orchestrator.py          # Main orchestrator
├── legislative_tracker.py         # Legislative tracker
├── plain_language_engine.py     # Plain language engine
├── impact_simulator.py           # Impact simulator
├── democratic_interface.py       # Democratic interface
├── transparency_hub.py           # Transparency hub
├── config.py                     # Configuration
├── requirements.txt              # Dependencies
├── docs/                        # Documentation
│   ├── ARCHITEKTURA.md          # This file
│   ├── METODOLOGIA.md           # Methodology
│   └── ZRODLA_DANYCH.md         # Data sources
├── prezentacja/                 # Presentations
│   ├── prezentacja.md           # Main presentation
│   └── scenariusz_filmu.md      # Demo scenario
└── outputs/                    # Generated outputs
```

---

## Wnioski

System **Ścieżka Prawa (GQPA Legislative Navigator)** to kompleksowe rozwiązanie wykorzystujące zaawansowane technologie AI i architekturę GQPA do monitorowania, analizy i prognozowania procesów legislacyjnych, zwiększając transparentność i partycypację obywatelską.

