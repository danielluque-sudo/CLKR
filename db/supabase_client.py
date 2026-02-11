# db/supabase_client.py
from typing import Dict, List, Optional
from supabase import create_client, Client
import logging
from datetime import datetime
import config


class SupabaseClient:
    """Client for interacting with Supabase database"""

    def __init__(self):
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            raise ValueError("Supabase credentials not set in environment")

        self.client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        self.logger = logging.getLogger("supabase_client")

    def insert_law(self, law_data: Dict) -> Optional[str]:
        """
        Insert a law into the database

        Args:
            law_data: Dictionary containing law information

        Returns:
            Law ID if successful, None otherwise
        """
        try:
            # Prepare data for insertion
            insert_data = {
                'law_number': law_data.get('law_number'),
                'law_type': law_data.get('law_type', 'Ley'),
                'year': law_data.get('year'),
                'title': law_data.get('title'),
                'summary': law_data.get('summary'),
                'full_text': law_data.get('full_text'),
                'publication_date': law_data.get('publication_date'),
                'source_url': law_data.get('source_url'),
                'source_name': law_data.get('source_name'),
                'pdf_url': law_data.get('pdf_url'),
                'issuing_entity': law_data.get('issuing_entity'),
                'subject_area': law_data.get('subject_area'),
                'status': law_data.get('status', 'vigente'),
                'scraped_at': datetime.now().isoformat()
            }

            # Remove None values
            insert_data = {k: v for k, v in insert_data.items() if v is not None}

            response = self.client.table('laws').insert(insert_data).execute()

            if response.data:
                law_id = response.data[0]['id']
                self.logger.info(f"Successfully inserted law: {law_data.get('law_number')} (ID: {law_id})")
                return law_id
            else:
                self.logger.error(f"Failed to insert law: {law_data.get('law_number')}")
                return None

        except Exception as e:
            self.logger.error(f"Error inserting law {law_data.get('law_number')}: {e}")
            return None

    def update_law(self, law_id: str, update_data: Dict) -> bool:
        """
        Update an existing law

        Args:
            law_id: ID of the law to update
            update_data: Dictionary of fields to update

        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.table('laws').update(update_data).eq('id', law_id).execute()

            if response.data:
                self.logger.info(f"Successfully updated law ID: {law_id}")
                return True
            else:
                self.logger.error(f"Failed to update law ID: {law_id}")
                return False

        except Exception as e:
            self.logger.error(f"Error updating law {law_id}: {e}")
            return False

    def get_law_by_number(self, law_number: str) -> Optional[Dict]:
        """
        Retrieve a law by its number

        Args:
            law_number: Law number (e.g., "Ley 1234 de 2020")

        Returns:
            Law data if found, None otherwise
        """
        try:
            response = self.client.table('laws').select('*').eq('law_number', law_number).execute()

            if response.data:
                return response.data[0]
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error retrieving law {law_number}: {e}")
            return None

    def get_laws_by_year(self, year: int) -> List[Dict]:
        """
        Get all laws from a specific year

        Args:
            year: Year to query

        Returns:
            List of law dictionaries
        """
        try:
            response = self.client.table('laws').select('*').eq('year', year).execute()
            return response.data if response.data else []

        except Exception as e:
            self.logger.error(f"Error retrieving laws for year {year}: {e}")
            return []

    def get_laws_by_subject(self, subject: str) -> List[Dict]:
        """
        Get all laws in a subject area

        Args:
            subject: Subject area

        Returns:
            List of law dictionaries
        """
        try:
            response = self.client.table('laws').select('*').ilike('subject_area', f'%{subject}%').execute()
            return response.data if response.data else []

        except Exception as e:
            self.logger.error(f"Error retrieving laws for subject {subject}: {e}")
            return []

    def search_laws(self, query: str, limit: int = 50) -> List[Dict]:
        """
        Full-text search across laws

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching laws
        """
        try:
            # Search in title, summary, and full_text
            response = self.client.table('laws').select('*').or_(
                f'title.ilike.%{query}%,summary.ilike.%{query}%,full_text.ilike.%{query}%'
            ).limit(limit).execute()

            return response.data if response.data else []

        except Exception as e:
            self.logger.error(f"Error searching laws with query '{query}': {e}")
            return []

    def insert_article(self, law_id: str, article_data: Dict) -> Optional[str]:
        """
        Insert an article for a law

        Args:
            law_id: ID of the parent law
            article_data: Article data

        Returns:
            Article ID if successful
        """
        try:
            insert_data = {
                'law_id': law_id,
                'article_number': article_data.get('article_number'),
                'content': article_data.get('content'),
                'created_at': datetime.now().isoformat()
            }

            response = self.client.table('articles').insert(insert_data).execute()

            if response.data:
                return response.data[0]['id']
            return None

        except Exception as e:
            self.logger.error(f"Error inserting article: {e}")
            return None

    def insert_amendment(self, law_id: str, amendment_data: Dict) -> Optional[str]:
        """
        Record an amendment relationship

        Args:
            law_id: ID of the amending law
            amendment_data: Amendment data

        Returns:
            Amendment ID if successful
        """
        try:
            insert_data = {
                'amending_law_id': law_id,
                'related_law_number': amendment_data.get('related_law'),
                'amendment_type': amendment_data.get('amendment_type'),
                'articles_affected': amendment_data.get('articles_affected'),
                'created_at': datetime.now().isoformat()
            }

            response = self.client.table('amendments').insert(insert_data).execute()

            if response.data:
                return response.data[0]['id']
            return None

        except Exception as e:
            self.logger.error(f"Error inserting amendment: {e}")
            return None

    def log_scraper_start(self, source: str, scrape_type: str) -> str:
        """
        Log the start of a scraping run

        Args:
            source: Source name (e.g., "senado")
            scrape_type: Type of scrape (e.g., "full_scrape", "incremental")

        Returns:
            Run ID
        """
        try:
            insert_data = {
                'source': source,
                'scrape_type': scrape_type,
                'status': 'running',
                'started_at': datetime.now().isoformat()
            }

            response = self.client.table('scraper_runs').insert(insert_data).execute()

            if response.data:
                run_id = response.data[0]['id']
                self.logger.info(f"Started scraper run: {run_id}")
                return run_id
            return None

        except Exception as e:
            self.logger.error(f"Error logging scraper start: {e}")
            return None

    def log_scraper_complete(self, run_id: str, laws_found: int, laws_processed: int):
        """
        Log the completion of a scraping run

        Args:
            run_id: Run ID from log_scraper_start
            laws_found: Number of laws found
            laws_processed: Number of laws successfully processed
        """
        try:
            update_data = {
                'status': 'completed',
                'completed_at': datetime.now().isoformat(),
                'laws_found': laws_found,
                'laws_processed': laws_processed
            }

            self.client.table('scraper_runs').update(update_data).eq('id', run_id).execute()
            self.logger.info(f"Completed scraper run: {run_id}")

        except Exception as e:
            self.logger.error(f"Error logging scraper completion: {e}")

    def log_scraper_failed(self, run_id: str, error_message: str):
        """
        Log a failed scraping run

        Args:
            run_id: Run ID
            error_message: Error description
        """
        try:
            update_data = {
                'status': 'failed',
                'completed_at': datetime.now().isoformat(),
                'error_message': error_message
            }

            self.client.table('scraper_runs').update(update_data).eq('id', run_id).execute()
            self.logger.info(f"Logged scraper failure: {run_id}")

        except Exception as e:
            self.logger.error(f"Error logging scraper failure: {e}")

    def get_latest_law_by_source(self, source: str) -> Optional[Dict]:
        """
        Get the most recent law from a source

        Args:
            source: Source name

        Returns:
            Most recent law data
        """
        try:
            response = self.client.table('laws').select('*').eq('source_name', source).order(
                'publication_date', desc=True
            ).limit(1).execute()

            if response.data:
                return response.data[0]
            return None

        except Exception as e:
            self.logger.error(f"Error getting latest law from {source}: {e}")
            return None

    def check_law_exists(self, law_number: str) -> bool:
        """
        Check if a law already exists in the database

        Args:
            law_number: Law number to check

        Returns:
            True if exists, False otherwise
        """
        try:
            response = self.client.table('laws').select('id').eq('law_number', law_number).execute()
            return bool(response.data)

        except Exception as e:
            self.logger.error(f"Error checking if law exists: {e}")
            return False
