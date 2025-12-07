"""
System ochrony przed data poisoning
Weryfikacja źródeł, wykrywanie anomalii, weryfikacja krzyżowa
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter
import logging
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SourceReputation:
    """Reputacja źródła danych"""
    source_url: str
    domain: str
    reputation_score: float  # 0.0-1.0
    verification_count: int
    anomaly_count: int
    last_verified: Optional[datetime] = None
    is_trusted: bool = False


@dataclass
class AnomalyDetection:
    """Wykryta anomalia"""
    fact_id: str
    anomaly_type: str  # 'outlier', 'contradiction', 'suspicious_pattern'
    severity: float  # 0.0-1.0
    description: str
    related_facts: List[str] = None


class AntiPoisoningSystem:
    """
    System ochrony przed celowym zanieczyszczaniem danych
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.source_reputations: Dict[str, SourceReputation] = {}
        self.anomalies_detected: List[AnomalyDetection] = []
        self.cross_references: Dict[str, List[str]] = defaultdict(list)  # fact_id -> [source_ids]
        self.min_source_count = config.get("min_source_count", 3)
        self.anomaly_threshold = 0.7
        
        # Zaufane domeny (oficjalne źródła)
        self.trusted_domains = {
            "gov.uk", "state.gov", "europa.eu", "nato.int", "un.org",
            "oecd.org", "auswaertiges-amt.de", "diplomatie.gouv.fr",
            "mea.gov.in", "mofa.gov.sa", "fmprc.gov.cn", "mid.ru"
        }
    
    def verify_source(self, source_url: str, content: str) -> SourceReputation:
        """Weryfikuje źródło i zwraca jego reputację"""
        from urllib.parse import urlparse
        
        domain = urlparse(source_url).netloc
        
        if domain in self.source_reputations:
            rep = self.source_reputations[domain]
            rep.verification_count += 1
            rep.last_verified = datetime.now()
        else:
            # Nowe źródło - inicjalizacja
            is_trusted = domain in self.trusted_domains
            rep = SourceReputation(
                source_url=source_url,
                domain=domain,
                reputation_score=0.9 if is_trusted else 0.5,
                verification_count=1,
                anomaly_count=0,
                last_verified=datetime.now(),
                is_trusted=is_trusted
            )
            self.source_reputations[domain] = rep
        
        # Sprawdzenie anomalii w treści
        anomalies = self._detect_content_anomalies(content)
        if anomalies:
            rep.anomaly_count += len(anomalies)
            rep.reputation_score = max(0.0, rep.reputation_score - 0.1 * len(anomalies))
        
        return rep
    
    def _detect_content_anomalies(self, content: str) -> List[Dict]:
        """Wykrywa anomalie w treści"""
        anomalies = []
        
        # 1. Sprawdzenie podejrzanych wzorców językowych
        suspicious_patterns = [
            r'[A-Z]{10,}',  # Zbyt dużo wielkich liter
            r'[!]{3,}',  # Zbyt dużo wykrzykników
            r'http[s]?://[^\s]{50,}',  # Długie podejrzane linki
        ]
        
        for pattern in suspicious_patterns:
            matches = re.findall(pattern, content)
            if matches:
                anomalies.append({
                    "type": "suspicious_pattern",
                    "pattern": pattern,
                    "matches": len(matches)
                })
        
        # 2. Sprawdzenie spójności (jeśli treść jest bardzo krótka lub bardzo długa)
        word_count = len(content.split())
        if word_count < 10:
            anomalies.append({
                "type": "outlier",
                "reason": "treść zbyt krótka",
                "value": word_count
            })
        elif word_count > 10000:
            anomalies.append({
                "type": "outlier",
                "reason": "treść zbyt długa",
                "value": word_count
            })
        
        return anomalies
    
    def cross_reference_fact(self, fact_id: str, fact_content: str, source_id: str) -> Tuple[bool, float]:
        """
        Weryfikuje fakt przez weryfikację krzyżową z innymi źródłami
        Zwraca (is_verified, confidence)
        """
        self.cross_references[fact_id].append(source_id)
        
        # Sprawdzenie czy mamy wystarczającą liczbę źródeł
        source_count = len(self.cross_references[fact_id])
        
        if source_count >= self.min_source_count:
            # Fakt zweryfikowany przez wiele źródeł
            confidence = min(0.95, 0.5 + 0.15 * source_count)
            return True, confidence
        else:
            # Potrzeba więcej źródeł
            confidence = 0.3 + 0.1 * source_count
            return False, confidence
    
    def detect_contradictions(self, facts: List[Dict]) -> List[Dict]:
        """
        Wykrywa sprzeczności między faktami
        facts: Lista słowników z kluczami 'id', 'content', 'source'
        """
        contradictions = []
        
        # Grupowanie faktów po tematach (uproszczone - w rzeczywistości użyj NLP)
        topic_groups = defaultdict(list)
        for fact in facts:
            # Ekstrakcja kluczowych słów (uproszczone)
            keywords = set(fact.get('content', '').lower().split()[:10])
            topic_key = tuple(sorted(keywords)[:5])  # Klucz tematu
            topic_groups[topic_key].append(fact)
        
        # Sprawdzanie sprzeczności w grupach tematycznych
        for topic, topic_facts in topic_groups.items():
            if len(topic_facts) < 2:
                continue
            
            # Porównanie par faktów
            for i, fact1 in enumerate(topic_facts):
                for fact2 in topic_facts[i+1:]:
                    contradiction_score = self._calculate_contradiction_score(
                        fact1.get('content', ''),
                        fact2.get('content', '')
                    )
                    
                    if contradiction_score > self.anomaly_threshold:
                        contradictions.append({
                            "fact1_id": fact1.get('id'),
                            "fact2_id": fact2.get('id'),
                            "score": contradiction_score,
                            "type": "contradiction"
                        })
        
        return contradictions
    
    def _calculate_contradiction_score(self, text1: str, text2: str) -> float:
        """
        Oblicza score sprzeczności między dwoma tekstami
        Uproszczona implementacja - w rzeczywistości użyj modelu NLP
        """
        # Sprawdzenie przeciwnych słów kluczowych
        positive_words = {'wzrost', 'rozwój', 'sukces', 'pozytywny', 'dobry', 'zwiększenie'}
        negative_words = {'spadek', 'kryzys', 'porażka', 'negatywny', 'zły', 'zmniejszenie'}
        
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        text1_positive = any(word in text1_lower for word in positive_words)
        text1_negative = any(word in text1_lower for word in negative_words)
        text2_positive = any(word in text2_lower for word in positive_words)
        text2_negative = any(word in text2_lower for word in negative_words)
        
        # Sprzeczność jeśli jeden pozytywny a drugi negatywny
        if (text1_positive and text2_negative) or (text1_negative and text2_positive):
            return 0.8
        
        return 0.0
    
    def filter_poisoned_data(self, facts: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Filtruje zanieczyszczone dane
        Zwraca (clean_facts, poisoned_facts)
        """
        clean_facts = []
        poisoned_facts = []
        
        for fact in facts:
            source_url = fact.get('source', '')
            content = fact.get('content', '')
            
            # Weryfikacja źródła
            reputation = self.verify_source(source_url, content)
            
            # Sprawdzenie anomalii
            anomalies = self._detect_content_anomalies(content)
            
            # Decyzja o filtracji
            if reputation.reputation_score < 0.3 or len(anomalies) > 2:
                poisoned_facts.append({
                    **fact,
                    "poisoning_reason": f"reputation: {reputation.reputation_score:.2f}, anomalies: {len(anomalies)}"
                })
            else:
                clean_facts.append({
                    **fact,
                    "reputation_score": reputation.reputation_score
                })
        
        logger.info(f"Filtracja: {len(clean_facts)} czystych faktów, {len(poisoned_facts)} zanieczyszczonych")
        
        return clean_facts, poisoned_facts
    
    def get_source_statistics(self) -> Dict[str, Any]:
        """Zwraca statystyki źródeł"""
        total_sources = len(self.source_reputations)
        trusted_sources = sum(1 for r in self.source_reputations.values() if r.is_trusted)
        avg_reputation = sum(r.reputation_score for r in self.source_reputations.values()) / total_sources if total_sources > 0 else 0.0
        
        return {
            "total_sources": total_sources,
            "trusted_sources": trusted_sources,
            "average_reputation": avg_reputation,
            "anomalies_detected": len(self.anomalies_detected),
            "cross_references": len(self.cross_references)
        }

