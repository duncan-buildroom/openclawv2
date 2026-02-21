#!/usr/bin/env python3
"""
Skool Comments Daily Cron
Picks communities, comments directly via browser, logs to Notion after.
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

# Comment batch time slots (minutes after start)
TIME_SLOTS = [
    0,      # Immediate
    150,    # 2.5 hours
    300,    # 5 hours
    450,    # 7.5 hours
    600     # 10 hours
]

def generate_comments_for_community(community_slug, target_count=6):
    """
    Spawn skoolposts agent to:
    1. Scan community for newest posts (24h)
    2. Filter out posts Duncan already engaged with
    3. Generate target_count comments (1-3 sentences each)
    
    Returns list of dicts: [{"post_url": "...", "comment": "..."}, ...]
    """
    agent_dir = Path(__file__).parent
    
    cmd = [
        "openclaw", "agents", "spawn",
        "--agent", "skoolposts",
        "--message", f"""Scan /{community_slug} for the newest posts (last 24 hours, ALL categories).

Find {target_count} posts where Duncan can add value.
Skip any posts Duncan already commented on.

For each post, generate a comment:
- 1-3 sentences
- Short, friendly, casual
- Match the community voice
- No politics, no drama

Output JSON array:
[
  {{"post_title": "...", "post_url": "...", "comment": "..."}},
  ...
]
""",
        "--timeout", "120"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=agent_dir)
    
    if result.returncode != 0:
        print(f"  ❌ Agent spawn failed: {result.stderr}")
        return []
    
    # Parse JSON output
    try:
        output = result.stdout.strip()
        # Look for JSON array in output
        if "[" in output and "]" in output:
            json_start = output.index("[")
            json_end = output.rindex("]") + 1
            json_str = output[json_start:json_end]
            comments = json.loads(json_str)
            return comments
        else:
            print(f"  ⚠️  No JSON array found in output")
            return []
    except Exception as e:
        print(f"  ❌ Failed to parse comments: {e}")
        return []

def push_comments_to_notion(community, comments, scheduled_time):
    """Push comment drafts to Notion for Duncan's review."""
    import os
    import requests
    
    notion_token = os.environ.get("NOTION_TOKEN")
    db_id = "30cf259c-0f17-81a9-ae1f-de9720b5cb64"
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    pushed = 0
    
    for comment_data in comments:
        post_title = comment_data.get("post_title", "")
        post_url = comment_data.get("post_url", "")
        comment_text = comment_data.get("comment", "")
        
        # Create page in Skool Posts DB
        page_data = {
            "parent": {"database_id": db_id},
            "properties": {
                "Community": {
                    "select": {"name": community}
                },
                "Type": {
                    "select": {"name": "Comment"}
                },
                "Status": {
                    "select": {"name": "Draft"}
                },
                "Scheduled": {
                    "date": {"start": scheduled_time}
                },
                "Post URL": {
                    "url": post_url if post_url else None
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": f"Reply to: {post_title}"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": comment_text}}]
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
            pushed += 1
        else:
            print(f"    ⚠️  Failed to push comment: {response.status_code}")
    
    print(f"  ✅ Pushed {pushed}/{len(comments)} comments to Notion")
    return pushed

def main():
    print(f"\n{'='*60}")
    mode = "TEST MODE (Build Room only)" if TEST_MODE else "PRODUCTION"
    print(f"Skool Comments Daily Run — {mode}")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    # Reset state if new day
    if reset_if_new_day():
        print("🔄 New day detected, rotation state reset\n")
    
    # Pick communities
    if TEST_MODE:
        communities = CONFIG["test_communities"]
        comment_limit = CONFIG["test_limits"]["comments_per_day"]
        # In test mode, just one community (Build Room) with N total comments
        print(f"🧪 TEST MODE: {comment_limit} comments to Build Room\n")
    else:
        communities = pick_communities(5, "comments")
    
    print(f"📋 Communities selected for comments:")
    for i, comm in enumerate(communities, 1):
        slot_time = TIME_SLOTS[i-1]
        hours = slot_time // 60
        mins = slot_time % 60
        time_str = f"10:{mins:02d}am" if hours < 2 else f"{10 + hours}:{mins:02d}{'am' if hours < 2 else 'pm'}"
        print(f"  {i}. /{comm} at {time_str} (5-6 comments)")
    
    print()
    
    # Process each community at its scheduled time
    start_time = time.time()
    total_comments = 0
    
    for i, community in enumerate(communities):
        slot_minutes = TIME_SLOTS[i]
        target_time = start_time + (slot_minutes * 60)
        now = time.time()
        
        # Wait until target time
        if now < target_time:
            wait_seconds = target_time - now
            wait_minutes = wait_seconds / 60
            print(f"⏳ Waiting {wait_minutes:.1f} minutes until next batch...")
            time.sleep(wait_seconds)
        
        # Generate comments
        print(f"\n💬 Generating comments for /{community}...")
        comments = generate_comments_for_community(community, target_count=6)
        
        if comments:
            # Calculate scheduled time for Notion
            scheduled_time = datetime.fromtimestamp(target_time).isoformat()
            
            # Push to Notion
            pushed = push_comments_to_notion(community, comments, scheduled_time)
            total_comments += pushed
        else:
            print(f"  ⚠️  No comments generated for /{community}")
    
    print(f"\n{'='*60}")
    print(f"✅ Daily comment run complete — {total_comments} comments drafted")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
