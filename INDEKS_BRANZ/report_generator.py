"""
📝 Generator Raportów

Generuje raporty tekstowe dla każdej branży oraz raport ogólny.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from config import REPORTS_DIR, KATEGORIE_BRANZ


class ReportGenerator:
    """Klasa do generowania raportów tekstowych"""
    
    def __init__(self):
        self.reports_dir = REPORTS_DIR
    
    def generate_all_reports(self, df_classified: pd.DataFrame, 
                            weights_explanation: str) -> Dict[str, str]:
        """
        Generuje wszystkie raporty
        
        Args:
            df_classified: DataFrame z klasyfikacją branż
            weights_explanation: Tekstowe wyjaśnienie wag
        
        Returns:
            Dict z ścieżkami do plików raportów
        """
        print("\n[INFO] Generowanie raportow...")
        
        reports = {}
        
        # 1. Raport ogólny
        reports['ogolny'] = self._generate_general_report(df_classified, weights_explanation)
        
        # 2. Raporty dla każdej branży
        for idx, row in df_classified.iterrows():
            branch_report = self._generate_branch_report(row)
            reports[f"branza_{row['pkd']}"] = branch_report
        
        print("[OK] Raporty wygenerowane\n")
        
        return reports
    
    def _generate_general_report(self, df: pd.DataFrame, weights_explanation: str) -> str:
        """Generuje ogólny raport podsumowujący"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# RAPORT OGÓLNY - INDEKS BRANŻ HAMA DIAMOND
Data wygenerowania: {timestamp}

## Podsumowanie

Niniejszy raport przedstawia ocenę kondycji {len(df)} branż w Polsce 
na podstawie analizy przeprowadzonej przez system HAMA Diamond (Human-AI Meta-Analysis Diamond).

## Metodologia

System wykorzystuje 6-etapową metodologię HAMA Diamond:

1. **Zbieranie danych** - agregacja z wielu źródeł (GUS, KRS, Google Trends, NBP)
2. **Normalizacja** - standaryzacja wskaźników do skali 0-1
3. **Dynamiczne ważenie** - HAMA Diamond przypisuje wagi na podstawie znaczenia i korelacji
4. **Agregacja** - syntetyczny indeks branżowy (0-100)
5. **Klasyfikacja** - przypisanie do 5 kategorii
6. **Interpretacja** - generowanie raportów tekstowych

{weights_explanation}

## Statystyki Ogólne

- **Sredni indeks HAMA Diamond**: {df['indeks_hama'].mean():.1f}
- **Mediana indeksu**: {df['indeks_hama'].median():.1f}
- **Najwyzszy indeks**: {df['indeks_hama'].max():.1f}
- **Najnizszy indeks**: {df['indeks_hama'].min():.1f}

## Rozkład Kategorii

