"""
🧠 HAMA DIAMOND - CZĘŚĆ 4: MODEL ŚWIATA I PAMIĘĆ
Używa lokalnych modeli LLM (Ollama/Llama) zamiast Google Generative AI
"""

# ============================================================================
# IMPORTY
# ============================================================================

from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import random
import time

# Importy z innych części HAMA Diamond (opcjonalne - jeśli dostępne)
try:
    from hama_part1 import Concept, Episode  # type: ignore
    HAMA_IMPORTS_AVAILABLE = True
except ImportError:
    HAMA_IMPORTS_AVAILABLE = False
    # Fallback - proste klasy zastępcze
    class Concept:  # type: ignore
        def __init__(self, **kwargs):
            self.name = kwargs.get('name', 'unknown')
            self.relations = kwargs.get('relations', {})
    
    class Episode:  # type: ignore
        def __init__(self, **kwargs):
            self.timestamp = kwargs.get('timestamp', time.time())
            self.context = kwargs.get('context', {})
            self.actions = kwargs.get('actions', [])
            self.emotions = kwargs.get('emotions', [])
            self.importance = kwargs.get('importance', 0.5)

# ============================================================================
# MODEL ŚWIATA
# ============================================================================

class WorldModel:
    def __init__(self):
        self.objects: Dict[str, Concept] = {}
        self.agents: Dict[str, Dict] = {}
        self.relations: Dict[str, List[tuple]] = {}
        self.causal_rules: List[Dict] = []
        self.temporal_state = {}

    def update_from_perception(self, concepts: List[Concept]):
        for concept in concepts:
            self.objects[concept.name] = concept
            for rel_type, targets in concept.relations.items():
                if rel_type not in self.relations:
                    self.relations[rel_type] = []
                for target in targets:
                    self.relations[rel_type].append((concept.name, target))

    def simulate_future(self, goal: str, steps: int = 5) -> List[Dict]:
        scenarios = []
        for _ in range(3):
            scenario = {
                "goal": goal,
                "actions": [],
                "predicted_states": [],
                "utility": random.uniform(0.4, 0.9)
            }
            for step in range(steps):
                scenario["actions"].append({"step": step, "type": "simulated"})
            scenarios.append(scenario)
        return scenarios

print("OK Model swiata zdefiniowany")

# ============================================================================
# ULEPSZONA PAMIĘĆ Z KONSOLIDACJĄ
# ============================================================================

