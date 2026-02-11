# parsers/pdf_parser.py
from typing import Optional
import PyPDF2
import logging
import os


class PDFParser:
    """Parser for extracting text from PDF files"""

    def __init__(self):
        self.logger = logging.getLogger("pdf_parser")

    def extract_text(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from a PDF file

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text or None if failed
        """
        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            return None

        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)

                self.logger.info(f"Processing PDF with {num_pages} pages: {pdf_path}")

                text_parts = []

                for page_num in range(num_pages):
                    try:
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()

                        if text:
                            text_parts.append(text)
                        else:
                            self.logger.warning(f"No text extracted from page {page_num + 1}")

                    except Exception as e:
                        self.logger.error(f"Error extracting page {page_num + 1}: {e}")
                        continue

                full_text = "\n\n".join(text_parts)

                if full_text.strip():
                    self.logger.info(f"Successfully extracted {len(full_text)} characters from PDF")
                    return full_text
                else:
                    self.logger.warning("No text could be extracted from PDF")
                    return None

        except Exception as e:
            self.logger.error(f"Error parsing PDF {pdf_path}: {e}")
            return None

    def get_pdf_metadata(self, pdf_path: str) -> dict:
        """
        Extract metadata from PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary of metadata
        """
        metadata = {}

        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                if pdf_reader.metadata:
                    metadata = {
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'creator': pdf_reader.metadata.get('/Creator', ''),
                        'producer': pdf_reader.metadata.get('/Producer', ''),
                        'creation_date': pdf_reader.metadata.get('/CreationDate', ''),
                    }

                metadata['num_pages'] = len(pdf_reader.pages)

        except Exception as e:
            self.logger.error(f"Error extracting PDF metadata: {e}")

        return metadata

    def is_scanned_pdf(self, pdf_path: str) -> bool:
        """
        Check if PDF appears to be a scanned document (image-based)

        Args:
            pdf_path: Path to PDF file

        Returns:
            True if appears to be scanned, False otherwise
        """
        try:
            text = self.extract_text(pdf_path)

            if not text or len(text.strip()) < 100:
                return True  # Likely scanned

            # Check ratio of extracted text to pages
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                avg_chars_per_page = len(text) / num_pages

                # If very few characters per page, likely scanned
                if avg_chars_per_page < 50:
                    return True

            return False

        except Exception as e:
            self.logger.error(f"Error checking if PDF is scanned: {e}")
            return True  # Assume scanned if we can't determine
