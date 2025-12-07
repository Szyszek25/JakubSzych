# 🔑 Konfiguracja Google Gemini API

## Szybki Start

### 1. Uzyskaj API Key

1. Przejdź do: **https://aistudio.google.com/**
2. Zaloguj się kontem Google
3. Kliknij **"Get API Key"** lub przejdź do ustawień
4. Utwórz nowy API Key
5. Skopiuj klucz (zaczyna się od `AIza...`)

### 2. Ustaw Klucz API

#### Opcja A: Zmienna środowiskowa (Zalecane)

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

**Aby ustawić na stałe (Windows):**
```powershell
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'twój_klucz', 'User')
```

**Aby ustawić na stałe (Linux/Mac):**
Dodaj do `~/.bashrc` lub `~/.zshrc`:
```bash
export GOOGLE_API_KEY="twój_klucz_api"
```

#### Opcja B: Plik .env

Utwórz plik `.env` w katalogu `ZANT/`:
```
GOOGLE_API_KEY=twój_klucz_api_tutaj
```

### 3. Weryfikacja

```bash
# Sprawdź czy klucz jest ustawiony
python -c "import os; print('✅ OK' if os.getenv('GOOGLE_API_KEY') else '❌ BRAK')"
```

## Rozwiązywanie Problemów

### Błąd: "Gemini API nie dostępne"

**Przyczyna:** Klucz API nie jest ustawiony lub jest nieprawidłowy.

**Rozwiązanie:**
1. Sprawdź czy klucz jest ustawiony:
   ```bash
   echo $GOOGLE_API_KEY  # Linux/Mac
   echo %GOOGLE_API_KEY%  # Windows CMD
   ```

2. Upewnij się, że klucz jest poprawny (zaczyna się od `AIza...`)

3. Sprawdź czy masz dostęp do Gemini API:
   - Przejdź do https://aistudio.google.com/
   - Sprawdź czy API jest włączone

### Błąd: "google-genai nie dostępne"

**Rozwiązanie:**
```bash
pip install --upgrade google-genai
```

### Błąd: "API quota exceeded"

**Przyczyna:** Przekroczono limit zapytań API.

**Rozwiązanie:**
- Sprawdź limity na https://aistudio.google.com/
- Poczekaj na reset limitu
- Rozważ użycie innego klucza API

## Model Gemini

Domyślnie używany jest model: **`models/gemini-3-pro-preview`**

To najnowszy model Google Gemini, specjalnie zaprojektowany do zaawansowanych zadań reasoningowych.

Możesz zmienić model ustawiając zmienną środowiskową:
```bash
export GEMINI_MODEL_NAME="models/gemini-3-pro-preview"
```

Dostępne modele:
- `models/gemini-3-pro-preview` (domyślny, zaawansowany reasoning)
- `gemini-2.5-flash` (szybszy, mniej zaawansowany)
- `gemini-1.5-pro` (stabilny, sprawdzony)

## Bezpieczeństwo

⚠️ **WAŻNE:** Nigdy nie commituj klucza API do repozytorium!

- Używaj zmiennych środowiskowych
- Dodaj `.env` do `.gitignore`
- Nie udostępniaj klucza publicznie

## Testowanie

Po skonfigurowaniu, przetestuj:

```python
from backend.services.accident_assistant import AccidentAssistant

assistant = AccidentAssistant()
if assistant.llm and assistant.llm.is_available():
    print("✅ Gemini działa!")
else:
    print("❌ Gemini nie działa - sprawdź konfigurację")
```

