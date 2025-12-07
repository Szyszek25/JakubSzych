# 🏛️ ASYSTENT AI DLA ADMINISTRACJI - FINALNY PRODUKT

## ✅ Kompletne rozwiązanie dla HackNation 2025

### 📦 Co zawiera projekt:

1. **Backend API** (FastAPI) - `AIWSLUZBIE/api_dashboard.py`
2. **Frontend Dashboard** (React + TypeScript) - `dashboard-frontend/`
3. **Główny system asystenta** - `AIWSLUZBIE/asystent_ai_gqpa_integrated.py`
4. **Integracja GQPA** - `system/gqpa_core/`

## 🚀 Szybki start

### Krok 1: Backend API

```bash
cd AIWSLUZBIE
pip install fastapi uvicorn pydantic
python api_dashboard.py
```

✅ Backend działa na: **http://localhost:8000**
📚 API Docs: **http://localhost:8000/docs**

### Krok 2: Frontend Dashboard

```bash
cd dashboard-frontend
npm install
npm run dev
```

✅ Dashboard dostępny na: **http://localhost:3000**

## 🎯 Funkcjonalności

### Dashboard zawiera:

1. **Statystyki w czasie rzeczywistym**
   - Łącznie spraw
   - Średni czas analizy
   - Zakończone analizy
   - Krytyczne terminy
   - Średni czas decyzji

2. **Wizualizacje danych**
   - Wykresy słupkowe (status, typ spraw)
   - Wykres kołowy (rozkład ryzyka)
   - Responsywne wykresy (Recharts)

3. **Lista spraw administracyjnych**
   - Pełna lista wszystkich spraw
   - Szczegóły każdej sprawy
   - Status, ryzyko, terminy

4. **Status systemu**
   - GQPA Core (Background IP)
   - Ollama (lokalny model open-source)
   - Guardrails (bezpieczeństwo)

5. **Terminy i priorytety**
   - Krytyczne terminy (czerwone)
   - Nadchodzące terminy
   - Liczba dni do terminu

6. **Truth Guardian (COI)**
   - System immunologiczny kognitywny
   - Wykrywanie dezinformacji
   - Statystyki weryfikacji

## 📊 Jak użyć danych demo

1. Otwórz dashboard: http://localhost:3000
2. Kliknij przycisk **"Dane Demo"** (zielony przycisk w headerze)
3. Dashboard automatycznie wypełni się przykładowymi danymi:
   - 5 spraw administracyjnych
   - Różne typy spraw (kwalifikacja, kategoria hotelu, zakaz działalności)
   - Różne statusy (nowa, w trakcie, oczekuje decyzji, zakończona)
   - Terminy (w tym 1 krytyczny)

## 🔧 Technologie

### Backend:
- **Python 3.9+**
- **FastAPI** - nowoczesny framework API
- **GQPA DIAMOND** - architektura kognitywna (Background IP)
- **Ollama** - lokalny model open-source (llama3.2)

### Frontend:
- **React 18** - framework UI
- **TypeScript** - type safety
- **Vite** - build tool
- **Recharts** - wykresy
- **Lucide React** - ikony

## 🔒 Bezpieczeństwo

- **Guardrails** - walidacja wejścia/wyjścia
- **RODO compliance** - sprawdzanie danych osobowych
- **Audit log** - logowanie wszystkich operacji
- **Sanityzacja danych** - ochrona przed XSS

## 📁 Struktura projektu

```
HACKNATION/
├── AIWSLUZBIE/
│   ├── api_dashboard.py              # Backend API
│   ├── asystent_ai_gqpa_integrated.py # Główny system
│   └── requirements_dashboard.txt     # Zależności backend
│
├── dashboard-frontend/               # Frontend React
│   ├── src/
│   │   ├── components/               # Komponenty UI
│   │   ├── services/                 # API client
│   │   └── types.ts                  # TypeScript types
│   └── package.json
│
└── system/
    └── gqpa_core/                    # GQPA DIAMOND (Background IP)
```

## 🎨 Design

- Profesjonalny wygląd dla administracji państwowej
- Responsywny (desktop, tablet, mobile)
- Auto-refresh co 30 sekund
- Nowoczesne animacje i przejścia

## 📝 API Endpoints

- `GET /api/dashboard/stats` - statystyki dashboardu
- `GET /api/cases` - lista spraw
- `POST /api/cases` - utworzenie sprawy
- `POST /api/cases/{id}/analyze` - analiza sprawy
- `POST /api/cases/{id}/generate-decision` - generowanie decyzji
- `POST /api/demo/init` - inicjalizacja danych demo
- `GET /api/system/status` - status systemu
- `GET /api/deadlines` - terminy

## ✅ Wymagania hackathonu - spełnione

- ✅ Repozytorium kodu
- ✅ Opis mechanizmów zabezpieczających (guardrails)
- ✅ Opis technologii i architektury
- ✅ Model językowy (Ollama - open-source)
- ✅ Plan integracji z systemami
- ✅ Funkcje wspierające tworzenie dokumentów
- ✅ Bezpieczeństwo i RODO
- ✅ Dashboard interaktywny
- ✅ Zgodność z regulacjami

## 🏆 Gotowe do prezentacji!

Projekt jest kompletny i gotowy do prezentacji na hackathonie HackNation 2025.

**Autorzy:** Zespół HackNation 2025
**Data:** 2025
**Wersja:** 1.0.0 - Production Ready

