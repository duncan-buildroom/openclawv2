#!/usr/bin/env python3
"""
Skool Posts Daily Cron
Picks communities, posts directly via browser, logs to Notion after.
TEST_MODE: restricts to Build Room only for testing.
"""

import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from rotation_state import pick_communities, reset_if_new_day

# Load config
CONFIG = json.loads((Path(__file__).parent / "config.json").read_text())
TEST_MODE = CONFIG.get("test_mode", False)

# Post time slots (minutes after start)
TIME_SLOTS = [
    0,      # Immediate
    150,    # 2.5 hours
    300,    # 5 hours
    450,    # 7.5 hours
    600     # 10 hours
]

def post_to_skool_browser(community_slug, title, body, category="Hangout"):
    """
    Post directly to Skool via browser automation.
    Returns post URL on success, None on failure.
    """
    sys.path.insert(0, str(Path(__file__).parent))
    from skool_post_automation import post_to_skool, format_post_body
    
    # Format body (sentence per paragraph)
    body_formatted = format_post_body(body)
    
    # Post
    result = post_to_skool(community_slug, title, body_formatted, category)
    
    if result["success"]:
        return result["url"]
    else:
        print(f"  ❌ {result['error']}")
        return None

def log_to_notion(community, post_text, post_url, posted_time):
    """Log posted content to Notion for Duncan's review."""
    import os
    import requests
    
    notion_token = os.environ.get("NOTION_TOKEN")
    db_id = "30cf259c-0f17-81a9-ae1f-de9720b5cb64"
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # Create page in Skool Posts DB
    page_data = {
        "parent": {"database_id": db_id},
        "properties": {
            "Community": {
                "select": {"name": community}
            },
            "Type": {
                "select": {"name": "Post"}
            },
            "Status": {
                "select": {"name": "Posted ✅"}
            },
            "Posted": {
                "date": {"start": posted_time}
            },
            "URL": {
                "url": post_url if post_url else None
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": post_text}}]
                }
            }
        ]
    }
    
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=page_data,
        timeout=30
    )
    
    if response.status_code == 200:
        page = response.json()
        print(f"  ✅ Pushed to Notion: {page['url']}")
        return page["id"]
    else:
        print(f"  ❌ Notion push failed: {response.status_code}")
        print(response.text[:200])
        return None

def main():
    print(f"\n{'='*60}")
    mode = "TEST MODE (Build Room only)" if TEST_MODE else "PRODUCTION"
    print(f"Skool Posts Daily Run — {mode}")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    # Reset state if new day
    if reset_if_new_day():
        print("🔄 New day detected, rotation state reset\n")
    
    # Pick communities
    if TEST_MODE:
        communities = CONFIG["test_communities"]
        post_limit = CONFIG["test_limits"]["posts_per_day"]
        communities = communities[:post_limit]
        print(f"🧪 TEST MODE: {len(communities)} posts to Build Room\n")
    else:
        communities = pick_communities(5, "posts")
    
    print(f"📋 Communities selected for today:")
    for i, comm in enumerate(communities, 1):
        slot_time = TIME_SLOTS[i-1]
        hours = slot_time // 60
        mins = slot_time % 60
        time_str = f"9:{mins:02d}am" if hours == 0 else f"{9 + hours}:{mins:02d}{'am' if hours < 3 else 'pm'}"
        print(f"  {i}. /{comm} at {time_str}")
    
    print()
    
    # Process each post at its scheduled time
    start_time = time.time()
    
    for i, community in enumerate(communities):
        slot_minutes = TIME_SLOTS[i]
        target_time = start_time + (slot_minutes * 60)
        now = time.time()
        
        # Wait until target time
        if now < target_time:
            wait_seconds = target_time - now
            wait_minutes = wait_seconds / 60
            print(f"⏳ Waiting {wait_minutes:.1f} minutes until next post...")
            time.sleep(wait_seconds)
        
        # Generate post via agent (for now, use placeholder)
        print(f"\n📝 Generating post for /{community}...")
        
        # TODO: Integrate with skoolposts agent properly
        # For now, generate contextual posts based on community
        if community == "buildroom":
            title = "Quick question"
            body = "What's one automation you built this week that actually saved you time? Drop it below."
            category = "Hangout"
        else:
            title = f"Sharing from The Build Room"
            body = f"Quick insight I wanted to share with this community. What's your experience been?"
            category = None  # Let it default
        
        print(f"  Title: {title}")
        print(f"  Body: {body[:50]}...")
        
        # Post to Skool via browser
        print(f"  📤 Posting to Skool...")
        post_url = post_to_skool_browser(community, title, body, category)
        
        if post_url:
            # Log to Notion
            posted_time = datetime.now().isoformat()
            log_to_notion(community, post_text, post_url, posted_time)
        else:
            print(f"  ⚠️  Posting failed, not logging to Notion")
    
    print(f"\n{'='*60}")
    print("✅ Daily post run complete")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
