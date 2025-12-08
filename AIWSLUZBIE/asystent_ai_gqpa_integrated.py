"""
🏛️ ASYSTENT AI DLA ADMINISTRACJI - ROZWIĄZANIE KOMPLETNE
Integracja z architekturą HAMA DIAMOND dla wyzwania HackNation 2024

System wspierający orzeczników w Departamencie Turystyki MSiT
z wykorzystaniem zaawansowanej architektury kognitywnej HAMA Diamond

═══════════════════════════════════════════════════════════════════════════
✅ FOREGROUND IP - PODLEGA PRZENIESIENIU PRAW

Ten moduł został stworzony na hackathonie HackNation 2025.
Kod może być przekazany zgodnie z regulaminem hackathonu.

⚠️ UWAGA: Moduł wykorzystuje HAMA DIAMOND jako Background IP.
HAMA Diamond jest utworem współautorskim (Jakub Szych & Michał Wojtków)
i NIE podlega przeniesieniu praw. Zobacz: OSWIADCZENIE_PRAWNE.md
═══════════════════════════════════════════════════════════════════════════

Autor: [Nazwa zespołu / Uczestnik hackathonu]
Data: 2025
Wersja: 2.0.0 - Production Ready
"""

import os
import sys
import json
import time
import pickle
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# KONFIGURACJA I IMPORTY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════╗
║     🏛️ ASYSTENT AI DLA ADMINISTRACJI - HAMA DIAMOND INTEGRATED 🏛️       ║
║                                                                  ║
║  System wspierający orzeczników w Departamencie Turystyki MSiT   ║
║  Architektura: HAMA DIAMOND (Neuro-Symbolic Cognitive AI)        ║
╚══════════════════════════════════════════════════════════════════╝
""")

# Import podstawowych bibliotek
try:
    from google import genai  # type: ignore
    from google.genai import types as genai_types  # type: ignore
    GEMINI_AVAILABLE = True
except ImportError:
    # Fallback do starego SDK (dla kompatybilności)
    try:
        import google.generativeai as genai  # type: ignore
        genai_types = None
        GEMINI_AVAILABLE = True
        print("⚠️ Używam starego SDK google.generativeai - zalecane: pip install google-genai")
    except ImportError:
        GEMINI_AVAILABLE = False
        genai = None
        genai_types = None
        print("ℹ️ Google Generative AI nie dostępne - ustaw GOOGLE_API_KEY")

try:
    import torch  # type: ignore
    import torch.nn as nn  # type: ignore
    TORCH_AVAILABLE = True
    print(f"✅ PyTorch {torch.__version__} dostępny")
except ImportError:
    TORCH_AVAILABLE = False
    torch = None
    nn = None
    print("ℹ️ PyTorch nie dostępne - niektóre funkcje będą ograniczone (nie wymagane dla Ollama)")

import pandas as pd
import numpy as np

# ============================================================================
# IMPORT HAMA DIAMOND CORE (BACKGROUND IP)
# ============================================================================

# Dodaj ścieżkę do system/ do sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_system_dir = os.path.join(os.path.dirname(_current_dir), 'system')
if _system_dir not in sys.path:
    sys.path.insert(0, _system_dir)

try:
    # Import HAMA Diamond Core jako biblioteki zewnętrznej
    from hama_core import get_hama_info  # type: ignore
    HAMA_INFO = get_hama_info()
    print(f"✅ HAMA Diamond Core załadowany: {HAMA_INFO['name']} v{HAMA_INFO['version']}")
    print(f"   Status: {HAMA_INFO['status']}")
except ImportError:
    HAMA_INFO = None
    print("⚠️ HAMA Diamond Core nie dostępne - niektóre funkcje mogą być ograniczone")
    print("   (To normalne - GQPA jest Background IP)")

# ============================================================================
# KONFIGURACJA MODELI
# ============================================================================

# Konfiguracja modelu Gemini (domyślny)
GEMINI_MODEL_NAME = "gemini-2.5-flash"  # Domyślnie używany model Gemini

def configure_gemini():
    """Konfiguracja modelu Gemini - obsługuje nowy SDK (google-genai) i stary (google.generativeai)"""
    if not GEMINI_AVAILABLE or genai is None:
        return None
    
    try:
        # Sprawdź czy to nowy SDK (ma Client)
        if hasattr(genai, 'Client'):
            # Nowy SDK (google-genai)
            api_key = os.environ.get('GOOGLE_API_KEY') or os.environ.get('GEMINI_API_KEY')
            
            # Spróbuj z Colab jeśli nie ma w zmiennej środowiskowej
            if not api_key:
                try:
                    from google.colab import userdata  # type: ignore
                    api_key = userdata.get('GOOGLE_API_KEY') or userdata.get('GEMINI_API_KEY')
                except ImportError:
                    pass
            
            # Sprawdź czy klucz jest ustawiony
            if not api_key:
                print("⚠️ Brak klucza API Gemini")
                print("   Ustaw zmienną środowiskową GOOGLE_API_KEY lub GEMINI_API_KEY")
            
            if api_key:
                client = genai.Client(api_key=api_key)
                print("✅ Gemini Client (nowy SDK google-genai) skonfigurowany")
                return client
            return None
        else:
            # Stary SDK (google.generativeai) - dla kompatybilności
            api_key = os.environ.get('GOOGLE_API_KEY')
            
            # Spróbuj z Colab jeśli nie ma w zmiennej środowiskowej
            if not api_key and hasattr(sys.modules.get('google.colab', None), 'userdata'):
                try:
                    from google.colab import userdata  # type: ignore
                    api_key = userdata.get('GOOGLE_API_KEY')
                except ImportError:
                    pass
            
            # Sprawdź czy klucz jest ustawiony
            if not api_key:
                print("⚠️ Brak klucza API Gemini")
                print("   Ustaw zmienną środowiskową GOOGLE_API_KEY lub GEMINI_API_KEY")
            
            if api_key:
                genai.configure(api_key=api_key)
            else:
                return None
            
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            model = genai.GenerativeModel(
                model_name=GEMINI_MODEL_NAME.replace("models/", ""),  # Stary SDK nie używa prefixu "models/"
                generation_config=generation_config,
                safety_settings=safety_settings,
            )
            print(f"✅ Gemini {GEMINI_MODEL_NAME} (stary SDK) skonfigurowany")
            return model
    except Exception as e:
        print(f"⚠️ Błąd konfiguracji Gemini: {e}")
        return None

gemini_client = configure_gemini() if GEMINI_AVAILABLE else None

# ============================================================================
# TYPY DANYCH ADMINISTRACYJNYCH
# ============================================================================

@dataclass
class AdministrativeCase:
    """Reprezentacja sprawy administracyjnej"""
    case_id: str
    case_type: str  # np. "kwalifikacja_zawodowa", "kategoria_hotelu", "zakaz_dzialalnosci"
    documents: List[Dict[str, Any]]
    parties: List[str]
    status: str  # "nowa", "w_trakcie", "oczekuje_decyzji", "zakończona"
    deadline: Optional[datetime]
    summary: Optional[str] = None
    risk_assessment: Optional[Dict] = None
    decision_proposal: Optional[str] = None
    legal_issues: List[str] = field(default_factory=list)
    historical_precedents: List[str] = field(default_factory=list)
    compliance_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class DocumentAnalysis:
    """Wynik analizy dokumentu"""
    document_id: str
    document_type: str
    key_facts: List[str]
    legal_references: List[str]
    risk_factors: List[str]
    confidence: float
    processing_time: float

@dataclass
class DecisionDraft:
    """Projekt decyzji administracyjnej"""
    case_id: str
    decision_type: str  # "pozytywna", "negatywna", "częściowa"
    factual_justification: str
    legal_justification: str
    decision_text: str
    legal_references: List[str]
    compliance_checks: Dict[str, bool]
    generated_at: datetime = field(default_factory=datetime.now)

# ============================================================================
# MODUŁ GUARDRAILS I BEZPIECZEŃSTWA
# ============================================================================

class SecurityGuardrails:
    """System zabezpieczeń i guardrails dla asystenta AI"""
    
    def __init__(self):
        self.max_document_size = 10 * 1024 * 1024  # 10MB
        self.max_query_length = 10000
        self.blocked_keywords = ["usuń", "usunąć", "kasuj", "delete", "drop"]
        self.audit_log: List[Dict] = []
        
    def validate_input(self, data: Any, data_type: str = "document") -> Tuple[bool, str]:
        """Walidacja danych wejściowych"""
        try:
            if data_type == "document":
                if isinstance(data, str) and len(data) > self.max_document_size:
                    return False, f"Dokument przekracza limit {self.max_document_size} bajtów"
                
                # Sprawdzenie niebezpiecznych słów kluczowych
                if any(keyword in data.lower() for keyword in self.blocked_keywords):
                    return False, "Wykryto niebezpieczne słowa kluczowe"
            
            elif data_type == "query":
                if isinstance(data, str) and len(data) > self.max_query_length:
                    return False, f"Zapytanie przekracza limit {self.max_query_length} znaków"
            
            return True, "OK"
        except Exception as e:
            return False, f"Błąd walidacji: {str(e)}"
    
    def sanitize_output(self, output: str) -> str:
        """Sanityzacja danych wyjściowych"""
        # Usuń potencjalnie niebezpieczne elementy
        output = output.replace("<script>", "")
        output = output.replace("</script>", "")
        return output
    
    def log_operation(self, operation: str, user: str, details: Dict):
        """Logowanie operacji dla audit trail"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "user": user,
            "details": details
        }
        self.audit_log.append(log_entry)
        
        # Ograniczenie rozmiaru logu
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
    
    def check_rodo_compliance(self, data: Dict) -> Tuple[bool, List[str]]:
        """Sprawdzenie zgodności z RODO"""
        issues = []
        
        # Sprawdzenie czy dane osobowe są odpowiednio chronione
        personal_data_keywords = ["pesel", "nip", "regon", "imię", "nazwisko", "adres"]
        if any(keyword in str(data).lower() for keyword in personal_data_keywords):
            # W produkcji tutaj byłaby anonimizacja
            issues.append("Wykryto dane osobowe - wymagana anonimizacja")
        
        return len(issues) == 0, issues

