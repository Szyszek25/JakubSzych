# 📚 Źródła Danych - HAMA-ZANT

## Przegląd

ZANT wykorzystuje różne źródła danych do analizy zgłoszeń wypadków przy pracy. Dokument opisuje wszystkie źródła danych używane w systemie.

---

## 1. Dane Wejściowe od Użytkownika

### 1.1 Zgłoszenie Wypadku

**Źródło:** Formularz wypełniany przez obywatela

**Dane:**
- Data wypadku (YYYY-MM-DD)
- Godzina wypadku (HH:MM)
- Miejsce wypadku (tekst)
- Okoliczności wypadku (tekst narracyjny)
- Przyczyna wypadku (tekst)
- Dane poszkodowanego (imię, nazwisko, PESEL/NIP)
- Rodzaj działalności (tekst)
- Opis urazu (tekst)

**Format:** JSON przez API

**Walidacja:**
- Wymagane pola zgodnie z wzorcem ZUS
- Format daty i godziny
- Długość tekstu (min/max)

### 1.2 Dokumentacja PDF

**Źródło:** Upload pliku PDF przez pracownika ZUS

**Typy dokumentów:**
- Karty wypadków
- Zaświadczenia lekarskie
- Protokoły
- Inne dokumenty związane z wypadkiem

**Przetwarzanie:**
- Tekstowe PDF: bezpośrednia ekstrakcja
- Zeskanowane PDF: OCR (Tesseract)

---

## 2. Wzorzec ZUS

### 2.1 Wzorzec Zgłoszenia

**Źródło:** `backend/config.py` - `ZUS_ACCIDENT_REPORT_TEMPLATE`

**Zawartość:**
- Lista wymaganych pól
- Opisy pól
- Format wymagany dla każdego pola

**Użycie:**
- Walidacja kompletności zgłoszenia
- Generowanie sugestii
- Wykrywanie brakujących elementów

### 2.2 Definicja Wypadku

**Źródło:** `backend/config.py` - `ACCIDENT_DEFINITION`

**Zawartość:**
- Definicja wypadku przy pracy
- Wymagane warunki (4 warunki)
- Czynniki wykluczające

**Użycie:**
- Weryfikacja czy zdarzenie jest wypadkiem
- Analiza warunków
- Identyfikacja wykluczeń

### 2.3 Reguły Decyzyjne

**Źródło:** `backend/config.py` - `DECISION_RULES`

**Zawartość:**
- Warunki uznania wypadku
- Warunki nieuznania wypadku
- Próg pewności (min_confidence: 0.7)

**Użycie:**
- Zastosowanie reguł decyzyjnych
- Generowanie rekomendacji
- Scoring pewności

---

## 3. HAMA Diamond Knowledge Base

### 3.1 Model LLM

**Źródło:** Google Gemini API

**Model:** `models/gemini-3-pro-preview`

**Zawartość:**
- Wiedza ogólna o wypadkach przy pracy
- Rozumienie języka polskiego
- Reasoning capabilities
- Legal knowledge

**Użycie:**
- Analiza tekstu narracyjnego
- Wykrywanie brakujących elementów
- Generowanie sugestii
- Analiza warunków definicji
- Generowanie uzasadnień

### 3.2 Cognitive Reasoning

**Źródło:** HAMA Diamond Framework

**Zawartość:**
- Logika reasoningowa
- Pattern matching
- Context understanding
- Uncertainty handling

**Użycie:**
- Analiza logiczna warunków
- Wykrywanie niespójności
- Scoring pewności
- Risk assessment

---

## 4. Precedensy i Przykłady

### 4.1 Przykładowe Zgłoszenia

**Źródło:** Dane testowe od ZUS

**Zawartość:**
- Kilkadziesiąt prawdziwych przypadków
- Karty wypadków
- Rozstrzygnięcia ZUS

**Użycie:**
- Testowanie systemu
- Walidacja jakości
- Benchmarki

**Status:** Dostępne podczas hackathonu

### 4.2 Baza Precedensów (Planowane)

**Źródło:** System ZUS (integracja przyszłościowa)

**Zawartość:**
- Historia decyzji ZUS
- Podobne przypadki
- Statystyki

**Użycie:**
- Porównanie z podobnymi przypadkami
- Analiza trendów
- Uczenie się z historii

**Status:** Planowane dla produkcji

---

## 5. Podstawy Prawne

### 5.1 Ustawa o Ubezpieczeniu Społecznym

**Źródło:** Przepisy prawne

**Zawartość:**
- Ustawa z dnia 30 października 2002 r.
- Definicje prawne
- Warunki uznania wypadku

**Użycie:**
- Weryfikacja zgodności
- Generowanie podstaw prawnych
- Uzasadnienia decyzji

### 5.2 Wytyczne ZUS

**Źródło:** Dokumentacja wewnętrzna ZUS

**Zawartość:**
- Procedury ZUS
- Wzorce dokumentów
- Wytyczne interpretacyjne

**Użycie:**
- Walidacja zgodności z procedurami
- Generowanie dokumentów
- Zapewnienie spójności

---

## 6. Dane Techniczne

### 6.1 Konfiguracja Systemu

**Źródło:** `backend/config.py`

**Zawartość:**
- Ustawienia API
- Konfiguracja OCR
- Parametry HAMA
- Limity i progi

**Użycie:**
- Konfiguracja systemu
- Dostosowanie parametrów
- Optymalizacja wydajności

### 6.2 Logi i Metryki

**Źródło:** System generuje podczas działania

**Zawartość:**
- Logi operacji
- Metryki wydajności
- Statystyki użycia
- Błędy i ostrzeżenia

**Użycie:**
- Debugging
- Monitoring
- Analiza wydajności
- Audyt

---

## Przepływ Danych

### Wejście

```
Użytkownik → Formularz → API → Backend
PDF → Upload → API → PDFExtractor
```

### Przetwarzanie

```
Backend → HAMA/Gemini → Analiza → Reguły → Decyzja
```

### Wyjście

```
Backend → API → Frontend → Użytkownik
Backend → Storage → Raporty → Eksport
```

---

## Bezpieczeństwo Danych

### Ochrona

- **Szyfrowanie** - dane wrażliwe szyfrowane
- **Autentykacja** - kontrola dostępu
- **Audyt** - logowanie operacji
- **Minimalizacja** - tylko niezbędne dane

### RODO Compliance

- **Prawo do usunięcia** - możliwość usunięcia danych
- **Prawo do dostępu** - dostęp do swoich danych
- **Poufność** - dane nie udostępniane osobom trzecim
- **Bezpieczeństwo** - ochrona przed wyciekiem

---

## Planowane Rozszerzenia

### 1. Integracja z Systemami ZUS

- Połączenie z bazą danych ZUS
- Synchronizacja z systemami wewnętrznymi
- Automatyczne pobieranie danych

### 2. Baza Precedensów

- Vector database dla podobnych przypadków
- Semantic search
- Recommendation engine

### 3. Zewnętrzne Źródła

- Integracja z systemami medycznymi
- Dane z urzędów
- Statystyki GUS

---

## Podsumowanie

ZANT wykorzystuje:
- ✅ **Dane użytkownika** - zgłoszenia i dokumentacja
- ✅ **Wzorce ZUS** - formalne wymagania
- ✅ **HAMA Diamond** - inteligentna analiza
- ✅ **Gemini 3 Pro** - zaawansowany LLM
- ✅ **Przepisy prawne** - podstawy decyzji

Rezultat: **Kompleksowy system wsparcia decyzji** oparty na wiarygodnych źródłach

