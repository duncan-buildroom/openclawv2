#!/usr/bin/env python3
"""
Test script: Post 1 message to Build Room to verify browser automation works.
"""

import json
import subprocess
from pathlib import Path

CONFIG = json.loads((Path(__file__).parent / "config.json").read_text())

print("🧪 Testing Skool Post to Build Room\n")

# Step 1: Generate test post
print("📝 Generating test post...")

# For now, use a hardcoded test post to verify browser automation
# TODO: Integrate with skoolposts agent properly
post_text = """What's one automation you built this week that actually saved you time?

I'm curious what's working for people right now.

Drop it below."""

print("✅ Using test post")

print(f"\n✅ Post generated ({len(post_text)} chars):")
print("─" * 60)
print(post_text)
print("─" * 60)
print()

# Step 2: Browser automation test
print("📤 Testing browser automation...")
print("⚠️  This will:")
print("  1. Open browser")
print("  2. Log in to Skool")
print("  3. Navigate to Build Room")
print("  4. Post the message")
print()

response = input("Continue? (y/n): ")
if response.lower() != 'y':
    print("Cancelled.")
    exit(0)

# Import browser helper
import sys
sys.path.insert(0, str(Path(__file__).parent))
from skool_browser import login_to_skool, post_to_community, close_all_tabs

# Login
print("\n🔐 Logging in...")
if not login_to_skool(CONFIG["credentials"]["email"], CONFIG["credentials"]["password"]):
    print("❌ Login failed")
    exit(1)

print("✅ Logged in")

# Post
print("\n📤 Posting to /buildroom...")
post_url = post_to_community("buildroom", post_text)

if post_url:
    print(f"✅ Posted successfully!")
    print(f"   URL: {post_url}")
    
    # Log to Notion
    print("\n📝 Logging to Notion...")
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
            "Status": {"select": {"name": "Posted ✅ (TEST)"}},
            "Posted": {"date": {"start": datetime.now().isoformat()}},
            "URL": {"url": post_url}
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
        print(f"✅ Logged to Notion: {notion_url}")
    else:
        print(f"⚠️  Notion logging failed: {resp.status_code}")
else:
    print("❌ Posting failed")

# Cleanup
print("\n🧹 Closing browser tabs...")
close_all_tabs()

print("\n✅ Test complete!")
