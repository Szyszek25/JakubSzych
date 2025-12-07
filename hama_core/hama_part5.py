"""
HAMA DIAMOND - CZESC 5: AGENT KOGNITYWNY I INTEGRATOR
Uzywa lokalnych modeli LLM (Ollama/Llama) zamiast Google Generative AI
"""
from typing import Dict, Any, List, Optional, Tuple
from collections import deque
import time
import random

# Import torch (opcjonalne - jeśli dostępne)
try:
    import torch  # type: ignore
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    # Prosty fallback dla torch
    class TorchFallback:
        @staticmethod
        def tensor(data, **kwargs):
            return data
        class long:
            pass
    torch = TorchFallback()  # type: ignore

# Importy z innych części HAMA Diamond (opcjonalne - jeśli dostępne)
try:
    from hama_part1 import SensoryData, Action, ModalityType, EmotionType as EmotionTypeOriginal  # type: ignore
    from hama_part2 import HAMA2CognitiveConfig, HAMA2CognitiveCore  # type: ignore
    from hama_part3 import ComplexDynamicEnvironment, SensoryMotorModule, GlobalWorkspace, ComplexPerceptionModule, PlanningDecisionModule, LanguageModule, SelfReflectionModule, EmotionValueModule, CreativityModule, ContinuousLearningModule  # type: ignore
    from hama_part4 import WorldModel, EnhancedMemoryNexus, Episode, Concept, CognitiveSequenceGenerator  # type: ignore
    EmotionType = EmotionTypeOriginal  # type: ignore
    HAMA_IMPORTS_AVAILABLE = True
except ImportError:
    # Fallback - proste klasy zastępcze
    HAMA_IMPORTS_AVAILABLE = False
    
    # Proste klasy zastępcze
    class ComplexDynamicEnvironment:
        def generate_sensory_data(self): return []
        def execute_action(self, action): return {'success': True}
    
    class SensoryMotorModule:
        def process_sensory_input(self, data): return []
        def generate_motor_commands(self, intentions): return []
    
    class GlobalWorkspace:
        def __init__(self): self.working_memory = []
        def integrate_multimodal(self, data): return []
        def update_working_memory(self, items): pass
        def form_intention(self, goal): return []
    
    class ComplexPerceptionModule:
        def recognize_patterns(self, content): return {}
        def conceptualize(self, patterns): return []
    
    class PlanningDecisionModule:
        def generate_plan(self, goal, world_model): return []
        def set_goal(self, goal): pass
    
    class LanguageModule:
        def engage_dialogue(self, input_text): return "Response"
    
    class SelfReflectionModule:
        def monitor_progress(self, goal, context): return {'completion': 0.5}
        def evaluate_action(self, action, result): return 0.5
    
    class EmotionValueModule:
        def __init__(self):
            self.current_emotions = []
        def evaluate_situation(self, situation): return []
        def get_motivation(self): return 0.5
    
    class CreativityModule:
        def generate_ideas(self, goal, context): return []
    
    class ContinuousLearningModule:
        def reinforcement_learn(self, context, action, reward): pass
    
    class WorldModel:
        def __init__(self):
            self.objects = {}
        def update_from_perception(self, concepts): pass
    
    class EnhancedMemoryNexus:
        def __init__(self):
            self.episodic_memory = []
        def store_episode(self, episode): pass
    
    class Episode:
        def __init__(self, **kwargs): pass
    
    class Concept:
        def __init__(self, **kwargs): pass
    
    class HAMA2CognitiveConfig:
        def __init__(self):
            self.vocab_size = 512
    
    class HAMA2CognitiveCore:
        def __init__(self, config): pass
        def get_emergent_metrics(self): return {}
        def __call__(self, *args, **kwargs): return (None, None)
        def update_emergent_state(self, *args, **kwargs): pass
    
    class CognitiveSequenceGenerator:
        def __init__(self, vocab_size): pass
        def map_cognitive_data(self, data): return []
    
    # Fallback EmotionType - użyj Enum jeśli dostępne
    try:
        from enum import Enum
        class EmotionType(Enum):  # type: ignore
            CURIOSITY = "curiosity"
            JOY = "joy"
            FEAR = "fear"
            FRUSTRATION = "frustration"
            SATISFACTION = "satisfaction"
    except ImportError:
        # Najprostszy fallback
        class EmotionType:  # type: ignore
            CURIOSITY = "curiosity"
            JOY = "joy"
            FEAR = "fear"
            FRUSTRATION = "frustration"
            SATISFACTION = "satisfaction"

