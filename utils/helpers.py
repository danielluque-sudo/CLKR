# utils/helpers.py
from typing import Dict, List, Optional
import re
from datetime import datetime


def clean_text(text: str) -> str:
    """
    Clean and normalize text

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)

    return text.strip()


def extract_law_number(text: str) -> Optional[str]:
    """
    Extract law number from text

    Args:
        text: Text to search

    Returns:
        Law number or None
    """
    patterns = [
        r'Ley\s+(\d+)\s+de\s+(\d{4})',
        r'Decreto\s+(\d+)\s+de\s+(\d{4})',
        r'Resolución\s+(\d+)\s+de\s+(\d{4})'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)

    return None


def parse_colombian_date(date_str: str) -> Optional[str]:
    """
    Parse Colombian date format to ISO format

    Args:
        date_str: Date string in Spanish

    Returns:
        ISO format date string or None
    """
    months = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }

    # Pattern: "1 de enero de 2020" or "01 de enero de 2020"
    pattern = r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
    match = re.search(pattern, date_str, re.IGNORECASE)

    if match:
        day = int(match.group(1))
        month_name = match.group(2).lower()
        year = int(match.group(3))

        month = months.get(month_name)
        if month:
            return f"{year}-{month:02d}-{day:02d}"

    return None


def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """
    Truncate text to maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def calculate_text_stats(text: str) -> Dict[str, int]:
    """
    Calculate statistics about text

    Args:
        text: Text to analyze

    Returns:
        Dictionary of statistics
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)

    return {
        'characters': len(text),
        'words': len(words),
        'sentences': len(sentences),
        'paragraphs': len(text.split('\n\n')),
        'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0
    }


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def validate_law_data(law_data: Dict) -> List[str]:
    """
    Validate law data dictionary

    Args:
        law_data: Law data to validate

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    required_fields = ['law_number', 'title', 'source_url']

    for field in required_fields:
        if field not in law_data or not law_data[field]:
            errors.append(f"Missing required field: {field}")

    if 'year' in law_data:
        year = law_data['year']
        if not isinstance(year, int) or year < 1900 or year > datetime.now().year + 1:
            errors.append(f"Invalid year: {year}")

    if 'full_text' in law_data:
        text_len = len(law_data['full_text'])
        if text_len < 50:
            errors.append(f"Full text too short: {text_len} characters")

    return errors


def merge_law_data(existing: Dict, new: Dict) -> Dict:
    """
    Merge new law data with existing, preferring non-empty values

    Args:
        existing: Existing law data
        new: New law data

    Returns:
        Merged dictionary
    """
    merged = existing.copy()

    for key, value in new.items():
        if value and (key not in merged or not merged[key]):
            merged[key] = value

    return merged
