"""
Moduł zbierania danych z określonych źródeł internetowych
"""
import requests
from bs4 import BeautifulSoup
import feedparser  
from newspaper import Article  # type: ignore
from typing import List, Dict, Optional
from datetime import datetime
import asyncio
import aiohttp  # type: ignore
from dataclasses import dataclass
import logging
from urllib.parse import urljoin, urlparse
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DataSource:
    """Reprezentacja źródła danych"""
    url: str
    title: str
    content: str
    date: Optional[datetime]
    source_type: str  # 'ministry', 'institution', 'think_tank'
    country: Optional[str] = None
    language: str = "en"
    tags: Optional[List[str]] = None


class DataCollector:
    """Klasa odpowiedzialna za zbieranie danych z określonych źródeł"""
    
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.collected_data: List[DataSource] = []
        
    def _is_valid_date(self, date_str: str) -> bool:
        """Sprawdza czy data jest po 31 grudnia 2020"""
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            threshold = datetime.strptime(self.config["date_threshold"], "%Y-%m-%d")
            return date >= threshold
        except:
            return False
    
    def _extract_text_from_url(self, url: str) -> Optional[str]:
        """Ekstraktuje tekst z URL używając newspaper3k"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            logger.warning(f"Nie udało się pobrać tekstu z {url}: {e}")
            return None
    
    def _scrape_ministry_page(self, base_url: str, country: str, ministry: str) -> List[DataSource]:
        """Pobiera dane ze strony ministerstwa"""
        sources = []
        
        # Próba znalezienia RSS feed
        rss_urls = [
            f"{base_url}/feed",
            f"{base_url}/rss",
            f"{base_url}/news/feed",
            f"{base_url}/en/feed"
        ]
        
        for rss_url in rss_urls:
            try:
                feed = feedparser.parse(rss_url)
                if feed.entries:
                    for entry in feed.entries[:20]:  # Ostatnie 20 wpisów
                        if hasattr(entry, 'published'):
                            if self._is_valid_date(entry.published[:10]):
                                content = self._extract_text_from_url(entry.link)
                                if content:
                                    sources.append(DataSource(
                                        url=entry.link,
                                        title=entry.title,
                                        content=content,
                                        date=datetime.strptime(entry.published[:10], "%Y-%m-%d"),
                                        source_type="ministry",
                                        country=country,
                                        language="en"
                                    ))
            except Exception as e:
                logger.debug(f"RSS feed nie dostępny dla {rss_url}: {e}")
        
        # Jeśli RSS nie działa, próba bezpośredniego scrapingu
        try:
            response = self.session.get(base_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Szukanie linków do newsów/komunikatów
                news_links = soup.find_all('a', href=True)
                for link in news_links[:10]:  # Pierwsze 10 linków
                    # Bezpieczne pobranie atrybutu href używając getattr
                    href_attr = getattr(link, 'get', lambda key, default='': default)('href', '')
                    if not href_attr or not isinstance(href_attr, str):
                        continue
                    href = urljoin(base_url, str(href_attr))
                    if any(keyword in href.lower() for keyword in ['news', 'press', 'statement', 'announcement']):
                        content = self._extract_text_from_url(href)
                        if content:
                            # Bezpieczne pobranie tekstu
                            get_text_method = getattr(link, 'get_text', None)
                            title = get_text_method(strip=True) if get_text_method else 'No title'
                            sources.append(DataSource(
                                url=href,
                                title=title,
                                content=content,
                                date=datetime.now(),  # Domyślna data
                                source_type="ministry",
                                country=country,
                                language="en"
                            ))
        except Exception as e:
            logger.warning(f"Błąd podczas scrapingu {base_url}: {e}")
        
        return sources
    
    def collect_ministry_data(self) -> List[DataSource]:
        """Zbiera dane ze stron ministerstw"""
        all_sources = []
        
        # Mapowanie krajów na domeny (przykładowe)
        country_domains = {
            "Germany": "https://www.auswaertiges-amt.de",
            "France": "https://www.diplomatie.gouv.fr",
            "UK": "https://www.gov.uk/government/organisations/foreign-commonwealth-development-office",
            "USA": "https://www.state.gov",
            "Russia": "https://mid.ru",
            "China": "https://www.fmprc.gov.cn",
            "India": "https://www.mea.gov.in",
            "Saudi Arabia": "https://www.mofa.gov.sa"
        }
        
        for country, base_url in country_domains.items():
            for ministry in self.config["ministries"]["ministries"]:
                # Konstrukcja URL (może wymagać dostosowania dla każdego kraju)
                ministry_url = f"{base_url}/en"  # Próba wersji angielskiej
                sources = self._scrape_ministry_page(ministry_url, country, ministry)
                all_sources.extend(sources)
                time.sleep(1)  # Rate limiting
        
        return all_sources
    
    def collect_institution_data(self) -> List[DataSource]:
        """Zbiera dane z instytucji międzynarodowych"""
        all_sources = []
        
        institution_urls = {
            "European Commission": "https://ec.europa.eu",
            "NATO": "https://www.nato.int",
            "UN": "https://www.un.org",
            "OECD": "https://www.oecd.org",
            "International Institute for Strategic Studies": "https://www.iiss.org",
            "Center for Strategic and International Studies": "https://www.csis.org",
            "Chatham House": "https://www.chathamhouse.org",
            "European Council on Foreign Relations": "https://ecfr.eu",
            "Atlantic Council": "https://www.atlanticcouncil.org",
            "Kiel Institute": "https://www.ifw-kiel.de"
        }
        
        for institution, base_url in institution_urls.items():
            try:
                # Próba RSS
                rss_url = f"{base_url}/feed"
                feed = feedparser.parse(rss_url)
                if feed.entries:
                    for entry in feed.entries[:15]:
                        if hasattr(entry, 'published'):
                            if self._is_valid_date(entry.published[:10]):
                                content = self._extract_text_from_url(entry.link)
                                if content:
                                    all_sources.append(DataSource(
                                        url=entry.link,
                                        title=entry.title,
                                        content=content,
                                        date=datetime.strptime(entry.published[:10], "%Y-%m-%d"),
                                        source_type="institution",
                                        language="en"
                                    ))
            except Exception as e:
                logger.warning(f"Błąd podczas pobierania danych z {institution}: {e}")
        
        return all_sources
    
    def collect_all_data(self) -> List[DataSource]:
        """Zbiera wszystkie dane z określonych źródeł"""
        logger.info("Rozpoczynam zbieranie danych...")
        
        all_sources = []
        all_sources.extend(self.collect_ministry_data())
        all_sources.extend(self.collect_institution_data())
        
        # Filtrowanie po dacie
        filtered_sources = [
            s for s in all_sources 
            if s.date and s.date >= datetime.strptime(self.config["date_threshold"], "%Y-%m-%d")
        ]
        
        logger.info(f"Zebrano {len(filtered_sources)} źródeł danych")
        self.collected_data = filtered_sources
        return filtered_sources
    
    def get_data_summary(self) -> Dict:
        """Zwraca podsumowanie zebranych danych"""
        return {
            "total_sources": len(self.collected_data),
            "by_type": {},
            "by_country": {},
            "total_words": sum(len(s.content.split()) for s in self.collected_data)
        }

