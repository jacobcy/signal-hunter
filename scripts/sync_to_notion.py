import os
import requests
import sys
from dotenv import load_dotenv

load_dotenv()

NOTION_KEY = os.getenv("NOTION_API_KEY")
ROOT_PAGE_ID = os.getenv("NOTION_PAGE_ID")
HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def find_subpage(parent_id, title):
    """Find a child page by title."""
    url = f"https://api.notion.com/v1/blocks/{parent_id}/children"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        return None
    
    for block in resp.json().get('results', []):
        if block['type'] == 'child_page' and block['child_page']['title'] == title:
            return block['id']
    return None

def create_page(parent_id, title, markdown_content):
    """Create a new page."""
    url = "https://api.notion.com/v1/pages"
    
    blocks = [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": title}}]}
        }
    ]

    # Split content into chunks of 1800 chars
    chunk_size = 1800
    for i in range(0, len(markdown_content), chunk_size):
        chunk = markdown_content[i:i+chunk_size]
        blocks.append({
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}],
                "language": "markdown"
            }
        })

    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"text": {"content": title}}]}
        },
        "children": blocks
    }
    
    resp = requests.post(url, json=payload, headers=HEADERS)
    if resp.status_code == 200:
        print(f"✅ Created: {title}")
        return resp.json()['id']
    else:
        print(f"❌ Failed to create {title}: {resp.text}")
        return None

def main():
    target_page_name = "团队资源 (Team Resources)"
    files_to_sync = ["TEAM.md", "WORKFLOW.md", "CAPABILITIES.md", "memory/api_assets.md"]

    # 1. Find Target Page
    target_id = find_subpage(ROOT_PAGE_ID, target_page_name)
    if not target_id:
        print(f"⚠️ Could not find '{target_page_name}', creating it under root...")
        target_id = create_page(ROOT_PAGE_ID, target_page_name, "Sync Root")
    
    print(f"📍 Target Page ID: {target_id}")

    # 2. Sync Files
    for filepath in files_to_sync:
        if not os.path.exists(filepath):
            print(f"⚠️ Skipping missing file: {filepath}")
            continue
            
        with open(filepath, 'r') as f:
            content = f.read()
            
        filename = os.path.basename(filepath)
        # Check if exists (Simple: just create new one for now to avoid update logic complexity in this quick script)
        # Ideally we should update, but Notion API update block is tricky.
        # Let's just create a new page for this session.
        create_page(target_id, f"📄 {filename}", content)

if __name__ == "__main__":
    main()
