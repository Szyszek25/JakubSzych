"""
🏷️ Klasyfikator Branż

Klasyfikuje branże do 5 kategorii:
1. Wzrostowe
2. Stabilne
3. Ryzykowne
4. Kurczące się
5. Wymagające finansowania
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from config import KATEGORIE_BRANZ


class IndustryClassifier:
    """Klasa do klasyfikacji branż"""
    
    def __init__(self):
        self.kategorie = KATEGORIE_BRANZ
    
    def classify_industries(self, df_with_index: pd.DataFrame) -> pd.DataFrame:
        """
        Klasyfikuje branże na podstawie indeksu HAMA Diamond i dodatkowych kryteriów
        
        Args:
            df_with_index: DataFrame z kolumna 'indeks_hama'
        
        Returns:
            DataFrame z kolumną 'kategoria'
        """
        print("\n[INFO] Klasyfikacja branz...")
        
        df = df_with_index.copy()
        df['kategoria'] = None
        df['kategoria_opis'] = None
        
        for idx, row in df.iterrows():
            indeks = row.get('indeks_hama', 0)
            
            # Podstawowa klasyfikacja na podstawie indeksu
            if indeks >= 70:
                kategoria = 'wzrostowe'
            elif indeks >= 50:
                kategoria = 'stabilne'
            elif indeks >= 30:
                kategoria = 'ryzykowne'
            else:
                kategoria = 'kurczace_sie'
            
            # Dodatkowa logika: "Wymagające finansowania"
            # Branże z potencjałem (średni indeks) ale wysokim zadłużeniem lub potrzebą inwestycji
            if 40 <= indeks <= 70:
                zadluzenie = row.get('zadluzenie', 0)
                inwestycje = row.get('inwestycje', 0)
                
                # Jeśli wysokie zadłużenie LUB wysokie inwestycje = potrzeba kapitału
                if zadluzenie > 1.2 or inwestycje > 15:
                    kategoria = 'wymagajace_finansowania'
            
            df.at[idx, 'kategoria'] = kategoria
            df.at[idx, 'kategoria_opis'] = self.kategorie[kategoria]['opis']
        
        # Statystyki klasyfikacji
        print("\n[STATS] Statystyki klasyfikacji:")
        category_counts = df['kategoria'].value_counts()
        for kategoria, count in category_counts.items():
            print(f"  {kategoria}: {count} branz")
        
        print("[OK] Klasyfikacja zakonczona\n")
        
        return df
    
    def get_category_summary(self, df_classified: pd.DataFrame) -> Dict[str, Dict]:
        """
        Zwraca podsumowanie dla każdej kategorii
        
        Returns:
            Dict z statystykami dla każdej kategorii
        """
        summary = {}
        
        for kategoria in self.kategorie.keys():
            df_cat = df_classified[df_classified['kategoria'] == kategoria]
            
            if len(df_cat) == 0:
                continue
            
            summary[kategoria] = {
                'liczba_branz': len(df_cat),
                'sredni_indeks': df_cat['indeks_hama'].mean(),
                'min_indeks': df_cat['indeks_hama'].min(),
                'max_indeks': df_cat['indeks_hama'].max(),
                'branze': df_cat[['pkd', 'nazwa', 'indeks_hama']].to_dict('records')
            }
        
        return summary


if __name__ == "__main__":
    # Test klasyfikacji
    from data_collector import DataCollector
    from indicators import IndustryIndicators
    from hama_scoring import HAMADiamondScoringEngine
    
    print("🧪 Test Industry Classifier...\n")
    
    # Pobierz dane i oblicz indeks
    collector = DataCollector()
    data = collector.collect_all_data()
    
    indicators_calc = IndustryIndicators()
    df_indicators = indicators_calc.calculate_all_indicators(data)
    
    scoring = HAMADiamondScoringEngine()
    df_index = scoring.calculate_index(df_indicators)
    
    # Klasyfikuj
    classifier = IndustryClassifier()
    df_classified = classifier.classify_industries(df_index)
    
    print("\n📊 Przykładowe wyniki klasyfikacji:")
    print(df_classified[['pkd', 'nazwa', 'indeks_hama', 'kategoria']].head(10))
    
    print("\n📈 Podsumowanie kategorii:")
    summary = classifier.get_category_summary(df_classified)
    for kategoria, stats in summary.items():
        print(f"\n{kategoria.upper()}:")
        print(f"  Liczba branż: {stats['liczba_branz']}")
        print(f"  Średni indeks: {stats['sredni_indeks']:.1f}")

