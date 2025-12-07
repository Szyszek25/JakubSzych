"""
🔧 Adapter Modelu - Gemini API
Obsługa Google Gemini API przez google-genai SDK
"""

import os
import time
from typing import Dict, Any, Optional
from datetime import datetime

# Domyślny klucz API dla jury (fallback jeśli nie ustawiono zmiennej środowiskowej)
DEFAULT_GEMINI_API_KEY = "AIzaSyC3EB_JAX2pTWLJAAiXuiKXTQA8pz4iZzo"

# ============================================================================
# GEMINI ADAPTER (używa google-genai SDK)
# ============================================================================

class GeminiAdapter:
    """Adapter dla Google Gemini API - używa google-genai SDK"""
    
    def __init__(self, model_name: str = None, api_key: str = None):
        # Domyślnie użyj gemini-2.5-flash jeśli nie podano
        if model_name is None:
            try:
                import asystent_ai_gqpa_integrated
                model_name = getattr(asystent_ai_gqpa_integrated, 'GEMINI_MODEL_NAME', 'gemini-2.5-flash')
            except (ImportError, AttributeError):
                model_name = "gemini-2.5-flash"  # Fallback
        
        self.model_name = model_name
        self.available = False
        self.client = None
        
        # Sprawdź dostępność Gemini API
        try:
            from google import genai  # type: ignore
            from google.genai import types as genai_types  # type: ignore
            
            # Pobierz API key - najpierw z parametru, potem ze zmiennej środowiskowej, na końcu domyślny
            if api_key is None:
                api_key = os.environ.get('GOOGLE_API_KEY') or os.environ.get('GEMINI_API_KEY')
            
            # Fallback do domyślnego klucza dla jury
            if not api_key:
                api_key = DEFAULT_GEMINI_API_KEY
                print("ℹ️ Używam domyślnego klucza API (dla jury)")
            
            if api_key:
                try:
                    self.client = genai.Client(api_key=api_key)
                    self.available = True
                    print(f"✅ Gemini API dostępne - model: {model_name}")
                except Exception as e:
                    print(f"⚠️ Błąd konfiguracji Gemini: {e}")
                    print(f"   Ustaw zmienną środowiskową GOOGLE_API_KEY lub GEMINI_API_KEY")
            else:
                print(f"⚠️ Brak klucza API Gemini")
                print(f"   Ustaw zmienną środowiskową GOOGLE_API_KEY lub GEMINI_API_KEY")
        except ImportError:
            print("⚠️ Biblioteka 'google-genai' nie dostępna - zainstaluj: pip install google-genai")
        except Exception as e:
            print(f"⚠️ Gemini nie dostępne: {e}")
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generowanie odpowiedzi przez Gemini API"""
        if not self.available or self.client is None:
            return {
                'response': "[GEMINI NIE DOSTĘPNE] Ustaw GOOGLE_API_KEY lub GEMINI_API_KEY",
                'success': False,
                'error': 'Gemini nie dostępne'
            }
        
        # JSON Mode - jeśli format="json" w kwargs
        use_json_mode = kwargs.get('format') == 'json' or kwargs.get('json_mode', False)
        
        start_time = time.time()
        try:
            from google.genai import types as genai_types
            
            # Konfiguracja generowania
            config_dict = {
                'temperature': kwargs.get('temperature', 0.7),
                'top_p': kwargs.get('top_p', 0.95),
                'top_k': kwargs.get('top_k', 40),
                'max_output_tokens': kwargs.get('max_tokens', 2048),
            }
            
            # Jeśli JSON mode, ustaw response_mime_type
            if use_json_mode:
                config_dict['response_mime_type'] = 'application/json'
            
            # Próbuj użyć GenerateContentConfig, jeśli dostępne
            try:
                config = genai_types.GenerateContentConfig(**config_dict)
            except (AttributeError, TypeError):
                config = config_dict
            
            # Generuj odpowiedź
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            
            response_text = response.text if hasattr(response, 'text') else str(response)
            latency = time.time() - start_time
            
            return {
                'response': response_text,
                'success': True,
                'error': None,
                'latency': latency
            }
        except Exception as e:
            return {
                'response': f"Błąd Gemini API: {str(e)}",
                'success': False,
                'error': str(e),
                'latency': time.time() - start_time
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
# UNIFIED MODEL ADAPTER
# ============================================================================

class LocalModelAdapter:
    """Unified adapter dla modeli - używa Gemini API jako domyślnego"""
    
    def __init__(self, preferred_backend: str = "gemini", model_name: str = None, api_key: str = None):
        self.preferred_backend = preferred_backend
        self.gemini = None
        self.huggingface = None
        self.active_adapter = None
        
        # Ustaw domyślny model jeśli nie podano
        if model_name is None:
            try:
                import asystent_ai_gqpa_integrated
                model_name = getattr(asystent_ai_gqpa_integrated, 'GEMINI_MODEL_NAME', 'gemini-2.5-flash')
            except (ImportError, AttributeError):
                model_name = "gemini-2.5-flash"  # Fallback
        
        # Spróbuj Gemini (domyślne)
        if preferred_backend in ["gemini", "auto"]:
            self.gemini = GeminiAdapter(model_name=model_name, api_key=api_key)
            if self.gemini.available:
                self.active_adapter = self.gemini
                return
        
        # Spróbuj Hugging Face (fallback)
        if preferred_backend in ["huggingface", "transformers", "auto"]:
            try:
                self.huggingface = HuggingFaceAdapter()
                if self.huggingface.available:
                    self.active_adapter = self.huggingface
                    return
            except Exception as e:
                print(f"⚠️ Hugging Face nie dostępne: {e}")
        
        print("⚠️ Żaden model nie jest dostępny - ustaw GOOGLE_API_KEY dla Gemini")
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generowanie odpowiedzi - używa aktywnego adaptera"""
        if self.active_adapter:
            return self.active_adapter.generate(prompt, **kwargs)
        else:
            return {
                'response': "[MODEL NIE DOSTĘPNY] Ustaw GOOGLE_API_KEY dla Gemini API",
                'success': False,
                'error': 'Brak dostępnego modelu'
            }
    
    def is_available(self) -> bool:
        """Sprawdza czy model jest dostępny"""
        return self.active_adapter is not None and (
            (self.gemini and self.gemini.available) or
            (self.huggingface and self.huggingface.available)
        )

# ============================================================================
# HYBRID ADAPTER (Lokalny + API Fallback)
# ============================================================================

class HybridModelAdapter:
    """Hybrydowy adapter - preferuje Gemini API"""
    
    def __init__(self, prefer_gemini: bool = True):
        self.prefer_gemini = prefer_gemini
        self.gemini_adapter = LocalModelAdapter(preferred_backend="gemini") if prefer_gemini else None
        self.api_adapter = None  # Będzie ustawiony przez GeminiCognitiveAdapter
    
    def set_api_adapter(self, api_adapter):
        """Ustawia adapter API jako fallback"""
        self.api_adapter = api_adapter
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generowanie - próbuje Gemini, potem fallback"""
        # Próbuj Gemini
        if self.prefer_gemini and self.gemini_adapter and self.gemini_adapter.is_available():
            result = self.gemini_adapter.generate(prompt, **kwargs)
            if result['success']:
                result['source'] = 'gemini'
                return result
        
        # Fallback do API adaptera
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