# ============================================================================
# GŁÓWNY AGENT KOGNITYWNY
# ============================================================================

class CognitiveAgent:
    def __init__(self):
        self.environment = ComplexDynamicEnvironment()
        self.sensory_motor = SensoryMotorModule()
        self.workspace = GlobalWorkspace()
        self.perception_module = ComplexPerceptionModule()
        self.planning_module = PlanningDecisionModule()
        self.language_module = LanguageModule()
        self.reflection_module = SelfReflectionModule()
        self.emotion_module = EmotionValueModule()
        self.creativity_module = CreativityModule()
        self.learning_module = ContinuousLearningModule()
        self.world_model = WorldModel()
        self.memory = EnhancedMemoryNexus()
        self.current_goal = "explore"
        self.cycle_count = 0

    def cognitive_cycle(self):
        self.cycle_count += 1

        # 1. Percepcja
        raw_sensory = self.environment.generate_sensory_data()
        processed_sensory = self.sensory_motor.process_sensory_input(raw_sensory)

        # 2. Working Memory
        working_items = self.workspace.integrate_multimodal(processed_sensory)
        self.workspace.update_working_memory(working_items)

        # 3. Rozpoznawanie wzorców
        perceived_patterns = []
        for item in self.workspace.working_memory:
            pattern = self.perception_module.recognize_patterns(item.content)
            perceived_patterns.append(pattern)

        # 4. Konceptualizacja
        concepts = self.perception_module.conceptualize(perceived_patterns)
        self.world_model.update_from_perception(concepts)

        # 5. Emocje
        situation = {
            "novel": len(concepts) > 2,
            "goal_achieved": random.random() > 0.7
        }
        emotions = self.emotion_module.evaluate_situation(situation)
        motivation = self.emotion_module.get_motivation()

        # 6. Planowanie
        plan = self.planning_module.generate_plan(self.current_goal, self.world_model)
        progress = self.reflection_module.monitor_progress(
            self.current_goal, 
            {"cycle": self.cycle_count}
        )

        # 7. Kreatywność (co 5 cykli)
        if self.cycle_count % 5 == 0:
            ideas = self.creativity_module.generate_ideas(self.current_goal, {})

        # 8. Intencje
        intentions = self.workspace.form_intention(self.current_goal)
        if plan:
            intentions.extend(plan[:2])

        # 9. Akcje
        motor_commands = self.sensory_motor.generate_motor_commands(intentions)
        action_results = []
        for command in motor_commands[:3]:
            result = self.environment.execute_action(command)
            action_results.append(result)

            # Learning
            score = self.reflection_module.evaluate_action(command, result)
            reward = 1.0 if result['success'] else 0.0
            self.learning_module.reinforcement_learn(
                {"cycle": self.cycle_count}, 
                command, 
                reward
            )

        # 10. Pamięć
        episode = Episode(
            timestamp=time.time(),
            context={"goal": self.current_goal, "cycle": self.cycle_count},
            actions=motor_commands,
            outcomes=action_results,
            emotions=emotions,
            importance=motivation
        )
        self.memory.store_episode(episode)

    def set_goal(self, goal: str):
        self.current_goal = goal
        self.planning_module.set_goal(goal)

    def interact(self, user_input: str) -> str:
        return self.language_module.engage_dialogue(user_input)

print("OK Agent kognitywny zdefiniowany")

# ============================================================================
# INTEGRATOR EMERGENTNY
# ============================================================================

