# Troubleshooting Guide

## Common Issues and Solutions

### 1. 403 Forbidden Errors When Scraping

**Problem**: Getting `403 Client Error: Forbidden` when trying to scrape websites.

**Cause**: Websites have anti-bot measures that detect and block automated scraping.

**Solutions**:

**A. Use a Proxy or VPN**
```python
# In scrapers/base_scraper.py, modify __init__:
proxies = {
    'http': 'http://your-proxy:port',
    'https': 'http://your-proxy:port',
}
self.session.proxies.update(proxies)
```

**B. Add More Realistic Headers**
```python
# In scrapers/base_scraper.py:
self.session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-CO,es;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
})
```

**C. Increase Delay Between Requests**
```python
# In config.py:
SCRAPER_DELAY = 5  # Increase to 5+ seconds
```

**D. Use Selenium with a Real Browser**
```bash
pip install selenium webdriver-manager
```

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
html = driver.page_source
```

**E. Try Different Years**

2024 laws might not be accessible yet. Try older years:
```bash
python main.py test --start-year 2020 --max-laws 3 --no-db
```

**F. Use Alternative Data Sources**

Consider using official APIs or data exports if available:
- SUIN-Juriscol: Sistema Único de Información Normativa
- Contact government offices for bulk data access

---

### 2. ANTHROPIC_API_KEY Not Set

**Problem**: `ValueError: ANTHROPIC_API_KEY not set in environment`

**Solution**:

1. Get API key from https://console.anthropic.com/
2. Add to `.env` file:
```env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

3. Or set as environment variable:
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key'
```

4. Run without AI processing:
```bash
python main.py test --no-db  # Skips AI processing
```

---

### 3. Supabase Connection Failed

**Problem**: `Database connection failed` or `Supabase credentials not set`

**Solution**:

1. Get credentials from https://supabase.com/dashboard
2. Add to `.env`:
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key
```

3. Create required tables:
```sql
-- Run in Supabase SQL Editor
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

CREATE TABLE articles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  law_id UUID REFERENCES laws(id),
  article_number VARCHAR(20),
  content TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE amendments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  amending_law_id UUID REFERENCES laws(id),
  related_law_number VARCHAR(100),
  amendment_type VARCHAR(50),
  articles_affected TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

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

4. Run without database:
```bash
python main.py test --no-db  # Saves to JSON only
```

---

### 4. PDF Extraction Fails

**Problem**: `No text could be extracted from PDF` or OCR not working

**Solutions**:

**For Digital PDFs**:
- Ensure PDF is not corrupted
- Try alternative PDF libraries:
```bash
pip install pdfminer.six
```

**For Scanned PDFs**:

Install Tesseract OCR:

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa
```

**Mac**:
```bash
brew install tesseract tesseract-lang
```

**Windows**:
Download from: https://github.com/UB-Mannheim/tesseract/wiki

Then install Python packages:
```bash
pip install pdf2image pytesseract
```

---

### 5. Module Import Errors

**Problem**: `ModuleNotFoundError` or `ImportError`

**Solutions**:

1. Ensure you're in the correct directory:
```bash
cd /path/to/colombian-legal-db
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Use virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Add project to PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

### 6. Rate Limiting / Too Many Requests

**Problem**: Getting rate-limited by websites

**Solutions**:

1. Increase delays in `config.py`:
```python
SCRAPER_DELAY = 5  # Seconds between requests
```

2. Add random delays:
```python
import random
time.sleep(random.uniform(2, 5))
```

3. Implement exponential backoff (already in code):
```python
time.sleep(5 * (attempt + 1))  # Increases with each retry
```

4. Reduce concurrent requests:
- Run smaller batches
- Use `--max-laws` parameter

---

### 7. Memory Issues with Large Datasets

**Problem**: Out of memory errors when processing many laws

**Solutions**:

1. Process in smaller batches:
```bash
python main.py full --start-year 2020 --end-year 2020  # One year at a time
```

2. Enable checkpoints (already implemented):
- Checkpoints saved every 10 laws
- Resume from checkpoint if crash

3. Clear text after processing:
```python
# In main.py, after database insert:
law_data['full_text'] = None  # Free memory
```

4. Use generator instead of list:
```python
# Instead of loading all laws at once
for law in scraper.scrape_laws_generator():
    process(law)
```

---

### 8. Unicode / Encoding Errors

**Problem**: `UnicodeDecodeError` or garbled text

**Solutions**:

1. Ensure UTF-8 encoding:
```python
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()
```

2. Handle encoding errors:
```python
with open(file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()
```

3. Normalize Spanish characters:
```python
import unicodedata
text = unicodedata.normalize('NFKD', text)
```

---

### 9. Tests Failing

**Problem**: Unit tests fail

**Solutions**:

1. Skip tests requiring API keys:
```bash
# Tests automatically skip if no ANTHROPIC_API_KEY
python -m pytest tests/ -v
```

2. Run specific test:
```bash
python -m pytest tests/test_scrapers.py::TestHelpers -v
```

3. Update test data:
- Tests use mock data that might need updating

---

### 10. Logs Directory Permission Denied

**Problem**: Cannot write to logs directory

**Solutions**:

1. Create logs directory with proper permissions:
```bash
mkdir -p logs
chmod 755 logs
```

2. Change log location in `config.py`:
```python
LOGS_DIR = '/tmp/scraper_logs'  # Use temp directory
```

3. Run with elevated permissions (not recommended):
```bash
sudo python main.py test
```

---

## Performance Tips

### Optimize Scraping Speed

1. **Reduce delays for known-good servers**:
```python
SCRAPER_DELAY = 1  # If server allows
```

2. **Use concurrent requests** (advanced):
```python
import asyncio
import aiohttp
# Implement async scraping
```

3. **Cache responses**:
```python
import requests_cache
requests_cache.install_cache('scraper_cache')
```

### Optimize AI Processing

1. **Batch similar operations**:
```python
# Summarize multiple laws in one prompt
summaries = ai.batch_summarize([law1, law2, law3])
```

2. **Use shorter prompts**:
- Reduces token usage and cost
- Faster responses

3. **Cache AI responses**:
```python
# Don't reprocess if already summarized
if not law_data.get('summary'):
    law_data['summary'] = ai.summarize_law(text)
```

---

## Getting Help

If you encounter issues not covered here:

1. Check logs in `logs/` directory
2. Enable debug logging:
```python
# In main.py:
logging.basicConfig(level=logging.DEBUG)
```

3. Create a GitHub issue with:
   - Error message and traceback
   - Log file excerpts
   - Steps to reproduce
   - Python version and OS

4. Contact: [your-email@example.com]

---

## Known Limitations

1. **Website Structure Changes**: Scrapers may break if government websites are redesigned
2. **Access Restrictions**: Some documents may require authentication
3. **PDF-Only Content**: Some laws are only available as scanned PDFs (harder to extract)
4. **Incomplete Data**: Not all fields may be available for all laws
5. **Rate Limits**: Government servers may limit request frequency
6. **API Costs**: Claude AI processing incurs usage costs

---

## Best Practices

1. **Always test first**: Use `--no-db` flag for testing
2. **Start small**: Test with small year ranges
3. **Monitor costs**: Check Anthropic usage dashboard
4. **Respect servers**: Don't overwhelm government websites
5. **Keep logs**: Useful for debugging and auditing
6. **Backup data**: Regularly export database
7. **Version control**: Commit changes frequently
8. **Document changes**: Update README when modifying scrapers
