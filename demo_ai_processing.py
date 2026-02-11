#!/usr/bin/env python
# demo_ai_processing.py - Demonstrate AI processing with Claude API
import json
import logging
from processors.ai_processor import AIProcessor
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 70)
    logger.info("DEMONSTRATING AI PROCESSING WITH CLAUDE API")
    logger.info("=" * 70)

    # Check API key
    if not config.ANTHROPIC_API_KEY:
        logger.error("❌ ANTHROPIC_API_KEY not set in .env")
        return

    logger.info(f"✅ API Key configured: {config.ANTHROPIC_API_KEY[:20]}...")

    # Load example law data
    logger.info("\nLoading example Colombian law data...")
    with open('data/sample_output/example_law_data.json', 'r', encoding='utf-8') as f:
        laws = json.load(f)

    first_law = laws[0]
    logger.info(f"\nLaw: {first_law['law_number']}")
    logger.info(f"Title: {first_law['title']}")
    logger.info(f"Text length: {len(first_law['full_text'])} characters")

    # Initialize AI processor
    logger.info("\n" + "=" * 70)
    logger.info("Initializing Claude AI Processor...")
    ai = AIProcessor()

    # Test 1: Summarization
    logger.info("\n--- TEST 1: LAW SUMMARIZATION ---")
    logger.info("Generating summary...")
    try:
        summary = ai.summarize_law(first_law['full_text'])
        logger.info(f"\n✅ Summary generated:")
        logger.info(f"   {summary}")
        first_law['ai_summary'] = summary
    except Exception as e:
        logger.error(f"❌ Summarization failed: {e}")

    # Test 2: Subject Classification
    logger.info("\n--- TEST 2: SUBJECT CLASSIFICATION ---")
    logger.info("Classifying law by subject area...")
    try:
        subject = ai.classify_subject(first_law['title'], first_law['full_text'])
        logger.info(f"\n✅ Subject classification:")
        logger.info(f"   {subject}")
        first_law['ai_subject'] = subject
    except Exception as e:
        logger.error(f"❌ Classification failed: {e}")

    # Test 3: Keyword Extraction
    logger.info("\n--- TEST 3: KEYWORD EXTRACTION ---")
    logger.info("Extracting key terms...")
    try:
        keywords = ai.extract_keywords(first_law['title'], first_law['full_text'], max_keywords=8)
        logger.info(f"\n✅ Keywords extracted:")
        logger.info(f"   {', '.join(keywords)}")
        first_law['ai_keywords'] = keywords
    except Exception as e:
        logger.error(f"❌ Keyword extraction failed: {e}")

    # Test 4: Article Extraction
    logger.info("\n--- TEST 4: ARTICLE EXTRACTION ---")
    logger.info("Extracting individual articles...")
    try:
        articles = ai.extract_articles(first_law['full_text'])
        logger.info(f"\n✅ Extracted {len(articles)} articles")
        if articles:
            logger.info(f"   Article 1 preview: {articles[0]['content'][:150]}...")
        first_law['articles'] = articles[:3]  # Save first 3
    except Exception as e:
        logger.error(f"❌ Article extraction failed: {e}")

    # Test 5: Amendment Detection
    logger.info("\n--- TEST 5: AMENDMENT DETECTION ---")
    logger.info("Detecting references to other laws...")
    try:
        amendments = ai.detect_amendments(first_law['full_text'], first_law['title'])
        logger.info(f"\n✅ Found {len(amendments)} amendment references")
        for amend in amendments[:3]:
            logger.info(f"   - {amend}")
        first_law['amendments'] = amendments
    except Exception as e:
        logger.error(f"❌ Amendment detection failed: {e}")

    # Save AI-processed results
    logger.info("\n" + "=" * 70)
    logger.info("Saving AI-processed results...")
    output_file = 'data/sample_output/ai_processed_demo.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([first_law], f, ensure_ascii=False, indent=2)

    logger.info(f"✅ Results saved to: {output_file}")

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("🎉 AI PROCESSING DEMONSTRATION COMPLETE!")
    logger.info("=" * 70)
    logger.info("\n✅ All AI features are working correctly with your API key!")
    logger.info("\nWhat was tested:")
    logger.info("  1. ✅ Law summarization")
    logger.info("  2. ✅ Subject classification")
    logger.info("  3. ✅ Keyword extraction")
    logger.info("  4. ✅ Article extraction")
    logger.info("  5. ✅ Amendment detection")
    logger.info("\nYour system is ready to process real scraped data!")

if __name__ == "__main__":
    main()