class EmergentCognitiveIntegrator:
    def __init__(self, cognitive_agent):
        self.cognitive_agent = cognitive_agent
        self.config = HAMA2CognitiveConfig()
        self.hama2_core = HAMA2CognitiveCore(self.config)
        self.sequence_generator = CognitiveSequenceGenerator(self.config.vocab_size)
        self.integration_cycles = 0
        self.cognitive_patterns = {}
        self.prediction_buffer = deque(maxlen=50)

    def integrate_cognitive_cycle(self):
        self.integration_cycles += 1
        cognitive_data = self._prepare_cognitive_data()
        emergent_output = self._update_emergent_core(cognitive_data)
        self._integrate_emergent_insights(emergent_output, cognitive_data)
        return emergent_output

    def _prepare_cognitive_data(self):
        agent = self.cognitive_agent
        cognitive_data = {
            'perception': [],
            'concepts': [],
            'emotions': agent.emotion_module.current_emotions,
            'actions': [],
            'goal': agent.current_goal,
            'working_memory': len(agent.workspace.working_memory),
            'world_objects': len(agent.world_model.objects)
        }

        for item in agent.workspace.working_memory:
            cognitive_data['perception'].append({
                'modality': getattr(item.content, 'modality', 'unknown'),
                'features': getattr(item.content, 'features', {}),
                'activation': item.activation
            })

        cognitive_data['concepts'] = list(agent.world_model.objects.values())

        if hasattr(agent, 'memory') and agent.memory.episodic_memory:
            last_episode = agent.memory.episodic_memory[-1]
            cognitive_data['actions'] = last_episode.actions[:3]

        return cognitive_data

    def _update_emergent_core(self, cognitive_data):
        cognitive_sequence = self.sequence_generator.map_cognitive_data(cognitive_data)
        
        if cognitive_sequence:
            if TORCH_AVAILABLE:
                input_tensor = torch.tensor([cognitive_sequence], dtype=torch.long)
                output, _ = self.hama2_core(input_tensor, cognitive_data)
            else:
                input_tensor = [cognitive_sequence]  # Fallback bez torch
                output, _ = self.hama2_core(input_tensor, cognitive_data) if hasattr(self.hama2_core, '__call__') else (None, None)

            cognitive_feedback = {
                'goal_progress': self._estimate_goal_progress(),
                'emotional_arousal': self._calculate_emotional_arousal(),
                'novelty': self._estimate_novelty(),
                'importance': self._estimate_importance(cognitive_data)
            }

            self.hama2_core.update_emergent_state(
                output, input_tensor,
                loss=None,
                cognitive_feedback=cognitive_feedback
            )

            return {
                'emergent_metrics': self.hama2_core.get_emergent_metrics(),
                'cognitive_feedback': cognitive_feedback
            }
        return {'emergent_metrics': self.hama2_core.get_emergent_metrics()}

    def _integrate_emergent_insights(self, emergent_output, cognitive_data):
        agent = self.cognitive_agent
        emergent_metrics = emergent_output.get('emergent_metrics', {})
        chaos_level = emergent_metrics.get('chaos_level', 0.15)
        emergent_state = emergent_metrics.get('emergent_state', 0.0)

        if chaos_level > 0.25:
            self._enhance_exploration(agent)
        elif emergent_state > 0.3:
            self._enhance_creativity(agent)

    def _enhance_exploration(self, agent):
        if not any(e.value == 'curiosity' for e in agent.emotion_module.current_emotions):
            agent.emotion_module.current_emotions.append(EmotionType.CURIOSITY)

    def _enhance_creativity(self, agent):
        if hasattr(agent, 'creativity_module') and agent.cycle_count % 5 == 0:
            ideas = agent.creativity_module.generate_ideas(
                agent.current_goal,
                {'emergent_state': 'high'}
            )

    def _estimate_goal_progress(self) -> float:
        agent = self.cognitive_agent
        if hasattr(agent, 'reflection_module'):
            progress = agent.reflection_module.monitor_progress(
                agent.current_goal,
                {'cycle': agent.cycle_count}
            )
            return progress.get('completion', 0.5)
        return 0.5

    def _calculate_emotional_arousal(self) -> float:
        agent = self.cognitive_agent
        emotions = agent.emotion_module.current_emotions
        if not emotions:
            return 0.5
        arousal_map = {
            'joy': 0.7, 'fear': 0.9, 'curiosity': 0.8,
            'satisfaction': 0.6, 'frustration': 0.85
        }
        total_arousal = sum(arousal_map.get(e.value, 0.5) for e in emotions)
        return total_arousal / len(emotions)

    def _estimate_novelty(self) -> float:
        agent = self.cognitive_agent
        world_objects = len(agent.world_model.objects)
        working_memory_items = len(agent.workspace.working_memory)
        if world_objects == 0:
            return 0.5
        return min(working_memory_items / world_objects, 1.0)

    def _estimate_importance(self, cognitive_data: Dict[str, Any]) -> float:
        importance_factors = []
        concepts_count = len(cognitive_data.get('concepts', []))
        importance_factors.append(min(concepts_count / 10.0, 1.0))
        emotions_count = len(cognitive_data.get('emotions', []))
        importance_factors.append(min(emotions_count / 3.0, 1.0))
        working_memory_usage = cognitive_data.get('working_memory', 0) / 7.0
        importance_factors.append(working_memory_usage)
        return sum(importance_factors) / len(importance_factors)

    def get_integration_status(self):
        return {
            'integration_cycles': self.integration_cycles,
            'emergent_metrics': self.hama2_core.get_emergent_metrics(),
            'cognitive_patterns_count': len(self.cognitive_patterns),
            'prediction_buffer_size': len(self.prediction_buffer)
        }

