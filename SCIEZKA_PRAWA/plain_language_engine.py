"""
GQPA Plain Language Engine
Moduł upraszczania języka urzędowego
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from config import PLAIN_LANGUAGE_CONFIG


@dataclass
class SimplifiedText:
    """Uproszczona wersja tekstu"""
    original: str
    simplified: str
    complexity_score: float  # 0.0 = bardzo prosty, 1.0 = bardzo złożony
    changes: List[Dict[str, str]]  # Lista zmian: {"type": "...", "original": "...", "simplified": "..."}
    readability_score: float  # Wskaźnik czytelności (wyższy = lepszy)


class PlainLanguageEngine:
    """
    Silnik upraszczania języka urzędowego
    Wykorzystuje GQPA do analizy semantycznej i parafrazy
    """
    
    def __init__(self):
        self.config = PLAIN_LANGUAGE_CONFIG
        self.complex_patterns = [
            (r'\b(zgodnie z przepisami|zgodnie z art\.|na podstawie|w myśl)', 'zgodnie z'),
            (r'\b(przeprowadzić|zrealizować|wykonać)', 'zrobić'),
            (r'\b(przedsięwzięcie|działanie|operacja)', 'działanie'),
            (r'\b(obowiązany|zobowiązany)', 'musi'),
            (r'\b(uprawniony|ma prawo)', 'może'),
            (r'\b(ustanowiony|określony|wyznaczony)', 'ustalony'),
            (r'\b(przeprowadzany|realizowany)', 'wykonywany'),
            (r'\b(przedmiotowy|omawiany)', 'ten'),
            (r'\b(przeprowadzić analizę)', 'przeanalizować'),
            (r'\b(zawiadomić|powiadomić)', 'poinformować'),
        ]
        
    def simplify_text(self, text: str, use_llm: bool = False) -> SimplifiedText:
        """
        Upraszcza tekst urzędowy
        
        Args:
            text: Tekst do uproszczenia
            use_llm: Czy używać LLM do głębszej analizy (wymaga GQPA)
        """
        original = text
        simplified = text
        changes = []
        
        # 1. Podstawowe uproszczenia (reguły)
        for pattern, replacement in self.complex_patterns:
            matches = re.finditer(pattern, simplified, re.IGNORECASE)
            for match in matches:
                original_phrase = match.group(0)
                simplified_phrase = replacement
                if original_phrase.lower() != simplified_phrase.lower():
                    changes.append({
                        "type": "phrase_replacement",
                        "original": original_phrase,
                        "simplified": simplified_phrase
                    })
                simplified = simplified.replace(original_phrase, simplified_phrase)
        
        # 2. Dzielenie długich zdań
        sentences = re.split(r'[.!?]+', simplified)
        simplified_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Jeśli zdanie jest za długie, spróbuj podzielić
            if len(sentence.split()) > self.config["max_sentence_length"]:
                # Podziel na przecinki lub spójniki
                parts = re.split(r'[,;]\s+(oraz|i|oraz|a także|ponadto)', sentence)
                if len(parts) > 1:
                    simplified_sentences.extend([p.strip() for p in parts if p.strip()])
                    changes.append({
                        "type": "sentence_split",
                        "original": sentence,
                        "simplified": " | ".join([p.strip() for p in parts if p.strip()])
                    })
                else:
                    simplified_sentences.append(sentence)
            else:
                simplified_sentences.append(sentence)
        
        simplified = ". ".join(simplified_sentences)
        if simplified and not simplified.endswith(('.', '!', '?')):
            simplified += "."
        
        # 3. Upraszczanie liczb i dat
        simplified = self._simplify_numbers(simplified, changes)
        
        # 4. Usuwanie zbędnych słów
        simplified = self._remove_redundancy(simplified, changes)
        
        # 5. Obliczanie metryk
        complexity_score = self._calculate_complexity(original, simplified)
        readability_score = self._calculate_readability(simplified)
        
        return SimplifiedText(
            original=original,
            simplified=simplified,
            complexity_score=complexity_score,
            changes=changes,
            readability_score=readability_score
        )
    
    def _simplify_numbers(self, text: str, changes: List[Dict]) -> str:
        """Upraszcza zapis liczb"""
        # Zamień "30 dni" na "miesiąc" jeśli to ma sens
        # (uproszczona wersja - w pełnej implementacji użyjemy GQPA)
        return text
    
    def _remove_redundancy(self, text: str, changes: List[Dict]) -> str:
        """Usuwa zbędne powtórzenia"""
        # Usuń powtórzenia słów w bliskim sąsiedztwie
        words = text.split()
        cleaned_words = []
        prev_word = None
        
        for word in words:
            if word.lower() != prev_word:
                cleaned_words.append(word)
            prev_word = word.lower()
        
        return " ".join(cleaned_words)
    
    def _calculate_complexity(self, original: str, simplified: str) -> float:
        """Oblicza wskaźnik złożoności (0.0-1.0)"""
        # Prosty wskaźnik oparty na długości słów i zdań
        original_words = original.split()
        simplified_words = simplified.split()
        
        avg_word_len_orig = sum(len(w) for w in original_words) / len(original_words) if original_words else 0
        avg_word_len_simp = sum(len(w) for w in simplified_words) / len(simplified_words) if simplified_words else 0
        
        # Normalizuj do 0-1
        complexity = min(1.0, (avg_word_len_orig - 5) / 10)  # Założenie: słowa >15 znaków = złożone
        
        return max(0.0, min(1.0, complexity))
    
    def _calculate_readability(self, text: str) -> float:
        """Oblicza wskaźnik czytelności (0.0-1.0, wyższy = lepszy)"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        
        if not sentences or not words:
            return 0.5
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(w) for w in words) / len(words)
        
        # Wskaźnik Flesch (uproszczony)
        # Im krótsze zdania i słowa, tym wyższy wynik
        readability = 1.0 - min(1.0, (avg_sentence_length / 30) * 0.5 + (avg_word_length / 10) * 0.5)
        
        return max(0.0, min(1.0, readability))
    
    def simplify_legal_document(self, document_text: str, 
                                sections: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Upraszcza cały dokument prawny
        
        Args:
            document_text: Pełny tekst dokumentu
            sections: Opcjonalna lista sekcji do uproszczenia
        """
        # Podziel na sekcje (artykuły)
        if sections:
            section_texts = sections
        else:
            # Automatyczne wykrywanie sekcji
            section_texts = re.split(r'\n\s*(Art\.|§|Rozdział)', document_text)
            section_texts = [s.strip() for s in section_texts if s.strip()]
        
        simplified_sections = []
        total_changes = []
        
        for section in section_texts:
            if not section.strip():
                continue
            
            simplified = self.simplify_text(section)
            simplified_sections.append({
                "original": simplified.original,
                "simplified": simplified.simplified,
                "complexity_score": simplified.complexity_score,
                "readability_score": simplified.readability_score,
                "changes": simplified.changes
            })
            total_changes.extend(simplified.changes)
        
        # Oblicz średnie metryki
        avg_complexity = sum(s["complexity_score"] for s in simplified_sections) / len(simplified_sections) if simplified_sections else 0.0
        avg_readability = sum(s["readability_score"] for s in simplified_sections) / len(simplified_sections) if simplified_sections else 0.0
        
        return {
            "original_document": document_text,
            "simplified_sections": simplified_sections,
            "overall_complexity": avg_complexity,
            "overall_readability": avg_readability,
            "total_changes": len(total_changes),
            "improvement_percentage": max(0, (1.0 - avg_complexity) * 100)
        }
    
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generuje krótkie streszczenie tekstu"""
        # Uproszczona wersja - w pełnej implementacji użyjemy GQPA do ekstrakcji kluczowych informacji
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Wybierz pierwsze zdania do limitu
        summary_sentences = []
        current_length = 0
        
        for sentence in sentences:
            if current_length + len(sentence) <= max_length:
                summary_sentences.append(sentence)
                current_length += len(sentence)
            else:
                break
        
        summary = ". ".join(summary_sentences)
        if summary and not summary.endswith('.'):
            summary += "."
        
        return summary

