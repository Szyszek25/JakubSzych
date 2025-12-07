"""
Konfiguracja narzędzia Scenariusze Jutra
"""
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# Konfiguracja API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4-turbo-preview"  # lub gpt-4 dla lepszej jakości
TEMPERATURE_REALISTIC = 0.3  # Realistyczne scenariusze
TEMPERATURE_CREATIVE = 0.8   # Kreatywne scenariusze (bonus)

# Konfiguracja państwa Atlantis
ATLANTIS_PROFILE = {
    "name": "Atlantis",
    "population": 28_000_000,
    "climate": "umiarkowany",
    "geography": {
        "baltic_sea_access": True,
        "navigable_rivers": True,
        "limited_fresh_water": True
    },
    "economy": {
        "strong_sectors": [
            "przemysł ciężki",
            "motoryzacyjny",
            "spożywczy",
            "chemiczny",
            "ICT",
            "OZE",
            "przetwarzanie surowców krytycznych",
            "infrastruktura AI"
        ],
        "currency": "inna niż euro",
        "gdp_rank": 25
    },
    "military": {
        "personnel": 150_000
    },
    "digitalization": "powyżej średniej europejskiej",
    "key_relations": [
        "Niemcy", "Francja", "Finlandia", "Ukraina", "USA", "Japonia"
    ],
    "memberships": {
        "EU": "od 1997",
        "NATO": "od 1997"
    },
    "threats": {
        "political": [
            "niestabilność w UE",
            "rozpad UE na grupy różnych prędkości",
            "negatywna kampania wizerunkowa"
        ],
        "economic": [
            "zakłócenia w dostawach paliw węglowodorowych",
            "embargo na wysokozaawansowane procesory"
        ],
        "military": [
            "zagrożenie atakiem zbrojnym sąsiada",
            "ataki hybrydowe",
            "ataki na infrastrukturę krytyczną i cyberprzestrzeń"
        ]
    }
}

# Źródła danych do analizy
DATA_SOURCES = {
    "ministries": {
        "countries": [
            "Germany", "France", "UK", "USA", "Russia", "China", "India", "Saudi Arabia"
        ],
        "ministries": [
            "foreign affairs", "defense", "interior", "economy", "trade",
            "energy", "climate", "higher education", "new technologies",
            "digitalization", "education"
        ]
    },
    "institutions": [
        "European Commission",
        "NATO",
        "UN",
        "OECD",
        "Gulf Cooperation Council",
        "International Institute for Strategic Studies",
        "Center for Strategic and International Studies",
        "Chatham House",
        "European Council on Foreign Relations",
        "Atlantic Council",
        "Kiel Institute",
        "NASDAQ",
        "London Stock Exchange Group",
        "Japan Exchange Group"
    ]
}

# Parametry analizy
ANALYSIS_CONFIG = {
    "max_words": 50_000_000,  # Wersja podstawowa: 50 mln słów
    "date_threshold": "2020-12-31",  # Dane po tej dacie
    "languages": ["en", "pl"],
    "memory_size": 10,  # 10 ostatnich promptów
    "scenario_timeframes": [12, 36],  # miesiące
    "scenario_types": ["positive", "negative"]
}

# Wagi scenariuszy (z opisu zadania)
SCENARIO_WEIGHTS = {
    "a": 30,  # Katastrofa producenta procesorów
    "b": 15,  # Przemysł motoryzacyjny
    "c": 15,  # PKB strefy euro
    "d": 10,  # Ukraina
    "e": 5,   # Inwestycje w Ukrainie
    "f": 25   # OZE i paliwa węglowodorowe
}

# Konfiguracja bezpieczeństwa
SECURITY_CONFIG = {
    "encrypt_prompts": True,
    "domain_restriction": "msz.gov.pl",  # Tylko dla domeny MSZ
    "log_queries": True,
    "max_query_length": 10000
}

# Konfiguracja ochrony przed data poisoning
ANTI_POISONING_CONFIG = {
    "source_verification": True,
    "cross_reference_sources": True,
    "anomaly_detection": True,
    "reputation_check": True,
    "min_source_count": 3  # Minimum źródeł potwierdzających fakt
}