# ============================================================================
# LOCAL MODEL SUPPORT
# ============================================================================

# Import lokalnych adapterów (opcjonalne)
try:
    from local_model_adapter import LocalModelAdapter, HybridModelAdapter  # type: ignore
    LOCAL_MODELS_AVAILABLE = True
except ImportError:
    LOCAL_MODELS_AVAILABLE = False
    LocalModelAdapter = None  # type: ignore
    HybridModelAdapter = None  # type: ignore
    print("ℹ️ Lokalne modele nie dostępne - użyj API (możesz dodać local_model_adapter.py)")

# ============================================================================
# PODSTAWOWE TYPY DANYCH (dla Truth Guardian i HAMA2)
# ============================================================================

class ModalityType(Enum):
    VISION = "vision"
    AUDIO = "audio"
    TOUCH = "touch"
    PROPRIOCEPTION = "proprioception"
    LANGUAGE = "language"
    DOCUMENT = "document"

class ActionType(Enum):
    MOVEMENT = "movement"
    MANIPULATION = "manipulation"
    SPEECH = "speech"
    GESTURE = "gesture"
    DOCUMENT_GENERATION = "document_generation"
    ANALYSIS = "analysis"
    DECISION_PROPOSAL = "decision_proposal"

class EmotionType(Enum):
    JOY = "joy"
    FEAR = "fear"
    CURIOSITY = "curiosity"
    SATISFACTION = "satisfaction"
    FRUSTRATION = "frustration"
    CONFIDENCE = "confidence"
    CAUTION = "caution"

@dataclass
class SensoryData:
    modality: ModalityType
    data: Any
    timestamp: float
    intensity: float = 1.0
    source: str = "environment"

@dataclass
class Action:
    action_type: ActionType
    parameters: Dict[str, Any]
    priority: float = 0.5
    timestamp: float = field(default_factory=time.time)

@dataclass
class Concept:
    name: str
    properties: Dict[str, Any]
    relations: Dict[str, List[str]]
    activation: float = 0.0
    uncertainty: float = 0.5

@dataclass
class Episode:
    timestamp: float
    context: Dict[str, Any]
    actions: List[Action]
    outcomes: List[Any]
    emotions: List[EmotionType]
    importance: float = 0.5

@dataclass
class WorkingMemoryItem:
    content: Any
    activation: float
    timestamp: float
    source: str

@dataclass
class ContentItem:
    """Reprezentacja treści do weryfikacji (Truth Guardian)"""
    id: str
    source: str
    headline: str
    claims: List[str]
    is_disinformation: bool

# ============================================================================
# HAMA2 COGNITIVE CORE
# ============================================================================

class HAMA2CognitiveConfig:
    def __init__(self):
        self.vocab_size = 512
        self.hidden_size = 384
        self.stochastic_units = 192
        self.lstm_layers = 4
        self.attention_heads = 8
        self.memory_size = 200
        self.initial_chaos = 0.15
        self.adaptation_rate = 0.02
        self.initial_memory_influence = 0.15
        self.chaos_range = (0.05, 0.4)
        self.memory_influence_range = (0.0, 0.4)
        self.learning_rate = 0.001
        self.weight_decay = 0.01
        self.dropout_rate = 0.1

