"""
Moduł ekstrakcji danych z dokumentów PDF
Wykorzystuje OCR do odczytu zeskanowanych dokumentów
"""
import os
import time
from typing import Dict, Any, Optional
import logging
from pathlib import Path

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    import pdf2image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from backend.models.accident import DocumentExtraction
from backend.config import OCR_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFExtractor:
    """Ekstraktor danych z PDF - obsługuje zarówno tekstowe jak i zeskanowane dokumenty"""
    
    def __init__(self):
        self.ocr_enabled = OCR_CONFIG.get("engine") == "tesseract" and TESSERACT_AVAILABLE
        if not self.ocr_enabled:
            logger.warning("⚠️ OCR nie dostępne - tylko tekstowe PDF będą obsługiwane")
    
    def extract_from_pdf(self, pdf_path: str) -> DocumentExtraction:
        """
        Ekstrahuje dane z pliku PDF
        Próbuje najpierw wyodrębnić tekst, jeśli nie ma - używa OCR
        """
        start_time = time.time()
        document_id = Path(pdf_path).stem
        
        # Krok 1: Próba wyodrębnienia tekstu bezpośrednio z PDF
        text_content = self._extract_text_from_pdf(pdf_path)
        ocr_used = False
        
        # Krok 2: Jeśli tekst jest pusty lub bardzo krótki, użyj OCR
        if not text_content or len(text_content.strip()) < 50:
            logger.info("Tekst z PDF jest pusty, używam OCR...")
            text_content = self._extract_with_ocr(pdf_path)
            ocr_used = True
        
        # Krok 3: Wyodrębnij strukturalne dane z tekstu
        extracted_fields = self._extract_structured_data(text_content)
        
        processing_time = time.time() - start_time
        
        return DocumentExtraction(
            document_id=document_id,
            text_content=text_content,
            extracted_fields=extracted_fields,
            confidence=0.8 if text_content else 0.3,
            processing_time=processing_time,
            ocr_used=ocr_used
        )
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Wyodrębnia tekst bezpośrednio z PDF (dla tekstowych PDF)"""
        if not PDFPLUMBER_AVAILABLE:
            logger.warning("pdfplumber nie dostępne")
            return ""
        
        try:
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"Błąd podczas wyodrębniania tekstu z PDF: {e}")
            return ""
    
    def _extract_with_ocr(self, pdf_path: str) -> str:
        """Wyodrębnia tekst z zeskanowanego PDF używając OCR"""
        if not self.ocr_enabled:
            logger.warning("OCR nie dostępne")
            return ""
        
        try:
            # Konwersja PDF na obrazy
            images = pdf2image.convert_from_path(pdf_path)
            
            text_parts = []
            for img in images:
                # OCR na każdym obrazie
                text = pytesseract.image_to_string(img, lang=OCR_CONFIG.get("language", "pol"))
                text_parts.append(text)
            
            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"Błąd podczas OCR: {e}")
            return ""
    
    def _extract_structured_data(self, text: str) -> Dict[str, Any]:
        """
        Wyodrębnia strukturalne dane z tekstu
        Używa prostych wzorców regex + HAMA do inteligentnej ekstrakcji
        """
        import re
        from datetime import datetime
        
        extracted = {}
        
        # Wzorce dla typowych pól
        patterns = {
            "data_wypadku": [
                r"data[:\s]+(\d{4}[-/]\d{2}[-/]\d{2})",
                r"(\d{2}\.\d{2}\.\d{4})",
                r"(\d{2}/\d{2}/\d{4})"
            ],
            "godzina_wypadku": [
                r"godzina[:\s]+(\d{2}:\d{2})",
                r"(\d{2}:\d{2})"
            ],
            "miejsce_wypadku": [
                r"miejsce[:\s]+(.+?)(?:\n|$)",
                r"adres[:\s]+(.+?)(?:\n|$)"
            ],
            "dane_poszkodowanego": [
                r"poszkodowany[:\s]+(.+?)(?:\n|$)",
                r"imie[:\s]+(.+?)\s+nazwisko[:\s]+(.+?)(?:\n|$)"
            ]
        }
        
        for field, field_patterns in patterns.items():
            for pattern in field_patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    extracted[field] = match.group(1) if match.groups() else match.group(0)
                    break
        
        # Dodaj pełny tekst jako fallback
        extracted["full_text"] = text[:5000]  # Ograniczenie do 5000 znaków
        
        return extracted

