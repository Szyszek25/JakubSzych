# GQPA-INDEKS BRANŻ
## System Analizy Kondycji Branż w Polsce

**Hackathon PKO BP 2025**

---

## SLIDE 1: PROBLEM I CEL

### Problem
- Bank potrzebuje narzędzia do oceny kondycji branż
- Kluczowe dla portfela kredytowego i strategii sektorowych
- Wymaga syntetycznej oceny wielu wskaźników

### Rozwiązanie
**GQPA-Indeks Branż** - system wykorzystujący **GQPA (General Quantitative Policy Analysis)** do:
- Agregacji danych z wielu źródeł
- Budowy syntetycznego indeksu branżowego
- Klasyfikacji i rankingowania branż
- Generowania automatycznych raportów

---

## SLIDE 2: METODOLOGIA - 6 ETAPÓW GQPA

1. **Zbieranie danych** - GUS, KRS, Google Trends, NBP
2. **Normalizacja** - standaryzacja wskaźników (0-1)
3. **Dynamiczne ważenie** - GQPA przypisuje wagi
4. **Agregacja** - syntetyczny indeks (0-100)
5. **Klasyfikacja** - 5 kategorii branż
6. **Interpretacja** - raporty tekstowe

### Dlaczego GQPA?
- Deterministyczna metodologia (uzasadnione wagi)
- Interpretowalność wyników
- Automatyczna analiza korelacji
- Generowanie naturalnych raportów

---

## SLIDE 3: WSKAŹNIKI BRANŻOWE

System analizuje **10 wskaźników**:

| Wskaźnik | Waga | Źródło |
|----------|------|--------|
| Dynamika przychodów | 20% | GUS |
| Rentowność | 15% | GUS |
| Zadłużenie | 15% | GUS |
| Szkodowość | 15% | KRS |
| Dynamika eksportu | 10% | GUS |
| Inwestycje | 10% | GUS |
| Nastroje konsumenckie | 5% | NBP |
| Trendy wyszukiwań | 5% | Google Trends |
| Nowe firmy | 3% | KRS |
| Produktywność | 2% | GUS |

**Wagi są dynamicznie dostosowywane przez GQPA** na podstawie korelacji między wskaźnikami.

---

## SLIDE 4: KLASYFIKACJA BRANŻ

System klasyfikuje branże do **5 kategorii**:

1. **🚀 Wzrostowe** (indeks 70-100)
   - Wysokie tempo rozwoju, niskie ryzyko
   - Rekomendacja: zwiększone finansowanie

2. **✅ Stabilne** (indeks 50-70)
   - Umiarkowany wzrost, stabilne fundamenty
   - Rekomendacja: standardowe finansowanie

3. **⚠️ Ryzykowne** (indeks 30-50)
   - Wysokie zadłużenie lub spowolnienie
   - Rekomendacja: ograniczone finansowanie

4. **📉 Kurczące się** (indeks 0-30)
   - Negatywna dynamika, wysokie ryzyko
   - Rekomendacja: minimalizacja ekspozycji

5. **💰 Wymagające finansowania** (indeks 40-70)
   - Potencjał wzrostu, potrzeba kapitału
   - Rekomendacja: selektywne finansowanie

---

## SLIDE 5: PRZYKŁADOWE WYNIKI

### Top 5 Branż (Najwyższy Indeks)

| Branża | Indeks | Kategoria |
|--------|--------|-----------|
| Działalność związana z oprogramowaniem | 85.2 | Wzrostowe |
| Produkcja komputerów i elektroniki | 78.5 | Wzrostowe |
| Handel hurtowy | 72.3 | Stabilne |
| Transport lądowy | 68.9 | Stabilne |
| Budownictwo | 65.4 | Stabilne |

### Branże Wymagające Uwagi

