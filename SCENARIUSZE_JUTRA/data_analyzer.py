"""
Moduł analizy danych z wykorzystaniem NLP i deep research
"""
import openai
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any
from dataclasses import dataclass
import logging
from collections import defaultdict
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AnalyzedFact:
    """Reprezentacja przeanalizowanego faktu"""
    content: str
    source: str
    date: str
    relevance_score: float
    tags: List[str]
    entities: List[str]  # Nazwane encje (kraje, organizacje, osoby)
    sentiment: str  # 'positive', 'negative', 'neutral'
    confidence: float
    related_facts: List[str]  # ID powiązanych faktów


@dataclass
class Correlation:
    """Reprezentacja korelacji między faktami"""
    fact_ids: List[str]
    correlation_type: str  # 'causal', 'temporal', 'thematic'
    strength: float
    explanation: str


class DataAnalyzer:
    """Klasa odpowiedzialna za analizę zebranych danych"""
    
    def __init__(self, config, openai_api_key: str):
        self.config = config
        openai.api_key = openai_api_key
        self.llm = OpenAI(temperature=0.3, model_name=config.get("OPENAI_MODEL", "gpt-4"))
        self.analyzed_facts: List[AnalyzedFact] = []
        self.correlations: List[Correlation] = []
        self.fact_index: Dict[str, AnalyzedFact] = {}
        
    def _extract_entities(self, text: str) -> List[str]:
        """Ekstraktuje nazwane encje z tekstu"""
        # Używa LLM do ekstrakcji encji
        prompt = f"""
        Wyodrębnij z poniższego tekstu wszystkie nazwane encje:
        - Kraje
        - Organizacje międzynarodowe
        - Osoby publiczne
        - Instytucje
        - Kluczowe terminy ekonomiczne/polityczne
        
        Tekst: {text[:1000]}
        
        Zwróć listę encji oddzielonych przecinkami.
        """
        
        try:
            response = self.llm(prompt)
            entities = [e.strip() for e in response.split(',')]
            return entities[:20]  # Maksymalnie 20 encji
        except Exception as e:
            logger.warning(f"Błąd podczas ekstrakcji encji: {e}")
            return []
    
    def _analyze_sentiment(self, text: str) -> tuple:
        """Analizuje sentyment tekstu"""
        prompt = f"""
        Oceń sentyment poniższego tekstu w kontekście polityki międzynarodowej.
        Zwróć jedną z opcji: 'positive', 'negative', 'neutral'
        oraz poziom pewności (0.0-1.0).
        
        Tekst: {text[:500]}
        
        Format odpowiedzi: SENTIMENT|CONFIDENCE
        """
        
        try:
            response = self.llm(prompt)
            if '|' in response:
                sentiment, confidence = response.split('|')
                return sentiment.strip().lower(), float(confidence.strip())
            return 'neutral', 0.5
        except Exception as e:
            logger.warning(f"Błąd podczas analizy sentymentu: {e}")
            return 'neutral', 0.5
    
    def _calculate_relevance(self, fact: AnalyzedFact, atlantis_profile: Dict) -> float:
        """Oblicza relewantność faktu dla państwa Atlantis"""
        relevance_score = 0.0
        
        # Sprawdzenie czy fakt dotyczy kluczowych relacji
        key_relations = atlantis_profile.get("key_relations", [])
        for relation in key_relations:
            if relation.lower() in fact.content.lower():
                relevance_score += 0.3
        
        # Sprawdzenie czy dotyczy sektorów gospodarki
        strong_sectors = atlantis_profile.get("economy", {}).get("strong_sectors", [])
        for sector in strong_sectors:
            if any(word in fact.content.lower() for word in sector.lower().split()):
                relevance_score += 0.2
        
        # Sprawdzenie czy dotyczy zagrożeń
        threats = atlantis_profile.get("threats", {})
        threat_keywords = []
        for threat_list in threats.values():
            threat_keywords.extend([t.lower() for t in threat_list])
        
        for keyword in threat_keywords:
            if keyword in fact.content.lower():
                relevance_score += 0.25
        
        # Sprawdzenie czy dotyczy UE/NATO
        if any(org in fact.content for org in ["EU", "European Union", "NATO"]):
            relevance_score += 0.15
        
        return min(relevance_score, 1.0)
    
    def analyze_data(self, data_sources: List, atlantis_profile: Dict) -> List[AnalyzedFact]:
        """Analizuje zebrane dane źródłowe"""
        logger.info("Rozpoczynam analizę danych...")
        
        analyzed_facts = []
        
        for idx, source in enumerate(data_sources):
            # Ekstrakcja encji
            entities = self._extract_entities(source.content)
            
            # Analiza sentymentu
            sentiment, confidence = self._analyze_sentiment(source.content)
            
            # Tworzenie faktu
            fact = AnalyzedFact(
                content=source.content[:2000],  # Ograniczenie długości
                source=source.url,
                date=str(source.date) if source.date else "unknown",
                relevance_score=0.0,  # Zostanie obliczone później
                tags=entities[:10],
                entities=entities,
                sentiment=sentiment,
                confidence=confidence,
                related_facts=[]
            )
            
            # Obliczenie relewantności
            fact.relevance_score = self._calculate_relevance(fact, atlantis_profile)
            
            # Indeksowanie
            fact_id = f"fact_{idx}"
            self.fact_index[fact_id] = fact
            fact.content = f"[{fact_id}] {fact.content}"
            
            analyzed_facts.append(fact)
            
            if (idx + 1) % 10 == 0:
                logger.info(f"Przeanalizowano {idx + 1}/{len(data_sources)} źródeł")
        
        self.analyzed_facts = analyzed_facts
        logger.info(f"Zakończono analizę {len(analyzed_facts)} faktów")
        
        return analyzed_facts
    
    def find_correlations(self) -> List[Correlation]:
        """Znajduje korelacje między faktami"""
        logger.info("Szukam korelacji między faktami...")
        
        correlations = []
        
        # Grupowanie faktów po tematach
        topic_groups = defaultdict(list)
        for fact_id, fact in self.fact_index.items():
            for tag in fact.tags[:3]:  # Top 3 tagi
                topic_groups[tag].append(fact_id)
        
        # Analiza korelacji w grupach tematycznych
        for topic, fact_ids in topic_groups.items():
            if len(fact_ids) >= 2:
                # Użycie LLM do analizy korelacji
                facts_text = "\n".join([
                    f"{fid}: {self.fact_index[fid].content[:200]}"
                    for fid in fact_ids[:5]
                ])
                
                prompt = f"""
                Przeanalizuj poniższe fakty i określ czy są między nimi korelacje.
                Zwróć typ korelacji: 'causal' (przyczynowo-skutkowa), 'temporal' (czasowa), 
                'thematic' (tematyczna) oraz siłę korelacji (0.0-1.0) i krótkie wyjaśnienie.
                
                Fakty:
                {facts_text}
                
                Format: TYPE|STRENGTH|EXPLANATION
                """
                
                try:
                    response = self.llm(prompt)
                    if '|' in response:
                        parts = response.split('|')
                        if len(parts) >= 3:
                            corr_type = parts[0].strip()
                            strength = float(parts[1].strip())
                            explanation = '|'.join(parts[2:]).strip()
                            
                            correlations.append(Correlation(
                                fact_ids=fact_ids[:5],
                                correlation_type=corr_type,
                                strength=strength,
                                explanation=explanation
                            ))
                except Exception as e:
                    logger.warning(f"Błąd podczas analizy korelacji: {e}")
        
        self.correlations = correlations
        logger.info(f"Znaleziono {len(correlations)} korelacji")
        
        return correlations
    
    def get_priority_facts(self, top_n: int = 50) -> List[AnalyzedFact]:
        """Zwraca najważniejsze fakty na podstawie relewantności i pewności"""
        sorted_facts = sorted(
            self.analyzed_facts,
            key=lambda f: f.relevance_score * f.confidence,
            reverse=True
        )
        return sorted_facts[:top_n]

