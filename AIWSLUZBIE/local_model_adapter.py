"""
🔧 Lokalny Adapter Modelu - Open Source LLM
Obsługa lokalnych modeli językowych (Ollama, Hugging Face, itp.)
"""

import os
import time
from typing import Dict, Any, Optional
from datetime import datetime

# ============================================================================
# OLLAMA ADAPTER (najłatwiejszy w użyciu)
# ============================================================================

class OllamaAdapter:
    """Adapter dla Ollama - lokalne modele open-source"""
    
    def __init__(self, model_name: str = None, base_url: str = "http://localhost:11434"):
        # Domyślnie użyj llama3.2 jeśli nie podano
        if model_name is None:
            try:
                import asystent_ai_gqpa_integrated
                model_name = getattr(asystent_ai_gqpa_integrated, 'OLLAMA_MODEL_NAME', 'llama3.2')
            except (ImportError, AttributeError):
                model_name = "llama3.2"  # Fallback
        self.model_name = model_name
        self.base_url = base_url
        self.available = False
        
        # Sprawdź dostępność Ollama
        try:
            import requests  # type: ignore
            self.requests = requests
            
            # Sprawdź czy serwer Ollama działa
            try:
                response = requests.get(f"{base_url}/api/tags", timeout=2)
                if response.status_code == 200:
                    self.available = True
                    print(f"✅ Ollama dostępne - model: {model_name}")
                else:
                    print(f"⚠️ Ollama nie odpowiada na {base_url}")
                    print(f"   Uruchom: ollama serve")
            except requests.exceptions.ConnectionError:
                print(f"⚠️ Ollama nie działa na {base_url}")
                print(f"   Instrukcja naprawy: zobacz NAPRAWA_OLLAMA_WINDOWS.md")
                print(f"   Lub uruchom: ollama serve")
        except ImportError:
            print("⚠️ Biblioteka 'requests' nie dostępna - zainstaluj: pip install requests")
        except Exception as e:
            print(f"⚠️ Ollama nie dostępne: {e}")
            print(f"   Sprawdź: NAPRAWA_OLLAMA_WINDOWS.md")
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generowanie odpowiedzi przez Ollama"""
        if not self.available:
            return {
                'response': "[OLLAMA NIE DOSTĘPNE] Uruchom Ollama: ollama serve",
                'success': False,
                'error': 'Ollama nie dostępne'
            }
        
        # JSON Mode - jeśli format="json" w kwargs
        use_json_mode = kwargs.get('format') == 'json' or kwargs.get('json_mode', False)
        
        # Dodaj instrukcję JSON jeśli wymagane
        if use_json_mode:
            prompt = f"""{prompt}

WAŻNE: Odpowiedz TYLKO w formacie JSON, bez dodatkowego tekstu. Użyj następującej struktury:
{{
  "key_facts": ["fakt1", "fakt2"],
  "legal_references": ["art. 1", "ust. 2"],
  "risk_factors": ["czynnik1"],
  "confidence": 0.85
}}"""
        
        try:
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json" if use_json_mode else None,
                    "options": {
                        "temperature": kwargs.get('temperature', 0.7),
                        "top_p": kwargs.get('top_p', 0.95),
                        "num_predict": kwargs.get('max_tokens', 2048),
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'response': result.get('response', ''),
                    'success': True,
                    'error': None,
                    'latency': result.get('total_duration', 0) / 1e9  # nanosekundy na sekundy
                }
            else:
                return {
                    'response': f"Błąd Ollama: {response.status_code}",
                    'success': False,
                    'error': f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                'response': f"Błąd połączenia z Ollama: {str(e)}",
                'success': False,
                'error': str(e)
            }

# ============================================================================
# HUGGING FACE TRANSFORMERS ADAPTER
# ============================================================================

class HuggingFaceAdapter:
    """Adapter dla modeli Hugging Face (transformers)"""
    
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.available = False
        
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore
            import torch  # type: ignore
            
            print(f"📥 Ładowanie modelu {model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            self.available = True
            print(f"✅ Model {model_name} załadowany")
        except ImportError:
            print("⚠️ Transformers nie dostępne - zainstaluj: pip install transformers torch")
        except Exception as e:
            print(f"⚠️ Błąd ładowania modelu: {e}")
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generowanie odpowiedzi przez Hugging Face"""
        if not self.available or self.model is None or self.tokenizer is None:
            return {
                'response': "[HF MODEL NIE DOSTĘPNY]",
                'success': False,
                'error': 'Model nie załadowany'
            }
        
        try:
            start_time = time.time()
            
            inputs = self.tokenizer(prompt, return_tensors="pt")
            if hasattr(self.model, 'device'):
                inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            with torch.no_grad():  # type: ignore
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=kwargs.get('max_tokens', 512),
                    temperature=kwargs.get('temperature', 0.7),
                    top_p=kwargs.get('top_p', 0.95),
                    do_sample=True
                )
            
            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Usuń prompt z odpowiedzi
            if prompt in response_text:
                response_text = response_text.split(prompt, 1)[1].strip()
            
            latency = time.time() - start_time
            
            return {
                'response': response_text,
                'success': True,
                'error': None,
                'latency': latency
            }
        except Exception as e:
            return {
                'response': f"Błąd generowania: {str(e)}",
                'success': False,
                'error': str(e)
            }

