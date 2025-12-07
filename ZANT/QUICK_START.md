# 🚀 Quick Start - ZANT

## Najszybszy sposób uruchomienia (5 minut)

### 1. Uzyskaj Google Gemini API Key

1. Przejdź do: https://aistudio.google.com/
2. Zaloguj się kontem Google
3. Utwórz nowy API Key
4. Skopiuj klucz

### 2. Ustaw zmienną środowiskową

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="twój_klucz_api"
```

**Windows (CMD):**
```cmd
set GOOGLE_API_KEY=twój_klucz_api
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="twój_klucz_api"
```

**LUB** utwórz plik `.env` w katalogu ZANT:
```
GOOGLE_API_KEY=twój_klucz_api
```

### 3. Zainstaluj zależności

```bash
cd ZANT
pip install -r requirements.txt
```

### 3. Uruchom backend

```bash
cd backend
python -m api.main
```

Backend będzie dostępny na: **http://localhost:8000**

### 4. Otwórz frontend

Otwórz plik `frontend/index.html` w przeglądarce.

LUB użyj prostego serwera:
```bash
cd frontend
python -m http.server 3000
# Otwórz: http://localhost:3000
```

## Testowanie

### Test 1: Asystent Zgłoszenia

1. Otwórz frontend
2. Przejdź do zakładki "Asystent Zgłoszenia"
3. Wypełnij kilka pól (np. tylko "Okoliczności wypadku")
4. Kliknij "Analizuj Zgłoszenie"
5. Zobaczysz brakujące pola i sugestie

### Test 2: Wsparcie Decyzji

1. Przejdź do zakładki "Wsparcie Decyzji"
2. Przeciągnij plik PDF z dokumentacją wypadku
3. Poczekaj na analizę (10-30 sekund)
4. Zobaczysz rekomendację decyzji

## API Endpoints

- `GET /` - Health check
- `POST /api/report/analyze` - Analiza zgłoszenia
- `POST /api/report/submit` - Zapisanie zgłoszenia
- `POST /api/decision/analyze` - Analiza dokumentacji PDF
- `GET /api/report/{report_id}` - Pobranie zgłoszenia
- `GET /api/card/{card_id}` - Pobranie karty wypadku

Dokumentacja API: **http://localhost:8000/docs**

## Rozwiązywanie Problemów

### Backend nie startuje
```bash
# Sprawdź czy port 8000 jest wolny
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac
```

### Gemini API nie działa
```bash
# Sprawdź czy klucz API jest ustawiony
echo $GOOGLE_API_KEY  # Linux/Mac
echo %GOOGLE_API_KEY%  # Windows CMD
$env:GOOGLE_API_KEY   # Windows PowerShell

# Jeśli nie, ustaw:
export GOOGLE_API_KEY="twój_klucz"  # Linux/Mac
set GOOGLE_API_KEY=twój_klucz       # Windows CMD
$env:GOOGLE_API_KEY="twój_klucz"    # Windows PowerShell
```

### Błąd importu modułów
```bash
# Upewnij się, że jesteś w katalogu ZANT
cd ZANT

# Zainstaluj zależności ponownie
pip install -r requirements.txt
```

## Następne Kroki

- Przeczytaj [README.md](README.md) - pełna dokumentacja
- Zobacz [ARCHITEKTURA.md](ARCHITEKTURA.md) - szczegóły techniczne
- Sprawdź [PLAN_24H.md](PLAN_24H.md) - plan pracy na hackathon

