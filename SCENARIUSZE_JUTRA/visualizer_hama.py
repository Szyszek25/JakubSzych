"""
HAMA Diamond Visualizer dla Scenariusze Jutra

Tworzy zaawansowane wizualizacje 2D i 3D dla scenariuszy foresightowych:
- Wykresy prawdopodobieństw scenariuszy
- Mapa ryzyka i szans
- Wykresy 3D (czas vs prawdopodobieństwo vs wpływ)
- Heatmap korelacji czynników
- HAMA Diamond Radar dla scenariuszy
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any
import re
import json
from datetime import datetime

# Plotly import
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("[WARNING] Plotly nie jest zainstalowany - wizualizacje beda niedostepne")


class ScenarioVisualizer:
    """Klasa do tworzenia wizualizacji dla scenariuszy foresightowych"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        if output_dir is None:
            self.output_dir = Path(__file__).parent / "outputs" / "wykresy"
        else:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.colors = {
            'pozytywny': '#2ecc71',
            'negatywny': '#e74c3c',
            'neutralny': '#3498db',
            'bazowy': '#95a5a6'
        }
    
    def parse_raport(self, raport_path: str) -> Dict[str, Any]:
        """
        Parsuje raport scenariuszy i wyciąga dane
        
        Returns:
            Dict z danymi scenariuszy
        """
        with open(raport_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        scenarios = {
            'pozytywny_12m': [],
            'negatywny_12m': [],
            'pozytywny_36m': [],
            'negatywny_36m': []
        }
        
        # Wyciągnij scenariusze
        for scenario_type in scenarios.keys():
            pattern = f"### Scenariusz {'pozytywny' if 'pozytywny' in scenario_type else 'negatywny'} - {'12' if '12' in scenario_type else '36'} miesięcy"
            section_match = re.search(pattern, content, re.IGNORECASE)
            
            if section_match:
                # Znajdź sekcję z wydarzeniami
                section_start = section_match.end()
                next_section = content.find('###', section_start)
                section_content = content[section_start:next_section] if next_section > 0 else content[section_start:]
                
                # Wyciągnij wydarzenia (format: {'name': ..., 'probability': ..., ...})
                events = re.findall(r"\{'name':\s*'([^']+)',\s*'probability':\s*([\d.]+)", section_content)
                
                # Alternatywnie: wyciągnij z listy "Prawdopodobieństwa:"
                prob_section = re.search(r'\*\*Prawdopodobieństwa:\*\*', section_content, re.IGNORECASE)
                if prob_section:
                    prob_lines = section_content[prob_section.end():].split('\n')[:10]  # Max 10 linii
                    for line in prob_lines:
                        # Format: "  - Nazwa wydarzenia: XX%"
                        match = re.search(r'-\s*([^:]+):\s*(\d+)%', line)
                        if match:
                            event_name = match.group(1).strip()
                            prob = float(match.group(2)) / 100.0
                            scenarios[scenario_type].append({
                                'name': event_name,
                                'probability': prob,
                                'type': 'pozytywny' if 'pozytywny' in scenario_type else 'negatywny',
                                'horizon': '12m' if '12' in scenario_type else '36m'
                            })
                
                # Jeśli nie znaleziono w sekcji prawdopodobieństw, użyj wydarzeń z dict
                if not scenarios[scenario_type] and events:
                    for event_name, prob in events:
                        scenarios[scenario_type].append({
                            'name': event_name,
                            'probability': float(prob),
                            'type': 'pozytywny' if 'pozytywny' in scenario_type else 'negatywny',
                            'horizon': '12m' if '12' in scenario_type else '36m'
                        })
        
        return scenarios
    
    def create_all_visualizations(self, raport_path: str) -> Dict[str, str]:
        """
        Tworzy wszystkie wizualizacje dla raportu scenariuszy
        
        Args:
            raport_path: Ścieżka do pliku raportu
        
        Returns:
            Dict z ścieżkami do plików HTML
        """
        if not PLOTLY_AVAILABLE:
            print("[WARNING] Plotly niedostepny - pomijam wizualizacje")
            return {}
        
        print("\n[INFO] Tworzenie wizualizacji scenariuszy...")
        
        # Parsuj raport
        scenarios = self.parse_raport(raport_path)
        
        charts = {}
        
        # 1. Wykres prawdopodobieństw scenariuszy
        charts['prawdopodobienstwa'] = self._create_probability_chart(scenarios)
        
        # 2. Mapa ryzyka i szans (2D)
        charts['mapa_ryzyka'] = self._create_risk_opportunity_map(scenarios)
        
        # 3. Wykres 3D (czas vs prawdopodobieństwo vs wpływ)
        charts['wykres_3d'] = self._create_3d_timeline_chart(scenarios)
        
        # 4. Heatmap prawdopodobieństw
        charts['heatmap'] = self._create_probability_heatmap(scenarios)
        
        # 5. HAMA Diamond Radar dla scenariuszy
        charts['hama_diamond_radar'] = self._create_hama_diamond_radar(scenarios)
        
        # 6. Porównanie horyzontów czasowych
        charts['porownanie_horyzontow'] = self._create_horizon_comparison(scenarios)
        
        print("[OK] Wizualizacje utworzone\n")
        
        return charts
    
    def _create_probability_chart(self, scenarios: Dict) -> str:
        """Tworzy wykres słupkowy prawdopodobieństw scenariuszy"""
        fig = go.Figure()
        
        all_events = []
        for scenario_type, events in scenarios.items():
            for event in events:
                all_events.append({
                    'name': event['name'],
                    'probability': event['probability'],
                    'type': event['type'],
                    'horizon': event['horizon']
                })
        
        if not all_events:
            return ""
        
        df = pd.DataFrame(all_events)
        df = df.sort_values('probability', ascending=True)
        
        # Kolory według typu
        colors_list = [self.colors.get(row['type'], '#95a5a6') for _, row in df.iterrows()]
        
        fig.add_trace(go.Bar(
            x=df['probability'] * 100,
            y=df['name'],
            orientation='h',
            marker=dict(color=colors_list),
            text=[f"{p*100:.0f}%" for p in df['probability']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Prawdopodobienstwo: %{x:.1f}%<br>Typ: %{customdata[0]}<br>Horyzont: %{customdata[1]}<extra></extra>',
            customdata=df[['type', 'horizon']].values
        ))
        
        fig.update_layout(
            title='Prawdopodobienstwa Scenariuszy - HAMA Diamond',
            xaxis_title='Prawdopodobienstwo (%)',
            yaxis_title='Wydarzenie',
            height=max(400, len(df) * 40),
            width=1200,
            showlegend=False,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'prawdopodobienstwa_scenariuszy.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_risk_opportunity_map(self, scenarios: Dict) -> str:
        """Tworzy mapę ryzyka i szans (2D scatter)"""
        fig = go.Figure()
        
        all_events = []
        for scenario_type, events in scenarios.items():
            for event in events:
                # Symuluj wpływ (w produkcji: wyciągnij z raportu)
                impact = np.random.uniform(0.3, 1.0) if event['type'] == 'pozytywny' else np.random.uniform(-1.0, -0.3)
                all_events.append({
                    'name': event['name'],
                    'probability': event['probability'],
                    'impact': impact,
                    'type': event['type'],
                    'horizon': event['horizon']
                })
        
        if not all_events:
            return ""
        
        df = pd.DataFrame(all_events)
        
        # Grupuj według typu
        for event_type in df['type'].unique():
            df_type = df[df['type'] == event_type]
            
            fig.add_trace(go.Scatter(
                x=df_type['probability'] * 100,
                y=df_type['impact'],
                mode='markers+text',
                name=event_type.title(),
                marker=dict(
                    size=15,
                    color=self.colors.get(event_type, '#95a5a6'),
                    line=dict(width=2, color='white')
                ),
                text=df_type['name'],
                textposition='top center',
                hovertemplate='<b>%{text}</b><br>Prawdopodobienstwo: %{x:.1f}%<br>Wplyw: %{y:.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Mapa Ryzyka i Szans - Scenariusze',
            xaxis_title='Prawdopodobienstwo (%)',
            yaxis_title='Wplyw (pozytywny/negatywny)',
            height=800,
            width=1200,
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        filepath = self.output_dir / 'mapa_ryzyka_szans.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_3d_timeline_chart(self, scenarios: Dict) -> str:
        """Tworzy wykres 3D: czas vs prawdopodobieństwo vs wpływ"""
        fig = go.Figure()
        
        all_events = []
        for scenario_type, events in scenarios.items():
            for event in events:
                horizon_months = 12 if '12' in event['horizon'] else 36
                impact = np.random.uniform(0.3, 1.0) if event['type'] == 'pozytywny' else np.random.uniform(-1.0, -0.3)
                
                all_events.append({
                    'name': event['name'],
                    'probability': event['probability'],
                    'impact': impact,
                    'horizon': horizon_months,
                    'type': event['type']
                })
        
        if not all_events:
            return ""
        
        df = pd.DataFrame(all_events)
        
        # Grupuj według typu
        for event_type in df['type'].unique():
            df_type = df[df['type'] == event_type]
            
            fig.add_trace(go.Scatter3d(
                x=df_type['horizon'],
                y=df_type['probability'] * 100,
                z=df_type['impact'],
                mode='markers+text',
                name=event_type.title(),
                marker=dict(
                    size=12,
                    color=self.colors.get(event_type, '#95a5a6'),
                    opacity=0.8,
                    line=dict(width=1, color='white')
                ),
                text=df_type['name'],
                hovertemplate='<b>%{text}</b><br>Horyzont: %{x} mies.<br>Prawdopodobienstwo: %{y:.1f}%<br>Wplyw: %{z:.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Wykres 3D - Czas vs Prawdopodobienstwo vs Wplyw',
            scene=dict(
                xaxis_title='Horyzont czasowy (mies.)',
                yaxis_title='Prawdopodobienstwo (%)',
                zaxis_title='Wplyw',
                bgcolor='white'
            ),
            height=800,
            width=1200,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'wykres_3d_timeline.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_probability_heatmap(self, scenarios: Dict) -> str:
        """Tworzy heatmap prawdopodobieństw według typu i horyzontu"""
        # Przygotuj dane
        data = []
        for scenario_type, events in scenarios.items():
            event_type = 'pozytywny' if 'pozytywny' in scenario_type else 'negatywny'
            horizon = '12m' if '12' in scenario_type else '36m'
            
            if events:
                avg_prob = np.mean([e['probability'] for e in events])
                data.append({
                    'type': event_type,
                    'horizon': horizon,
                    'avg_probability': avg_prob
                })
        
        if not data:
            return ""
        
        df = pd.DataFrame(data)
        
        # Utwórz macierz
        matrix = np.zeros((2, 2))  # 2 typy x 2 horyzonty
        type_map = {'pozytywny': 0, 'negatywny': 1}
        horizon_map = {'12m': 0, '36m': 1}
        
        for _, row in df.iterrows():
            i = type_map[row['type']]
            j = horizon_map[row['horizon']]
            matrix[i, j] = row['avg_probability']
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=['12 mies.', '36 mies.'],
            y=['Pozytywny', 'Negatywny'],
            colorscale='RdYlGn',
            text=matrix.round(2),
            texttemplate='%{text}',
            textfont={"size": 14},
            hovertemplate='Typ: %{y}<br>Horyzont: %{x}<br>Srednie prawdopodobienstwo: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Heatmap Prawdopodobienstw Scenariuszy',
            height=400,
            width=600,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'heatmap_prawdopodobienstw.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_hama_diamond_radar(self, scenarios: Dict) -> str:
        """Tworzy wykres radarowy HAMA Diamond dla scenariuszy"""
        # Przygotuj dane dla radaru
        categories = ['Pozytywny 12m', 'Negatywny 12m', 'Pozytywny 36m', 'Negatywny 36m']
        
        values = []
        for cat in categories:
            scenario_key = f"{'pozytywny' if 'Pozytywny' in cat else 'negatywny'}_{'12' if '12' in cat else '36'}m"
            events = scenarios.get(scenario_key, [])
            if events:
                avg_prob = np.mean([e['probability'] for e in events]) * 100
            else:
                avg_prob = 0
            values.append(avg_prob)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Scenariusze',
            line=dict(color='#4ECDC4', width=3),
            hovertemplate='%{theta}: %{r:.1f}%<extra></extra>'
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
            showlegend=False,
            title='HAMA Diamond Profile - Scenariusze',
            height=700,
            width=800,
            template='plotly_white'
        )
        
        filepath = self.output_dir / 'hama_diamond_radar_scenariusze.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _create_horizon_comparison(self, scenarios: Dict) -> str:
        """Tworzy porównanie scenariuszy dla różnych horyzontów czasowych"""
        fig = go.Figure()
        
        horizons = ['12m', '36m']
        types = ['pozytywny', 'negatywny']
        
        for event_type in types:
            values = []
            for horizon in horizons:
                scenario_key = f"{event_type}_{horizon}"
                events = scenarios.get(scenario_key, [])
                if events:
                    avg_prob = np.mean([e['probability'] for e in events]) * 100
                else:
                    avg_prob = 0
                values.append(avg_prob)
            
            fig.add_trace(go.Bar(
                x=horizons,
                y=values,
                name=event_type.title(),
                marker=dict(color=self.colors.get(event_type, '#95a5a6')),
                text=[f"{v:.1f}%" for v in values],
                textposition='outside',
                hovertemplate='<b>%{fullData.name}</b><br>Horyzont: %{x}<br>Srednie prawdopodobienstwo: %{y:.1f}%<extra></extra>'
            ))
        
        fig.update_layout(
            title='Porownanie Horyzontow Czasowych',
            xaxis_title='Horyzont czasowy',
            yaxis_title='Srednie prawdopodobienstwo (%)',
            height=500,
            width=800,
            template='plotly_white',
            barmode='group'
        )
        
        filepath = self.output_dir / 'porownanie_horyzontow.html'
        fig.write_html(str(filepath))
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)


if __name__ == "__main__":
    # Test wizualizacji
    import sys
    from pathlib import Path
    
    # Znajdź raport w folderze outputs
    base_dir = Path(__file__).parent / "outputs"
    raport_files = list(base_dir.glob("raport_atlantis*.txt"))
    
    if not raport_files:
        print("[ERROR] Nie znaleziono raportu scenariuszy")
        sys.exit(1)
    
    raport_path = raport_files[0]
    print(f"[INFO] Uzywam raportu: {raport_path.name}")
    
    visualizer = ScenarioVisualizer()
    charts = visualizer.create_all_visualizations(str(raport_path))
    
    print(f"\n[OK] Utworzono {len(charts)} wizualizacji")

