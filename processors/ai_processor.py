# processors/ai_processor.py
from typing import Dict, List, Optional, Tuple
import anthropic
import logging
import config
import re


class AIProcessor:
    """AI-powered processing of legal documents using Claude API"""

    def __init__(self):
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")

        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.logger = logging.getLogger("ai_processor")
        self.model = "claude-3-5-sonnet-20241022"

    def _call_claude(self, prompt: str, max_tokens: int = 4096) -> Optional[str]:
        """Make a call to Claude API with error handling"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            return None

    def summarize_law(self, full_text: str, max_length: int = 500) -> str:
        """
        Generate a concise summary of the law

        Args:
            full_text: Full text of the law
            max_length: Maximum characters for summary

        Returns:
            Summary text
        """
        # Truncate very long texts to save tokens
        text_sample = full_text[:8000] if len(full_text) > 8000 else full_text

        prompt = f"""Analiza la siguiente ley colombiana y proporciona un resumen conciso en español.

El resumen debe:
- Ser de máximo {max_length} caracteres
- Explicar el propósito principal de la ley
- Mencionar los puntos más importantes
- Estar escrito en lenguaje claro y directo

Ley:
{text_sample}

Resumen:"""

        summary = self._call_claude(prompt, max_tokens=1024)

        if summary:
            # Ensure it's within max_length
            if len(summary) > max_length:
                summary = summary[:max_length-3] + "..."
            return summary.strip()
        else:
            return "Error: No se pudo generar resumen"

    def classify_subject(self, title: str, full_text: str) -> str:
        """
        Classify the law into subject area(s)

        Args:
            title: Title of the law
            full_text: Full text of the law

        Returns:
            Subject area classification
        """
        # First try keyword matching
        text_combined = (title + " " + full_text[:2000]).lower()

        matches = []
        for subject, keywords in config.SUBJECT_AREAS.items():
            for keyword in keywords:
                if keyword.lower() in text_combined:
                    matches.append(subject)
                    break

        if matches:
            return ", ".join(matches[:3])  # Return top 3 matches

        # Fallback to AI classification
        prompt = f"""Clasifica la siguiente ley colombiana en una o más de estas categorías:

Categorías: laboral, tributario, civil, penal, comercial, administrativo, inmigración, ambiental, educación, salud

Título: {title}
Texto (muestra): {full_text[:2000]}

Responde solo con el nombre de la(s) categoría(s) separadas por comas, sin explicaciones adicionales.