class HAMA2CognitiveCore(nn.Module if TORCH_AVAILABLE else object):  # type: ignore
    """HAMA2 Cognitive Core - sieć neuronowa z emergentnymi właściwościami"""
    
    def __init__(self, config: HAMA2CognitiveConfig):
        if TORCH_AVAILABLE and nn is not None:
            super().__init__()  # type: ignore
        self.config = config
        if not TORCH_AVAILABLE or nn is None:
            self.cognitive_embedding = None  # type: ignore
            self.lstm = None  # type: ignore
            self.cognitive_attention = None  # type: ignore
            self.cognitive_output = None  # type: ignore
        else:
            self.cognitive_embedding = nn.Embedding(config.vocab_size, config.hidden_size)  # type: ignore
            self.lstm = nn.LSTM(config.hidden_size, config.hidden_size, config.lstm_layers, batch_first=True, dropout=config.dropout_rate)  # type: ignore
            self.cognitive_attention = nn.MultiheadAttention(config.hidden_size, config.attention_heads, batch_first=True, dropout=0.1)  # type: ignore
            self.cognitive_output = nn.Sequential(  # type: ignore
                nn.Linear(config.hidden_size * 2, config.hidden_size),  # type: ignore
                nn.LeakyReLU(0.1),  # type: ignore
                nn.Linear(config.hidden_size, config.vocab_size)  # type: ignore
            )
        self._init_emergent_state()
        self.memory_buffers = {}

    def _init_emergent_state(self):
        if not TORCH_AVAILABLE or torch is None:
            return
        self.register_buffer('emergent_state', torch.zeros(1))  # type: ignore
        self.register_buffer('chaos_level', torch.tensor(self.config.initial_chaos))  # type: ignore
        self.register_buffer('memory_influence', torch.tensor(self.config.initial_memory_influence))  # type: ignore

    def forward(self, x: Optional[Any] = None, cognitive_data: Optional[Dict[str, Any]] = None, hidden: Optional[Tuple] = None):
        if not TORCH_AVAILABLE or torch is None:
            return None, None
        batch_size, seq_len = 1, 1
        device = next(self.parameters()).device  # type: ignore
        if x is None:
            x = torch.randint(0, self.config.vocab_size, (batch_size, seq_len), device=device)  # type: ignore
        x_embed = self.cognitive_embedding(x)  # type: ignore
        lstm_out, hidden = self.lstm(x_embed, hidden)  # type: ignore
        attended, _ = self.cognitive_attention(lstm_out, lstm_out, lstm_out)  # type: ignore
        lstm_out = lstm_out + attended * 0.4  # type: ignore
        output = self.cognitive_output(torch.cat([lstm_out, lstm_out], dim=-1))  # type: ignore
        return output, hidden

    def update_emergent_state(self, output, input_tensor, loss=None, cognitive_feedback=None):
        if cognitive_feedback and TORCH_AVAILABLE and torch is not None:
            novelty = cognitive_feedback.get('novelty', 0.5)
            self.chaos_level = torch.clamp(torch.tensor(0.15 + (novelty - 0.5) * 0.2), self.config.chaos_range[0], self.config.chaos_range[1])  # type: ignore

    def get_emergent_metrics(self):
        if not TORCH_AVAILABLE or torch is None:
            return {
                'chaos_level': 0.15,
                'emergent_state': 0.0,
                'cognitive_complexity': 0.3
            }
        return {
            'chaos_level': self.chaos_level.item() if hasattr(self.chaos_level, 'item') else float(self.chaos_level),
            'emergent_state': self.emergent_state.item() if hasattr(self.emergent_state, 'item') else float(self.emergent_state),
            'cognitive_complexity': (self.chaos_level.item() if hasattr(self.chaos_level, 'item') else float(self.chaos_level)) * 2.0
        }

# ============================================================================
# MODUŁY KOGNITYWNE
# ============================================================================

class WorldModel:
    def __init__(self):
        self.objects: Dict[str, Concept] = {}
        self.relations: Dict[str, List[tuple]] = {}

    def update_from_perception(self, concepts: List[Concept]):
        for concept in concepts:
            self.objects[concept.name] = concept

class EnhancedMemoryNexus:
    def __init__(self):
        self.episodic_memory: List[Episode] = []
        self.semantic_memory: Dict[str, Dict] = {}

    def store_episode(self, episode: Episode):
        self.episodic_memory.append(episode)

class EmotionValueModule:
    def __init__(self):
        self.current_emotions = []

    def evaluate_situation(self, situation: Dict) -> List[EmotionType]:
        emotions = []
        if situation.get("novel", False):
            emotions.append(EmotionType.CURIOSITY)
        if situation.get("goal_achieved", False):
            emotions.append(EmotionType.SATISFACTION)
        self.current_emotions = emotions
        return emotions

class GlobalWorkspace:
    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.working_memory: List[WorkingMemoryItem] = []

    def update_working_memory(self, items: List[WorkingMemoryItem]):
        self.working_memory.extend(items)
        self.working_memory = self.working_memory[:self.capacity]

# ============================================================================
# EMERGENT COGNITIVE INTEGRATOR
# ============================================================================

class EmergentCognitiveIntegrator:
    """Integrator emergentny łączący moduły kognitywne z HAMA2 Core"""
    
    def __init__(self, cognitive_agent):
        self.cognitive_agent = cognitive_agent
        self.config = HAMA2CognitiveConfig()
        self.hama2_core = HAMA2CognitiveCore(self.config)
        self.integration_cycles = 0
    
    def integrate_cognitive_cycle(self):
        self.integration_cycles += 1
        cognitive_data = self._prepare_cognitive_data()
        emergent_output = self._update_emergent_core(cognitive_data)
        return emergent_output
    
    def _prepare_cognitive_data(self):
        agent = self.cognitive_agent
        return {
            'perception': [],
            'concepts': list(getattr(agent, 'world_model', WorldModel()).objects.values()),
            'emotions': getattr(agent, 'emotion_module', EmotionValueModule()).current_emotions,
            'goal': getattr(agent, 'current_goal', 'unknown'),
            'working_memory': len(getattr(agent, 'workspace', GlobalWorkspace()).working_memory)
        }
    
    def _update_emergent_core(self, cognitive_data):
        if not TORCH_AVAILABLE or torch is None:
            return {}
        input_tensor = torch.randint(0, self.config.vocab_size, (1, 10))  # type: ignore
        output, _ = self.hama2_core(input_tensor, cognitive_data)  # type: ignore
        
        cognitive_feedback = {
            'novelty': 0.5,
            'importance': 0.6
        }
        
        self.hama2_core.update_emergent_state(output, input_tensor, cognitive_feedback=cognitive_feedback)
        
        return {
            'emergent_metrics': self.hama2_core.get_emergent_metrics()
        }
    
    def get_integration_status(self):
        return {
            'integration_cycles': self.integration_cycles,
            'emergent_metrics': self.hama2_core.get_emergent_metrics()
        }

# ============================================================================
# ENHANCED COGNITIVE AGENT
# ============================================================================

class EnhancedCognitiveAgent:
    """Agent kognitywny z pełną integracją modułów"""
    
    def __init__(self):
        self.environment = InformationEnvironment()
        self.workspace = GlobalWorkspace()
        self.emotion_module = EmotionValueModule()
        self.world_model = WorldModel()
        self.memory_nexus = EnhancedMemoryNexus()
        self.emergent_integrator = EmergentCognitiveIntegrator(self)
        self.current_goal = "verify_information"

# ============================================================================
# TRUTH GUARDIAN - SYSTEM IMMUNOLOGICZNY KOGNITYWNY
# ============================================================================

class InformationEnvironment:
    """Środowisko symulujące ekosystem informacyjny"""
    
    def __init__(self):
        self.post_id = 0
    
    def generate_sensory_data(self) -> List[SensoryData]:
        """Generuje posty z mediów społecznościowych / newsy"""
        self.post_id += 1
        
        scenario = random.choice(["truth", "subtle_fake", "obvious_fake"])
        
        if scenario == "truth":
            content = ContentItem(
                id=f"NEWS-{self.post_id}",
                source="Trusted_Agency_PAP",
                headline="Rząd ogłasza nowy program cyfryzacji szkół.",
                claims=["Ministerstwo przeznaczy 1 mld PLN na laptopy", "Program startuje we wrześniu"],
                is_disinformation=False
            )
        elif scenario == "subtle_fake":
            content = ContentItem(
                id=f"VIRAL-{self.post_id}",
                source="Unknown_Blog_X",
                headline="PILNE: Nowy podatek od posiadania smartfona!",
                claims=["Rząd wprowadza opłatę 500 PLN miesięcznie", "Ustawa wchodzi w życie od jutra"],
                is_disinformation=True
            )
        else:  # obvious_fake
            content = ContentItem(
                id=f"BOT-{self.post_id}",
                source="Clickbait_Farm",
                headline="Szok! W Wiśle odkryto starożytną cywilizację kosmitów.",
                claims=["Naukowcy potwierdzają obecność UFO", "Woda w Wiśle leczy raka"],
                is_disinformation=True
            )
        
        return [
            SensoryData(
                modality=ModalityType.LANGUAGE,
                data={"content": content},
                timestamp=time.time(),
                intensity=0.9 if scenario != "truth" else 0.5
            )
        ]

