#!/usr/bin/env python3
"""
Daily Briefing Generator - Produces 7am briefing in Duncan's format
Reads: Notion Daily Tracker, recent memory files, active projects
Outputs: Formatted briefing ready for Telegram
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DAILY_TRACKER_DB = "306f259c0f178157bdf1c249e4f4dcb0"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def get_yesterday_entry():
    """Get yesterday's Notion Daily Tracker entry"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    query = {
        "filter": {
            "property": "Date",
            "date": {"equals": yesterday}
        }
    }
    
    resp = requests.post(
        f"https://api.notion.com/v1/databases/{DAILY_TRACKER_DB}/query",
        headers=HEADERS,
        json=query
    )
    
    results = resp.json().get("results", [])
    if not results:
        return None
    
    page = results[0]
    props = page.get("properties", {})
    
    # Extract data
    entry = {
        "date": yesterday,
        "llm_cost": props.get("Total Cost ($)", {}).get("number", 0),
        "tasks_completed": [],
        "notes": ""
    }
    
    # Get tasks from multi-select
    tasks_prop = props.get("Top 3 Tasks", {}).get("multi_select", [])
    entry["tasks_completed"] = [t["name"] for t in tasks_prop]
    
    # Get notes from rich_text
    notes_prop = props.get("Notes", {}).get("rich_text", [])
    if notes_prop:
        entry["notes"] = notes_prop[0].get("plain_text", "")
    
    return entry

def get_today_entry():
    """Get or create today's Notion Daily Tracker entry"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    query = {
        "filter": {
            "property": "Date",
            "date": {"equals": today}
        }
    }
    
    resp = requests.post(
        f"https://api.notion.com/v1/databases/{DAILY_TRACKER_DB}/query",
        headers=HEADERS,
        json=query
    )
    
    results = resp.json().get("results", [])
    if results:
        page = results[0]
        props = page.get("properties", {})
        
        entry = {
            "date": today,
            "page_id": page["id"],
            "tasks": [],
            "notes": ""
        }
        
        tasks_prop = props.get("Top 3 Tasks", {}).get("multi_select", [])
        entry["tasks"] = [t["name"] for t in tasks_prop]
        
        notes_prop = props.get("Notes", {}).get("rich_text", [])
        if notes_prop:
            entry["notes"] = notes_prop[0].get("plain_text", "")
        
        return entry
    
    return None

def read_recent_memory():
    """Read yesterday and today's memory files"""
    memory_dir = Path("/data/.openclaw/workspace/memory")
    
    if not memory_dir.exists():
        return {"yesterday": "", "today": ""}
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    
    memory = {"yesterday": "", "today": ""}
    
    yesterday_file = memory_dir / f"{yesterday}.md"
    if yesterday_file.exists():
        memory["yesterday"] = yesterday_file.read_text()
    
    today_file = memory_dir / f"{today}.md"
    if today_file.exists():
        memory["today"] = today_file.read_text()
    
    return memory

def generate_briefing():
    """Generate formatted briefing"""
    yesterday_data = get_yesterday_entry()
    today_data = get_today_entry()
    memory = read_recent_memory()
    
    # Build briefing sections
    briefing = []
    
    # 1. One Metric - Yesterday's LLM cost
    if yesterday_data:
        cost = yesterday_data.get("llm_cost", 0)
        target = 5.00
        status = "🟢" if cost < target else "🟡" if cost < target * 1.5 else "🔴"
        briefing.append(f"📊 **One Metric**")
        briefing.append(f"Yesterday LLM: ${cost:.2f} {status} (target: <${target:.2f})")
        briefing.append("")
    
    # 2. Yesterday - Progress recap
    briefing.append(f"✅ **Yesterday**")
    if yesterday_data and yesterday_data.get("tasks_completed"):
        for task in yesterday_data["tasks_completed"]:
            briefing.append(f"• {task}")
    elif memory["yesterday"]:
        # Extract key points from memory
        lines = memory["yesterday"].split("\n")
        headlines = [l.strip("# ") for l in lines if l.startswith("## ")]
        if headlines:
            briefing.append(f"• {headlines[0]}")
        else:
            briefing.append("• See memory/yesterday.md")
    else:
        briefing.append("• No logged work")
    briefing.append("")
    
    # 3. Top 3 Today - Priority tasks
    briefing.append(f"🎯 **Top 3 Today**")
    
    # Check Notion for existing tasks
    if today_data and today_data.get("tasks"):
        for task in today_data["tasks"][:3]:
            briefing.append(f"• {task}")
    else:
        # Default based on active projects (from MEMORY.md context)
        briefing.append("• [📊 Audience] Post Carousel #002 to Instagram/TikTok (30m)")
        briefing.append("• [📝 Content] Twitter thread: Feedback-Loop system (45m)")
        briefing.append("• [⚙️ Systems] Test OpenClaw setup guide end-to-end (1h)")
    briefing.append("")
    
    # 4. My Tasks - What I'll work on
    briefing.append(f"🔨 **My Tasks**")
    briefing.append("• Monitor X auto-reply for 'AI' keyword")
    briefing.append("• Track thread engagement (8h intervals)")
    briefing.append("• Update cost tracker at midnight")
    briefing.append("")
    
    # 5. Your Tasks - What Duncan needs to do
    briefing.append(f"📋 **Your Tasks**")
    briefing.append("• Post Carousel #002 to Instagram/Twitter (ready in Notion)")
    briefing.append("• Review setup guide for hosting affiliate link placement")
    briefing.append("• Decide: Test setup guide or ship Twitter thread first?")
    briefing.append("")
    
    # 6. Quick Decisions - Yes/No unblocking
    briefing.append(f"❓ **Quick Decisions**")
    briefing.append("• Activate X auto-reply monitoring? (Y/N)")
    briefing.append("• Add Hostinger affiliate to setup guide manually? (Y/N)")
    briefing.append("• Ship Twitter thread today or wait for Carousel #002 results? (Today/Wait)")
    briefing.append("")
    
    # 7. Growth Ideas - 2-3 opportunities
    briefing.append(f"💡 **Growth Ideas**")
    briefing.append("• Package format_validator.py as 'Quality Control' mini-course for Build Room")
    briefing.append("• Turn OpenClaw setup into YouTube tutorial series (5-7 videos)")
    briefing.append("• Cross-promote Comment Content Engine in X replies to content strategy questions")
    
    return "\n".join(briefing)

def save_briefing(briefing_text):
    """Save briefing to file for cron delivery"""
    output_file = Path("/tmp/daily_briefing.txt")
    output_file.write_text(briefing_text)
    return output_file

if __name__ == "__main__":
    import sys
    
    briefing = generate_briefing()
    
    # Check for --save flag
    if "--save" in sys.argv:
        output_file = save_briefing(briefing)
        print(f"✅ Briefing saved to {output_file}")
    else:
        print(briefing)
