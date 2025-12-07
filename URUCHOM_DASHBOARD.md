# 🚀 Jak uruchomić Dashboard

## ⚠️ WAŻNE: Uruchom z właściwego folderu!

## Krok 1: Backend API (Terminal 1)

```bash
cd AIWSLUZBIE
python api_dashboard.py
```

✅ Backend działa na: http://localhost:8000

## Krok 2: Frontend Dashboard (Terminal 2)

**MUSISZ BYĆ W FOLDERZE `dashboard-frontend`!**

```bash
cd dashboard-frontend
npm install
npm run dev
```

✅ Frontend działa na: http://localhost:3000

## 🔍 Rozwiązywanie problemów

### Błąd: "Could not read package.json"
**Przyczyna:** Jesteś w złym folderze (np. `AIWSLUZBIE` zamiast `dashboard-frontend`)

**Rozwiązanie:**
```bash
cd c:\Users\jakub\Desktop\HACKNATION\dashboard-frontend
npm install
npm run dev
```

### Sprawdź czy jesteś w właściwym folderze:
```bash
# Windows PowerShell
pwd
# Powinno pokazać: C:\Users\jakub\Desktop\HACKNATION\dashboard-frontend

# Sprawdź czy package.json istnieje
ls package.json
```

### Jeśli nie masz node_modules:
```bash
cd dashboard-frontend
npm install
```

## 📝 Szybkie komendy

### Windows (PowerShell):
```powershell
# Terminal 1 - Backend
cd AIWSLUZBIE
python api_dashboard.py

# Terminal 2 - Frontend
cd dashboard-frontend
npm install  # tylko pierwszy raz
npm run dev
```

### Windows (CMD):
```cmd
REM Terminal 1 - Backend
cd AIWSLUZBIE
python api_dashboard.py

REM Terminal 2 - Frontend
cd dashboard-frontend
npm install
npm run dev
```

## ✅ Sprawdzenie czy działa

1. Backend: http://localhost:8000 - powinien pokazać `{"status":"ok"}`
2. Frontend: http://localhost:3000 - powinien pokazać dashboard
3. API Docs: http://localhost:8000/docs - dokumentacja API

## 🎯 Struktura folderów

```
HACKNATION/
├── AIWSLUZBIE/              ← Backend (Python)
│   ├── api_dashboard.py
│   └── asystent_ai_gqpa_integrated.py
│
└── dashboard-frontend/      ← Frontend (React) ⭐ TUTAJ URUCHAMIAJ npm
    ├── package.json         ← Ten plik musi istnieć!
    ├── src/
    └── ...
```

