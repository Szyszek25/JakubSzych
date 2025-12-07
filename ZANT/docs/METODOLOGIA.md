# 📊 Metodologia HAMA-ZANT

## Wprowadzenie

ZANT wykorzystuje **HAMA Diamond** (Hybrid Adaptive Multi-Agent) do inteligentnej analizy zgłoszeń wypadków przy pracy. Metodologia opiera się na kombinacji:

1. **HAMA Reasoning** - analiza logiczna i kognitywna
2. **Reguły Decyzyjne ZUS** - formalne przepisy
3. **Natural Language Processing** - rozumienie tekstu
4. **Pattern Matching** - wykrywanie wzorców

---

## Metodologia Analizy Zgłoszenia

### Krok 1: Ekstrakcja Informacji

**Cel:** Wyodrębnienie wszystkich dostępnych danych z zgłoszenia

**Metody:**
- Parsowanie strukturalnych pól (data, godzina, miejsce)
- Analiza tekstu narracyjnego (okoliczności, przyczyny)
- Wykrywanie encji (osoby, miejsca, zdarzenia)

**HAMA Contribution:**
- Semantic understanding - rozumienie kontekstu
- Entity extraction - wyodrębnianie faktów
- Relation detection - wykrywanie relacji

### Krok 2: Weryfikacja Kompletności

**Cel:** Sprawdzenie czy wszystkie wymagane pola są wypełnione

**Wzorzec ZUS:**
- 8 wymaganych pól
- Priorytetyzacja (high/medium/low)
- Walidacja formatów

**HAMA Contribution:**
- Intelligent gap detection - wykrywanie braków w kontekście
- Quality assessment - ocena jakości wypełnionych pól
- Suggestion generation - generowanie sugestii

### Krok 3: Analiza Jakości

**Cel:** Ocena czy wypełnione pola są wystarczająco szczegółowe

**Kryteria:**
- Szczegółowość opisu
- Spójność informacji
- Zgodność z wymaganiami

**HAMA Contribution:**
- Cognitive analysis - analiza kognitywna
- Consistency checking - sprawdzanie spójności
- Improvement suggestions - sugestie ulepszeń

---

## Metodologia Analizy Decyzji

### Krok 1: Ekstrakcja z Dokumentacji

**Cel:** Wyodrębnienie danych z dokumentacji PDF

**Metody:**
- Tekstowe PDF: bezpośrednia ekstrakcja
- Zeskanowane PDF: OCR (Tesseract)
- Strukturalne dane: regex patterns + HAMA

**HAMA Contribution:**
- Intelligent extraction - inteligentna ekstrakcja
- Context understanding - rozumienie kontekstu
- Data validation - walidacja danych

### Krok 2: Weryfikacja Warunków Definicji

**Cel:** Sprawdzenie czy zdarzenie spełnia definicję wypadku

**Definicja Wypadku:**
```
Nagłe zdarzenie wywołane przyczyną zewnętrzną, 
powodujące uraz lub śmierć, związane z pracą
```

**4 Warunki:**
1. **Zdarzenie nagłe** - czy było nagłe?
2. **Przyczyna zewnętrzna** - czy była przyczyna zewnętrzna?
3. **Uraz lub śmierć** - czy nastąpił uraz/śmierć?
4. **Związek z pracą** - czy było związane z pracą?

**HAMA Contribution:**
- Logical reasoning - rozumowanie logiczne
- Evidence evaluation - ocena dowodów
- Confidence scoring - scoring pewności

### Krok 3: Zastosowanie Reguł Decyzyjnych

**Cel:** Wygenerowanie rekomendacji na podstawie warunków

**Reguły:**

**UZNAĆ jeśli:**
- Wszystkie 4 warunki spełnione
- Confidence ≥ 0.7
- Brak czynników wykluczających

**NIE UZNAWAĆ jeśli:**
- Czynniki wykluczające obecne
- Brak związku z pracą
- Choroba zawodowa

