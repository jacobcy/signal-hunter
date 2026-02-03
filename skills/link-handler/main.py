#!/usr/bin/env python3
"""
Link Handler: A smart URL opener that uses the appropriate tool based on the URL.
"""
import sys
import re
from urllib.parse import urlparse

def handle_x_link(url: str) -> str:
    """Handle X/Twitter links using the bird skill."""
    # In a real implementation, this would call the `bird` CLI tool.
    # For now, we'll simulate it by returning a message.
    return f"[X/Twitter Link Handler] Would fetch content from: {url}\n(Implementation pending integration with 'bird' skill)"

def handle_web_link(url: str) -> str:
    """Handle regular web links using web_fetch."""
    # In a real implementation, this would call the `web_fetch` tool.
    return f"[Web Link Handler] Would fetch content from: {url}\n(Implementation pending integration with 'web_fetch' tool)"

def main():
    if len(sys.argv) != 2:
        print("Usage: link-handler <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    parsed_url = urlparse(url)
    
    # Check for X/Twitter domains
    if parsed_url.netloc in ['x.com', 'twitter.com']:
        result = handle_x_link(url)
    else:
        result = handle_web_link(url)
    
    print(result)

if __name__ == "__main__":
    main()