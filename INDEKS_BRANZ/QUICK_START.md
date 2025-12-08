# 🚀 Quick Start - GQPA-Indeks Branż

## Szybkie uruchomienie (5 minut)

### Windows

1. **Otwórz terminal** w folderze `INDEKS_BRANZ`

2. **Uruchom skrypt**:
   ```bash
   run.bat
   ```

3. **Gotowe!** Wyniki w folderze `outputs/`

---

### Linux/Mac

1. **Otwórz terminal** w folderze `INDEKS_BRANZ`

2. **Utwórz venv**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Zainstaluj wymagania**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Uruchom analizę**:
   ```bash
   python main.py --full
   ```

5. **Gotowe!** Wyniki w folderze `outputs/`

---

## Co otrzymasz?

Po uruchomieniu otrzymasz:

1. **`indeks_branz.csv`** - finalny indeks z wszystkimi wskaźnikami
2. **`indeks_branz.xlsx`** - wersja Excel
3. **`wykresy/`** - interaktywne wykresy HTML
4. **`raporty/`** - raporty tekstowe (Markdown)

---

## Opcje uruchomienia

### Pełna analiza (domyślna)
```bash
python main.py --full
```

### Tylko scoring (z istniejących danych)
```bash
python main.py --scoring-only
```

### Tylko wizualizacje
```bash
python main.py --visualize-only
```

### Bez wizualizacji
```bash
python main.py --full --no-viz
```

### Bez raportów
```bash
python main.py --full --no-reports
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError"

**Rozwiązanie**: Zainstaluj wymagania:
```bash
pip install -r requirements.txt
```

### Problem: "GQPA Core nie znaleziony"

**Rozwiązanie**: To jest OK - system użyje uproszczonego silnika. 
GQPA Core jest opcjonalny (znajduje się w `../gqpa_core/`).

### Problem: "Google Trends nie działa"

**Rozwiązanie**: To jest OK - system użyje wartości symulowanych.
Google Trends wymaga biblioteki `pytrends` i może mieć rate limits.

### Problem: "Brak danych"

**Rozwiązanie**: System używa symulowanych danych w wersji demo.
W produkcji podmień `data_collector.py` aby czytał z prawdziwych źródeł.

---

## Następne kroki

1. **Przejrzyj wyniki** w `outputs/indeks_branz.csv`
2. **Otwórz wizualizacje** w `outputs/wykresy/`
3. **Przeczytaj raporty** w `outputs/raporty/`
4. **Dostosuj konfigurację** w `config.py`
5. **Dodaj prawdziwe dane** (zobacz `docs/ZRODLA_DANYCH.md`)

---

**Gotowe! System działa! 🎉**


