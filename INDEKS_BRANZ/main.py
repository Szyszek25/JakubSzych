#!/usr/bin/env python3
"""
HAMA Diamond - Indeks Branz - Glowny plik uruchomieniowy

Uruchamia pelna analize branz:
1. Pobieranie danych
2. Obliczanie wskaznikow
3. Scoring HAMA Diamond
4. Klasyfikacja
5. Wizualizacje
6. Generowanie raportow
7. Eksport do CSV
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

from data_collector import DataCollector
from indicators import IndustryIndicators
from hama_scoring import HAMADiamondScoringEngine
from classifier import IndustryClassifier
from visualizer import IndustryVisualizer
from report_generator import ReportGenerator

from config import OUTPUTS_DIR


def main():
    """Główna funkcja"""
    parser = argparse.ArgumentParser(description='HAMA Diamond-Indeks Branż')
    parser.add_argument('--full', action='store_true', 
                       help='Pełna analiza (pobieranie danych + scoring + raporty)')
    parser.add_argument('--scoring-only', action='store_true',
                       help='Tylko scoring (z istniejących danych)')
    parser.add_argument('--visualize-only', action='store_true',
                       help='Tylko wizualizacje (z istniejących danych)')
    parser.add_argument('--no-viz', action='store_true',
                       help='Pomiń wizualizacje')
    parser.add_argument('--no-reports', action='store_true',
                       help='Pomiń generowanie raportów')
    
    args = parser.parse_args()
    
    # Domyślnie: pełna analiza
    if not any([args.full, args.scoring_only, args.visualize_only]):
        args.full = True
    
    print("\n" + "="*70)
    print("HAMA DIAMOND - INDEKS BRANZ - SYSTEM ANALIZY KONDYCJI BRANZY")
    print("="*70 + "\n")
    
    # ETAP 1: Pobieranie danych
    if args.full:
        print("[ETAP 1] Pobieranie danych...")
        collector = DataCollector()
        data = collector.collect_all_data()
    else:
        # Załaduj istniejące dane
        collector = DataCollector()
        data = {}
        for source in ['gus', 'krs', 'trends', 'npk']:
            df = collector.load_raw_data(source)
            if df is not None:
                data[source] = df
        
        if not data:
            print("❌ Brak danych! Uruchom z --full aby pobrać dane.")
            sys.exit(1)
    
    # ETAP 2: Obliczanie wskaźników
    if args.full or args.scoring_only:
        print("\n[ETAP 2] Obliczanie wskaznikow branzowych...")
        indicators_calc = IndustryIndicators()
        df_indicators = indicators_calc.calculate_all_indicators(data)
    else:
        # Załaduj istniejące wskaźniki
        indicators_file = OUTPUTS_DIR / 'wskaźniki.csv'
        if indicators_file.exists():
            df_indicators = pd.read_csv(indicators_file, encoding='utf-8-sig')
        else:
            print("❌ Brak pliku wskaźników! Uruchom z --full lub --scoring-only.")
            sys.exit(1)
    
    # ETAP 3: Scoring HAMA Diamond
    if args.full or args.scoring_only:
        print("\n[ETAP 3] Scoring HAMA Diamond...")
        scoring = HAMADiamondScoringEngine()
        df_index = scoring.calculate_index(df_indicators)
        weights_explanation = scoring.get_weights_explanation()
    else:
        # Załaduj istniejący indeks
        index_file = OUTPUTS_DIR / 'indeks_branz.csv'
        if index_file.exists():
            df_index = pd.read_csv(index_file, encoding='utf-8-sig')
            weights_explanation = "Wagi zostały załadowane z poprzedniej analizy."
        else:
            print("❌ Brak pliku indeksu! Uruchom z --full lub --scoring-only.")
            sys.exit(1)
    
    # ETAP 4: Klasyfikacja
    if args.full or args.scoring_only:
        print("\n[ETAP 4] Klasyfikacja branz...")
        classifier = IndustryClassifier()
        df_classified = classifier.classify_industries(df_index)
    else:
        # Załaduj istniejącą klasyfikację
        index_file = OUTPUTS_DIR / 'indeks_branz.csv'
        if index_file.exists():
            df_classified = pd.read_csv(index_file, encoding='utf-8-sig')
        else:
            print("❌ Brak pliku klasyfikacji! Uruchom z --full lub --scoring-only.")
            sys.exit(1)
    
    # ETAP 5: Eksport do CSV
    if args.full or args.scoring_only:
        print("\n[ETAP 5] Eksport do CSV...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Przygotuj finalny DataFrame
        df_final = df_classified.copy()
        
        # Wybierz kolumny do eksportu
        export_cols = [
            'pkd', 'nazwa', 'indeks_hama', 'kategoria', 'kategoria_opis',
            'dynamika_przychodow', 'rentownosc', 'zadluzenie', 'szkodowosc',
            'dynamika_eksportu', 'inwestycje', 'nastroje_konsumenckie',
            'trendy_wyszukiwan', 'nowe_firmy', 'produktywnosc'
        ]
        
        # Dodaj kolumny wag jeśli istnieją
        weight_cols = [col for col in df_final.columns if col.startswith('waga_')]
        export_cols.extend(weight_cols)
        
        # Filtruj tylko istniejące kolumny
        export_cols = [col for col in export_cols if col in df_final.columns]
        
        df_export = df_final[export_cols].copy()
        
        # Sortuj według indeksu
        df_export = df_export.sort_values('indeks_hama', ascending=False)
        
        # Zapis
        csv_file = OUTPUTS_DIR / 'indeks_branz.csv'
        df_export.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"  [OK] Zapisano: {csv_file}")
        
        # Zapis również do Excel
        try:
            excel_file = OUTPUTS_DIR / 'indeks_branz.xlsx'
            df_export.to_excel(excel_file, index=False, engine='openpyxl')
            print(f"  [OK] Zapisano: {excel_file}")
        except Exception as e:
            print(f"  [WARNING] Nie udalo sie zapisac do Excel: {e}")
    
    # ETAP 6: Wizualizacje
    if not args.no_viz and (args.full or args.visualize_only):
        print("\n[ETAP 6] Tworzenie wizualizacji...")
        visualizer = IndustryVisualizer()
        charts = visualizer.create_all_visualizations(df_classified)
        print(f"  [OK] Utworzono {len(charts)} wizualizacji")
    
    # ETAP 7: Generowanie raportów
    if not args.no_reports and (args.full or args.scoring_only):
        print("\n[ETAP 7] Generowanie raportow...")
        if 'weights_explanation' not in locals():
            weights_explanation = "Wagi zostaly zaladowane z poprzedniej analizy."
        
        report_gen = ReportGenerator()
        reports = report_gen.generate_all_reports(df_classified, weights_explanation)
        print(f"  [OK] Wygenerowano {len(reports)} raportow")
    
    # Podsumowanie
    print("\n" + "="*70)
    print("[OK] ANALIZA ZAKONCZONA POMYSLNIE!")
    print("="*70)
    print(f"\n[INFO] Wyniki zapisane w: {OUTPUTS_DIR}")
    print(f"\n[TOP 5] Branze:")
    df_top5 = df_classified.nlargest(5, 'indeks_hama')
    for idx, row in df_top5.iterrows():
        print(f"  {row['nazwa']}: {row['indeks_hama']:.1f} ({row['kategoria']})")
    print("\n")


if __name__ == "__main__":
    main()

