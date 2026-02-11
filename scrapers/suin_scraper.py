# scrapers/suin_scraper.py
from .base_scraper import BaseScraper
from typing import List, Dict, Optional
from datetime import datetime
import re
import json


class SuinScraper(BaseScraper):
    """
    Scraper for SUIN-Juriscol (Sistema Único de Información Normativa)
    Official Colombian legal information system
    https://www.suin-juriscol.gov.co/
    """

    BASE_URL = "https://www.suin-juriscol.gov.co"
    SEARCH_URL = f"{BASE_URL}/viewDocument.asp"
    API_URL = f"{BASE_URL}/api/busqueda"  # If they have an API

    def __init__(self):
        super().__init__("suin")

    def scrape_laws(self, start_year: int = 2020, end_year: int = None) -> List[Dict]:
        """
        Scrape laws from SUIN

        Args:
            start_year: Start year for scraping
            end_year: End year for scraping

        Returns:
            List of scraped laws
        """
        if end_year is None:
            end_year = datetime.now().year

        laws = []

        for year in range(start_year, end_year + 1):
            self.logger.info(f"Scraping SUIN for year {year}")
            year_laws = self.scrape_year(year)
            laws.extend(year_laws)
            self.logger.info(f"Found {len(year_laws)} laws for {year}")

        return laws

    def scrape_year(self, year: int, max_attempts: int = 100) -> List[Dict]:
        """Scrape all laws for a specific year"""
        laws = []

        # SUIN uses different URL patterns, try to search
        search_url = f"{self.BASE_URL}/clp/contenidos.dll/Leyes/{year}"

        soup = self.fetch_page(search_url)
        if not soup:
            self.logger.warning(f"Could not access SUIN for year {year}")
            return []

        # Parse the search results page
        # This will need to be adjusted based on actual SUIN structure
        law_links = soup.find_all('a', href=re.compile(r'viewDocument'))

        for link in law_links:
            law_url = link.get('href')
            if not law_url.startswith('http'):
                law_url = f"{self.BASE_URL}/{law_url}"

            law_data = self.scrape_single_law(law_url)
            if law_data:
                laws.append(law_data)

        return laws

    def scrape_single_law(self, url: str) -> Optional[Dict]:
        """
        Scrape a single law from SUIN

        Args:
            url: URL of the law

        Returns:
            Law data dictionary
        """
        soup = self.fetch_page(url)
        if not soup:
            return None

        try:
            # Extract law information
            # SUIN typically has better structured data

            # Try to find the main content
            content = soup.find('div', {'class': 'document-content'}) or \
                     soup.find('div', {'id': 'content'}) or \
                     soup.find('div', {'class': 'norma'})

            if not content:
                self.logger.warning(f"Could not find content in {url}")
                return None

            # Extract title
            title_tag = soup.find('h1') or soup.find('h2') or soup.find('title')
            title = title_tag.get_text(strip=True) if title_tag else "Unknown"

            # Extract law number and year
            law_match = re.search(r'Ley\s+(\d+)\s+de\s+(\d{4})', title, re.IGNORECASE)
            if law_match:
                law_num = law_match.group(1)
                year = int(law_match.group(2))
                law_number = f"Ley {law_num} de {year}"
            else:
                law_number = "Unknown"
                year = None

            # Extract full text
            full_text = content.get_text(separator='\n', strip=True)
            full_text = self._clean_text(full_text)

            # Look for publication date
            date_pattern = r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
            date_match = re.search(date_pattern, full_text[:2000])
            publication_date = self._parse_spanish_date(date_match) if date_match else None

            # Look for metadata
            metadata = soup.find('div', {'class': 'metadata'})
            issuing_entity = "Congreso de la República"  # Default

            if metadata:
                # Extract entity, status, etc.
                pass

            return {
                'law_number': law_number,
                'law_type': 'Ley',
                'year': year,
                'title': title,
                'publication_date': publication_date,
                'source_url': url,
                'source_name': self.source_name,
                'full_text': full_text,
                'pdf_url': None,  # SUIN might have PDFs
                'issuing_entity': issuing_entity,
                'status': 'vigente'
            }

        except Exception as e:
            self.logger.error(f"Error parsing SUIN law from {url}: {e}")
            return None

    def search_by_keyword(self, keyword: str, limit: int = 50) -> List[Dict]:
        """
        Search SUIN by keyword

        Args:
            keyword: Search term
            limit: Maximum results

        Returns:
            List of matching laws
        """
        self.logger.info(f"Searching SUIN for: {keyword}")

        # SUIN might have a search API or form
        search_url = f"{self.BASE_URL}/buscar"

        # Build search request
        params = {
            'q': keyword,
            'limit': limit
        }

        try:
            response = self.session.get(search_url, params=params)
            response.raise_for_status()

            soup = self.fetch_page(search_url)
            # Parse results...

            return []

        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []

    def _parse_spanish_date(self, match) -> Optional[str]:
        """Convert Spanish date to ISO format"""
        if not match:
            return None

        months = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
            'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
            'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }

        try:
            day, month_name, year = match.groups()
            month = months.get(month_name.lower())
            if month:
                return f"{year}-{month:02d}-{int(day):02d}"
        except:
            pass
        return None

    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'Imprimir\s*', '', text)
        text = re.sub(r'Compartir\s*', '', text)
        return text.strip()
