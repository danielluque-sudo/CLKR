# Colombian Legal Database Scraper

An automated system for scraping, processing, and analyzing Colombian legal documents using web scraping and AI.

## Overview

This project creates a comprehensive database of Colombian laws by:
- Scraping legal documents from multiple government sources (Senado, Función Pública, DIAN)
- Extracting text from HTML and PDF documents
- Using Claude AI to summarize, classify, and analyze laws
- Detecting amendments and relationships between laws
- Storing structured data in Supabase (PostgreSQL)

## Features

- **Multi-Source Scraping**: Collect laws from various Colombian government websites
- **AI-Powered Analysis**:
  - Automatic summarization of laws
  - Subject area classification
  - Article extraction
  - Amendment detection
  - Keyword extraction
- **Robust PDF Processing**: Extract text from both digital and scanned PDFs (with OCR)
- **Database Integration**: Store and query laws in Supabase
- **Incremental Updates**: Run daily updates to capture new laws
- **Test Mode**: Test scraping without API costs
- **Comprehensive Logging**: Track all operations and errors

## Project Structure

```
colombian-legal-db/
├── scrapers/           # Web scraping modules
│   ├── base_scraper.py
│   ├── senado_scraper.py
│   ├── funcionpublica_scraper.py
│   └── dian_scraper.py
├── parsers/            # PDF and OCR parsing
│   ├── pdf_parser.py
│   ├── ocr_parser.py
│   └── law_parser.py
├── processors/         # AI processing
│   ├── ai_processor.py
│   ├── relationship_detector.py
│   └── keyword_extractor.py
├── db/                 # Database interaction
│   ├── supabase_client.py
│   └── models.py
├── utils/              # Utility functions
│   ├── logger.py
│   └── helpers.py
├── tests/              # Unit tests
├── data/               # Output data
│   └── sample_output/
├── logs/               # Log files
├── config.py           # Configuration
├── main.py             # Main entry point
└── requirements.txt    # Dependencies
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- (Optional) Tesseract OCR for scanned PDFs

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/colombian-legal-db.git
cd colombian-legal-db
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Copy the example environment file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
ANTHROPIC_API_KEY=sk-ant-your-api-key
TEST_MODE=false
```

### Step 5: (Optional) Install Tesseract for OCR

For processing scanned PDFs:

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-spa
```

**Mac:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## Usage

### Test Mode (Recommended First)

Test the scraper without using API credits:

```bash
python main.py test --start-year 2024 --max-laws 3 --no-db
```

This will:
- Scrape 3 laws from 2024
- Save results to `data/sample_output/test_raw_laws_2024.json`
- Skip AI processing and database storage

### Test Mode with AI Processing

If you have an Anthropic API key:

```bash
python main.py test --start-year 2024 --max-laws 3 --no-db
```

This will also process the first law with Claude AI.

### Full Scrape

Scrape all laws for a year range:

```bash
# Scrape laws from 2020 to 2024
python main.py full --start-year 2020 --end-year 2024

# Scrape laws from 2024 only (without database)
python main.py full --start-year 2024 --end-year 2024 --no-db
```

### Incremental Update

Update the database with new laws since the last run:

```bash
python main.py incremental
```

This automatically detects the most recent law in your database and scrapes only newer laws.

## Command Line Options

```
main.py [-h] {test,full,incremental} [options]

Arguments:
  mode                  Scraper mode: test, full, or incremental

Options:
  --start-year YEAR     Start year for scraping (default: 2024)
  --end-year YEAR       End year for scraping (default: current year)
  --max-laws N          Maximum laws for test mode (default: 5)
  --no-db               Skip database storage, save to JSON only
```

## Architecture

### Scrapers

**Base Scraper** (`scrapers/base_scraper.py`)
- Abstract base class for all scrapers
- Handles HTTP requests with retry logic
- Rate limiting and error handling

**Senado Scraper** (`scrapers/senado_scraper.py`)
- Scrapes laws from Secretaría del Senado
- URL pattern: `http://www.secretariasenado.gov.co/senado/basedoc/ley_XXXX_YYYY.html`
- Extracts title, full text, publication date, and PDF links

### AI Processor

**AIProcessor** (`processors/ai_processor.py`)

Methods:
- `summarize_law()`: Generate concise summaries
- `classify_subject()`: Classify into subject areas (laboral, tributario, civil, etc.)
- `extract_articles()`: Parse individual articles
- `detect_amendments()`: Identify references to other laws
- `extract_keywords()`: Extract key terms
- `detect_law_relations()`: Find related laws
- `translate_to_english()`: Translate to English
- `analyze_impact()`: Analyze scope and impact

### Database Client

**SupabaseClient** (`db/supabase_client.py`)

Methods:
- `insert_law()`: Insert a law into database
- `update_law()`: Update existing law
- `get_law_by_number()`: Retrieve specific law
- `get_laws_by_year()`: Get all laws from a year
- `get_laws_by_subject()`: Filter by subject area
- `search_laws()`: Full-text search
- `insert_article()`: Store individual articles
- `insert_amendment()`: Record amendments
- Scraper run logging methods