"""
        
        # Statystyki kategorii
        category_counts = df['kategoria'].value_counts()
        for kategoria, count in category_counts.items():
            df_cat = df[df['kategoria'] == kategoria]
            avg_index = df_cat['indeks_hama'].mean()
            report += f"- **{kategoria.replace('_', ' ').title()}**: {count} branż (średni indeks: {avg_index:.1f})\n"
        
        report += "\n## Top 5 Branż (Najwyższy Indeks)\n\n"
        
        df_top5 = df.nlargest(5, 'indeks_hama')
        for idx, row in df_top5.iterrows():
            report += f"1. **{row['nazwa']}** (PKD: {row['pkd']})\n"
            report += f"   - Indeks HAMA Diamond: {row['indeks_hama']:.1f}\n"
            report += f"   - Kategoria: {row['kategoria'].replace('_', ' ').title()}\n"
            report += f"   - Dynamika przychodów: {row.get('dynamika_przychodow', 0):.1f}%\n"
            report += f"   - Rentowność: {row.get('rentownosc', 0):.1f}%\n\n"
        
        report += "\n## Branże Wymagające Uwagi (Najniższy Indeks)\n\n"
        
        df_bottom5 = df.nsmallest(5, 'indeks_hama')
        for idx, row in df_bottom5.iterrows():
            report += f"- **{row['nazwa']}** (PKD: {row['pkd']})\n"
            report += f"  - Indeks HAMA Diamond: {row['indeks_hama']:.1f}\n"
            report += f"  - Kategoria: {row['kategoria'].replace('_', ' ').title()}\n"
            report += f"  - Główne problemy: "
            
            # Identyfikuj problemy
            problems = []
            if row.get('zadluzenie', 0) > 1.5:
                problems.append("wysokie zadłużenie")
            if row.get('szkodowosc', 0) > 1.0:
                problems.append("wysoka szkodowość")
            if row.get('dynamika_przychodow', 0) < 0:
                problems.append("spadek przychodów")
            
            if problems:
                report += ", ".join(problems)
            else:
                report += "ogólne osłabienie kondycji"
            
            report += "\n\n"
        
        report += "\n## Perspektywy na 12-36 miesięcy\n\n"
        report += "Na podstawie analizy wskaźników, system HAMA Diamond przewiduje:\n\n"
        
        # Perspektywy dla każdej kategorii
        for kategoria in ['wzrostowe', 'stabilne', 'ryzykowne', 'kurczace_sie', 'wymagajace_finansowania']:
            df_cat = df[df['kategoria'] == kategoria]
            if len(df_cat) == 0:
                continue
            
            report += f"### {kategoria.replace('_', ' ').title()}\n\n"
            
            if kategoria == 'wzrostowe':
                report += "Branże w tej kategorii wykazują silne fundamenty i pozytywne trendy. "
                report += "Oczekiwany jest dalszy wzrost w perspektywie 12-36 miesięcy. "
                report += "Rekomendacja: zwiększone finansowanie, monitoring trendów.\n\n"
            
            elif kategoria == 'stabilne':
                report += "Branże stabilne charakteryzują się umiarkowanym wzrostem. "
                report += "Perspektywy są pozytywne, ale wymagają regularnego monitoringu. "
                report += "Rekomendacja: standardowe finansowanie, okresowe przeglądy.\n\n"
            
            elif kategoria == 'ryzykowne':
                report += "Branże ryzykowne wymagają zwiększonej uwagi. "
                report += "Możliwe jest spowolnienie lub pogorszenie kondycji. "
                report += "Rekomendacja: ograniczone finansowanie, częsty monitoring, analiza ryzyka.\n\n"
            
            elif kategoria == 'kurczace_sie':
                report += "Branże kurczące się wykazują negatywne trendy. "
                report += "Wysokie ryzyko dalszego pogorszenia. "
                report += "Rekomendacja: minimalizacja ekspozycji, analiza alternatywnych scenariuszy.\n\n"
            
            elif kategoria == 'wymagajace_finansowania':
                report += "Branże z potencjałem wzrostu, ale wymagające kapitału. "
                report += "Przy odpowiednim finansowaniu możliwy jest rozwój. "
                report += "Rekomendacja: selektywne finansowanie, monitoring postępów.\n\n"
        
        report += "\n---\n\n"
        report += "*Raport wygenerowany automatycznie przez system HAMA Diamond-Indeks Branż*\n"
        
        # Zapis
        filepath = self.reports_dir / 'raport_ogolny.md'
        filepath.write_text(report, encoding='utf-8')
        print(f"  [OK] Zapisano: {filepath.name}")
        
        return str(filepath)
    
    def _generate_branch_report(self, row: pd.Series) -> str:
        """Generuje raport dla pojedynczej branży"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# RAPORT BRANŻOWY - {row['nazwa']}
PKD: {row['pkd']}
Data wygenerowania: {timestamp}

## Podsumowanie

**Indeks HAMA Diamond**: {row['indeks_hama']:.1f}/100
**Kategoria**: {row['kategoria'].replace('_', ' ').title()}

## Analiza Wskaźników

