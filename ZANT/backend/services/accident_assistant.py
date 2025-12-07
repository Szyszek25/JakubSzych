"""
HAMA Diamond-based Asystent Zgłoszenia Wypadku
Analizuje zgłoszenie i wykrywa brakujące elementy
Używa Google Gemini API
"""
import sys
import os
from typing import Dict, List, Any, Optional
import logging

# Dodaj ścieżki do adapterów
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'AIWSLUZBIE'))

try:
    from local_model_adapter import LocalModelAdapter
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    logging.warning("LocalModelAdapter nie dostępne - zainstaluj: pip install google-genai")

from backend.models.accident import AccidentReport, ReportAnalysis, MissingField
from backend.config import ZUS_ACCIDENT_REPORT_TEMPLATE, TEMPERATURE_ANALYSIS, GEMINI_MODEL_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AccidentAssistant:
    """
    Asystent zgłoszenia wypadku wykorzystujący HAMA Diamond
    Analizuje tekst zgłoszenia i wykrywa brakujące elementy
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
            logger.warning("⚠️ LLM nie dostępne - używam prostych reguł")
        
        self.template = ZUS_ACCIDENT_REPORT_TEMPLATE
        self.required_fields = self.template["required_fields"]
        self.field_descriptions = self.template["field_descriptions"]
    
    def analyze_report(self, report: AccidentReport) -> ReportAnalysis:
        """
        Analizuje zgłoszenie wypadku i wykrywa brakujące elementy
        """
        # Krok 1: Sprawdź które pola są wypełnione
        filled_fields = self._get_filled_fields(report)
        missing_fields_list = self._identify_missing_fields(filled_fields)
        
        # Krok 2: Użyj HAMA Diamond do analizy jakości wypełnionych pól
        suggestions = []
        validation_errors = []
        
        if self.llm:
            # Analiza jakości z użyciem LLM
            quality_analysis = self._analyze_quality_with_llm(report, filled_fields)
            suggestions.extend(quality_analysis.get("suggestions", []))
            validation_errors.extend(quality_analysis.get("errors", []))
        else:
            # Prosta walidacja bez LLM
            validation_errors = self._simple_validation(report)
        
        # Krok 3: Oblicz score kompletności
        completeness_score = len(filled_fields) / len(self.required_fields)
        
        # Krok 4: Wygeneruj sugestie dla brakujących pól
        missing_fields_with_suggestions = self._generate_suggestions_for_missing_fields(
            missing_fields_list,
            report
        )
        
        return ReportAnalysis(
            report_id=report.report_id,
            completeness_score=completeness_score,
            missing_fields=missing_fields_with_suggestions,
            suggestions=suggestions,
            validation_errors=validation_errors,
            confidence=0.85 if self.llm else 0.6
        )
    
    def _get_filled_fields(self, report: AccidentReport) -> Dict[str, Any]:
        """Zwraca słownik wypełnionych pól"""
        filled = {}
        for field in self.required_fields:
            value = getattr(report, field, None)
            if value and str(value).strip():
                filled[field] = value
        return filled
    
    def _identify_missing_fields(self, filled_fields: Dict[str, Any]) -> List[str]:
        """Identyfikuje brakujące pola"""
        return [field for field in self.required_fields if field not in filled_fields]
    
    def _analyze_quality_with_llm(
        self,
        report: AccidentReport,
        filled_fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analizuje jakość wypełnionych pól używając LLM"""
        if not self.llm:
            return {"suggestions": [], "errors": []}
        
        # Przygotuj prompt dla LLM
        filled_text = "\n".join([
            f"- {self.field_descriptions.get(field, field)}: {value}"
            for field, value in filled_fields.items()
        ])
        
        prompt = f"""
Jesteś asystentem ZUS pomagającym w zgłaszaniu wypadków przy pracy.

WYPEŁNIONE POLA:
{filled_text}

ZADANIE:
1. Oceń jakość wypełnionych pól
2. Wskaż czy opisy są wystarczająco szczegółowe
3. Zidentyfikuj potencjalne błędy lub niejasności
4. Zaproponuj konkretne ulepszenia

Odpowiedz w formacie JSON:
{{
  "suggestions": ["sugestia1", "sugestia2"],
  "errors": ["błąd1", "błąd2"],
  "quality_score": 0.85
}}
"""
        
        try:
            result = self.llm.generate(
                prompt,
                temperature=TEMPERATURE_ANALYSIS,
                max_tokens=1000,
                format="json",
                json_mode=True
            )
            
            response = result.get('response', '') if isinstance(result, dict) else str(result)
            
            # Parsowanie JSON
            import json
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except Exception as e:
            logger.error(f"Błąd podczas analizy LLM: {e}")
        
        return {"suggestions": [], "errors": []}
    
    def _simple_validation(self, report: AccidentReport) -> List[str]:
        """Prosta walidacja bez LLM"""
        errors = []
        
        # Walidacja daty
        if report.data_wypadku:
            import re
            if not re.match(r'\d{4}-\d{2}-\d{2}', report.data_wypadku):
                errors.append("Nieprawidłowy format daty (wymagany: YYYY-MM-DD)")
        
        # Walidacja godziny
        if report.godzina_wypadku:
            import re
            if not re.match(r'\d{2}:\d{2}', report.godzina_wypadku):
                errors.append("Nieprawidłowy format godziny (wymagany: HH:MM)")
        
        return errors
    
    def _generate_suggestions_for_missing_fields(
        self,
        missing_fields: List[str],
        report: AccidentReport
    ) -> List[MissingField]:
        """Generuje sugestie dla brakujących pól"""
        missing_with_suggestions = []
        
        for field in missing_fields:
            description = self.field_descriptions.get(field, field)
            
            # Określ priorytet
            high_priority_fields = ["data_wypadku", "miejsce_wypadku", "okolicznosci_wypadku"]
            priority = "high" if field in high_priority_fields else "medium"
            
            # Generuj sugestię używając LLM jeśli dostępne
            suggestion = None
            if self.llm:
                suggestion = self._generate_field_suggestion(field, description, report)
            
            missing_with_suggestions.append(
                MissingField(
                    field_name=field,
                    field_description=description,
                    priority=priority,
                    suggestion=suggestion
                )
            )
        
        return missing_with_suggestions
    
    def _generate_field_suggestion(
        self,
        field: str,
        description: str,
        report: AccidentReport
    ) -> Optional[str]:
        """Generuje sugestię dla konkretnego pola używając LLM"""
        if not self.llm:
            return None
        
        # Użyj kontekstu z wypełnionych pól
        context = ""
        if report.okolicznosci_wypadku:
            context = f"Okoliczności wypadku: {report.okolicznosci_wypadku[:200]}"
        
        prompt = f"""
Jesteś asystentem ZUS pomagającym wypełnić zgłoszenie wypadku.

BRAKUJĄCE POLE: {field}
OPIS POLA: {description}

KONTEKST:
{context}

ZADANIE:
Wygeneruj przyjazną, prostą sugestię jak wypełnić to pole. 
Użyj prostego języka, bez specjalistycznego słownictwa.
Maksymalnie 2-3 zdania.

Przykład: "Proszę podać dokładną datę wypadku w formacie YYYY-MM-DD, np. 2024-12-07"
"""
        
        try:
            result = self.llm.generate(
                prompt,
                temperature=TEMPERATURE_ANALYSIS,
                max_tokens=200
            )
            response = result.get('response', '') if isinstance(result, dict) else str(result)
            return response.strip()
        except Exception as e:
            logger.error(f"Błąd podczas generowania sugestii: {e}")
            return None

