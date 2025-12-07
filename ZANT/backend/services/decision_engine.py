"""
Silnik decyzyjny - analizuje dokumentację i rekomenduje decyzję
Wykorzystuje HAMA Diamond do reasoning + reguły decyzyjne
Używa Google Gemini API
"""
import sys
import os
from typing import Dict, List, Any, Optional
import logging
import json
import re
import time

# Dodaj ścieżki do adapterów
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'AIWSLUZBIE'))

try:
    from local_model_adapter import LocalModelAdapter
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    logging.warning("LocalModelAdapter nie dostępne - zainstaluj: pip install google-genai")

from backend.models.accident import AccidentCard, DecisionRecommendation, DocumentExtraction
from backend.config import ACCIDENT_DEFINITION, DECISION_RULES, TEMPERATURE_ANALYSIS, GEMINI_MODEL_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DecisionEngine:
    """
    Silnik decyzyjny wykorzystujący HAMA Diamond do analizy i rekomendacji
    Używa Google Gemini API
    """
    
    def __init__(self):
        if LLM_AVAILABLE:
            try:
                # Użyj Gemini jako preferowanego backendu
                self.llm = LocalModelAdapter(preferred_backend="gemini", model_name=GEMINI_MODEL_NAME)
                if self.llm.is_available():
                    logger.info("✅ Gemini API dostępne")
                else:
                    logger.warning("⚠️ Gemini API nie dostępne - ustaw GOOGLE_API_KEY")
                    self.llm = None
            except Exception as e:
                logger.warning(f"⚠️ Błąd inicjalizacji Gemini: {e}")
                self.llm = None
        else:
            self.llm = None
            logger.warning("⚠️ LLM nie dostępne - używam tylko reguł")
        
        self.accident_definition = ACCIDENT_DEFINITION
        self.decision_rules = DECISION_RULES
    
    def analyze_and_recommend(
        self,
        document_extraction: DocumentExtraction,
        report_id: str
    ) -> AccidentCard:
        """
        Analizuje dokumentację i rekomenduje decyzję
        """
        # Krok 1: Analiza z użyciem HAMA Diamond
        hama_analysis = self._analyze_with_hama(document_extraction)
        
        # Krok 2: Weryfikacja warunków definicji wypadku
        conditions_check = self._check_accident_conditions(
            document_extraction,
            hama_analysis
        )
        
        # Krok 3: Zastosuj reguły decyzyjne
        decision, confidence, reasoning = self._apply_decision_rules(
            conditions_check,
            hama_analysis
        )
        
        # Krok 4: Wygeneruj uzasadnienie prawne
        legal_basis = self._extract_legal_basis(hama_analysis)
        
        # Krok 5: Zidentyfikuj czynniki ryzyka
        risk_factors = self._identify_risk_factors(conditions_check, hama_analysis)
        
        card_id = f"CARD-{report_id}-{int(time.time())}"
        
        return AccidentCard(
            card_id=card_id,
            report_id=report_id,
            decision=decision,
            confidence=confidence,
            reasoning=reasoning,
            extracted_data=document_extraction.extracted_fields,
            legal_basis=legal_basis,
            risk_factors=risk_factors
        )
    
    def _analyze_with_hama(
        self,
        document_extraction: DocumentExtraction
    ) -> Dict[str, Any]:
        """Analizuje dokumentację używając HAMA Diamond"""
        if not self.llm:
            return self._simple_analysis(document_extraction)
        
        prompt = f"""
Jesteś ekspertem ZUS analizującym dokumentację wypadku przy pracy.

DEFINICJA WYPADKU PRZY PRACY:
{self.accident_definition['definition']}

WYMAGANE WARUNKI:
{chr(10).join(f"- {cond}" for cond in self.accident_definition['required_conditions'])}

DOKUMENTACJA:
{document_extraction.text_content[:3000]}

ZADANIE:
1. Oceń czy zdarzenie spełnia definicję wypadku przy pracy
2. Sprawdź każdy wymagany warunek:
   - zdarzenie_nagłe: Czy zdarzenie było nagłe?
   - przyczyna_zewnetrzna: Czy była przyczyna zewnętrzna?
   - uraz_lub_smierc: Czy nastąpił uraz lub śmierć?
   - zwiazek_z_praca: Czy zdarzenie było związane z pracą?
3. Zidentyfikuj czynniki wykluczające
4. Oceń poziom pewności (0.0-1.0)

Odpowiedz TYLKO w formacie JSON:
{{
  "zdarzenie_nagłe": {{"potwierdzone": true, "pewnosc": 0.9, "uzasadnienie": "tekst"}},
  "przyczyna_zewnetrzna": {{"potwierdzone": true, "pewnosc": 0.85, "uzasadnienie": "tekst"}},
  "uraz_lub_smierc": {{"potwierdzone": true, "pewnosc": 0.95, "uzasadnienie": "tekst"}},
  "zwiazek_z_praca": {{"potwierdzone": true, "pewnosc": 0.8, "uzasadnienie": "tekst"}},
  "czynniki_wykluczajace": ["lista", "czynników"],
  "ogolna_pewnosc": 0.85,
  "rekomendacja": "recognize|not_recognize|needs_review",
  "uzasadnienie": "szczegółowe uzasadnienie decyzji"
}}
"""
        
        try:
            result = self.llm.generate(
                prompt,
                temperature=TEMPERATURE_ANALYSIS,
                max_tokens=2000,
                format="json",
                json_mode=True
            )
            
            response = result.get('response', '') if isinstance(result, dict) else str(result)
            
            # Parsowanie JSON
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except Exception as e:
            logger.error(f"Błąd podczas analizy HAMA Diamond: {e}")
        
        return self._simple_analysis(document_extraction)
    
    def _simple_analysis(
        self,
        document_extraction: DocumentExtraction
    ) -> Dict[str, Any]:
        """Prosta analiza bez LLM - tylko reguły"""
        text = document_extraction.text_content.lower()
        
        # Proste sprawdzenie warunków
        conditions = {
            "zdarzenie_nagłe": {
                "potwierdzone": any(word in text for word in ["nagle", "nagly", "nagłe", "nagły", "niespodziewanie"]),
                "pewnosc": 0.6,
                "uzasadnienie": "Analiza tekstu"
            },
            "przyczyna_zewnetrzna": {
                "potwierdzone": any(word in text for word in ["przyczyna", "spowodowane", "wywołane"]),
                "pewnosc": 0.6,
                "uzasadnienie": "Analiza tekstu"
            },
            "uraz_lub_smierc": {
                "potwierdzone": any(word in text for word in ["uraz", "obrażenie", "złamanie", "rany", "śmierć"]),
                "pewnosc": 0.7,
                "uzasadnienie": "Analiza tekstu"
            },
            "zwiazek_z_praca": {
                "potwierdzone": any(word in text for word in ["praca", "pracował", "w trakcie", "podczas pracy"]),
                "pewnosc": 0.6,
                "uzasadnienie": "Analiza tekstu"
            }
        }
        
        all_confirmed = all(c["potwierdzone"] for c in conditions.values())
        
        return {
            **conditions,
            "czynniki_wykluczajace": [],
            "ogolna_pewnosc": 0.6,
            "rekomendacja": "recognize" if all_confirmed else "needs_review",
            "uzasadnienie": "Analiza oparta na prostych regułach (LLM nie dostępne)"
        }
    
    def _check_accident_conditions(
        self,
        document_extraction: DocumentExtraction,
        hama_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Weryfikuje warunki definicji wypadku"""
        conditions = {}
        
        for condition in self.accident_definition["required_conditions"]:
            condition_data = hama_analysis.get(condition, {})
            conditions[condition] = {
                "confirmed": condition_data.get("potwierdzone", False),
                "confidence": condition_data.get("pewnosc", 0.5),
                "justification": condition_data.get("uzasadnienie", "")
            }
        
        return conditions
    
    def _apply_decision_rules(
        self,
        conditions_check: Dict[str, Any],
        hama_analysis: Dict[str, Any]
    ) -> tuple[DecisionRecommendation, float, str]:
        """
        Zastosowuje reguły decyzyjne i zwraca rekomendację
        """
        # Sprawdź czy wszystkie warunki są spełnione
        all_confirmed = all(
            cond["confirmed"] for cond in conditions_check.values()
        )
        
        # Sprawdź czynniki wykluczające
        exclusion_factors = hama_analysis.get("czynniki_wykluczajace", [])
        has_exclusions = len(exclusion_factors) > 0
        
        # Oblicz confidence
        avg_confidence = sum(
            cond["confidence"] for cond in conditions_check.values()
        ) / len(conditions_check) if conditions_check else 0.5
        
        overall_confidence = hama_analysis.get("ogolna_pewnosc", avg_confidence)
        
        # Zastosuj reguły
        if has_exclusions:
            decision = DecisionRecommendation.NOT_RECOGNIZE
            reasoning = f"Czynniki wykluczające: {', '.join(exclusion_factors)}"
        elif all_confirmed and overall_confidence >= self.decision_rules["uznac_wypadek"]["min_confidence"]:
            decision = DecisionRecommendation.RECOGNIZE
            reasoning = hama_analysis.get("uzasadnienie", "Wszystkie warunki definicji wypadku są spełnione")
        elif all_confirmed and overall_confidence < self.decision_rules["uznac_wypadek"]["min_confidence"]:
            decision = DecisionRecommendation.NEEDS_REVIEW
            reasoning = "Warunki spełnione, ale wymagana dodatkowa weryfikacja"
        else:
            decision = DecisionRecommendation.NEEDS_REVIEW
            reasoning = "Nie wszystkie warunki są jasno potwierdzone - wymagana weryfikacja"
        
        return decision, overall_confidence, reasoning
    
    def _extract_legal_basis(self, hama_analysis: Dict[str, Any]) -> List[str]:
        """Wyodrębnia podstawy prawne"""
        # Podstawowe przepisy
        legal_basis = [
            "Ustawa z dnia 30 października 2002 r. o ubezpieczeniu społecznym z tytułu wypadków przy pracy i chorób zawodowych"
        ]
        
        # Można dodać więcej na podstawie analizy
        if hama_analysis.get("uzasadnienie"):
            # Można użyć LLM do wyodrębnienia konkretnych artykułów
            pass
        
        return legal_basis
    
    def _identify_risk_factors(
        self,
        conditions_check: Dict[str, Any],
        hama_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identyfikuje czynniki ryzyka"""
        risk_factors = []
        
        # Sprawdź niską pewność warunków
        for condition, data in conditions_check.items():
            if data["confidence"] < 0.7:
                risk_factors.append(f"Niska pewność dla warunku: {condition}")
        
        # Czynniki wykluczające
        exclusion_factors = hama_analysis.get("czynniki_wykluczajace", [])
        risk_factors.extend(exclusion_factors)
        
        return risk_factors

