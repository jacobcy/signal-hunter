import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_KEY = os.getenv("NOTION_API_KEY")
PAGE_ID = os.getenv("NOTION_PAGE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"  # Using a stable version
}

def check_page():
    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Connection Successful! Page ID: {PAGE_ID}")
        data = response.json()
        print(f"Found {len(data['results'])} blocks on the page.")
        for block in data['results']:
            btype = block['type']
            if btype == 'child_page':
                print(f"  - 📄 {block['child_page']['title']}")
            elif btype == 'child_database':
                print(f"  - 🗄️  {block['child_database']['title']}")
            elif btype == 'heading_1':
                print(f"  - H1: {block['heading_1']['rich_text'][0]['plain_text']}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    check_page()
