# 🏗️ Architektura ZANT

## Przegląd Systemu

ZANT (ZUS Accident Notification Tool) to system wykorzystujący **HAMA Diamond (Hybrid Adaptive Multi-Agent)** do wspierania procesu zgłaszania i analizy wypadków przy pracy.

## Komponenty

### 1. Backend (FastAPI)

```
backend/
├── api/
│   └── main.py              # FastAPI endpoints
├── models/
│   └── accident.py          # Modele danych
├── services/
│   ├── accident_assistant.py    # HAMA-based asystent zgłoszenia
│   ├── decision_engine.py       # Silnik decyzyjny
│   └── pdf_extractor.py         # Ekstrakcja z PDF
└── config.py                # Konfiguracja
```

### 2. Frontend (HTML/JS)

- Prosty interfejs webowy
- Dwa tryby: Asystent Zgłoszenia / Wsparcie Decyzji
- Komunikacja z backendem przez REST API

### 3. HAMA Integration

System wykorzystuje moduły HAMA z `../AIWSLUZBIE`:
- `LocalModelAdapter` - adapter dla Google Gemini
- Reasoning engine - analiza logiczna
- Cognitive analysis - analiza kognitywna

## Przepływ Danych

### Asystent Zgłoszenia

```
Użytkownik → Formularz → AccidentAssistant → HAMA/Gemini → Analiza → Sugestie
```

1. Użytkownik wypełnia formularz
2. `AccidentAssistant` analizuje zgłoszenie
3. HAMA wykrywa brakujące pola
4. LLM generuje sugestie
5. Wynik zwracany do użytkownika

### Wsparcie Decyzji

```
PDF → PDFExtractor → OCR/Text → DecisionEngine → HAMA/Gemini → Rekomendacja → Karta Wypadku
```

1. Upload dokumentacji PDF
2. `PDFExtractor` ekstrahuje tekst (OCR jeśli potrzeba)
3. `DecisionEngine` analizuje używając HAMA Diamond
4. Weryfikacja warunków definicji wypadku
5. Zastosowanie reguł decyzyjnych
6. Generowanie rekomendacji i karty wypadku

## Reguły Decyzyjne

### Definicja Wypadku

Wypadek przy pracy = **nagłe zdarzenie** + **przyczyna zewnętrzna** + **uraz/śmierć** + **związek z pracą**

### Warunki Uznania

- ✅ Wszystkie 4 warunki spełnione + confidence ≥ 0.7 → **UZNAĆ**
- ⚠️ Warunki spełnione + confidence < 0.7 → **WERYFIKACJA**
- ❌ Czynniki wykluczające → **NIE UZNAWAĆ**

## Bezpieczeństwo

- **RODO**: Dane przechowywane lokalnie (w produkcji: szyfrowanie)
- **Walidacja**: Wszystkie dane wejściowe walidowane
- **CORS**: Konfigurowalne źródła (w produkcji: konkretne domeny)

## Skalowanie

- **Backend**: FastAPI (async) - gotowe do skalowania
- **LLM**: Google Gemini 3 Pro API - skalowalne przez Google
- **Storage**: Obecnie w pamięci (w produkcji: PostgreSQL/MongoDB)

## Plan Wdrożenia

### Faza 1: MVP (Hackathon)
- ✅ Podstawowy asystent zgłoszenia
- ✅ Analiza PDF
- ✅ Rekomendacja decyzji
- ✅ Prosty frontend

### Faza 2: Produkcja
- Baza danych
- Autentykacja użytkowników
- Integracja z systemami ZUS
- Zaawansowane OCR
- Logowanie i audyt

### Faza 3: Rozszerzenia
- Machine Learning dla klasyfikacji
- Integracja z bazą precedensów
- Automatyczne generowanie dokumentów
- Dashboard analityczny

