# parsers/ocr_parser.py
from typing import Optional, List
import logging
import os

try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class OCRParser:
    """Parser for extracting text from scanned PDFs using OCR"""

    def __init__(self):
        self.logger = logging.getLogger("ocr_parser")

        if not OCR_AVAILABLE:
            self.logger.warning("OCR dependencies not available. Install pdf2image and pytesseract.")

    def extract_text_from_scanned_pdf(self, pdf_path: str, language: str = 'spa') -> Optional[str]:
        """
        Extract text from scanned PDF using OCR

        Args:
            pdf_path: Path to scanned PDF
            language: Tesseract language code (default: 'spa' for Spanish)

        Returns:
            Extracted text or None if failed
        """
        if not OCR_AVAILABLE:
            self.logger.error("OCR not available. Install: pip install pdf2image pytesseract")
            return None

        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            return None

        try:
            self.logger.info(f"Starting OCR on {pdf_path}")

            # Convert PDF to images
            images = convert_from_path(pdf_path)
            self.logger.info(f"Converted PDF to {len(images)} images")

            text_parts = []

            for i, image in enumerate(images, 1):
                try:
                    self.logger.info(f"Processing page {i}/{len(images)}")

                    # Perform OCR
                    text = pytesseract.image_to_string(image, lang=language)

                    if text.strip():
                        text_parts.append(text)
                    else:
                        self.logger.warning(f"No text extracted from page {i}")

                except Exception as e:
                    self.logger.error(f"Error OCR-ing page {i}: {e}")
                    continue

            full_text = "\n\n".join(text_parts)

            if full_text.strip():
                self.logger.info(f"Successfully extracted {len(full_text)} characters via OCR")
                return full_text
            else:
                self.logger.warning("No text could be extracted via OCR")
                return None

        except Exception as e:
            self.logger.error(f"Error performing OCR on {pdf_path}: {e}")
            return None

    def extract_text_from_image(self, image_path: str, language: str = 'spa') -> Optional[str]:
        """
        Extract text from a single image file

        Args:
            image_path: Path to image file
            language: Tesseract language code

        Returns:
            Extracted text or None if failed
        """
        if not OCR_AVAILABLE:
            self.logger.error("OCR not available")
            return None

        try:
            from PIL import Image

            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang=language)

            return text.strip() if text else None

        except Exception as e:
            self.logger.error(f"Error extracting text from image {image_path}: {e}")
            return None

    def check_tesseract_installed(self) -> bool:
        """
        Check if Tesseract is installed and accessible

        Returns:
            True if Tesseract is available, False otherwise
        """
        if not OCR_AVAILABLE:
            return False

        try:
            version = pytesseract.get_tesseract_version()
            self.logger.info(f"Tesseract version: {version}")
            return True
        except Exception as e:
            self.logger.error(f"Tesseract not found: {e}")
            return False

    def get_available_languages(self) -> List[str]:
        """
        Get list of available Tesseract languages

        Returns:
            List of language codes
        """
        if not OCR_AVAILABLE:
            return []

        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception as e:
            self.logger.error(f"Error getting Tesseract languages: {e}")
            return []
