# 📊 Metodologia GQPA-Indeks Branż

## 6-Etapowa Metodologia Scoringu

### ETAP 1: Zbieranie Danych

System pobiera dane z następujących źródeł:

- **GUS (stat.gov.pl)**
  - Przychody branżowe
  - Eksport/import
  - Zatrudnienie
  - Inwestycje

- **KRS (ekrs.ms.gov.pl)**
  - Liczba nowych firm
  - Upadłości
  - Liczba podmiotów

- **Google Trends**
  - Trendy wyszukiwań dla nazw branż

- **NBP**
  - Indeks nastrojów konsumenckich

**Uwaga**: W wersji produkcyjnej dane mogą być pobierane przez API lub pliki CSV.

---

### ETAP 2: Normalizacja Wskaźników

Wszystkie wskaźniki są normalizowane do skali **0-1** przy użyciu jednej z metod:

#### Metoda 1: Min-Max
```
x_norm = (x - min) / (max - min)
```

#### Metoda 2: Z-Score (z normalizacją sigmoid)
```
z = (x - mean) / std
x_norm = 1 / (1 + exp(-z))
```

#### Metoda 3: Robust (używa mediany i IQR)
```
x_norm = (x - median) / IQR
# Następnie clip do [-3, 3] i normalizacja do [0, 1]
```

**Wskaźniki odwrócone** (gdzie niższe = lepsze):
- Zadłużenie: `x_norm = 1 - x_norm`
- Szkodowość: `x_norm = 1 - x_norm`

---

### ETAP 3: Dynamiczne Ważenie

GQPA przypisuje wagi wskaźnikom na podstawie:

1. **Wagi początkowe** (zdefiniowane w `config.py`)
2. **Analiza korelacji** - jeśli wskaźniki są silnie skorelowane (>0.8), ich wagi są zmniejszane
3. **Znaczenie dla oceny** - wskaźniki kluczowe (np. dynamika przychodów) mają wyższe wagi

**Normalizacja wag**: Suma wag = 1.0

**Przykładowe wagi**:
- Dynamika przychodów: 20%
- Rentowność: 15%
- Zadłużenie: 15%
- Szkodowość: 15%
- Dynamika eksportu: 10%
- Inwestycje: 10%
- Nastroje konsumenckie: 5%
- Trendy wyszukiwań: 5%
- Nowe firmy: 3%
- Produktywność: 2%

---

### ETAP 4: Agregacja do Indeksu

Znormalizowane wskaźniki są agregowane do jednego indeksu przy użyciu:

#### Metoda 1: Weighted Sum (domyślna)
```
indeks = Σ (w_i * x_i_norm)
```

#### Metoda 2: Geometric Mean (ważona)
```
indeks = exp(Σ (w_i * log(x_i_norm)))
```

#### Metoda 3: Harmonic Mean (ważona)
```
indeks = Σ(w_i) / Σ(w_i / x_i_norm)
```

**Skalowanie**: Indeks jest następnie skalowany do **0-100**.

---

### ETAP 5: Klasyfikacja

Branże są klasyfikowane do **5 kategorii** na podstawie:

1. **Indeks GQPA** (główny czynnik)
2. **Dodatkowe kryteria**:
   - Wysokie zadłużenie (>1.2) → "Wymagające finansowania"
   - Wysokie inwestycje (>15%) → "Wymagające finansowania"

**Progi kategorii**:
- **Wzrostowe**: indeks 70-100
- **Stabilne**: indeks 50-70
- **Ryzykowne**: indeks 30-50
- **Kurczące się**: indeks 0-30
- **Wymagające finansowania**: indeks 40-70 + (wysokie zadłużenie LUB wysokie inwestycje)

---

### ETAP 6: Interpretacja

System generuje **raporty tekstowe** zawierające:

1. **Analizę wskaźników** - wartości dla każdej branży
2. **Interpretację wyników** - co oznacza indeks i kategoria
3. **Rekomendacje** - konkretne działania dla działów ryzyka

Raporty są generowane w **naturalnym języku polskim** z użyciem szablonów i logiki warunkowej.

---

## Uzasadnienie Metodologii

### Dlaczego GQPA?

1. **Determinizm** - wagi są uzasadnione, nie losowe
2. **Interpretowalność** - każdy wynik można wyjaśnić
3. **Elastyczność** - łatwe dodawanie nowych wskaźników
4. **Automatyzacja** - system może działać cyklicznie

### Dlaczego nie Machine Learning?

- **Transparentność** - bank potrzebuje uzasadnienia decyzji
- **Regulacje** - wymagają interpretowalności modeli
- **Kontrola** - analitycy muszą rozumieć logikę
- **Walidacja** - łatwiejsza weryfikacja wyników

### Dlaczego 10 wskaźników?

- **Wielowymiarowość** - kompleksowa ocena
- **Równowaga** - nie za mało (niedostateczna analiza), nie za dużo (szum)
- **Dostępność danych** - wszystkie wskaźniki są dostępne w open data

---

## Walidacja Metodologii

### Testy przeprowadzone:

1. **Spójność** - te same dane dają te same wyniki
2. **Czułość** - zmiana wskaźników zmienia indeks
3. **Stabilność** - małe zmiany danych nie powodują dużych zmian indeksu
4. **Interpretowalność** - wyniki są zrozumiałe dla analityków

### Benchmarki:

- Porównanie z rankingami branżowymi z innych źródeł
- Weryfikacja kategorii przez ekspertów branżowych
- Backtesting na danych historycznych

---

## Perspektywy Rozwoju

### Możliwe rozszerzenia:

1. **Więcej źródeł danych**
   - Dane giełdowe
   - Raporty branżowe
   - Media społecznościowe

2. **Predykcje**
   - Prognozy na 12-36 miesięcy
   - Scenariusze rozwojowe
   - Analiza trendów

3. **Benchmarki**
   - Porównanie z innymi krajami
   - Benchmarki sektorowe
   - Analiza konkurencyjności

4. **Automatyzacja**
   - Cykliczne odświeżanie
   - Powiadomienia o zmianach
   - Integracja z systemami bankowymi

---

**Dokumentacja metodologii jest kluczowa dla wdrożenia systemu w PKO BP.**

