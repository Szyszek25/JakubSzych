# 🏗️ Architektura GQPA-Indeks Branż

## Przegląd Systemu

System składa się z **7 głównych modułów**:

1. **Data Collector** - pobieranie danych
2. **Indicators** - obliczanie wskaźników
3. **GQPA Scoring** - scoring i agregacja
4. **Classifier** - klasyfikacja branż
5. **Visualizer** - wizualizacje
6. **Report Generator** - generowanie raportów
7. **Main** - orkiestracja

---

## Diagram Architektury

```
┌─────────────────────────────────────────────────────────┐
│                    MAIN (main.py)                       │
│              Orkiestracja całego procesu                │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Data         │ │          │ │             │
│ Collector    │ │ Indicators│ │ GQPA Scoring│
│              │ │           │ │             │
│ - GUS        │ │ - 10      │ │ - Normalize │
│ - KRS        │ │   wskaźników│ │ - Weight   │
│ - Trends     │ │           │ │ - Aggregate │
│ - NBP        │ │           │ │             │
└──────┬───────┘ └───┬───────┘ └───┬─────────┘
       │             │              │
       └─────────────┴──────────────┘
                     │
              ┌──────▼──────┐
              │  Classifier │
              │             │
              │ - 5 kategorii│
              └──────┬───────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Visualizer   │ │ Report    │ │ CSV Export  │
│              │ │ Generator │ │             │
│ - Ranking    │ │           │ │ - CSV       │
│ - Risk Map   │ │ - Ogólny  │ │ - Excel     │
│ - Categories │ │ - Branżowe│ │             │
└──────────────┘ └───────────┘ └─────────────┘
```

---

## Moduły Szczegółowo

### 1. Data Collector (`data_collector.py`)

**Odpowiedzialność**: Pobieranie danych z zewnętrznych źródeł

**Klasy**:
- `DataCollector` - główna klasa

**Metody**:
- `collect_all_data()` - pobiera wszystkie dane
- `_collect_gus_data()` - dane GUS
- `_collect_krs_data()` - dane KRS
- `_collect_google_trends()` - Google Trends
- `_collect_npk_data()` - nastroje konsumenckie

**Dane wyjściowe**: Dict z DataFrame dla każdego źródła

---

### 2. Indicators (`indicators.py`)

**Odpowiedzialność**: Obliczanie wskaźników branżowych

**Klasy**:
- `IndustryIndicators` - główna klasa

**Metody**:
- `calculate_all_indicators()` - oblicza wszystkie wskaźniki
- `_calculate_revenue_growth()` - dynamika przychodów
- `_calculate_profitability()` - rentowność
- `_calculate_debt_ratio()` - zadłużenie
- `_calculate_failure_rate()` - szkodowość
- `_calculate_export_growth()` - dynamika eksportu
- `_calculate_investment_growth()` - inwestycje
- `_calculate_consumer_sentiment()` - nastroje
- `_calculate_search_trends()` - trendy wyszukiwań
- `_calculate_new_companies_growth()` - nowe firmy
- `_calculate_productivity()` - produktywność

**Dane wyjściowe**: DataFrame z wskaźnikami dla każdej branży

---

### 3. GQPA Scoring (`gqpa_scoring.py`)

**Odpowiedzialność**: Scoring i agregacja wskaźników

**Klasy**:
- `GQPAScoringEngine` - główna klasa

**Metody**:
- `calculate_index()` - główna metoda obliczania indeksu
- `_normalize_indicators()` - normalizacja (ETAP 2)
- `_calculate_dynamic_weights()` - dynamiczne ważenie (ETAP 3)
- `_aggregate_to_index()` - agregacja (ETAP 4)
- `get_weights_explanation()` - wyjaśnienie wag

**Integracja z GQPA**:
- Używa `EnhancedCognitiveAgent` z GQPA Core (opcjonalnie)
- Analiza korelacji między wskaźnikami
- Dynamiczne dostosowywanie wag

**Dane wyjściowe**: DataFrame z indeksem GQPA (0-100)

---

### 4. Classifier (`classifier.py`)

**Odpowiedzialność**: Klasyfikacja branż do kategorii

**Klasy**:
- `IndustryClassifier` - główna klasa

**Metody**:
- `classify_industries()` - klasyfikuje branże
- `get_category_summary()` - podsumowanie kategorii

**Logika klasyfikacji**:
1. Podstawowa klasyfikacja na podstawie indeksu
2. Dodatkowa logika dla "Wymagające finansowania"

**Dane wyjściowe**: DataFrame z kolumną 'kategoria'

---

### 5. Visualizer (`visualizer.py`)

**Odpowiedzialność**: Tworzenie wizualizacji

**Klasy**:
- `IndustryVisualizer` - główna klasa

**Metody**:
- `create_all_visualizations()` - tworzy wszystkie wykresy
- `_create_ranking_chart()` - ranking branż
- `_create_risk_map()` - mapa ryzyka
- `_create_categories_chart()` - rozkład kategorii
- `_create_indicators_comparison()` - porównanie wskaźników

**Technologie**:
- Plotly (interaktywne wykresy)
- HTML export

