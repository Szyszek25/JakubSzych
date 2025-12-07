"""
🧪 Test integracji z GQPA Core
Sprawdza czy asystent poprawnie korzysta z biblioteki hama_core
"""

import os
import sys

# Dodaj ścieżkę do system/
_current_dir = os.path.dirname(os.path.abspath(__file__))
_system_dir = os.path.join(os.path.dirname(_current_dir), 'system')
if _system_dir not in sys.path:
    sys.path.insert(0, _system_dir)

print("="*70)
print("🧪 TEST INTEGRACJI Z GQPA CORE")
print("="*70)

# Test 1: Import GQPA Core
print("\n[1] Test importu GQPA Core...")
try:
    from hama_core import get_hama_info
    info = get_hama_info()
    print(f"✅ GQPA Core załadowany:")
    print(f"   - Nazwa: {info['name']}")
    print(f"   - Wersja: {info['version']}")
    print(f"   - Autorzy: {', '.join(info['authors'])}")
    print(f"   - Status: {info['status']}")
except ImportError as e:
    print(f"❌ Błąd importu GQPA Core: {e}")
    print("   Upewnij się, że folder system/hama_core/ istnieje")

# Test 2: Import asystenta
print("\n[2] Test importu asystenta...")
try:
    from asystent_ai_gqpa_integrated import (
        HAMAAdministrativeAssistant,
        GeminiCognitiveAdapter,
        create_demo_assistant
    )
    print("✅ Asystent załadowany poprawnie")
except ImportError as e:
    print(f"❌ Błąd importu asystenta: {e}")

# Test 3: Utworzenie asystenta
print("\n[3] Test utworzenia asystenta...")
try:
    assistant = create_demo_assistant()
    print("✅ Asystent utworzony poprawnie")
    
    # Sprawdź czy ma informację o GQPA
    if hasattr(assistant, 'hama_info') and assistant.hama_info:
        print(f"✅ Informacja o HAMA Diamond: {assistant.hama_info['name']}")
    else:
        print("⚠️ Brak informacji o GQPA (może być OK jeśli GQPA nie jest dostępne)")
        
except Exception as e:
    print(f"❌ Błąd utworzenia asystenta: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Sprawdzenie struktury
print("\n[4] Test struktury projektu...")
hama_core_path = os.path.join(_system_dir, 'hama_core', '__init__.py')
if os.path.exists(hama_core_path):
    print(f"✅ HAMA Diamond Core znajduje się w: {hama_core_path}")
else:
    print(f"⚠️ HAMA Diamond Core nie znaleziony w: {hama_core_path}")

license_path = os.path.join(_system_dir, 'LICENSE_GQPA.txt')
if os.path.exists(license_path):
    print(f"✅ Licencja GQPA znajduje się w: {license_path}")
else:
    print(f"⚠️ Licencja GQPA nie znaleziona w: {license_path}")

print("\n" + "="*70)
print("✅ TEST ZAKOŃCZONY")
print("="*70)
print("\nJeśli wszystkie testy przeszły ✅, integracja działa poprawnie!")
print("GQPA Core jest używane jako Background IP (biblioteka zewnętrzna).")

