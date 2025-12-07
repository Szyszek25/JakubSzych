# 🚀 HACKNATION - Zbiór Projektów Hackathonowych

**HACKNATION** to zbiór projektów hackathonowych wykorzystujących zaawansowane frameworki AI (HAMA Diamond, GQPA) do rozwiązywania problemów administracji publicznej i sektora finansowego.

---

## 📂 Projekty

1. **📊 INDEKS_BRANZ** - Analiza kondycji branż w Polsce (PKO BP)
2. **🌍 SCENARIUSZE_JUTRA** - System analizy foresightowej (MSZ)
3. **🏥 ZANT** - System wspierania zgłoszeń wypadków (ZUS)
4. **🏛️ SCIEZKA_PRAWA** - Navigator legislacyjny (BM MC)
5. **🤖 AIWSLUZBIE** - Asystent AI dla administracji (MSiT)

---

## 🚀 Szybki Start - Instalacja

### Wymagania Systemowe

- **Python 3.9+** (lub 3.10+ dla ZANT)
- **Node.js 18+** (dla frontendu)
- **Git** (do klonowania repozytorium)

### Instalacja - Krok po Kroku

#### 1. Sklonuj Repozytorium

```bash
git clone https://github.com/Szyszek25/HACKNATION.git
cd HACKNATION
```

#### 2. Wybierz Projekt i Zainstaluj

Każdy projekt ma własne skrypty instalacyjne. Wybierz projekt który Cię interesuje:

---

### 📊 INDEKS_BRANZ - Instalacja

**Windows:**
```bash
cd INDEKS_BRANZ
INSTALL.bat
```

**Linux/Mac:**
```bash
cd INDEKS_BRANZ
chmod +x INSTALL.sh
./INSTALL.sh
```

**Lub ręcznie:**
```bash
cd INDEKS_BRANZ
python -m venv venv
venv\Scripts\activate  # Windows
# lub
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**Uruchomienie:**
```bash
run.bat  # Windows
# lub
python main.py
```

---

### 🌍 SCENARIUSZE_JUTRA - Instalacja

**Windows:**
```bash
cd SCENARIUSZE_JUTRA
INSTALL.bat
```

**Linux/Mac:**
```bash
cd SCENARIUSZE_JUTRA
chmod +x INSTALL.sh
./INSTALL.sh
```

**Lub ręcznie:**
```bash
cd SCENARIUSZE_JUTRA
python -m venv venv
venv\Scripts\activate  # Windows
# lub
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**Uruchomienie:**
```bash
# Z głównego folderu HACKNATION:
python start_scenariusze_jutra.py

# Lub z folderu SCENARIUSZE_JUTRA:
python api_scenarios.py
```

**Frontend (opcjonalnie):**
```bash
cd dashboard-frontend
npm install
npm run dev
```

**Adresy:**
- Backend API: http://localhost:8002
- Frontend: http://localhost:5173
- Dokumentacja API: http://localhost:8002/docs

---

### 🏥 ZANT - Instalacja

**⚠️ Wymaga Google Gemini API Key**

**Windows:**
```bash
cd ZANT
INSTALL.bat
```

**Linux/Mac:**
```bash
cd ZANT
chmod +x INSTALL.sh
./INSTALL.sh
```

**Konfiguracja API Key:**
```bash
# Windows CMD
set GOOGLE_API_KEY=twój_klucz

# Windows PowerShell
$env:GOOGLE_API_KEY="twój_klucz"

# Linux/Mac
export GOOGLE_API_KEY=twój_klucz
```

**Lub utwórz plik `.env`:**
```
GOOGLE_API_KEY=twój_klucz
```

**Uzyskaj klucz:** https://aistudio.google.com/

**Lub ręcznie:**
```bash
cd ZANT
python -m venv venv
venv\Scripts\activate  # Windows
# lub
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**Uruchomienie:**
```bash
URUCHOM.bat  # Windows
# lub
cd backend
python -m api.main
```

**Frontend:** Otwórz `frontend/index.html` w przeglądarce

---

### 🏛️ SCIEZKA_PRAWA - Instalacja

**Windows:**
```bash
cd SCIEZKA_PRAWA
INSTALL.bat
```

**Linux/Mac:**
```bash
cd SCIEZKA_PRAWA
chmod +x INSTALL.sh
./INSTALL.sh
```

**Lub ręcznie:**
```bash
cd SCIEZKA_PRAWA
python -m venv venv
venv\Scripts\activate  # Windows
# lub
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**Uruchomienie:**
```bash
URUCHOM.bat  # Windows
# lub
python api.py
```

**API:** http://localhost:8003
**Dokumentacja:** http://localhost:8003/docs

---

### 🤖 AIWSLUZBIE - Instalacja

**Windows:**
```bash
cd AIWSLUZBIE
INSTALL.bat
```

**Linux/Mac:**
```bash
cd AIWSLUZBIE
chmod +x INSTALL.sh
./INSTALL.sh
```

