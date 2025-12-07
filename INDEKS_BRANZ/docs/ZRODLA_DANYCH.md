# 📥 Źródła Danych - GQPA-Indeks Branż

## Przegląd Źródeł

System wykorzystuje **4 główne źródła danych**:

1. **GUS** - Główny Urząd Statystyczny
2. **KRS** - Krajowy Rejestr Sądowy
3. **Google Trends** - Trendy wyszukiwań
4. **NBP** - Narodowy Bank Polski

---

## 1. GUS (stat.gov.pl)

### Dostępne dane:

- **Przychody branżowe** (roczne)
  - Format: CSV/Excel
  - Częstotliwość: roczna
  - Poziom: dział PKD (2-cyfrowy)

- **Eksport/Import** (roczne)
  - Format: CSV/Excel
  - Częstotliwość: roczna
  - Poziom: dział PKD

- **Zatrudnienie** (roczne)
  - Format: CSV/Excel
  - Częstotliwość: roczna
  - Poziom: dział PKD

- **Inwestycje (CAPEX)** (roczne)
  - Format: CSV/Excel
  - Częstotliwość: roczna
  - Poziom: dział PKD

### Jak pobrać:

1. Wejdź na https://stat.gov.pl
2. Przejdź do sekcji "Bank Danych Lokalnych"
3. Wybierz dane dla działów PKD
4. Pobierz pliki CSV/Excel

### Alternatywa:

- **API GUS** (jeśli dostępne)
- **Pliki udostępnione przez organizatorów hackathonu**

---

## 2. KRS (ekrs.ms.gov.pl)

### Dostępne dane:

- **Liczba nowych firm** (roczne)
  - Format: CSV/API
  - Częstotliwość: roczna
  - Poziom: dział PKD

- **Upadłości** (roczne)
  - Format: CSV/API
  - Częstotliwość: roczna
  - Poziom: dział PKD

- **Liczba podmiotów** (roczne)
  - Format: CSV/API
  - Częstotliwość: roczna
  - Poziom: dział PKD

### Jak pobrać:

1. Wejdź na https://ekrs.ms.gov.pl
2. Użyj wyszukiwarki zaawansowanej
3. Filtruj według PKD
4. Eksportuj wyniki

### Alternatywa:

- **API KRS** (jeśli dostępne)
- **Pliki udostępnione przez organizatorów hackathonu**

---

## 3. Google Trends (trends.google.com)

### Dostępne dane:

- **Trendy wyszukiwań** (12 miesięcy)
  - Format: API (pytrends)
  - Częstotliwość: tygodniowa/miesięczna
  - Skala: 0-100 (50 = średnie)

### Jak pobrać:

1. Zainstaluj bibliotekę `pytrends`:
   ```bash
   pip install pytrends
   ```

2. Użyj kodu w `data_collector.py`:
   ```python
   from pytrends.request import TrendReq
   pytrends = TrendReq(hl='pl-PL', tz=360)
   ```

### Uwagi:

- **Rate limits** - Google ogranicza liczbę zapytań
- **Opóźnienia** - dodaj `time.sleep(1)` między zapytaniami
- **Fallback** - jeśli API nie działa, użyj wartości symulowanych

---

## 4. NBP (nbp.pl)

### Dostępne dane:

- **Indeks nastrojów konsumenckich** (miesięczny)
  - Format: CSV/Excel
  - Częstotliwość: miesięczna
  - Skala: 0-200 (100 = neutralne)

### Jak pobrać:

1. Wejdź na https://www.nbp.pl
2. Przejdź do sekcji "Statystyka"
3. Znajdź "Indeks nastrojów konsumenckich"
4. Pobierz pliki CSV/Excel

### Alternatywa:

- **API NBP** (jeśli dostępne)
- **Wartości symulowane** (dla demo)

---

## Struktura Danych

### Format plików:

- **CSV** - UTF-8 z BOM (dla Excel)
- **Excel** - .xlsx (openpyxl)
- **JSON** - dla API

### Kolumny wymagane:

#### GUS:
- `pkd` - kod PKD
- `nazwa` - nazwa branży
- `przychody_2023`, `przychody_2022`, `przychody_2021`
- `eksport_2023`, `eksport_2022`
- `zatrudnienie_2023`, `zatrudnienie_2022`
- `inwestycje_2023`, `inwestycje_2022`

#### KRS:
- `pkd` - kod PKD
- `nazwa` - nazwa branży
- `nowe_firmy_2023`, `nowe_firmy_2022`
- `upadlosci_2023`, `upadlosci_2022`
- `liczba_podmiotow_2023`, `liczba_podmiotow_2022`

#### Google Trends:
- `pkd` - kod PKD
- `nazwa` - nazwa branży
- `trend_wyszukiwan` - średnia wartość (0-100)

#### NBP:
- `pkd` - kod PKD
- `nazwa` - nazwa branży
- `indeks_nastrojow` - wartość indeksu
- `oczekiwania` - oczekiwania konsumentów
- `sytuacja_biezaca` - bieżąca sytuacja

---

## Przetwarzanie Danych

### Krok 1: Pobranie

```python
collector = DataCollector()
data = collector.collect_all_data()
```

### Krok 2: Walidacja

- Sprawdź brakujące wartości
- Sprawdź zakresy wartości
- Sprawdź spójność danych

### Krok 3: Zapis

- Surowe dane → `data/raw/`
- Przetworzone dane → `data/processed/`

---

## Symulowane Dane (Demo)

W wersji demo system używa **symulowanych danych**:

- Losowe wartości w realistycznych zakresach
- Zachowane relacje między wskaźnikami
- Możliwość podmiany na prawdziwe dane

### Jak podmienić na prawdziwe dane:

1. Pobierz dane z GUS, KRS, NBP
2. Zapisz w formacie CSV zgodnym ze strukturą
3. Umieść w `data/raw/`
4. Zmodyfikuj `data_collector.py` aby czytał z plików

---

## Aktualizacja Danych

### Częstotliwość:

- **GUS**: roczna (dane za poprzedni rok)
- **KRS**: roczna (dane za poprzedni rok)
- **Google Trends**: tygodniowa/miesięczna
- **NBP**: miesięczna

### Automatyzacja:

W wersji produkcyjnej:
- Skrypt cron (Linux) / Task Scheduler (Windows)
- Pobieranie danych co miesiąc/kwartał
- Automatyczne odświeżanie indeksu

---

## Licencje i Ograniczenia

### GUS:
- **Licencja**: Open Data (CC BY)
- **Ograniczenia**: Brak

### KRS:
- **Licencja**: Publiczne dane
- **Ograniczenia**: Możliwe limity API

### Google Trends:
- **Licencja**: Terms of Service Google
- **Ograniczenia**: Rate limits, tylko dane agregowane

### NBP:
- **Licencja**: Publiczne dane
- **Ograniczenia**: Brak

---

**Wszystkie źródła danych są ogólnodostępne i zgodne z wymaganiami hackathonu.**

