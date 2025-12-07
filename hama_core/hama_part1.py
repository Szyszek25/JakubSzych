"""
🎯 HAMA DIAMOND - CZĘŚĆ 1: PODSTAWOWE TYPY DANYCH
Używa lokalnych modeli LLM (Ollama/Llama) zamiast Google Generative AI
"""

# ============================================================================
# IMPORTY
# ============================================================================

import time
import json
import math
import random
from typing import Dict, List, Any, Optional, Tuple
from collections import deque, defaultdict
from dataclasses import dataclass, field
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# Opcjonalne importy (dla kompatybilności)
try:
    import torch  # type: ignore
    import torch.nn as nn  # type: ignore
    import torch.nn.functional as F  # type: ignore
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import matplotlib.pyplot as plt  # type: ignore
    import seaborn as sns  # type: ignore
    import pandas as pd  # type: ignore
    import numpy as np  # type: ignore
    from tqdm import tqdm  # type: ignore
    # Konfiguracja wykresów
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False

print("OK Importy zakonczone")

# ============================================================================
# PODSTAWOWE TYPY DANYCH
# ============================================================================

class ModalityType(Enum):
    VISION = "vision"
    AUDIO = "audio"
    TOUCH = "touch"
    PROPRIOCEPTION = "proprioception"
    LANGUAGE = "language"

class ActionType(Enum):
    MOVEMENT = "movement"
    MANIPULATION = "manipulation"
    SPEECH = "speech"
    GESTURE = "gesture"

class EmotionType(Enum):
    JOY = "joy"
    FEAR = "fear"
    CURIOSITY = "curiosity"
    SATISFACTION = "satisfaction"
    FRUSTRATION = "frustration"

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

print("OK Typy danych zdefiniowane")
print("\n" + "="*70)
print("CZESC 1 ZAKONCZONA - Przejdz do CZESCI 2")
print("="*70)