**Lub ręcznie:**
```bash
cd AIWSLUZBIE
python -m venv venv
venv\Scripts\activate  # Windows
# lub
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**Uruchomienie:**
```bash
python run_simple.py
# lub
python api_dashboard.py
```

---

## 📚 Dokumentacja

### Dla Jury

- **📄 README_DLA_JURY.md** - Przewodnik nawigacji po folderach

### Dla Developerów

Każdy projekt ma własną dokumentację:

- `PROJEKT/README.md` - Opis projektu
- `PROJEKT/docs/ARCHITEKTURA.md` - Architektura systemu
- `PROJEKT/docs/METODOLOGIA.md` - Metodologia
- `PROJEKT/docs/ZRODLA_DANYCH.md` - Źródła danych
- `PROJEKT/prezentacja/prezentacja.md` - Prezentacja (10 slajdów)

---

## 🎯 Który Projekt Wybrać?

**Zależy od Twojego zainteresowania:**

- **Finanse i analiza ryzyka** → `INDEKS_BRANZ/`
- **Geopolityka i foresight** → `SCENARIUSZE_JUTRA/`
- **Obsługa obywateli** → `ZANT/`
- **Transparentność i legislacja** → `SCIEZKA_PRAWA/`
- **Wsparcie administracji** → `AIWSLUZBIE/`

---

## 🔧 Rozwiązywanie Problemów

### Port zajęty

Jeśli port jest zajęty, zatrzymaj proces używający tego portu:

**Windows:**
```bash
netstat -ano | findstr :8002
taskkill /F /PID <PID>
```

**Linux/Mac:**
```bash
lsof -ti:8002
kill -9 $(lsof -ti:8002)
```

### Brak venv

Każdy projekt ma skrypt `INSTALL.bat` (Windows) lub `INSTALL.sh` (Linux/Mac) który automatycznie tworzy venv.

### Błędy importów

Upewnij się że:
1. Venv jest aktywowane
2. Wszystkie zależności są zainstalowane: `pip install -r requirements.txt`
3. Jesteś w odpowiednim folderze projektu

### Node.js dla frontendu

**SCENARIUSZE_JUTRA** wymaga Node.js dla frontendu:

```bash
cd dashboard-frontend
npm install
npm run dev
```

---

## 📁 Struktura Projektu

```
HACKNATION/
│
├── 📊 INDEKS_BRANZ/          # Projekt 1: Analiza kondycji branż
│   ├── INSTALL.bat           # Skrypt instalacyjny (Windows)
│   ├── INSTALL.sh            # Skrypt instalacyjny (Linux/Mac)
│   ├── requirements.txt      # Zależności Python
│   ├── README.md             # Dokumentacja projektu
│   └── prezentacja/          # Prezentacja dla jury
│
├── 🌍 SCENARIUSZE_JUTRA/      # Projekt 2: Analiza foresightowa
│   ├── INSTALL.bat
│   ├── INSTALL.sh
│   ├── requirements.txt
│   └── ...
│
├── 🏥 ZANT/                   # Projekt 3: System wsparcia ZUS
│   ├── INSTALL.bat
│   ├── INSTALL.sh
│   ├── requirements.txt
│   └── ...
│
├── 🏛️ SCIEZKA_PRAWA/          # Projekt 4: Navigator legislacyjny
│   ├── INSTALL.bat
│   ├── INSTALL.sh
│   ├── requirements.txt
│   └── ...
│
├── 🤖 AIWSLUZBIE/             # Projekt 5: Asystent AI
│   ├── INSTALL.bat
│   ├── INSTALL.sh
│   ├── requirements.txt
│   └── ...
│
├── 🎨 dashboard-frontend/     # Wspólny frontend
│   ├── package.json
│   └── ...
│
├── ⚙️ hama_core/              # Core framework HAMA Diamond
│   ├── requirements.txt
│   └── ...
│
└── 📄 README.md               # Ten plik
```

---

## 🎬 Demo - Szybkie Uruchomienie

**Najprostszy sposób:**

```bash
# Scenariusze Jutra (z frontendem)
python start_scenariusze_jutra.py

# Indeks Branż
cd INDEKS_BRANZ
run.bat  # Windows
python main.py  # Linux/Mac

# ZANT
cd ZANT
URUCHOM.bat  # Windows

# Ścieżka Prawa
cd SCIEZKA_PRAWA
URUCHOM.bat  # Windows

# AI w Służbie
cd AIWSLUZBIE
python run_simple.py
```

---

## 📝 Licencja

Projekty wykorzystują:
- **HAMA Diamond** - Background IP (Copyright © 2024-2025)
- **GQPA** - Background IP
- **Foreground IP** - Własność autorów projektów

---

## 👥 Autorzy

Zespół HACKNATION - Hackathon 2025

---

## 📞 Kontakt

Wszystkie projekty są częścią hackathonu HACKNATION.

**Struktura:**
- Każdy projekt jest niezależny
- Można uruchomić każdy osobno
- Wspólny frontend w `dashboard-frontend/`
- Wspólny core w `hama_core/`

---

**Powodzenia! 🚀**
