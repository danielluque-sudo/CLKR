# scrapers/senado_scraper.py
from .base_scraper import BaseScraper
from typing import List, Dict, Optional
from datetime import datetime
import re


class SenadoScraper(BaseScraper):
    """Scraper for Secretaría del Senado (senado.gov.co)"""

    BASE_URL = "http://www.secretariasenado.gov.co"
    LAWS_URL = f"{BASE_URL}/senado/basedoc/ley_"

    def __init__(self):
        super().__init__("senado")

    def scrape_laws(self, start_year: int = 1990, end_year: int = None) -> List[Dict]:
        """
        Scrape laws from Senado
        Colombian laws are numbered sequentially per year
        """
        if end_year is None:
            end_year = datetime.now().year

        laws = []

        for year in range(start_year, end_year + 1):
            self.logger.info(f"Scraping laws for year {year}")
            year_laws = self.scrape_year(year)
            laws.extend(year_laws)
            self.logger.info(f"Found {len(year_laws)} laws for {year}")

        return laws

    def scrape_year(self, year: int, max_law_number: int = 300) -> List[Dict]:
        """Scrape all laws for a specific year"""
        laws = []
        consecutive_failures = 0

        for law_num in range(1, max_law_number + 1):
            law_data = self.scrape_law_by_number(law_num, year)

            if law_data:
                laws.append(law_data)
                consecutive_failures = 0
                self.logger.info(f"✓ Found: Ley {law_num} de {year}")
            else:
                consecutive_failures += 1

                # If we haven't found anything in 50 consecutive attempts, probably no more laws
                if consecutive_failures >= 50:
                    self.logger.info(f"No laws found for 50 consecutive numbers, stopping at {law_num}")
                    break

        return laws

    def scrape_law_by_number(self, law_number: int, year: int) -> Optional[Dict]:
        """Scrape a specific law by number and year"""
        # Senado URLs: ley_XXXX_YYYY.html
        url = f"{self.LAWS_URL}{law_number:04d}_{year}.html"

        soup = self.fetch_page(url)
        if not soup:
            return None

        try:
            # Extract title
            title_tag = soup.find(['h1', 'h2', 'h3'])
            if title_tag:
                title = title_tag.get_text(strip=True)
            else:
                title = f"Ley {law_number} de {year}"

            # Clean title - remove "LEY" prefix if present
            title = re.sub(r'^LEY\s+\d+\s+DE\s+\d+\s*-?\s*', '', title, flags=re.IGNORECASE)

            # Extract full text from main content
            content_div = soup.find('div', {'class': 'contenido'}) or \
                         soup.find('div', {'id': 'content'}) or \
                         soup.find('div', {'class': 'articulo'})

            if content_div:
                full_text = content_div.get_text(separator='\n', strip=True)
            else:
                # Fallback: get all text from body
                full_text = soup.get_text(separator='\n', strip=True)

            # Clean up the text
            full_text = self._clean_text(full_text)

            # Extract publication date
            date_pattern = r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
            date_match = re.search(date_pattern, full_text[:1000])
            publication_date = self._parse_spanish_date(date_match) if date_match else f"{year}-01-01"

            # Look for PDF link
            pdf_link = soup.find('a', href=re.compile(r'\.pdf$', re.I))
            if pdf_link and pdf_link.get('href'):
                href = pdf_link['href']
                pdf_url = href if href.startswith('http') else f"{self.BASE_URL}{href}"
            else:
                pdf_url = None

            # Validate we got meaningful content
            if len(full_text) < 100:
                self.logger.warning(f"Law {law_number}/{year} has very short content ({len(full_text)} chars)")

            return {
                'law_number': f"Ley {law_number} de {year}",
                'law_type': 'Ley',
                'year': year,
                'title': title,
                'publication_date': publication_date,
                'source_url': url,
                'source_name': self.source_name,
                'full_text': full_text,
                'pdf_url': pdf_url,
                'issuing_entity': 'Congreso de la República',
                'status': 'vigente'  # Default, can be updated later
            }

        except Exception as e:
            self.logger.error(f"Error parsing law {law_number}/{year}: {e}")
            return None

    def scrape_single_law(self, url: str) -> Optional[Dict]:
        """Scrape a single law from a direct URL"""
        # Extract year and law number from URL if possible
        match = re.search(r'ley_(\d{4})_(\d{4})\.html', url)
        if match:
            law_number = int(match.group(1))
            year = int(match.group(2))
            return self.scrape_law_by_number(law_number, year)

        return None

    def _parse_spanish_date(self, match) -> Optional[str]:
        """Convert Spanish date format to ISO format"""
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
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)

        # Remove common navigation/UI elements
        text = re.sub(r'Imprimir\s*', '', text)
        text = re.sub(r'Compartir\s*', '', text)
        text = re.sub(r'Descargar\s*', '', text)

        return text.strip()
