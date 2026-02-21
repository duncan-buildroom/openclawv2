#!/usr/bin/env python3
"""
Road to $1M Daily Page Creator
Creates a new day page in the Road to $1M Notion database with all 9 sections.
Can be run manually or via cron at 6pm to build tomorrow's content.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Notion config
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
ROADTO1M_DB_ID = "30bf259c0f178138b849f25efdc0b4b0"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Content buckets (rotate through these)
BUCKETS = ["🔨 Build", "💡 Lesson", "🎁 Giveaway", "📈 Growth", "💰 Money"]

def get_existing_days():
    """Query database to see what days already exist"""
    response = requests.post(
        f"https://api.notion.com/v1/databases/{ROADTO1M_DB_ID}/query",
        headers=HEADERS,
        json={"sorts": [{"property": "Day", "direction": "descending"}]}
    )
    
    if response.status_code != 200:
        print(f"❌ Error querying database: {response.status_code}")
        print(response.text)
        return []
    
    results = response.json().get("results", [])
    days = []
    
    for page in results:
        props = page.get("properties", {})
        day_num = props.get("Day", {}).get("number")
        if day_num:
            days.append(int(day_num))
    
    return sorted(days)

def pick_next_bucket(existing_days):
    """Pick the next bucket based on rotation"""
    if not existing_days:
        return BUCKETS[0]  # Start with Build
    
    last_day = max(existing_days)
    # Rotate through buckets
    bucket_index = (last_day - 1) % len(BUCKETS)
    return BUCKETS[bucket_index]

def generate_content(day_num, topic, bucket, context=""):
    """
    Generate all 9 sections for the day using the roadto1m agent.
    Calls generate_with_agent.py which uses Claude API.
    """
    
    import subprocess
    
    script_dir = Path(__file__).parent
    generator = script_dir / "generate_with_agent.py"
    
    cmd = [
        "python3", str(generator),
        "--day", str(day_num),
        "--topic", topic,
        "--bucket", bucket
    ]
    
    if context:
        cmd.extend(["--context", context])
    
    print(f"🤖 Generating content with roadto1m agent...")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            print(f"❌ Agent generation failed: {result.stderr}")
            # Fall back to template
            return generate_template_content(day_num, topic, bucket)
        
        data = json.loads(result.stdout)
        
        if data.get("success"):
            generated = data["content"]
            usage = data.get("usage", {})
            
            input_tokens = usage.get("input_tokens", 0)
            output_tokens = usage.get("output_tokens", 0)
            print(f"✅ Generated content ({input_tokens} in, {output_tokens} out)")
            
            return {
                "hook": generated["hook"],
                "deliverable": generated["deliverable"],
                "deliverable_link": generated.get("deliverable_link", "Inside The Build Room"),
                "content": {
                    "short_form_script": generated["short_form_script"],
                    "tiktok": generated["tiktok"],
                    "twitter": generated["twitter"],
                    "linkedin": generated["linkedin"],
                    "skool": generated["skool"],
                    "reddit": generated["reddit"],
                    "carousel": generated["carousel"],
                    "youtube": generated["youtube"],
                    "classroom": generated["classroom"]
                }
            }
        else:
            error = data.get("error", "Unknown error")
            print(f"❌ Agent returned error: {error}")
            # Fall back to template
            return generate_template_content(day_num, topic, bucket)
    
    except Exception as e:
        print(f"❌ Exception calling agent: {e}")
        # Fall back to template
        return generate_template_content(day_num, topic, bucket)

def generate_template_content(day_num, topic, bucket):
    """Fallback template content if agent generation fails"""
    
    hook = f"Day {day_num} of building a $1M personal brand with AI"
    
    return {
        "hook": hook,
        "deliverable": f"[Placeholder: {topic} deliverable - agent generation failed]",
        "deliverable_link": "Inside The Build Room",
        "content": {
            "short_form_script": f"{hook}.\n\nToday I'm giving you {topic}.\n\n[Script content - agent generation failed]\n\nThis is in The Build Room.",
            "tiktok": f"{hook}. {topic}. Link in bio.",
            "twitter": f"Day {day_num}. {topic}. The Build Room, link in bio.",
            "linkedin": f"{hook}.\n\n[LinkedIn post - agent generation failed]\n\nThe Build Room, link in bio.",
            "skool": f"[Skool post - agent generation failed]",
            "reddit": f"[Reddit post - agent generation failed]",
            "carousel": f"[Carousel concept - agent generation failed]",
            "youtube": f"[YouTube concept - agent generation failed]",
            "classroom": f"[Classroom module copy - agent generation failed]"
        }
    }

def create_page_blocks(day_num, topic, bucket, content):
    """Build the page body blocks (9 sections)"""
    
    blocks = []
    
    # Section 1: 📱 Short-Form Script
    blocks.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "📱 Short-Form Script"}}]}
    })
    blocks.append({
        "type": "callout",
        "callout": {
            "icon": {"emoji": "🎬"},
            "rich_text": [{"text": {"content": content["short_form_script"]}}]
        }
    })
    
    # Section 2: 🎵 TikTok
    blocks.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "🎵 TikTok"}}]}
    })
    blocks.append({
        "type": "callout",
        "callout": {
            "icon": {"emoji": "📱"},
            "rich_text": [{"text": {"content": content["tiktok"]}}]
        }
    })
    
    # Section 3: 🐦 X / Twitter
    blocks.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "🐦 X / Twitter"}}]}
    })
    blocks.append({
        "type": "callout",
        "callout": {
            "icon": {"emoji": "✍️"},
            "rich_text": [{"text": {"content": content["twitter"]}}]
        }
    })
    
    # Section 4: 💼 LinkedIn
    blocks.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "💼 LinkedIn"}}]}
    })
    blocks.append({
        "type": "callout",
        "callout": {
            "icon": {"emoji": "💼"},
            "rich_text": [{"text": {"content": content["linkedin"]}}]
        }
    })
    
    # Section 5: 🏠 Skool Posts
    blocks.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "🏠 Skool Posts"}}]}
    })
    blocks.append({
        "type": "callout",
        "callout": {
            "icon": {"emoji": "🏫"},
            "rich_text": [{"text": {"content": content["skool"]}}]
        }
    })
    
    # Section 6: 🔴 Reddit
    blocks.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "🔴 Reddit"}}]}
    })
    blocks.append({
        "type": "callout",
        "callout": {
            "icon": {"emoji": "📝"},
            "rich_text": [{"text": {"content": content["reddit"]}}]
        }
    })
    
    # Section 7: 📸 Carousel
    blocks.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "📸 Carousel"}}]}
    })
    blocks.append({
        "type": "callout",
        "callout": {
            "icon": {"emoji": "🎨"},
            "rich_text": [{"text": {"content": content["carousel"]}}]
        }
    })
    
    # Section 8: 🎬 YouTube
    blocks.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "🎬 YouTube"}}]}
    })
    blocks.append({
        "type": "callout",
        "callout": {
            "icon": {"emoji": "📹"},
            "rich_text": [{"text": {"content": content["youtube"]}}]
        }
    })
    
    # Section 9: 🎓 Classroom Copy
    blocks.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "🎓 Classroom Copy"}}]}
    })
    blocks.append({
        "type": "callout",
        "callout": {
            "icon": {"emoji": "📚"},
            "rich_text": [{"text": {"content": content["classroom"]}}]
        }
    })
    
    return blocks

def create_day_page(day_num, topic, bucket=None, date=None, context=""):
    """Create a new day page in the Road to $1M database"""
    
    if not bucket:
        existing_days = get_existing_days()
        bucket = pick_next_bucket(existing_days)
    
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Generate content with roadto1m agent
    generated = generate_content(day_num, topic, bucket, context)
    
    # Build page blocks
    blocks = create_page_blocks(day_num, topic, bucket, generated["content"])
    
    # Create the page
    page_payload = {
        "parent": {"database_id": ROADTO1M_DB_ID},
        "properties": {
            "Topic": {
                "title": [{"text": {"content": topic}}]
            },
            "Day": {
                "number": day_num
            },
            "Date": {
                "date": {"start": date}
            },
            "Bucket": {
                "select": {"name": bucket}
            },
            "Hook": {
                "rich_text": [{"text": {"content": generated["hook"]}}]
            },
            "Deliverable": {
                "rich_text": [{"text": {"content": generated["deliverable"]}}]
            },
            "Deliverable Link": {
                "url": generated.get("deliverable_link") if generated.get("deliverable_link", "").startswith("http") else None
            },
            "Classroom Copy": {
                "rich_text": [{"text": {"content": generated["content"]["classroom"]}}]
            },
            "Status": {
                "select": {"name": "Scripted"}
            }
        },
        "children": blocks
    }
    
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=HEADERS,
        json=page_payload
    )
    
    if response.status_code == 200:
        page = response.json()
        page_id = page["id"]
        page_url = page["url"]
        
        print(f"✅ Created Day {day_num}: {topic}")
        print(f"   Bucket: {bucket}")
        print(f"   URL: {page_url}")
        print(f"   Page ID: {page_id}")
        
        return {
            "success": True,
            "page_id": page_id,
            "url": page_url,
            "day": day_num,
            "topic": topic,
            "bucket": bucket
        }
    else:
        print(f"❌ Failed to create page: {response.status_code}")
        print(response.text)
        return {"success": False, "error": response.text}

def build_next_day():
    """Automatically build the next day in the series"""
    existing_days = get_existing_days()
    
    if not existing_days:
        next_day = 1
    else:
        next_day = max(existing_days) + 1
    
    # For now, use placeholder topic
    # In production, roadto1m agent should decide this
    topic = f"[Day {next_day} topic to be determined]"
    
    print(f"Building Day {next_day}...")
    result = create_day_page(next_day, topic)
    
    return result

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create Road to $1M daily page")
    parser.add_argument("--day", type=int, help="Day number")
    parser.add_argument("--topic", type=str, help="Topic/deliverable for the day")
    parser.add_argument("--bucket", type=str, choices=BUCKETS, help="Content bucket")
    parser.add_argument("--date", type=str, help="Date (YYYY-MM-DD)")
    parser.add_argument("--context", type=str, default="", help="Additional context for content generation")
    parser.add_argument("--auto", action="store_true", help="Auto-build next day")
    
    args = parser.parse_args()
    
    if args.auto:
        result = build_next_day()
    elif args.day and args.topic:
        result = create_day_page(args.day, args.topic, args.bucket, args.date, args.context)
    else:
        print("Usage:")
        print("  Auto-build next day:    python3 create_daily_page.py --auto")
        print("  Manual:                 python3 create_daily_page.py --day 4 --topic 'Topic Name' [--bucket '🔨 Build']")
        sys.exit(1)
    
    if result.get("success"):
        sys.exit(0)
    else:
        sys.exit(1)
