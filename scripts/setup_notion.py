import os
import json
import requests
from typing import List, Dict

# Configuration
NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
ROOT_PAGE_ID = os.environ.get("NOTION_PAGE_ID")

if not NOTION_API_KEY or not ROOT_PAGE_ID:
    print("❌ Error: NOTION_API_KEY or NOTION_PAGE_ID not found in environment.")
    # Fallback to reading from config files if env vars aren't set in this shell session
    try:
        with open(os.path.expanduser("~/.config/notion/api_key"), "r") as f:
            NOTION_API_KEY = f.read().strip()
        with open(os.path.expanduser("~/.config/notion/page_id"), "r") as f:
            ROOT_PAGE_ID = f.read().strip()
    except Exception as e:
        print(f"❌ Failed to load credentials from file: {e}")
        exit(1)

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28" 
}

# Structure to create
PAGES_TO_CREATE = [
    {"icon": "📊", "title": "情报中心 (Intelligence Hub)", "children": ["X/Twitter监控看板", "AI进展追踪", "OpenClaw使用技巧", "搞钱策略研究"]},
    {"icon": "🔬", "title": "可行性研究 (Feasibility Studies)", "children": ["交易策略研究", "SaaS机会分析", "内容变现路径", "技术趋势评估"]},
    {"icon": "📋", "title": "项目文档 (Project Docs)", "children": ["Signal Hunter", "Project X (待立项)", "Project Y (待立项)"]},
    {"icon": "🛠️", "title": "团队资源 (Team Resources)", "children": ["技能清单", "API配置", "工具使用指南", "最佳实践"]},
    {"icon": "📈", "title": "复盘总结 (Retrospectives)", "children": ["周度复盘", "月度总结", "策略优化记录"]}
]

def get_block_children(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Failed to list children: {response.text}")
        return []
    return response.json().get("results", [])

def create_page(parent_id, title, icon=None):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {
                "title": [{"text": {"content": title}}]
            }
        }
    }
    if icon:
        data["icon"] = {"type": "emoji", "emoji": icon}
    
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print(f"✅ Created page: {icon} {title}")
        return response.json()["id"]
    else:
        print(f"❌ Failed to create page '{title}': {response.text}")
        return None

def main():
    print(f"🔍 Checking root page: {ROOT_PAGE_ID}")
    
    # List existing pages to avoid duplicates
    existing_pages = {}
    children = get_block_children(ROOT_PAGE_ID)
    for block in children:
        if block["type"] == "child_page":
            title = block["child_page"]["title"]
            existing_pages[title] = block["id"]
            print(f"   Found existing page: {title}")

    print("\n🚀 Building AI Studio Structure...")
    
    for page_def in PAGES_TO_CREATE:
        full_title = page_def["title"] # Title includes text like "情报中心..."
        # Simplify title check? No, let's match exact title or just the text part if needed.
        # Assuming titles match exactly.
        
        page_id = existing_pages.get(full_title)
        
        if not page_id:
            page_id = create_page(ROOT_PAGE_ID, full_title, page_def["icon"])
        else:
            print(f"ℹ️  Page already exists: {full_title}")
            
        if page_id:
            # Create sub-pages
            # First check existing sub-pages
            sub_children = get_block_children(page_id)
            existing_subs = {b["child_page"]["title"]: b["id"] for b in sub_children if b["type"] == "child_page"}
            
            for sub_title in page_def["children"]:
                if sub_title not in existing_subs:
                    create_page(page_id, sub_title)
                else:
                    pass
                    # print(f"   - Sub-page exists: {sub_title}")

if __name__ == "__main__":
    main()
