# 💎 HAMA Diamond Visualizations - Kompletny System Wizualizacji

## 📋 Przegląd

System **HAMA Diamond Visualizations** został stworzony dla wszystkich projektów w workspace, wykorzystując zaawansowane wizualizacje 2D i 3D oparte na wynikach analiz.

## 🎯 Projekty z Wizualizacjami HAMA Diamond

### 1. ✅ INDEKS_BRANZ
**Status**: Gotowe i działające

**Moduły**:
- `visualizer.py` - główny moduł wizualizacji
- `hama_scoring.py` - silnik scoringu HAMA Diamond
- `analyze_scenarios.py` - analiza scenariuszy

**Wizualizacje** (7 typów):
1. Ranking branż (bar chart)
2. Mapa ryzyka (scatter 2D)
3. Rozkład kategorii (pie chart)
4. Porównanie wskaźników (radar)
5. **Wykres 3D** - Indeks vs Zadłużenie vs Rentowność
6. **Heatmap korelacji** - korelacje między wskaźnikami
7. **HAMA Diamond Radar** - profil branż

**Lokalizacja wyników**:
- `INDEKS_BRANZ/outputs/wykresy/*.html`
- `INDEKS_BRANZ/outputs/indeks_branz.csv`

---

### 2. ✅ SCENARIUSZE_JUTRA
**Status**: Gotowe i działające

**Moduły**:
- `visualizer_hama.py` - wizualizacje scenariuszy
- `analyze_scenarios.py` - analiza raportów scenariuszy

**Wizualizacje** (6 typów):
1. Prawdopodobieństwa scenariuszy (bar chart)
2. Mapa ryzyka i szans (scatter 2D)
3. **Wykres 3D Timeline** - czas vs prawdopodobieństwo vs wpływ
4. **Heatmap prawdopodobieństw** - typ/horyzont
5. **HAMA Diamond Radar** - profil scenariuszy
6. Porównanie horyzontów (12m vs 36m)

**Lokalizacja wyników**:
- `SCENARIUSZE_JUTRA/outputs/wykresy/*.html`
- `SCENARIUSZE_JUTRA/outputs/analiza_scenariuszy.csv`

**Użycie**:
```bash
cd SCENARIUSZE_JUTRA
python analyze_scenarios.py
```

---

### 3. 📊 GQPA_LEGISLATIVE_NAVIGATOR
**Status**: Moduły gotowe (wymaga danych)

**Moduły**:
- `visualizer_hama.py` - wizualizacje legislacyjne
- `analyze_legislative.py` - analiza dokumentów

**Wizualizacje** (5 typów):
1. Ranking przepisów (bar chart)
2. Mapa wpływu (scatter 2D)
3. **Wykres 3D** - wpływ vs czas vs obszar
4. **Heatmap korelacji** - korelacje między przepisami
5. **HAMA Diamond Radar** - profil przepisów

**Użycie**:
```bash
cd GQPA_LEGISLATIVE_NAVIGATOR
python analyze_legislative.py
```

---

### 4. 📊 AIWSLUZBIE
**Status**: Moduły gotowe (wymaga danych)

**Moduły**:
- `visualizer_hama.py` - wizualizacje spraw administracyjnych

**Wizualizacje** (5 typów):
1. Ranking spraw (bar chart)
2. Mapa ryzyka prawnego (scatter 2D)
3. **Wykres 3D** - priorytet vs ryzyko vs czas
4. **Heatmap korelacji** - korelacje między sprawami
5. **HAMA Diamond Radar** - profil spraw

---

## 🎨 Typy Wizualizacji HAMA Diamond

### Wykresy 2D
- **Bar Charts** - rankingi i porównania
- **Scatter Plots** - mapy ryzyka/szans
- **Pie Charts** - rozkłady kategorii
- **Heatmaps** - korelacje i macierze

### Wykresy 3D
- **Scatter3D** - wielowymiarowa analiza
- **Timeline 3D** - czas vs prawdopodobieństwo vs wpływ

### Wykresy Radarowe
- **HAMA Diamond Radar** - profil wielowymiarowy
- Inspirowany GQPA Diamond Profile

---

## 🚀 Szybki Start

### Dla INDEKS_BRANZ:
```bash
cd INDEKS_BRANZ
python main.py --full
```

### Dla SCENARIUSZE_JUTRA:
```bash
cd SCENARIUSZE_JUTRA
python analyze_scenarios.py
```

### Dla GQPA_LEGISLATIVE_NAVIGATOR:
```bash
cd GQPA_LEGISLATIVE_NAVIGATOR
python analyze_legislative.py
```

---

## 📊 Wspólne Cechy

Wszystkie moduły wykorzystują:
- **HAMA Diamond** jako silnik analityczny
- **Plotly** do interaktywnych wykresów
- **Pandas** do przetwarzania danych
- **Indeks HAMA Diamond** jako syntetyczny wskaźnik

---

## 📁 Struktura Plików

Każdy projekt ma:
```
PROJEKT/
├── visualizer_hama.py      # Moduł wizualizacji
├── analyze_*.py            # Moduł analizy (jeśli potrzebny)
├── outputs/
│   ├── *.csv               # Dane
│   ├── *.md                # Raporty
│   └── wykresy/
│       └── *.html          # Wizualizacje
```

---

## 🎯 Następne Kroki

1. **Dodaj dane** do projektów, które ich potrzebują
2. **Uruchom analizy** dla każdego projektu
3. **Otwórz wizualizacje** w przeglądarce
4. **Użyj w prezentacjach** - wszystkie wykresy są interaktywne

---

**Wszystkie wizualizacje wykorzystują HAMA Diamond i są gotowe do użycia! 💎**


