"""
🚀 Uruchomienie Asystenta AI z Ollama 3.2
"""

import os
import sys

# Dodaj ścieżkę do system/ do sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_system_dir = os.path.join(os.path.dirname(_current_dir), 'system')
if _system_dir not in sys.path:
    sys.path.insert(0, _system_dir)

print("="*70)
print("  ASYSTENT AI DLA ADMINISTRACJI - OLLAMA 3.2")
print("="*70)
print("  Uruchamianie z lokalnym modelem open-source (llama3.2)")
print("="*70)
print()

try:
    from asystent_ai_gqpa_integrated import create_demo_assistant, demo_full_workflow
    
    print("✅ Moduły załadowane\n")
    print("Tworzenie asystenta z lokalnym modelem Ollama 3.2...\n")
    
    # Utwórz asystenta z lokalnym modelem (domyślnie True)
    assistant = create_demo_assistant()
    
    print("\n" + "="*70)
    print("Uruchamianie pełnej demonstracji workflow...")
    print("="*70 + "\n")
    
    # Uruchom pełną demonstrację
    demo_full_workflow()
    
    print("\n" + "="*70)
    print("✅ ZAKOŃCZONO POMYŚLNIE")
    print("="*70)
    
except ImportError as e:
    print(f"\n❌ Błąd importu: {e}")
    print("\nRozwiązanie:")
    print("1. Upewnij się, że jesteś w folderze AIWSLUZBIE")
    print("2. Sprawdź czy plik asystent_ai_gqpa_integrated.py istnieje")
    print("3. Zainstaluj brakujące zależności: pip install -r requirements.txt")
    sys.exit(1)

except Exception as e:
    print(f"\n❌ Błąd: {e}")
    import traceback
    traceback.print_exc()
    print("\n💡 Wskazówki:")
    print("- Sprawdź czy serwer Ollama działa: ollama serve")
    print("- Sprawdź czy model llama3.2 jest zainstalowany: ollama list")
    print("- Zobacz szczegóły błędu powyżej")
    sys.exit(1)

