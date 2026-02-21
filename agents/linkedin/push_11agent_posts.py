import requests
import json

TOKEN = "$NOTION_TOKEN"
DB_ID = "d4266f2c-ed0a-4c5b-8b81-7cb4e2ffad86"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def make_paragraph(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text}}] if text.strip() else []
        }
    }

posts = [
    {
        "title": "11 AI agents run my entire content operation. Here's every single one.",
        "angle": "Pattern Interrupt — Giving away the whole system as the hook. Stops the scroll by leading with access, not a pitch.",
        "body": """11 AI agents run my entire content operation. Here's every single one.

Not a breakdown. Not a tutorial. The actual copy-paste prompts I use every day.

This is the system behind 110,000 followers built in under 12 months.

11 specialized agents. Each with one job:

→ Orchestrator, coordinates your entire content calendar
→ Daily Briefer, pulls research and trends every morning
→ Short-Form Scripter, writes Reels and TikTok scripts
→ Carousel Creator, builds your LinkedIn slide decks
→ Trend Researcher, keeps everything timely and relevant
→ Plus X Agent, Reddit Agent, Lead Magnet Builder, Image Generator, Community Writer, LinkedIn Writer

Each agent includes beginner setup steps, [bracket] variables, and pro tips.

Works in Claude, ChatGPT, or any LLM. No tools required.

Whatever I build, you get it. Inside The Build Room.

The Build Room, link in bio.

---

IMAGE BRIEF A (Abstract/Illustrated):
Type: infographic
Hook text overlay: 11 Agents. One System.
Background concept: Cartoon robot team, each bot labeled with a role, arranged in a circle around a central hub
Accent colors: neon green #00FF00 on black background

IMAGE BRIEF B (Concrete/Results):
Type: result_card
Hook text overlay: 110K Followers. 11 Agents.
Background concept: Analytics dashboard showing follower growth curve from 0 to 110K over 12 months
Accent colors: orange #FF6600"""
    },
    {
        "title": "Most people use AI for one thing. That's why their content still feels like a grind.",
        "angle": "Pain Point — Hits the exact frustration of treating AI as a one-off tool instead of a system. Calls out the behavior before offering the fix.",
        "body": """Most people use AI for one thing. That's why their content still feels like a grind.

You open ChatGPT. Type a prompt. Get a caption. Close the tab.

That's a calculator, not a content team.

I built 11 specialized agents instead. Each one trained for a single job:

→ Orchestrator coordinates your entire strategy
→ Daily Briefer surfaces trending topics every morning
→ Short-Form Scripter writes Reels scripts in minutes
→ LinkedIn Writer handles posts like this one
→ Trend Researcher keeps content relevant without the doomscrolling
→ Plus X Agent, Reddit Agent, Carousel Creator, Lead Magnet Builder, Image Generator

This is the exact system behind 110,000 followers built in under 12 months.

Copy-paste prompts. [Bracket] variables. Works in Claude, ChatGPT, or any LLM. No tools required.

Whatever I build, you get it. Inside The Build Room.

The Build Room, link in bio.

---

IMAGE BRIEF A (Abstract/Illustrated):
Type: infographic
Hook text overlay: Calculator vs. Content Team
Background concept: Split panel, left side shows lonely person at laptop with one robot, right side shows an army of 11 specialized robots in action
Accent colors: neon green #00FF00 on black background

IMAGE BRIEF B (Concrete/Results):
Type: result_card
Hook text overlay: 11 Agents. Zero Grind.
Background concept: Side-by-side of a content calendar fully populated by agents vs. an empty one, showing automation output
Accent colors: orange #FF6600"""
    },
    {
        "title": "Stop using AI like a personal assistant. It can run your entire content team.",
        "angle": "Contrarian — Challenges the default way people think about AI. The take is that treating AI as a single assistant is the wrong mental model entirely.",
        "body": """Stop using AI like a personal assistant. It can run your entire content team.

Most creators use one prompt for one output. That's not a system, that's a slot machine.

I built 11 specialized agents instead. Each one has a job. All of them work together.

→ Orchestrator coordinates the whole content strategy
→ Trend Researcher surfaces what's worth posting about
→ Short-Form Scripter writes Reels scripts on demand
→ Reddit Agent engages communities without sounding like an ad
→ Lead Magnet Builder turns ideas into downloadable products

This is the exact system behind 110,000 followers built in under 12 months.

Copy-paste prompts. [Bracket] variables. Beginner setup steps. Works in Claude, ChatGPT, or any LLM. No tools required.

Whatever I build, you get it. Inside The Build Room.

The Build Room, link in bio.

---

IMAGE BRIEF A (Abstract/Illustrated):
Type: infographic
Hook text overlay: Stop Using AI Wrong.
Background concept: Cartoon slot machine being smashed, replaced by a coordinated robot assembly line labeled with agent names
Accent colors: neon green #00FF00 on black background

IMAGE BRIEF B (Concrete/Results):
Type: result_card
Hook text overlay: 11 Agents. 110K Followers.
Background concept: Terminal or n8n-style workflow showing 11 agent nodes all firing simultaneously with checkmarks
Accent colors: orange #FF6600"""
    }
]

for post in posts:
    lines = post["body"].split("\n")
    blocks = [make_paragraph(line) for line in lines]

    payload = {
        "parent": {"database_id": DB_ID},
        "properties": {
            "Title": {
                "title": [{"type": "text", "text": {"content": post["title"]}}]
            },
            "Status": {
                "select": {"name": "Draft"}
            },
            "Notes": {
                "rich_text": [{"type": "text", "text": {"content": post["angle"]}}]
            }
        },
        "children": blocks
    }

    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        page_id = response.json().get("id", "")
        print(f"✅ Created: {post['title'][:60]}...")
        print(f"   Page ID: {page_id}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   {response.text[:300]}")
    print()