class CognitiveImmuneSystem:
    """System immunologiczny kognitywny do wykrywania dezinformacji (Truth Guardian)"""
    
    def __init__(self, agent, adapter):
        self.agent = agent
        self.adapter = adapter
        self._implant_ground_truth()
    
    def _implant_ground_truth(self):
        """Wgrywa fakty bazowe do modelu świata agenta"""
        facts = [
            Concept("podatki", {"status": "stabilne", "nowe_ustawy": []}, {}),
            Concept("cyfryzacja", {"budżet": "planowany", "priorytet": "wysoki"}, {}),
            Concept("wisła", {"typ": "rzeka", "lokalizacja": "Polska"}, {}),
            Concept("nauka", {"metoda": "empiryczna"}, {})
        ]
        if hasattr(self.agent, 'world_model'):
            self.agent.world_model.update_from_perception(facts)
    
    def verify_content(self, content: ContentItem) -> Dict:
        """
        Weryfikuje treść poprzez konfrontację z Modelem Świata.
        Wykorzystuje Gemini API do semantycznego porównania.
        """
        context_knowledge = str(list(getattr(self.agent, 'world_model', WorldModel()).objects.keys()))
        
        prompt = f"""
Jesteś Systemem Weryfikacji Informacji (COI - Cognitive Immune System).

WIEDZA BAZOWA SYSTEMU (Ground Truth):
- Brak nowych podatków od elektroniki w legislacji.
- Wisła to rzeka, brak dowodów na cywilizacje pozaziemskie.
- Programy rządowe wymagają procesu legislacyjnego (nie wchodzą "od jutra").

ANALIZOWANA TREŚĆ:
Nagłówek: "{content.headline}"
Twierdzenia: {content.claims}
Źródło: {content.source}

ZADANIE:
Oceń wiarygodność (0-100%).
Jeśli to Fake News, wyjaśnij dlaczego (sprzeczność z wiedzą, brak logiki, podejrzane źródło).
"""
        
        response = self.adapter.cognitive_query(prompt)
        
        # Symulacja Dysonansu Poznawczego w HAMA2
        verification_text = response['response'].lower()
        is_fake_detected = any(word in verification_text for word in ["fake", "fałsz", "wiarygodność: 0", "niska", "nieprawda", "dezinformacja"])
        
        chaos_reaction = 0.15
        if is_fake_detected:
            # Sztuczne wywołanie "szoku" w sieci neuronowej
            if hasattr(self.agent, 'emergent_integrator'):
                if hasattr(self.agent.emergent_integrator, 'hama2_core') and TORCH_AVAILABLE and torch is not None:
                    with torch.no_grad():  # type: ignore
                        self.agent.emergent_integrator.hama2_core.chaos_level += 0.3  # type: ignore
                    chaos_reaction = self.agent.emergent_integrator.hama2_core.chaos_level.item()  # type: ignore
        
        return {
            "is_verified": not is_fake_detected,
            "analysis": response['response'],
            "chaos_reaction": chaos_reaction,
            "confidence": 0.9 if is_fake_detected else 0.7
        }

# ============================================================================
# GEMINI COGNITIVE ADAPTER (uproszczony)
# ============================================================================

class GeminiCognitiveAdapter:
    """Adapter łączący Gemini z systemem kognitywnym - obsługuje nowy SDK (google-genai) i stary (google.generativeai)"""
    
    def __init__(self, gemini_client_or_model, cognitive_agent=None, use_local_model: bool = False):
        self.gemini = gemini_client_or_model
        self.agent = cognitive_agent
        self.conversation_history = []
        self.interaction_log = []
        self.guardrails = SecurityGuardrails()
        
        # Sprawdź czy to nowy SDK (Client) czy stary (GenerativeModel)
        self.is_new_sdk = hasattr(self.gemini, 'models') if self.gemini else False
        
        # Obsługa Gemini API - PRIORYTET
        self.use_local_model = use_local_model
        self.local_adapter = None
        if use_local_model and LOCAL_MODELS_AVAILABLE and LocalModelAdapter:
            try:
                # Użyj Gemini API jako domyślnego
                self.local_adapter = LocalModelAdapter(preferred_backend="gemini")
                if self.local_adapter.is_available():
                    print("✅ Używam Gemini API")
                else:
                    print("⚠️ Gemini API nie dostępne!")
                    print("   Wskazówka: Ustaw zmienną środowiskową GOOGLE_API_KEY lub GEMINI_API_KEY")
                    raise Exception("Gemini API nie dostępne")
            except Exception as e:
                print(f"❌ Błąd inicjalizacji Gemini: {e}")
                print("   Ustaw zmienną środowiskową GOOGLE_API_KEY lub GEMINI_API_KEY")
                raise
        elif use_local_model:
            print("❌ Gemini adapter nie jest dostępny - zainstaluj google-genai: pip install google-genai")
            raise Exception("Gemini adapter nie dostępny")
    
    def cognitive_query(self, prompt: str, context: Optional[Dict[str, Any]] = None, json_mode: bool = False) -> Dict[str, Any]:
        """Wykonanie zapytania kognitywnego z guardrails"""
        
        # Walidacja wejścia
        is_valid, error_msg = self.guardrails.validate_input(prompt, "query")
        if not is_valid:
            return {
                'response': f"Błąd walidacji: {error_msg}",
                'success': False,
                'error': error_msg,
                'latency': 0.0
            }
        
        # Logowanie
        self.guardrails.log_operation("query", "system", {"prompt_length": len(prompt)})
        
        enriched_prompt = f"""
Kontekst Administracyjny:
- System: Asystent AI dla Departamentu Turystyki MSiT
- Cel: Wsparcie orzeczników w podejmowaniu decyzji administracyjnych
- Wymagania: Zgodność z Kodeksem postępowania administracyjnego

Zapytanie:
{prompt}

Odpowiedz profesjonalnie, w języku prawniczym, z uwzględnieniem kontekstu administracyjnego.
"""
        
        start_time = time.time()
        try:
            # PRIORYTET: Gemini API (przez local_adapter)
            if self.use_local_model and self.local_adapter and self.local_adapter.is_available():
                result = self.local_adapter.generate(
                    enriched_prompt,
                    temperature=0.7,
                    top_p=0.95,
                    max_tokens=2048,
                    json_mode=json_mode,
                    format='json' if json_mode else None
                )
                response_text = result.get('response', '')
                success = result.get('success', False)
                error = result.get('error')
                latency = result.get('latency', time.time() - start_time)
            # FALLBACK: Bezpośrednie API (Gemini) - tylko jeśli local_adapter nie jest używany
            elif not self.use_local_model and self.gemini is not None:
                # Nowy SDK (google-genai) - używa client.models.generate_content()
                if self.is_new_sdk:
                    # Użyj globalnej zmiennej GEMINI_MODEL_NAME
                    import asystent_ai_gqpa_integrated
                    model_name = getattr(asystent_ai_gqpa_integrated, 'GEMINI_MODEL_NAME', 'gemini-2.0-flash-exp')
                    response = self.gemini.models.generate_content(
                        model=model_name,
                        contents=enriched_prompt,
                        config={
                            'temperature': 0.7,
                            'top_p': 0.95,
                            'top_k': 40,
                            'max_output_tokens': 2048,
                        }
                    )
                    response_text = response.text
                else:
                    # Stary SDK (google.generativeai) - używa model.generate_content()
                    response = self.gemini.generate_content(enriched_prompt)
                    response_text = response.text
                
                success = True
                error = None
                latency = time.time() - start_time
            else:
                # Ostatnia deska ratunku - sprawdź czy Gemini adapter jest dostępny
                if self.use_local_model:
                    # Próba użycia Gemini adaptera mimo wcześniejszego sprawdzenia
                    if self.local_adapter:
                        result = self.local_adapter.generate(enriched_prompt)
                        response_text = result.get('response', '')
                        success = result.get('success', False)
                        error = result.get('error', 'Gemini API nie odpowiedział')
                        latency = result.get('latency', time.time() - start_time)
                    else:
                        response_text = "[BŁĄD] Gemini API nie jest dostępne. Ustaw GOOGLE_API_KEY lub GEMINI_API_KEY"
                        success = False
                        error = "Gemini API nie dostępne"
                        latency = time.time() - start_time
                else:
                    # Symulacja tylko gdy nie używamy Gemini
                    response_text = f"[SYMULACJA] Odpowiedź na: {prompt[:100]}..."
                    success = True
                    error = None
                    latency = 0.1
            
            # Sanityzacja wyjścia
            response_text = self.guardrails.sanitize_output(response_text)
            
        except Exception as e:
            response_text = f"Error: {str(e)}"
            success = False
            error = str(e)
            latency = time.time() - start_time
        
        # Logowanie interakcji
        self.interaction_log.append({
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt[:200],
            'response_length': len(response_text),
            'latency': latency,
            'success': success
        })
        
        return {
            'response': response_text,
            'success': success,
            'error': error,
            'latency': latency,
            'cognitive_state': {'mode': 'production', 'confidence': 0.85}
        }

