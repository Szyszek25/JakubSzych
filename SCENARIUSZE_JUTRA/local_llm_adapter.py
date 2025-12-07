"""
Adapter dla lokalnych modeli LLM (Ollama/Llama)
Zamiast OpenAI używamy lokalnych modeli open-source
"""
import requests
from requests.exceptions import Timeout as RequestsTimeout
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaAdapter:
    """Adapter dla Ollama - lokalne modele Llama"""
    
    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.available = False
        self._check_availability()
    
    def _check_availability(self):
        """Sprawdza czy Ollama jest dostępne"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                self.available = True
                logger.info(f"✅ Ollama dostępne, model: {self.model_name}")
            else:
                logger.warning("⚠️ Ollama nie odpowiada")
        except Exception as e:
            logger.warning(f"⚠️ Ollama nie dostępne: {e}")
            logger.info("   Uruchom Ollama: ollama serve")
    
    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2000, **kwargs) -> Dict[str, Any]:
        """Generuje odpowiedź używając Ollama"""
        if not self.available:
            return {
                'response': "[OLLAMA NIE DOSTĘPNE] Uruchom Ollama: ollama serve",
                'success': False,
                'error': 'Ollama nie dostępne'
            }
        
        try:
            # JSON Mode jeśli wymagane
            use_json_mode = kwargs.get('format') == 'json' or kwargs.get('json_mode', False)
            
            if use_json_mode:
                prompt = f"""{prompt}

WAZNE: Odpowiedz TYLKO w formacie JSON, bez dodatkowego tekstu."""
            
            # Dla długich promptów (>5000 znaków) zmniejszamy max_tokens, żeby przyspieszyć
            if len(prompt) > 5000:
                max_tokens = min(max_tokens, 2000)  # Ograniczamy do 2000 tokenów
                logger.info(f"Prompt jest dlugi ({len(prompt)} znakow), ograniczam max_tokens do {max_tokens}")
            
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            logger.info(f"Wysylam prompt do Ollama (model: {self.model_name}, dlugosc: {len(prompt)} znakow, max_tokens: {max_tokens})...")
            if self.model_name == "mistral":
                logger.info(f"UWAGA: Mistral moze byc wolny - to moze zajac 2-5 minut dla dlugich promptow...")
            
            import time
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120  # 2 minuty timeout - jeśli trwa dłużej, jest problem
            )
            elapsed = time.time() - start_time
            logger.info(f"Otrzymano odpowiedz z Ollama po {elapsed:.1f} sekundach (status: {response.status_code})")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'response': data.get('response', ''),
                    'success': True,
                    'error': None
                }
            else:
                return {
                    'response': f"Błąd Ollama: {response.status_code}",
                    'success': False,
                    'error': f"HTTP {response.status_code}"
                }
                
        except RequestsTimeout:
            logger.error(f"Timeout podczas generowania - prompt był za długi lub model zbyt wolny")
            return {
                'response': "[TIMEOUT] Generowanie trwało zbyt długo. Spróbuj skrócić prompt lub użyć szybszego modelu.",
                'success': False,
                'error': 'Timeout'
            }
        except Exception as e:
            logger.error(f"Błąd podczas generowania: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                'response': f"[BŁĄD] {str(e)}",
                'success': False,
                'error': str(e)
            }


class LocalLLMAdapter:
    """
    Unified adapter - automatycznie używa Ollama jeśli dostępne
    Fallback do prostych odpowiedzi jeśli Ollama nie działa
    """
    
    def __init__(self, model_name: str = "llama3.2"):
        self.ollama = OllamaAdapter(model_name=model_name)
        self.model_name = model_name
    
    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2000, **kwargs) -> str:
        """Generuje odpowiedź - zwraca string zamiast dict"""
        result = self.ollama.generate(prompt, temperature, max_tokens, **kwargs)
        
        if result['success']:
            return result['response']
        else:
            # Fallback - prosta odpowiedź
            logger.warning(f"Ollama nie dostępne, używam fallback: {result.get('error')}")
            return self._simple_fallback(prompt)
    
    def _simple_fallback(self, prompt: str) -> str:
        """Prosty fallback gdy Ollama nie działa"""
        # Podstawowa analiza bez LLM
        if "scenariusz" in prompt.lower() or "scenario" in prompt.lower():
            return """{
    "title": "Scenariusz analityczny",
    "description": "Analiza wymaga lokalnego modelu LLM. Uruchom Ollama: ollama serve",
    "key_events": [],
    "probabilities": {},
    "impacts": {},
    "recommendations": ["Zainstaluj i uruchom Ollama dla pełnej funkcjonalności"],
    "reasoning": {"confidence": 0.5}
}"""
        return "[OLLAMA NIE DOSTĘPNE] Uruchom: ollama serve"

