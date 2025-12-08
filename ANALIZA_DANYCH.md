# 📊 Analiza Danych w Projektach - Prawdziwe vs Symulowane

## Podsumowanie

Po analizie kodu i wykresów, oto status danych w projektach:

---

## 🔴 INDEKS_BRANZ - **WSZYSTKIE DANE SYMULOWANE**

### Status: ⚠️ **SYMULOWANE**

**Wszystkie dane wejściowe są generowane losowo:**

1. **GUS (Główny Urząd Statystyczny)** - ❌ SYMULOWANE
   - Lokalizacja: `data_collector.py` linie 88-109
   - Kod: `np.random.uniform(50, 500) * 1e9` dla przychodów
   - Komentarz: `# Symulowane dane GUS`
   - **W produkcji**: Powinno być API GUS lub pliki CSV

2. **KRS (Krajowy Rejestr Sądowy)** - ❌ SYMULOWANE
   - Lokalizacja: `data_collector.py` linie 121-131
   - Kod: `np.random.randint(500, 5000)` dla nowych firm
   - Komentarz: `# Symulacja danych KRS`
   - **W produkcji**: Powinno być API KRS lub pliki CSV

3. **Google Trends** - ⚠️ CZĘŚCIOWO PRAWDZIWE (z fallback)
   - Lokalizacja: `data_collector.py` linie 136-183
   - Próbuje pobrać prawdziwe dane przez `pytrends`
   - **Fallback**: Jeśli nie działa → `np.random.uniform(20, 80)`
   - W praktyce często używa fallback (rate limiting, błędy)

4. **NBP (Nastroje Konsumenckie)** - ❌ SYMULOWANE
   - Lokalizacja: `data_collector.py` linie 191-210
   - Kod: `np.random.uniform(80, 120)` dla indeksu nastrojów
   - Komentarz: `# Symulowane dane NPK`

5. **Wskaźniki (Rentowność, Zadłużenie)** - ❌ CZĘŚCIOWO SYMULOWANE
   - Lokalizacja: `indicators.py` linie 124, 142
   - Rentowność: Symulowana na podstawie przychodów
   - Zadłużenie: `np.random.uniform(0.3, 2.5)`
   - Komentarz: `# Symulacja`

### Wykresy w INDEKS_BRANZ:

✅ **Prawdziwe**: 
- Struktura danych (nazwy branż, PKD)
- Metodologia obliczeń (formuły, wagi)
- Klasyfikacja branż

❌ **Symulowane**:
- Wszystkie wartości liczbowe (przychody, eksport, zatrudnienie, itp.)
- Wszystkie wskaźniki (rentowność, zadłużenie, dynamika)
- Indeks GQPA Diamond (bazuje na symulowanych danych)

---

## 🟡 SCENARIUSZE_JUTRA - **MIESZANKA**

### Status: ⚠️ **CZĘŚCIOWO PRAWDZIWE**

**Scenariusze są prawdziwe (z LLM), ale niektóre wartości są symulowane:**

1. **Scenariusze (wydarzenia, prawdopodobieństwa)** - ✅ PRAWDZIWE
   - Generowane przez LLM (Ollama/OpenAI/Gemini)
   - Przykład z raportu Atlantis: konkretne wydarzenia jak "Katastrofa naturalna w Azji Wschodniej"
   - Prawdopodobieństwa: 0.8, 0.7, 0.6, 0.4 - z LLM

2. **Wartości "impact" w wizualizacjach** - ❌ SYMULOWANE
   - Lokalizacja: `visualizer_hama.py` linie 208-209, 266
   - Kod: `impact = np.random.uniform(0.3, 1.0)` dla pozytywnych
   - Kod: `impact = np.random.uniform(-1.0, -0.3)` dla negatywnych
   - Komentarz: `# Symuluj wpływ (w produkcji: wyciągnij z raportu)`
   - **Problem**: Impact powinien być wyciągnięty z raportu LLM, nie losowany!

3. **Wartości "impact" w analizie** - ❌ SYMULOWANE
   - Lokalizacja: `analyze_scenarios.py` linia 50
   - Kod: `impact = np.random.uniform(...)`
   - **Problem**: Powinno być z raportu, nie losowane

### Wykresy w SCENARIUSZE_JUTRA:

✅ **Prawdziwe**:
- Nazwy scenariuszy
- Prawdopodobieństwa wydarzeń
- Horyzonty czasowe (12M, 36M)
- Typy scenariuszy (pozytywny/negatywny)

❌ **Symulowane**:
- Wartości "impact" (wpływ) w wykresach
- Wartości w mapie ryzyka/szans
- Wartości w wykresie 3D

---

## 🔧 Co Należy Naprawić

### INDEKS_BRANZ:

1. **Podpiąć prawdziwe dane GUS**:
   ```python
   # Zamiast:
   'przychody_2023': np.random.uniform(50, 500) * 1e9
   
   # Powinno być:
   df_gus = pd.read_csv('data/raw/gus_przychody_2023.csv')
   ```

2. **Podpiąć prawdziwe dane KRS**:
   ```python
   # Zamiast:
   'nowe_firmy_2023': np.random.randint(500, 5000)
   
   # Powinno być:
   df_krs = pd.read_csv('data/raw/krs_nowe_firmy_2023.csv')
   ```

3. **Poprawić Google Trends** (już próbuje, ale ma fallback)

4. **Podpiąć prawdziwe dane NBP**:
   ```python
   # Zamiast:
   'indeks_nastrojow': np.random.uniform(80, 120)
   
   # Powinno być:
   response = requests.get('https://api.nbp.pl/...')
   ```

### SCENARIUSZE_JUTRA:

1. **Wyciągnąć "impact" z raportu LLM**:
   ```python
   # Zamiast:
   impact = np.random.uniform(0.3, 1.0)
   
   # Powinno być:
   impact = event.get('impacts', {}).get('economy', 0.5)  # Z raportu
   ```

2. **Parsować raport i wyciągać wartości impact**:
   - Raport zawiera `'impacts': {'gospodarka': '...', 'economy': '...'}`
   - Należy wyciągnąć wartości numeryczne z tych opisów
   - Lub poprosić LLM o zwrócenie wartości numerycznych

---

## 📝 Rekomendacje

### Dla Demo/Prezentacji:

✅ **OK** - Symulowane dane są akceptowalne dla:
- Prezentacji koncepcji
- Demo systemu
- Testów funkcjonalności

❌ **NIE OK** - Dla:
- Prawdziwej analizy
- Decyzji biznesowych
- Produkcji

### Dla Produkcji:

1. **INDEKS_BRANZ**: Wymaga podpięcia prawdziwych danych z GUS, KRS, NBP
2. **SCENARIUSZE_JUTRA**: Wymaga wyciągnięcia wartości impact z raportów LLM

---

## ✅ Podsumowanie

| Projekt | Scenariusze/Wydarzenia | Wartości Liczbowe | Wykresy |
|---------|----------------------|-------------------|---------|
| **INDEKS_BRANZ** | ✅ Prawdziwe (struktura) | ❌ Symulowane | ❌ Na symulowanych danych |
| **SCENARIUSZE_JUTRA** | ✅ Prawdziwe (z LLM) | ⚠️ Częściowo symulowane | ⚠️ Częściowo na prawdziwych danych |

**Wniosek**: Wykresy są **częściowo na prawdziwych danych** (struktura, scenariusze), ale **wartości liczbowe są często symulowane**.


