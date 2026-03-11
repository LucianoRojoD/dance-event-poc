import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.milongas_in import scrape_milongas_in
from scrapers.tangocat import scrape_tangocat
from scrapers.tangomango import scrape_tangomango
from pipeline.database import init_db, save_events

async def run_pipeline():
    print("Starting Dance Event Discovery Pipeline...")
    
    # Initialize DB
    init_db()
    
    # 1. Scrape Milongas-In (Sync)
    print("Scraping Milongas-In...")
    milongas_in_events = scrape_milongas_in()
    print(f"Found {len(milongas_in_events)} events from Milongas-In")
    save_events(milongas_in_events)
    
    # 2. Scrape TangoCat (Async)
    print("Scraping TangoCat...")
    tangocat_events = await scrape_tangocat()
    print(f"Found {len(tangocat_events)} events from TangoCat")
    save_events(tangocat_events)
    
    # 3. Scrape TangoMango (Async)
    print("Scraping TangoMango...")
    tangomango_events = await scrape_tangomango()
    print(f"Found {len(tangomango_events)} events from TangoMango")
    save_events(tangomango_events)
    
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
