import asyncio
import typer
from loguru import logger
from src.models.schemas import Source, PlatformType
from src.core.fetcher import FetcherFactory

app = typer.Typer()

# Signal Hunter version
VERSION = "0.2.0-worktree"

from src.core.engine import Engine

@app.command()
def run():
    """
    Run the main Signal Hunter engine cycle.
    """
    logger.info(f"🚀 Signal Hunter v{VERSION} starting...")
    engine = Engine()
    engine.load_sources_from_memory()
    asyncio.run(engine.run_cycle())

@app.command()
def test_bird(handle: str = "vista8"):
    """
    Test the Twitter Adapter by fetching recent tweets from a handle.
    """
    logger.info(f"🧪 Testing Bird Adapter for @{handle}")
    
    # Construct a dummy source
    source = Source(
        name="TestUser",
        url=f"https://x.com/{handle}",
        platform=PlatformType.TWITTER
    )
    
    adapter = FetcherFactory.get_adapter(source)
    
    # Run async fetch in sync CLI
    results = asyncio.run(adapter.fetch())
    
    logger.success(f"✅ Fetched {len(results)} tweets")
    for tweet in results:
        # Bird's JSON structure varies, adjust accessors as needed
        text = tweet.get('full_text') or tweet.get('text') or "No text"
        print(f"--------------------------------------------------")
        print(f"📄 {text[:100]}...")
        print(f"🔗 {tweet.get('url', 'N/A')}")

if __name__ == "__main__":
    app()
