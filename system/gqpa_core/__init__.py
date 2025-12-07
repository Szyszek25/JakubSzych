"""
⚠️ BACKGROUND IP - NIE PODLEGA PRZENIESIENIU PRAW

GQPA DIAMOND - Generic Quantum-Phenomenological Architecture
Cognitive AI Framework

Copyright © 2024-2025 Jakub Szych & Michał Wojtków
All rights reserved.

Zobacz: LICENSE_GQPA.txt
"""

# Minimalne API GQPA dla asystenta administracyjnego
# Pełna implementacja w plikach gqpa_part*.py

__version__ = "1.0.0"
__authors__ = ["Jakub Szych", "Michał Wojtków"]

# Eksport podstawowych komponentów (jeśli są używane)
# W razie potrzeby można dodać importy z gqpa_part*.py

def get_gqpa_info():
    """Zwraca informacje o GQPA"""
    return {
        "name": "GQPA DIAMOND",
        "version": __version__,
        "authors": __authors__,
        "status": "Background IP - Not transferable",
        "license": "See LICENSE_GQPA.txt"
    }

