import os
#!/usr/bin/env python3
"""
Push LinkedIn post to Notion LinkedIn Posts database
"""

import requests
import json
from datetime import datetime

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
LINKEDIN_POSTS_DB_ID = "d4266f2c-ed0a-4c5b-8b81-7cb4e2ffad86"
LEAD_MAGNET_PAGE_ID = "308f259c-0f17-8197-9efd-f89bf3b20ecd"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Post content
post_content = """4 cron jobs run my entire business while I sleep.

Here's what happens between midnight and 7am (without me):

I built these in 48 hours. Now they run 24/7 for ~$5/day.

**What executes automatically:**
• 7:00 AM — Morning briefing lands in my inbox (trends, priorities, what needs attention)
• 12:00 AM — Daily tracker logs everything (revenue, growth, decisions)
• 12:00 AM — GitHub backup runs (entire workspace, versioned, safe)
• 11:00 PM Sunday — Trend research compiles the week's signals

I wake up to a briefing. My workspace is backed up. Trends are researched.

Zero manual work.

These exact 4 jobs helped me grow to 110K+ followers. Not because they post for me—because they free my brain for the work that actually matters.

The Autopilot Stack: 4 copy-paste prompts that configure themselves in OpenClaw.

Want them? Two ways:
→ Comment "AUTOPILOT" 
→ Or join skool.com/buildroom"""

hook_variants = [
    "4 cron jobs run my entire business while I sleep.",
    "My AI does more before 7am than most people do all day.",
    "I haven't manually backed up my work in 6 months. Here's why:"
]

# Create page content blocks
children = [
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "Main Post"}}]}
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"text": {"content": post_content}}]}
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "Hook Variants"}}]}
    }
]

# Add hook variants as numbered list
for i, hook in enumerate(hook_variants, 1):
    children.append({
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": [{"text": {"content": hook}}]}
    })

# Prepare the page payload
payload = {
    "parent": {"database_id": LINKEDIN_POSTS_DB_ID},
    "properties": {
        "Title": {"title": [{"text": {"content": "The Autopilot Stack — 4 Cron Jobs"}}]},
        "Lead Magnet": {"relation": [{"id": LEAD_MAGNET_PAGE_ID}]},
        "Status": {"select": {"name": "Draft"}},
        "Notes": {"rich_text": [{"text": {"content": "~150 words | Behind-the-scenes, results-driven | CTA: Comment AUTOPILOT or skool.com/buildroom"}}]}
    },
    "children": children
}

# Create the page
resp = requests.post(
    "https://api.notion.com/v1/pages",
    headers=headers,
    json=payload,
    timeout=30
)

if resp.status_code == 200:
    data = resp.json()
    print(f"✅ LinkedIn post created: {data['url']}")
    print(f"✅ Post title: The Autopilot Stack — 4 Cron Jobs")
    print(f"✅ Lead magnet relation set")
else:
    print(f"❌ Error {resp.status_code}: {resp.text[:500]}")
