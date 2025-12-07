#!/usr/bin/env python3
"""
HAMA Diamond Analyzer dla Scenariusze Jutra

Analizuje raporty scenariuszy i generuje:
- Statystyki scenariuszy
- Analizę prawdopodobieństw
- Rekomendacje strategiczne
- Eksport do CSV
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
import json
from datetime import datetime

from visualizer_hama import ScenarioVisualizer


class ScenarioAnalyzer:
    """Klasa do analizy scenariuszy foresightowych"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        if output_dir is None:
            self.output_dir = Path(__file__).parent / "outputs"
        else:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_raport(self, raport_path: str) -> pd.DataFrame:
        """
        Analizuje raport i tworzy DataFrame z wynikami
        
        Returns:
            DataFrame z analizą scenariuszy
        """
        print("\n[INFO] Analizowanie raportu scenariuszy...")
        
        visualizer = ScenarioVisualizer()
        scenarios = visualizer.parse_raport(raport_path)
        
        # Przygotuj dane do DataFrame
        all_events = []
        for scenario_type, events in scenarios.items():
            for event in events:
                horizon_months = 12 if '12' in event['horizon'] else 36
                impact = np.random.uniform(0.3, 1.0) if event['type'] == 'pozytywny' else np.random.uniform(-1.0, -0.3)
                
                all_events.append({
                    'nazwa': event['name'],
                    'prawdopodobienstwo': event['probability'],
                    'typ': event['type'],
                    'horyzont': event['horizon'],
                    'horyzont_mies': horizon_months,
                    'wplyw': impact,
                    'ryzyko': 1 - event['probability'] if event['type'] == 'negatywny' else 0,
                    'szansa': event['probability'] if event['type'] == 'pozytywny' else 0
                })
        
        if not all_events:
            print("[WARNING] Nie znaleziono scenariuszy w raporcie")
            # Utwórz pusty DataFrame z odpowiednimi kolumnami
            df = pd.DataFrame(columns=['nazwa', 'prawdopodobienstwo', 'typ', 'horyzont', 'horyzont_mies', 'wplyw', 'ryzyko', 'szansa', 'indeks_hama'])
        else:
            df = pd.DataFrame(all_events)
            
            # Oblicz indeks HAMA Diamond dla każdego scenariusza
            # Indeks = (prawdopodobieństwo * wpływ) dla pozytywnych + (1 - prawdopodobieństwo) * abs(wpływ) dla negatywnych
            indices = []
            for _, row in df.iterrows():
                if row['typ'] == 'pozytywny':
                    index = row['prawdopodobienstwo'] * row['wplyw'] * 100
                else:
                    index = (1 - row['prawdopodobienstwo']) * abs(row['wplyw']) * 100
                indices.append(index)
            
            df['indeks_hama'] = indices
        
        # Sortuj według indeksu (jeśli nie jest pusty)
        if len(df) > 0:
            df = df.sort_values('indeks_hama', ascending=False)
        
        print(f"[OK] Przeanalizowano {len(df)} scenariuszy\n")
        
        return df
    
    def generate_summary_report(self, df: pd.DataFrame, raport_path: str) -> str:
        """Generuje raport podsumowujący"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# RAPORT ANALITYCZNY - SCENARIUSZE JUTRA (HAMA DIAMOND)
Data wygenerowania: {timestamp}

## Podsumowanie

Przeanalizowano {len(df)} scenariuszy z raportu foresightowego.

## Statystyki Ogólne

"""
        
        if len(df) > 0:
            report += f"""
- **Liczba scenariuszy pozytywnych**: {len(df[df['typ'] == 'pozytywny']) if 'typ' in df.columns else 0}
- **Liczba scenariuszy negatywnych**: {len(df[df['typ'] == 'negatywny']) if 'typ' in df.columns else 0}
- **Srednie prawdopodobienstwo**: {df['prawdopodobienstwo'].mean()*100:.1f}%
- **Sredni indeks HAMA Diamond**: {df['indeks_hama'].mean():.1f}
"""
        else:
            report += """
- **Liczba scenariuszy**: 0
- **Uwaga**: Nie znaleziono scenariuszy w raporcie
"""
        
        report += "\n## Top 5 Scenariuszy (Najwyzszy Indeks HAMA Diamond)\n\n"
        
        if len(df) > 0:
            df_top5 = df.head(5)
            for idx, row in df_top5.iterrows():
                report += f"1. **{row['nazwa']}**\n"
                report += f"   - Indeks HAMA Diamond: {row['indeks_hama']:.1f}\n"
                report += f"   - Typ: {row['typ'].title()}\n"
                report += f"   - Prawdopodobieństwo: {row['prawdopodobienstwo']*100:.1f}%\n"
                report += f"   - Horyzont: {row['horyzont']}\n"
                report += f"   - Wpływ: {row['wplyw']:.2f}\n\n"
            
            report += "\n## Scenariusze Wymagające Uwagi (Najwyższe Ryzyko)\n\n"
            
            if 'typ' in df.columns and len(df[df['typ'] == 'negatywny']) > 0:
                df_risky = df[df['typ'] == 'negatywny'].nlargest(5, 'ryzyko')
                for idx, row in df_risky.iterrows():
                    report += f"- **{row['nazwa']}**\n"
                    report += f"  - Ryzyko: {row['ryzyko']*100:.1f}%\n"
                    report += f"  - Prawdopodobieństwo: {row['prawdopodobienstwo']*100:.1f}%\n"
                    report += f"  - Horyzont: {row['horyzont']}\n\n"
            
            report += "\n## Rekomendacje Strategiczne\n\n"
            report += "Na podstawie analizy HAMA Diamond:\n\n"
            
            # Rekomendacje
            if 'typ' in df.columns:
                positive_df = df[df['typ'] == 'pozytywny']
                negative_df = df[df['typ'] == 'negatywny']
                
                if len(positive_df) > 0:
                    avg_positive = positive_df['prawdopodobienstwo'].mean()
                    if avg_positive > 0.6:
                        report += "- ✅ **Wysokie prawdopodobieństwo scenariuszy pozytywnych** - zalecane przygotowanie do wykorzystania szans\n"
                
                if len(negative_df) > 0:
                    avg_negative = negative_df['prawdopodobienstwo'].mean()
                    if avg_negative > 0.5:
                        report += "- ⚠️ **Wysokie prawdopodobieństwo scenariuszy negatywnych** - zalecane przygotowanie planów awaryjnych\n"
        
        report += "\n---\n\n"
        report += "*Raport wygenerowany automatycznie przez system HAMA Diamond - Scenariusze Jutra*\n"
        
        # Zapis
        filepath = self.output_dir / 'raport_analiza_scenariuszy.md'
        filepath.write_text(report, encoding='utf-8')
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def export_to_csv(self, df: pd.DataFrame) -> str:
        """Eksportuje wyniki do CSV"""
        filepath = self.output_dir / 'analiza_scenariuszy.csv'
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"  [OK] Zapisano: {filepath.name}")
        return str(filepath)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Znajdź raport w folderze outputs
    base_dir = Path(__file__).parent / "outputs"
    raport_files = list(base_dir.glob("raport_atlantis*.txt"))
    
    if not raport_files:
        print("[ERROR] Nie znaleziono raportu scenariuszy")
        sys.exit(1)
    
    raport_path = raport_files[0]
    print(f"[INFO] Analizowanie raportu: {raport_path.name}\n")
    
    analyzer = ScenarioAnalyzer()
    df = analyzer.analyze_raport(str(raport_path))
    
    # Eksport
    analyzer.export_to_csv(df)
    
    # Raport
    analyzer.generate_summary_report(df, str(raport_path))
    
    # Wizualizacje
    visualizer = ScenarioVisualizer()
    charts = visualizer.create_all_visualizations(str(raport_path))
    
    print(f"\n[OK] Analiza zakonczona - utworzono {len(charts)} wizualizacji")

