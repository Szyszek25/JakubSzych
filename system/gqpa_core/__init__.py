"""
⚠️ BACKGROUND IP - NIE PODLEGA PRZENIESIENIU PRAW

HAMA DIAMOND - Human-AI Meta-Analysis Diamond
Cognitive AI Framework

Copyright © 2024-2025 Jakub Szych & Michał Wojtków
All rights reserved.

Zobacz: LICENSE_GQPA.txt
"""

# Minimalne API HAMA Diamond dla asystenta administracyjnego
# Pełna implementacja w plikach hama_part*.py

__version__ = "1.0.0"
__authors__ = ["Jakub Szych", "Michał Wojtków"]

# Eksport podstawowych komponentów (jeśli są używane)
# W razie potrzeby można dodać importy z hama_part*.py

def get_hama_info():
    """Zwraca informacje o HAMA Diamond"""
    return {
        "name": "HAMA DIAMOND",
        "version": __version__,
        "authors": __authors__,
        "status": "Background IP - Not transferable",
        "license": "See LICENSE_GQPA.txt"
    }

# Alias dla kompatybilności wstecznej
def get_gqpa_info():
    """Alias dla get_hama_info() - kompatybilność wsteczna"""
    return get_hama_info()