"""
        
        # Lista wskaźników
        indicators = {
            'Dynamika przychodów (YoY %)': row.get('dynamika_przychodow', np.nan),
            'Rentowność (%)': row.get('rentownosc', np.nan),
            'Wskaźnik zadłużenia (D/E)': row.get('zadluzenie', np.nan),
            'Szkodowość (% upadłości)': row.get('szkodowosc', np.nan),
            'Dynamika eksportu (YoY %)': row.get('dynamika_eksportu', np.nan),
            'Dynamika inwestycji (YoY %)': row.get('inwestycje', np.nan),
            'Nastroje konsumenckie': row.get('nastroje_konsumenckie', np.nan),
            'Trendy wyszukiwań': row.get('trendy_wyszukiwan', np.nan),
            'Dynamika nowych firm (YoY %)': row.get('nowe_firmy', np.nan),
            'Produktywność (tys. PLN/etat)': row.get('produktywnosc', np.nan)
        }
        
        for indicator_name, value in indicators.items():
            if pd.notna(value):
                report += f"- **{indicator_name}**: {value:.2f}\n"
            else:
                report += f"- **{indicator_name}**: Brak danych\n"
        
        report += f"\n## Interpretacja\n\n"
        
        # Interpretacja na podstawie kategorii
        kategoria = row['kategoria']
        indeks = row['indeks_hama']
        
        if kategoria == 'wzrostowe':
            report += f"Branza {row['nazwa']} znajduje sie w kategorii **wzrostowej**. "
            report += f"Indeks HAMA Diamond wynosi {indeks:.1f}, co wskazuje na bardzo dobra kondycje. "
            report += "Branża wykazuje silne fundamenty finansowe i pozytywne trendy rozwojowe.\n\n"
        
        elif kategoria == 'stabilne':
            report += f"Branża {row['nazwa']} jest klasyfikowana jako **stabilna**. "
            report += f"Indeks HAMA Diamond ({indeks:.1f}) wskazuje na umiarkowaną, ale stabilną kondycję. "
            report += "Branża nie wykazuje znaczących problemów, ale też nie notuje dynamicznego wzrostu.\n\n"
        
        elif kategoria == 'ryzykowne':
            report += f"Branża {row['nazwa']} została zaklasyfikowana jako **ryzykowna**. "
            report += f"Indeks HAMA Diamond ({indeks:.1f}) wskazuje na podwyższone ryzyko. "
            report += "Wymagana jest zwiększona czujność i regularny monitoring sytuacji.\n\n"
        
        elif kategoria == 'kurczace_sie':
            report += f"Branża {row['nazwa']} znajduje się w kategorii **kurczących się**. "
            report += f"Indeks HAMA Diamond ({indeks:.1f}) wskazuje na poważne problemy. "
            report += "Branża wykazuje negatywne trendy i wysokie ryzyko dalszego pogorszenia.\n\n"
        
        elif kategoria == 'wymagajace_finansowania':
            report += f"Branża {row['nazwa']} jest klasyfikowana jako **wymagająca finansowania**. "
            report += f"Indeks HAMA Diamond ({indeks:.1f}) wskazuje na potencjał wzrostu, ale branża potrzebuje kapitału. "
            report += "Przy odpowiednim finansowaniu możliwy jest rozwój.\n\n"
        
        report += "## Rekomendacje\n\n"
        
        # Rekomendacje
        if kategoria in ['wzrostowe', 'stabilne']:
            report += "- ✅ Kontynuacja standardowego finansowania\n"
            report += "- 📊 Regularny monitoring wskaźników\n"
            report += "- 🎯 Rozważenie zwiększenia ekspozycji przy pozytywnych trendach\n\n"
        
        elif kategoria == 'ryzykowne':
            report += "- ⚠️ Ograniczenie nowego finansowania\n"
            report += "- 📊 Zwiększona częstotliwość monitoringu\n"
            report += "- 🔍 Analiza przyczyn osłabienia kondycji\n"
            report += "- 💼 Rozważenie restrukturyzacji istniejących kredytów\n\n"
        
        elif kategoria == 'kurczace_sie':
            report += "- 🛑 Minimalizacja ekspozycji\n"
            report += "- 📉 Przygotowanie planów wyjścia\n"
            report += "- 🔍 Analiza alternatywnych scenariuszy\n"
            report += "- ⚠️ Wysoka czujność wobec nowych transakcji\n\n"
        
        elif kategoria == 'wymagajace_finansowania':
            report += "- 💰 Selektywne finansowanie projektów rozwojowych\n"
            report += "- 📊 Monitoring postępów i wykorzystania kapitału\n"
            report += "- 🎯 Wsparcie strategicznych inwestycji\n"
            report += "- ⚖️ Ocena ryzyka vs. potencjału wzrostu\n\n"
        
        report += "\n---\n\n"
        report += "*Raport wygenerowany automatycznie przez system HAMA Diamond-Indeks Branż*\n"
        
        # Zapis
        filepath = self.reports_dir / f"raport_{row['pkd']}_{row['nazwa'].replace(' ', '_')}.md"
        filepath.write_text(report, encoding='utf-8')
        
        return str(filepath)


if __name__ == "__main__":
    # Test generatora raportów
    from data_collector import DataCollector
    from indicators import IndustryIndicators
    from hama_scoring import HAMADiamondScoringEngine
    from classifier import IndustryClassifier
    
    print("🧪 Test Report Generator...\n")
    
    # Przygotuj dane
    collector = DataCollector()
    data = collector.collect_all_data()
    
    indicators_calc = IndustryIndicators()
    df_indicators = indicators_calc.calculate_all_indicators(data)
    
    scoring = HAMADiamondScoringEngine()
    df_index = scoring.calculate_index(df_indicators)
    weights_explanation = scoring.get_weights_explanation()
    
    classifier = IndustryClassifier()
    df_classified = classifier.classify_industries(df_index)
    
    # Generuj raporty
    report_gen = ReportGenerator()
    reports = report_gen.generate_all_reports(df_classified, weights_explanation)
    
    print(f"\n✅ Wygenerowano {len(reports)} raportów")

