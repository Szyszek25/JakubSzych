"""
🚀 PROSTY SKRYPT URUCHOMIENIA
Kopiuj i wklej - gotowe do użycia!
"""

import os
import sys
from datetime import datetime, timedelta

# ============================================================================
# KONFIGURACJA - USTAW SWÓJ KLUCZ API TUTAJ
# ============================================================================

# Opcja 1: Ustaw tutaj bezpośrednio (nie zalecane dla produkcji)
# os.environ['GOOGLE_API_KEY'] = 'TWÓJ_KLUCZ_API_TUTAJ'

# Opcja 2: Użyj zmiennej środowiskowej (zalecane)
# W PowerShell: $env:GOOGLE_API_KEY="twój_klucz"
# W CMD: set GOOGLE_API_KEY=twój_klucz
# W Linux/Mac: export GOOGLE_API_KEY="twój_klucz"

# ============================================================================
# SPRAWDZENIE KONFIGURACJI
# ============================================================================

print("="*70)
print("🏛️ ASYSTENT AI DLA ADMINISTRACJI - PROSTY START")
print("="*70)

# Sprawdź klucz API
api_key = os.environ.get('GOOGLE_API_KEY')
if api_key:
    print(f"✅ Klucz API: {api_key[:10]}...{api_key[-4:]}")
else:
    print("⚠️  Klucz API nie ustawiony - system będzie działał w trybie symulacji")
    print("   Ustaw: os.environ['GOOGLE_API_KEY'] = 'twój_klucz'")

# Sprawdź zależności
print("\n📦 Sprawdzanie zależności...")
try:
    import google.generativeai
    print("   ✅ google-generativeai")
except ImportError:
    print("   ❌ google-generativeai - uruchom: pip install google-generativeai")
    sys.exit(1)

try:
    import pandas
    print("   ✅ pandas")
except ImportError:
    print("   ❌ pandas - uruchom: pip install pandas")

try:
    import numpy
    print("   ✅ numpy")
except ImportError:
    print("   ❌ numpy - uruchom: pip install numpy")

# ============================================================================
# IMPORT I URUCHOMIENIE
# ============================================================================

print("\n🚀 Uruchamianie systemu...\n")

try:
    # Import głównego modułu
    from asystent_ai_gqpa_integrated import (
        create_demo_assistant,
        AdministrativeCase,
        demo_full_workflow
    )
    
    print("✅ Moduły załadowane\n")
    
    # Wybór trybu uruchomienia
    print("Wybierz tryb:")
    print("1. Pełna demonstracja (demo_full_workflow)")
    print("2. Prosty przykład (własna sprawa)")
    print("3. Wszystkie przykłady z examples_integration.py")
    
    choice = input("\nTwój wybór (1/2/3, Enter=1): ").strip() or "1"
    
    if choice == "1":
        # Pełna demonstracja
        print("\n" + "="*70)
        print("DEMONSTRACJA PEŁNEGO WORKFLOW")
        print("="*70 + "\n")
        demo_full_workflow()
    
    elif choice == "2":
        # Prosty przykład
        print("\n" + "="*70)
        print("PROSTY PRZYKŁAD")
        print("="*70 + "\n")
        
        # Utworzenie asystenta
        assistant = create_demo_assistant()
        
        # Utworzenie sprawy
        case = AdministrativeCase(
            case_id="DEMO-001",
            case_type="kwalifikacja_zawodowa",
            documents=[
                {
                    "type": "wniosek",
                    "content": "Wniosek o nadanie kwalifikacji przewodnika turystycznego. Wnioskodawca: Jan Kowalski."
                }
            ],
            parties=["Jan Kowalski", "MSiT"],
            status="w_trakcie",
            deadline=datetime.now() + timedelta(days=15)
        )
        
        # Dodanie sprawy
        assistant.add_case(case)
        print(f"✅ Sprawa {case.case_id} dodana")
        
        # Analiza
        print("\n🔍 Analiza sprawy...")
        analysis = assistant.analyze_case(case.case_id)
        print(f"✅ Analiza zakończona")
        print(f"   Poziom ryzyka: {analysis['risk_assessment']['level']}")
        print(f"   Czas: {analysis['analysis_time']:.2f}s")
        
        # Generowanie decyzji
        print("\n📄 Generowanie projektu decyzji...")
        draft = assistant.generate_decision_draft(case.case_id, "pozytywna")
        print(f"✅ Projekt decyzji wygenerowany")
        print(f"   Zgodność: {sum(draft.compliance_checks.values())}/{len(draft.compliance_checks)}")
    
    elif choice == "3":
        # Wszystkie przykłady
        print("\n" + "="*70)
        print("WSZYSTKIE PRZYKŁADY")
        print("="*70 + "\n")
        
        try:
            from examples_integration import example_full_workflow
            example_full_workflow()
        except ImportError:
            print("❌ Nie można załadować examples_integration.py")
            print("   Upewnij się, że plik istnieje w tym samym folderze")
    
    else:
        print("❌ Nieprawidłowy wybór")
    
    print("\n" + "="*70)
    print("✅ ZAKOŃCZONO POMYŚLNIE")
    print("="*70)

except ImportError as e:
    print(f"\n❌ Błąd importu: {e}")
    print("\nRozwiązanie:")
    print("1. Upewnij się, że jesteś w folderze AIWSLUZBIE")
    print("2. Sprawdź czy plik asystent_ai_gqpa_integrated.py istnieje")
    print("3. Zainstaluj brakujące zależności: pip install google-generativeai pandas numpy")

except Exception as e:
    print(f"\n❌ Błąd: {e}")
    import traceback
    traceback.print_exc()
    print("\n💡 Wskazówki:")
    print("- Sprawdź czy klucz API jest poprawny")
    print("- Sprawdź połączenie internetowe")
    print("- Zobacz szczegóły błędu powyżej")

