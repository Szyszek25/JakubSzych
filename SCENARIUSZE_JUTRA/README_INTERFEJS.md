# 🎯 Scenariusze Jutra - Nowoczesny Interfejs UI

## ✅ Co zostało stworzone

### 1. **Frontend - React/TypeScript**
- `dashboard-frontend/src/components/ScenarioCardsStack.tsx` - Główny komponent z kartami scenariuszy
- `dashboard-frontend/src/components/ScenarioCardsStack.css` - Profesjonalny styling (dark mode, navy, gold accents)
- `dashboard-frontend/src/services/scenariosApi.ts` - API client dla scenariuszy

### 2. **Backend API - FastAPI**
- `SCENARIUSZE_JUTRA/api_scenarios.py` - Endpointy API dla interfejsu
- Port: **8002**

## 🚀 Jak uruchomić

### Krok 1: Backend API

```bash
cd SCENARIUSZE_JUTRA
.\URUCHOM_API.bat
```

Lub ręcznie:
```bash
cd SCENARIUSZE_JUTRA
venv\Scripts\python.exe api_scenarios.py
```

✅ API działa na: **http://localhost:8002**
📚 Dokumentacja: **http://localhost:8002/docs**

### Krok 2: Frontend

```bash
cd dashboard-frontend
npm install
npm run dev
```

✅ Frontend działa na: **http://localhost:5173**

## 🎨 Funkcjonalności UI

### 1. **Karty Scenariuszy (Swipeable Cards)**
- ✅ Swipe RIGHT → Akceptuj scenariusz
- ✅ Swipe LEFT → Odrzuć scenariusz
- ✅ Tap → Rozwiń szczegóły
- ✅ Animacje i przejścia

### 2. **Panel "What If"**
- ✅ 3 sliderki:
  - Energy Market Instability
  - Geopolitical Conflict Escalation
  - Foreign Investment Flow
- ✅ Dynamiczne przeliczanie scenariuszy

### 3. **Rekomendacje Strategiczne**
- ✅ Karty z rekomendacjami
- ✅ Kliknięcie → animacja wpływu na scenariusz

### 4. **Explainability**
- ✅ Wizualizacja kluczowych czynników z wagami
- ✅ Podsumowanie logiki (bez surowego chain-of-thought)
- ✅ Wykresy wag

## 📡 API Endpoints

- `GET /api/scenarios` - Pobierz wszystkie scenariusze
- `POST /api/scenarios/{id}/accept` - Akceptuj scenariusz
- `POST /api/scenarios/{id}/reject` - Odrzuć scenariusz
- `POST /api/scenarios/update-weights` - Zaktualizuj wagi (What if)
- `GET /api/scenarios/{id}` - Szczegóły scenariusza

## 🎯 Format danych

Scenariusz w formacie JSON:
```json
{
  "scenario_id": "S12_POS",
  "title": "Energy Stabilization",
  "horizon": "12M",
  "risk_level": "LOW",
  "confidence": 0.84,
  "drivers": ["Increase in OZE share", "Energy oversupply"],
  "recommendations": ["Accelerate renewable investments"],
  "explainability": {
    "key_factors": [
      {"factor": "OZE growth", "weight": 0.25}
    ],
    "logic_summary": "Lower energy prices reduce..."
  }
}
```

## 🎬 Demo dla Jury (60 sekund)

1. **Otwórz interfejs**: http://localhost:5173
2. **Swipe pierwszą kartę** → pokaż interakcję
3. **Przesuń slider "Conflict escalation"** → karta się zmienia
4. **Kliknij rekomendację** → animacja wpływu
5. **Rozwiń kartę** → pokaż explainability

## 💡 Odpowiedź na pytanie jury

> "Czy to tylko UI?"

**Odpowiedź:**
> "Nie. UI wizualizuje działanie silnika scenariuszowego HAMA Diamond – decyzje wpływają na wagi i zmieniają trajektorię przyszłych zdarzeń."

## 🎨 Design

- **Dark mode** - profesjonalny, rządowy
- **Kolory**: deep navy, charcoal, muted gold accents
- **Animacje**: subtelne (0.3-0.5s)
- **Typografia**: clean, serious, readable
- **Wygląd**: system wewnętrzny MSZ z 2030, nie demo

## 🔧 Integracja z HAMA Diamond

Interfejs automatycznie:
1. Ładuje scenariusze z `main_orchestrator.py`
2. Mapuje dane na format UI
3. Wysyła akcje (accept/reject) do backendu
4. Przelicza scenariusze przy zmianie sliderów

## 📝 Uwagi

- API działa na porcie **8002**
- Frontend domyślnie łączy się z `http://localhost:8002`
- Jeśli backend nie działa, frontend pokaże błąd połączenia

