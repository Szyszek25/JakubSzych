"""
Konfiguracja systemu ZANT
"""
import os
from typing import Dict, List
from dotenv import load_dotenv

# Upewnij się, że temp_uploads istnieje
TEMP_UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp_uploads")
os.makedirs(TEMP_UPLOADS_DIR, exist_ok=True)

load_dotenv()

# Konfiguracja LLM - Google Gemini (HAMA Model)
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "models/gemini-3-pro-preview")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
TEMPERATURE_ANALYSIS = 0.3  # Dla analizy - niska temperatura = bardziej deterministyczne
TEMPERATURE_SUGGESTIONS = 0.5  # Dla sugestii - wyższa temperatura = bardziej kreatywne

# Fallback do Ollama (opcjonalnie)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Konfiguracja ZUS - Wzorzec zgłoszenia wypadku
ZUS_ACCIDENT_REPORT_TEMPLATE = {
    "required_fields": [
        "data_wypadku",
        "godzina_wypadku",
        "miejsce_wypadku",
        "okolicznosci_wypadku",
        "przyczyna_wypadku",
        "dane_poszkodowanego",
        "rodzaj_dzialalnosci",
        "opis_urazu"
    ],
    "field_descriptions": {
        "data_wypadku": "Data zdarzenia (format: YYYY-MM-DD)",
        "godzina_wypadku": "Godzina zdarzenia (format: HH:MM)",
        "miejsce_wypadku": "Szczegółowy adres lub lokalizacja wypadku",
        "okolicznosci_wypadku": "Szczegółowy opis tego, co się wydarzyło",
        "przyczyna_wypadku": "Przyczyna bezpośrednia wypadku",
        "dane_poszkodowanego": "Imię, nazwisko, PESEL lub NIP",
        "rodzaj_dzialalnosci": "Rodzaj prowadzonej działalności gospodarczej",
        "opis_urazu": "Opis doznanych obrażeń"
    }
}

# Definicja wypadku przy pracy (zgodnie z przepisami)
ACCIDENT_DEFINITION = {
    "definition": "Nagłe zdarzenie wywołane przyczyną zewnętrzną, powodujące uraz lub śmierć, związane z pracą",
    "required_conditions": [
        "zdarzenie_nagłe",
        "przyczyna_zewnetrzna",
        "uraz_lub_smierc",
        "zwiazek_z_praca"
    ],
    "exclusions": [
        "choroba zawodowa",
        "wypadek w drodze do pracy (bez związku z pracą)",
        "wypadek podczas przerwy (bez związku z pracą)"
    ]
}

# Reguły decyzyjne dla klasyfikacji
DECISION_RULES = {
    "uznac_wypadek": {
        "min_confidence": 0.7,
        "required_indicators": [
            "zdarzenie_nagłe_potwierdzone",
            "przyczyna_zewnetrzna_okreslona",
            "uraz_dokumentowany",
            "zwiazek_z_praca_udowodniony"
        ]
    },
    "nie_uznac_wypadek": {
        "indicators": [
            "brak_zwiazku_z_praca",
            "choroba_zawodowa",
            "zdarzenie_nie_nagle",
            "brak_przyczyny_zewnetrznej"
        ]
    }
}

# Konfiguracja OCR
OCR_CONFIG = {
    "engine": "tesseract",  # lub "paddleocr", "easyocr"
    "language": "pol",
    "preprocessing": True
}

# Konfiguracja API
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "cors_origins": ["*"],  # W produkcji: konkretne domeny
    "max_file_size": 10 * 1024 * 1024  # 10MB
}

# Konfiguracja ścieżek
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# TEMP_UPLOADS_DIR już zdefiniowane na początku pliku