| Branża | Indeks | Kategoria | Problem |
|--------|--------|-----------|---------|
| Działalność związana z nieruchomościami | 42.1 | Ryzykowne | Wysokie zadłużenie |
| Zakwaterowanie i gastronomia | 38.7 | Ryzykowne | Spowolnienie |

---

## SLIDE 6: WIZUALIZACJE

System generuje **interaktywne wykresy**:

1. **Ranking branż** - bar chart z kolorami kategorii
2. **Mapa ryzyka** - scatter plot (indeks vs zadłużenie)
3. **Rozkład kategorii** - pie chart
4. **Porównanie wskaźników** - radar chart (top 5 branż)

### Korzyści
- Intuicyjna prezentacja wyników
- Interaktywne eksplorowanie danych
- Gotowe do prezentacji zarządowi

---

## SLIDE 7: AUTOMATYCZNE RAPORTY

System generuje **raporty tekstowe** dla:

### Raport Ogólny
- Statystyki wszystkich branż
- Top 5 i Bottom 5
- Perspektywy na 12-36 miesięcy
- Rekomendacje ogólne

### Raporty Branżowe
- Analiza wskaźników dla każdej branży
- Interpretacja wyników
- Konkretne rekomendacje dla działów ryzyka

### Format
- Markdown (łatwa konwersja do PDF)
- Naturalny język polski
- Gotowe do użycia przez analityków

---

## SLIDE 8: ARCHITEKTURA SYSTEMU

```
┌─────────────────┐
│  Data Collector │  ← GUS, KRS, Google Trends, NBP
└────────┬────────┘
         │
┌────────▼────────┐
│   Indicators     │  ← 10 wskaźników branżowych
└────────┬────────┘
         │
┌────────▼────────┐
│  GQPA Scoring   │  ← Normalizacja + Ważenie + Agregacja
└────────┬────────┘
         │
┌────────▼────────┐
│   Classifier    │  ← 5 kategorii
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│Viz    │ │Reports│
└───────┘ └───────┘
```

**Modularna architektura** - łatwa rozbudowa i utrzymanie.

---

## SLIDE 9: PERSPEKTYWY WDROŻENIOWE

### Automatyzacja
- Cykliczne pobieranie danych (co miesiąc/kwartał)
- Automatyczne odświeżanie indeksu
- Powiadomienia o zmianach kategorii

### Integracja
- API dla innych systemów bankowych
- Dashboard dla analityków
- Eksport do systemów BI

### Rozszerzenia
- Więcej źródeł danych (np. dane giełdowe)
- Predykcje ML (opcjonalnie)
- Analiza sezonowości
- Benchmarki międzynarodowe

### Wartość dla PKO BP
- **Redukcja ryzyka** - wczesne wykrywanie problemów
- **Optymalizacja portfela** - alokacja kapitału
- **Automatyzacja** - oszczędność czasu analityków
- **Uzasadnienie decyzji** - transparentna metodologia

---

## SLIDE 10: PODSUMOWANIE

### Co oferujemy?

✅ **Kompletne rozwiązanie** - od danych do raportów
✅ **Metodologia GQPA** - deterministyczna i uzasadniona
✅ **10 wskaźników** - wielowymiarowa analiza
✅ **5 kategorii** - czytelna klasyfikacja
✅ **Automatyczne raporty** - gotowe do użycia
✅ **Interaktywne wizualizacje** - prezentacja wyników
✅ **Gotowość do wdrożenia** - modularna architektura

### Deliverables

📁 **Repozytorium kodu** - kompletny system
📊 **CSV/XLSX** - indeks branż z wskaźnikami
📄 **Prezentacja** - 10 slajdów (ten dokument)
🎬 **Film** - 3-minutowa prezentacja (opcjonalnie)

### Kontakt

- **Discord**: `indeks-branż`
- **Stoisko**: PKO BP Hackathon

---

**Dziękujemy za uwagę!**

*GQPA-Indeks Branż - System analizy kondycji branż w Polsce*


