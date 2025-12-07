"""
📊 Moduł wizualizacji wyników

Tworzy interaktywne wykresy:
- Ranking branż
- Mapa ryzyka
- Trendy czasowe
- Porównania sektorowe
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Optional

# Plotly import - opcjonalny
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # Dummy classes dla fallback
    class go:
        class Figure:
            def __init__(self): pass
            def add_trace(self, *args, **kwargs): pass
            def update_layout(self, *args, **kwargs): pass
            def write_html(self, *args, **kwargs): pass
        class Bar:
            def __init__(self, *args, **kwargs): pass
        class Scatter:
            def __init__(self, *args, **kwargs): pass
        class Scatterpolar:
            def __init__(self, *args, **kwargs): pass
        class Pie:
            def __init__(self, *args, **kwargs): pass

from config import CHARTS_DIR, VIZ_CONFIG, KATEGORIE_BRANZ


class IndustryVisualizer:
    """Klasa do tworzenia wizualizacji"""
    
    def __init__(self):
        self.charts_dir = CHARTS_DIR
        self.config = VIZ_CONFIG
        self.colors = VIZ_CONFIG['kolory']
    
    def create_all_visualizations(self, df_classified: pd.DataFrame) -> Dict[str, str]:
        """
        Tworzy wszystkie wizualizacje
        
        Returns:
            Dict z ścieżkami do plików HTML
        """
        if not PLOTLY_AVAILABLE:
            print("[WARNING] Plotly niedostepny - pomijam wizualizacje")
            return {}
        
        print("\n[INFO] Tworzenie wizualizacji...")
        
        charts = {}
        
        # 1. Ranking branż
        charts['ranking'] = self._create_ranking_chart(df_classified)
        
        # 2. Mapa ryzyka
        charts['mapa_ryzyka'] = self._create_risk_map(df_classified)
        
        # 3. Wykres kategorii
        charts['kategorie'] = self._create_categories_chart(df_classified)
        
        # 4. Porównanie wskaźników
        charts['porownanie_wskaznikow'] = self._create_indicators_comparison(df_classified)
        
        # 5. Wykres 3D - Indeks vs Zadłużenie vs Rentowność
        charts['wykres_3d'] = self._create_3d_chart(df_classified)
        
        # 6. Heatmap korelacji wskaźników
        charts['heatmap_korelacji'] = self._create_correlation_heatmap(df_classified)
        
        # 7. Wykres radarowy HAMA Diamond
        charts['hama_diamond_radar'] = self._create_hama_diamond_radar(df_classified)
        
        print("[OK] Wizualizacje utworzone\n")
        
        return charts
    
    def _create_ranking_chart(self, df: pd.DataFrame) -> str:
        """Tworzy wykres rankingowy branż"""
        df_sorted = df.sort_values('indeks_hama', ascending=True)
        
        # Kolory według kategorii
        colors_list = [self.colors.get(row['kategoria'], '#95a5a6') 
                      for _, row in df_sorted.iterrows()]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_sorted['indeks_hama'],
            y=df_sorted['nazwa'],
            orientation='h',
            marker=dict(color=colors_list),
            text=[f"{val:.1f}" for val in df_sorted['indeks_hama']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Indeks: %{x:.1f}<br>Kategoria: %{customdata}<extra></extra>',
            customdata=df_sorted['kategoria']
        ))
        
        fig.update_layout(
            title='Ranking Branz - Indeks HAMA Diamond',
            xaxis_title='Indeks HAMA Diamond (0-100)',
            yaxis_title='Branża',
            height=600,
            width=1200,
            showlegend=False,
            template='plotly_white'
        )
        
        filepath = self.charts_dir / 'ranking_branz.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_risk_map(self, df: pd.DataFrame) -> str:
        """Tworzy mapę ryzyka (2D scatter: indeks vs zadłużenie)"""
        fig = go.Figure()
        
        # Grupuj według kategorii
        for kategoria in df['kategoria'].unique():
            df_cat = df[df['kategoria'] == kategoria]
            
            fig.add_trace(go.Scatter(
                x=df_cat['indeks_hama'],
                y=df_cat.get('zadluzenie', 0),
                mode='markers+text',
                name=kategoria.replace('_', ' ').title(),
                marker=dict(
                    size=15,
                    color=self.colors.get(kategoria, '#95a5a6'),
                    line=dict(width=2, color='white')
                ),
                text=df_cat['nazwa'],
                textposition='top center',
                hovertemplate='<b>%{text}</b><br>Indeks: %{x:.1f}<br>Zadłużenie: %{y:.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Mapa Ryzyka Branz',
            xaxis_title='Indeks HAMA Diamond',
            yaxis_title='Wskaźnik Zadłużenia (D/E)',
            height=800,
            width=1200,
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        filepath = self.charts_dir / 'mapa_ryzyka.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_categories_chart(self, df: pd.DataFrame) -> str:
        """Tworzy wykres pokazujący rozkład kategorii"""
        category_counts = df['kategoria'].value_counts()
        
        colors_list = [self.colors.get(cat, '#95a5a6') for cat in category_counts.index]
        
        fig = go.Figure(data=[go.Pie(
            labels=[cat.replace('_', ' ').title() for cat in category_counts.index],
            values=category_counts.values,
            hole=0.4,
            marker=dict(colors=colors_list),
            textinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>Liczba branż: %{value}<br>Procent: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title='Rozklad Kategorii Branz',
            height=600,
            width=800,
            template='plotly_white'
        )
        
        filepath = self.charts_dir / 'kategorie_branz.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_indicators_comparison(self, df: pd.DataFrame) -> str:
        """Tworzy wykres porównujący wskaźniki dla top 5 branż"""
        df_top5 = df.nlargest(5, 'indeks_hama')
        
        # Wybierz wskaźniki do porównania
        indicator_cols = [
            'dynamika_przychodow',
            'rentownosc',
            'dynamika_eksportu',
            'inwestycje',
            'produktywnosc'
        ]
        
        # Normalizuj wskaźniki do 0-100 dla porównania
        fig = go.Figure()
        
        for idx, row in df_top5.iterrows():
            values = []
            for col in indicator_cols:
                if col in df.columns:
                    val = row[col]
                    if pd.notna(val):
                        # Normalizuj do 0-100 (uproszczone)
                        values.append(min(100, max(0, val)))
                    else:
                        values.append(0)
                else:
                    values.append(0)
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=[col.replace('_', ' ').title() for col in indicator_cols],
                fill='toself',
                name=row['nazwa'],
                hovertemplate='<b>%{fullData.name}</b><br>%{theta}: %{r:.1f}<extra></extra>'
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title='Porownanie Wskaznikow - Top 5 Branz',
            height=800,
            width=1000,
            template='plotly_white'
        )
        
        filepath = self.charts_dir / 'porownanie_wskaznikow.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_3d_chart(self, df: pd.DataFrame) -> str:
        """Tworzy wykres 3D: Indeks vs Zadłużenie vs Rentowność"""
        fig = go.Figure()
        
        # Grupuj według kategorii
        for kategoria in df['kategoria'].unique():
            df_cat = df[df['kategoria'] == kategoria]
            
            fig.add_trace(go.Scatter3d(
                x=df_cat['indeks_hama'],
                y=df_cat.get('zadluzenie', 0),
                z=df_cat.get('rentownosc', 0),
                mode='markers+text',
                name=kategoria.replace('_', ' ').title(),
                marker=dict(
                    size=12,
                    color=self.colors.get(kategoria, '#95a5a6'),
                    opacity=0.8,
                    line=dict(width=1, color='white')
                ),
                text=df_cat['nazwa'],
                hovertemplate='<b>%{text}</b><br>Indeks: %{x:.1f}<br>Zadluzenie: %{y:.2f}<br>Rentownosc: %{z:.1f}%<extra></extra>'
            ))
        
        fig.update_layout(
            title='Wykres 3D - Indeks HAMA Diamond vs Zadluzenie vs Rentownosc',
            scene=dict(
                xaxis_title='Indeks HAMA Diamond',
                yaxis_title='Zadluzenie (D/E)',
                zaxis_title='Rentownosc (%)',
                bgcolor='white'
            ),
            height=800,
            width=1200,
            template='plotly_white'
        )
        
        filepath = self.charts_dir / 'wykres_3d.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_correlation_heatmap(self, df: pd.DataFrame) -> str:
        """Tworzy heatmap korelacji między wskaźnikami"""
        # Wybierz wskaźniki numeryczne
        indicator_cols = [
            'indeks_hama',
            'dynamika_przychodow',
            'rentownosc',
            'zadluzenie',
            'szkodowosc',
            'dynamika_eksportu',
            'inwestycje',
            'produktywnosc'
        ]
        
        # Filtruj tylko istniejące kolumny
        available_cols = [col for col in indicator_cols if col in df.columns]
        
        if len(available_cols) < 2:
            return ""
        
        # Oblicz korelację
        corr_matrix = df[available_cols].corr()
        
        # Utwórz heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=[col.replace('_', ' ').title() for col in corr_matrix.columns],
            y=[col.replace('_', ' ').title() for col in corr_matrix.index],
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='%{y} vs %{x}<br>Korelacja: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Heatmap Korelacji Wskaznikow',
            height=700,
            width=900,
            template='plotly_white'
        )
        
        filepath = self.charts_dir / 'heatmap_korelacji.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_hama_diamond_radar(self, df: pd.DataFrame) -> str:
        """Tworzy wykres radarowy HAMA Diamond Profile"""
        # Wybierz top 5 branż
        df_top5 = df.nlargest(5, 'indeks_hama')
        
        # Wskaźniki do radaru (5 kluczowych)
        indicators = {
            'Dynamika\nPrzychodow': 'dynamika_przychodow',
            'Rentownosc': 'rentownosc',
            'Eksport': 'dynamika_eksportu',
            'Inwestycje': 'inwestycje',
            'Produktywnosc': 'produktywnosc'
        }
        
        fig = go.Figure()
        
        for idx, row in df_top5.iterrows():
            values = []
            theta = []
            
            for label, col in indicators.items():
                if col in df.columns:
                    val = row[col]
                    if pd.notna(val):
                        # Normalizuj do 0-100
                        # Dla każdego wskaźnika osobno
                        if col == 'dynamika_przychodow':
                            normalized = min(100, max(0, (val + 20) * 2))  # -20% do 30% -> 0-100
                        elif col == 'rentownosc':
                            normalized = min(100, max(0, val * 6.67))  # 0-15% -> 0-100
                        elif col == 'dynamika_eksportu':
                            normalized = min(100, max(0, (val + 20) * 2))
                        elif col == 'inwestycje':
                            normalized = min(100, max(0, (val + 20) * 2))
                        elif col == 'produktywnosc':
                            normalized = min(100, max(0, val / 10))  # 0-1000 -> 0-100
                        else:
                            normalized = min(100, max(0, val))
                        values.append(normalized)
                    else:
                        values.append(50)  # Średnia
                else:
                    values.append(50)
                theta.append(label)
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=theta,
                fill='toself',
                name=row['nazwa'],
                line=dict(color=self.colors.get(row['kategoria'], '#95a5a6'), width=2),
                hovertemplate='<b>%{fullData.name}</b><br>%{theta}: %{r:.1f}<extra></extra>'
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    tickfont=dict(size=11)
                )
            ),
            showlegend=True,
            title='HAMA Diamond Profile - Top 5 Branz',
            height=800,
            width=1000,
            template='plotly_white',
            legend=dict(
                orientation='v',
                yanchor='top',
                y=1,
                xanchor='left',
                x=1.05
            )
        )
        
        filepath = self.charts_dir / 'hama_diamond_radar.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)


if __name__ == "__main__":
    # Test wizualizacji
    from data_collector import DataCollector
    from indicators import IndustryIndicators
    from hama_scoring import HAMADiamondScoringEngine
    from classifier import IndustryClassifier
    
    print("🧪 Test Industry Visualizer...\n")
    
    # Przygotuj dane
    collector = DataCollector()
    data = collector.collect_all_data()
    
    indicators_calc = IndustryIndicators()
    df_indicators = indicators_calc.calculate_all_indicators(data)
    
    scoring = HAMADiamondScoringEngine()
    df_index = scoring.calculate_index(df_indicators)
    
    classifier = IndustryClassifier()
    df_classified = classifier.classify_industries(df_index)
    
    # Twórz wizualizacje
    visualizer = IndustryVisualizer()
    charts = visualizer.create_all_visualizations(df_classified)
    
    print(f"\n✅ Utworzono {len(charts)} wizualizacji")

