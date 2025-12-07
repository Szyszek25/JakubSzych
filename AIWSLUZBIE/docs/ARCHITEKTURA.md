# 🏗️ Architektura Asystent AI dla Administracji

## Przegląd Systemu

System **Asystent AI dla Administracji** to zaawansowane rozwiązanie wspierające orzeczników w Departamencie Turystyki MSiT, wykorzystujące architekturę GQPA (General Quantum Process Architecture) do inteligentnej analizy spraw administracyjnych.

## Główne Komponenty

System składa się z **7 głównych modułów**:

1. **API Dashboard** - FastAPI endpointy dla dashboardu React
2. **Administrative Assistant** - Główny asystent AI (GQPA)
3. **Document Analyzer** - Analiza dokumentów
4. **Security Guardrails** - Zabezpieczenia i walidacja
5. **Cognitive Agent** - Agent kognitywny (Truth Guardian)
6. **LLM Adapter** - Adapter dla modeli LLM (Gemini/Ollama/OpenAI)
7. **Vector DB** - Baza danych wektorowych dla dokumentów

---

## Diagram Architektury

```
┌─────────────────────────────────────────────────────────┐
│         FRONTEND (React Dashboard)                       │
│         Port: 3000                                       │
│         - Lista spraw                                    │
│         - Statystyki                                     │
│         - Analiza spraw                                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│         API DASHBOARD (FastAPI)                         │
│         Port: 8000                                      │
│         - /api/cases                                    │
│         - /api/analyze                                  │
│         - /api/stats                                    │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Administrative│ │          │ │             │
│ Assistant      │ │ Document │ │ Security    │
│ (GQPA)        │ │ Analyzer │ │ Guardrails  │
│               │ │           │ │             │
│ - Cases       │ │ - Extract │ │ - Validate │
│ - Analysis    │ │ - Parse   │ │ - Sanitize │
│ - Decisions   │ │ - Analyze │ │ - Check    │
└──────┬────────┘ └───┬───────┘ └───┬─────────┘
       │               │              │
       └───────────────┴──────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Cognitive    │ │ LLM      │ │ Vector DB   │
│ Agent        │ │ Adapter  │ │             │
│              │ │          │ │             │
│ - Truth      │ │ - Gemini │ │ - Embeddings│
│   Guardian   │ │ - Ollama │ │ - Search    │
│ - Reasoning  │ │ - OpenAI │ │ - Similarity│
└──────────────┘ └──────────┘ └─────────────┘
```

---

## Szczegółowy Opis Modułów

### 1. API Dashboard (`api_dashboard.py`)

**FastAPI** endpointy dla dashboardu React:

- `GET /api/cases` - Pobierz wszystkie sprawy
- `POST /api/cases` - Utwórz nową sprawę
- `GET /api/cases/{id}` - Pobierz szczegóły sprawy
- `POST /api/analyze` - Przeanalizuj sprawę
- `GET /api/stats` - Statystyki dashboardu
- `POST /api/demo/init` - Inicjalizacja danych demo

**Funkcje:**
- CORS dla frontendu
- Background tasks
- Error handling
- JSON responses

---

### 2. Administrative Assistant (`asystent_ai_gqpa_integrated.py`)

**Główny moduł asystenta** wykorzystujący GQPA:

**Komponenty:**
- **Document Analyzer** - Analiza dokumentów
- **External Systems Integration** - Integracja z systemami zewnętrznymi
- **Security Guardrails** - Zabezpieczenia
- **Cognitive Agent** - Agent kognitywny (Truth Guardian)

**Funkcje:**
- Analiza spraw administracyjnych
- Generowanie rekomendacji
- Weryfikacja zgodności
- Zarządzanie terminami

---

### 3. Document Analyzer

**Analiza dokumentów** używając LLM:

**Funkcje:**
- Ekstrakcja informacji z dokumentów
- Parsowanie tekstu
- Identyfikacja kluczowych elementów
- Klasyfikacja dokumentów

**Obsługiwane formaty:**
- PDF
- DOCX
- TXT
- HTML

---

### 4. Security Guardrails (`guardrails_detailed.py`)

