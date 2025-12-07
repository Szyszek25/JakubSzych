"""
HAMA DIAMOND - CZESC 6: LLM COGNITIVE ADAPTER I TESTY HAMA DIAMOND
Uzywa lokalnych modeli LLM (Ollama/Llama) zamiast Google Generative AI
"""

# ============================================================================
# IMPORTY
# ============================================================================

from typing import Dict, List, Any, Optional, Tuple
import time
import sys
import os
import json
import random

# Opcjonalne importy
try:
    import numpy as np  # type: ignore
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    # Fallback dla numpy
    class np:  # type: ignore
        @staticmethod
        def mean(data):
            return sum(data) / len(data) if data else 0
        class random:  # type: ignore
            @staticmethod
            def uniform(a, b):
                return random.uniform(a, b)
            @staticmethod
            def choice(seq):
                return random.choice(seq)
        @staticmethod
        def polyfit(x, y, deg):
            return [0.0] * (deg + 1)
        pi = 3.141592653589793

try:
    from tqdm import tqdm  # type: ignore
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    # Fallback dla tqdm
    def tqdm(iterable, *args, **kwargs):
        return iterable

try:
    import matplotlib.pyplot as plt  # type: ignore
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False
    # Fallback dla matplotlib
    class plt:  # type: ignore
        @staticmethod
        def figure(*args, **kwargs):
            return None
        @staticmethod
        def subplot(*args, **kwargs):
            return None
        @staticmethod
        def plot(*args, **kwargs):
            pass
        @staticmethod
        def savefig(*args, **kwargs):
            pass
        @staticmethod
        def suptitle(*args, **kwargs):
            pass
        @staticmethod
        def show(*args, **kwargs):
            pass

# Import lokalnego adaptera LLM (jeśli dostępny)
try:
    # Próbuj zaimportować z SCENARIUSZE_JUTRA
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'SCENARIUSZE_JUTRA'))
    from local_llm_adapter import LocalLLMAdapter  # type: ignore
    LLM_ADAPTER_AVAILABLE = True
except ImportError:
    LLM_ADAPTER_AVAILABLE = False
    # Fallback - prosty adapter
    class LocalLLMAdapter:  # type: ignore
        def __init__(self, model_name="llama3.2"):
            self.model_name = model_name
        def generate(self, prompt, **kwargs):
            return "[LLM ADAPTER NIE DOSTEPNY] Uruchom Ollama: ollama serve"

# ============================================================================
# LLM COGNITIVE ADAPTER (dla Llama/Ollama)
# ============================================================================

