"""
Knowledge Representation Layer
Fakty → Koncepty → Relacje → Graf przyczynowo-skutkowy
"""
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import networkx as nx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Concept:
    """Reprezentacja konceptu wyekstrahowanego z faktów"""
    name: str
    concept_type: str  # 'country', 'organization', 'event', 'trend', 'resource'
    attributes: Dict[str, Any] = field(default_factory=dict)
    source_facts: List[str] = field(default_factory=list)
    confidence: float = 0.5
    relevance_to_atlantis: float = 0.0


@dataclass
class Relation:
    """Relacja między konceptami"""
    source_concept: str
    target_concept: str
    relation_type: str  # 'causes', 'affects', 'influences', 'depends_on', 'conflicts_with'
    strength: float  # 0.0-1.0
    timeframe: str  # 'immediate', 'short_term', 'medium_term', 'long_term'
    evidence_facts: List[str] = field(default_factory=list)
    confidence: float = 0.5


class KnowledgeGraph:
    """
    Graf wiedzy reprezentujący fakty, koncepty i relacje
    """
    
    def __init__(self):
        self.concepts: Dict[str, Concept] = {}
        self.relations: List[Relation] = []
        self.graph = nx.DiGraph()  # Graf skierowany dla relacji przyczynowych
        self.fact_to_concepts: Dict[str, List[str]] = defaultdict(list)
        self.conflict_relations: List[Tuple[str, str]] = []
    
    def add_concept(self, concept: Concept):
        """Dodaje koncept do grafu"""
        self.concepts[concept.name] = concept
        self.graph.add_node(concept.name, **concept.attributes)
    
    def add_relation(self, relation: Relation):
        """Dodaje relację między konceptami"""
        self.relations.append(relation)
        
        # Dodanie do grafu NetworkX
        if relation.relation_type in ['causes', 'affects', 'influences']:
            self.graph.add_edge(
                relation.source_concept,
                relation.target_concept,
                relation_type=relation.relation_type,
                strength=relation.strength,
                timeframe=relation.timeframe,
                confidence=relation.confidence
            )
        elif relation.relation_type == 'conflicts_with':
            self.conflict_relations.append((relation.source_concept, relation.target_concept))
    
    def link_fact_to_concept(self, fact_id: str, concept_name: str):
        """Łączy fakt z konceptem"""
        self.fact_to_concepts[fact_id].append(concept_name)
        if concept_name in self.concepts:
            if fact_id not in self.concepts[concept_name].source_facts:
                self.concepts[concept_name].source_facts.append(fact_id)
    
    def find_causal_paths(self, source: str, target: str, max_depth: int = 5) -> List[List[str]]:
        """Znajduje ścieżki przyczynowe między konceptami"""
        try:
            paths = list(nx.all_simple_paths(self.graph, source, target, cutoff=max_depth))
            return paths
        except (nx.NodeNotFound, nx.NetworkXNoPath):
            return []
    
    def detect_conflicts(self) -> List[Dict[str, Any]]:
        """Wykrywa konflikty informacyjne w grafie"""
        conflicts = []
        
        # Konflikty bezpośrednie
        for source, target in self.conflict_relations:
            conflicts.append({
                "type": "direct_conflict",
                "concept1": source,
                "concept2": target,
                "severity": "high"
            })
        
        # Konflikty przez sprzeczne relacje
        for rel1 in self.relations:
            for rel2 in self.relations:
                if (rel1.source_concept == rel2.target_concept and 
                    rel1.target_concept == rel2.source_concept and
                    rel1.relation_type == 'causes' and rel2.relation_type == 'causes'):
                    conflicts.append({
                        "type": "circular_causality",
                        "concept1": rel1.source_concept,
                        "concept2": rel1.target_concept,
                        "severity": "medium"
                    })
        
        return conflicts
    
    def get_concept_importance(self, concept_name: str) -> float:
        """Oblicza ważność konceptu na podstawie centralności w grafie"""
        if concept_name not in self.graph:
            return 0.0
        
        # Centralność stopnia (degree centrality)
        degree_centrality = nx.degree_centrality(self.graph)
        # Centralność międzywęzłowa (betweenness centrality)
        betweenness = nx.betweenness_centrality(self.graph)
        
        importance = (
            degree_centrality.get(concept_name, 0.0) * 0.5 +
            betweenness.get(concept_name, 0.0) * 0.5
        )
        
        return importance
    
    def get_related_concepts(self, concept_name: str, max_relations: int = 10) -> List[Tuple[str, str, float]]:
        """Zwraca powiązane koncepty z typem relacji i siłą"""
        related = []
        
        for relation in self.relations:
            if relation.source_concept == concept_name:
                related.append((relation.target_concept, relation.relation_type, relation.strength))
            elif relation.target_concept == concept_name:
                related.append((relation.source_concept, relation.relation_type, relation.strength))
        
        # Sortowanie po sile relacji
        related.sort(key=lambda x: x[2], reverse=True)
        return related[:max_relations]
    
    def export_for_visualization(self) -> Dict[str, Any]:
        """Eksportuje graf do formatu dla wizualizacji"""
        nodes = []
        edges = []
        
        for concept_name, concept in self.concepts.items():
            nodes.append({
                "id": concept_name,
                "type": concept.concept_type,
                "relevance": concept.relevance_to_atlantis,
                "confidence": concept.confidence
            })
        
        for relation in self.relations:
            edges.append({
                "source": relation.source_concept,
                "target": relation.target_concept,
                "type": relation.relation_type,
                "strength": relation.strength
            })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "conflicts": self.detect_conflicts()
        }


