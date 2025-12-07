"""
📄 Chunkowanie dokumentów dla długich tekstów
Dzieli długie dokumenty na mniejsze fragmenty dla lepszej obsługi kontekstu
"""

from typing import List, Dict, Any
import re

class DocumentChunker:
    """Klasa do dzielenia długich dokumentów na mniejsze fragmenty"""
    
    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 200):
        """
        Args:
            chunk_size: Maksymalna długość chunka (znaki)
            chunk_overlap: Nakładka między chunkami (znaki)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Dzieli dokument na mniejsze fragmenty
        
        Args:
            document: Dokument do podziału (musi mieć 'content')
            
        Returns:
            Lista fragmentów dokumentu
        """
        content = document.get('content', '')
        doc_type = document.get('type', 'unknown')
        doc_id = document.get('id', 'unknown')
        
        # Jeśli dokument jest krótki, zwróć jako jeden chunk
        if len(content) <= self.chunk_size:
            return [{
                'id': f"{doc_id}_chunk_0",
                'type': doc_type,
                'content': content,
                'chunk_index': 0,
                'total_chunks': 1,
                'start_char': 0,
                'end_char': len(content)
            }]
        
        # Dziel na fragmenty
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(content):
            # Określ koniec chunka
            end = min(start + self.chunk_size, len(content))
            
            # Spróbuj znaleźć naturalne miejsce podziału (koniec zdania/akapitu)
            if end < len(content):
                # Szukaj końca zdania lub akapitu
                natural_break = self._find_natural_break(content, start, end)
                if natural_break > start:
                    end = natural_break
            
            # Wyciągnij fragment
            chunk_content = content[start:end].strip()
            
            if chunk_content:  # Tylko jeśli fragment nie jest pusty
                chunks.append({
                    'id': f"{doc_id}_chunk_{chunk_index}",
                    'type': doc_type,
                    'content': chunk_content,
                    'chunk_index': chunk_index,
                    'total_chunks': 0,  # Zaktualizujemy później
                    'start_char': start,
                    'end_char': end
                })
                chunk_index += 1
            
            # Przesuń start z nakładką
            start = end - self.chunk_overlap
            if start >= len(content):
                break
        
        # Zaktualizuj total_chunks
        for chunk in chunks:
            chunk['total_chunks'] = len(chunks)
        
        return chunks
    
    def _find_natural_break(self, text: str, start: int, end: int) -> int:
        """Znajduje naturalne miejsce podziału (koniec zdania/akapitu)"""
        # Szukaj od końca chunka wstecz
        search_text = text[start:end]
        
        # Priorytety: koniec akapitu > koniec zdania > spacja
        patterns = [
            r'\n\n',  # Podwójny enter (akapit)
            r'\.\s+[A-ZĄĆĘŁŃÓŚŹŻ]',  # Koniec zdania + wielka litera
            r'\.\s*\n',  # Koniec zdania + nowa linia
            r'[.!?]\s+',  # Koniec zdania
            r'\s+',  # Spacja
        ]
        
        for pattern in patterns:
            matches = list(re.finditer(pattern, search_text))
            if matches:
                # Weź ostatnie dopasowanie przed końcem
                for match in reversed(matches):
                    pos = start + match.end()
                    if pos >= start + self.chunk_size * 0.7:  # Nie za wcześnie
                        return pos
        
        return end  # Jeśli nie znaleziono, użyj końca
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Dzieli tekst na fragmenty
        
        Args:
            text: Tekst do podziału
            metadata: Opcjonalne metadane do dodania do każdego chunka
            
        Returns:
            Lista fragmentów
        """
        document = {
            'content': text,
            'type': metadata.get('type', 'text') if metadata else 'text',
            'id': metadata.get('id', 'text') if metadata else 'text'
        }
        
        chunks = self.chunk_document(document)
        
        # Dodaj metadane jeśli podano
        if metadata:
            for chunk in chunks:
                chunk.update({k: v for k, v in metadata.items() if k not in ['content', 'type', 'id']})
        
        return chunks
    
    def merge_chunks(self, chunks: List[Dict[str, Any]], max_length: int = None) -> str:
        """
        Łączy chunków z powrotem w tekst
        
        Args:
            chunks: Lista fragmentów
            max_length: Maksymalna długość (opcjonalnie)
            
        Returns:
            Połączony tekst
        """
        # Sortuj po chunk_index
        sorted_chunks = sorted(chunks, key=lambda x: x.get('chunk_index', 0))
        
        # Usuń duplikaty (nakładki)
        merged_text = ""
        last_end = -1
        
        for chunk in sorted_chunks:
            start = chunk.get('start_char', 0)
            content = chunk.get('content', '')
            
            if start > last_end:
                merged_text += content + "\n\n"
                last_end = chunk.get('end_char', start + len(content))
            elif start == last_end:
                merged_text += content + "\n\n"
                last_end = chunk.get('end_char', start + len(content))
        
        if max_length and len(merged_text) > max_length:
            return merged_text[:max_length] + "..."
        
        return merged_text.strip()

