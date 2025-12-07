"""
🌍 HAMA DIAMOND - CZĘŚĆ 3: ŚRODOWISKO I MODUŁY KOGNITYWNE
Gotowe do wklejenia w Google Colab
"""

# ============================================================================
# IMPORTY
# ============================================================================

from typing import Dict, List, Any, Optional, Tuple
import time
import random
from collections import deque

# Import typów z hama_part1
try:
    from hama_part1 import (
        SensoryData,
        Action,
        ActionType,
        ModalityType,
        EmotionType,
        WorkingMemoryItem,
        Concept
    )
except ImportError:
    # Fallback jeśli import nie działa
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from hama_part1 import (
        SensoryData,
        Action,
        ActionType,
        ModalityType,
        EmotionType,
        WorkingMemoryItem,
        Concept
    )

# ============================================================================
# DYNAMICZNE ŚRODOWISKO
# ============================================================================

class ComplexDynamicEnvironment:
    def __init__(self):
        self.state = {
            "objects": ["ball", "box", "table", "chair", "book", "lamp", "key", "door"],
            "agents": ["agent_self", "other_agent_1"],
            "time": 0,
            "events": [],
            "weather": "sunny",
            "time_of_day": "morning",
            "object_states": {
                "door": "closed",
                "lamp": "off",
                "key": "on_table"
            }
        }
        self.history = []
        self.event_probability = 0.3
        self.complexity_level = 0.5

    def generate_sensory_data(self) -> List[SensoryData]:
        data = []
        
        # Vision
        visible_objects = random.sample(
            self.state["objects"], 
            k=random.randint(2, min(6, len(self.state["objects"])))
        )
        data.append(SensoryData(
            modality=ModalityType.VISION,
            data={
                "objects_visible": visible_objects,
                "scene": random.choice(["living_room", "kitchen", "bedroom"]),
                "lighting": self.state["time_of_day"]
            },
            timestamp=time.time(),
            intensity=random.uniform(0.7, 1.0)
        ))
        
        # Audio
        if random.random() > 0.5:
            data.append(SensoryData(
                modality=ModalityType.AUDIO,
                data={
                    "sound": random.choice(["voice", "door_opening", "footsteps", "silence"]),
                    "volume": random.uniform(0.2, 0.9)
                },
                timestamp=time.time(),
                intensity=random.uniform(0.4, 0.9)
            ))
        
        # Random events
        if random.random() < self.event_probability:
            self._generate_random_event()
        
        return data

    def _generate_random_event(self):
        events = [
            {"type": "door_opens", "impact": "high"},
            {"type": "light_changes", "impact": "medium"},
            {"type": "object_moves", "impact": "low"}
        ]
        event = random.choice(events)
        self.state["events"].append({**event, "timestamp": time.time()})

    def execute_action(self, action: Action) -> Dict[str, Any]:
        self.history.append(action)
        self.state["time"] += 1
        
        success_prob = 0.7 - (self.complexity_level * 0.2)
        success = random.random() < success_prob
        
        feedback = {
            "success": success,
            "effect": f"Executed {action.action_type.value}",
            "state_change": {"time": self.state["time"]},
            "reward": 1.0 if success else -0.2
        }
        
        return feedback

    def increase_complexity(self, amount: float = 0.1):
        self.complexity_level = min(1.0, self.complexity_level + amount)

print("✅ Środowisko zdefiniowane")

# ============================================================================
# MODUŁY KOGNITYWNE
# ============================================================================

class SensoryMotorModule:
    def __init__(self):
        self.sensory_buffer = deque(maxlen=100)
        self.motor_commands = deque(maxlen=50)
        self.grounding_map = {}

    def process_sensory_input(self, raw_data: List[SensoryData]) -> List[Dict[str, Any]]:
        processed = []
        for data in raw_data:
            self.sensory_buffer.append(data)
            processed_item = {
                "modality": data.modality,
                "features": self._extract_features(data),
                "intensity": data.intensity,
                "timestamp": data.timestamp
            }
            processed.append(processed_item)
        return processed

    def _extract_features(self, data: SensoryData) -> Dict[str, Any]:
        if data.modality == ModalityType.VISION:
            return {
                "objects": data.data.get("objects_visible", []),
                "scene_type": data.data.get("scene", "unknown")
            }
        elif data.modality == ModalityType.AUDIO:
            return {
                "sound_type": data.data.get("sound", "unknown"),
                "volume": data.data.get("volume", 0.5)
            }
        return {}

    def generate_motor_commands(self, intentions: List[Action]) -> List[Action]:
        commands = []
        for intention in intentions:
            command = Action(
                action_type=intention.action_type,
                parameters={**intention.parameters, "motor_ready": True},
                priority=intention.priority,
                timestamp=time.time()
            )
            self.motor_commands.append(command)
            commands.append(command)
        return commands