class GeminiCognitiveAdapter:
    """
    Adapter kognitywny dla LLM - kompatybilny z interfejsem Gemini
    Używa lokalnego adaptera Llama/Ollama zamiast Google Generative AI
    """
    def __init__(self, gemini_model, cognitive_agent):
        # gemini_model może być None - używamy lokalnego adaptera
        self.agent = cognitive_agent
        self.conversation_history = []
        self.interaction_log = []
        
        # Inicjalizacja lokalnego adaptera LLM
        if LLM_ADAPTER_AVAILABLE:
            self.llm_adapter = LocalLLMAdapter(model_name="llama3.2")
        else:
            self.llm_adapter = None

    def cognitive_query(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        cognitive_context = self._prepare_cognitive_context(context)

        enriched_prompt = f"""
Kontekst Kognitywny Agenta:
- Cel: {self.agent.current_goal}
- Cykl: {self.agent.cycle_count}
- Obiekty w modelu świata: {list(self.agent.world_model.objects.keys())}
- Emocje: {[e.value for e in self.agent.emotion_module.current_emotions]}
- Tryb behawioralny: {getattr(self.agent, 'adaptive_behavior_mode', 'unknown')}

Zapytanie:
{prompt}

Odpowiedz uwzględniając powyższy kontekst kognitywny agenta.
"""

        start_time = time.time()
        try:
            # Użyj lokalnego adaptera LLM zamiast Gemini
            if self.llm_adapter:
                response_text = self.llm_adapter.generate(
                    enriched_prompt,
                    temperature=0.3,
                    max_tokens=2000
                )
                success = True
                error = None
            else:
                response_text = "[LLM ADAPTER NIE DOSTEPNY] Uruchom Ollama: ollama serve"
                success = False
                error = "LLM adapter nie dostępny"
        except Exception as e:
            response_text = f"Error: {str(e)}"
            success = False
            error = str(e)

        latency = time.time() - start_time

        # Pobierz stan kognitywny agenta (z fallback jeśli metoda nie istnieje)
        try:
            cognitive_state = self.agent.get_enhanced_state_summary()
        except AttributeError:
            # Fallback dla podstawowego CognitiveAgent
            cognitive_state = {
                'cycle': getattr(self.agent, 'cycle_count', 0),
                'goal': getattr(self.agent, 'current_goal', 'unknown'),
                'working_memory_items': len(getattr(self.agent.workspace, 'working_memory', [])),
                'world_objects': len(getattr(self.agent.world_model, 'objects', {})),
                'episodes': len(getattr(self.agent.memory, 'episodic_memory', [])),
                'emotions': [e.value for e in getattr(self.agent.emotion_module, 'current_emotions', [])],
                'emergent_metrics': {'chaos_level': 0.0},
                'adaptive_behavior_mode': 'balanced'
            }
        
        interaction = {
            'timestamp': time.time(),
            'prompt': prompt,
            'response': response_text,
            'latency': latency,
            'success': success,
            'error': error,
            'cognitive_state': cognitive_state
        }
        self.interaction_log.append(interaction)

        return interaction

    def _get_agent_state_safe(self) -> Dict[str, Any]:
        """Bezpieczne pobranie stanu agenta z fallback"""
        try:
            return self.agent.get_enhanced_state_summary()
        except AttributeError:
            # Fallback dla podstawowego CognitiveAgent
            return {
                'cycle': getattr(self.agent, 'cycle_count', 0),
                'goal': getattr(self.agent, 'current_goal', 'unknown'),
                'working_memory_items': len(getattr(self.agent.workspace, 'working_memory', [])),
                'world_objects': len(getattr(self.agent.world_model, 'objects', {})),
                'episodes': len(getattr(self.agent.memory, 'episodic_memory', [])),
                'emotions': [e.value for e in getattr(self.agent.emotion_module, 'current_emotions', [])],
                'emergent_metrics': {'chaos_level': 0.0},
                'adaptive_behavior_mode': 'balanced'
            }
    
    def _prepare_cognitive_context(self, context: Optional[Dict[str, Any]] = None) -> str:
        # Pobierz stan kognitywny agenta (z fallback jeśli metoda nie istnieje)
        try:
            state = self.agent.get_enhanced_state_summary()
        except AttributeError:
            # Fallback dla podstawowego CognitiveAgent
            state = {
                'working_memory_items': len(getattr(self.agent.workspace, 'working_memory', [])),
                'world_objects': len(getattr(self.agent.world_model, 'objects', {})),
                'episodes': len(getattr(self.agent.memory, 'episodic_memory', [])),
                'emergent_metrics': {'chaos_level': 0.0}
            }
        # Bezpieczne pobranie cognitive_complexity
        cognitive_complexity = state['emergent_metrics'].get('cognitive_complexity', 0.0)
        
        context_str = f"""
Working Memory: {state['working_memory_items']} items
World Objects: {state['world_objects']}
Episodes: {state['episodes']}
Emergent Chaos: {state['emergent_metrics'].get('chaos_level', 0.0):.3f}
Cognitive Complexity: {cognitive_complexity:.3f}
"""
        return context_str

    def get_interaction_statistics(self) -> Dict[str, Any]:
        if not self.interaction_log:
            return {}

        successful = [i for i in self.interaction_log if i['success']]

        latencies = [i['latency'] for i in successful]
        response_lengths = [len(i['response']) for i in successful]
        
        return {
            'total_interactions': len(self.interaction_log),
            'successful': len(successful),
            'failed': len(self.interaction_log) - len(successful),
            'avg_latency': np.mean(latencies) if latencies else 0,
            'total_tokens_estimate': sum(len(i['response'].split()) for i in successful),
            'avg_response_length': np.mean(response_lengths) if response_lengths else 0
        }

print("OK LLM Cognitive Adapter zdefiniowany")

# ============================================================================
# HAMA DIAMOND TESTS
# ============================================================================

class HAMADiamondTests:
    """
    HAMA Diamond - Zaawansowane testy kognitywne
    G - Generalization (Transfer Learning)
    Q - Quality (Robustness)
    P - Performance (Speed & Efficiency)
    A - Adaptation (Meta-Learning)
    """

    def __init__(self, agent, adapter):
        self.agent = agent
        self.adapter = adapter
        self.results = {}

    # ========================================================================
    # TEST G: GENERALIZATION
    # ========================================================================

    def test_generalization(self, n_cycles=50):
        print("\n" + "="*70)
        print("💎 HAMA DIAMOND TEST G: GENERALIZATION (Transfer Learning)")
        print("="*70)

        # Nowe środowisko
        new_objects = ["sphere", "cube", "cylinder", "pyramid",
                      "portal", "switch", "lever", "terminal"]
        old_objects = self.agent.environment.state["objects"].copy()
        self.agent.environment.state["objects"] = new_objects
        self.agent.world_model.objects.clear()

        discovery_rate = []

        for i in tqdm(range(n_cycles), desc="Transfer learning"):
            self.agent.cognitive_cycle()
            discovery_rate.append(len(self.agent.world_model.objects))

        final_objects = len(self.agent.world_model.objects)
        learning_speed = final_objects / n_cycles

        # Przywróć środowisko
        self.agent.environment.state["objects"] = old_objects

        self.results['generalization'] = {
            'final_objects': final_objects,
            'learning_speed': learning_speed,
            'discovery_rate': discovery_rate,
            'score': min(learning_speed / 0.16, 1.0)  # Normalized
        }

        print(f"\n📊 Wyniki Generalizacji:")
        print(f"  Obiekty poznane: {final_objects}/{len(new_objects)}")
        print(f"  Learning speed: {learning_speed:.3f} obj/cycle")
        print(f"  Score G: {self.results['generalization']['score']*100:.1f}/100")

        return self.results['generalization']

    # ========================================================================
    # TEST Q: QUALITY (Robustness)
    # ========================================================================

    def test_quality(self, n_trials=20):
        print("\n" + "="*70)
        print("💎 HAMA DIAMOND TEST Q: QUALITY (Adversarial Robustness)")
        print("="*70)

        perturbations = ['object_removal', 'complexity_spike', 'goal_conflict']
        recovery_times = []
        success_count = 0

        for trial in tqdm(range(n_trials), desc="Quality tests"):
            perturbation = np.random.choice(perturbations)
            baseline_chaos = self.agent.emergent_integrator.get_integration_status()['emergent_metrics']['chaos_level']

            # Apply perturbation
            if perturbation == 'object_removal' and self.agent.world_model.objects:
                obj = list(self.agent.world_model.objects.keys())[0]
                del self.agent.world_model.objects[obj]
            elif perturbation == 'complexity_spike':
                old_comp = self.agent.environment.complexity_level
                self.agent.environment.complexity_level = 1.0
            elif perturbation == 'goal_conflict':
                self.agent.set_goal("explore and stay still")

            # Measure recovery
            recovered = False
            for recovery_cycle in range(20):
                self.agent.cognitive_cycle()
                current_chaos = self.agent.emergent_integrator.get_integration_status()['emergent_metrics']['chaos_level']
                if abs(current_chaos - baseline_chaos) < 0.05:
                    recovered = True
                    recovery_times.append(recovery_cycle + 1)
                    success_count += 1
                    break

            if not recovered:
                recovery_times.append(20)

            # Restore
            if perturbation == 'complexity_spike':
                self.agent.environment.complexity_level = old_comp
            elif perturbation == 'goal_conflict':
                self.agent.set_goal("explore")

        robustness = success_count / n_trials

        self.results['quality'] = {
            'robustness_score': robustness,
            'avg_recovery': np.mean(recovery_times),
            'recovery_times': recovery_times,
            'score': robustness
        }

        print(f"\n📊 Wyniki Jakości:")
        print(f"  Robustness: {robustness*100:.1f}%")
        print(f"  Avg recovery: {np.mean(recovery_times):.1f} cycles")
        print(f"  Score Q: {self.results['quality']['score']*100:.1f}/100")

        return self.results['quality']

    # ========================================================================
    # TEST P: PERFORMANCE
    # ========================================================================

    def test_performance(self, n_cycles=200):
        print("\n" + "="*70)
        print("💎 HAMA DIAMOND TEST P: PERFORMANCE (Speed & Memory)")
        print("="*70)

        cycle_times = []
        memory_usage = []

        for i in tqdm(range(n_cycles), desc="Performance test"):
            start = time.time()
            self.agent.cognitive_cycle()
            cycle_times.append(time.time() - start)

            if i % 10 == 0:
                memory_usage.append({
                    'cycle': i,
                    'episodic': len(self.agent.memory.episodic_memory),
                    'semantic': len(self.agent.memory.semantic_memory)
                })

        avg_cycle_time = np.mean(cycle_times)
        early_time = np.mean(cycle_times[:50])
        late_time = np.mean(cycle_times[-50:])
        degradation = (late_time - early_time) / early_time * 100

        # Scoring (inverse of time, with degradation penalty)
        speed_score = min(1.0, 0.01 / avg_cycle_time)  # Faster = higher score
        efficiency_score = max(0, 1.0 - (degradation / 100))
        combined_score = (speed_score + efficiency_score) / 2

        self.results['performance'] = {
            'avg_cycle_time': avg_cycle_time,
            'degradation_pct': degradation,
            'memory_trajectory': memory_usage,
            'score': combined_score
        }

        print(f"\n📊 Wyniki Wydajności:")
        print(f"  Avg cycle time: {avg_cycle_time*1000:.2f}ms")
        print(f"  Degradacja: {degradation:+.1f}%")
        print(f"  Score P: {self.results['performance']['score']*100:.1f}/100")

        return self.results['performance']

    # ========================================================================
    # TEST A: ADAPTATION (Meta-Learning)
    # ========================================================================

    def test_adaptation(self, n_tasks=5):
        print("\n" + "="*70)
        print("💎 HAMA DIAMOND TEST A: ADAPTATION (Meta-Learning)")
        print("="*70)

        learning_speeds = []

        for task_id in tqdm(range(n_tasks), desc="Meta-learning"):
            new_objs = [f"meta_{task_id}_{i}" for i in range(5)]
            old_objs = self.agent.environment.state["objects"].copy()
            self.agent.environment.state["objects"] = new_objs
            self.agent.world_model.objects.clear()

            discovered = []
            for cycle in range(20):
                self.agent.cognitive_cycle()
                discovered.append(len(self.agent.world_model.objects))

            # Cycles to reach 4/5 objects
            target = 4
            cycles_to_target = next((i for i, v in enumerate(discovered) if v >= target), 20)
            learning_speeds.append(cycles_to_target)

            self.agent.environment.state["objects"] = old_objs

        # Calculate meta-learning trend (negative = improvement)
        meta_trend = np.polyfit(range(len(learning_speeds)), learning_speeds, 1)[0]
        improvement = learning_speeds[0] - learning_speeds[-1]

        # Scoring (negative trend = positive score)
        adaptation_score = max(0, min(1.0, 1.0 - (meta_trend / 0.1)))

        self.results['adaptation'] = {
            'speeds': learning_speeds,
            'trend': meta_trend,
            'improvement': improvement,
            'score': adaptation_score
        }

        print(f"\n📊 Wyniki Adaptacji:")
        print(f"  First task: {learning_speeds[0]} cycles")
        print(f"  Last task: {learning_speeds[-1]} cycles")
        print(f"  Improvement: {improvement} cycles")
        print(f"  Score A: {self.results['adaptation']['score']*100:.1f}/100")

        return self.results['adaptation']

    # ========================================================================
    # COMPREHENSIVE HAMA DIAMOND REPORT
    # ========================================================================

    def _get_agent_state_safe(self) -> Dict[str, Any]:
        """Bezpieczne pobranie stanu agenta z fallback"""
        try:
            return self.agent.get_enhanced_state_summary()
        except AttributeError:
            # Fallback dla podstawowego CognitiveAgent
            return {
                'cycle': getattr(self.agent, 'cycle_count', 0),
                'goal': getattr(self.agent, 'current_goal', 'unknown'),
                'working_memory_items': len(getattr(self.agent.workspace, 'working_memory', [])),
                'world_objects': len(getattr(self.agent.world_model, 'objects', {})),
                'episodes': len(getattr(self.agent.memory, 'episodic_memory', [])),
                'emotions': [e.value for e in getattr(self.agent.emotion_module, 'current_emotions', [])],
                'emergent_metrics': {'chaos_level': 0.0},
                'adaptive_behavior_mode': 'balanced'
            }
    
    def generate_hama_report(self):
        print("\n" + "="*70)
        print("💎 HAMA DIAMOND - COMPREHENSIVE REPORT")
        print("="*70)

        # Calculate overall HAMA Diamond score
        scores = {
            'G': self.results.get('generalization', {}).get('score', 0),
            'Q': self.results.get('quality', {}).get('score', 0),
            'P': self.results.get('performance', {}).get('score', 0),
            'A': self.results.get('adaptation', {}).get('score', 0)
        }

        overall_score = np.mean(list(scores.values()))

        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'agent_state': self._get_agent_state_safe(),
            'hama_scores': scores,
            'overall_score': overall_score,
            'detailed_results': self.results,
            'grade': self._calculate_grade(overall_score)
        }

        # Save report
        with open('hama_diamond_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print("\n📊 HAMA DIAMOND SCORES:")
        print(f"  G (Generalization): {scores['G']*100:.1f}/100")
        print(f"  Q (Quality):        {scores['Q']*100:.1f}/100")
        print(f"  P (Performance):    {scores['P']*100:.1f}/100")
        print(f"  A (Adaptation):     {scores['A']*100:.1f}/100")
        print(f"\n  OVERALL:            {overall_score*100:.1f}/100")
        print(f"  GRADE:              {report['grade']}")

        print("\nOK Report saved: hama_diamond_report.json")

        return report

    def _calculate_grade(self, score):
        if score >= 0.9:
            return "💎 DIAMOND"
        elif score >= 0.8:
            return "🏆 PLATINUM"
        elif score >= 0.7:
            return "🥇 GOLD"
        elif score >= 0.6:
            return "🥈 SILVER"
        elif score >= 0.5:
            return "🥉 BRONZE"
        else:
            return "📊 DEVELOPING"

    def plot_hama_results(self):
        if not PLOTTING_AVAILABLE:
            print("⚠️ Matplotlib nie dostępne - pomijam wizualizacje")
            return
        
        print("\n📊 Generating HAMA Diamond visualizations...")

        fig = plt.figure(figsize=(16, 10))
        if fig is None:
            print("⚠️ Nie można utworzyć figury - pomijam wizualizacje")
            return
        
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)  # type: ignore

        # 1. HAMA Diamond Radar Chart
        ax1 = fig.add_subplot(gs[0, :], projection='polar')  # type: ignore
        categories = ['G\nGeneralization', 'Q\nQuality', 'P\nPerformance', 'A\nAdaptation']
        values = [
            self.results.get('generalization', {}).get('score', 0),
            self.results.get('quality', {}).get('score', 0),
            self.results.get('performance', {}).get('score', 0),
            self.results.get('adaptation', {}).get('score', 0)
        ]

        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        values += values[:1]
        angles += angles[:1]

        ax1.plot(angles, values, 'o-', linewidth=3, color='#4ECDC4', markersize=10)
        ax1.fill(angles, values, alpha=0.25, color='#4ECDC4')
        ax1.set_xticks(angles[:-1])
        ax1.set_xticklabels(categories, size=12)
        ax1.set_ylim(0, 1)
        ax1.set_title('HAMA Diamond Profile', fontsize=16, fontweight='bold', pad=20)
        ax1.grid(True)

        # 2. Generalization Discovery
        if 'generalization' in self.results:
            ax2 = fig.add_subplot(gs[1, 0])  # type: ignore
            discovery = self.results['generalization']['discovery_rate']
            ax2.plot(discovery, 'b-', linewidth=2)
            ax2.set_title('G: Transfer Learning', fontweight='bold')
            ax2.set_xlabel('Cycle')
            ax2.set_ylabel('Objects Discovered')
            ax2.grid(True, alpha=0.3)

        # 3. Quality Robustness
        if 'quality' in self.results:
            ax3 = fig.add_subplot(gs[1, 1])  # type: ignore
            recovery_times = self.results['quality']['recovery_times']
            ax3.hist(recovery_times, bins=10, color='orange', alpha=0.7, edgecolor='black')
            ax3.set_title('Q: Robustness Recovery', fontweight='bold')
            ax3.set_xlabel('Recovery Time (cycles)')
            ax3.set_ylabel('Frequency')
            ax3.grid(True, alpha=0.3, axis='y')

        plt.suptitle('HAMA DIAMOND TEST RESULTS', fontsize=18, fontweight='bold')
        plt.savefig('hama_diamond_results.png', dpi=300, bbox_inches='tight')
        print("OK Visualization saved: hama_diamond_results.png")
        plt.show()

print("OK HAMA Diamond Tests zdefiniowane")
print("\n" + "="*70)
print("CZESC 6 ZAKONCZONA - Przejdz do CZESCI 7 (Uruchomienie)")
print("="*70)
