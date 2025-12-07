# 📁 HACKNATION - Przewodnik dla Jury

## 🎯 O Projekcie

**HACKNATION** to zbiór projektów hackathonowych wykorzystujących zaawansowane frameworki AI (HAMA Diamond, GQPA) do rozwiązywania problemów administracji publicznej i sektora finansowego.

---

## 📂 Struktura Folderów - Jak Nawigować

### 🗺️ Mapa Projektów

```
HACKNATION/
│
├── 📊 INDEKS_BRANZ/          # Projekt 1: Analiza kondycji branż (PKO BP)
├── 🌍 SCENARIUSZE_JUTRA/      # Projekt 2: Analiza foresightowa (MSZ)
├── 🏥 ZANT/                   # Projekt 3: System wsparcia ZUS
├── 🏛️ SCIEZKA_PRAWA/          # Projekt 4: Navigator legislacyjny
├── 🤖 AIWSLUZBIE/             # Projekt 5: Asystent AI dla administracji
│
├── 🎨 dashboard-frontend/     # Frontend dla wszystkich projektów
├── ⚙️ hama_core/              # Core framework HAMA Diamond
└── 📄 README.md              # Główny README projektu
```

---

## 📋 Szczegółowy Opis Projektów

### 1. 📊 INDEKS_BRANZ - Analiza Kondycji Branż

**Cel:** System analizy kondycji branż w Polsce dla PKO BP

**Gdzie znaleźć:**
- 📁 Folder: `INDEKS_BRANZ/`
- 📄 Prezentacja: `INDEKS_BRANZ/prezentacja/prezentacja.md`
- 📊 Wyniki: `INDEKS_BRANZ/outputs/`
- 📖 Dokumentacja: `INDEKS_BRANZ/README.md`

**Co zawiera:**
- Syntetyczny indeks branżowy (0-100)
- Klasyfikacja branż (5 kategorii)
- Raporty analityczne
- Wizualizacje interaktywne

**Szybki start:**
```bash
cd INDEKS_BRANZ
python main.py
```

---

### 2. 🌍 SCENARIUSZE_JUTRA - Analiza Foresightowa

**Cel:** System generowania scenariuszy rozwojowych dla MSZ (12-36 miesięcy)

**Gdzie znaleźć:**
- 📁 Folder: `SCENARIUSZE_JUTRA/`
- 📄 Prezentacja: `SCENARIUSZE_JUTRA/prezentacja/prezentacja.md`
- 📊 Wyniki: `SCENARIUSZE_JUTRA/outputs/`
- 📖 Dokumentacja: `SCENARIUSZE_JUTRA/README.md`

**Co zawiera:**
- Generator scenariuszy (HAMA Diamond)
- Analiza prawdopodobieństw
- Wizualizacje 3D i heatmapy
- API REST (port 8002)

**Szybki start:**
```bash
python start_scenariusze_jutra.py
# Lub
cd SCENARIUSZE_JUTRA
python api_scenarios.py
```

---

### 3. 🏥 ZANT - ZUS Accident Notification Tool

**Cel:** System wspierania zgłoszeń i decyzji ZUS w sprawie wypadków przy pracy

**Gdzie znaleźć:**
- 📁 Folder: `ZANT/`
- 📄 Prezentacja: `ZANT/prezentacja/prezentacja.md`
- 📖 Dokumentacja: `ZANT/README.md`
- 🧪 Testy: `ZANT/TESTY_DLA_JURY.md`

**Co zawiera:**
- Asystent dla obywateli (zgłoszenia wypadków)
- System wsparcia decyzji dla pracowników ZUS
- Analiza dokumentacji PDF
- Integracja z Google Gemini

**Szybki start:**
```bash
cd ZANT
URUCHOM.bat  # Windows
# Lub
python backend/api/main.py
```

---

### 4. 🏛️ SCIEZKA_PRAWA - Legislative Navigator

**Cel:** System monitorowania i analizy procesów legislacyjnych

**Gdzie znaleźć:**
- 📁 Folder: `SCIEZKA_PRAWA/`
- 📄 Prezentacja: `SCIEZKA_PRAWA/prezentacja/prezentacja.md`
- 📖 Dokumentacja: `SCIEZKA_PRAWA/README.md`

**Co zawiera:**
- Legislative Tracker (śledzenie zmian)
- Plain Language Engine (upraszczanie języka)
- Impact Simulator (analiza skutków)
- Democratic Interface (dla obywateli)

**Szybki start:**
```bash
cd SCIEZKA_PRAWA
URUCHOM.bat  # Windows
# Lub
python api.py
```

---

### 5. 🤖 AIWSLUZBIE - Asystent AI dla Administracji

**Cel:** Wspieranie orzeczników w Departamencie Turystyki MSiT

**Gdzie znaleźć:**
- 📁 Folder: `AIWSLUZBIE/`
- 📄 Prezentacja: `AIWSLUZBIE/prezentacja/prezentacja.md`
- 📖 Dokumentacja: `AIWSLUZBIE/docs/`

**Co zawiera:**
- Automatyczna analiza dokumentów
- Truth Guardian (weryfikacja wiarygodności)
- Dashboard z wizualizacjami
- Integracja z LLM (Gemini/Ollama)

