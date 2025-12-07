# 🚀 Quick Start - Scenariusze Jutra

## ⚡ Szybka instalacja z venv (ZALECANE)

### Windows
```cmd
cd SCENARIUSZE_JUTRA
setup_venv.bat
```

Po utworzeniu venv, aktywuj go:
```cmd
venv\Scripts\activate.bat
```

### Linux/Mac
```bash
cd SCENARIUSZE_JUTRA
chmod +x setup_venv.sh
./setup_venv.sh
```

Po utworzeniu venv, aktywuj go:
```bash
source venv/bin/activate
```

## Instalacja bez venv (niezalecane)

### Windows (PowerShell)
```powershell
cd SCENARIUSZE_JUTRA
python -m pip install -r requirements.txt
```

### Linux/Mac
```bash
cd SCENARIUSZE_JUTRA
python3 -m pip install -r requirements.txt
```

## Konfiguracja

1. Utwórz plik `.env` w katalogu `SCENARIUSZE_JUTRA`:
```env
OPENAI_API_KEY=twoj_klucz_tutaj
```

2. (Opcjonalnie) Jeśli nie masz klucza OpenAI, system będzie używał uproszczonej wersji.

## Uruchomienie

### 1. Aktywuj wirtualne środowisko (jeśli używasz venv)

**Windows:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2. Uruchom demo

**Demo Flow (bez zbierania danych z internetu):**
```bash
python run_demo.py
```

### Pełna analiza (ze zbieraniem danych)
```python
from main_orchestrator import ScenarioOrchestrator, create_situation_factors_from_weights
from config import OPENAI_API_KEY

config = {...}  # Zobacz main_orchestrator.py
orchestrator = ScenarioOrchestrator(config, OPENAI_API_KEY)
situation_factors = create_situation_factors_from_weights()
results = orchestrator.run_full_analysis(situation_factors, collect_data=True)
```

## Ważne uwagi

- **`data_collector.py`** to moduł, nie skrypt do bezpośredniego uruchomienia
- Użyj **`run_demo.py`** lub **`main_orchestrator.py`** do uruchomienia systemu
- System wymaga Python 3.9+

## Rozwiązywanie problemów

### ModuleNotFoundError
Jeśli widzisz błąd `ModuleNotFoundError`, zainstaluj zależności:
```bash
python -m pip install -r requirements.txt
```

### Brak klucza OpenAI
System będzie działał w trybie uproszczonym bez klucza API, ale scenariusze będą mniej szczegółowe.

