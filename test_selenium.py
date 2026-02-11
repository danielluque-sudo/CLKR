#!/usr/bin/env python
# test_selenium.py - Test Selenium scraper
import logging
import sys
import json
from scrapers.selenium_scraper import SeleniumSenadoScraper
from processors.ai_processor import AIProcessor
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 60)
    logger.info("Testing Selenium Scraper for Colombian Laws")
    logger.info("=" * 60)

    # Initialize scraper
    logger.info("Initializing Selenium scraper...")
    scraper = SeleniumSenadoScraper()

    # Test with 2023 (recent year)
    year = 2023
    max_laws = 3

    logger.info(f"\nScraping up to {max_laws} laws from {year}...")

    laws = []
    for law_num in range(1, 10):  # Try first 10 law numbers
        if len(laws) >= max_laws:
            break

        logger.info(f"\n--- Trying Law {law_num} of {year} ---")
        law_data = scraper.scrape_law_by_number(law_num, year)

        if law_data:
            laws.append(law_data)
            logger.info(f"✅ SUCCESS: {law_data['law_number']}")
            logger.info(f"   Title: {law_data['title'][:100]}...")
            logger.info(f"   Text length: {len(law_data.get('full_text', ''))} chars")
        else:
            logger.info(f"❌ Law {law_num} not found or failed")

    logger.info(f"\n{'=' * 60}")
    logger.info(f"RESULTS: Successfully scraped {len(laws)} laws")
    logger.info(f"{'=' * 60}")

    if laws:
        # Save results
        output_file = 'data/sample_output/selenium_test_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(laws, f, ensure_ascii=False, indent=2)
        logger.info(f"\n✅ Results saved to: {output_file}")

        # Test AI processing if API key is set
        if config.ANTHROPIC_API_KEY:
            logger.info("\n--- Testing AI Processing ---")
            try:
                ai = AIProcessor()
                first_law = laws[0]

                logger.info(f"Summarizing: {first_law['law_number']}...")
                summary = ai.summarize_law(first_law['full_text'])
                logger.info(f"Summary: {summary[:200]}...")

                logger.info(f"\nClassifying subject area...")
                subject = ai.classify_subject(first_law['title'], first_law['full_text'])
                logger.info(f"Subject: {subject}")

                first_law['summary'] = summary
                first_law['subject_area'] = subject

                # Save processed version
                with open('data/sample_output/selenium_test_processed.json', 'w', encoding='utf-8') as f:
                    json.dump([first_law], f, ensure_ascii=False, indent=2)

                logger.info("\n✅ AI processing successful!")

            except Exception as e:
                logger.error(f"AI processing failed: {e}")
        else:
            logger.info("\n⚠️ ANTHROPIC_API_KEY not set - skipping AI processing")

        # Statistics
        total_chars = sum(len(law.get('full_text', '')) for law in laws)
        avg_chars = total_chars / len(laws) if laws else 0

        logger.info(f"\n--- Statistics ---")
        logger.info(f"Laws scraped: {len(laws)}")
        logger.info(f"Total characters: {total_chars:,}")
        logger.info(f"Average per law: {avg_chars:,.0f} characters")

        logger.info("\n🎉 TEST SUCCESSFUL! Selenium scraper is working!")

    else:
        logger.error("\n❌ No laws were scraped. Check the logs above for errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
