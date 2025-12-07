"""
🚀 GQPA DIAMOND - CZĘŚĆ 8: PRODUCTION DEPLOYMENT
Gotowe do wklejenia w Google Colab

⚠️ BACKGROUND IP - NIE PODLEGA PRZENIESIENIU PRAW
Copyright © 2024-2025 Jakub Szych & Michał Wojtków
"""

import os
import sys
import pickle
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import gzip
import base64

# Opcjonalne importy
try:
    import cloudpickle  # type: ignore
    CLOUDPICKLE_AVAILABLE = True
except ImportError:
    CLOUDPICKLE_AVAILABLE = False
    cloudpickle = pickle  # Fallback do standardowego pickle
    print("⚠️ cloudpickle nie dostępne - używam standardowego pickle")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️ numpy nie dostępne - niektóre funkcje będą ograniczone")

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    # Fallback dla tqdm
    def tqdm(iterable, desc=None, **kwargs):
        return iterable
    print("⚠️ tqdm nie dostępne - pasek postępu wyłączony")

print("""
╔══════════════════════════════════════════════════════════════════╗
║              🚀 PRODUCTION DEPLOYMENT SYSTEM 🚀                  ║
║                                                                  ║
║  Opcje deployment:                                              ║
║  1. Save/Load Agent State (pickle)                              ║
║  2. Export to REST API                                          ║
║  3. Batch Processing Mode                                       ║
║  4. Checkpoint System                                           ║
║  5. Cloud Storage Integration                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")

# ============================================================================
# 1. AGENT STATE MANAGEMENT
# ============================================================================

class AgentStateManager:
    """Zarządzanie stanem agenta - save/load/checkpoint"""
    
    def __init__(self, agent, adapter):
        self.agent = agent
        self.adapter = adapter
        self.checkpoint_dir = "/content/checkpoints"
        self._ensure_checkpoint_dir()
    
    def _ensure_checkpoint_dir(self):
        if not os.path.exists(self.checkpoint_dir):
            os.makedirs(self.checkpoint_dir)
    
    def save_agent(self, filename="agent_production.pkl", compress=True):
        """
        Zapisuje pełny stan agenta
        
        Args:
            filename: nazwa pliku
            compress: czy kompresować (zalecane dla dużych agentów)
        """
        print(f"\n💾 Zapisywanie agenta: {filename}")
        
        # Przygotuj dane do zapisu
        state = {
            'agent_state': self._serialize_agent_state(),
            'adapter_state': self._serialize_adapter_state(),
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'cycles': self.agent.cycle_count,
                'learning_progress': self.agent.emergent_integrator.get_integration_status()['emergent_metrics']['learning_progress'],
                'version': '1.0.0'
            }
        }
        
        filepath = f"{self.checkpoint_dir}/{filename}"
        
        if compress:
            with gzip.open(filepath + '.gz', 'wb') as f:
                if CLOUDPICKLE_AVAILABLE:
                    cloudpickle.dump(state, f)
                else:
                    pickle.dump(state, f)
            print(f"✅ Agent zapisany (skompresowany): {filepath}.gz")
            if os.path.exists(filepath + '.gz'):
                print(f"   Rozmiar: {os.path.getsize(filepath + '.gz') / 1024:.2f} KB")
        else:
            with open(filepath, 'wb') as f:
                if CLOUDPICKLE_AVAILABLE:
                    cloudpickle.dump(state, f)
                else:
                    pickle.dump(state, f)
            print(f"✅ Agent zapisany: {filepath}")
            if os.path.exists(filepath):
                print(f"   Rozmiar: {os.path.getsize(filepath) / 1024:.2f} KB")
        
        return filepath
    
    def load_agent(self, filename="agent_production.pkl", compressed=True):
        """
        Wczytuje stan agenta
        
        Args:
            filename: nazwa pliku
            compressed: czy plik jest skompresowany
        """
        print(f"\n📂 Wczytywanie agenta: {filename}")
        
        filepath = f"{self.checkpoint_dir}/{filename}"
        if compressed:
            filepath += '.gz'
        
        if compressed:
            with gzip.open(filepath, 'rb') as f:
                if CLOUDPICKLE_AVAILABLE:
                    state = cloudpickle.load(f)
                else:
                    state = pickle.load(f)
        else:
            with open(filepath, 'rb') as f:
                if CLOUDPICKLE_AVAILABLE:
                    state = cloudpickle.load(f)
                else:
                    state = pickle.load(f)
        
        print(f"✅ Agent wczytany!")
        print(f"   Timestamp: {state['metadata']['timestamp']}")
        print(f"   Cycles: {state['metadata']['cycles']}")
        print(f"   Learning: {state['metadata']['learning_progress']*100:.1f}%")
        
        # Przywróć stan
        self._deserialize_agent_state(state['agent_state'])
        self._deserialize_adapter_state(state['adapter_state'])
        
        return state['metadata']
    
    def _serialize_agent_state(self):
        """Serializacja stanu agenta"""
        return {
            'cycle_count': self.agent.cycle_count,
            'current_goal': self.agent.current_goal,
            'world_model_objects': dict(self.agent.world_model.objects),
            'episodic_memory': self.agent.memory.episodic_memory[-100:],  # Last 100
            'semantic_memory': dict(self.agent.memory.semantic_memory),
            'emergent_metrics': self.agent.emergent_integrator.get_integration_status()['emergent_metrics'],
            'adaptive_behavior_mode': self.agent.adaptive_behavior_mode
        }
    
    def _serialize_adapter_state(self):
        """Serializacja stanu adaptera"""
        return {
            'interaction_log': self.adapter.interaction_log[-50:],  # Last 50
            'conversation_history': self.adapter.conversation_history[-20:]  # Last 20
        }
    
    def _deserialize_agent_state(self, state):
        """Deserializacja stanu agenta"""
        self.agent.cycle_count = state['cycle_count']
        self.agent.current_goal = state['current_goal']
        self.agent.world_model.objects = state['world_model_objects']
        self.agent.memory.semantic_memory = state['semantic_memory']
        self.agent.adaptive_behavior_mode = state['adaptive_behavior_mode']
        # Note: episodic memory można dodać, ale wymaga rekonstrukcji Episode obiektów
    
    def _deserialize_adapter_state(self, state):
        """Deserializacja stanu adaptera"""
        self.adapter.interaction_log = state['interaction_log']
        self.adapter.conversation_history = state['conversation_history']
    
    def create_checkpoint(self, name=None):
        """Tworzy checkpoint z timestamp"""
        if name is None:
            name = f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return self.save_agent(f"{name}.pkl", compress=True)
    
    def list_checkpoints(self):
        """Lista dostępnych checkpointów"""
        import os
        checkpoints = [f for f in os.listdir(self.checkpoint_dir) if f.endswith('.pkl.gz')]
        print(f"\n📋 Dostępne checkpointy ({len(checkpoints)}):")
        for i, cp in enumerate(checkpoints, 1):
            size = os.path.getsize(f"{self.checkpoint_dir}/{cp}") / 1024
            print(f"   {i}. {cp} ({size:.2f} KB)")
        return checkpoints

print("✅ AgentStateManager zdefiniowany")

# ============================================================================
# 2. REST API WRAPPER
# ============================================================================

class AgentAPIWrapper:
    """REST API wrapper dla agenta"""
    
    def __init__(self, agent, adapter):
        self.agent = agent
        self.adapter = adapter
        self.request_count = 0
        self.start_time = time.time()
    
    def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Przetwarza request API
        
        Request format:
        {
            "action": "query" | "goal" | "cycle" | "status",
            "data": {...}
        }
        """
        self.request_count += 1
        start = time.time()
        
        action = request_data.get('action', 'status')
        data = request_data.get('data', {})
        
        try:
            if action == 'query':
                result = self._handle_query(data)
            elif action == 'goal':
                result = self._handle_goal(data)
            elif action == 'cycle':
                result = self._handle_cycle(data)
            elif action == 'status':
                result = self._handle_status(data)
            else:
                result = {"error": f"Unknown action: {action}"}
            
            response = {
                "success": True,
                "action": action,
                "result": result,
                "processing_time_ms": (time.time() - start) * 1000,
                "request_id": self.request_count,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            response = {
                "success": False,
                "error": str(e),
                "action": action,
                "request_id": self.request_count,
                "timestamp": datetime.now().isoformat()
            }
        
        return response
    
    def _handle_query(self, data):
        """Handle Gemini query"""
        prompt = data.get('prompt', '')
        if not prompt:
            return {"error": "No prompt provided"}
        
        response = self.adapter.cognitive_query(prompt)
        return {
            "response": response['response'],
            "latency_ms": response['latency'] * 1000,
            "cognitive_state": response['cognitive_state']
        }
    
    def _handle_goal(self, data):
        """Handle goal setting"""
        new_goal = data.get('goal', '')
        if not new_goal:
            return {"error": "No goal provided"}
        
        old_goal = self.agent.current_goal
        self.agent.set_goal(new_goal)
        
        return {
            "old_goal": old_goal,
            "new_goal": new_goal,
            "behavior_mode": self.agent.adaptive_behavior_mode
        }
    
    def _handle_cycle(self, data):
        """Handle cognitive cycles"""
        n_cycles = data.get('cycles', 1)
        n_cycles = min(n_cycles, 100)  # Limit to 100
        
        start_cycle = self.agent.cycle_count
        
        for _ in range(n_cycles):
            self.agent.cognitive_cycle()
        
        return {
            "cycles_executed": n_cycles,
            "total_cycles": self.agent.cycle_count,
            "new_objects": len(self.agent.world_model.objects),
            "episodes": len(self.agent.memory.episodic_memory)
        }
    
    def _handle_status(self, data):
        """Handle status request"""
        return self.agent.get_enhanced_state_summary()
    
    def get_api_stats(self):
        """Statystyki API"""
        uptime = time.time() - self.start_time
        return {
            "total_requests": self.request_count,
            "uptime_seconds": uptime,
            "requests_per_minute": (self.request_count / uptime) * 60 if uptime > 0 else 0,
            "agent_cycles": self.agent.cycle_count
        }

print("✅ AgentAPIWrapper zdefiniowany")

# ============================================================================
# 3. BATCH PROCESSOR
# ============================================================================

class BatchProcessor:
    """Przetwarzanie wsadowe zadań"""
    
    def __init__(self, agent, adapter):
        self.agent = agent
        self.adapter = adapter
        self.jobs = []
        self.results = []
    
    def add_job(self, job_type: str, params: Dict[str, Any], priority: int = 5):
        """
        Dodaje zadanie do kolejki
        
        Args:
            job_type: 'goal' | 'cycles' | 'query' | 'analysis'
            params: parametry zadania
            priority: priorytet (1-10, 10=najwyższy)
        """
        job = {
            'id': len(self.jobs) + 1,
            'type': job_type,
            'params': params,
            'priority': priority,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        self.jobs.append(job)
        print(f"✅ Dodano zadanie #{job['id']}: {job_type}")
        return job['id']
    
    def process_batch(self, max_jobs: Optional[int] = None):
        """Przetwarza wszystkie zadania"""
        print(f"\n🔄 Przetwarzanie {len(self.jobs)} zadań...")
        
        # Sortuj po priorytecie
        self.jobs.sort(key=lambda x: x['priority'], reverse=True)
        
        jobs_to_process = self.jobs[:max_jobs] if max_jobs is not None else self.jobs
        
        if TQDM_AVAILABLE:
            iterator = tqdm(jobs_to_process, desc="Processing jobs")
        else:
            iterator = jobs_to_process
            print(f"Przetwarzanie {len(jobs_to_process)} zadań...")
        
        for i, job in enumerate(iterator):
            result = self._process_job(job)
            self.results.append(result)
            job['status'] = 'completed'
        
        print(f"✅ Przetworzono {len(jobs_to_process)} zadań")
        return self.results
    
    def _process_job(self, job):
        """Przetwarza pojedyncze zadanie"""
        start = time.time()
        
        try:
            if job['type'] == 'goal':
                self.agent.set_goal(job['params']['goal'])
                output = {'goal_set': job['params']['goal']}
            
            elif job['type'] == 'cycles':
                n = job['params'].get('cycles', 10)
                for _ in range(n):
                    self.agent.cognitive_cycle()
                output = {'cycles_completed': n}
            
            elif job['type'] == 'query':
                response = self.adapter.cognitive_query(job['params']['prompt'])
                output = {'response': response['response'][:200]}
            
            elif job['type'] == 'analysis':
                output = self.agent.get_enhanced_state_summary()
            
            else:
                output = {'error': 'Unknown job type'}
            
            return {
                'job_id': job['id'],
                'type': job['type'],
                'success': True,
                'output': output,
                'processing_time': time.time() - start
            }
        
        except Exception as e:
            return {
                'job_id': job['id'],
                'type': job['type'],
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start
            }
    
    def get_summary(self):
        """Podsumowanie batch processing"""
        total = len(self.jobs)
        completed = sum(1 for j in self.jobs if j['status'] == 'completed')
        pending = total - completed
        
        if self.results:
            avg_time = np.mean([r['processing_time'] for r in self.results])
            success_rate = sum(1 for r in self.results if r['success']) / len(self.results)
        else:
            avg_time = 0
            success_rate = 0
        
        return {
            'total_jobs': total,
            'completed': completed,
            'pending': pending,
            'avg_processing_time': avg_time,
            'success_rate': success_rate
        }

print("✅ BatchProcessor zdefiniowany")

# ============================================================================
# 4. MONITORING & LOGGING
# ============================================================================

class ProductionMonitor:
    """Monitoring produkcyjny agenta"""
    
    def __init__(self, agent):
        self.agent = agent
        self.metrics_history = []
        self.alerts = []
        self.start_time = time.time()
    
    def collect_metrics(self):
        """Zbiera metryki"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'uptime': time.time() - self.start_time,
            'cycles': self.agent.cycle_count,
            'learning_progress': self.agent.emergent_integrator.get_integration_status()['emergent_metrics']['learning_progress'],
            'chaos_level': self.agent.emergent_integrator.get_integration_status()['emergent_metrics']['chaos_level'],
            'world_objects': len(self.agent.world_model.objects),
            'episodes': len(self.agent.memory.episodic_memory),
            'semantic_concepts': len(self.agent.memory.semantic_memory)
        }
        
        self.metrics_history.append(metrics)
        self._check_alerts(metrics)
        
        return metrics
    
    def _check_alerts(self, metrics):
        """Sprawdza alerty"""
        # Alert: Chaos za wysoki
        if metrics['chaos_level'] > 0.35:
            self.alerts.append({
                'level': 'WARNING',
                'message': f"High chaos level: {metrics['chaos_level']:.3f}",
                'timestamp': metrics['timestamp']
            })
        
        # Alert: Brak postępu
        if len(self.metrics_history) > 10:
            recent_progress = [m['learning_progress'] for m in self.metrics_history[-10:]]
            if max(recent_progress) - min(recent_progress) < 0.01:
                self.alerts.append({
                    'level': 'INFO',
                    'message': "Learning progress plateau detected",
                    'timestamp': metrics['timestamp']
                })
    
    def get_health_status(self):
        """Status zdrowia systemu"""
        if not self.metrics_history:
            return "UNKNOWN"
        
        latest = self.metrics_history[-1]
        recent_alerts = [a for a in self.alerts if 'WARNING' in a['level']][-5:]
        
        if len(recent_alerts) > 3:
            return "DEGRADED"
        elif latest['chaos_level'] > 0.4:
            return "WARNING"
        else:
            return "HEALTHY"
    
    def generate_report(self):
        """Generuje raport monitoringu"""
        health = self.get_health_status()
        latest = self.metrics_history[-1] if self.metrics_history else {}
        
        print("\n" + "="*70)
        print("📊 PRODUCTION MONITORING REPORT")
        print("="*70)
        print(f"\n🏥 Health Status: {health}")
        print(f"\n📈 Current Metrics:")
        for key, value in latest.items():
            if isinstance(value, float):
                print(f"   {key}: {value:.3f}")
            else:
                print(f"   {key}: {value}")
        
        if self.alerts:
            print(f"\n⚠️  Recent Alerts ({len(self.alerts)}):")
            for alert in self.alerts[-5:]:
                print(f"   [{alert['level']}] {alert['message']}")
        
        return {
            'health': health,
            'metrics': latest,
            'alerts': self.alerts[-10:]
        }

print("✅ ProductionMonitor zdefiniowany")

# ============================================================================
# 5. DEPLOYMENT MANAGER - GŁÓWNA KLASA
# ============================================================================

class DeploymentManager:
    """Główny manager deployment"""
    
    def __init__(self, agent, adapter):
        self.agent = agent
        self.adapter = adapter
        self.state_manager = AgentStateManager(agent, adapter)
        self.api_wrapper = AgentAPIWrapper(agent, adapter)
        self.batch_processor = BatchProcessor(agent, adapter)
        self.monitor = ProductionMonitor(agent)
        
        print("\n✅ Deployment Manager zainicjalizowany")
        print("   - State Management: ✓")
        print("   - API Wrapper: ✓")
        print("   - Batch Processor: ✓")
        print("   - Production Monitor: ✓")
    
    def quick_save(self):
        """Szybki zapis stanu"""
        return self.state_manager.create_checkpoint()
    
    def quick_load(self, checkpoint_name):
        """Szybkie wczytanie checkpointu"""
        return self.state_manager.load_agent(checkpoint_name, compressed=True)
    
    def health_check(self):
        """Sprawdzenie zdrowia systemu"""
        self.monitor.collect_metrics()
        return self.monitor.get_health_status()
    
    def full_status(self):
        """Pełny status deployment"""
        print("\n" + "="*70)
        print("🚀 DEPLOYMENT STATUS")
        print("="*70)
        
        # Agent status
        state = self.agent.get_enhanced_state_summary()
        print(f"\n🤖 Agent Status:")
        print(f"   Cycles: {state['cycle']}")
        print(f"   Learning: {state['emergent_metrics']['learning_progress']*100:.1f}%")
        print(f"   Mode: {state['adaptive_behavior_mode']}")
        
        # API stats
        api_stats = self.api_wrapper.get_api_stats()
        print(f"\n🌐 API Stats:")
        print(f"   Requests: {api_stats['total_requests']}")
        print(f"   Uptime: {api_stats['uptime_seconds']:.1f}s")
        print(f"   RPM: {api_stats['requests_per_minute']:.2f}")
        
        # Batch stats
        batch_stats = self.batch_processor.get_summary()
        print(f"\n📦 Batch Stats:")
        print(f"   Jobs: {batch_stats['completed']}/{batch_stats['total_jobs']}")
        print(f"   Success: {batch_stats['success_rate']*100:.1f}%")
        
        # Health
        health = self.health_check()
        print(f"\n🏥 Health: {health}")
        
        return {
            'agent': state,
            'api': api_stats,
            'batch': batch_stats,
            'health': health
        }

print("✅ DeploymentManager zdefiniowany")

print("\n" + "="*70)
print("CZĘŚĆ 8 ZAKOŃCZONA - Deployment System Gotowy!")
print("="*70)