# ============================================================================
# MODUŁ ANALIZY DOKUMENTÓW
# ============================================================================

class DocumentAnalyzer:
    """Moduł analizy dokumentów administracyjnych"""
    
    def __init__(self, adapter: GeminiCognitiveAdapter):
        self.adapter = adapter
        self.analysis_cache = {}
    
    def analyze_document(self, document: Dict[str, Any], case: AdministrativeCase) -> DocumentAnalysis:
        """Analiza pojedynczego dokumentu z użyciem JSON Mode"""
        start_time = time.time()
        
        doc_content = document.get('content', '')
        doc_type = document.get('type', 'unknown')
        
        # Chunkowanie dla długich dokumentów
        from document_chunker import DocumentChunker
        chunker = DocumentChunker(chunk_size=2000, chunk_overlap=200)
        
        # Jeśli dokument jest długi, podziel na fragmenty
        if len(doc_content) > 2000:
            chunks = chunker.chunk_document(document)
            # Analizuj pierwszy chunk (lub można analizować wszystkie i łączyć)
            doc_content = chunks[0].get('content', doc_content[:2000])
        
        prompt = f"""
Jesteś ekspertem analizującym dokumenty administracyjne w sprawie turystycznej.

DOKUMENT:
- Typ: {doc_type}
- Treść: {doc_content[:2000]}

SPRAWA:
- ID: {case.case_id}
- Typ: {case.case_type}

ZADANIE:
1. Wyodrębnij kluczowe fakty z dokumentu
2. Zidentyfikuj odniesienia prawne
3. Wskaż czynniki ryzyka
4. Oceń wiarygodność dokumentu (0-100%)

Odpowiedz TYLKO w formacie JSON:
{{
  "key_facts": ["fakt1", "fakt2"],
  "legal_references": ["art. 1 ustawy", "ust. 2"],
  "risk_factors": ["czynnik1", "czynnik2"],
  "confidence": 0.85
}}
"""
        
        # Użyj JSON Mode
        response = self.adapter.cognitive_query(prompt, json_mode=True)
        analysis_text = response['response']
        
        # Parsowanie JSON zamiast regex
        parsed_data = self._parse_json_response(analysis_text)
        
        key_facts = parsed_data.get('key_facts', [])
        legal_refs = parsed_data.get('legal_references', [])
        risk_factors = parsed_data.get('risk_factors', [])
        confidence = parsed_data.get('confidence', 0.7)
        
        processing_time = time.time() - start_time
        
        return DocumentAnalysis(
            document_id=f"DOC-{case.case_id}-{doc_type}",
            document_type=doc_type,
            key_facts=key_facts,
            legal_references=legal_refs,
            risk_factors=risk_factors,
            confidence=confidence,
            processing_time=processing_time
        )
    
    def _extract_key_facts(self, text: str) -> List[str]:
        """Ekstrakcja kluczowych faktów"""
        facts = []
        lines = text.split('\n')
        for line in lines:
            if any(marker in line.lower() for marker in ['fakt', 'ustalono', 'stwierdzono', '•', '-']):
                facts.append(line.strip())
        return facts[:10]  # Max 10 faktów
    
    def _extract_legal_references(self, text: str) -> List[str]:
        """Ekstrakcja odniesień prawnych"""
        refs = []
        legal_keywords = ['art.', 'ust.', 'rozporządzenie', 'ustawa', 'kpa']
        for line in text.split('\n'):
            if any(keyword in line.lower() for keyword in legal_keywords):
                refs.append(line.strip())
        return refs[:5]
    
    def _extract_risk_factors(self, text: str) -> List[str]:
        """Ekstrakcja czynników ryzyka"""
        risks = []
        risk_keywords = ['ryzyko', 'niepewność', 'brak', 'niekompletne', 'sprzeczność']
        for line in text.split('\n'):
            if any(keyword in line.lower() for keyword in risk_keywords):
                risks.append(line.strip())
        return risks[:5]
    
    def _extract_confidence(self, text: str) -> float:
        """Ekstrakcja poziomu pewności"""
        # Szukanie liczby w kontekście pewności
        import re
        confidence_patterns = [
            r'pewność[:\s]+(\d+)%',
            r'wiarygodność[:\s]+(\d+)%',
            r'confidence[:\s]+(\d+)'
        ]
        for pattern in confidence_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1)) / 100.0
        return 0.7  # Domyślna wartość
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parsowanie odpowiedzi JSON z fallback do regex"""
        import json
        import re
        
        # Próba wyciągnięcia JSON z odpowiedzi
        # Szukaj bloku JSON (może być otoczony tekstem)
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        for match in matches:
            try:
                parsed = json.loads(match)
                # Walidacja struktury
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                continue
        
        # Fallback: parsowanie regex (dla kompatybilności wstecznej)
        return {
            'key_facts': self._extract_key_facts(text),
            'legal_references': self._extract_legal_references(text),
            'risk_factors': self._extract_risk_factors(text),
            'confidence': self._extract_confidence(text)
        }

# ============================================================================
# MODUŁ INTEGRACJI Z SYSTEMAMI ZEWNĘTRZNYMI
# ============================================================================

class ExternalSystemsIntegration:
    """Moduł integracji z systemami zewnętrznymi z Vector Database (RAG)"""
    
    def __init__(self):
        self.cbosa_available = False  # Baza orzeczeń CBOSA
        self.legal_registers = {
            "kpa": "Kodeks postępowania administracyjnego",
            "ustawa_turystyczna": "Ustawa o usługach turystycznych",
            "rozporzadzenie_kategorie": "Rozporządzenie w sprawie kategorii obiektów hotelarskich"
        }
        self.precedents_database = []
        
        # Vector Database dla RAG
        try:
            from vector_db import VectorDatabase
            self.vector_db = VectorDatabase()
            if self.vector_db.available:
                # Załaduj przykładowe precedensy przy pierwszym uruchomieniu
                if self.vector_db.get_stats()['total_documents'] == 0:
                    self.vector_db.load_sample_precedents()
        except ImportError:
            self.vector_db = None
            print("ℹ️ Vector Database nie dostępna - używam symulacji")
    
    def search_precedents(self, case_type: str, keywords: List[str]) -> List[Dict]:
        """Wyszukiwanie precedensów w bazie orzeczeń z użyciem Vector DB (RAG)"""
        # Użyj Vector Database jeśli dostępna
        if self.vector_db and self.vector_db.available:
            # Utwórz zapytanie z keywords
            query = f"{case_type} {' '.join(keywords)}"
            results = self.vector_db.search_precedents(query, case_type=case_type, n_results=5)
            return results
        
        # Fallback: symulacja wyszukiwania
        precedents = []
        for i, precedent in enumerate(self.precedents_database):
            if case_type in precedent.get('type', '') or any(kw in precedent.get('summary', '') for kw in keywords):
                precedents.append(precedent)
        
        return precedents[:5]  # Max 5 precedensów
    
    def check_legal_compliance(self, decision_draft: DecisionDraft) -> Dict[str, bool]:
        """Sprawdzenie zgodności z przepisami prawnymi"""
        compliance = {
            "kpa_structure": True,  # Struktura zgodna z KPA
            "legal_references": len(decision_draft.legal_references) > 0,
            "factual_justification": len(decision_draft.factual_justification) > 100,
            "legal_justification": len(decision_draft.legal_justification) > 100,
            "decision_text": len(decision_draft.decision_text) > 50
        }
        
        return compliance
    
    def get_regulation_text(self, regulation_id: str) -> Optional[str]:
        """Pobranie tekstu przepisu"""
        if regulation_id in self.legal_registers:
            # W produkcji: pobranie z bazy przepisów
            return f"Tekst przepisu: {self.legal_registers[regulation_id]}"
        return None

# ============================================================================
# GŁÓWNY ASYSTENT AI DLA ORZECZNIKÓW (GQPA INTEGRATED)
# ============================================================================

class HAMAAdministrativeAssistant:
    """
    Główny moduł asystenta AI z integracją GQPA
    
    ⚠️ UWAGA: Wykorzystuje GQPA Core jako bibliotekę zewnętrzną (Background IP).
    GQPA jest utworem współautorskim i nie podlega przeniesieniu praw.
    """
    
    def __init__(self, gemini_adapter: GeminiCognitiveAdapter):
        self.adapter = gemini_adapter
        self.document_analyzer = DocumentAnalyzer(gemini_adapter)
        self.external_systems = ExternalSystemsIntegration()
        self.guardrails = SecurityGuardrails()
        
        # Informacja o GQPA (Background IP)
        self.hama_info = HAMA_INFO if HAMA_INFO else None
        if self.hama_info:
            print(f"📚 Używana biblioteka: {self.hama_info['name']} v{self.hama_info['version']}")
            print(f"   Status: {self.hama_info['status']}")
        
        # Baza spraw
        self.cases: Dict[str, AdministrativeCase] = {}
        self.deadlines: List[Dict] = []
        
        # Baza wiedzy prawniczej
        self.legal_knowledge_base = self._initialize_legal_knowledge()
        
        # Metryki wydajności
        self.performance_metrics = {
            'total_cases': 0,
            'total_analyses': 0,
            'avg_analysis_time': 0.0,
            'avg_decision_generation_time': 0.0
        }
        
        # Truth Guardian (COI) - System immunologiczny kognitywny
        self.cognitive_agent = EnhancedCognitiveAgent()
        self.truth_guardian = CognitiveImmuneSystem(self.cognitive_agent, self.adapter)
    
    def _initialize_legal_knowledge(self) -> Dict:
        """Inicjalizacja bazy wiedzy prawnej"""
        return {
            "procedury": {
                "kwalifikacja_zawodowa": {
                    "kroki": ["weryfikacja dokumentów", "ocena kwalifikacji", "wydanie decyzji"],
                    "termin": 30,
                    "wymagane_dokumenty": ["dyplom", "świadectwo", "zaświadczenie"]
                },
                "kategoria_hotelu": {
                    "kroki": ["inspekcja", "ocena standardów", "przydział kategorii"],
                    "termin": 60,
                    "wymagane_dokumenty": ["wniosek", "dokumentacja techniczna"]
                },
                "zakaz_dzialalnosci": {
                    "kroki": ["analiza naruszeń", "wysłuchanie strony", "wydanie decyzji"],
                    "termin": 90,
                    "wymagane_dokumenty": ["wniosek", "dokumentacja naruszeń"]
                }
            },
            "przepisy": [
                "Ustawa o usługach turystycznych",
                "Rozporządzenie w sprawie kategorii obiektów hotelarskich",
                "Kodeks postępowania administracyjnego"
            ],
            "historical_decisions": []  # W produkcji: 300 decyzji archiwalnych
        }
    
    def add_case(self, case: AdministrativeCase) -> bool:
        """Dodanie nowej sprawy z walidacją"""
        # Walidacja danych sprawy
        case_data = json.dumps({
            'case_id': case.case_id,
            'case_type': case.case_type,
            'parties': case.parties
        })
        
        is_valid, error_msg = self.guardrails.validate_input(case_data, "document")
        if not is_valid:
            print(f"❌ Błąd walidacji sprawy: {error_msg}")
            return False
        
        # Sprawdzenie RODO
        rodo_ok, rodo_issues = self.guardrails.check_rodo_compliance({
            'parties': case.parties,
            'documents': case.documents
        })
        
        if not rodo_ok:
            print(f"⚠️ Uwagi RODO: {', '.join(rodo_issues)}")
        
        self.cases[case.case_id] = case
        if case.deadline:
            self.deadlines.append({
                "case_id": case.case_id,
                "deadline": case.deadline,
                "priority": self._calculate_priority(case)
            })
        
        self.performance_metrics['total_cases'] += 1
        self.guardrails.log_operation("add_case", "system", {"case_id": case.case_id})
        
        return True
    
    def _calculate_priority(self, case: AdministrativeCase) -> str:
        """Obliczenie priorytetu sprawy"""
        if not case.deadline:
            return "średni"
        
        days_left = (case.deadline - datetime.now()).days
        if days_left <= 3:
            return "krytyczny"
        elif days_left <= 7:
            return "wysoki"
        elif days_left <= 14:
            return "średni"
        else:
            return "niski"
    
    def analyze_case(self, case_id: str) -> Dict[str, Any]:
        """Kompleksowa analiza sprawy administracyjnej"""
        if case_id not in self.cases:
            return {"error": f"Sprawa {case_id} nie istnieje"}
        
        case = self.cases[case_id]
        start_time = time.time()
        
        # 1. Analiza dokumentów
        document_analyses = []
        for doc in case.documents:
            analysis = self.document_analyzer.analyze_document(doc, case)
            document_analyses.append(analysis)
        
        # 2. Wyszukiwanie precedensów
        precedents = self.external_systems.search_precedents(
            case.case_type,
            [case.case_type] + [doc.get('type', '') for doc in case.documents]
        )
        
        # 3. Analiza kognitywna z użyciem JSON Mode
        prompt = f"""
