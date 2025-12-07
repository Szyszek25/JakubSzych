# 🏥 ZANT - ZUS Accident Notification Tool

**System wspierania zgłoszeń i decyzji ZUS w sprawie uznania zdarzeń za wypadki przy pracy**

## 📋 Opis

ZANT to inteligentny system wykorzystujący HAMA Diamond (Hybrid Adaptive Multi-Agent) do:
1. **Asystowania obywatelom** w zgłaszaniu wypadków przy pracy
2. **Wspierania pracowników ZUS** w podejmowaniu decyzji o uznaniu wypadku

## 🏗️ Architektura

```
ZANT/
├── backend/
│   ├── api/              # FastAPI endpoints
│   ├── core/             # HAMA Diamond integration
│   ├── models/           # Modele danych
│   ├── services/         # Logika biznesowa
│   └── utils/            # Narzędzia pomocnicze
├── frontend/             # React/HTML interface
├── data/                 # Przykładowe dane testowe
└── docs/                 # Dokumentacja
```

## 🚀 Szybki Start

### Wymagania
- Python 3.10+
- Google Gemini API Key (uzyskaj na https://aistudio.google.com/)
- Node.js 18+ (opcjonalnie dla frontendu)

### Instalacja

```bash
# 1. Uzyskaj Google Gemini API Key
# Przejdź do: https://aistudio.google.com/

# 2. Ustaw klucz API
export GOOGLE_API_KEY="twój_klucz"  # Linux/Mac
set GOOGLE_API_KEY=twój_klucz       # Windows CMD
$env:GOOGLE_API_KEY="twój_klucz"    # Windows PowerShell

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Uruchom backend
cd backend
python -m api.main

# 5. Otwórz frontend
# Otwórz frontend/index.html w przeglądarce
```

## 📊 Funkcjonalności

### 1. Asystent Zgłoszenia Wypadku
- Analiza tekstu zgłoszenia
- Wykrywanie brakujących elementów
- Sugestie uzupełnień
- Walidacja zgodności z wzorcem ZUS

### 2. Wsparcie Decyzji
- Analiza dokumentacji PDF
- Ekstrakcja danych z kart wypadków
- Rekomendacja: uznać/nie uznać
- Generowanie projektu karty wypadku

## 🔧 Technologie

- **Backend**: FastAPI, HAMA Diamond Core, Google Gemini
- **Frontend**: React/HTML5
- **OCR**: Tesseract/PaddleOCR
- **LLM**: Google Gemini 2.5 Flash

## 📝 Licencja

Projekt hackathonowy dla ZUS

