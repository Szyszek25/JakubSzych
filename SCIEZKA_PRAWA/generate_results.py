"""
🚀 Generowanie wyników demo dla Ścieżka Prawa
Tworzy przykładowe dokumenty legislacyjne i ich analizy
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Dodaj ścieżkę do modułów
sys.path.insert(0, os.path.dirname(__file__))

from main_orchestrator import GQPALegislativeOrchestrator

# Utwórz folder outputs
OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR = OUTPUTS_DIR / "raporty"
REPORTS_DIR.mkdir(exist_ok=True)
VISUALIZATIONS_DIR = OUTPUTS_DIR / "wykresy"
VISUALIZATIONS_DIR.mkdir(exist_ok=True)

def generate_demo_results():
    """Generuje przykładowe wyniki dla jury"""
    
    print("="*70)
    print("🏛️ GENEROWANIE WYNIKÓW - ŚCIEŻKA PRAWA")
    print("="*70)
    
    orchestrator = GQPALegislativeOrchestrator()
    
    # Przykładowe dokumenty legislacyjne
    demo_documents = [
        {
            "title": "Ustawa o cyfryzacji usług publicznych",
            "description": "Projekt ustawy mający na celu cyfryzację usług publicznych i uproszczenie procedur administracyjnych",
            "text": """
            Art. 1. Ustawa określa zasady i tryb świadczenia usług publicznych w formie elektronicznej oraz zasady 
            funkcjonowania systemu teleinformatycznego umożliwiającego świadczenie tych usług.
            
            Art. 2. Minister właściwy do spraw informatyzacji prowadzi centralny rejestr usług publicznych świadczonych 
            w formie elektronicznej, zwany dalej "rejestrem".
            
            Art. 3. Organy administracji publicznej są obowiązane do świadczenia usług publicznych w formie elektronicznej, 
            z zastrzeżeniem art. 4.
            
            Art. 4. Wyłączenia od obowiązku świadczenia usług w formie elektronicznej określa rozporządzenie.
            """,
            "metadata": {
                "autor": "Ministerstwo Cyfryzacji",
                "data_publikacji": "2024-11-15",
                "typ": "ustawa",
                "status_poczatkowy": "prekonsultacje"
            },
            "create_consultation": True,
            "policies_to_check": ["RODO", "DSA", "WCAG"]
        },
        {
            "title": "Rozporządzenie w sprawie ochrony danych osobowych w systemach teleinformatycznych",
            "description": "Rozporządzenie określające szczegółowe wymagania dotyczące ochrony danych osobowych",
            "text": """
            § 1. Rozporządzenie określa szczegółowe wymagania techniczne i organizacyjne dotyczące ochrony danych osobowych 
            w systemach teleinformatycznych używanych przez organy administracji publicznej.
            
            § 2. Administratorzy danych są obowiązani do stosowania szyfrowania danych osobowych przesyłanych przez sieć 
            publiczną oraz do prowadzenia rejestru przetwarzania danych osobowych.
            
            § 3. Wymagania dotyczące bezpieczeństwa systemów teleinformatycznych określa załącznik nr 1 do rozporządzenia.
            """,
            "metadata": {
                "autor": "Urząd Ochrony Danych Osobowych",
                "data_publikacji": "2024-10-20",
                "typ": "rozporządzenie",
                "status_poczatkowy": "konsultacje_spoleczne"
            },
            "create_consultation": True,
            "policies_to_check": ["RODO"]
        },
        {
            "title": "Projekt ustawy o dostępności cyfrowej",
            "description": "Ustawa mająca na celu zapewnienie dostępności cyfrowej stron internetowych i aplikacji mobilnych",
            "text": """
            Art. 1. Ustawa określa wymagania dotyczące dostępności cyfrowej stron internetowych i aplikacji mobilnych 
            podmiotów publicznych.
            
            Art. 2. Podmioty publiczne są obowiązane do zapewnienia dostępności cyfrowej swoich stron internetowych i 
            aplikacji mobilnych zgodnie z wymaganiami określonymi w ustawie.
            
            Art. 3. Wymagania dostępności cyfrowej obejmują m.in. możliwość odczytu treści przez czytniki ekranu, 
            odpowiedni kontrast kolorów oraz możliwość nawigacji za pomocą klawiatury.
            """,
            "metadata": {
                "autor": "Ministerstwo Funduszy i Polityki Regionalnej",
                "data_publikacji": "2024-12-01",
                "typ": "projekt_ustawy",
                "status_poczatkowy": "prekonsultacje"
            },
            "create_consultation": False,
            "policies_to_check": ["WCAG", "RODO"]
        }
    ]
    
    results = []
    
    for i, doc_data in enumerate(demo_documents, 1):
        print(f"\n[{i}/{len(demo_documents)}] Przetwarzanie: {doc_data['title']}")
        
        try:
            # Przetwórz dokument
            result = orchestrator.process_new_document(doc_data)
            doc_id = result["document_id"]
            
            # Pobierz kompleksowy raport
            comprehensive_report = orchestrator.get_comprehensive_report(doc_id)
            
            # Zapisz raport
            report_file = REPORTS_DIR / f"raport_{doc_id}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(comprehensive_report, f, ensure_ascii=False, indent=2, default=str)
            
            # Zapisz również w formacie czytelnym
            report_md = REPORTS_DIR / f"raport_{doc_id}.md"
            with open(report_md, 'w', encoding='utf-8') as f:
                f.write(f"# Raport: {doc_data['title']}\n\n")
                f.write(f"**ID Dokumentu:** {doc_id}\n\n")
                f.write(f"**Data wygenerowania:** {datetime.now().isoformat()}\n\n")
                f.write(f"## Status\n\n")
                f.write(f"- Status: {comprehensive_report.get('document', {}).get('status', 'N/A')}\n")
                f.write(f"- Etap: {comprehensive_report.get('document', {}).get('current_stage', 'N/A')}\n\n")
                f.write(f"## Analiza Wpływu\n\n")
                impact = comprehensive_report.get('impact_analysis', {})
                if impact:
                    f.write(f"- Typy analizy: {len(impact.get('analyses', []))}\n")
                    f.write(f"- Scenariusze: {len(comprehensive_report.get('scenarios', []))}\n\n")
                f.write(f"## Konsultacje Społeczne\n\n")
                consultations = comprehensive_report.get('consultations', [])
                f.write(f"- Liczba konsultacji: {len(consultations)}\n\n")
                if consultations:
                    for cons in consultations:
                        f.write(f"  - {cons.get('title', 'N/A')} (Status: {cons.get('status', 'N/A')})\n")
            
            results.append({
                "document_id": doc_id,
                "title": doc_data["title"],
                "status": comprehensive_report.get('document', {}).get('status', 'N/A'),
                "report_file": str(report_file),
                "report_md": str(report_md)
            })
            
            print(f"  ✅ Raport zapisany: {report_file.name}")
            
        except Exception as e:
            print(f"  ❌ Błąd: {e}")
            import traceback
            traceback.print_exc()
    
    # Zapisz podsumowanie
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_documents": len(results),
        "documents": results,
        "dashboard_data": orchestrator.get_dashboard_data()
    }
    
    summary_file = OUTPUTS_DIR / "podsumowanie_wynikow.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ Wygenerowano {len(results)} dokumentów")
    print(f"✅ Podsumowanie zapisane: {summary_file}")
    print(f"\n📁 Lokalizacja wyników:")
    print(f"   - Raporty JSON: {REPORTS_DIR}")
    print(f"   - Raporty Markdown: {REPORTS_DIR}")
    print(f"   - Podsumowanie: {summary_file}")
    
    return results

if __name__ == "__main__":
    generate_demo_results()

