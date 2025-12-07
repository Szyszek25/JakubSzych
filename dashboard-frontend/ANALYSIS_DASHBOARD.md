# Analysis Dashboard - Instrukcja dla Jury

## 🎯 Cel Dashboardu

Futurystyczny dashboard analityczny prezentujący system analizy foresightowej w stylu "2030-level" - wygląda jak prawdziwy system operacyjny do analiz państwowych, działający w czasie rzeczywistym.

## 🚀 Uruchomienie

```bash
cd dashboard-frontend
npm install
npm run dev
```

Dashboard automatycznie otworzy się w trybie **Analysis Dashboard** (futurystyczny).

## 🎥 Demo Flow dla Jury (90 sekund)

### 0-10s: Hero Section
- **Co pokazać**: Animowany graf zależności w tle
- **Co powiedzieć**: "To jest system analityczny dla instytucji publicznych. Widzimy mechanikę decyzyjną w akcji."

### 10-30s: Data Ingestion
- **Co pokazać**: Strumienie danych wpływające do systemu
- **Co powiedzieć**: "System analizuje dane z wielu źródeł: media międzynarodowe, raporty instytucjonalne, dane ekonomiczne. Wszystko w czasie rzeczywistym."

### 30-50s: Analysis Progress
- **Co pokazać**: Pasek postępu i etapy analizy
- **Co powiedzieć**: "System przechodzi przez etapy: identyfikacja czynników, budowa łańcuchów przyczynowo-skutkowych, symulacja przyszłości, generowanie scenariuszy."

### 50-70s: Scenarios Generation
- **Co pokazać**: Scenariusze wyłaniające się z animacją
- **Co powiedzieć**: "Oto wygenerowane scenariusze - pozytywne i negatywne, dla horyzontów 12 i 36 miesięcy. Każdy ma poziom pewności i wpływ na różne sektory."

### 70-90s: System Status
- **Co pokazać**: Panel boczny z terminalem
- **Co powiedzieć**: "System pokazuje status w czasie rzeczywistym. To nie jest prezentacja - to działający system analityczny."

## 🎨 Kluczowe Elementy Wizualne

### Kolorystyka
- **Tło**: Ciemny grafit/granat (#0a0e27)
- **Akcenty**: Bursztyn (#ffc107)
- Typografia: Jasna, kontrastowa

### Animacje
1. **Data Ingestion**: Pulsujące strumienie danych
2. **Graph**: Węzły i połączenia rysowane sekwencyjnie
3. **Progress**: Płynny pasek postępu
4. **Scenarios**: Karty wyłaniające się z efektem slide-in

## 🔄 Przełączanie Między Trybami

W prawym górnym rogu jest przycisk do przełączania między:
- **Analysis Dashboard** (futurystyczny) - domyślny
- **Standard Dashboard** (oryginalny)

## 📊 Integracja z Backendem

Dashboard jest gotowy do integracji z API. Obecnie używa symulowanych danych, ale można łatwo podłączyć:

```typescript
// W AnalysisDashboard.tsx
const response = await fetch('/api/scenarios')
const data = await response.json()
setScenarios(data.scenarios)
```

## 🎯 Język i Narracja

**Używamy:**
- ✅ "System analizuje"
- ✅ "System modeluje"
- ✅ "System rekomenduje"

**NIE używamy:**
- ❌ "chatbot"
- ❌ "porozmawiaj z AI"
- ❌ "zapytaj model"

## 🏛️ Styl Instytucjonalny

Dashboard wygląda jak:
- System analityczny think-tanku
- Centrum dowodzenia strategicznego
- Dashboard decyzyjny ministerstwa

**Zero:**
- Neonów
- Startupowego kiczu
- Marketingowego języka

## 🧩 Customization

Możesz łatwo dostosować:
- Kolory w `AnalysisDashboard.css`
- Animacje (timing, efekty)
- Layout (grid, flexbox)
- Dane (scenariusze, statusy)

## 📝 Notatki dla Prezentacji

1. **Nie mów "AI"** - mów "system analityczny"
2. **Podkreśl proces** - nie tylko wyniki
3. **Pokazuj animacje** - to dowód "myślenia" systemu
4. **Używaj języka formalnego** - instytucjonalnego
5. **Podkreśl wyjaśnialność** - mechanika decyzyjna jest widoczna

## 🎬 Efekt Końcowy

Jury powinno pomyśleć:
> "To wygląda jak system, który mógłby działać w ministerstwie w 2030 roku."

A nie:
> "Ładna stronka."

