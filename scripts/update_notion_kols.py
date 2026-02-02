import os
import requests
import json

# Configuration
PAGE_ID = "2f973a85-7f76-819b-9874-cc6420136d81" # X/Twitter监控看板
try:
    with open(os.path.expanduser('~/.config/notion/api_key'), 'r') as f:
        API_KEY = f.read().strip()
except:
    print('❌ API Key not found')
    exit(1)

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# KOL Data
kol_categories = [
    {
        "name": "🧠 技术领袖 (Technical Leaders)",
        "kols": [
            {"name": "Sam Altman", "handle": "@sama", "desc": "OpenAI CEO，风向标"},
            {"name": "Andrej Karpathy", "handle": "@karpathy", "desc": "前OpenAI/Tesla，AI教育家"},
            {"name": "Yann LeCun", "handle": "@ylecun", "desc": "Meta首席科学家，开源模型支持者"},
            {"name": "Demis Hassabis", "handle": "@demishassabis", "desc": "Google DeepMind CEO"},
            {"name": "Jim Fan", "handle": "@DrJimFan", "desc": "NVIDIA高级科学家，Agent专家"}
        ]
    },
    {
        "name": "⚡ 行业洞察 (Industry Insiders)",
        "kols": [
            {"name": "Ethan Mollick", "handle": "@emollick", "desc": "沃顿商学院教授，AI应用研究"},
            {"name": "Bindu Reddy", "handle": "@bindureddy", "desc": "Abacus.AI CEO，模型评测"},
            {"name": "Rowan Cheung", "handle": "@rowancheung", "desc": "The Rundown AI创始人，新闻聚合"},
            {"name": "Suhail Doshi", "handle": "@Suhail", "desc": "Playground AI创始人，产品设计"},
            {"name": "Greg Brockman", "handle": "@gdb", "desc": "OpenAI联合创始人"}
        ]
    },
    {
        "name": "🛠️ 独立开发与实战 (Indie & Engineering)",
        "kols": [
            {"name": "Pietro Schirano", "handle": "@skirano", "desc": "AI设计与产品实战"},
            {"name": "Simon Willison", "handle": "@simonw", "desc": "LLM工具开发，Datasette作者"},
            {"name": "Shawn 'swyx' Wang", "handle": "@swyx", "desc": "AI工程师，Latent Space主理人"},
            {"name": "Mckay Wrigley", "handle": "@mckaywrigley", "desc": "AI编程实战，Cursor高级玩家"},
            {"name": "宝玉", "handle": "@dotey", "desc": "中文AI圈，翻译与深度解读"}
        ]
    }
]

def create_blocks(categories):
    blocks = []
    
    # Intro
    blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": "本看板由 Web Researcher 维护，旨在追踪全球 AI 核心动态。数据最后更新：2026-02-01"}}]
        }
    })

    for cat in categories:
        # Category Header
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": cat["name"]}}]
            }
        })
        
        # KOL List (Bullet points for now, simpler than database for Phase 1)
        for kol in cat["kols"]:
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": kol["name"], "link": None}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " ("}},
                        {"type": "text", "text": {"content": kol["handle"], "link": {"url": f"https://twitter.com/{kol['handle'][1:]}"}}},
                        {"type": "text", "text": {"content": f"): {kol['desc']}"}}
                    ]
                }
            })
            
    return blocks

def append_to_page(page_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    # Notion API limits block appends per request (usually 100 is safe, we have ~20)
    data = {"children": blocks}
    
    response = requests.patch(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print("✅ Successfully wrote KOL list to Notion page!")
    else:
        print(f"❌ Failed to write to Notion: {response.text}")

if __name__ == "__main__":
    print(f"📝 Generating content for page {PAGE_ID}...")
    blocks = create_blocks(kol_categories)
    append_to_page(PAGE_ID, blocks)
