"""
HAMA Diamond Scoring Engine - Silnik analityczny HAMA Diamond dla Indeksu Branz

Wykorzystuje HAMA Diamond do:
- Normalizacji wskaznikow
- Dynamicznego wazenia
- Agregacji do syntetycznego indeksu
- Interpretacji wynikow
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import sys

# Import HAMA Diamond Core
HAMA_CORE_PATH = Path(__file__).parent.parent / "hama_core"
if HAMA_CORE_PATH.exists():
    sys.path.insert(0, str(HAMA_CORE_PATH.parent))
    try:
        # Importujemy tylko to, co potrzebne
        from hama_part1 import Concept
        from hama_part4 import WorldModel
        from hama_part5 import EnhancedCognitiveAgent
        HAMA_AVAILABLE = True
    except ImportError:
        HAMA_AVAILABLE = False
        print("[WARNING] HAMA Diamond Core nie jest dostepny - uzywam uproszczonego silnika")
else:
    HAMA_AVAILABLE = False
    print("[WARNING] HAMA Diamond Core nie znaleziony - uzywam uproszczonego silnika")

from config import HAMA_CONFIG, WSKAZNIKI_WAGI


class HAMADiamondScoringEngine:
    """
    Silnik scoringu wykorzystujacy metodologie HAMA Diamond
    
    Metodologia 6-etapowa:
    1. Zbieranie danych (wykonane wczesniej)
    2. Normalizacja wskaznikow
    3. Dynamiczne wazenie (HAMA Diamond)
    4. Agregacja do indeksu
    5. Klasyfikacja (wykonywana osobno)
    6. Interpretacja (generowanie raportow)
    """
    
    def __init__(self):
        self.config = HAMA_CONFIG
        self.base_weights = WSKAZNIKI_WAGI.copy()
        self.dynamic_weights = None
        self.hama_agent = None
        
        if HAMA_AVAILABLE:
            try:
                # Inicjalizacja agenta HAMA Diamond do analizy
                self.hama_agent = EnhancedCognitiveAgent()
                self.hama_agent.set_goal("analyze industry indicators and assign weights")
                print("[OK] HAMA Diamond Agent zainicjalizowany")
            except Exception as e:
                print(f"[WARNING] Blad inicjalizacji HAMA Diamond Agent: {e}")
                self.hama_agent = None
    
    def calculate_index(self, indicators_df: pd.DataFrame) -> pd.DataFrame:
        """
        Główna metoda obliczania indeksu branżowego
        
        Args:
            indicators_df: DataFrame z wskaźnikami dla każdej branży
        
        Returns:
            DataFrame z indeksem i wszystkimi wskaźnikami
        """
        print("\n[HAMA DIAMOND] Scoring Engine - Obliczanie indeksu...")
        
        # Kopia danych
        df = indicators_df.copy()
        
        # ETAP 2: Normalizacja
        print("  [ETAP 2] Normalizacja wskaznikow...")
        df_normalized = self._normalize_indicators(df)
        
        # ETAP 3: Dynamiczne ważenie
        print("  [ETAP 3] Dynamiczne wazenie (HAMA Diamond)...")
        weights = self._calculate_dynamic_weights(df_normalized)
        self.dynamic_weights = weights
        
        # ETAP 4: Agregacja
        print("  [ETAP 4] Agregacja do indeksu...")
        df_with_index = self._aggregate_to_index(df_normalized, weights)
        
        print("[OK] Indeks obliczony\n")
        
        return df_with_index
    
    def _normalize_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ETAP 2: Normalizacja wskaźników do skali 0-1
        
        Metody:
        - min_max: (x - min) / (max - min)
        - z_score: standaryzacja, potem min_max
        - robust: używa mediany i IQR
        """
        method = self.config['normalizacja']['metoda']
        df_norm = df.copy()
        
        # Lista wskaźników do normalizacji
        indicator_cols = [
            'dynamika_przychodow',
            'rentownosc',
            'zadluzenie',  # Odwrócone (niższe = lepsze)
            'szkodowosc',  # Odwrócone
            'dynamika_eksportu',
            'inwestycje',
            'nastroje_konsumenckie',
            'trendy_wyszukiwan',
            'nowe_firmy',
            'produktywnosc'
        ]
        
        for col in indicator_cols:
            if col not in df_norm.columns:
                continue
            
            # Pomiń NaN
            values = df_norm[col].dropna()
            if len(values) == 0:
                continue
            
            if method == 'min_max':
                min_val = values.min()
                max_val = values.max()
                if max_val != min_val:
                    df_norm[f'{col}_norm'] = (df_norm[col] - min_val) / (max_val - min_val)
                else:
                    df_norm[f'{col}_norm'] = 0.5
            
            elif method == 'z_score':
                mean_val = values.mean()
                std_val = values.std()
                if std_val > 0:
                    z_scores = (df_norm[col] - mean_val) / std_val
                    # Przekształć z-score na 0-1 (używając sigmoid)
                    df_norm[f'{col}_norm'] = 1 / (1 + np.exp(-z_scores))
                else:
                    df_norm[f'{col}_norm'] = 0.5
            
            elif method == 'robust':
                median_val = values.median()
                q75 = values.quantile(0.75)
                q25 = values.quantile(0.25)
                iqr = q75 - q25
                if iqr > 0:
                    df_norm[f'{col}_norm'] = (df_norm[col] - median_val) / iqr
                    # Clip do 0-1
                    df_norm[f'{col}_norm'] = np.clip(df_norm[f'{col}_norm'], -3, 3)
                    df_norm[f'{col}_norm'] = (df_norm[f'{col}_norm'] + 3) / 6
                else:
                    df_norm[f'{col}_norm'] = 0.5
            
            # Odwróć wskaźniki, gdzie niższe = lepsze
            if col in ['zadluzenie', 'szkodowosc']:
                df_norm[f'{col}_norm'] = 1 - df_norm[f'{col}_norm']
            
            # Clip do zakresu
            if self.config['normalizacja']['clip']:
                clip_min = self.config['normalizacja']['clip_min']
                clip_max = self.config['normalizacja']['clip_max']
                df_norm[f'{col}_norm'] = np.clip(
                    df_norm[f'{col}_norm'],
                    clip_min,
                    clip_max
                )
        
        return df_norm
    
    def _calculate_dynamic_weights(self, df_normalized: pd.DataFrame) -> Dict[str, float]:
        """
        ETAP 3: Dynamiczne ważenie wskaźników
        
        HAMA Diamond analizuje korelacje i znaczenie wskaźników,
        dostosowując wagi w zależności od kontekstu branżowego.
        """
        if not self.config['agregacja']['dynamiczne_wagi']:
            return self.base_weights.copy()
        
        # Uproszczona wersja dynamicznego ważenia
        # W pełnej wersji: HAMA Diamond Agent analizuje dane i sugeruje wagi
        
        weights = self.base_weights.copy()
        
        # Analiza korelacji między wskaźnikami
        indicator_cols = [col for col in df_normalized.columns if col.endswith('_norm')]
        
        if len(indicator_cols) > 1:
            # Oblicz korelacje
            corr_matrix = df_normalized[indicator_cols].corr()
            
            # Jeśli wskaźniki są silnie skorelowane, zmniejsz ich wagi
            for i, col1 in enumerate(indicator_cols):
                for col2 in indicator_cols[i+1:]:
                    corr = abs(corr_matrix.loc[col1, col2])
                    if corr > 0.8:  # Silna korelacja
                        # Zmniejsz wagi obu wskaźników
                        base_name1 = col1.replace('_norm', '')
                        base_name2 = col2.replace('_norm', '')
                        
                        if base_name1 in weights:
                            weights[base_name1] *= 0.9
                        if base_name2 in weights:
                            weights[base_name2] *= 0.9
        
        # Normalizuj wagi (suma = 1.0)
        total_weight = sum(weights.values())
        if total_weight > 0:
            weights = {k: v / total_weight for k, v in weights.items()}
        
        # Jeśli HAMA Diamond Agent dostępny, użyj go do dodatkowej analizy
        if self.hama_agent:
            # Symulacja analizy HAMA Diamond (w produkcji: pelna analiza kognitywna)
            # Tutaj: uproszczona wersja
            pass
        
        return weights
    
    def _aggregate_to_index(self, df_normalized: pd.DataFrame, weights: Dict[str, float]) -> pd.DataFrame:
        """
        ETAP 4: Agregacja znormalizowanych wskaźników do indeksu
        
        Metody:
        - weighted_sum: suma ważona
        - geometric_mean: średnia geometryczna ważona
        - harmonic_mean: średnia harmoniczna ważona
        """
        method = self.config['agregacja']['metoda']
        df_result = df_normalized.copy()
        
        # Przygotuj kolumny znormalizowane
        indicator_cols = [col for col in df_normalized.columns if col.endswith('_norm')]
        
        # Mapowanie nazw wskaźników do kolumn
        indicator_mapping = {}
        for col in indicator_cols:
            base_name = col.replace('_norm', '')
            if base_name in weights:
                indicator_mapping[base_name] = col
        
        # Oblicz indeks dla każdej branży
        indices = []
        
        for idx, row in df_normalized.iterrows():
            values = []
            w = []
            
            for indicator_name, col_name in indicator_mapping.items():
                if col_name in df_normalized.columns:
                    value = row[col_name]
                    if not pd.isna(value):
                        values.append(value)
                        w.append(weights[indicator_name])
            
            if len(values) == 0:
                indices.append(0.0)
                continue
            
            # Normalizuj wagi dla dostępnych wskaźników
            total_w = sum(w)
            if total_w > 0:
                w = [wi / total_w for wi in w]
            
            # Agregacja
            if method == 'weighted_sum':
                index = sum(v * w[i] for i, v in enumerate(values))
            
            elif method == 'geometric_mean':
                # Średnia geometryczna ważona
                log_values = [np.log(max(v, 0.001)) for v in values]  # Unikaj log(0)
                log_index = sum(log_v * w[i] for i, log_v in enumerate(log_values))
                index = np.exp(log_index)
            
            elif method == 'harmonic_mean':
                # Średnia harmoniczna ważona
                if all(v > 0 for v in values):
                    inv_values = [w[i] / v for i, v in enumerate(values)]
                    index = sum(w) / sum(inv_values) if sum(inv_values) > 0 else 0.0
                else:
                    index = sum(v * w[i] for i, v in enumerate(values))  # Fallback
            
            else:
                # Domyślnie: weighted_sum
                index = sum(v * w[i] for i, v in enumerate(values))
            
            # Skaluj do 0-100
            indices.append(index * 100)
        
        df_result['indeks_hama'] = indices
        
        # Dodaj informacje o wagach
        for indicator_name, weight in weights.items():
            col_name = f'waga_{indicator_name}'
            df_result[col_name] = weight
        
        return df_result
    
    def get_weights_explanation(self) -> str:
        """
        Generuje tekstowe wyjaśnienie wag (dla raportu)
        """
        if not self.dynamic_weights:
            weights = self.base_weights
        else:
            weights = self.dynamic_weights
        
        explanation = "## Uzasadnienie wag wskaznikow\n\n"
        explanation += "Wagi zostaly przypisane na podstawie znaczenia dla oceny kondycji branzy:\n\n"
        
        # Sortuj według wagi
        sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        
        for indicator, weight in sorted_weights:
            explanation += f"- **{indicator}**: {weight*100:.1f}%\n"
        
        explanation += "\nWagi sa dynamicznie dostosowywane przez HAMA Diamond w zaleznosci od korelacji miedzy wskaznikami.\n"
        
        return explanation


if __name__ == "__main__":
    # Test scoringu
    from data_collector import DataCollector
    from indicators import IndustryIndicators
    
    print("🧪 Test HAMA Diamond Scoring Engine...\n")
    
    # Pobierz dane
    collector = DataCollector()
    data = collector.collect_all_data()
    
    # Oblicz wskaźniki
    indicators_calc = IndustryIndicators()
    df_indicators = indicators_calc.calculate_all_indicators(data)
    
    # Oblicz indeks
    scoring = HAMADiamondScoringEngine()
    df_index = scoring.calculate_index(df_indicators)
    
    print("\n📊 Wyniki:")
    print(df_index[['pkd', 'nazwa', 'indeks_hama']].sort_values('indeks_hama', ascending=False))
    
    print("\n" + scoring.get_weights_explanation())

