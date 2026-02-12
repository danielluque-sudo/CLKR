# scrapers/base_scraper.py
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
import certifi
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time
import config


class BaseScraper(ABC):
    """Base class for all legal document scrapers"""

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-CO,es;q=0.9,en;q=0.8',
        })
        # Force a known CA bundle to avoid missing system certs in containers.
        self.session.verify = certifi.where()
        if config.SCRAPER_DISABLE_SSL_VERIFY:
            self.logger.warning("SCRAPER_DISABLE_SSL_VERIFY=true: SSL verification disabled")
            self.session.verify = False
        self.logger = logging.getLogger(f"scraper.{source_name}")

    @abstractmethod
    def scrape_laws(self, start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None) -> List[Dict]:
        """Scrape laws from the source"""
        pass

    @abstractmethod
    def scrape_single_law(self, url: str) -> Optional[Dict]:
        """Scrape a single law document"""
        pass

    def fetch_page(self, url: str, timeout: int = None) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page with retry logic"""
        if timeout is None:
            timeout = config.TIMEOUT

        for attempt in range(config.MAX_RETRIES):
            try:
                self.logger.info(f"Fetching {url} (attempt {attempt + 1}/{config.MAX_RETRIES})")
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()

                # Rate limiting
                time.sleep(config.SCRAPER_DELAY)

                return BeautifulSoup(response.content, 'html.parser')

            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < config.MAX_RETRIES - 1:
                    time.sleep(5 * (attempt + 1))  # Exponential backoff
                else:
                    self.logger.error(f"Failed to fetch {url} after {config.MAX_RETRIES} attempts")
                    return None
            except Exception as e:
                self.logger.error(f"Unexpected error fetching {url}: {e}")
                return None

    def download_pdf(self, url: str, save_path: str) -> bool:
        """Download PDF file with retry logic"""
        for attempt in range(config.MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=config.TIMEOUT)
                response.raise_for_status()
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
            except Exception as e:
                self.logger.error(f"Error downloading PDF {url} (attempt {attempt + 1}): {e}")
                if attempt < config.MAX_RETRIES - 1:
                    time.sleep(3)
        return False
