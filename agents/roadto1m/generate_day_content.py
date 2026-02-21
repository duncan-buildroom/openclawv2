#!/usr/bin/env python3
"""
Generate real content for a Road to $1M day.
This script is meant to be called BY the roadto1m agent when it needs to create a day's content.
It provides the structure, the agent provides the voice.
"""

import sys
import json
from datetime import datetime

def generate_day_content(day_num, topic, bucket, context=""):
    """
    Generate all 9 sections for a Road to $1M day.
    
    Args:
        day_num: Day number (1-30+)
        topic: What the day is about (e.g. "Creator Content Cloner")
        bucket: Content bucket (Build/Lesson/Giveaway/Growth/Money)
        context: Additional context about what was built/done
    
    Returns:
        Dict with all sections
    """
    
    # This is where the roadto1m agent's logic goes
    # For now, return a JSON structure that the agent should fill in
    
    hook = f"Day {day_num} of building a $1M personal brand with AI"
    
    # Build the prompt for content generation
    prompt = f"""
Generate complete content for Day {day_num} of the Road to $1M series.

**Topic:** {topic}
**Bucket:** {bucket}
**Context:** {context if context else "None provided"}

Generate ALL 9 sections following these rules:

## 1. 📱 Short-Form Script (60-90 sec video)
**Format:**
- Hook: "{hook}"
- Giveaway: "Today I'm giving you [specific asset]" (SECOND sentence, no context first)
- Content: One idea, 30-60 seconds, Duncan's voice (direct, operator tone, short sentences)
- Close: "This is in The Build Room. Along with everything else I've already built."

**Voice rules:**
- Documenting > teaching
- First person, concrete details
- No em dashes, use commas
- Casual confidence ("literally," "actually," "honestly," "the thing is")
- Proof over persuasion (numbers, not adjectives)

## 2. 🎵 TikTok Caption
**Format:**
- Lead with "{hook}."
- 2-3 punchy lines summarizing the value
- NO hashtags (TikTok handles discovery differently)
- CTA: "Link in bio."
- Under 150 words

## 3. 🐦 X / Twitter
**Format:**
- Short documenting voice
- Max 280 chars including CTA
- CTA: "The Build Room, link in bio."

## 4. 💼 LinkedIn
**Format:**
- Hook: First 3 lines must stop the scroll
- Length: 100-150 words
- Voice: Founder-to-founder documentation
- Tone: Professional but still Duncan (not corporate)
- CTA: "The Build Room, link in bio."

## 5. 🏠 Skool Posts
**Format:**
- 50-100 words
- Café conversation tone
- Personal interjections
- Connect deliverable to member pain point
- End with asset link or call to action within community

## 6. 🔴 Reddit
**Format:**
- 100-150 words
- Value-first, NOT promotional
- Actual insight or story
- Mention Build Room only in context if at all
- Focus on helping, not selling

## 7. 📸 Carousel Concept
**Format:**
- Story arc: Hook → Problem → Mechanism → Proof → CTA
- 7 slides (character images + workflow screenshots + infographic)
- Visual theme from CAROUSEL_THEMES.md
- Slide-by-slide breakdown with image concepts

## 8. 🎬 YouTube Concept
**Format:**
- Video title (under 100 chars)
- Hook for first 10 seconds
- 3-5 key points to cover
- CTA at end
- Estimated length

## 9. 🎓 Classroom Copy (120-150 words)
**Format:**
- One sentence: what this day's asset is
- 2-3 sentences: the problem it solves for the ICP
- 1-2 sentences: what changes when they use it
- Link to deliverable
- Reminder: "Whatever I build, you get."

**ICP Context:**
Expertise-rich, audience-poor business owners doing $8K-20K/mo from referrals. They're good at what they do but invisible online. They see Duncan's journey and think "I could do that."

**Output as JSON:**
{{
    "hook": "{hook}",
    "deliverable": "Specific deliverable description",
    "deliverable_link": "URL or 'In Build Room'",
    "short_form_script": "Full script...",
    "tiktok": "Caption...",
    "twitter": "Tweet...",
    "linkedin": "Post...",
    "skool": "Post...",
    "reddit": "Post...",
    "carousel": "Concept...",
    "youtube": "Concept...",
    "classroom": "Module copy..."
}}
"""
    
    return {
        "prompt": prompt,
        "day": day_num,
        "topic": topic,
        "bucket": bucket,
        "hook": hook
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Road to $1M day content")
    parser.add_argument("--day", type=int, required=True, help="Day number")
    parser.add_argument("--topic", type=str, required=True, help="Topic")
    parser.add_argument("--bucket", type=str, required=True, help="Content bucket")
    parser.add_argument("--context", type=str, default="", help="Additional context")
    
    args = parser.parse_args()
    
    result = generate_day_content(args.day, args.topic, args.bucket, args.context)
    
    print(json.dumps(result, indent=2))
