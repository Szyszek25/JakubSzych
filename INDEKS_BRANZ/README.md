# 🏦 GQPA-Indeks Branż - System Analizy Kondycji Branż w Polsce

## 📋 Opis Projektu

**GQPA-Indeks Branż** to zaawansowany system analityczny wykorzystujący **GQPA (General Quantitative Policy Analysis)** do oceny kondycji i perspektyw rozwoju branż w Polsce. System został opracowany na potrzeby hackathonu PKO BP.

### 🎯 Cel

Stworzenie syntetycznego indeksu branżowego, który pozwala:
- **Identyfikować** branże w dobrej kondycji vs. narażone na ryzyko
- **Przewidywać** perspektywy rozwoju na 12-36 miesięcy
- **Klasyfikować** branże według poziomu ryzyka i potencjału wzrostu
- **Generować** automatyczne raporty dla analityków kredytowych

### 🧠 Architektura GQPA

System wykorzystuje **GQPA** jako silnik analityczny do:
- Agregacji danych z wielu źródeł
- Budowy syntetycznych wskaźników
- Dynamicznego ważenia wskaźników
- Klasyfikacji i rankingowania branż
- Generowania naturalnych raportów tekstowych

## 📁 Struktura Projektu

```
INDEKS_BRANZ/
├── README.md                    # Ten plik
├── requirements.txt             # Zależności Python
├── config.py                    # Konfiguracja systemu
├── main.py                      # Główny plik uruchomieniowy
├── data_collector.py            # Pobieranie danych (GUS, KRS, etc.)
├── indicators.py                # Definicje wskaźników branżowych
├── gqpa_scoring.py              # Silnik scoringu GQPA
├── classifier.py                # Klasyfikacja branż
├── visualizer.py                # Wizualizacje (Plotly)
├── report_generator.py          # Generowanie raportów
├── data/                        # Dane źródłowe
│   ├── raw/                     # Surowe dane
│   └── processed/               # Przetworzone dane
├── outputs/                     # Wyniki
│   ├── indeks_branz.csv         # Finalny indeks
│   ├── raporty/                 # Raporty tekstowe
│   └── wykresy/                 # Wizualizacje
├── prezentacja/                 # Materiały prezentacyjne
│   ├── prezentacja.pdf          # 10 slajdów
│   └── scenariusz_filmu.md      # Scenariusz 3-min filmu
└── docs/                        # Dokumentacja
    ├── METODOLOGIA.md           # Metodologia scoringu
    ├── ZRODLA_DANYCH.md         # Źródła danych
    └── ARCHITEKTURA.md          # Architektura systemu
```

## 🚀 Szybki Start

### 1. Instalacja

```bash
# Utwórz środowisko wirtualne
python -m venv venv

# Aktywuj (Windows)
venv\Scripts\activate

# Aktywuj (Linux/Mac)
source venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt
```

### 2. Konfiguracja

Edytuj `config.py` i ustaw:
- Ścieżki do danych
- Parametry wskaźników
- Wagi GQPA

### 3. Uruchomienie

```bash
# Pełna analiza (pobieranie danych + scoring + raporty)
python main.py --full

# Tylko scoring (z istniejących danych)
python main.py --scoring-only

# Tylko wizualizacje
python main.py --visualize-only
```

## 📊 Metodologia

### 6-Etapowa Metodologia Scoringu GQPA

1. **Zbieranie danych** - agregacja z wielu źródeł
2. **Normalizacja** - standaryzacja wskaźników (0-1)
3. **Ważenie dynamiczne** - GQPA przypisuje wagi na podstawie znaczenia
4. **Agregacja** - syntetyczny indeks branżowy
5. **Klasyfikacja** - 5 kategorii branż
6. **Interpretacja** - generowanie raportów tekstowych

### Wskaźniki Branżowe

System analizuje **8-10 wskaźników**:

1. **Dynamika przychodów** (YoY %)
2. **Rentowność** (marża zysku)
3. **Zadłużenie** (D/E ratio)
4. **Szkodowość** (% upadłości)
5. **Dynamika eksportu** (GUS)
6. **Inwestycje** (CAPEX dynamika)
7. **Nastroje konsumenckie** (NPK)
8. **Trendy wyszukiwań** (Google Trends)
9. **Liczba nowych firm** (KRS)
10. **Produktywność** (przychód/etat)

## 🎯 Klasyfikacja Branż

System klasyfikuje branże do **5 kategorii**:

1. **🚀 Wzrostowe** - wysokie tempo rozwoju, niskie ryzyko
2. **✅ Stabilne** - umiarkowany wzrost, stabilne fundamenty
3. **⚠️ Ryzykowne** - wysokie zadłużenie lub spowolnienie
4. **📉 Kurczące się** - negatywna dynamika, wysokie ryzyko
5. **💰 Wymagające finansowania** - potencjał wzrostu, potrzeba kapitału

## 📈 Wyniki

### Plik CSV

`outputs/indeks_branz.csv` zawiera:
- Kod PKD/NACE
- Nazwa branży
- Indeks GQPA (0-100)
- Kategoria
- Wszystkie wskaźniki składowe
- Perspektywy 12-36 miesięcy

### Raporty

W `outputs/raporty/` znajdziesz:
- Raporty dla każdej branży
- Analizę trendów
- Rekomendacje dla działów ryzyka

### Wizualizacje

W `outputs/wykresy/`:
- Ranking branż (interaktywny)
- Mapa ryzyka (2D scatter)
- Trendy czasowe
- Porównania sektorowe

## 🔧 Wymagania Techniczne

- Python 3.9+
- GQPA Core (z `gqpa_core/`)
- Pandas, NumPy, Plotly
- Opcjonalnie: API klucze (Google Trends, GUS)

## 📝 Licencja

Projekt wykorzystuje **GQPA** jako bibliotekę zewnętrzną (Background IP).
GQPA jest utworem współautorskim i nie podlega przeniesieniu praw.

## 👥 Autorzy

Zespół HACKNATION - Hackathon PKO BP 2025

## 📞 Kontakt

- Discord: `indeks-branż`
- Stoisko: PKO BP Hackathon


