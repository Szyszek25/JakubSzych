"""
💼 PRZYKŁADY INTEGRACJI I UŻYCIA
Asystent AI dla Administracji - Przykłady praktyczne
"""

from asystent_ai_gqpa_integrated import (
    HAMAAdministrativeAssistant,
    AdministrativeCase,
    GeminiCognitiveAdapter,
    create_demo_assistant,
    demo_full_workflow
)
from datetime import datetime, timedelta
import json

# ============================================================================
# PRZYKŁAD 1: PODSTAWOWE UŻYCIE - ANALIZA SPRAWY
# ============================================================================

def example_basic_case_analysis():
    """Przykład podstawowej analizy sprawy"""
    print("\n" + "="*70)
    print("PRZYKŁAD 1: Podstawowa analiza sprawy")
    print("="*70)
    
    # Utworzenie asystenta
    assistant = create_demo_assistant()
    
    # Utworzenie sprawy
    case = AdministrativeCase(
        case_id="SPR-2024-001",
        case_type="kwalifikacja_zawodowa",
        documents=[
            {
                "type": "wniosek",
                "content": """
                Wniosek o nadanie kwalifikacji przewodnika turystycznego.
                
                Wnioskodawca: Jan Kowalski
                Adres: ul. Przykładowa 1, 00-001 Warszawa
                
                Uzasadnienie:
                Posiadam dyplom ukończenia studiów wyższych na kierunku Turystyka i Rekreacja
                na Uniwersytecie Warszawskim. Ukończyłem również kurs przewodnicki organizowany
                przez Polskie Towarzystwo Turystyczno-Krajoznawcze.
                """
            },
            {
                "type": "dyplom",
                "content": """
                Dyplom ukończenia studiów wyższych
                Kierunek: Turystyka i Rekreacja
                Uczelnia: Uniwersytet Warszawski
                Rok ukończenia: 2020
                """
            }
        ],
        parties=["Jan Kowalski", "Departament Turystyki MSiT"],
        status="w_trakcie",
        deadline=datetime.now() + timedelta(days=15)
    )
    
    # Dodanie sprawy
    assistant.add_case(case)
    print(f"✅ Sprawa {case.case_id} dodana")
    
    # Analiza sprawy
    print("\n📊 Analiza sprawy...")
    analysis = assistant.analyze_case(case.case_id)
    
    print(f"\nWyniki analizy:")
    print(f"  - Poziom ryzyka: {analysis['risk_assessment']['level']}")
    print(f"  - Kwestie prawne: {len(analysis['legal_issues'])}")
    print(f"  - Czas analizy: {analysis['analysis_time']:.2f}s")
    print(f"\nStreszczenie:")
    print(analysis['summary'][:300] + "...")
    
    return assistant, case

# ============================================================================
# PRZYKŁAD 2: GENEROWANIE PROJEKTU DECYZJI
# ============================================================================

def example_decision_generation(assistant, case_id: str):
    """Przykład generowania projektu decyzji"""
    print("\n" + "="*70)
    print("PRZYKŁAD 2: Generowanie projektu decyzji")
    print("="*70)
    
    # Generowanie projektu decyzji pozytywnej
    print(f"\n📄 Generowanie projektu decyzji dla sprawy {case_id}...")
    draft = assistant.generate_decision_draft(case_id, "pozytywna")
    
    print(f"\n✅ Projekt decyzji wygenerowany")
    print(f"\nZgodność z przepisami:")
    for check, passed in draft.compliance_checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}: {passed}")
    
    print(f"\nOdniesienia prawne ({len(draft.legal_references)}):")
    for ref in draft.legal_references[:5]:
        print(f"  - {ref}")
    
    print(f"\nUzasadnienie faktyczne (fragment):")
    print(draft.factual_justification[:200] + "...")
    
    return draft

# ============================================================================
# PRZYKŁAD 3: MONITOROWANIE TERMINÓW
# ============================================================================

def example_deadline_monitoring(assistant):
    """Przykład monitorowania terminów"""
    print("\n" + "="*70)
    print("PRZYKŁAD 3: Monitorowanie terminów")
    print("="*70)
    
    # Dodanie kilku spraw z różnymi terminami
    cases = [
        AdministrativeCase(
            case_id=f"SPR-2024-{i:03d}",
            case_type="kategoria_hotelu",
            documents=[{"type": "wniosek", "content": "Wniosek o kategorię"}],
            parties=[f"Hotel {i}", "MSiT"],
            status="w_trakcie",
            deadline=datetime.now() + timedelta(days=i*2)
        )
        for i in range(1, 6)
    ]
    
    for case in cases:
        assistant.add_case(case)
    
    print(f"\n✅ Dodano {len(cases)} spraw")
    
    # Sprawdzenie terminów
    print("\n⏰ Sprawdzanie terminów w ciągu 7 dni...")
    deadlines = assistant.check_deadlines(days_ahead=7)
    
    if deadlines:
        print(f"\nZnaleziono {len(deadlines)} spraw z terminami:")
        for d in deadlines:
            priority_icon = "🔴" if d['priority'] == "krytyczny" else "🟡" if d['priority'] == "wysoki" else "🟢"
            print(f"  {priority_icon} {d['case_id']}: {d['days_left']} dni (priorytet: {d['priority']})")
    else:
        print("  Brak spraw z terminami w ciągu 7 dni")

