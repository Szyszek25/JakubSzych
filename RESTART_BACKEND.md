# 🔄 Restart Backend API

## ⚠️ WAŻNE: Zrestartuj backend po zmianach!

Jeśli widzisz błąd 404 dla `/api/demo/init`:

1. **Zatrzymaj backend** (Ctrl+C w terminalu gdzie działa `api_dashboard.py`)
2. **Uruchom ponownie:**
   ```bash
   cd AIWSLUZBIE
   python api_dashboard.py
   ```

3. **Sprawdź czy endpoint działa:**
   - Otwórz: http://localhost:8000/docs
   - Znajdź endpoint: `POST /api/demo/init`
   - Kliknij "Try it out" → "Execute"

4. **W dashboardzie kliknij "Dane Demo"** - powinno działać!

## ✅ Po restarcie:

- ✅ Endpoint `/api/demo/init` będzie dostępny
- ✅ Przycisk "Dane Demo" w dashboardzie zadziała
- ✅ Dashboard wypełni się danymi

