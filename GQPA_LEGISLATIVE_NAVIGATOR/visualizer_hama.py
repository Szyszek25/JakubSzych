"""
HAMA Diamond Visualizer dla Legislative Navigator

Tworzy wizualizacje dla analizy legislacyjnej:
- Wykresy wpływu przepisów
- Mapa relacji między aktami prawnymi
- Wykresy 3D (wpływ vs czas vs obszar)
- Heatmap korelacji
- HAMA Diamond Radar dla przepisów
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any

# Plotly import
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("[WARNING] Plotly nie jest zainstalowany - wizualizacje beda niedostepne")


class LegislativeVisualizer:
    """Klasa do tworzenia wizualizacji dla analizy legislacyjnej"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        if output_dir is None:
            self.output_dir = Path(__file__).parent / "outputs" / "wykresy"
        else:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_visualizations_from_data(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Tworzy wizualizacje z danych legislacyjnych
        
        Args:
            data: Dict z danymi (przepisy, wpływy, relacje)
        
        Returns:
            Dict z ścieżkami do plików HTML
        """
        if not PLOTLY_AVAILABLE:
            print("[WARNING] Plotly niedostepny - pomijam wizualizacje")
            return {}
        
        print("\n[INFO] Tworzenie wizualizacji legislacyjnych...")
        
        charts = {}
        
        # Jeśli dane są w formie DataFrame
        if isinstance(data, pd.DataFrame):
            charts['ranking_przepisow'] = self._create_regulations_ranking(data)
            charts['mapa_wplywow'] = self._create_impact_map(data)
            charts['wykres_3d'] = self._create_3d_impact_chart(data)
            charts['heatmap'] = self._create_correlation_heatmap(data)
            charts['hama_diamond_radar'] = self._create_hama_diamond_radar(data)
        
        print("[OK] Wizualizacje utworzone\n")
        
        return charts
    
    def _create_regulations_ranking(self, df: pd.DataFrame) -> str:
        """Tworzy ranking przepisów według wpływu"""
        if 'wplyw' not in df.columns:
            return ""
        
        df_sorted = df.sort_values('wplyw', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_sorted['wplyw'],
            y=df_sorted.get('nazwa', df_sorted.index),
            orientation='h',
            marker=dict(color='#3498db'),
            text=[f"{val:.2f}" for val in df_sorted['wplyw']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Wplyw: %{x:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Ranking Przepisow wedlug Wplywu - HAMA Diamond',
            xaxis_title='Wplyw',
            yaxis_title='Przepis',
            height=max(400, len(df) * 40),
            width=1200,
            showlegend=False,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'ranking_przepisow.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_impact_map(self, df: pd.DataFrame) -> str:
        """Tworzy mapę wpływu przepisów"""
        if 'wplyw' not in df.columns or 'czas' not in df.columns:
            return ""
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df.get('czas', range(len(df))),
            y=df['wplyw'],
            mode='markers+text',
            marker=dict(size=15, color='#e74c3c', line=dict(width=2, color='white')),
            text=df.get('nazwa', df.index),
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>Czas: %{x}<br>Wplyw: %{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Mapa Wplywu Przepisow',
            xaxis_title='Czas',
            yaxis_title='Wplyw',
            height=800,
            width=1200,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'mapa_wplywow.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_3d_impact_chart(self, df: pd.DataFrame) -> str:
        """Tworzy wykres 3D: wpływ vs czas vs obszar"""
        required_cols = ['wplyw']
        if not all(col in df.columns for col in required_cols):
            return ""
        
        # Symuluj brakujące kolumny
        if 'czas' not in df.columns:
            df['czas'] = range(len(df))
        if 'obszar' not in df.columns:
            df['obszar'] = np.random.uniform(0, 10, len(df))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter3d(
            x=df['czas'],
            y=df['wplyw'],
            z=df['obszar'],
            mode='markers+text',
            marker=dict(size=12, color='#3498db', opacity=0.8),
            text=df.get('nazwa', df.index),
            hovertemplate='<b>%{text}</b><br>Czas: %{x}<br>Wplyw: %{y:.2f}<br>Obszar: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Wykres 3D - Wplyw vs Czas vs Obszar',
            scene=dict(
                xaxis_title='Czas',
                yaxis_title='Wplyw',
                zaxis_title='Obszar',
                bgcolor='white'
            ),
            height=800,
            width=1200,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'wykres_3d_wplyw.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_correlation_heatmap(self, df: pd.DataFrame) -> str:
        """Tworzy heatmap korelacji między przepisami"""
        # Wybierz kolumny numeryczne
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            return ""
        
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=[str(col) for col in corr_matrix.columns],
            y=[str(col) for col in corr_matrix.index],
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            hovertemplate='%{y} vs %{x}<br>Korelacja: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Heatmap Korelacji Przepisow',
            height=700,
            width=900,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'heatmap_korelacji.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_hama_diamond_radar(self, df: pd.DataFrame) -> str:
        """Tworzy wykres radarowy HAMA Diamond dla przepisów"""
        # Wybierz top 5 przepisów
        if 'wplyw' not in df.columns:
            return ""
        
        df_top5 = df.nlargest(5, 'wplyw')
        
        # Wskaźniki do radaru
        indicators = ['wplyw', 'znaczenie', 'pilnosc', 'kompleksowosc', 'wpływ_społeczny']
        available_indicators = [ind for ind in indicators if ind in df.columns]
        
        if len(available_indicators) < 3:
            return ""
        
        fig = go.Figure()
        
        for idx, row in df_top5.iterrows():
            values = []
            for ind in available_indicators:
                val = row[ind]
                # Normalizuj do 0-100
                normalized = min(100, max(0, val * 10)) if val < 10 else min(100, val)
                values.append(normalized)
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=[ind.replace('_', ' ').title() for ind in available_indicators],
                fill='toself',
                name=row.get('nazwa', f"Przepis {idx}"),
                hovertemplate='<b>%{fullData.name}</b><br>%{theta}: %{r:.1f}<extra></extra>'
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
            title='HAMA Diamond Profile - Przepisy',
            height=800,
            width=1000,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'hama_diamond_radar_przepisy.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)