print("OK Integrator emergentny zdefiniowany")

# ============================================================================
# ROZSZERZONY AGENT
# ============================================================================

class EnhancedCognitiveAgent(CognitiveAgent):
    def __init__(self):
        super().__init__()
        self.emergent_integrator = EmergentCognitiveIntegrator(self)
        self.emergent_insights = {}
        self.adaptive_behavior_mode = "balanced"

    def cognitive_cycle(self):
        self.cycle_count += 1
        super().cognitive_cycle()
        emergent_output = self.emergent_integrator.integrate_cognitive_cycle()
        self._adapt_behavior_from_emergence(emergent_output)
        self.emergent_insights = emergent_output

    def _adapt_behavior_from_emergence(self, emergent_output):
        metrics = emergent_output.get('emergent_metrics', {})
        chaos = metrics.get('chaos_level', 0.15)
        emergent_state = metrics.get('emergent_state', 0.0)

        goal_lower = self.current_goal.lower()

        if any(word in goal_lower for word in ['explore', 'discover', 'search']):
            if chaos > 0.15 or emergent_state > 0.0:
                self.adaptive_behavior_mode = "exploratory"
                if EmotionType.CURIOSITY not in self.emotion_module.current_emotions:
                    self.emotion_module.current_emotions.append(EmotionType.CURIOSITY)
            else:
                self.adaptive_behavior_mode = "exploratory"

        elif any(word in goal_lower for word in ['create', 'innovate', 'design']):
            self.adaptive_behavior_mode = "creative"
            if self.cycle_count % 3 == 0:
                self.creativity_module.generate_ideas(
                    self.current_goal,
                    {'emergence_triggered': True}
                )

        elif any(word in goal_lower for word in ['optimize', 'routine', 'efficient']):
            self.adaptive_behavior_mode = "exploitative"

        else:
            if chaos > 0.25 and emergent_state > 0.2:
                self.adaptive_behavior_mode = "exploratory"
            elif emergent_state > 0.3:
                self.adaptive_behavior_mode = "creative"
            else:
                self.adaptive_behavior_mode = "balanced"

    def get_enhanced_state_summary(self) -> Dict[str, Any]:
        base_summary = {
            'cycle': self.cycle_count,
            'goal': self.current_goal,
            'working_memory_items': len(self.workspace.working_memory),
            'world_objects': len(self.world_model.objects),
            'episodes': len(self.memory.episodic_memory),
            'emotions': [e.value for e in self.emotion_module.current_emotions],
        }
        integration_status = self.emergent_integrator.get_integration_status()

        enhanced_summary = {
            **base_summary,
            'emergent_metrics': integration_status['emergent_metrics'],
            'adaptive_behavior_mode': self.adaptive_behavior_mode,
            'integration_cycles': integration_status['integration_cycles'],
            'emergent_insights_count': len(self.emergent_insights)
        }
        return enhanced_summary

print("OK Rozszerzony agent zdefiniowany")
print("\n" + "="*70)
print("CZESC 5 ZAKONCZONA - Przejdz do CZESCI 6")
print("="*70)