class EnhancedMemoryNexus:
    def __init__(self):
        self.episodic_memory: List[Episode] = []
        self.semantic_memory: Dict[str, Dict] = {}
        self.consolidation_threshold = 0.3
        self.consolidation_frequency = 10
        self.episode_counter = 0
        self.semantic_patterns = defaultdict(list)

    def store_episode(self, episode: Episode):
        self.episodic_memory.append(episode)
        self.episode_counter += 1

        # Konsolidacja oparta na importance
        if episode.importance > self.consolidation_threshold:
            self.consolidate_to_semantic(episode)

        # Forced consolidation co N epizodów
        if self.episode_counter % self.consolidation_frequency == 0:
            self._forced_consolidation()

    def consolidate_to_semantic(self, episode: Episode):
        # 1. Konsoliduj akcje
        for action in episode.actions:
            action_type = action.action_type.value
            if action_type not in self.semantic_memory:
                self.semantic_memory[action_type] = {
                    "count": 0,
                    "success_rate": 0.0,
                    "typical_contexts": [],
                    "learned_at_cycle": episode.timestamp
                }
            self.semantic_memory[action_type]["count"] += 1

        # 2. Konsoliduj emocje
        for emotion in episode.emotions:
            emotion_key = f"emotion_{emotion.value}"
            if emotion_key not in self.semantic_memory:
                self.semantic_memory[emotion_key] = {
                    "count": 0,
                    "contexts": [],
                    "learned_at_cycle": episode.timestamp
                }
            self.semantic_memory[emotion_key]["count"] += 1

        # 3. Konsoliduj kontekst
        context_key = f"context_{episode.context.get('goal', 'unknown')}"
        if context_key not in self.semantic_memory:
            self.semantic_memory[context_key] = {
                "count": 0,
                "importance": episode.importance,
                "learned_at_cycle": episode.timestamp
            }
        self.semantic_memory[context_key]["count"] += 1

        # 4. Wykryj wzorce
        self._detect_patterns(episode)

    def _detect_patterns(self, episode: Episode):
        # Pattern: action sequence
        if len(episode.actions) >= 2:
            sequence = tuple(a.action_type.value for a in episode.actions[:3])
            pattern_key = f"pattern_seq_{hash(sequence) % 1000}"

            if pattern_key not in self.semantic_memory:
                self.semantic_memory[pattern_key] = {
                    "type": "action_sequence",
                    "sequence": sequence,
                    "count": 0
                }
            self.semantic_memory[pattern_key]["count"] += 1

        # Pattern: emotion-action correlation
        if episode.emotions and episode.actions:
            for emotion in episode.emotions:
                for action in episode.actions:
                    correlation_key = f"corr_{emotion.value}_{action.action_type.value}"
                    if correlation_key not in self.semantic_memory:
                        self.semantic_memory[correlation_key] = {
                            "type": "emotion_action_correlation",
                            "emotion": emotion.value,
                            "action": action.action_type.value,
                            "count": 0
                        }
                    self.semantic_memory[correlation_key]["count"] += 1

    def _forced_consolidation(self):
        recent_episodes = self.episodic_memory[-self.consolidation_frequency:]
        for episode in recent_episodes:
            if episode.importance < self.consolidation_threshold:
                episode.importance = self.consolidation_threshold + 0.1
                self.consolidate_to_semantic(episode)

    def retrieve_episodic(self, query: Dict, k: int = 5) -> List[Episode]:
        relevant = []
        for episode in self.episodic_memory:
            relevance = self._compute_relevance(episode, query)
            if relevance > 0.3:
                relevant.append((episode, relevance))
        relevant.sort(key=lambda x: x[1], reverse=True)
        return [ep for ep, _ in relevant[:k]]

    def _compute_relevance(self, episode: Episode, query: Dict) -> float:
        relevance = 0.0
        query_context = query.get("context", {})
        shared_keys = set(episode.context.keys()) & set(query_context.keys())
        if shared_keys:
            relevance += 0.5
        return relevance

    def get_semantic_statistics(self):
        stats = {
            'total_concepts': len(self.semantic_memory),
            'by_type': defaultdict(int),
            'most_common': []
        }

        for key, data in self.semantic_memory.items():
            concept_type = data.get('type', 'basic')
            stats['by_type'][concept_type] += 1

        sorted_concepts = sorted(
            self.semantic_memory.items(),
            key=lambda x: x[1].get('count', 0),
            reverse=True
        )
        stats['most_common'] = [(k, v.get('count', 0)) for k, v in sorted_concepts[:5]]

        return stats

print("OK Ulepszona pamiec zdefiniowana")

# ============================================================================
# GENERATOR SEKWENCJI KOGNITYWNYCH
# ============================================================================

class CognitiveSequenceGenerator:
    def __init__(self, vocab_size: int = 512):
        self.vocab_size = vocab_size
        self.concept_mappings = {}

    def map_cognitive_data(self, cognitive_data: Dict[str, Any]) -> List[int]:
        sequence = []
        
        if 'perception' in cognitive_data:
            for modality_data in cognitive_data['perception']:
                modality_hash = hash(str(modality_data.get('modality', 'unknown'))) % 100
                sequence.append(modality_hash)
        
        if 'concepts' in cognitive_data:
            for concept in cognitive_data['concepts']:
                concept_hash = hash(getattr(concept, 'name', 'unknown')) % 100 + 100
                sequence.append(concept_hash)
        
        if 'emotions' in cognitive_data:
            for emotion in cognitive_data['emotions']:
                emotion_hash = hash(getattr(emotion, 'value', 'unknown')) % 50 + 200
                sequence.append(emotion_hash)
        
        if 'actions' in cognitive_data:
            for action in cognitive_data['actions']:
                action_hash = hash(getattr(action.action_type, 'value', 'unknown')) % 50 + 250
                sequence.append(action_hash)
        
        if not sequence:
            sequence = [random.randint(0, self.vocab_size-1)]
        
        return sequence

print("OK Generator sekwencji zdefiniowany")
print("\n" + "="*70)
print("CZESC 4 ZAKONCZONA - Przejdz do CZESCI 5")
print("="*70)
