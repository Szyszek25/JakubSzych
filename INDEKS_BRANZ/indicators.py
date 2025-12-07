"""
📊 Moduł wskaźników branżowych

Definiuje i oblicza wskaźniki dla każdej branży:
1. Dynamika przychodów
2. Rentowność
3. Zadłużenie
4. Szkodowość
5. Dynamika eksportu
6. Inwestycje
7. Nastroje konsumenckie
8. Trendy wyszukiwań
9. Nowe firmy
10. Produktywność
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from config import BRANZE_PKD


class IndustryIndicators:
    """Klasa do obliczania wskaźników branżowych"""
    
    def __init__(self):
        self.branze = BRANZE_PKD
    
    def calculate_all_indicators(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Oblicza wszystkie wskaźniki dla wszystkich branż
        
        Args:
            data: Dict z DataFrame dla każdego źródła (gus, krs, trends, npk)
        
        Returns:
            DataFrame z wskaźnikami dla każdej branży
        """
        print("\n[INFO] Obliczanie wskaznikow branzowych...")
        
        # Przygotuj dane
        gus_df = data.get('gus', pd.DataFrame())
        krs_df = data.get('krs', pd.DataFrame())
        trends_df = data.get('trends', pd.DataFrame())
        npk_df = data.get('npk', pd.DataFrame())
        
        # Zbuduj wynikowy DataFrame
        results = []
        
        for pkd in self.branze.keys():
            indicators = {
                'pkd': pkd,
                'nazwa': self.branze[pkd]['nazwa']
            }
            
            # 1. Dynamika przychodów (YoY %)
            indicators['dynamika_przychodow'] = self._calculate_revenue_growth(gus_df, pkd)
            
            # 2. Rentowność (marża zysku - symulowana)
            indicators['rentownosc'] = self._calculate_profitability(gus_df, pkd)
            
            # 3. Zadłużenie (D/E ratio - symulowane)
            indicators['zadluzenie'] = self._calculate_debt_ratio(gus_df, pkd)
            
            # 4. Szkodowość (% upadłości)
            indicators['szkodowosc'] = self._calculate_failure_rate(krs_df, pkd)
            
            # 5. Dynamika eksportu (YoY %)
            indicators['dynamika_eksportu'] = self._calculate_export_growth(gus_df, pkd)
            
            # 6. Inwestycje (dynamika CAPEX)
            indicators['inwestycje'] = self._calculate_investment_growth(gus_df, pkd)
            
            # 7. Nastroje konsumenckie (indeks)
            indicators['nastroje_konsumenckie'] = self._calculate_consumer_sentiment(npk_df, pkd)
            
            # 8. Trendy wyszukiwań (Google Trends)
            indicators['trendy_wyszukiwan'] = self._calculate_search_trends(trends_df, pkd)
            
            # 9. Nowe firmy (dynamika)
            indicators['nowe_firmy'] = self._calculate_new_companies_growth(krs_df, pkd)
            
            # 10. Produktywność (przychód/etat)
            indicators['produktywnosc'] = self._calculate_productivity(gus_df, pkd)
            
            results.append(indicators)
        
        df = pd.DataFrame(results)
        print(f"[OK] Obliczono wskazniki dla {len(df)} branz\n")
        
        return df
    
    def _calculate_revenue_growth(self, gus_df: pd.DataFrame, pkd: str) -> float:
        """Oblicza dynamikę przychodów YoY (%)"""
        if gus_df.empty or pkd not in gus_df['pkd'].values:
            return np.nan
        
        row = gus_df[gus_df['pkd'] == pkd].iloc[0]
        
        if pd.isna(row.get('przychody_2023')) or pd.isna(row.get('przychody_2022')):
            return np.nan
        
        if row['przychody_2022'] == 0:
            return 0.0
        
        growth = ((row['przychody_2023'] - row['przychody_2022']) / row['przychody_2022']) * 100
        return growth
    
    def _calculate_profitability(self, gus_df: pd.DataFrame, pkd: str) -> float:
        """
        Oblicza rentowność (marża zysku %)
        
        W produkcji: zysk_netto / przychody * 100
        Tutaj: symulujemy na podstawie przychodów
        """
        if gus_df.empty or pkd not in gus_df['pkd'].values:
            return np.nan
        
        row = gus_df[gus_df['pkd'] == pkd].iloc[0]
        
        if pd.isna(row.get('przychody_2023')):
            return np.nan
        
        # Symulacja: większe branże mają niższą marżę (konkurencja)
        # Zakres: 2-15%
        base_margin = 8.0
        size_factor = min(row['przychody_2023'] / 1e12, 1.0)  # Normalizacja
        margin = base_margin * (1 - size_factor * 0.5) + np.random.uniform(-2, 2)
        
        return max(2.0, min(15.0, margin))
    
    def _calculate_debt_ratio(self, gus_df: pd.DataFrame, pkd: str) -> float:
        """
        Oblicza wskaźnik zadłużenia (D/E)
        
        W produkcji: dług / kapitał własny
        Tutaj: symulujemy
        """
        if gus_df.empty or pkd not in gus_df['pkd'].values:
            return np.nan
        
        # Symulacja: zakres 0.3-2.5 (zdrowe: <1.0, ryzykowne: >1.5)
        debt_ratio = np.random.uniform(0.3, 2.5)
        return debt_ratio
    
    def _calculate_failure_rate(self, krs_df: pd.DataFrame, pkd: str) -> float:
        """Oblicza szkodowość (% upadłości)"""
        if krs_df.empty or pkd not in krs_df['pkd'].values:
            return np.nan
        
        row = krs_df[krs_df['pkd'] == pkd].iloc[0]
        
        if pd.isna(row.get('upadlosci_2023')) or pd.isna(row.get('liczba_podmiotow_2023')):
            return np.nan
        
        if row['liczba_podmiotow_2023'] == 0:
            return 0.0
        
        failure_rate = (row['upadlosci_2023'] / row['liczba_podmiotow_2023']) * 100
        return failure_rate
    
    def _calculate_export_growth(self, gus_df: pd.DataFrame, pkd: str) -> float:
        """Oblicza dynamikę eksportu YoY (%)"""
        if gus_df.empty or pkd not in gus_df['pkd'].values:
            return np.nan
        
        row = gus_df[gus_df['pkd'] == pkd].iloc[0]
        
        if pd.isna(row.get('eksport_2023')) or pd.isna(row.get('eksport_2022')):
            return np.nan
        
        if row['eksport_2022'] == 0:
            return 0.0
        
        growth = ((row['eksport_2023'] - row['eksport_2022']) / row['eksport_2022']) * 100
        return growth
    
    def _calculate_investment_growth(self, gus_df: pd.DataFrame, pkd: str) -> float:
        """Oblicza dynamikę inwestycji YoY (%)"""
        if gus_df.empty or pkd not in gus_df['pkd'].values:
            return np.nan
        
        row = gus_df[gus_df['pkd'] == pkd].iloc[0]
        
        if pd.isna(row.get('inwestycje_2023')) or pd.isna(row.get('inwestycje_2022')):
            return np.nan
        
        if row['inwestycje_2022'] == 0:
            return 0.0
        
        growth = ((row['inwestycje_2023'] - row['inwestycje_2022']) / row['inwestycje_2022']) * 100
        return growth
    
    def _calculate_consumer_sentiment(self, npk_df: pd.DataFrame, pkd: str) -> float:
        """
        Oblicza wskaźnik nastrojów konsumenckich
        
        Skala: 0-200 (100 = neutralne)
        """
        if npk_df.empty or pkd not in npk_df['pkd'].values:
            return 100.0  # Neutralne
        
        row = npk_df[npk_df['pkd'] == pkd].iloc[0]
        return row.get('indeks_nastrojow', 100.0)
    
    def _calculate_search_trends(self, trends_df: pd.DataFrame, pkd: str) -> float:
        """
        Oblicza wskaźnik trendów wyszukiwań (Google Trends)
        
        Skala: 0-100 (50 = średnie)
        """
        if trends_df.empty or pkd not in trends_df['pkd'].values:
            return 50.0  # Średnie
        
        row = trends_df[trends_df['pkd'] == pkd].iloc[0]
        return row.get('trend_wyszukiwan', 50.0)
    
    def _calculate_new_companies_growth(self, krs_df: pd.DataFrame, pkd: str) -> float:
        """Oblicza dynamikę liczby nowych firm YoY (%)"""
        if krs_df.empty or pkd not in krs_df['pkd'].values:
            return np.nan
        
        row = krs_df[krs_df['pkd'] == pkd].iloc[0]
        
        if pd.isna(row.get('nowe_firmy_2023')) or pd.isna(row.get('nowe_firmy_2022')):
            return np.nan
        
        if row['nowe_firmy_2022'] == 0:
            return 0.0
        
        growth = ((row['nowe_firmy_2023'] - row['nowe_firmy_2022']) / row['nowe_firmy_2022']) * 100
        return growth
    
    def _calculate_productivity(self, gus_df: pd.DataFrame, pkd: str) -> float:
        """
        Oblicza produktywność (przychód na etat w tys. PLN)
        """
        if gus_df.empty or pkd not in gus_df['pkd'].values:
            return np.nan
        
        row = gus_df[gus_df['pkd'] == pkd].iloc[0]
        
        if pd.isna(row.get('przychody_2023')) or pd.isna(row.get('zatrudnienie_2023')):
            return np.nan
        
        if row['zatrudnienie_2023'] == 0:
            return 0.0
        
        productivity = (row['przychody_2023'] / row['zatrudnienie_2023']) / 1000  # w tys. PLN
        return productivity


if __name__ == "__main__":
    # Test obliczania wskaźników
    from data_collector import DataCollector
    
    collector = DataCollector()
    data = collector.collect_all_data()
    
    indicators = IndustryIndicators()
    df_indicators = indicators.calculate_all_indicators(data)
    
    print("\n📊 Przykładowe wskaźniki:")
    print(df_indicators.head())

