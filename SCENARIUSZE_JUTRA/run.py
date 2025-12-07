#!/usr/bin/env python3
"""
Główny plik uruchomieniowy systemu Scenariusze Jutra
"""
import sys
import os

# Dodanie ścieżek do importów
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

if __name__ == "__main__":
    from run_demo import main
    sys.exit(main())

