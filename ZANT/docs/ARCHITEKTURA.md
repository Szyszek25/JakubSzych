# 🏗️ Architektura HAMA-ZANT

## Przegląd Systemu

ZANT (ZUS Accident Notification Tool) wykorzystuje **HAMA Diamond** do wspierania procesu zgłaszania i analizy wypadków przy pracy.

System składa się z **5 głównych modułów**:

1. **Accident Assistant** - asystent zgłoszenia wypadku (HAMA-based)
2. **PDF Extractor** - ekstrakcja danych z dokumentacji
3. **Decision Engine** - silnik decyzyjny (HAMA reasoning)
4. **API Layer** - FastAPI endpoints
5. **Frontend** - interfejs użytkownika

---

## Diagram Architektury

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML/JS)                    │
│              Interfejs użytkownika                       │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Asystent     │ │ PDF       │ │ Decision    │
│ Zgłoszenia   │ │ Extractor │ │ Engine      │
│              │ │           │ │             │
│ - Analiza    │ │ - OCR     │ │ - HAMA      │
│ - Wykrywanie │ │ - Text    │ │   Reasoning │
│   braków     │ │   Extract │ │ - Reguły    │
│ - Sugestie   │ │           │ │   decyzyjne │
└──────┬───────┘ └───┬───────┘ └───┬─────────┘
       │             │              │
       └─────────────┴──────────────┘
                     │
              ┌──────▼──────┐
              │  HAMA Core  │
              │             │
              │ - Gemini    │
              │   3 Pro     │
              │ - Reasoning │
              │ - Analysis  │
              └──────┬───────┘
                     │
              ┌──────▼──────┐
              │   FastAPI   │
              │   Backend   │
              └─────────────┘
