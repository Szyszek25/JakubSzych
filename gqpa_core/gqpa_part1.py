"""
🎯 GQPA DIAMOND - CZĘŚĆ 1: INSTALACJA I KONFIGURACJA
Gotowe do wklejenia w Google Colab
"""

# ============================================================================
# INSTALACJA BIBLIOTEK
# ============================================================================

!pip install -q google-generativeai torch matplotlib seaborn pandas numpy tqdm scikit-learn networkx

print("✅ Biblioteki zainstalowane")

# ============================================================================
# IMPORTY
# ============================================================================

import google.generativeai as genai
from google.colab import userdata
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
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

# Konfiguracja wykresów
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

print("✅ Importy zakończone")

# ============================================================================
# KONFIGURACJA GEMINI 2.5 FLASH
# ============================================================================

# WAŻNE: Dodaj swój klucz API w Secrets (🔑 ikona po lewej)
# Nazwa: GOOGLE_API_KEY
GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

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

gemini_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",  # Najnowszy model
    generation_config=generation_config,
    safety_settings=safety_settings,
)

print("✅ Gemini 2.0 Flash Experimental skonfigurowany")

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

print("✅ Typy danych zdefiniowane")
print("\n" + "="*70)
print("CZĘŚĆ 1 ZAKOŃCZONA - Przejdź do CZĘŚCI 2")
print("="*70)
