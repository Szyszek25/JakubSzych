"""
Konfiguracja systemu Ścieżka Prawa (GQPA Legislative Navigator)
"""

import os
from pathlib import Path
from typing import Dict, Any

# Ścieżki
BASE_DIR = Path(__file__).parent.absolute()
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Tworzenie katalogów
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Konfiguracja API
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8003,
    "title": "Ścieżka Prawa API (GQPA Legislative Navigator)",
    "version": "1.0.0",
    "description": "System analizy i prognozowania procesów legislacyjnych"
}

# Konfiguracja GQPA
GQPA_CONFIG = {
    "cognitive_cycles": 10,
    "memory_size": 1000,
    "impact_analysis_depth": 5,
    "scenario_horizon_months": 12
}

# Źródła danych legislacyjnych
LEGISLATIVE_SOURCES = {
    "rcl": "https://www.gov.pl/web/rcl",
    "sejm": "https://www.sejm.gov.pl",
    "senat": "https://www.senat.gov.pl",
    "bip": "https://www.bip.gov.pl"
}

# Statusy legislacyjne
LEGISLATIVE_STATUSES = [
    "prekonsultacje",
    "konsultacje_spoleczne",
    "projekt_rzadowy",
    "rada_ministrow",
    "sejm_pierwsze_czytanie",
    "sejm_drugie_czytanie",
    "sejm_trzecie_czytanie",
    "senat",
    "podpis_prezydenta",
    "opublikowanie",
    "wejscie_w_zycie"
]

# Typy analizy wpływu
IMPACT_TYPES = [
    "finansowy",
    "spoleczny",
    "technologiczny",
    "operacyjny",
    "prawny",
    "ekonomiczny"
]

# Konfiguracja Plain Language
PLAIN_LANGUAGE_CONFIG = {
    "max_sentence_length": 20,
    "max_word_length": 12,
    "avoid_jargon": True,
    "use_active_voice": True,
    "simplify_numbers": True
}

# Konfiguracja bezpieczeństwa
SECURITY_CONFIG = {
    "rodo_compliant": True,
    "data_encryption": True,
    "access_logging": True,
    "rate_limiting": True
}

# Konfiguracja dostępności
ACCESSIBILITY_CONFIG = {
    "wcag_level": "AA",
    "screen_reader_support": True,
    "keyboard_navigation": True,
    "high_contrast_mode": True
}


