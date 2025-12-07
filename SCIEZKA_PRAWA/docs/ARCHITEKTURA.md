# 🏗️ Architektura Ścieżka Prawa

## Przegląd Systemu

System **Ścieżka Prawa (GQPA Legislative Navigator)** to kompleksowe rozwiązanie do monitorowania, analizy i prognozowania procesów legislacyjnych.

## Główne Komponenty

1. **Legislative Tracker** - Śledzenie zmian prawnych
2. **Plain Language Engine** - Upraszczanie języka urzędowego
3. **Impact Simulator** - Analiza skutków regulacji
4. **Democratic Interface** - Interfejs dla obywateli
5. **Transparency Hub** - Centrum transparentności
6. **Main Orchestrator** - Orkiestracja modułów

---

## Diagram Architektury

```
┌─────────────────────────────────────────────────────────┐
│         API (FastAPI) - Port: 8003                     │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Legislative  │ │ Plain    │ │ Impact      │
│ Tracker      │ │ Language │ │ Simulator   │
│              │ │ Engine   │ │             │
│ - Track      │ │ - Simplify│ │ - Analyze  │
│ - Status     │ │ - Translate│ │ - Forecast │
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
└──────────────┘ └────────────┘ └────────────┘
```

---

## Szczegółowy Opis Modułów

### 1. Legislative Tracker

Śledzenie dokumentów legislacyjnych przez wszystkie etapy:
- Prekonsultacje → Konsultacje → Projekt → Sejm → Senat → Podpis → Publikacja → Wejście w życie

### 2. Plain Language Engine

Upraszczanie języka urzędowego:
- Skracanie zdań
- Usuwanie żargonu
- Aktywna forma
- Uproszczenie liczb

### 3. Impact Simulator

Analiza skutków regulacji:
- Finansowe
- Społeczne
- Technologiczne
- Operacyjne
- Prawne
- Ekonomiczne

### 4. Democratic Interface

Interfejs dla obywateli:
- Śledzenie konsultacji
- Składanie uwag
- Feedback
- Profil obywatela

### 5. Transparency Hub

Centrum transparentności:
- Raporty zgodności
- Relacje między dokumentami
- Metadane
- Compliance checking

---

## Technologie

- Python 3.9+, FastAPI
- GQPA Core
- LLM (Ollama/OpenAI/Gemini)
- React (frontend)

---

## Porty

- Backend API: `http://localhost:8003`
- API Docs: `http://localhost:8003/docs`