**Zabezpieczenia** i walidacja:

**Funkcje:**
- Walidacja danych wejściowych
- Sanityzacja tekstu
- Wykrywanie niebezpiecznych wzorców
- Ochrona przed prompt injection
- Rate limiting

---

### 5. Cognitive Agent (Truth Guardian)

**Agent kognitywny** do weryfikacji informacji:

**Komponenty:**
- **Information Environment** - Środowisko informacyjne
- **Global Workspace** - Globalna przestrzeń robocza
- **Emotion Value Module** - Moduł wartości emocjonalnych
- **World Model** - Model świata
- **Memory Nexus** - Pamięć

**Funkcje:**
- Weryfikacja prawdziwości informacji
- Wykrywanie dezinformacji
- Analiza wiarygodności
- Cognitive immune system

---

### 6. LLM Adapter

**Adapter** dla różnych modeli LLM:

**Obsługiwane modele:**
- **Google Gemini** (Gemini Pro)
- **Ollama** (llama3.2, mistral)
- **OpenAI** (GPT-4, GPT-3.5)

**Funkcje:**
- Unified interface
- Fallback mechanisms
- Error handling
- Token management

---

### 7. Vector DB (`vector_db.py`)

**Baza danych wektorowych** dla dokumentów:

**Funkcje:**
- Embeddings dokumentów
- Semantic search
- Similarity matching
- Knowledge base

**Technologie:**
- ChromaDB / FAISS
- Sentence transformers
- Embeddings models

---

## Przepływ Danych

```
Użytkownik (Frontend)
    ↓
API Dashboard (FastAPI)
    ↓
Administrative Assistant
    ↓
┌─────────────────────────┐
│ Document Analyzer      │ → Analiza dokumentów
│ Security Guardrails    │ → Walidacja
│ Cognitive Agent        │ → Weryfikacja
│ LLM Adapter            │ → LLM processing
└─────────────────────────┘
    ↓
Vector DB (Knowledge Base)
    ↓
Rekomendacje i Decyzje
    ↓
Response (JSON)
```

---

## Integracja z GQPA

System wykorzystuje **GQPA Core** jako Background IP:

1. **Cognitive Processing** - Przetwarzanie kognitywne
2. **Reasoning** - Wnioskowanie
3. **Memory Management** - Zarządzanie pamięcią
4. **Decision Making** - Podejmowanie decyzji

---

## Bezpieczeństwo

**Security Guardrails:**
- Input validation
- Output sanitization
- Prompt injection protection
- Rate limiting
- Access control

**RODO Compliance:**
- Anonimizacja danych
- Szyfrowanie
- Logowanie dostępu
- Audit trail

---

## Technologie

- **Backend**: Python 3.9+, FastAPI, GQPA Core
- **LLM**: Google Gemini, Ollama, OpenAI
- **Vector DB**: ChromaDB / FAISS
- **Frontend**: React, TypeScript
- **Data**: JSON, PDF, DOCX

---

## Porty i Endpointy

- **Backend API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Frontend**: `http://localhost:3000`

---

## Struktura Folderów

```
AIWSLUZBIE/
├── api_dashboard.py              # FastAPI endpoints
├── asystent_ai_gqpa_integrated.py # Main assistant
├── document_chunker.py            # Document processing
├── guardrails_detailed.py         # Security
├── local_model_adapter.py         # LLM adapter
├── vector_db.py                   # Vector database
├── requirements.txt               # Dependencies
├── docs/                         # Documentation
│   ├── ARCHITEKTURA.md           # This file
│   ├── METODOLOGIA.md            # Methodology
│   └── ZRODLA_DANYCH.md          # Data sources
├── prezentacja/                  # Presentations
│   ├── prezentacja.md            # Main presentation
│   └── scenariusz_filmu.md       # Demo scenario
└── outputs/                     # Generated outputs
```

---

## Wnioski

System **Asystent AI dla Administracji** to kompleksowe rozwiązanie wykorzystujące zaawansowane technologie AI i architekturę GQPA do wspierania orzeczników w analizie spraw administracyjnych.