# ============================================================================
# PRZYKŁAD 4: PRZETWARZANIE WSADOWE
# ============================================================================

def example_batch_processing():
    """Przykład przetwarzania wsadowego spraw"""
    print("\n" + "="*70)
    print("PRZYKŁAD 4: Przetwarzanie wsadowe")
    print("="*70)
    
    assistant = create_demo_assistant()
    
    # Utworzenie wielu spraw
    batch_cases = []
    for i in range(1, 6):
        case = AdministrativeCase(
            case_id=f"BATCH-{i:03d}",
            case_type="kwalifikacja_zawodowa",
            documents=[
                {
                    "type": "wniosek",
                    "content": f"Wniosek numer {i} o kwalifikację przewodnika turystycznego."
                }
            ],
            parties=[f"Wnioskodawca {i}", "MSiT"],
            status="nowa",
            deadline=datetime.now() + timedelta(days=20 + i*5)
        )
        batch_cases.append(case)
        assistant.add_case(case)
    
    print(f"\n✅ Dodano {len(batch_cases)} spraw do przetworzenia")
    
    # Przetwarzanie wsadowe
    print("\n🔄 Przetwarzanie wsadowe...")
    results = []
    
    for case in batch_cases:
        try:
            analysis = assistant.analyze_case(case.case_id)
            results.append({
                "case_id": case.case_id,
                "status": "success",
                "risk_level": analysis['risk_assessment']['level'],
                "analysis_time": analysis['analysis_time']
            })
            print(f"  ✅ {case.case_id}: {analysis['risk_assessment']['level']} ({analysis['analysis_time']:.2f}s)")
        except Exception as e:
            results.append({
                "case_id": case.case_id,
                "status": "error",
                "error": str(e)
            })
            print(f"  ❌ {case.case_id}: Błąd - {e}")
    
    # Podsumowanie
    successful = sum(1 for r in results if r['status'] == 'success')
    avg_time = sum(r['analysis_time'] for r in results if 'analysis_time' in r) / max(successful, 1)
    
    print(f"\n📊 Podsumowanie:")
    print(f"  - Przetworzono: {successful}/{len(batch_cases)}")
    print(f"  - Średni czas: {avg_time:.2f}s")
    
    return results

# ============================================================================
# PRZYKŁAD 5: INTEGRACJA Z SYSTEMAMI ZEWNĘTRZNYMI
# ============================================================================

def example_external_integration(assistant):
    """Przykład integracji z systemami zewnętrznymi"""
    print("\n" + "="*70)
    print("PRZYKŁAD 5: Integracja z systemami zewnętrznymi")
    print("="*70)
    
    # Symulacja wyszukiwania precedensów
    print("\n🔍 Wyszukiwanie precedensów...")
    precedents = assistant.external_systems.search_precedents(
        "kwalifikacja_zawodowa",
        ["przewodnik", "turystyka", "kwalifikacja"]
    )
    
    print(f"  Znaleziono {len(precedents)} precedensów")
    
    # Sprawdzenie zgodności z przepisami
    print("\n📋 Sprawdzanie zgodności z przepisami...")
    
    # Utworzenie przykładowego projektu decyzji
    from asystent_ai_gqpa_integrated import DecisionDraft
    
    draft = DecisionDraft(
        case_id="TEST-001",
        decision_type="pozytywna",
        factual_justification="Ustalenia faktyczne...",
        legal_justification="Uzasadnienie prawne zgodne z art. 10 KPA...",
        decision_text="Decyzja pozytywna...",
        legal_references=["art. 10 KPA", "Ustawa o usługach turystycznych"],
        compliance_checks={}
    )
    
    compliance = assistant.external_systems.check_legal_compliance(draft)
    
    print(f"  Zgodność z przepisami:")
    for check, passed in compliance.items():
        status = "✅" if passed else "❌"
        print(f"    {status} {check}: {passed}")
    
    # Pobranie tekstu przepisu
    print("\n📖 Pobieranie tekstu przepisu...")
    regulation = assistant.external_systems.get_regulation_text("kpa")
    if regulation:
        print(f"  {regulation[:200]}...")

# ============================================================================
# PRZYKŁAD 6: METRYKI I RAPORTY
# ============================================================================