**Dane wyjściowe**: Pliki HTML w `outputs/wykresy/`

---

### 6. Report Generator (`report_generator.py`)

**Odpowiedzialność**: Generowanie raportów tekstowych

**Klasy**:
- `ReportGenerator` - główna klasa

**Metody**:
- `generate_all_reports()` - generuje wszystkie raporty
- `_generate_general_report()` - raport ogólny
- `_generate_branch_report()` - raport dla branży

**Format**:
- Markdown (łatwa konwersja do PDF)
- Naturalny język polski

**Dane wyjściowe**: Pliki Markdown w `outputs/raporty/`

---

### 7. Main (`main.py`)

**Odpowiedzialność**: Orkiestracja całego procesu

**Funkcje**:
- `main()` - główna funkcja

**Argumenty wiersza poleceń**:
- `--full` - pełna analiza
- `--scoring-only` - tylko scoring
- `--visualize-only` - tylko wizualizacje
- `--no-viz` - pomiń wizualizacje
- `--no-reports` - pomiń raporty

**Przepływ**:
1. Pobieranie danych
2. Obliczanie wskaźników
3. Scoring GQPA
4. Klasyfikacja
5. Eksport do CSV
6. Wizualizacje
7. Generowanie raportów

---

## Struktura Danych

### DataFrame Indicators

```
pkd | nazwa | dynamika_przychodow | rentownosc | zadluzenie | ...
----|-------|---------------------|------------|------------|----
46  | Handel| 5.2                | 8.5        | 1.2        | ...
```

### DataFrame Index

```
pkd | nazwa | indeks_gqpa | dynamika_przychodow_norm | waga_dynamika_przychodow | ...
----|-------|-------------|--------------------------|-------------------------|----
46  | Handel| 72.3        | 0.65                      | 0.20                     | ...
```

### DataFrame Classified

```
pkd | nazwa | indeks_gqpa | kategoria | kategoria_opis | ...
----|-------|-------------|------------|----------------|----
46  | Handel| 72.3        | stabilne   | Branże o...    | ...
```

---

## Konfiguracja

### Plik `config.py`

Zawiera:
- Definicje branż (PKD)
- Wagi wskaźników
- Kategorie branż
- Źródła danych
- Parametry GQPA
- Konfiguracja wizualizacji

---

## Zależności

### Wymagane:
- pandas, numpy, scipy
- plotly, matplotlib, seaborn
- requests, beautifulsoup4

### Opcjonalne:
- pytrends (Google Trends)
- openpyxl (Excel export)

### GQPA Core:
- `gqpa_part1.py` - typy danych
- `gqpa_part4.py` - WorldModel
- `gqpa_part5.py` - EnhancedCognitiveAgent

---

## Rozszerzalność

### Dodanie nowego wskaźnika:

1. Dodaj metodę w `indicators.py`:
   ```python
   def _calculate_new_indicator(self, df, pkd):
       # logika obliczania
       return value
   ```

2. Dodaj do `calculate_all_indicators()`:
   ```python
   indicators['nowy_wskaźnik'] = self._calculate_new_indicator(gus_df, pkd)
   ```

3. Dodaj wagę w `config.py`:
   ```python
   WSKAZNIKI_WAGI['nowy_wskaźnik'] = 0.05
   ```

4. Zaktualizuj normalizację w `gqpa_scoring.py`

### Dodanie nowego źródła danych:

1. Dodaj metodę w `data_collector.py`:
   ```python
   def _collect_new_source(self):
       # logika pobierania
       return df
   ```

2. Dodaj do `collect_all_data()`:
   ```python
   data['nowe_zrodlo'] = self._collect_new_source()
   ```

3. Użyj w `indicators.py` do obliczania wskaźników

---

## Testowanie

### Testy jednostkowe:

Każdy moduł może być testowany osobno:

```python
# Test data_collector
collector = DataCollector()
data = collector.collect_all_data()

# Test indicators
indicators = IndustryIndicators()
df_indicators = indicators.calculate_all_indicators(data)

# Test scoring
scoring = GQPAScoringEngine()
df_index = scoring.calculate_index(df_indicators)
```

### Testy integracyjne:

Uruchom pełną analizę:

```bash
python main.py --full
```

---

## Wydajność

### Optymalizacje:

- **Caching** - zapis surowych danych
- **Lazy loading** - ładowanie tylko potrzebnych danych
- **Parallel processing** - równoległe pobieranie danych (opcjonalnie)

### Czas wykonania:

- Pobieranie danych: ~30-60 sekund
- Obliczanie wskaźników: ~1-2 sekundy
- Scoring: ~2-5 sekund
- Klasyfikacja: ~0.5 sekundy
- Wizualizacje: ~5-10 sekund
- Raporty: ~2-5 sekund

**Total**: ~1-2 minuty dla 10 branż

---

## Bezpieczeństwo

### Walidacja danych:

- Sprawdzanie zakresów wartości
- Obsługa brakujących danych
- Walidacja formatów

### Obsługa błędów:

- Try-except dla każdego źródła danych
- Fallback values dla brakujących danych
- Logowanie błędów

---

**Architektura jest modularna, łatwa w utrzymaniu i rozbudowie.**