**Szybki start:**
```bash
cd AIWSLUZBIE
python run_simple.py
# Lub
python api_dashboard.py
```

---

## 🎨 Dashboard Frontend

**Wspólny frontend dla wszystkich projektów**

**Gdzie znaleźć:**
- 📁 Folder: `dashboard-frontend/`
- 📖 Dokumentacja: `dashboard-frontend/README.md`

**Co zawiera:**
- React + TypeScript
- Komponenty wizualizacji
- Integracja z backendami
- Panel analityczny

**Szybki start:**
```bash
cd dashboard-frontend
npm install
npm run dev
```

---

## 🔍 Gdzie Znaleźć Prezentacje?

**Wszystkie prezentacje znajdują się w folderach `prezentacja/` każdego projektu:**

1. **INDEKS_BRANZ** → `INDEKS_BRANZ/prezentacja/prezentacja.md`
2. **SCENARIUSZE_JUTRA** → `SCENARIUSZE_JUTRA/prezentacja/prezentacja.md`
3. **ZANT** → `ZANT/prezentacja/prezentacja.md`
4. **SCIEZKA_PRAWA** → `SCIEZKA_PRAWA/prezentacja/prezentacja.md`
5. **AIWSLUZBIE** → `AIWSLUZBIE/prezentacja/prezentacja.md`

**Każda prezentacja zawiera:**
- 10 slajdów w formacie Markdown
- Scenariusz 3-minutowego filmu
- Opis problemu i rozwiązania

---

## 📚 Dokumentacja Techniczna

**Każdy projekt ma folder `docs/` z dokumentacją:**

- `ARCHITEKTURA.md` - Architektura systemu
- `METODOLOGIA.md` - Metodologia analizy
- `ZRODLA_DANYCH.md` - Źródła danych

**Przykład:**
```
INDEKS_BRANZ/docs/
├── ARCHITEKTURA.md
├── METODOLOGIA.md
└── ZRODLA_DANYCH.md
```

---

## 🚀 Szybka Nawigacja - Najważniejsze Pliki

### Dla Jury - Co Przeczytać Najpierw?

1. **Ten plik** (`README_DLA_JURY.md`) - przegląd projektu
2. **Prezentacje** w folderach `prezentacja/prezentacja.md` każdego projektu
3. **README.md** w każdym folderze projektu - szczegóły techniczne

### Dla Developerów

1. `README.md` (główny) - instalacja i uruchomienie
2. `requirements.txt` w każdym projekcie - zależności
3. `docs/ARCHITEKTURA.md` - architektura systemu

---

## 🎯 Który Projekt Wybrać?

**Zależy od Twojego zainteresowania:**

- **Finanse i analiza ryzyka** → `INDEKS_BRANZ/`
- **Geopolityka i foresight** → `SCENARIUSZE_JUTRA/`
- **Obsługa obywateli** → `ZANT/`
- **Transparentność i legislacja** → `SCIEZKA_PRAWA/`
- **Wsparcie administracji** → `AIWSLUZBIE/`

---

## 🔧 Wymagania Techniczne

**Wspólne dla wszystkich projektów:**
- Python 3.9+
- Node.js 18+ (dla frontendu)
- Git

**Opcjonalne:**
- Ollama (dla lokalnych modeli LLM)
- Google Gemini API Key (dla niektórych projektów)

---

## 📞 Kontakt i Wsparcie

**Wszystkie projekty są częścią hackathonu HACKNATION**

**Struktura:**
- Każdy projekt jest niezależny
- Można uruchomić każdy osobno
- Wspólny frontend w `dashboard-frontend/`
- Wspólny core w `hama_core/`

---

## 🎬 Demo - Jak Uruchomić?

**Najprostszy sposób - jeden plik:**

```bash
# Z głównego folderu HACKNATION
python start.py
```

**Lub dla konkretnego projektu:**

```bash
# Scenariusze Jutra
python start_scenariusze_jutra.py

# Indeks Branż
cd INDEKS_BRANZ
python main.py

# ZANT
cd ZANT
URUCHOM.bat

# Ścieżka Prawa
cd SCIEZKA_PRAWA
URUCHOM.bat

# AI w Służbie
cd AIWSLUZBIE
python run_simple.py
```

---

## 📝 Notatki dla Jury

**Co warto sprawdzić:**

1. ✅ **Prezentacje** - każdy projekt ma 10-slajdową prezentację
2. ✅ **Wyniki** - foldery `outputs/` z raportami i wizualizacjami
3. ✅ **Kod** - główne pliki `.py` w każdym projekcie
4. ✅ **Dokumentacja** - foldery `docs/` z architekturą
5. ✅ **Testy** - niektóre projekty mają `TESTY_DLA_JURY.md`

**Struktura każdego projektu:**
```
PROJEKT/
├── prezentacja/          ← PREZENTACJA DLA JURY
├── docs/                 ← DOKUMENTACJA TECHNICZNA
├── outputs/              ← WYNIKI I WIZUALIZACJE
├── README.md             ← OPIS PROJEKTU
└── *.py                  ← KOD ŹRÓDŁOWY
```

---

**Powodzenia w ocenie! 🚀**

