import os
#!/usr/bin/env python3
import requests
import json

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
LINKEDIN_POSTS_DB_ID = "d4266f2c-ed0a-4c5b-8b81-7cb4e2ffad86"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

resp = requests.get(
    f"https://api.notion.com/v1/databases/{LINKEDIN_POSTS_DB_ID}",
    headers=headers,
    timeout=30
)

if resp.status_code == 200:
    data = resp.json()
    print("✅ Database properties:")
    print(json.dumps(data.get('properties', {}), indent=2))
else:
    print(f"❌ Error {resp.status_code}: {resp.text}")