**WERYFIKACJA jeśli:**
- Warunki spełnione ale confidence < 0.7
- Niepewność co do warunków

**HAMA Contribution:**
- Rule application - zastosowanie reguł
- Uncertainty handling - obsługa niepewności
- Risk assessment - ocena ryzyka

### Krok 4: Generowanie Uzasadnienia

**Cel:** Stworzenie szczegółowego uzasadnienia decyzji

**Elementy:**
- Analiza każdego warunku
- Uzasadnienie dla każdego warunku
- Podstawa prawna
- Czynniki ryzyka

**HAMA Contribution:**
- Explanation generation - generowanie wyjaśnień
- Legal basis extraction - wyodrębnianie podstaw prawnych
- Risk factor identification - identyfikacja czynników ryzyka

---

## HAMA Diamond Framework

### G - Generalization (Uogólnianie)

**Zastosowanie w ZANT:**
- Uczenie się z poprzednich przypadków
- Transfer knowledge między podobnymi wypadkami
- Adaptacja do nowych sytuacji

### Q - Quality (Jakość)

**Zastosowanie w ZANT:**
- Robustność analizy
- Wykrywanie błędów
- Walidacja wyników

### P - Performance (Wydajność)

**Zastosowanie w ZANT:**
- Szybka analiza (< 30 sekund)
- Efektywne wykorzystanie zasobów
- Skalowalność

### A - Adaptation (Adaptacja)

**Zastosowanie w ZANT:**
- Adaptacja do nowych przepisów
- Uczenie się z feedbacku
- Meta-learning

---

## Scoring i Confidence

### Confidence Scoring

**Metoda:**
1. Analiza każdego warunku osobno
2. Scoring confidence dla każdego warunku (0.0-1.0)
3. Agregacja do overall confidence

**Czynniki wpływające na confidence:**
- Jakość dokumentacji
- Szczegółowość opisu
- Spójność informacji
- Obecność dowodów

### Decision Scoring

**Formuła:**
```
overall_confidence = (Σ confidence_i) / n

decision = 
  if all_confirmed AND overall_confidence >= 0.7: RECOGNIZE
  elif has_exclusions: NOT_RECOGNIZE
  else: NEEDS_REVIEW
```

---

## Walidacja i Testowanie

### Testy Jednostkowe

- Testy każdego modułu osobno
- Mock data dla HAMA
- Testy reguł decyzyjnych

### Testy Integracyjne

- Pełny przepływ: zgłoszenie → analiza → decyzja
- Testy z prawdziwymi danymi ZUS
- Porównanie z decyzjami ekspertów

### Metryki Jakości

- **Accuracy** - trafność rekomendacji
- **Precision** - precyzja wykrywania
- **Recall** - kompletność wykrywania
- **F1-Score** - zbalansowana metryka

---

## Ewaluacja

### Benchmarki

- Porównanie z decyzjami ekspertów ZUS
- Analiza przypadków granicznych
- Testy z różnymi typami wypadków

### Ciągłe Ulepszanie

- Feedback loop z użytkownikami
- Aktualizacja reguł decyzyjnych
- Fine-tuning modelu HAMA

---

## Ograniczenia

### Obecne Ograniczenia

1. **Jakość OCR** - zależy od jakości skanów
2. **Złożone przypadki** - wymagają weryfikacji eksperta
3. **Zmiany przepisów** - wymagają aktualizacji reguł

### Planowane Ulepszenia

1. Lepsze OCR (PaddleOCR)
2. Machine Learning dla klasyfikacji
3. Integracja z bazą precedensów

---

## Podsumowanie

Metodologia HAMA-ZANT łączy:
- **Inteligencję AI** (HAMA Diamond + Gemini 3 Pro)
- **Formalne reguły** (przepisy ZUS)
- **Praktyczne doświadczenie** (precedensy)

Rezultat: **Wysokiej jakości wsparcie decyzji** dla ZUS

