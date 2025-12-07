"""
Demo flow dla systemu Scenariusze Jutra
Uruchamia pełną analizę z przykładowymi danymi
"""
import os
import sys
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych
load_dotenv()

from main_orchestrator import ScenarioOrchestrator, create_situation_factors_from_weights
from config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE_REALISTIC, ANALYSIS_CONFIG

def main():
    print("=" * 80)
    print("🌍 SCENARIUSZE JUTRA - SYSTEM ANALIZY FORESIGHTOWEJ DLA MSZ")
    print("=" * 80)
    print()
    print("System analizuje sytuację międzynarodową i generuje scenariusze")
    print("dla państwa Atlantis w perspektywie 12 i 36 miesięcy.")
    print()
    
    # Sprawdzenie klucza API
    if not OPENAI_API_KEY:
        print("⚠️  UWAGA: Brak klucza OPENAI_API_KEY w zmiennych środowiskowych")
        print("   System będzie używał uproszczonej wersji bez LLM")
        print()
    
    # Konfiguracja
    config = {
        "OPENAI_MODEL": OPENAI_MODEL,
        "TEMPERATURE_REALISTIC": TEMPERATURE_REALISTIC,
        "ANALYSIS_CONFIG": ANALYSIS_CONFIG,
        "ANTI_POISONING_CONFIG": {
            "min_source_count": 3,
            "source_verification": True,
            "cross_reference_sources": True,
            "anomaly_detection": True,
            "reputation_check": True
        }
    }
    
    # Inicjalizacja orchestratora
    print("🔧 Inicjalizacja systemu...")
    orchestrator = ScenarioOrchestrator(config, OPENAI_API_KEY or "", gemini_model=None)
    print("✅ System gotowy")
    print()
    
    # Przygotowanie czynników sytuacyjnych
    print("📋 Przygotowanie czynników sytuacyjnych...")
    situation_factors = create_situation_factors_from_weights()
    print(f"✅ Zarejestrowano {len(situation_factors)} czynników z wagami")
    print()
    
    # Wyświetlenie czynników
    print("Czynniki sytuacyjne:")
    for factor_id, factor_data in situation_factors.items():
        print(f"  {factor_id.upper()}: waga {factor_data['weight']}")
        print(f"    {factor_data['description'][:100]}...")
    print()
    
    # Uruchomienie analizy
    print("🚀 Rozpoczynam analizę...")
    print("   (W trybie demo - bez zbierania danych z internetu)")
    print()
    
    try:
        results = orchestrator.run_full_analysis(
            situation_factors,
            collect_data=False  # Demo - bez zbierania danych
        )
        
        # Wyświetlenie wyników
        print("\n" + "=" * 80)
        print("📊 WYNIKI ANALIZY")
        print("=" * 80)
        print()
        
        print(f"Wygenerowano {len(results['scenarios'])} scenariuszy:")
        for scenario in results['scenarios']:
            type_name = "pozytywny" if scenario.scenario_type == "positive" else "negatywny"
            print(f"  - {type_name.upper()}, {scenario.timeframe_months} miesięcy: {scenario.title}")
        
        print()
        print(f"Wygenerowano rekomendacje:")
        print(f"  - Unikanie negatywnych scenariuszy: {len(results['recommendations']['avoid_negative'])}")
        print(f"  - Realizacja pozytywnych scenariuszy: {len(results['recommendations']['pursue_positive'])}")
        
        print()
        print("📈 Statystyki analizy:")
        stats = results['statistics']
        print(f"  - Źródła danych: {stats['data_sources']}")
        print(f"  - Przeanalizowane fakty: {stats['analyzed_facts']}")
        print(f"  - Znalezione korelacje: {stats['correlations']}")
        print(f"  - Koncepty w grafie wiedzy: {stats['concepts']}")
        print(f"  - Relacje w grafie: {stats['relations']}")
        print(f"  - Łańcuchy przyczynowe: {stats['causal_chains']}")
        
        # Zapisanie raportu
        from datetime import datetime
        report_file = f"raport_atlantis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(results['report'])
        
        print()
        print(f"✅ Raport zapisany do: {report_file}")
        print()
        print("=" * 80)
        print("✅ ANALIZA ZAKOŃCZONA POMYŚLNIE")
        print("=" * 80)
        
        # Wyświetlenie fragmentu raportu
        print("\n📄 Fragment raportu:")
        print("-" * 80)
        report_lines = results['report'].split('\n')
        for line in report_lines[:30]:  # Pierwsze 30 linii
            print(line)
        print("...")
        print(f"(Pełny raport w pliku: {report_file})")
        
    except Exception as e:
        print(f"\n❌ Błąd podczas analizy: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

