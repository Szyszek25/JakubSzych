"""
🔧 Konfiguracja HAMA Diamond-Indeks Branż
"""

from pathlib import Path
from typing import Dict, List

# ============================================================================
# ŚCIEŻKI
# ============================================================================

BASE_DIR = Path(__file__).parent.absolute()
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "raporty"
CHARTS_DIR = OUTPUTS_DIR / "wykresy"

# Tworzenie katalogów
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR, CHARTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ============================================================================
# DEFINICJE BRANŻ (PKD/NACE)
# ============================================================================

# Poziom: DZIAŁ (2-cyfrowy kod PKD)
# Wybrane branże do analizy (przykładowe)

BRANZE_PKD = {
    "46": {
        "nazwa": "Handel hurtowy",
        "poziom": "dzial",
        "pkd_2007": "46",
        "pkd_2025": "46"
    },
    "47": {
        "nazwa": "Handel detaliczny",
        "poziom": "dzial",
        "pkd_2007": "47",
        "pkd_2025": "47"
    },
    "41": {
        "nazwa": "Budownictwo",
        "poziom": "dzial",
        "pkd_2007": "41",
        "pkd_2025": "41"
    },
    "25": {
        "nazwa": "Produkcja wyrobów metalowych",
        "poziom": "dzial",
        "pkd_2007": "25",
        "pkd_2025": "25"
    },
    "26": {
        "nazwa": "Produkcja komputerów i elektroniki",
        "poziom": "dzial",
        "pkd_2007": "26",
        "pkd_2025": "26"
    },
    "62": {
        "nazwa": "Działalność związana z oprogramowaniem",
        "poziom": "dzial",
        "pkd_2007": "62",
        "pkd_2025": "62"
    },
    "68": {
        "nazwa": "Działalność związana z nieruchomościami",
        "poziom": "dzial",
        "pkd_2007": "68",
        "pkd_2025": "68"
    },
    "56": {
        "nazwa": "Działalność związana z zakwaterowaniem i usługami gastronomicznymi",
        "poziom": "dzial",
        "pkd_2007": "56",
        "pkd_2025": "56"
    },
    "49": {
        "nazwa": "Transport lądowy",
        "poziom": "dzial",
        "pkd_2007": "49",
        "pkd_2025": "49"
    },
    "52": {
        "nazwa": "Magazynowanie i działalność usługowa wspomagająca transport",
        "poziom": "dzial",
        "pkd_2007": "52",
        "pkd_2025": "52"
    }
}

# ============================================================================
# WSKAŹNIKI - WAGI POCZĄTKOWE
# ============================================================================

# Wagi będą dynamicznie dostosowywane przez HAMA Diamond
# Te są wartościami początkowymi

WSKAZNIKI_WAGI = {
    "dynamika_przychodow": 0.20,
    "rentownosc": 0.15,
    "zadluzenie": 0.15,
    "szkodowosc": 0.15,
    "dynamika_eksportu": 0.10,
    "inwestycje": 0.10,
    "nastroje_konsumenckie": 0.05,
    "trendy_wyszukiwan": 0.05,
    "nowe_firmy": 0.03,
    "produktywnosc": 0.02
}

# ============================================================================
# KLASYFIKACJA BRANŻ
# ============================================================================

KATEGORIE_BRANZ = {
    "wzrostowe": {
        "indeks_min": 70,
        "indeks_max": 100,
        "opis": "Branże o wysokim tempie rozwoju, niskim ryzyku"
    },
    "stabilne": {
        "indeks_min": 50,
        "indeks_max": 70,
        "opis": "Branże o umiarkowanym wzroście, stabilnych fundamentach"
    },
    "ryzykowne": {
        "indeks_min": 30,
        "indeks_max": 50,
        "opis": "Branże z wysokim zadłużeniem lub spowolnieniem"
    },
    "kurczace_sie": {
        "indeks_min": 0,
        "indeks_max": 30,
        "opis": "Branże z negatywną dynamiką, wysokim ryzykiem"
    },
    "wymagajace_finansowania": {
        "indeks_min": 40,
        "indeks_max": 70,
        "opis": "Branże z potencjałem wzrostu, wymagające kapitału"
    }
}

# ============================================================================
# ŹRÓDŁA DANYCH
# ============================================================================

ZRODLA_DANYCH = {
    "gus": {
        "url_base": "https://stat.gov.pl",
        "api_available": False,  # Wymaga manualnego pobrania
        "dane_dostepne": [
            "przychody_branz",
            "eksport_import",
            "zatrudnienie",
            "inwestycje"
        ]
    },
    "krs": {
        "url_base": "https://ekrs.ms.gov.pl",
        "api_available": False,
        "dane_dostepne": [
            "nowe_firmy",
            "upadlosci",
            "liczba_podmiotow"
        ]
    },
    "google_trends": {
        "api_available": True,
        "library": "pytrends",
        "dane_dostepne": [
            "trendy_wyszukiwan"
        ]
    },
    "npk": {
        "url_base": "https://www.nbp.pl",
        "api_available": False,
        "dane_dostepne": [
            "nastroje_konsumenckie"
        ]
    }
}

# ============================================================================
# PARAMETRY HAMA DIAMOND
# ============================================================================

HAMA_CONFIG = {
    "normalizacja": {
        "metoda": "min_max",  # min_max, z_score, robust
        "clip": True,
        "clip_min": 0.0,
        "clip_max": 1.0
    },
    "agregacja": {
        "metoda": "weighted_sum",  # weighted_sum, geometric_mean, harmonic_mean
        "dynamiczne_wagi": True
    },
    "horyzont_czasowy": {
        "min_miesiecy": 12,
        "max_miesiecy": 36,
        "domyslny": 24
    },
    "interpretacja": {
        "jezyk": "pl",
        "szczegolowosc": "srednia",  # niska, srednia, wysoka
        "format": "tekstowy"  # tekstowy, json, markdown
    }
}

# ============================================================================
# PARAMETRY WIZUALIZACJI
# ============================================================================

VIZ_CONFIG = {
    "format": "html",  # html, png, pdf
    "interaktywny": True,
    "kolory": {
        "wzrostowe": "#2ecc71",
        "stabilne": "#3498db",
        "ryzykowne": "#f39c12",
        "kurczace_sie": "#e74c3c",
        "wymagajace_finansowania": "#9b59b6"
    },
    "rozmiar": {
        "szerokosc": 1200,
        "wysokosc": 800
    }
}