def example_metrics_and_reports(assistant):
    """Przykład pobierania metryk i raportów"""
    print("\n" + "="*70)
    print("PRZYKŁAD 6: Metryki i raporty")
    print("="*70)
    
    # Metryki wydajności
    print("\n📊 Metryki wydajności:")
    metrics = assistant.get_performance_metrics()
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"  - {key}: {value:.2f}")
        else:
            print(f"  - {key}: {value}")
    
    # Audit log
    print("\n📋 Audit log (ostatnie 5 wpisów):")
    audit_log = assistant.export_audit_log()
    for entry in audit_log[-5:]:
        print(f"  [{entry['timestamp']}] {entry.get('operation', 'unknown')} - {entry.get('status', 'unknown')}")
    
    # Podsumowanie sprawy
    if assistant.cases:
        case_id = list(assistant.cases.keys())[0]
        print(f"\n📄 Podsumowanie sprawy {case_id}:")
        summary = assistant.get_case_summary(case_id)
        if summary:
            print(f"  - Typ: {summary['type']}")
            print(f"  - Status: {summary['status']}")
            print(f"  - Termin: {summary.get('deadline', 'Brak')}")
            if summary.get('risk_assessment'):
                print(f"  - Ryzyko: {summary['risk_assessment'].get('level', 'N/A')}")

# ============================================================================
# PRZYKŁAD 7: PEŁNY WORKFLOW
# ============================================================================

def example_full_workflow():
    """Przykład pełnego workflow od sprawy do decyzji"""
    print("\n" + "="*70)
    print("PRZYKŁAD 7: Pełny workflow")
    print("="*70)
    
    assistant = create_demo_assistant()
    
    # 1. Utworzenie sprawy
    print("\n[1] Utworzenie sprawy...")
    case = AdministrativeCase(
        case_id="WORKFLOW-001",
        case_type="kategoria_hotelu",
        documents=[
            {
                "type": "wniosek",
                "content": "Wniosek o nadanie kategorii hotelowi 'Grand Hotel' w Warszawie."
            },
            {
                "type": "dokumentacja_techniczna",
                "content": "Dokumentacja techniczna obiektu, standardy pokoi, wyposażenie."
            }
        ],
        parties=["Grand Hotel Sp. z o.o.", "Departament Turystyki MSiT"],
        status="nowa",
        deadline=datetime.now() + timedelta(days=30)
    )
    
    assistant.add_case(case)
    print(f"✅ Sprawa {case.case_id} utworzona")
    
    # 2. Analiza sprawy
    print("\n[2] Analiza sprawy...")
    analysis = assistant.analyze_case(case.case_id)
    print(f"✅ Analiza zakończona - ryzyko: {analysis['risk_assessment']['level']}")
    
    # 3. Generowanie projektu decyzji
    print("\n[3] Generowanie projektu decyzji...")
    draft = assistant.generate_decision_draft(case.case_id, "pozytywna")
    print(f"✅ Projekt decyzji wygenerowany")
    print(f"   Zgodność: {sum(draft.compliance_checks.values())}/{len(draft.compliance_checks)}")
    
    # 4. Sprawdzenie terminów
    print("\n[4] Sprawdzenie terminów...")
    deadlines = assistant.check_deadlines()
    print(f"✅ Sprawy z terminami: {len(deadlines)}")
    
    # 5. Raport końcowy
    print("\n[5] Raport końcowy:")
    metrics = assistant.get_performance_metrics()
    print(f"   - Łącznie spraw: {metrics['total_cases']}")
    print(f"   - Łącznie analiz: {metrics['total_analyses']}")
    print(f"   - Średni czas analizy: {metrics['avg_analysis_time']:.2f}s")
    
    print("\n✅ Workflow zakończony pomyślnie!")

# ============================================================================
# GŁÓWNA FUNKCJA
# ============================================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════╗
║          💼 PRZYKŁADY UŻYCIA ASYSTENTA AI DLA ADMINISTRACJI     ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    # Uruchomienie wszystkich przykładów
    try:
        # Przykład 1
        assistant, case = example_basic_case_analysis()
        
        # Przykład 2
        if case:
            example_decision_generation(assistant, case.case_id)
        
        # Przykład 3
        example_deadline_monitoring(assistant)
        
        # Przykład 4
        example_batch_processing()
        
        # Przykład 5
        example_external_integration(assistant)
        
        # Przykład 6
        example_metrics_and_reports(assistant)
        
        # Przykład 7
        example_full_workflow()
        
        print("\n" + "="*70)
        print("✅ WSZYSTKIE PRZYKŁADY ZAKOŃCZONE POMYŚLNIE")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Błąd podczas wykonywania przykładów: {e}")
        import traceback
        traceback.print_exc()