# ============================================================================
# UNIFIED LOCAL MODEL ADAPTER
# ============================================================================

class LocalModelAdapter:
    """Unified adapter dla lokalnych modeli - automatycznie wybiera najlepszy dostępny"""
    
    def __init__(self, preferred_backend: str = "ollama", model_name: str = None):
        self.preferred_backend = preferred_backend
        self.ollama = None
        self.huggingface = None
        self.active_adapter = None
        
        # Ustaw domyślny model jeśli nie podano
        if model_name is None:
            try:
                import asystent_ai_gqpa_integrated
                model_name = getattr(asystent_ai_gqpa_integrated, 'OLLAMA_MODEL_NAME', 'llama3.2')
            except (ImportError, AttributeError):
                model_name = "llama3.2"  # Fallback
        
        # Spróbuj Ollama (najłatwiejsze)
        if preferred_backend in ["ollama", "auto"]:
            self.ollama = OllamaAdapter(model_name=model_name)
            if self.ollama.available:
                self.active_adapter = self.ollama
                return
        
        # Spróbuj Hugging Face
        if preferred_backend in ["huggingface", "transformers", "auto"]:
            try:
                self.huggingface = HuggingFaceAdapter()
                if self.huggingface.available:
                    self.active_adapter = self.huggingface
                    return
            except Exception as e:
                print(f"⚠️ Hugging Face nie dostępne: {e}")
        
        print("⚠️ Żaden lokalny model nie jest dostępny - użyj API lub zainstaluj Ollama")
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generowanie odpowiedzi - używa aktywnego adaptera"""
        if self.active_adapter:
            return self.active_adapter.generate(prompt, **kwargs)
        else:
            return {
                'response': "[LOKALNY MODEL NIE DOSTĘPNY] Uruchom Ollama lub załaduj model Hugging Face",
                'success': False,
                'error': 'Brak dostępnego lokalnego modelu'
            }
    
    def is_available(self) -> bool:
        """Sprawdza czy lokalny model jest dostępny"""
        return self.active_adapter is not None and (
            (self.ollama and self.ollama.available) or
            (self.huggingface and self.huggingface.available)
        )

# ============================================================================
# HYBRID ADAPTER (Lokalny + API Fallback)
# ============================================================================

class HybridModelAdapter:
    """Hybrydowy adapter - preferuje lokalny model, fallback do API"""
    
    def __init__(self, prefer_local: bool = True):
        self.prefer_local = prefer_local
        self.local_adapter = LocalModelAdapter() if prefer_local else None
        self.api_adapter = None  # Będzie ustawiony przez GeminiCognitiveAdapter
    
    def set_api_adapter(self, api_adapter):
        """Ustawia adapter API jako fallback"""
        self.api_adapter = api_adapter
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generowanie - próbuje lokalny, potem API"""
        # Próbuj lokalny model
        if self.prefer_local and self.local_adapter and self.local_adapter.is_available():
            result = self.local_adapter.generate(prompt, **kwargs)
            if result['success']:
                result['source'] = 'local'
                return result
        
        # Fallback do API
        if self.api_adapter:
            result = self.api_adapter.cognitive_query(prompt)
            result['source'] = 'api'
            return result
        
        # Ostatnia deska ratunku - symulacja
        return {
            'response': f"[SYMULACJA] Odpowiedź na: {prompt[:100]}...",
            'success': True,
            'error': None,
            'latency': 0.1,
            'source': 'simulation'
        }