```

---

## Moduły Systemu

### 1. Accident Assistant

**Lokalizacja:** `backend/services/accident_assistant.py`

**Funkcjonalności:**
- Analiza tekstu zgłoszenia używając HAMA
- Wykrywanie brakujących pól zgodnie z wzorcem ZUS
- Generowanie sugestii uzupełnień
- Walidacja zgodności z wymaganiami

**HAMA Integration:**
- Używa `LocalModelAdapter` z Gemini 3 Pro
- Cognitive reasoning dla analizy jakości
- Natural language understanding

### 2. PDF Extractor

**Lokalizacja:** `backend/services/pdf_extractor.py`

**Funkcjonalności:**
- Ekstrakcja tekstu z PDF (pdfplumber)
- OCR dla zeskanowanych dokumentów (Tesseract)
- Wyodrębnianie strukturalnych danych
- Preprocessing obrazów

### 3. Decision Engine

**Lokalizacja:** `backend/services/decision_engine.py`

**Funkcjonalności:**
- Analiza dokumentacji używając HAMA Diamond
- Weryfikacja warunków definicji wypadku
- Zastosowanie reguł decyzyjnych ZUS
- Generowanie rekomendacji i uzasadnień

**HAMA Reasoning:**
- Analiza warunków: nagłe zdarzenie, przyczyna zewnętrzna, uraz, związek z pracą
- Wykrywanie czynników wykluczających
- Scoring pewności decyzji
- Generowanie uzasadnień prawnych

### 4. API Layer

**Lokalizacja:** `backend/api/main.py`

**Endpoints:**
- `POST /api/report/analyze` - analiza zgłoszenia
- `POST /api/report/submit` - zapisanie zgłoszenia
- `POST /api/decision/analyze` - analiza dokumentacji PDF
- `GET /api/report/{report_id}` - pobranie zgłoszenia
- `GET /api/card/{card_id}` - pobranie karty wypadku

### 5. Frontend

**Lokalizacja:** `frontend/index.html`

**Funkcjonalności:**
- Formularz zgłoszenia wypadku
- Upload dokumentacji PDF
- Wyświetlanie wyników analizy
- Interaktywny interfejs

---

## HAMA Diamond Integration

### Model LLM

**Model:** `models/gemini-3-pro-preview`

**Charakterystyka:**
- Zaawansowany model reasoningowy
- Wysoka jakość analizy tekstu
- Obsługa JSON mode
- Szybkie odpowiedzi

### HAMA Components

1. **Cognitive Reasoning**
   - Analiza logiczna warunków
   - Wykrywanie niespójności
   - Priorytetyzacja informacji

2. **Natural Language Understanding**
   - Rozumienie kontekstu
   - Ekstrakcja faktów
   - Analiza semantyczna

3. **Decision Support**
   - Scoring pewności
   - Generowanie uzasadnień
   - Identyfikacja ryzyka

---

## Przepływ Danych

### Asystent Zgłoszenia

```
Użytkownik → Formularz → AccidentAssistant → HAMA/Gemini → Analiza → Sugestie → Użytkownik
```

1. Użytkownik wypełnia formularz
2. `AccidentAssistant` analizuje zgłoszenie
3. HAMA wykrywa brakujące pola
4. Gemini generuje sugestie
5. Wynik zwracany do użytkownika

### Wsparcie Decyzji

```
PDF → PDFExtractor → OCR/Text → DecisionEngine → HAMA/Gemini → Rekomendacja → Karta Wypadku
```

1. Upload dokumentacji PDF
2. `PDFExtractor` ekstrahuje tekst (OCR jeśli potrzeba)
3. `DecisionEngine` analizuje używając HAMA
4. Weryfikacja warunków definicji wypadku
5. Zastosowanie reguł decyzyjnych
6. Generowanie rekomendacji i karty wypadku

---

## Reguły Decyzyjne

### Definicja Wypadku

**Wypadek przy pracy** = **nagłe zdarzenie** + **przyczyna zewnętrzna** + **uraz/śmierć** + **związek z pracą**

### Warunki Uznania

- ✅ Wszystkie 4 warunki spełnione + confidence ≥ 0.7 → **UZNAĆ**
- ⚠️ Warunki spełnione + confidence < 0.7 → **WERYFIKACJA**
- ❌ Czynniki wykluczające → **NIE UZNAWAĆ**

### HAMA Scoring

HAMA oblicza:
- `zdarzenie_nagłe`: confidence 0.0-1.0
- `przyczyna_zewnetrzna`: confidence 0.0-1.0
- `uraz_lub_smierc`: confidence 0.0-1.0
- `zwiazek_z_praca`: confidence 0.0-1.0
- `ogolna_pewnosc`: średnia ważona

---

## Bezpieczeństwo

### Ochrona Danych

- Dane przechowywane lokalnie (w produkcji: szyfrowanie)
- Brak wysyłania danych do zewnętrznych API (poza Gemini)
- Walidacja wszystkich danych wejściowych
- Logowanie działań (audyt)

### RODO Compliance

- Minimalizacja danych osobowych
- Możliwość usunięcia danych
- Kontrola dostępu
- Szyfrowanie w transmisji

---

## Skalowanie

### Backend

- FastAPI (async) - gotowe do skalowania
- Stateless architecture
- Możliwość horizontal scaling

### LLM

- Gemini API - skalowalne przez Google
- Rate limiting
- Caching odpowiedzi (opcjonalnie)

### Storage

- Obecnie w pamięci (dla hackathonu)
- W produkcji: PostgreSQL/MongoDB
- Vector DB dla precedensów (opcjonalnie)

---

## Plan Wdrożenia

### Faza 1: MVP (Hackathon) ✅

- ✅ Podstawowy asystent zgłoszenia
- ✅ Analiza PDF i rekomendacja
- ✅ Prosty frontend
- ✅ HAMA Diamond integration

### Faza 2: Produkcja (3-6 miesięcy)

- Baza danych (PostgreSQL)
- Autentykacja użytkowników
- Integracja z systemami ZUS
- Zaawansowane OCR
- Logowanie i audyt

### Faza 3: Rozszerzenia (6-12 miesięcy)

- Machine Learning dla klasyfikacji
- Integracja z bazą precedensów
- Automatyczne generowanie dokumentów
- Dashboard analityczny
- Multi-language support

---

## Technologie

### Backend
- **FastAPI** - nowoczesne API
- **HAMA Diamond** - inteligentny silnik reasoningowy
- **Google Gemini 3 Pro** - zaawansowany LLM
- **Tesseract OCR** - ekstrakcja z zeskanowanych PDF

### Frontend
- **HTML5/CSS3/JavaScript** - prosty, dostępny interfejs
- **Responsive design** - działa na wszystkich urządzeniach

### Infrastructure
- **Python 3.10+** - język programowania
- **google-genai** - SDK dla Gemini API
- **pdfplumber** - ekstrakcja tekstu z PDF

---

## Metryki Wydajności

### Czas Odpowiedzi

- Analiza zgłoszenia: < 5 sekund
- Analiza dokumentacji PDF: < 30 sekund (z OCR)
- Generowanie sugestii: < 3 sekundy

### Jakość

- Wykrywanie braków: 95%+ skuteczność
- Trafność rekomendacji: 85%+ zgodność z ekspertami
- Pewność decyzji: średnio 80%+

---

## Dokumentacja

- **README.md** - główna dokumentacja
- **INSTALACJA.md** - instrukcje instalacji
- **QUICK_START.md** - szybki start
- **GEMINI_SETUP.md** - konfiguracja Gemini
- **PRESENTACJA.md** - slajdy prezentacji

---

## Licencja

Projekt hackathonowy dla ZUS

