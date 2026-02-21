#!/usr/bin/env python3
"""
Call the roadto1m agent (via Claude API) to generate real content for a day.
"""

import os
import sys
import json
import requests
from pathlib import Path

# Read auth profiles to get Claude credentials
AUTH_PROFILES_PATH = "/data/.openclaw/agents/main/agent/auth-profiles.json"

def get_anthropic_key():
    """Get Anthropic API key from auth profiles"""
    if Path(AUTH_PROFILES_PATH).exists():
        with open(AUTH_PROFILES_PATH) as f:
            profiles = json.load(f)
            
            # Try fallback API key first
            fallback = profiles.get("profiles", {}).get("anthropic:fallback", {})
            if fallback.get("type") == "api_key" and fallback.get("key"):
                return fallback["key"]
            
            # Try default OAuth (but won't work for direct API calls)
            default = profiles.get("profiles", {}).get("anthropic:default", {})
            if default.get("type") == "api_key" and default.get("key"):
                return default["key"]
    
    return None

def load_agent_soul():
    """Load the roadto1m agent's SOUL.md for context"""
    soul_path = Path(__file__).parent / "SOUL.md"
    if soul_path.exists():
        return soul_path.read_text()
    return ""

def generate_content_with_claude(day_num, topic, bucket, context=""):
    """Call Claude API to generate content"""
    
    api_key = get_anthropic_key()
    if not api_key:
        return {"error": "No Anthropic API key found in auth-profiles.json"}
    
    # Load agent's SOUL for voice/format rules
    soul = load_agent_soul()
    
    # Build the prompt
    system_prompt = f"""You are the Road to $1M content agent. Your job is to generate all 9 sections for a daily video in Duncan's "Day X of building a $1M personal brand with AI" series.

{soul}

Generate content that sounds EXACTLY like Duncan. Direct, operator tone, proof over persuasion, documenting not teaching.

CRITICAL: Output ONLY valid JSON. No markdown, no explanations, just the JSON object."""

    user_prompt = f"""Generate complete content for Day {day_num}.

**Topic:** {topic}
**Bucket:** {bucket}
**Context:** {context if context else "Duncan just posted Day {day_num - 1}. Continue the series momentum."}

**Output this exact JSON structure:**
```json
{{
    "hook": "Day {day_num} of building a $1M personal brand with AI",
    "deliverable": "Specific deliverable description (what they're getting)",
    "deliverable_link": "URL or 'Inside The Build Room'",
    "short_form_script": "Full 60-90 sec video script. Hook → Giveaway → Content → 'This is in The Build Room.' Follow voice rules: direct, concrete, proof-driven.",
    "tiktok": "Caption under 150 words. Lead with hook, 2-3 punchy lines, NO hashtags, end with 'Link in bio.'",
    "twitter": "Max 280 chars. Documenting voice. End with 'The Build Room, link in bio.'",
    "linkedin": "100-150 words. Founder voice. Hook first 3 lines. End with 'The Build Room, link in bio.'",
    "skool": "50-100 words. Café tone. Connect to member pain. Call to action within community.",
    "reddit": "100-150 words. Value-first, NOT promotional. Insight or story. Mention Build Room only in context.",
    "carousel": "7-slide concept. Story arc: Hook → Problem → Mechanism → Proof → CTA. Slide-by-slide with image concepts.",
    "youtube": "Video concept: title (under 100 chars), hook, 3-5 key points, CTA, estimated length.",
    "classroom": "120-150 words. Format: asset → ICP problem → what changes → deliverable link → 'Whatever I build, you get.'"
}}
```

ICP: Expertise-rich, audience-poor business owners, $8K-20K/mo from referrals. Invisible online. See Duncan's journey and think "I could do that."

Generate now."""

    # Call Claude API
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    payload = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 4096,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload,
        timeout=120
    )
    
    if response.status_code != 200:
        return {"error": f"Claude API error: {response.status_code}", "details": response.text}
    
    data = response.json()
    content = data.get("content", [{}])[0].get("text", "")
    
    # Parse JSON from response
    try:
        # Try to extract JSON if wrapped in markdown
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        generated = json.loads(content)
        
        # Validate required fields
        required = ["hook", "deliverable", "short_form_script", "tiktok", "twitter", 
                   "linkedin", "skool", "reddit", "carousel", "youtube", "classroom"]
        
        for field in required:
            if field not in generated:
                return {"error": f"Missing required field: {field}"}
        
        return {
            "success": True,
            "content": generated,
            "usage": data.get("usage", {})
        }
    
    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse JSON from Claude response",
            "details": str(e),
            "raw": content
        }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate day content with Claude")
    parser.add_argument("--day", type=int, required=True)
    parser.add_argument("--topic", type=str, required=True)
    parser.add_argument("--bucket", type=str, required=True)
    parser.add_argument("--context", type=str, default="")
    
    args = parser.parse_args()
    
    result = generate_content_with_claude(args.day, args.topic, args.bucket, args.context)
    
    print(json.dumps(result, indent=2))