Clasificación:"""

        result = self._call_claude(prompt, max_tokens=100)

        if result:
            return result.strip()
        else:
            return "general"

    def extract_articles(self, full_text: str) -> List[Dict[str, str]]:
        """
        Extract individual articles from the law

        Args:
            full_text: Full text of the law

        Returns:
            List of articles with their numbers and content
        """
        articles = []

        # Pattern to match articles: "ARTÍCULO 1", "Artículo 1.", "Art. 1", etc.
        pattern = r'(?:ARTÍCULO|Artículo|ART\.|Art\.?)\s*(\d+)[°º]?\.?\s*[–-]?\s*(.*?)(?=(?:ARTÍCULO|Artículo|ART\.|Art\.?)\s*\d+|$)'

        matches = re.finditer(pattern, full_text, re.IGNORECASE | re.DOTALL)

        for match in matches:
            article_num = match.group(1)
            article_text = match.group(2).strip()

            # Clean up article text
            article_text = re.sub(r'\s+', ' ', article_text)

            if len(article_text) > 20:  # Ignore very short matches
                articles.append({
                    'article_number': article_num,
                    'content': article_text[:5000]  # Limit length
                })

        return articles

    def detect_amendments(self, full_text: str, title: str) -> List[Dict[str, str]]:
        """
        Detect references to amendments of other laws

        Args:
            full_text: Full text of the law
            title: Title of the law

        Returns:
            List of detected amendments
        """
        amendments = []

        # Common amendment patterns in Spanish
        patterns = [
            r'modifica(?:r)? la Ley (\d+) de (\d{4})',
            r'adiciona(?:r)? la Ley (\d+) de (\d{4})',
            r'deroga(?:r)? la Ley (\d+) de (\d{4})',
            r'reforma(?:r)? la Ley (\d+) de (\d{4})',
            r'sustituye? (?:el|los) artículo[s]? ([\d\s,y]+) de la Ley (\d+) de (\d{4})'
        ]

        text_sample = title + " " + full_text[:5000]

        for pattern in patterns:
            matches = re.finditer(pattern, text_sample, re.IGNORECASE)
            for match in matches:
                if 'sustituye' in pattern:
                    articles = match.group(1)
                    law_num = match.group(2)
                    year = match.group(3)
                else:
                    law_num = match.group(1)
                    year = match.group(2)
                    articles = None

                amendment_type = 'modificación'
                if 'adiciona' in pattern:
                    amendment_type = 'adición'
                elif 'deroga' in pattern:
                    amendment_type = 'derogación'
                elif 'reforma' in pattern:
                    amendment_type = 'reforma'
                elif 'sustituye' in pattern:
                    amendment_type = 'sustitución'

                amendments.append({
                    'related_law': f"Ley {law_num} de {year}",
                    'amendment_type': amendment_type,
                    'articles_affected': articles
                })

        return amendments

    def extract_keywords(self, title: str, full_text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract key terms and concepts from the law

        Args:
            title: Title of the law
            full_text: Full text of the law
            max_keywords: Maximum number of keywords to extract

        Returns:
            List of keywords
        """
        text_sample = full_text[:4000] if len(full_text) > 4000 else full_text

        prompt = f"""Extrae las {max_keywords} palabras clave o conceptos más importantes de esta ley colombiana.

Título: {title}
Texto: {text_sample}

Responde solo con las palabras clave separadas por comas, sin numeración ni explicaciones.

Palabras clave:"""

        result = self._call_claude(prompt, max_tokens=200)

        if result:
            keywords = [k.strip() for k in result.split(',')]
            return keywords[:max_keywords]
        else:
            # Fallback: extract from title
            words = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{3,}\b', title)
            return words[:5]

    def detect_law_relations(self, full_text: str) -> List[Dict[str, str]]:
        """
        Detect references to other laws and regulations

        Args:
            full_text: Full text of the law

        Returns:
            List of related laws
        """
        relations = []

        # Pattern to match law references
        law_pattern = r'Ley (\d+) de (\d{4})'
        decree_pattern = r'Decreto (\d+) de (\d{4})'

        text_sample = full_text[:8000]

        # Find law references
        law_matches = re.finditer(law_pattern, text_sample)
        for match in law_matches:
            law_num = match.group(1)
            year = match.group(2)
            relations.append({
                'related_law': f"Ley {law_num} de {year}",
                'relation_type': 'referencia'
            })

        # Find decree references
        decree_matches = re.finditer(decree_pattern, text_sample)
        for match in decree_matches:
            decree_num = match.group(1)
            year = match.group(2)
            relations.append({
                'related_law': f"Decreto {decree_num} de {year}",
                'relation_type': 'referencia'
            })

        # Remove duplicates
        unique_relations = []
        seen = set()
        for rel in relations:
            key = rel['related_law']
            if key not in seen:
                seen.add(key)
                unique_relations.append(rel)

        return unique_relations[:20]  # Limit to 20 relations

    def translate_to_english(self, text: str, max_length: int = 2000) -> str:
        """
        Translate Spanish text to English (for international users)

        Args:
            text: Spanish text to translate
            max_length: Maximum length of text to translate

        Returns:
            Translated English text
        """
        text_sample = text[:max_length]

        prompt = f"""Translate the following Spanish legal text to English. Maintain legal terminology accuracy.

Spanish text:
{text_sample}

English translation:"""

        result = self._call_claude(prompt, max_tokens=2048)

        return result.strip() if result else "Translation unavailable"

    def analyze_impact(self, full_text: str, title: str) -> Dict[str, any]:
        """
        Analyze the potential impact and scope of the law

        Args:
            full_text: Full text of the law
            title: Title of the law

        Returns:
            Impact analysis dictionary
        """
        text_sample = full_text[:4000]

        prompt = f"""Analiza el impacto y alcance de esta ley colombiana.

Título: {title}
Texto: {text_sample}

Proporciona:
1. Población o sector afectado (una línea)
2. Tipo de impacto (económico, social, regulatorio, etc.) (una palabra)
3. Alcance (nacional, regional, sectorial) (una palabra)

Formato de respuesta:
Afectados: [respuesta]
Impacto: [respuesta]
Alcance: [respuesta]"""

        result = self._call_claude(prompt, max_tokens=300)

        impact_data = {
            'affected_population': 'No especificado',
            'impact_type': 'general',
            'scope': 'nacional'
        }

        if result:
            # Parse the response
            if 'Afectados:' in result:
                affected = re.search(r'Afectados:\s*(.+?)(?:\n|$)', result)
                if affected:
                    impact_data['affected_population'] = affected.group(1).strip()

            if 'Impacto:' in result:
                impact = re.search(r'Impacto:\s*(.+?)(?:\n|$)', result)
                if impact:
                    impact_data['impact_type'] = impact.group(1).strip()

            if 'Alcance:' in result:
                scope = re.search(r'Alcance:\s*(.+?)(?:\n|$)', result)
                if scope:
                    impact_data['scope'] = scope.group(1).strip()

        return impact_data