## Database Schema

### laws table

```sql
CREATE TABLE laws (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  law_number VARCHAR(100) UNIQUE NOT NULL,
  law_type VARCHAR(50),
  year INTEGER,
  title TEXT NOT NULL,
  summary TEXT,
  full_text TEXT,
  publication_date DATE,
  source_url TEXT,
  source_name VARCHAR(100),
  pdf_url TEXT,
  issuing_entity VARCHAR(200),
  subject_area VARCHAR(200),
  status VARCHAR(50),
  scraped_at TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### articles table

```sql
CREATE TABLE articles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  law_id UUID REFERENCES laws(id),
  article_number VARCHAR(20),
  content TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### amendments table

```sql
CREATE TABLE amendments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  amending_law_id UUID REFERENCES laws(id),
  related_law_number VARCHAR(100),
  amendment_type VARCHAR(50),
  articles_affected TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### scraper_runs table

```sql
CREATE TABLE scraper_runs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source VARCHAR(100),
  scrape_type VARCHAR(50),
  status VARCHAR(50),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  laws_found INTEGER,
  laws_processed INTEGER,
  error_message TEXT
);
```

## Configuration

Edit `config.py` to customize:

- `SCRAPER_DELAY`: Seconds between requests (default: 2)
- `MAX_RETRIES`: Number of retry attempts (default: 3)
- `TIMEOUT`: Request timeout in seconds (default: 30)
- `SUBJECT_AREAS`: Keywords for classification

## Subject Areas

Laws are classified into these categories:

- **laboral**: Labor and employment law
- **tributario**: Tax law
- **civil**: Civil law
- **penal**: Criminal law
- **comercial**: Commercial law
- **administrativo**: Administrative law
- **inmigración**: Immigration law
- **ambiental**: Environmental law
- **educación**: Education law
- **salud**: Health law

## Logging

Logs are saved to `logs/` directory with timestamps:
- `logs/scraper_YYYYMMDD_HHMMSS.log`

Log levels:
- INFO: Normal operations
- WARNING: Recoverable issues
- ERROR: Errors that don't stop execution
- CRITICAL: Fatal errors

## Output Files

Test mode saves to `data/sample_output/`:
- `test_raw_laws_YYYY.json`: Raw scraped data
- `test_processed_law_YYYY.json`: AI-processed data

Full scrape saves:
- `full_scrape_YYYY_YYYY_raw.json`: All scraped laws
- `checkpoint_YYYY_YYYY_processed.json`: Incremental checkpoints

## Error Handling

The system includes robust error handling:
- Automatic retries with exponential backoff
- Rate limiting to respect server resources
- Graceful degradation (continues on individual failures)
- Comprehensive logging of all errors

## Performance

**Test Mode (3 laws, no AI):**
- Time: ~30 seconds
- Cost: $0

**Full Scrape (100 laws with AI):**
- Time: ~45 minutes
- Cost: ~$3-5 (Anthropic API)

**Tips for Reducing Costs:**
- Use `--no-db` for testing
- Run test mode first to verify
- Use incremental updates instead of full scrapes
- Process only recent years

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
- Add your API key to `.env` file
- Or use `--no-db` flag to skip AI processing

### "Supabase credentials not set"
- Add Supabase URL and key to `.env`
- Or use `--no-db` flag to save to JSON only

### "No laws found"
- Check internet connection
- Verify the year has published laws
- Check logs for specific errors

### "OCR not available"
- Install Tesseract: `sudo apt-get install tesseract-ocr`
- Or skip scanned PDFs

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding a New Scraper

1. Create file in `scrapers/` (e.g., `scrapers/new_source_scraper.py`)
2. Inherit from `BaseScraper`
3. Implement `scrape_laws()` and `scrape_single_law()` methods
4. Add to `main.py` imports and options

Example:

```python
from scrapers.base_scraper import BaseScraper

class NewSourceScraper(BaseScraper):
    def __init__(self):
        super().__init__("new_source")

    def scrape_laws(self, start_date=None, end_date=None):
        # Implementation
        pass

    def scrape_single_law(self, url):
        # Implementation
        pass
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Secretaría del Senado de Colombia for providing public access to legal documents
- Anthropic for Claude AI API
- Supabase for database infrastructure

## Contact

For questions or issues, please open an issue on GitHub or contact [your-email@example.com]

## Roadmap

- [ ] Add Función Pública scraper (decrees)
- [ ] Add DIAN scraper (tax regulations)
- [ ] Implement full-text search with embeddings
- [ ] Add web interface for querying laws
- [ ] Support for more document formats
- [ ] Multi-language support (English translations)
- [ ] API endpoints for third-party access
- [ ] Real-time monitoring dashboard

## Version History

**v1.0.0** (Current)
- Initial release
- Senado scraper implementation
- Claude AI integration
- Supabase database support
- Test and full scrape modes
