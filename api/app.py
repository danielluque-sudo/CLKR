"""
FastAPI application for Colombian Legal Scraper
Deploy-ready for Vercel
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add parent directory to path
# In Railway/production, __file__ is /app/api/app.py, parent is /app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
# Also add /app explicitly in case we're in Railway
if os.path.exists('/app'):
    sys.path.insert(0, '/app')

from scrapers.suin_scraper import SuinScraper
from processors.ai_processor import AIProcessor
from db.supabase_client import SupabaseClient
import config

# Initialize FastAPI
app = FastAPI(
    title="Colombian Legal Database API",
    description="API para consultar y scraper leyes colombianas",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ScrapeRequest(BaseModel):
    year: int
    max_laws: Optional[int] = 10

class LawResponse(BaseModel):
    law_number: str
    title: str
    year: Optional[int]
    publication_date: Optional[str]
    source_url: str
    summary: Optional[str]
    subject_area: Optional[str]

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10

# Initialize components
scraper = None
ai_processor = None
db_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global scraper, ai_processor, db_client

    # Only initialize if credentials are available
    if config.SUPABASE_URL and config.SUPABASE_KEY:
        db_client = SupabaseClient()

    if config.ANTHROPIC_API_KEY:
        ai_processor = AIProcessor()

@app.get("/")
def read_root():
    """API home endpoint"""
    return {
        "message": "Colombian Legal Database API",
        "status": "online",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "scrape": "/scrape",
            "search": "/search",
            "laws": "/laws"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if db_client else "not configured",
        "ai": "enabled" if ai_processor else "not configured"
    }

@app.post("/scrape", response_model=List[LawResponse])
async def scrape_laws(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """
    Scrape laws from SUIN for a specific year

    Example:
    ```json
    {
        "year": 2023,
        "max_laws": 5
    }
    ```
    """
    try:
        global scraper
        if not scraper:
            scraper = SuinScraper()

        # Scrape laws
        laws = scraper.scrape_year(request.year, max_attempts=request.max_laws)

        if not laws:
            raise HTTPException(status_code=404, detail=f"No laws found for year {request.year}")

        # Process with AI if available
        if ai_processor:
            for law in laws:
                try:
                    law['summary'] = ai_processor.summarize_law(law['full_text'])
                    law['subject_area'] = ai_processor.classify_subject(law['title'], law['full_text'])
                except:
                    pass

        # Store in database if available
        if db_client:
            for law in laws:
                background_tasks.add_task(db_client.insert_law, law)

        # Return response
        return [
            LawResponse(
                law_number=law['law_number'],
                title=law['title'],
                year=law.get('year'),
                publication_date=law.get('publication_date'),
                source_url=law['source_url'],
                summary=law.get('summary'),
                subject_area=law.get('subject_area')
            )
            for law in laws
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/laws", response_model=List[LawResponse])
async def get_laws(year: Optional[int] = None, limit: int = 10):
    """
    Get laws from database

    Query params:
    - year: Filter by year (optional)
    - limit: Maximum results (default: 10)
    """
    if not db_client:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        laws = db_client.get_laws(year=year, limit=limit)

        return [
            LawResponse(
                law_number=law['law_number'],
                title=law['title'],
                year=law.get('year'),
                publication_date=law.get('publication_date'),
                source_url=law['source_url'],
                summary=law.get('summary'),
                subject_area=law.get('subject_area')
            )
            for law in laws
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=List[LawResponse])
async def search_laws(request: SearchRequest):
    """
    Search laws by keyword

    Example:
    ```json
    {
        "query": "impuestos",
        "limit": 5
    }
    ```
    """
    if not db_client:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        laws = db_client.search_laws(request.query, limit=request.limit)

        if not laws:
            raise HTTPException(status_code=404, detail=f"No laws found matching: {request.query}")

        return [
            LawResponse(
                law_number=law['law_number'],
                title=law['title'],
                year=law.get('year'),
                publication_date=law.get('publication_date'),
                source_url=law['source_url'],
                summary=law.get('summary'),
                subject_area=law.get('subject_area')
            )
            for law in laws
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/laws/{law_number}")
async def get_law_by_number(law_number: str):
    """
    Get a specific law by its number

    Example: /laws/Ley%202294%20de%202023
    """
    if not db_client:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        law = db_client.get_law_by_number(law_number)

        if not law:
            raise HTTPException(status_code=404, detail=f"Law not found: {law_number}")

        return law

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get database statistics"""
    if not db_client:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        stats = db_client.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
