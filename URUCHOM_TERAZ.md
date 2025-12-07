# 🚀 URUCHOM TERAZ - KROK PO KROKU

## ✅ Proces został zatrzymany - port 8000 jest wolny!

## Krok 1: Uruchom Backend (Terminal 1)

```bash
cd AIWSLUZBIE
python api_dashboard.py
```

**Poczekaj aż zobaczysz:**
```
✅ GQPA Core załadowany
🚀 Uruchamianie API Dashboard...
📡 API dostępne na: http://localhost:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Krok 2: Sprawdź czy backend działa

Otwórz w przeglądarce: **http://localhost:8000**

Powinieneś zobaczyć: `{"status":"ok","service":"Asystent AI Dashboard API"}`

## Krok 3: Dashboard (już działa)

Dashboard powinien automatycznie połączyć się z backendem.

## Krok 4: Dodaj dane demo

1. Kliknij przycisk **"Dane Demo"** (zielony przycisk w headerze)
2. Poczekaj na komunikat: "✅ Dodano 5 spraw demo!"
3. Dashboard automatycznie się odświeży i pokaże:
   - 5 spraw w statystykach
   - Wykresy z danymi
   - Listę spraw
   - Terminy

## 🔧 Jeśli nadal nie działa:

1. **Sprawdź konsolę przeglądarki (F12)** - czy są błędy?
2. **Sprawdź terminal backendu** - czy są błędy?
3. **Odśwież dashboard** (F5) - może cache?

## ✅ Co zostało naprawione:

- ✅ Port 8000 zwolniony (stary proces zatrzymany)
- ✅ CasesList odświeża się automatycznie co 5 sekund
- ✅ Lepsze komunikaty błędów
- ✅ Auto-refresh po dodaniu danych demo

