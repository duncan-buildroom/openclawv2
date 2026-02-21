#!/usr/bin/env python3
"""
Feb 18, 2026 — Wednesday content queue.
Standalone tweets scheduled with 2-4hr gaps starting 9am ET.
"""

import sys
import random
import json
from datetime import datetime, timezone, timedelta

sys.path.insert(0, '/data/.openclaw/workspace/agents/threads')
import tweet_scheduler

# 9:00am ET = 14:00 UTC
base_time = datetime(2026, 2, 18, 14, 0, 0, tzinfo=timezone.utc)

tweets = [
    # 1. Trend-jacked: OpenClaw subscription abuse / API ban wave (HIGH heat)
    "Everyone's hacking their $20 Claude subscription to run agents. I just pay for the API. My agents have run 24/7 for months, zero bans, zero drama. Sometimes the 'expensive' route is the cheap one.",

    # 2. Fresh reaction: Figma MCP + Claude Code UI (FRESH today, design background)
    "Figma just shipped an MCP that turns Claude Code UI into editable Figma frames. I spent 15 years as an art director before I started building AI systems. This is the first tool that actually sits at the intersection of both.",

    # 3. Hot take: personal branding fatigue (LinkedIn backlash trend)
    "Personal branding didn't ruin LinkedIn. Lazy AI slop did. There's a difference between documenting real results and outsourcing your voice to GPT. 110K followers in 12 months, I wrote every word.",

    # 4. Proof / results: agent architecture
    "I run 7 AI agents from one orchestrator. They research trends, write tweets, build carousels, and publish my content, every day. Total daily cost: less than a coffee. Built it once. It runs forever.",
]

scheduled_times = []
current = base_time

for i, tweet in enumerate(tweets):
    tweet_scheduler.add_to_queue(tweet, scheduled_for=current.isoformat())
    scheduled_times.append(current.strftime("%I:%M %p ET"))
    gap = random.uniform(2.0, 4.0)
    current = current + timedelta(hours=gap)
    print(f"  Tweet {i+1}: {scheduled_times[-1]} ({len(tweet)} chars)")
    print(f"    {tweet[:80]}...")
    if i < len(tweets) - 1:
        print(f"  Next gap: {gap:.1f}hrs\n")

print(f"\n✅ {len(tweets)} tweets queued for Feb 18, 2026")
print(f"   Window: 9:00 AM ET → ~{current.strftime('%I:%M %p ET')}")
