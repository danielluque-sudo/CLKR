# scrapers/selenium_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from .senado_scraper import SenadoScraper
from bs4 import BeautifulSoup
import time


class SeleniumSenadoScraper(SenadoScraper):
    """
    Selenium-based scraper for Senado that bypasses anti-bot measures
    Uses a real Chrome browser to avoid 403 errors
    """

    def __init__(self):
        super().__init__()
        self.driver = None
        self._init_driver()

    def _init_driver(self):
        """Initialize Chrome WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

            # Add more realistic user agent
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            self.logger.info("Initializing Chrome WebDriver...")

            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )

            self.driver.set_page_load_timeout(30)
            self.logger.info("✅ Chrome WebDriver initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            self.driver = None

    def fetch_page(self, url: str, timeout: int = None) -> BeautifulSoup:
        """
        Fetch page using Selenium (overrides base class method)

        Args:
            url: URL to fetch
            timeout: Timeout in seconds

        Returns:
            BeautifulSoup object or None
        """
        if not self.driver:
            self.logger.error("WebDriver not initialized")
            return None

        try:
            self.logger.info(f"Fetching {url} with Selenium...")

            # Load the page
            self.driver.get(url)

            # Wait for page to load (wait for body tag)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                self.logger.warning(f"Timeout waiting for page to load: {url}")

            # Additional wait to ensure dynamic content loads
            time.sleep(2)

            # Get the page source
            html = self.driver.page_source

            # Check if we got a valid page (not an error page)
            if "404" in html or "403" in html or len(html) < 500:
                self.logger.warning(f"Got error page or very short content for {url}")
                return None

            soup = BeautifulSoup(html, 'html.parser')
            self.logger.info(f"✅ Successfully fetched {url} ({len(html)} chars)")

            # Rate limiting
            time.sleep(3)  # Be polite to the server

            return soup

        except WebDriverException as e:
            self.logger.error(f"WebDriver error for {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def __del__(self):
        """Clean up WebDriver on object destruction"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed")
            except:
                pass
