# 📦 Instalacja ZANT

## Wymagania Systemowe

- **Python 3.10+**
- **Google Gemini API Key** (uzyskaj na https://aistudio.google.com/)
- **Node.js 18+** (opcjonalnie - tylko jeśli chcesz React frontend)
- **Tesseract OCR** (opcjonalnie - dla OCR)

## Krok 1: Uzyskanie Google Gemini API Key

1. Przejdź do: https://aistudio.google.com/
2. Zaloguj się kontem Google
3. Kliknij "Get API Key" lub przejdź do ustawień
4. Utwórz nowy API Key
5. Skopiuj klucz (zaczyna się od `AIza...`)

## Krok 2: Konfiguracja API Key

### Opcja A: Zmienna środowiskowa

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

### Opcja B: Plik .env

Utwórz plik `.env` w katalogu `ZANT/`:
```
GOOGLE_API_KEY=twój_klucz_api
```

## Krok 3: Instalacja Zależności Python

```bash
cd ZANT
pip install -r requirements.txt
```

## Krok 3: Instalacja Tesseract (Opcjonalnie)

### Windows
1. Pobierz z: https://github.com/UB-Mannheim/tesseract/wiki
2. Zainstaluj
3. Dodaj do PATH lub ustaw w `backend/config.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Linux
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-pol
```

### Mac
```bash
brew install tesseract tesseract-lang
```

## Krok 4: Uruchomienie

### Szybkie uruchomienie (Windows)
```bash
URUCHOM.bat
```

### Ręczne uruchomienie

1. **Backend:**
```bash
cd backend
python -m api.main
```

2. **Frontend:**
   - Otwórz `frontend/index.html` w przeglądarce
   - LUB użyj prostego serwera:
   ```bash
   cd frontend
   python -m http.server 3000
   ```

## Weryfikacja

1. Sprawdź czy backend działa: http://localhost:8000
2. Sprawdź dokumentację API: http://localhost:8000/docs
3. Otwórz frontend i przetestuj funkcjonalności

## Rozwiązywanie Problemów

### Gemini API nie działa
```bash
# Sprawdź czy klucz API jest ustawiony
python -c "import os; print('OK' if os.getenv('GOOGLE_API_KEY') else 'BRAK')"

# Jeśli brak, ustaw:
export GOOGLE_API_KEY="twój_klucz"  # Linux/Mac
set GOOGLE_API_KEY=twój_klucz       # Windows CMD
$env:GOOGLE_API_KEY="twój_klucz"    # Windows PowerShell
```

### Błąd importu google-genai
```bash
pip install --upgrade google-genai
```

### Błąd importu modułów
```bash
# Upewnij się, że jesteś w katalogu ZANT
cd ZANT

# Zainstaluj zależności ponownie
pip install -r requirements.txt
```

### OCR nie działa
- Sprawdź czy Tesseract jest zainstalowany
- Sprawdź ścieżkę w konfiguracji
- System będzie działał bez OCR (tylko tekstowe PDF)

### Port 8000 zajęty
Zmień port w `backend/config.py`:
```python
API_CONFIG = {
    "port": 8001,  # Zmień na inny port
    ...
}
```

