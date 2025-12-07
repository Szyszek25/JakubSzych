# 🏛️ Ścieżka Prawa (GQPA Legislative Navigator)

**System Sztucznej Inteligencji do Analizy i Prognozowania Procesów Legislacyjnych**

## 📋 Opis Projektu

Ścieżka Prawa to kompleksowe rozwiązanie wykorzystujące architekturę GQPA (General Quantum Process Architecture) do monitorowania, analizy i prognozowania procesów legislacyjnych w administracji publicznej.

### 🎯 Główne Funkcje

1. **Legislative Tracker** - Śledzenie zmian prawnych od prekonsultacji do wejścia w życie
2. **Plain Language Engine** - Automatyczne upraszczanie języka urzędowego
3. **Impact Simulator** - Analiza skutków regulacji (finansowe, społeczne, operacyjne)
4. **Democratic Interface** - Interfejs dla obywateli do śledzenia konsultacji społecznych
5. **Transparency Hub** - Centrum transparentności dla administracji

## 🏗️ Architektura

System opiera się na 5 modułach GQPA:

```
┌─────────────────────────────────────────────────────────┐
│           Ścieżka Prawa (GQPA Legislative Navigator)    │
├─────────────────────────────────────────────────────────┤
│  Legislative Tracker  │  Plain Language Engine          │
│  Impact Simulator     │  Democratic Interface           │
│  Transparency Hub                                        │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Instalacja

### Wymagania

- Python 3.9+
- Ollama (opcjonalnie, dla lokalnych modeli LLM)
- Node.js 18+ (dla frontendu)

### Instalacja Backend

```bash
cd SCIEZKA_PRAWA
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

## 🎬 Uruchomienie

### Windows PowerShell

```powershell
cd SCIEZKA_PRAWA
.\URUCHOM.ps1
```

### Windows CMD

```cmd
cd SCIEZKA_PRAWA
.\URUCHOM.bat
```

### Linux/Mac

```bash
cd SCIEZKA_PRAWA
./URUCHOM.sh
```

### Bezpośrednio przez Python

```bash
cd SCIEZKA_PRAWA
python api.py
```

API będzie dostępne pod adresem: `http://localhost:8003`
Dokumentacja API: `http://localhost:8003/docs`

## 📚 Dokumentacja

Szczegółowa dokumentacja znajduje się w folderze `docs/`:

- `ARCHITECTURE.md` - Architektura systemu
- `API_DOCUMENTATION.md` - Dokumentacja API
- `MODULES.md` - Opis modułów

## 🎥 Prezentacja

Prezentacja projektu (10 slajdów) znajduje się w pliku `PREZENTACJA.pdf`

## 📞 Kontakt

Projekt przygotowany dla:
- **Wydział Dialogu Społecznego BM MC**
- **Podsekcja GRAI ds. demokracji cyfrowej**

## 📄 Licencja

Open Source - zgodnie z wymaganiami wyzwania
