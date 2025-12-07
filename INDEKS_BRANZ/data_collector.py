"""
📥 Moduł pobierania danych dla HAMA Diamond-Indeks Branż

Pobiera dane z różnych źródeł:
- GUS (stat.gov.pl)
- KRS (ekrs.ms.gov.pl)
- Google Trends (pytrends)
- NBP (nastroje konsumenckie)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import requests
from datetime import datetime, timedelta
import time
import json

try:
    from pytrends.request import TrendReq
    PTRENDS_AVAILABLE = True
except ImportError:
    PTRENDS_AVAILABLE = False
    print("[WARNING] pytrends nie jest zainstalowany - Google Trends bedzie niedostepne")

from config import RAW_DATA_DIR, BRANZE_PKD, ZRODLA_DANYCH


class DataCollector:
    """Klasa do pobierania danych z różnych źródeł"""
    
    def __init__(self):
        self.raw_data_dir = RAW_DATA_DIR
        self.branze = BRANZE_PKD
        self.pytrends = None
        
        if PTRENDS_AVAILABLE:
            try:
                self.pytrends = TrendReq(hl='pl-PL', tz=360)
            except Exception as e:
                print(f"⚠️ Nie udało się zainicjalizować pytrends: {e}")
    
    def collect_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Pobiera wszystkie dostępne dane
        
        Returns:
            Dict z DataFrame dla każdego źródła
        """
        print("\n[INFO] Rozpoczynam zbieranie danych...")
        
        data = {}
        
        # 1. Dane GUS (symulowane - w produkcji podpinamy API lub pliki CSV)
        print("  [GUS] Pobieranie danych GUS...")
        data['gus'] = self._collect_gus_data()
        
        # 2. Dane KRS (symulowane)
        print("  [KRS] Pobieranie danych KRS...")
        data['krs'] = self._collect_krs_data()
        
        # 3. Google Trends
        if self.pytrends:
            print("  [INFO] Pobieranie Google Trends...")
            data['trends'] = self._collect_google_trends()
        else:
            print("  [WARNING] Google Trends pominiete (brak pytrends)")
            data['trends'] = pd.DataFrame()
        
        # 4. Nastroje konsumenckie (NBP)
        print("  [NBP] Pobieranie nastrojow konsumenckich...")
        data['npk'] = self._collect_npk_data()
        
        # Zapis surowych danych
        self._save_raw_data(data)
        
        print("[OK] Zbieranie danych zakonczone\n")
        return data
    
    def _collect_gus_data(self) -> pd.DataFrame:
        """
        Pobiera dane z GUS (stat.gov.pl)
        
        W produkcji: podpinamy API GUS lub pobieramy pliki CSV
        Tutaj: generujemy przykładowe dane
        """
        # Symulowane dane GUS
        branze_list = list(self.branze.keys())
        data = []
        
        for pkd in branze_list:
            # Symulacja danych dla każdej branży
            data.append({
                'pkd': pkd,
                'nazwa': self.branze[pkd]['nazwa'],
                'przychody_2023': np.random.uniform(50, 500) * 1e9,  # w PLN
                'przychody_2022': np.random.uniform(45, 480) * 1e9,
                'przychody_2021': np.random.uniform(40, 460) * 1e9,
                'eksport_2023': np.random.uniform(10, 200) * 1e9,
                'eksport_2022': np.random.uniform(9, 190) * 1e9,
                'zatrudnienie_2023': np.random.randint(100000, 2000000),
                'zatrudnienie_2022': np.random.randint(95000, 1950000),
                'inwestycje_2023': np.random.uniform(5, 50) * 1e9,
                'inwestycje_2022': np.random.uniform(4, 48) * 1e9,
            })
        
        df = pd.DataFrame(data)
        return df
    
    def _collect_krs_data(self) -> pd.DataFrame:
        """
        Pobiera dane z KRS (ekrs.ms.gov.pl)
        
        W produkcji: podpinamy API KRS lub pobieramy pliki CSV
        """
        branze_list = list(self.branze.keys())
        data = []
        
        for pkd in branze_list:
            # Symulacja danych KRS
            data.append({
                'pkd': pkd,
                'nazwa': self.branze[pkd]['nazwa'],
                'nowe_firmy_2023': np.random.randint(500, 5000),
                'nowe_firmy_2022': np.random.randint(450, 4800),
                'upadlosci_2023': np.random.randint(10, 200),
                'upadlosci_2022': np.random.randint(8, 180),
                'liczba_podmiotow_2023': np.random.randint(10000, 200000),
                'liczba_podmiotow_2022': np.random.randint(9500, 195000),
            })
        
        df = pd.DataFrame(data)
        return df
    
    def _collect_google_trends(self) -> pd.DataFrame:
        """
        Pobiera dane z Google Trends
        
        Wymaga: pytrends
        """
        if not self.pytrends:
            return pd.DataFrame()
        
        branze_list = list(self.branze.keys())
        data = []
        
        # Google Trends ma limity - pobieramy pojedynczo z opóźnieniami
        for pkd in branze_list:
            nazwa = self.branze[pkd]['nazwa']
            
            try:
                # Pobierz trendy dla nazwy branży
                keywords = [nazwa]
                self.pytrends.build_payload(keywords, cat=0, timeframe='today 12-m', geo='PL')
                
                trends_data = self.pytrends.interest_over_time()
                
                if not trends_data.empty:
                    avg_trend = trends_data[keywords[0]].mean()
                else:
                    avg_trend = np.random.uniform(20, 80)  # Fallback
                
                data.append({
                    'pkd': pkd,
                    'nazwa': nazwa,
                    'trend_wyszukiwan': avg_trend
                })
                
                # Opóźnienie aby uniknąć rate limitów
                time.sleep(1)
                
            except Exception as e:
                print(f"    [WARNING] Blad dla {nazwa}: {e}")
                # Fallback - losowa wartość
                data.append({
                    'pkd': pkd,
                    'nazwa': nazwa,
                    'trend_wyszukiwan': np.random.uniform(20, 80)
                })
        
        df = pd.DataFrame(data)
        return df
    
    def _collect_npk_data(self) -> pd.DataFrame:
        """
        Pobiera dane o nastrojach konsumenckich (NBP)
        
        W produkcji: podpinamy API NBP lub pobieramy pliki CSV
        """
        # Symulowane dane NPK
        # W rzeczywistości: pobieramy z https://www.nbp.pl
        data = {
            'data': datetime.now().strftime('%Y-%m-%d'),
            'indeks_nastrojow': np.random.uniform(80, 120),  # 100 = neutralne
            'oczekiwania': np.random.uniform(75, 125),
            'sytuacja_biezaca': np.random.uniform(85, 115)
        }
        
        # Dla każdej branży przypisujemy podobny poziom (z małymi wariacjami)
        branze_list = list(self.branze.keys())
        df_data = []
        
        for pkd in branze_list:
            df_data.append({
                'pkd': pkd,
                'nazwa': self.branze[pkd]['nazwa'],
                'indeks_nastrojow': data['indeks_nastrojow'] + np.random.uniform(-10, 10),
                'oczekiwania': data['oczekiwania'] + np.random.uniform(-10, 10),
                'sytuacja_biezaca': data['sytuacja_biezaca'] + np.random.uniform(-10, 10)
            })
        
        df = pd.DataFrame(df_data)
        return df
    
    def _save_raw_data(self, data: Dict[str, pd.DataFrame]):
        """Zapisuje surowe dane do plików CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for source_name, df in data.items():
            if not df.empty:
                filepath = self.raw_data_dir / f"{source_name}_{timestamp}.csv"
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
                print(f"    [OK] Zapisano: {filepath.name}")
    
    def load_raw_data(self, source: str) -> Optional[pd.DataFrame]:
        """
        Ładuje ostatnie surowe dane dla danego źródła
        
        Args:
            source: nazwa źródła (gus, krs, trends, npk)
        
        Returns:
            DataFrame lub None
        """
        files = list(self.raw_data_dir.glob(f"{source}_*.csv"))
        if not files:
            return None
        
        # Najnowszy plik
        latest_file = max(files, key=lambda p: p.stat().st_mtime)
        return pd.read_csv(latest_file, encoding='utf-8-sig')


if __name__ == "__main__":
    # Test pobierania danych
    collector = DataCollector()
    data = collector.collect_all_data()
    
    print("\n📊 Podsumowanie pobranych danych:")
    for source, df in data.items():
        print(f"  {source}: {len(df)} rekordów")
        if not df.empty:
            print(f"    Kolumny: {', '.join(df.columns)}")

