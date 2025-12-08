# 📁 Struktura Projektu HAMA-ZANT

## Przegląd

Struktura projektu ZANT jest wzorowana na projekcie INDEKS_BRANZ i zawiera wszystkie niezbędne foldery i pliki.

## Struktura Folderów

```
ZANT/
├── backend/                 # Backend FastAPI
│   ├── api/                # Endpointy API
│   │   ├── __init__.py
│   │   └── main.py         # Główne endpointy
│   ├── models/             # Modele danych
│   │   ├── __init__.py
│   │   └── accident.py     # Modele wypadków
│   ├── services/           # Logika biznesowa
│   │   ├── __init__.py
│   │   ├── accident_assistant.py    # HAMA-based asystent
│   │   ├── decision_engine.py      # HAMA reasoning engine
│   │   └── pdf_extractor.py        # Ekstrakcja PDF
│   ├── __init__.py
│   └── config.py           # Konfiguracja (Gemini 3 Pro)
│
├── docs/                    # Dokumentacja techniczna
│   ├── ARCHITEKTURA.md     # Architektura systemu
│   ├── METODOLOGIA.md      # Metodologia HAMA
│   └── ZRODLA_DANYCH.md    # Źródła danych
│
├── outputs/                 # Wyniki działania systemu
│   ├── raporty/            # Raporty analiz zgłoszeń
│   ├── karty_wypadkow/     # Wygenerowane karty wypadków
│   ├── wykresy/            # Wizualizacje (opcjonalnie)
│   └── README.md           # Opis outputs
│
├── prezentacja/            # Materiały prezentacyjne
│   ├── prezentacja.md     # Slajdy prezentacji
│   └── scenariusz_demo.md  # Scenariusz demo
│
├── frontend/               # Interfejs użytkownika
│   └── index.html         # Główny interfejs
│
├── data/                   # Dane testowe (opcjonalnie)
│   ├── raw/               # Surowe dane
│   └── processed/         # Przetworzone dane
│
├── README.md               # Główna dokumentacja
├── ARCHITEKTURA.md         # Architektura (stary, przeniesiony do docs/)
├── INSTALACJA.md           # Instrukcje instalacji
├── QUICK_START.md          # Szybki start
├── GEMINI_SETUP.md         # Konfiguracja Gemini
├── PLAN_24H.md             # Plan pracy na hackathon
├── PRESENTACJA.md          # Prezentacja (stary, przeniesiony do prezentacja/)
├── PRZYKLAD_UZYCIA.md      # Przykłady użycia API
├── TESTY_DLA_JURY.md       # Przewodnik testowy
├── PODSUMOWANIE.md         # Podsumowanie projektu
├── STRUKTURA_PROJEKTU.md   # Ten plik
├── requirements.txt        # Zależności Python
├── URUCHOM.bat             # Skrypt uruchomienia (Windows)
└── .gitignore             # Ignorowane pliki
```

## Kluczowe Pliki

### Backend

- **`backend/config.py`** - Konfiguracja systemu
  - Model: `models/gemini-3-pro-preview`
  - Wzorce ZUS
  - Reguły decyzyjne

- **`backend/api/main.py`** - FastAPI endpoints
  - `/api/report/analyze` - analiza zgłoszenia
  - `/api/decision/analyze` - analiza dokumentacji

- **`backend/services/accident_assistant.py`** - HAMA-based asystent
  - Wykrywanie braków
  - Generowanie sugestii
  - Walidacja

- **`backend/services/decision_engine.py`** - HAMA reasoning engine
  - Analiza warunków
  - Rekomendacja decyzji
  - Generowanie uzasadnień

### Dokumentacja

- **`docs/ARCHITEKTURA.md`** - Szczegółowa architektura
- **`docs/METODOLOGIA.md`** - Metodologia HAMA
- **`docs/ZRODLA_DANYCH.md`** - Źródła danych

### Prezentacja

- **`prezentacja/prezentacja.md`** - Slajdy prezentacji
- **`prezentacja/scenariusz_demo.md`** - Scenariusz demo

### Outputs

- **`outputs/raporty/`** - Raporty analiz
- **`outputs/karty_wypadkow/`** - Karty wypadków
- **`outputs/wykresy/`** - Wizualizacje

## Model LLM

**Wszędzie używany model:** `models/gemini-3-pro-preview`

**Konfiguracja:**
- `backend/config.py`: `GEMINI_MODEL_NAME = "models/gemini-3-pro-preview"`
- Używany w: `accident_assistant.py`, `decision_engine.py`

## Framework

**Wszędzie używany framework:** **HAMA Diamond**

- Nie GQPA
- Nie Ollama
- Tylko HAMA Diamond + Gemini 3 Pro

## Porównanie z INDEKS_BRANZ

### Podobne:
- ✅ Struktura `docs/`, `outputs/`, `prezentacja/`
- ✅ Dokumentacja techniczna
- ✅ Materiały prezentacyjne

### Różnice:
- ZANT: Backend FastAPI (INDEKS_BRANZ: CLI)
- ZANT: Frontend HTML (INDEKS_BRANZ: Wykresy HTML)
- ZANT: HAMA Diamond (INDEKS_BRANZ: HAMA Scoring)

## Następne Kroki

1. ✅ Struktura folderów - gotowa
2. ✅ Dokumentacja - kompletna
3. ✅ Model Gemini 3 Pro - wszędzie ustawiony
4. ✅ HAMA Diamond - wszędzie używany
5. ⏳ Testy z prawdziwymi danymi
6. ⏳ Prezentacja

---

**Struktura gotowa do hackathonu! 🚀**