class GlobalWorkspace:
    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.working_memory: List[WorkingMemoryItem] = []
        self.broadcast_queue = deque(maxlen=20)

    def integrate_multimodal(self, inputs: List[Dict[str, Any]]) -> List[WorkingMemoryItem]:
        integrated = []
        for inp in inputs:
            salience = self._compute_salience(inp)
            if salience > 0.3:
                item = WorkingMemoryItem(
                    content=inp,
                    activation=salience,
                    timestamp=time.time(),
                    source=str(inp.get("modality", "unknown"))
                )
                integrated.append(item)
        return integrated

    def _compute_salience(self, item: Dict[str, Any]) -> float:
        salience = item.get("intensity", 0.5) * 0.3
        if "objects" in item.get("features", {}):
            salience += 0.4
        return min(salience + 0.3, 1.0)

    def update_working_memory(self, items: List[WorkingMemoryItem]):
        self.working_memory.extend(items)
        self.working_memory.sort(key=lambda x: x.activation, reverse=True)
        self.working_memory = self.working_memory[:self.capacity]
        for item in self.working_memory:
            item.activation *= 0.95

    def form_intention(self, goal: str) -> List[Action]:
        intentions = []
        if "explore" in goal.lower():
            intentions.append(Action(
                action_type=ActionType.MOVEMENT,
                parameters={"direction": "forward", "speed": 0.5},
                priority=0.7
            ))
        return intentions

class ComplexPerceptionModule:
    def __init__(self):
        self.patterns = {}

    def recognize_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        features = data.get("features", {})
        recognized = {
            "pattern_type": "unknown",
            "confidence": 0.0,
            "concepts": []
        }
        if "objects" in features:
            recognized["pattern_type"] = "object_configuration"
            recognized["confidence"] = 0.8
            recognized["concepts"] = features["objects"]
        return recognized

    def conceptualize(self, perceptions: List[Dict]) -> List[Concept]:
        concepts = []
        for perception in perceptions:
            for concept_name in perception.get("concepts", []):
                concept = Concept(
                    name=concept_name,
                    properties={"type": "object", "perceivable": True},
                    relations={"located_in": ["scene"]},
                    activation=0.8
                )
                concepts.append(concept)
        return concepts

class PlanningDecisionModule:
    def __init__(self):
        self.current_goal = None
        self.plan_stack = []

    def set_goal(self, goal: str):
        self.current_goal = goal

    def generate_plan(self, goal: str, world_model) -> List[Action]:
        plan = []
        for _ in range(3):
            plan.append(Action(
                action_type=ActionType.MOVEMENT,
                parameters={"step": "planned"},
                priority=0.6
            ))
        return plan

class EmotionValueModule:
    def __init__(self):
        self.current_emotions = []
        self.values = {"safety": 0.9, "curiosity": 0.7}

    def evaluate_situation(self, situation: Dict) -> List[EmotionType]:
        emotions = []
        if situation.get("novel", False):
            emotions.append(EmotionType.CURIOSITY)
        if situation.get("goal_achieved", False):
            emotions.append(EmotionType.SATISFACTION)
        self.current_emotions = emotions
        return emotions

    def get_motivation(self) -> float:
        if EmotionType.SATISFACTION in self.current_emotions:
            return 0.9
        return 0.7

class SelfReflectionModule:
    def __init__(self):
        self.performance_history = []

    def monitor_progress(self, goal: str, current_state: Dict) -> Dict[str, Any]:
        return {
            "goal": goal,
            "completion": random.uniform(0.3, 0.8),
            "success_probability": random.uniform(0.5, 0.9)
        }

    def evaluate_action(self, action: Action, outcome: Dict) -> float:
        score = 1.0 if outcome.get("success", False) else 0.3
        self.performance_history.append({"score": score, "timestamp": time.time()})
        return score

class CreativityModule:
    def __init__(self):
        self.idea_pool = []

    def generate_ideas(self, problem: str, constraints: Dict) -> List[Dict]:
        ideas = []
        for i in range(random.randint(2, 5)):
            idea = {
                "description": f"Solution {i+1} for {problem}",
                "novelty": random.uniform(0.5, 1.0),
                "feasibility": random.uniform(0.4, 0.9)
            }
            ideas.append(idea)
        self.idea_pool.extend(ideas)
        return ideas

class ContinuousLearningModule:
    def __init__(self):
        self.learning_rate = 0.01
        self.knowledge_base = {}

    def reinforcement_learn(self, state: Dict, action: Action, reward: float):
        key = f"{state.get('context', 'unknown')}_{action.action_type.value}"
        if key not in self.knowledge_base:
            self.knowledge_base[key] = {"q_value": 0.0, "visits": 0}
        old_q = self.knowledge_base[key]["q_value"]
        self.knowledge_base[key]["q_value"] = old_q + self.learning_rate * (reward - old_q)
        self.knowledge_base[key]["visits"] += 1

class LanguageModule:
    def __init__(self):
        self.context = []

    def understand(self, text: str) -> Dict[str, Any]:
        words = text.lower().split()
        understanding = {"intent": "unknown", "entities": []}
        if any(w in words for w in ["explore", "go"]):
            understanding["intent"] = "action_request"
        return understanding

    def generate(self, intent: str, content: Dict[str, Any]) -> str:
        if intent == "inform":
            return f"I perceive {', '.join(content.get('objects', []))}"
        return "I understand"

    def engage_dialogue(self, user_input: str) -> str:
        understanding = self.understand(user_input)
        self.context.append(understanding)
        return self.generate("respond", understanding)

print("✅ Moduły kognitywne zdefiniowane")
print("\n" + "="*70)
print("CZĘŚĆ 3 ZAKOŃCZONA - Przejdź do CZĘŚCI 4")
print("="*70)
