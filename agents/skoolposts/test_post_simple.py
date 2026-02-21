#!/usr/bin/env python3
"""
Simple test: Post to Build Room using browser automation.
"""

import json
import time
from pathlib import Path

CONFIG = json.loads((Path(__file__).parent / "config.json").read_text())

# Test post
post_text = """What's one automation you built this week that actually saved you time?

I'm curious what's working for people right now.

Drop it below."""

print("🧪 Testing Skool Post to Build Room\n")
print(f"Post text ({len(post_text)} chars):")
print("─" * 60)
print(post_text)
print("─" * 60)
print()

response = input("Post this to Build Room? (y/n): ")
if response.lower() != 'y':
    print("Cancelled.")
    exit(0)

print("\n📤 Posting via browser automation...")
print("⚠️  Note: This test uses browser tool which may need manual interaction")
print()

# Log what we would do
print("Would perform:")
print("  1. browser(action='open', targetUrl='https://www.skool.com/buildroom')")
print("  2. Find 'Create Post' button")
print("  3. Type post text")
print("  4. Click 'Post'")
print()
print("⚠️  Browser automation needs to be called from within OpenClaw context")
print("⚠️  This script is a template - actual posting requires integration")
print()

# Log to Notion (this part works)
print("📝 Logging to Notion as test entry...")
from datetime import datetime
import os
import requests

notion_token = os.environ.get("NOTION_TOKEN")
db_id = CONFIG["notion"]["db_id"]

headers = {
    "Authorization": f"Bearer {notion_token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

page_data = {
    "parent": {"database_id": db_id},
    "properties": {
        "Community": {"select": {"name": "Build Room"}},
        "Type": {"select": {"name": "Post"}},
        "Status": {"select": {"name": "Draft (TEST)"}},
        "Posted": {"date": {"start": datetime.now().isoformat()}},
    },
    "children": [{
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": post_text}}]
        }
    }]
}

resp = requests.post(
    "https://api.notion.com/v1/pages",
    headers=headers,
    json=page_data,
    timeout=30
)

if resp.status_code == 200:
    notion_url = resp.json().get("url")
    print(f"✅ Test entry logged to Notion: {notion_url}")
else:
    print(f"❌ Notion logging failed: {resp.status_code}")
    print(resp.text[:200])

print("\n✅ Test complete")
print("\nNext: Implement actual browser automation via OpenClaw browser tool")
