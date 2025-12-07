# 🌍 Scenariusze Jutra - System Analizy Foresightowej

System analizy foresightowej dla MSZ - generuje scenariusze rozwojowe w perspektywie 12 i 36 miesięcy.

## 🚀 Szybki Start

**Zalecane**: Użyj głównego pliku `start_scenariusze_jutra.py` w katalogu głównym projektu:

```bash
python start_scenariusze_jutra.py
```

Lub alternatywnie `start.py`:

```bash
python start.py
```

Oba skrypty uruchamiają backend API i frontend automatycznie.

## 📡 Endpointy API

- **Status**: http://localhost:8002/
- **Scenariusze**: http://localhost:8002/api/scenarios
- **Dokumentacja**: http://localhost:8002/docs
- **Przykłady requestów**: http://localhost:8002/api/docs/examples

## 🔧 Struktura Projektu

```
SCENARIUSZE_JUTRA/
├── api_scenarios.py          # Główny plik API (FastAPI)
├── scenario_generator.py     # Generator scenariuszy (HAMA Diamond)
├── local_llm_adapter.py      # Adapter dla lokalnych modeli LLM (Ollama)
├── analyze_scenarios.py       # Analiza scenariuszy
├── visualizer_hama.py        # Wizualizacje HAMA Diamond
├── requirements.txt          # Zależności Python
├── outputs/                  # Wygenerowane raporty i wykresy
│   ├── analiza_scenariuszy.csv
│   ├── raport_analiza_scenariuszy.md
│   └── wykresy/
└── README_INTERFEJS.md       # Dokumentacja interfejsu UI
```

## 🌐 Port API

System działa na porcie **8002**.

## 📚 Dokumentacja

- [Interfejs użytkownika](README_INTERFEJS.md)
- [Wizualizacje](README_VIZUALIZACJE.md)

## ⚙️ Instalacja

### Wymagania

- Python 3.9+
- Node.js 18+ (dla frontendu)

### Backend

```bash
cd SCENARIUSZE_JUTRA
python -m venv venv
venv\Scripts\activate  # Windows
# lub
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Frontend

```bash
cd dashboard-frontend
npm install
npm run dev
```

## 🔗 Integracja z HAMA Diamond

System wykorzystuje **HAMA Diamond** (Human-AI Meta-Analysis Diamond) jako silnik kognitywny do:
- Analizy danych geopolitycznych
- Generowania scenariuszy
- Wnioskowania i rekomendacji
