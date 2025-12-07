"""
HAMA Diamond Visualizer dla AI w Służbie

Tworzy wizualizacje dla analizy spraw administracyjnych:
- Wykresy priorytetów spraw
- Mapa ryzyka prawnego
- Wykresy 3D (priorytet vs ryzyko vs czas)
- Heatmap korelacji
- HAMA Diamond Radar dla spraw
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


class AdministrativeCaseVisualizer:
    """Klasa do tworzenia wizualizacji dla spraw administracyjnych"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        if output_dir is None:
            self.output_dir = Path(__file__).parent / "outputs" / "wykresy"
        else:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_visualizations_from_cases(self, cases_data: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Tworzy wizualizacje z danych spraw
        
        Args:
            cases_data: Lista dict ze sprawami
        
        Returns:
            Dict z ścieżkami do plików HTML
        """
        if not PLOTLY_AVAILABLE:
            print("[WARNING] Plotly niedostepny - pomijam wizualizacje")
            return {}
        
        print("\n[INFO] Tworzenie wizualizacji spraw administracyjnych...")
        
        # Konwertuj na DataFrame
        df = pd.DataFrame(cases_data)
        
        charts = {}
        
        if len(df) > 0:
            charts['ranking_spraw'] = self._create_cases_ranking(df)
            charts['mapa_ryzyka'] = self._create_risk_map(df)
            charts['wykres_3d'] = self._create_3d_risk_chart(df)
            charts['heatmap'] = self._create_correlation_heatmap(df)
            charts['hama_diamond_radar'] = self._create_hama_diamond_radar(df)
        
        print("[OK] Wizualizacje utworzone\n")
        
        return charts
    
    def _create_cases_ranking(self, df: pd.DataFrame) -> str:
        """Tworzy ranking spraw według priorytetu"""
        if 'priorytet' not in df.columns:
            return ""
        
        df_sorted = df.sort_values('priorytet', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_sorted['priorytet'],
            y=df_sorted.get('nazwa', df_sorted.index),
            orientation='h',
            marker=dict(color='#9b59b6'),
            text=[f"{val:.1f}" for val in df_sorted['priorytet']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Priorytet: %{x:.1f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Ranking Spraw Administracyjnych - HAMA Diamond',
            xaxis_title='Priorytet',
            yaxis_title='Sprawa',
            height=max(400, len(df) * 40),
            width=1200,
            showlegend=False,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'ranking_spraw.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_risk_map(self, df: pd.DataFrame) -> str:
        """Tworzy mapę ryzyka prawnego"""
        if 'ryzyko' not in df.columns or 'priorytet' not in df.columns:
            return ""
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['priorytet'],
            y=df['ryzyko'],
            mode='markers+text',
            marker=dict(size=15, color='#e74c3c', line=dict(width=2, color='white')),
            text=df.get('nazwa', df.index),
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>Priorytet: %{x:.1f}<br>Ryzyko: %{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Mapa Ryzyka Prawnego',
            xaxis_title='Priorytet',
            yaxis_title='Ryzyko',
            height=800,
            width=1200,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'mapa_ryzyka_prawnego.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_3d_risk_chart(self, df: pd.DataFrame) -> str:
        """Tworzy wykres 3D: priorytet vs ryzyko vs czas"""
        required_cols = ['priorytet', 'ryzyko']
        if not all(col in df.columns for col in required_cols):
            return ""
        
        # Symuluj czas jeśli brak
        if 'czas' not in df.columns:
            df['czas'] = np.random.uniform(1, 30, len(df))  # dni
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter3d(
            x=df['priorytet'],
            y=df['ryzyko'],
            z=df['czas'],
            mode='markers+text',
            marker=dict(size=12, color='#9b59b6', opacity=0.8),
            text=df.get('nazwa', df.index),
            hovertemplate='<b>%{text}</b><br>Priorytet: %{x:.1f}<br>Ryzyko: %{y:.2f}<br>Czas: %{z:.0f} dni<extra></extra>'
        ))
        
        fig.update_layout(
            title='Wykres 3D - Priorytet vs Ryzyko vs Czas',
            scene=dict(
                xaxis_title='Priorytet',
                yaxis_title='Ryzyko',
                zaxis_title='Czas (dni)',
                bgcolor='white'
            ),
            height=800,
            width=1200,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'wykres_3d_ryzyko.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_correlation_heatmap(self, df: pd.DataFrame) -> str:
        """Tworzy heatmap korelacji"""
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
            title='Heatmap Korelacji Spraw',
            height=700,
            width=900,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'heatmap_korelacji.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_hama_diamond_radar(self, df: pd.DataFrame) -> str:
        """Tworzy wykres radarowy HAMA Diamond dla spraw"""
        if 'priorytet' not in df.columns:
            return ""
        
        df_top5 = df.nlargest(5, 'priorytet')
        
        indicators = ['priorytet', 'ryzyko', 'znaczenie', 'pilnosc', 'kompleksowosc']
        available_indicators = [ind for ind in indicators if ind in df.columns]
        
        if len(available_indicators) < 3:
            return ""
        
        fig = go.Figure()
        
        for idx, row in df_top5.iterrows():
            values = []
            for ind in available_indicators:
                val = row[ind]
                normalized = min(100, max(0, val * 10)) if val < 10 else min(100, val)
                values.append(normalized)
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=[ind.replace('_', ' ').title() for ind in available_indicators],
                fill='toself',
                name=row.get('nazwa', f"Sprawa {idx}"),
                hovertemplate='<b>%{fullData.name}</b><br>%{theta}: %{r:.1f}<extra></extra>'
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title='HAMA Diamond Profile - Sprawy Administracyjne',
            height=800,
            width=1000,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'hama_diamond_radar_sprawy.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)

