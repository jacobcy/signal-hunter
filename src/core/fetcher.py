import json
import asyncio
import os
import subprocess
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from loguru import logger
from src.models.schemas import Source, Signal

class BaseAdapter(ABC):
    def __init__(self, source: Source):
        self.source = source

    @abstractmethod
    async def fetch(self) -> List[dict]:
        """Fetch raw data (posts/articles) from source"""
        pass

class TwitterAdapter(BaseAdapter):
    """
    Adapter for Twitter/X using the 'bird' CLI tool.
    Prerequisite: 'bird' must be installed and authenticated.
    """
    async def fetch(self) -> List[dict]:
        username = str(self.source.url).split('/')[-1]
        logger.info(f"🐦 Fetching tweets for @{username}...")
        
        # Construct bird command: bird user-tweets @username -n 5 --json --plain
        cmd = [
            "/opt/homebrew/bin/bird", 
            "user-tweets", 
            f"@{username}", 
            "-n", "5", 
            "--json", 
            "--plain"
        ]
        
        # Prepare environment variables specifically for bird
        env = os.environ.copy()
        if os.getenv("BIRD_AUTH_TOKEN"):
            env["AUTH_TOKEN"] = os.getenv("BIRD_AUTH_TOKEN")
        if os.getenv("BIRD_CT0"):
            env["CT0"] = os.getenv("BIRD_CT0")
            
        try:
            # Run bird in a subprocess (blocking call wrapped in async)
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"Bird CLI failed: {stderr.decode()}")
                return []
                
            output = stdout.decode()
            if not output.strip():
                return []

            # Bird outputs JSON lines or a JSON array depending on version/flags.
            # We assume --json returns a valid JSON structure or line-delimited JSON.
            try:
                data = json.loads(output)
                # Ensure it's a list
                if isinstance(data, dict):
                    data = [data]
                return data
            except json.JSONDecodeError:
                # Handle line-delimited JSON if necessary
                logger.warning("JSON decode failed, attempting line-parsing fallback (not impl yet)")
                return []
                
        except Exception as e:
            logger.exception(f"Error running bird adapter: {e}")
            return []

from src.core.adapter_web import GenericAdapter

class FetcherFactory:
    @staticmethod
    def get_adapter(source: Source) -> BaseAdapter:
        url_str = str(source.url).lower()
        if "x.com" in url_str or "twitter.com" in url_str:
            return TwitterAdapter(source)
        else:
            return GenericAdapter(source)