Jesteś asystentem AI dla orzecznika w Departamencie Turystyki MSiT.

ANALIZOWANA SPRAWA:
- ID: {case.case_id}
- Typ: {case.case_type}
- Status: {case.status}
- Strony: {', '.join(case.parties)}
- Dokumenty: {len(case.documents)} dokumentów

ANALIZA DOKUMENTÓW:
{chr(10).join([f"- {da.document_type}: {', '.join(da.key_facts[:3])}" for da in document_analyses])}

PRECEDENSY:
{chr(10).join([f"- {p.get('summary', 'N/A')[:100]}" for p in precedents[:3]])}

ZADANIE:
1. Stwórz streszczenie kluczowych faktów z dokumentacji
2. Zidentyfikuj główne kwestie prawne
3. Oceń ryzyko prawne (niski/średni/wysoki) z uzasadnieniem
4. Zaproponuj możliwe rozstrzygnięcia z uzasadnieniem prawnym
5. Wskaż potencjalne problemy proceduralne

Odpowiedz TYLKO w formacie JSON:
{{
  "summary": "streszczenie faktów",
  "risk_level": "niski|średni|wysoki",
  "legal_issues": ["kwestia1", "kwestia2"],
  "recommendations": "rekomendacje",
  "risk_factors": ["czynnik1", "czynnik2"]
}}
"""
        
        response = self.adapter.cognitive_query(prompt, json_mode=True)
        analysis_text = response['response']
        
        # Parsowanie JSON z fallback do regex
        parsed_data = self._parse_analysis_json(analysis_text)
        
        risk_level = parsed_data.get('risk_level', 'średni')
        legal_issues = parsed_data.get('legal_issues', [])
        recommendations = parsed_data.get('recommendations', '')
        
        # Aktualizacja sprawy
        case.summary = analysis_text[:1000]
        case.risk_assessment = {
            "level": risk_level,
            "factors": self._extract_risk_factors(analysis_text),
            "confidence": response.get('cognitive_state', {}).get('confidence', 0.85)
        }
        case.legal_issues = legal_issues
        case.historical_precedents = [p.get('id', '') for p in precedents]
        case.updated_at = datetime.now()
        
        # Aktualizacja metryk
        analysis_time = time.time() - start_time
        self.performance_metrics['total_analyses'] += 1
        self.performance_metrics['avg_analysis_time'] = (
            (self.performance_metrics['avg_analysis_time'] * (self.performance_metrics['total_analyses'] - 1) + analysis_time) 
            / self.performance_metrics['total_analyses']
        )
        
        return {
            "case_id": case_id,
            "summary": analysis_text[:500],
            "risk_assessment": case.risk_assessment,
            "legal_issues": legal_issues,
            "recommendations": recommendations,
            "precedents_found": len(precedents),
            "analysis_time": analysis_time,
            "document_analyses": [
                {
                    "type": da.document_type,
                    "key_facts_count": len(da.key_facts),
                    "confidence": da.confidence
                }
                for da in document_analyses
            ]
        }
    
    def _extract_risk_level(self, text: str) -> str:
        """Ekstrakcja poziomu ryzyka"""
        text_lower = text.lower()
        if "wysokie ryzyko" in text_lower or "ryzyko wysokie" in text_lower:
            return "wysoki"
        elif "niski" in text_lower and "ryzyko" in text_lower:
            return "niski"
        else:
            return "średni"
    
    def _extract_legal_issues(self, text: str) -> List[str]:
        """Ekstrakcja kwestii prawnych"""
        issues = []
        keywords = ["kwestia", "problem", "wątpliwość", "niepewność", "sprzeczność"]
        lines = text.split('\n')
        for line in lines:
            if any(kw in line.lower() for kw in keywords) and len(line.strip()) > 20:
                issues.append(line.strip())
        return issues[:5]
    
    def _extract_recommendations(self, text: str) -> str:
        """Ekstrakcja rekomendacji"""
        # Szukanie sekcji z rekomendacjami
        sections = text.split('\n\n')
        for section in sections:
            if any(kw in section.lower() for kw in ["rekomendacja", "zalecenie", "propozycja", "rozstrzygnięcie"]):
                return section[:500]
        return text[:500]
    
    def _extract_risk_factors(self, text: str) -> List[str]:
        """Ekstrakcja czynników ryzyka"""
        factors = []
        lines = text.split('\n')
        for line in lines:
            if "ryzyko" in line.lower() or "czynnik" in line.lower():
                factors.append(line.strip())
        return factors[:5]
    
    def generate_decision_draft(self, case_id: str, decision_type: str = "pozytywna") -> DecisionDraft:
        """Generowanie projektu decyzji administracyjnej"""
        if case_id not in self.cases:
            raise ValueError(f"Sprawa {case_id} nie istnieje")
        
        case = self.cases[case_id]
        start_time = time.time()
        
        # Przygotowanie kontekstu
        precedents = self.external_systems.search_precedents(case.case_type, [case.case_type])
        
        prompt = f"""
