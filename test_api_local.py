#!/usr/bin/env python
"""
Test the FastAPI locally before deploying to Vercel
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n🔍 Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_root():
    print("\n🔍 Testing / endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_scrape():
    print("\n🔍 Testing /scrape endpoint...")
    print("⚠️  This will take a while (scraping live data)...")

    payload = {
        "year": 2023,
        "max_laws": 2
    }

    response = requests.post(
        f"{BASE_URL}/scrape",
        json=payload,
        timeout=60
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        laws = response.json()
        print(f"✅ Successfully scraped {len(laws)} laws")
        for law in laws:
            print(f"\n  Law: {law['law_number']}")
            print(f"  Title: {law['title'][:80]}...")
    else:
        print(f"❌ Error: {response.text}")

def test_search():
    print("\n🔍 Testing /search endpoint...")

    payload = {
        "query": "sistema",
        "limit": 5
    }

    response = requests.post(
        f"{BASE_URL}/search",
        json=payload,
        timeout=10
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        results = response.json()
        print(f"✅ Found {len(results)} matching laws")
        for law in results:
            print(f"\n  Law: {law['law_number']}")
            print(f"  Title: {law['title'][:80]}...")
    elif response.status_code == 503:
        print("⚠️  Database not configured")
    else:
        print(f"Response: {response.text}")

def main():
    print("=" * 70)
    print("🚀 TESTING COLOMBIAN LEGAL API LOCALLY")
    print("=" * 70)
    print("\nMake sure the API is running:")
    print("  uvicorn api.app:app --reload")
    print("\nOr run: python api/app.py")
    print("=" * 70)

    input("\nPress Enter to start tests...")

    try:
        # Basic tests
        test_root()
        test_health()

        # Database-dependent tests
        print("\n" + "=" * 70)
        print("DATABASE TESTS (requires Supabase)")
        print("=" * 70)
        test_search()

        # Scraping test (slow)
        print("\n" + "=" * 70)
        print("SCRAPING TEST (SLOW - ~30-60 seconds)")
        print("=" * 70)
        choice = input("Do you want to test scraping? (y/n): ")

        if choice.lower() == 'y':
            test_scrape()
        else:
            print("⏭️  Skipping scraping test")

        print("\n" + "=" * 70)
        print("✅ LOCAL API TESTS COMPLETE!")
        print("=" * 70)
        print("\nYou can now deploy to Vercel:")
        print("  1. Install: npm install -g vercel")
        print("  2. Deploy: vercel")
        print("\nOr visit the docs: http://localhost:8000/docs")

    except requests.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("\nMake sure the API is running:")
        print("  python api/app.py")
        print("Or:")
        print("  uvicorn api.app:app --reload")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
