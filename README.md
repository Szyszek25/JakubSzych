# 🌍 Scenariusze Jutra - System Analizy Foresightowej

System analizy foresightowej dla MSZ - generuje scenariusze rozwojowe w perspektywie 12 i 36 miesięcy.

## 🚀 Szybki Start

### 1. Instalacja (jednorazowo)

#### Backend (Python)
```bash
cd scenariusze_jutra
python -m venv venv
venv\Scripts\activate  # Windows
# lub
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

#### Frontend (Node.js)
```bash
cd dashboard-frontend
npm install
```

### 2. Uruchomienie

**Najprostszy sposób - jeden plik:**

```bash
python start_scenariusze_jutra.py
```

Lub na Windows:
```bash
start.bat
```

To uruchomi:
- ✅ Backend API na porcie **8002**
- ✅ Frontend na porcie **5173** (lub następnym dostępnym)

## 📡 Adresy

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8002
- **Dokumentacja API**: http://localhost:8002/docs
- **Przykłady requestów**: http://localhost:8002/api/docs/examples

## 🛑 Zatrzymanie

Naciśnij `Ctrl+C` w terminalu - wszystkie serwisy zostaną zatrzymane automatycznie.

## 📋 Wymagania

- Python 3.9+
- Node.js 18+
- Ollama (dla lokalnego LLM) - opcjonalne

## 🔧 Rozwiązywanie problemów

### Port zajęty
Jeśli port 8002 lub 5173 jest zajęty, zatrzymaj inne aplikacje używające tych portów.

### Brak venv
```bash
cd scenariusze_jutra
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Brak node_modules
```bash
cd dashboard-frontend
npm install
```


## 📚 Dokumentacja

- [Architektura systemu](scenariusze_jutra/ARCHITECTURE.md)
- [API Documentation](http://localhost:8002/docs) (po uruchomieniu)
- [Przykłady requestów](http://localhost:8002/api/docs/examples) (po uruchomieniu)