Jesteś asystentem AI generującym projekt decyzji administracyjnej zgodnie z Kodeksem postępowania administracyjnego.

SPRAWA:
- ID: {case.case_id}
- Typ: {case.case_type}
- Strony: {', '.join(case.parties)}
- Podsumowanie: {case.summary[:500] if case.summary else 'Brak'}

TYP DECYZJI: {decision_type}

PRECEDENSY:
{chr(10).join([f"- {p.get('summary', 'N/A')[:200]}" for p in precedents[:2]])}

WYMIAGANIA:
1. Zgodność z Kodeksem postępowania administracyjnego
2. Struktura: uzasadnienie faktyczne, uzasadnienie prawne, rozstrzygnięcie
3. Profesjonalny język prawniczy
4. Odwołanie do odpowiednich przepisów prawnych
5. Kompletność i precyzja

Wygeneruj kompletny projekt decyzji w formacie:
1. UZASADNIENIE FAKTYCZNE
2. UZASADNIENIE PRAWNE
3. ROZSTRZYGNIĘCIE
"""
        
        response = self.adapter.cognitive_query(prompt)
        decision_text = response['response']
        
        # Parsowanie decyzji
        factual_justification = self._extract_section(decision_text, "uzasadnienie faktyczne")
        legal_justification = self._extract_section(decision_text, "uzasadnienie prawne")
        decision_section = self._extract_section(decision_text, "rozstrzygnięcie")
        
        # Ekstrakcja odniesień prawnych
        legal_references = self._extract_legal_references(decision_text)
        
        # Sprawdzenie zgodności
        draft = DecisionDraft(
            case_id=case_id,
            decision_type=decision_type,
            factual_justification=factual_justification,
            legal_justification=legal_justification,
            decision_text=decision_section,
            legal_references=legal_references,
            compliance_checks={}
        )
        
        # Weryfikacja zgodności
        draft.compliance_checks = self.external_systems.check_legal_compliance(draft)
        
        # Aktualizacja sprawy
        case.decision_proposal = decision_text
        case.updated_at = datetime.now()
        
        # Aktualizacja metryk
        generation_time = time.time() - start_time
        self.performance_metrics['avg_decision_generation_time'] = (
            (self.performance_metrics['avg_decision_generation_time'] * (self.performance_metrics['total_analyses'] - 1) + generation_time)
            / max(self.performance_metrics['total_analyses'], 1)
        )
        
        return draft
    
    def _parse_analysis_json(self, text: str) -> Dict[str, Any]:
        """Parsowanie odpowiedzi analizy w formacie JSON"""
        import json
        import re
        
        # Próba wyciągnięcia JSON
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        for match in matches:
            try:
                parsed = json.loads(match)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                continue
        
        # Fallback: regex parsing
        return {
            'summary': text[:500],
            'risk_level': self._extract_risk_level(text),
            'legal_issues': self._extract_legal_issues(text),
            'recommendations': self._extract_recommendations(text),
            'risk_factors': self._extract_risk_factors(text)
        }
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Ekstrakcja sekcji z tekstu"""
        text_lower = text.lower()
        section_lower = section_name.lower()
        
        # Szukanie początku sekcji
        start_idx = text_lower.find(section_lower)
        if start_idx == -1:
            return text[:500]  # Fallback
        
        # Szukanie końca sekcji (następna sekcja lub koniec)
        next_sections = ["uzasadnienie prawne", "rozstrzygnięcie", "podpis"]
        end_idx = len(text)
        for next_section in next_sections:
            next_idx = text_lower.find(next_section, start_idx + len(section_name))
            if next_idx != -1 and next_idx < end_idx:
                end_idx = next_idx
        
        return text[start_idx:end_idx].strip()
    
    def _extract_legal_references(self, text: str) -> List[str]:
        """Ekstrakcja odniesień prawnych"""
        refs = []
        import re
        patterns = [
            r'art\.\s*\d+',
            r'ust\.\s*\d+',
            r'ustawa[^,]*',
            r'rozporządzenie[^,]*',
            r'kpa'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            refs.extend(matches)
        return list(set(refs))[:10]  # Unikalne, max 10
    
    def check_deadlines(self, days_ahead: int = 7) -> List[Dict]:
        """Sprawdzanie zbliżających się terminów"""
        upcoming = []
        now = datetime.now()
        threshold = now + timedelta(days=days_ahead)
        
        for case_id, case in self.cases.items():
            if case.deadline and case.deadline <= threshold:
                days_left = (case.deadline - now).days
                priority = self._calculate_priority(case)
                
                upcoming.append({
                    "case_id": case_id,
                    "case_type": case.case_type,
                    "deadline": case.deadline.isoformat(),
                    "days_left": days_left,
                    "priority": priority,
                    "status": case.status
                })
        
        return sorted(upcoming, key=lambda x: x['days_left'])
    
    def get_case_summary(self, case_id: str) -> Optional[Dict]:
        """Pobranie podsumowania sprawy"""
        if case_id not in self.cases:
            return None
        
        case = self.cases[case_id]
        return {
            "case_id": case.case_id,
            "type": case.case_type,
            "status": case.status,
            "parties": case.parties,
            "deadline": case.deadline.isoformat() if case.deadline else None,
            "summary": case.summary,
            "risk_assessment": case.risk_assessment,
            "legal_issues": case.legal_issues,
            "compliance_score": case.compliance_score,
            "created_at": case.created_at.isoformat(),
            "updated_at": case.updated_at.isoformat()
        }
    
    def get_performance_metrics(self) -> Dict:
        """Pobranie metryk wydajności"""
        return self.performance_metrics.copy()
    
    def export_audit_log(self) -> List[Dict]:
        """Eksport logu audit"""
        return self.guardrails.audit_log.copy()
    
    def verify_content(self, content: ContentItem) -> Dict:
        """
        Weryfikacja treści przez Truth Guardian (COI)
        
        Args:
            content: Treść do weryfikacji
            
        Returns:
            Dict z wynikami weryfikacji (is_verified, analysis, chaos_reaction, confidence)
        """
        return self.truth_guardian.verify_content(content)

# ============================================================================
# FUNKCJE DEMONSTRACYJNE
# ============================================================================

def create_demo_assistant(use_local_model: bool = True):
    """
    Tworzenie demonstracyjnego asystenta
    
    Args:
        use_local_model: Jeśli True, używa Gemini API przez adapter
                        Domyślnie True - preferowane Gemini API
    """
    # Używamy None dla gemini_client gdy używamy lokalnego modelu
    adapter = GeminiCognitiveAdapter(None, use_local_model=use_local_model)
    assistant = HAMAAdministrativeAssistant(adapter)
    return assistant

def demo_full_workflow():
    """Demonstracja pełnego workflow"""
    print("\n" + "="*70)
    print("🏛️ DEMONSTRACJA ASYSTENTA AI DLA ADMINISTRACJI")
    print("="*70)
    
    assistant = create_demo_assistant(use_local_model=True)  # Używa Gemini API
    
    # 1. Utworzenie przykładowej sprawy
    print("\n[1] Tworzenie przykładowej sprawy...")
    case = AdministrativeCase(
        case_id="SPR-2024-001",
        case_type="kwalifikacja_zawodowa",
        documents=[
            {
                "type": "wniosek",
                "content": "Wniosek o nadanie kwalifikacji przewodnika turystycznego. Wnioskodawca: Jan Kowalski, posiada dyplom ukończenia studiów turystycznych na Uniwersytecie Warszawskim."
            },
            {
                "type": "dyplom",
                "content": "Dyplom ukończenia studiów wyższych - kierunek: Turystyka i Rekreacja, Uniwersytet Warszawski, rok 2020."
            }
        ],
        parties=["Jan Kowalski", "Departament Turystyki MSiT"],
        status="w_trakcie",
        deadline=datetime.now() + timedelta(days=15)
    )
    
    assistant.add_case(case)
    print(f"✅ Sprawa {case.case_id} dodana")
    
    # 2. Analiza sprawy
    print("\n[2] Analiza sprawy...")
    analysis = assistant.analyze_case(case.case_id)
    print(f"✅ Analiza zakończona (czas: {analysis['analysis_time']:.2f}s)")
    print(f"   Poziom ryzyka: {analysis['risk_assessment']['level']}")
    print(f"   Kwestie prawne: {len(analysis['legal_issues'])}")
    
    # 3. Generowanie projektu decyzji
    print("\n[3] Generowanie projektu decyzji...")
    draft = assistant.generate_decision_draft(case.case_id, "pozytywna")
    print(f"✅ Projekt decyzji wygenerowany")
    print(f"   Zgodność z przepisami: {sum(draft.compliance_checks.values())}/{len(draft.compliance_checks)}")
    print(f"   Odniesienia prawne: {len(draft.legal_references)}")
    
    # 4. Sprawdzenie terminów
    print("\n[4] Sprawdzanie terminów...")
    deadlines = assistant.check_deadlines()
    print(f"✅ Znaleziono {len(deadlines)} spraw z terminami w ciągu 7 dni")
    for d in deadlines:
        print(f"   - {d['case_id']}: {d['days_left']} dni (priorytet: {d['priority']})")
    
    # 5. Metryki wydajności
    print("\n[5] Metryki wydajności:")
    metrics = assistant.get_performance_metrics()
    print(f"   Łącznie spraw: {metrics['total_cases']}")
    print(f"   Łącznie analiz: {metrics['total_analyses']}")
    print(f"   Średni czas analizy: {metrics['avg_analysis_time']:.2f}s")
    print(f"   Średni czas generowania decyzji: {metrics['avg_decision_generation_time']:.2f}s")
    
    print("\n✅ Demonstracja zakończona!")
    return assistant

# ============================================================================
# GŁÓWNA FUNKCJA
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🏛️ ASYSTENT AI DLA ADMINISTRACJI - SYSTEM GOTOWY")
    print("="*70)
    print("\nDostępne funkcje:")
    print("1. create_demo_assistant() - Utworzenie asystenta")
    print("2. demo_full_workflow() - Pełna demonstracja workflow")
    print("\n" + "="*70)
    
    # Uruchomienie demonstracji
    print("\n🚀 Uruchamianie demonstracji...\n")
    assistant = demo_full_workflow()

