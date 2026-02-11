# main.py
import logging
import argparse
import json
import os
from datetime import datetime
from scrapers.senado_scraper import SenadoScraper
from db.supabase_client import SupabaseClient
from processors.ai_processor import AIProcessor
import config

# Setup logging
os.makedirs(config.LOGS_DIR, exist_ok=True)
os.makedirs(config.SAMPLE_OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{config.LOGS_DIR}/scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def save_to_json(data: list, filename: str):
    """Save scraped data to JSON file"""
    filepath = os.path.join(config.SAMPLE_OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved data to {filepath}")


def test_scraper(year: int = 2024, max_laws: int = 5):
    """Test mode: scrape a few laws and save to JSON"""
    logger.info(f"=== TEST MODE: Scraping up to {max_laws} laws from {year} ===")

    scraper = SenadoScraper()

    # Scrape laws
    all_laws = scraper.scrape_year(year, max_law_number=50)
    laws = all_laws[:max_laws]  # Limit to test amount

    logger.info(f"Scraped {len(laws)} laws")

    # Save raw scraped data
    save_to_json(laws, f'test_raw_laws_{year}.json')

    # Test AI processing on first law if we got any
    if laws and config.ANTHROPIC_API_KEY:
        logger.info("Testing AI processing on first law...")
        try:
            ai = AIProcessor()

            first_law = laws[0]

            # Generate summary
            summary = ai.summarize_law(first_law['full_text'])
            logger.info(f"Summary: {summary[:200]}...")

            # Classify subject
            subject = ai.classify_subject(first_law['title'], first_law['full_text'])
            logger.info(f"Subject: {subject}")

            # Save processed version
            first_law['summary'] = summary
            first_law['subject_area'] = subject
            save_to_json([first_law], f'test_processed_law_{year}.json')

        except Exception as e:
            logger.warning(f"AI processing skipped: {e}")
            logger.info("To enable AI processing, set ANTHROPIC_API_KEY in .env file")

    # Calculate statistics
    if laws:
        total_chars = sum(len(law.get('full_text', '')) for law in laws)
        avg_chars = total_chars / len(laws)
        logger.info(f"Average text length: {avg_chars:.0f} characters per law")

    logger.info("=== TEST COMPLETE ===")
    logger.info(f"Check the output in {config.SAMPLE_OUTPUT_DIR}/")

    return laws


def full_scrape(start_year: int, end_year: int = None, save_to_db: bool = True):
    """Full scrape with database storage"""
    if end_year is None:
        end_year = datetime.now().year

    logger.info(f"=== FULL SCRAPE: {start_year} to {end_year} ===")

    scraper = SenadoScraper()

    if config.ANTHROPIC_API_KEY:
        ai = AIProcessor()
    else:
        ai = None
        logger.warning("ANTHROPIC_API_KEY not set - AI processing disabled")

    if save_to_db:
        try:
            db = SupabaseClient()
            run_id = db.log_scraper_start('senado', 'full_scrape')
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            logger.info("Continuing without database storage...")
            save_to_db = False

    try:
        laws = scraper.scrape_laws(start_year=start_year, end_year=end_year)
        logger.info(f"Scraped {len(laws)} laws total")

        # Save raw data
        save_to_json(laws, f'full_scrape_{start_year}_{end_year}_raw.json')

        processed_count = 0
        for i, law_data in enumerate(laws, 1):
            logger.info(f"[{i}/{len(laws)}] Processing {law_data['law_number']}")

            # AI processing
            if ai and law_data.get('full_text') and len(law_data['full_text']) > 100:
                try:
                    law_data['summary'] = ai.summarize_law(law_data['full_text'])
                    law_data['subject_area'] = ai.classify_subject(law_data['title'], law_data['full_text'])
                except Exception as e:
                    logger.error(f"AI processing failed for {law_data['law_number']}: {e}")

            # Save to database
            if save_to_db:
                law_id = db.insert_law(law_data)
                if law_id:
                    processed_count += 1

            # Save checkpoint every 10 laws
            if i % 10 == 0:
                save_to_json(laws[:i], f'checkpoint_{start_year}_{end_year}_processed.json')

        if save_to_db:
            db.log_scraper_complete(run_id, len(laws), processed_count)

        logger.info(f"=== SCRAPE COMPLETE: {processed_count}/{len(laws)} laws processed ===")

    except Exception as e:
        logger.error(f"Scrape failed: {e}", exc_info=True)
        if save_to_db:
            db.log_scraper_failed(run_id, str(e))


def incremental_update(source: str = 'senado'):
    """Incremental update: only scrape new laws since last run"""
    logger.info(f"=== INCREMENTAL UPDATE: {source} ===")

    try:
        db = SupabaseClient()

        # Get the most recent law in database
        latest_law = db.get_latest_law_by_source(source)

        if latest_law:
            last_year = latest_law['year']
            logger.info(f"Last law in database: {latest_law['law_number']} ({last_year})")
            start_year = last_year
        else:
            logger.info("No laws in database, starting from 2023")
            start_year = 2023

        current_year = datetime.now().year

        # Run full scrape for the relevant years
        full_scrape(start_year, current_year, save_to_db=True)

    except Exception as e:
        logger.error(f"Incremental update failed: {e}", exc_info=True)


def main():
    parser = argparse.ArgumentParser(description='Colombian Legal Database Scraper')
    parser.add_argument('mode', choices=['test', 'full', 'incremental'],
                        help='Scraper mode')
    parser.add_argument('--start-year', type=int, default=2024,
                       help='Start year for scraping')
    parser.add_argument('--end-year', type=int, default=None,
                       help='End year for scraping')
    parser.add_argument('--max-laws', type=int, default=5,
                       help='Maximum laws for test mode')
    parser.add_argument('--no-db', action='store_true',
                       help='Skip database storage (JSON only)')

    args = parser.parse_args()

    logger.info(f"Starting scraper in {args.mode} mode")

    if args.mode == 'test':
        test_scraper(year=args.start_year, max_laws=args.max_laws)
    elif args.mode == 'full':
        full_scrape(args.start_year, args.end_year, save_to_db=not args.no_db)
    elif args.mode == 'incremental':
        incremental_update()

    logger.info("Scraper finished successfully")


if __name__ == "__main__":
    main()