class KnowledgeExtractor:
    """
    Ekstraktuje koncepty i relacje z faktów
    """
    
    def __init__(self, atlantis_profile: Dict):
        self.atlantis_profile = atlantis_profile
        self.key_entities = self._extract_key_entities()
    
    def _extract_key_entities(self) -> Set[str]:
        """Ekstraktuje kluczowe encje związane z Atlantis"""
        entities = set()
        
        # Kraje z kluczowych relacji
        entities.update(self.atlantis_profile.get("key_relations", []))
        
        # Organizacje
        entities.update(["EU", "NATO", "European Union"])
        
        # Sektory gospodarki
        for sector in self.atlantis_profile.get("economy", {}).get("strong_sectors", []):
            entities.add(sector)
        
        return entities
    
    def extract_concepts_from_facts(self, facts: List[Dict]) -> List[Concept]:
        """
        Ekstraktuje koncepty z faktów
        facts: Lista słowników z 'id', 'content', 'entities', 'tags'
        """
        concepts = {}
        
        for fact in facts:
            # Ekstrakcja encji z faktu
            entities = fact.get('entities', [])
            tags = fact.get('tags', [])
            
            # Tworzenie konceptów z encji
            for entity in entities:
                if entity not in concepts:
                    # Określenie typu konceptu
                    concept_type = self._determine_concept_type(entity, fact.get('content', ''))
                    
                    # Obliczenie relewantności dla Atlantis
                    relevance = self._calculate_relevance_to_atlantis(entity, fact.get('content', ''))
                    
                    concepts[entity] = Concept(
                        name=entity,
                        concept_type=concept_type,
                        attributes={
                            "first_seen_in": fact.get('id'),
                            "tags": tags
                        },
                        source_facts=[fact.get('id')],
                        relevance_to_atlantis=relevance
                    )
                else:
                    # Aktualizacja istniejącego konceptu
                    if fact.get('id') not in concepts[entity].source_facts:
                        concepts[entity].source_facts.append(fact.get('id'))
        
        return list(concepts.values())
    
    def _determine_concept_type(self, entity: str, context: str) -> str:
        """Określa typ konceptu na podstawie encji i kontekstu"""
        entity_lower = entity.lower()
        context_lower = context.lower()
        
        # Kraje
        country_keywords = ['country', 'nation', 'state', 'republic']
        if any(kw in context_lower for kw in country_keywords) or entity in self.key_entities:
            return 'country'
        
        # Organizacje
        org_keywords = ['organization', 'institution', 'union', 'alliance']
        if any(kw in context_lower for kw in org_keywords):
            return 'organization'
        
        # Wydarzenia
        event_keywords = ['crisis', 'conflict', 'agreement', 'summit', 'meeting']
        if any(kw in context_lower for kw in event_keywords):
            return 'event'
        
        # Trendy
        trend_keywords = ['growth', 'decline', 'increase', 'decrease', 'trend']
        if any(kw in context_lower for kw in trend_keywords):
            return 'trend'
        
        # Zasoby
        resource_keywords = ['oil', 'gas', 'energy', 'resource', 'commodity']
        if any(kw in context_lower for kw in resource_keywords):
            return 'resource'
        
        return 'general'
    
    def _calculate_relevance_to_atlantis(self, entity: str, context: str) -> float:
        """Oblicza relewantność konceptu dla Atlantis"""
        relevance = 0.0
        
        # Bezpośrednie odniesienie do Atlantis
        if 'atlantis' in context.lower():
            relevance += 0.5
        
        # Kluczowe relacje
        if entity in self.key_entities:
            relevance += 0.3
        
        # Sektory gospodarki Atlantis
        for sector in self.atlantis_profile.get("economy", {}).get("strong_sectors", []):
            if sector.lower() in context.lower():
                relevance += 0.2
        
        return min(relevance, 1.0)
    
    def extract_relations_from_facts(self, facts: List[Dict], concepts: List[Concept]) -> List[Relation]:
        """
        Ekstraktuje relacje między konceptami z faktów
        """
        relations = []
        concept_names = {c.name for c in concepts}
        
        for fact in facts:
            entities = fact.get('entities', [])
            content = fact.get('content', '').lower()
            
            # Wykrywanie relacji przyczynowych w tekście
            causal_keywords = {
                'causes': ['causes', 'leads to', 'results in', 'triggers'],
                'affects': ['affects', 'impacts', 'influences', 'affects'],
                'depends_on': ['depends on', 'relies on', 'requires']
            }
            
            for rel_type, keywords in causal_keywords.items():
                for keyword in keywords:
                    if keyword in content:
                        # Próba znalezienia pary konceptów w kontekście
                        for i, entity1 in enumerate(entities):
                            if entity1 not in concept_names:
                                continue
                            for entity2 in entities[i+1:]:
                                if entity2 not in concept_names:
                                    continue
                                
                                # Określenie timeframe na podstawie kontekstu
                                timeframe = self._extract_timeframe(content)
                                
                                relations.append(Relation(
                                    source_concept=entity1,
                                    target_concept=entity2,
                                    relation_type=rel_type,
                                    strength=0.6,  # Domyślna siła
                                    timeframe=timeframe,
                                    evidence_facts=[fact.get('id')],
                                    confidence=0.5
                                ))
        
        return relations
    
    def _extract_timeframe(self, content: str) -> str:
        """Ekstraktuje horyzont czasowy z treści"""
        if any(word in content for word in ['immediate', 'now', 'current', 'today']):
            return 'immediate'
        elif any(word in content for word in ['short', 'weeks', 'months', 'recent']):
            return 'short_term'
        elif any(word in content for word in ['medium', 'year', 'years']):
            return 'medium_term'
        elif any(word in content for word in ['long', 'future', 'decade']):
            return 'long_term'
        return 'medium_term'

