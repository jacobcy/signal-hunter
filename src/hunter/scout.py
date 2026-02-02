import yaml
import logging
import json
import subprocess
import shlex
import requests
from typing import List, Dict, Any, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("HunterScout")

class HunterConfig:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.topics = []
        self._load_config()

    def _load_config(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            data = yaml.safe_load(f)
            self.topics = data.get('topics', [])
            logger.info(f"Loaded {len(self.topics)} topics from config.")

class Scout:
    def __init__(self, config: HunterConfig, use_cli_tools: bool = True):
        self.config = config
        self.use_cli_tools = use_cli_tools

    def hunt(self) -> Dict[str, List[Dict[str, Any]]]:
        """Main execution loop for all topics."""
        logger.info("Starting hunt...")
        results = {}
        
        for topic in self.config.topics:
            topic_name = topic.get('name')
            logger.info(f"Scouting topic: {topic_name}")
            topic_results = []
            
            for source in topic.get('sources', []):
                source_type = source.get('type')
                query = source.get('query')
                
                try:
                    if source_type == 'web':
                        data = self._search_web(query)
                        topic_results.extend(data)
                    elif source_type == 'twitter':
                        data = self._search_twitter(query)
                        topic_results.extend(data)
                    elif source_type == 'twitter-user':
                        data = self._search_twitter_user(query)
                        topic_results.extend(data)
                    else:
                        logger.warning(f"Unknown source type: {source_type}")
                except Exception as e:
                    logger.error(f"Error scouting {source_type} for '{topic_name}': {e}")
            
            filtered_results = self._filter_results(topic_results, topic.get('keywords', []))
            results[topic_name] = filtered_results
            
        return results

    def _search_web(self, query: str) -> List[Dict[str, Any]]:
        """
        Executes a web search using the Tavily API.
        """
        logger.info(f"  [Web Search] Query: {query}")
        
        if self.use_cli_tools:
            try:
                api_key = "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"
                endpoint = "https://api.tavily.com/search"
                payload = {
                    "api_key": api_key,
                    "query": query,
                    "search_depth": "basic"
                }
                
                response = requests.post(endpoint, json=payload, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                # Transform Tavily format to internal format if needed
                results = []
                for res in data.get('results', []):
                    results.append({
                        "title": res.get("title"),
                        "url": res.get("url"),
                        "snippet": res.get("content")
                    })
                return results

            except Exception as e:
                logger.warning(f"Tavily web search failed: {e}")
                pass

        return []

    def _search_twitter(self, query: str) -> List[Dict[str, Any]]:
        """
        Executes a Twitter search (Bird tool).
        """
        logger.info(f"  [Twitter Search] Query: {query}")
        
        if self.use_cli_tools:
            try:
                # bird search "{query}" --json
                cmd = ["bird", "search", query, "--json"]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                try:
                    data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    logger.warning(f"Could not parse bird output as JSON: {result.stdout[:100]}...")
                    return []

                formatted_results = []
                items = data if isinstance(data, list) else data.get('tweets', [])
                
                for item in items[:5]:
                    formatted_results.append({
                        "text": item.get("text") or item.get("content", ""),
                        "author": item.get("author_username") or item.get("username", "unknown"),
                        "link": item.get("url") or item.get("permalink", "")
                    })
                return formatted_results

            except subprocess.CalledProcessError as e:
                logger.warning(f"Bird CLI failed (exit code {e.returncode}): {e.stderr}")
            except Exception as e:
                logger.warning(f"Twitter search failed: {e}")

        return []

    def _search_twitter_user(self, username: str) -> List[Dict[str, Any]]:
        """
        Executes a Twitter user timeline fetch (Bird tool).
        """
        # Remove @ if present
        username = username.lstrip('@')
        logger.info(f"  [Twitter User] Username: {username}")
        
        if self.use_cli_tools:
            try:
                # Use bird user-tweets <username> --json
                cmd = ["bird", "user-tweets", username, "--json"]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                try:
                    data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    logger.warning(f"Could not parse bird output as JSON: {result.stdout[:100]}...")
                    return []

                formatted_results = []
                items = data if isinstance(data, list) else data.get('tweets', [])
                
                # Limit to recent 5 tweets
                for item in items[:5]:
                    formatted_results.append({
                        "text": item.get("text") or item.get("content", ""),
                        "author": item.get("author_username") or item.get("username", username),
                        "link": item.get("url") or item.get("permalink", "")
                    })
                return formatted_results

            except subprocess.CalledProcessError as e:
                logger.warning(f"Bird CLI failed (exit code {e.returncode}): {e.stderr}")
            except Exception as e:
                logger.warning(f"Twitter user fetch failed: {e}")

        return []

    def _filter_results(self, results: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
        """
        Simple keyword filtering logic.
        """
        if not keywords:
            return results
            
        filtered = []
        for item in results:
            # Combine all text fields for searching
            text_content = " ".join([str(v) for v in item.values() if isinstance(v, str)]).lower()
            
            # Check if any keyword matches
            if any(k.lower() in text_content for k in keywords):
                filtered.append(item)
        
        logger.info(f"  Filtered {len(results)} items down to {len(filtered)} relevant items.")
        return filtered

if __name__ == "__main__":
    # Test run
    try:
        # Default to a relative config path for standalone testing
        cfg = HunterConfig("config/hunter.yaml")
        scout = Scout(cfg)
        findings = scout.hunt()
        print(json.dumps(findings, indent=2))
    except Exception as e:
        logger.error(f"Scout failed: {e}")
