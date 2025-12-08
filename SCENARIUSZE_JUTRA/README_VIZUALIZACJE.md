# 📊 HAMA Diamond Visualizer dla Scenariusze Jutra

## Opis

Moduł wizualizacji i analizy dla projektu **Scenariusze Jutra**, wykorzystujący **HAMA Diamond** do tworzenia zaawansowanych wykresów 2D i 3D.

## Funkcje

### 1. Analiza Scenariuszy (`analyze_scenarios.py`)

Analizuje raporty scenariuszy i generuje:
- **CSV** z analizą wszystkich scenariuszy
- **Raport Markdown** z podsumowaniem
- **Indeks HAMA Diamond** dla każdego scenariusza

### 2. Wizualizacje (`visualizer_hama.py`)

Tworzy **6 typów wykresów**:

1. **Prawdopodobieństwa scenariuszy** - bar chart
2. **Mapa ryzyka i szans** - scatter plot 2D
3. **Wykres 3D Timeline** - czas vs prawdopodobieństwo vs wpływ
4. **Heatmap prawdopodobieństw** - macierz typ/horyzont
5. **HAMA Diamond Radar** - profil scenariuszy
6. **Porównanie horyzontów** - 12m vs 36m

## Użycie

```bash
cd SCENARIUSZE_JUTRA
python analyze_scenarios.py
```

## Wyniki

Wszystkie pliki są zapisywane w:
- `outputs/analiza_scenariuszy.csv` - dane
- `outputs/raport_analiza_scenariuszy.md` - raport
- `outputs/wykresy/*.html` - wizualizacje

## Wymagania

- pandas
- numpy
- plotly

## Integracja z HAMA Diamond

System wykorzystuje metodologię **HAMA Diamond** do:
- Obliczania indeksu dla scenariuszy
- Dynamicznego ważenia prawdopodobieństw
- Klasyfikacji scenariuszy (pozytywne/negatywne)
- Generowania rekomendacji strategicznych


