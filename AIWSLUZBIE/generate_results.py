"""
🚀 Generator Wyników dla Asystenta AI
Generuje przykładowe wyniki bez wymagania pełnego LLM
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Dodaj ścieżkę do system/
_current_dir = os.path.dirname(os.path.abspath(__file__))
_system_dir = os.path.join(os.path.dirname(_current_dir), 'system')
if _system_dir not in sys.path:
    sys.path.insert(0, _system_dir)

# Utwórz folder outputs jeśli nie istnieje
outputs_dir = Path(_current_dir) / "outputs"
outputs_dir.mkdir(exist_ok=True)

print("="*70)
print("🏛️ GENERATOR WYNIKÓW - ASYSTENT AI DLA ADMINISTRACJI")
print("="*70)
print()

# Przykładowe sprawy
demo_cases = [
    {
        "case_id": "SPR-2024-001",
        "case_type": "kwalifikacja_zawodowa",
        "status": "w_trakcie",
        "parties": ["Jan Kowalski", "Departament Turystyki MSiT"],
        "deadline": (datetime.now() + timedelta(days=15)).isoformat(),
        "summary": "Wniosek o nadanie kwalifikacji przewodnika turystycznego",
        "risk_level": "niski",
        "compliance_score": 0.95,
        "legal_issues": ["Weryfikacja dyplomu", "Sprawdzenie doświadczenia"],
        "created_at": (datetime.now() - timedelta(days=5)).isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "case_id": "SPR-2024-002",
        "case_type": "licencja_turystyczna",
        "status": "do_weryfikacji",
        "parties": ["Firma ABC Sp. z o.o.", "MSiT"],
        "deadline": (datetime.now() + timedelta(days=7)).isoformat(),
        "summary": "Wniosek o wydanie licencji organizatora turystyki",
        "risk_level": "średni",
        "compliance_score": 0.85,
        "legal_issues": ["Weryfikacja kapitału", "Sprawdzenie ubezpieczenia"],
        "created_at": (datetime.now() - timedelta(days=10)).isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "case_id": "SPR-2024-003",
        "case_type": "kwalifikacja_zawodowa",
        "status": "zatwierdzona",
        "parties": ["Anna Nowak", "MSiT"],
        "deadline": (datetime.now() - timedelta(days=2)).isoformat(),
        "summary": "Wniosek o nadanie kwalifikacji pilota wycieczek",
        "risk_level": "niski",
        "compliance_score": 0.98,
        "legal_issues": [],
        "created_at": (datetime.now() - timedelta(days=20)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=2)).isoformat()
    },
    {
        "case_id": "SPR-2024-004",
        "case_type": "licencja_turystyczna",
        "status": "w_trakcie",
        "parties": ["XYZ Travel Sp. z o.o.", "MSiT"],
        "deadline": (datetime.now() + timedelta(days=3)).isoformat(),
        "summary": "Wniosek o przedłużenie licencji organizatora turystyki",
        "risk_level": "wysoki",
        "compliance_score": 0.72,
        "legal_issues": ["Brak aktualnego ubezpieczenia", "Niekompletna dokumentacja"],
        "created_at": (datetime.now() - timedelta(days=8)).isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "case_id": "SPR-2024-005",
        "case_type": "kwalifikacja_zawodowa",
        "status": "odrzucona",
        "parties": ["Piotr Wiśniewski", "MSiT"],
        "deadline": (datetime.now() - timedelta(days=5)).isoformat(),
        "summary": "Wniosek o nadanie kwalifikacji przewodnika górskiego",
        "risk_level": "średni",
        "compliance_score": 0.65,
        "legal_issues": ["Brak wymaganego doświadczenia", "Niekompletna dokumentacja"],
        "created_at": (datetime.now() - timedelta(days=30)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=5)).isoformat()
    }
]

# Statystyki
stats = {
    "total_cases": len(demo_cases),
    "cases_by_status": {
        "w_trakcie": len([c for c in demo_cases if c["status"] == "w_trakcie"]),
        "do_weryfikacji": len([c for c in demo_cases if c["status"] == "do_weryfikacji"]),
        "zatwierdzona": len([c for c in demo_cases if c["status"] == "zatwierdzona"]),
        "odrzucona": len([c for c in demo_cases if c["status"] == "odrzucona"])
    },
    "cases_by_type": {
        "kwalifikacja_zawodowa": len([c for c in demo_cases if c["case_type"] == "kwalifikacja_zawodowa"]),
        "licencja_turystyczna": len([c for c in demo_cases if c["case_type"] == "licencja_turystyczna"])
    },
    "cases_by_risk": {
        "niski": len([c for c in demo_cases if c["risk_level"] == "niski"]),
        "średni": len([c for c in demo_cases if c["risk_level"] == "średni"]),
        "wysoki": len([c for c in demo_cases if c["risk_level"] == "wysoki"]),
        "krytyczny": 0
    },
    "avg_compliance_score": sum(c["compliance_score"] for c in demo_cases) / len(demo_cases),
    "upcoming_deadlines": len([c for c in demo_cases if datetime.fromisoformat(c["deadline"]) > datetime.now()])
}

# Metryki wydajności
performance_metrics = {
    "total_cases": len(demo_cases),
    "total_analyses": 8,
    "avg_analysis_time": 2.5,
    "avg_decision_generation_time": 3.2
}

# Zapis wyników
results = {
    "timestamp": datetime.now().isoformat(),
    "cases": demo_cases,
    "statistics": stats,
    "performance_metrics": performance_metrics
}

# Zapis do JSON
output_file = outputs_dir / "wyniki_demo.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"✅ Wygenerowano {len(demo_cases)} spraw demo")
print(f"✅ Statystyki:")
print(f"   - Sprawy w trakcie: {stats['cases_by_status']['w_trakcie']}")
print(f"   - Sprawy do weryfikacji: {stats['cases_by_status']['do_weryfikacji']}")
print(f"   - Sprawy zatwierdzone: {stats['cases_by_status']['zatwierdzona']}")
print(f"   - Sprawy odrzucone: {stats['cases_by_status']['odrzucona']}")
print(f"   - Średni compliance score: {stats['avg_compliance_score']:.2f}")
print(f"   - Nadchodzące terminy: {stats['upcoming_deadlines']}")
print()
print(f"📁 Wyniki zapisane w: {output_file}")
print()

# Generowanie wizualizacji
print("📊 Generowanie wizualizacji...")
try:
    from visualizer_hama import AdministrativeCaseVisualizer
    
    # Przygotuj dane dla wizualizatora
    cases_for_viz = []
    for case in demo_cases:
        # Oblicz priorytet na podstawie deadline i compliance
        deadline_dt = datetime.fromisoformat(case["deadline"])
        days_left = (deadline_dt - datetime.now()).days
        priority = (1.0 / max(1, days_left)) * case["compliance_score"] * 100
        
        cases_for_viz.append({
            "case_id": case["case_id"],
            "nazwa": case["summary"],
            "priorytet": priority,
            "ryzyko": case["risk_level"],
            "compliance_score": case["compliance_score"],
            "status": case["status"],
            "case_type": case["case_type"],
            "days_left": days_left
        })
    
    visualizer = AdministrativeCaseVisualizer()
    charts = visualizer.create_visualizations_from_cases(cases_for_viz)
    
    print(f"✅ Wygenerowano {len(charts)} wizualizacji:")
    for chart_name, chart_path in charts.items():
        print(f"   - {chart_name}: {chart_path}")
    
except ImportError as e:
    print(f"⚠️ Nie można załadować visualizer: {e}")
    print("   Wizualizacje pominięte")
except Exception as e:
    print(f"⚠️ Błąd generowania wizualizacji: {e}")
    print("   Wizualizacje pominięte")

print()
print("="*70)
print("✅ GENEROWANIE ZAKOŃCZONE")
print("="*70)

