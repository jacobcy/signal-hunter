import httpx
from bs4 import BeautifulSoup
from loguru import logger
from typing import List
from src.models.schemas import Source
from src.core.fetcher import BaseAdapter

class GenericAdapter(BaseAdapter):
    """
    Generic Web Scraper using HTTPX + BeautifulSoup.
    Target: Standard HTML pages (blogs, news sites).
    """
    async def fetch(self) -> List[dict]:
        logger.info(f"🌐 Fetching generic web: {self.source.url}")
        
        # 搜狗微信特殊处理
        if "weixin.sogou.com" in str(self.source.url):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0",
                "Referer": "https://weixin.sogou.com/",
                "Cookie": "SUV=; SNUID=;"  # 基础Cookie，实际需要更多
            }
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(str(self.source.url), headers=headers)
                resp.raise_for_status()
                
                # Zero-Token Parsing: BeautifulSoup
                soup = BeautifulSoup(resp.text, "lxml")
                
                # Heuristic: Extract all paragraph text. 
                # In the future, we can use specific selectors from Source config.
                # If specific selectors are provided in source, use them.
                if self.source.selector_content:
                    elements = soup.select(self.source.selector_content)
                    texts = [e.get_text(strip=True) for e in elements]
                else:
                    # Fallback: Get all <p> text that is long enough
                    texts = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 20]
                
                combined_text = "\n".join(texts)
                
                if not combined_text:
                    logger.warning(f"⚠️ No content extracted from {self.source.url}")
                    return []
                
                # Wrap in a dict structure similar to Bird's output for consistency
                return [{
                    "full_text": combined_text,
                    "url": str(self.source.url),
                    "created_at": None # Generic web usually hard to parse date without specific selectors
                }]

        except httpx.HTTPError as e:
            logger.error(f"❌ HTTP Error for {self.source.url}: {e}")
            # TODO: Trigger Playwright Fallback here
            return []
        except Exception as e:
            logger.exception(f"❌ Unexpected error fetching {self.source.url}: {e}")
            return []
