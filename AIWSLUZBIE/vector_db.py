"""
🗄️ Vector Database dla RAG (Retrieval-Augmented Generation)
Wykorzystuje ChromaDB do przechowywania i wyszukiwania precedensów prawnych
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# Opcjonalna zależność - ChromaDB
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    chromadb = None
    print("ℹ️ ChromaDB nie dostępne - używam symulacji. Zainstaluj: pip install chromadb")

class VectorDatabase:
    """Vector Database dla precedensów prawnych i dokumentów"""
    
    def __init__(self, persist_directory: str = "./vector_db"):
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self.available = False
        
        if CHROMADB_AVAILABLE:
            try:
                # Utwórz klienta ChromaDB
                self.client = chromadb.Client(Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=persist_directory,
                    anonymized_telemetry=False
                ))
                
                # Utwórz lub pobierz kolekcję precedensów
                self.collection = self.client.get_or_create_collection(
                    name="legal_precedents",
                    metadata={"description": "Baza precedensów prawnych i orzeczeń"}
                )
                
                self.available = True
                print(f"✅ Vector Database (ChromaDB) załadowana: {len(self.collection.get()['ids'])} dokumentów")
            except Exception as e:
                print(f"⚠️ Błąd inicjalizacji ChromaDB: {e}")
                print("   Używam symulacji")
        else:
            print("⚠️ ChromaDB nie dostępne - używam symulacji")
            self.precedents_cache = []
    
    def add_precedent(self, precedent: Dict[str, Any]) -> bool:
        """Dodanie precedensu do bazy"""
        if not self.available:
            # Symulacja
            self.precedents_cache.append(precedent)
            return True
        
        try:
            # Przygotuj dane
            doc_id = precedent.get('id', f"precedent_{datetime.now().timestamp()}")
            text = f"{precedent.get('summary', '')} {precedent.get('content', '')}"
            metadata = {
                'case_type': precedent.get('case_type', ''),
                'date': precedent.get('date', ''),
                'source': precedent.get('source', ''),
                'keywords': ','.join(precedent.get('keywords', []))
            }
            
            # Dodaj do kolekcji
            self.collection.add(
                documents=[text],
                ids=[doc_id],
                metadatas=[metadata]
            )
            
            return True
        except Exception as e:
            print(f"⚠️ Błąd dodawania precedensu: {e}")
            return False
    
    def search_precedents(self, query: str, case_type: Optional[str] = None, n_results: int = 5) -> List[Dict[str, Any]]:
        """Wyszukiwanie precedensów przez podobieństwo semantyczne"""
        if not self.available:
            # Symulacja - zwróć cache lub puste
            results = []
            query_lower = query.lower()
            for prec in self.precedents_cache:
                if query_lower in str(prec).lower():
                    results.append(prec)
            return results[:n_results]
        
        try:
            # Filtry metadanych
            where = {}
            if case_type:
                where['case_type'] = case_type
            
            # Wyszukaj podobne dokumenty
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where if where else None
            )
            
            # Przekształć wyniki
            precedents = []
            if results['ids'] and len(results['ids'][0]) > 0:
                for i, doc_id in enumerate(results['ids'][0]):
                    precedents.append({
                        'id': doc_id,
                        'summary': results['documents'][0][i][:200] if i < len(results['documents'][0]) else '',
                        'relevance_score': 1.0 - results['distances'][0][i] if i < len(results['distances'][0]) else 0.0,
                        'metadata': results['metadatas'][0][i] if i < len(results['metadatas'][0]) else {}
                    })
            
            return precedents
        except Exception as e:
            print(f"⚠️ Błąd wyszukiwania: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Statystyki bazy"""
        if not self.available:
            return {
                'total_documents': len(self.precedents_cache),
                'status': 'simulation'
            }
        
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'status': 'active',
                'collection': 'legal_precedents'
            }
        except Exception as e:
            return {
                'total_documents': 0,
                'status': 'error',
                'error': str(e)
            }
    
    def load_sample_precedents(self):
        """Ładowanie przykładowych precedensów (dla demo)"""
        sample_precedents = [
            {
                'id': 'prec_001',
                'case_type': 'kwalifikacja_zawodowa',
                'summary': 'Decyzja pozytywna w sprawie nadania kwalifikacji przewodnika turystycznego. Wnioskodawca posiadał wymagane wykształcenie wyższe na kierunku turystycznym.',
                'content': 'Decyzja wydana na podstawie art. 15 ust. 1 ustawy o usługach turystycznych. Wnioskodawca przedstawił dyplom ukończenia studiów wyższych na kierunku Turystyka i Rekreacja. Wszystkie wymagania formalne zostały spełnione.',
                'date': '2024-01-15',
                'source': 'MSiT',
                'keywords': ['kwalifikacja', 'przewodnik', 'dyplom', 'studia']
            },
            {
                'id': 'prec_002',
                'case_type': 'kategoria_hotelu',
                'summary': 'Przydział kategorii 4-gwiazdkowej dla obiektu hotelarskiego. Obiekt spełnia wszystkie wymagania standardów.',
                'content': 'Decyzja wydana na podstawie rozporządzenia w sprawie kategorii obiektów hotelarskich. Obiekt posiada wymagane wyposażenie, powierzchnię pokoi oraz standardy obsługi.',
                'date': '2024-02-20',
                'source': 'MSiT',
                'keywords': ['kategoria', 'hotel', '4-gwiazdkowy', 'standardy']
            },
            {
                'id': 'prec_003',
                'case_type': 'zakaz_dzialalnosci',
                'summary': 'Decyzja o zakazie działalności biura podróży z powodu poważnych naruszeń przepisów ochrony konsumenta.',
                'content': 'Decyzja wydana na podstawie art. 45 ustawy o usługach turystycznych. Stwierdzono wielokrotne naruszenia przepisów dotyczących umów z klientami oraz brak wymaganych ubezpieczeń.',
                'date': '2024-03-10',
                'source': 'MSiT',
                'keywords': ['zakaz', 'biuro podróży', 'naruszenia', 'ochrona konsumenta']
            }
        ]
        
        for precedent in sample_precedents:
            self.add_precedent(precedent)
        
        print(f"✅ Załadowano {len(sample_precedents)} przykładowych precedensów")

