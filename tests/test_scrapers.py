# tests/test_scrapers.py
import unittest
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
from scrapers.senado_scraper import SenadoScraper
from processors.ai_processor import AIProcessor
from parsers.pdf_parser import PDFParser
import config


class TestSenadoScraper(unittest.TestCase):
    """Test cases for Senado scraper"""

    def setUp(self):
        self.scraper = SenadoScraper()

    def test_init(self):
        """Test scraper initialization"""
        self.assertEqual(self.scraper.source_name, "senado")
        self.assertIsNotNone(self.scraper.session)

    def test_clean_text(self):
        """Test text cleaning"""
        dirty_text = "   Texto   con    espacios    múltiples   \n\n\n\n   "
        clean = self.scraper._clean_text(dirty_text)
        self.assertNotIn("    ", clean)
        self.assertEqual(clean, "Texto con espacios múltiples")

    def test_parse_spanish_date(self):
        """Test Spanish date parsing"""
        import re
        text = "15 de marzo de 2024"
        match = re.search(r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', text)
        date = self.scraper._parse_spanish_date(match)
        self.assertEqual(date, "2024-03-15")

    @patch('scrapers.base_scraper.requests.Session.get')
    def test_fetch_page_success(self, mock_get):
        """Test successful page fetching"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body>Test</body></html>"
        mock_get.return_value = mock_response

        soup = self.scraper.fetch_page("http://example.com")
        self.assertIsNotNone(soup)
        self.assertIsInstance(soup, BeautifulSoup)

    @patch('scrapers.base_scraper.requests.Session.get')
    def test_fetch_page_failure(self, mock_get):
        """Test page fetching with errors"""
        mock_get.side_effect = Exception("Network error")

        soup = self.scraper.fetch_page("http://example.com")
        self.assertIsNone(soup)


class TestAIProcessor(unittest.TestCase):
    """Test cases for AI Processor"""

    def setUp(self):
        # Skip if no API key
        if not config.ANTHROPIC_API_KEY:
            self.skipTest("No ANTHROPIC_API_KEY set")
        self.processor = AIProcessor()

    def test_init(self):
        """Test processor initialization"""
        self.assertIsNotNone(self.processor.client)
        self.assertEqual(self.processor.model, "claude-3-5-sonnet-20241022")

    def test_truncate_text(self):
        """Test text truncation in summarization"""
        long_text = "A" * 10000
        # The processor should handle long texts
        self.assertTrue(len(long_text) > 8000)


class TestPDFParser(unittest.TestCase):
    """Test cases for PDF Parser"""

    def setUp(self):
        self.parser = PDFParser()

    def test_init(self):
        """Test parser initialization"""
        self.assertIsNotNone(self.parser.logger)

    def test_extract_text_nonexistent_file(self):
        """Test extraction from non-existent file"""
        result = self.parser.extract_text("/nonexistent/file.pdf")
        self.assertIsNone(result)


class TestHelpers(unittest.TestCase):
    """Test cases for utility helpers"""

    def test_clean_text(self):
        """Test text cleaning utility"""
        from utils.helpers import clean_text

        dirty = "Texto   con\n\n\n\nmuchos\t\t\tespacios"
        clean = clean_text(dirty)
        self.assertNotIn("   ", clean)
        self.assertNotIn("\n\n\n", clean)

    def test_extract_law_number(self):
        """Test law number extraction"""
        from utils.helpers import extract_law_number

        text = "Según la Ley 1234 de 2020, se establece..."
        law_num = extract_law_number(text)
        self.assertEqual(law_num, "Ley 1234 de 2020")

    def test_parse_colombian_date(self):
        """Test Colombian date parsing"""
        from utils.helpers import parse_colombian_date

        date_str = "15 de marzo de 2024"
        iso_date = parse_colombian_date(date_str)
        self.assertEqual(iso_date, "2024-03-15")

    def test_validate_law_data(self):
        """Test law data validation"""
        from utils.helpers import validate_law_data

        # Valid data
        valid_data = {
            'law_number': 'Ley 1234 de 2020',
            'title': 'Test Law',
            'source_url': 'http://example.com',
            'year': 2020,
            'full_text': 'A' * 100
        }
        errors = validate_law_data(valid_data)
        self.assertEqual(len(errors), 0)

        # Invalid data - missing fields
        invalid_data = {
            'title': 'Test Law'
        }
        errors = validate_law_data(invalid_data)
        self.assertGreater(len(errors), 0)

    def test_calculate_text_stats(self):
        """Test text statistics calculation"""
        from utils.helpers import calculate_text_stats

        text = "Esto es una prueba. Esta es otra oración."
        stats = calculate_text_stats(text)

        self.assertIn('characters', stats)
        self.assertIn('words', stats)
        self.assertIn('sentences', stats)
        self.assertGreater(stats['words'], 0)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
