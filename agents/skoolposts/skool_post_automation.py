#!/usr/bin/env python3
"""
Skool Post Automation - Correct flow based on actual HTML structure
"""

import time
import json
from pathlib import Path

def post_to_skool(community_slug, title, body, category_name="Hangout"):
    """
    Post to a Skool community using browser automation.
    
    Args:
        community_slug: e.g. "buildroom"
        title: Post title
        body: Post body (will be formatted with line breaks)
        category_name: Category to select (default: Hangout)
    
    Returns:
        dict with {"success": bool, "url": str, "error": str}
    """
    
    # Import browser tool (only works within OpenClaw context)
    try:
        from browser import browser
    except ImportError:
        # Fallback: call browser via subprocess
        import subprocess
        def browser(**kwargs):
            # This is a placeholder - real implementation would shell out to openclaw browser CLI
            raise NotImplementedError("Browser tool only available in OpenClaw runtime")
    
    try:
        # Step 1: Navigate to community
        print(f"  📂 Opening /{community_slug}...")
        browser(
            action="navigate",
            targetUrl=f"https://www.skool.com/{community_slug}",
            profile="openclaw"
        )
        time.sleep(2)
        
        # Step 2: Click "Write something" to open post composer
        print(f"  ✏️  Opening post composer...")
        browser(
            action="act",
            request={
                "kind": "click",
                "selector": "div.styled__TypographyWrapper-sc-70zmwu-0:has-text('Write something')"
            },
            profile="openclaw"
        )
        time.sleep(1)
        
        # Step 3: Fill in title
        print(f"  📝 Writing title...")
        # Title field should appear - find input/textarea for title
        browser(
            action="act",
            request={
                "kind": "type",
                "selector": "input[placeholder*='title' i], input[type='text']:first-of-type",
                "text": title
            },
            profile="openclaw"
        )
        time.sleep(0.5)
        
        # Step 4: Fill in body
        print(f"  📝 Writing body...")
        browser(
            action="act",
            request={
                "kind": "type",
                "selector": "textarea, div[contenteditable='true']",
                "text": body
            },
            profile="openclaw"
        )
        time.sleep(0.5)
        
        # Step 5: Select category
        print(f"  📁 Selecting category: {category_name}...")
        # Click the "Select a category" dropdown
        browser(
            action="act",
            request={
                "kind": "click",
                "selector": "div.styled__CategoryLabel-sc-1v9n50v-0"
            },
            profile="openclaw"
        )
        time.sleep(0.5)
        
        # Click the category option
        # This uses the React fiber workaround we documented
        # For now, use text selector
        browser(
            action="act",
            request={
                "kind": "click",
                "selector": f"div:has-text('{category_name}')"
            },
            profile="openclaw"
        )
        time.sleep(0.5)
        
        # Step 6: Click Post button
        print(f"  🚀 Posting...")
        browser(
            action="act",
            request={
                "kind": "click",
                "selector": "button.styled__SubmitButtonWrapper-sc-41pcfm-2:has-text('Post')"
            },
            profile="openclaw"
        )
        time.sleep(3)
        
        # Step 7: Get the post URL
        snapshot = browser(
            action="snapshot",
            profile="openclaw"
        )
        
        post_url = snapshot.get("url", "")
        
        print(f"  ✅ Posted successfully")
        
        return {
            "success": True,
            "url": post_url,
            "error": None
        }
        
    except Exception as e:
        print(f"  ❌ Post failed: {e}")
        return {
            "success": False,
            "url": None,
            "error": str(e)
        }

def format_post_body(text):
    """
    Format post body: sentence per paragraph.
    Splits on '. ' and adds line breaks.
    """
    sentences = text.split('. ')
    # Add period back to each sentence except last
    formatted = []
    for i, sentence in enumerate(sentences):
        if i < len(sentences) - 1:
            formatted.append(sentence + '.')
        else:
            formatted.append(sentence)
    
    # Join with double line breaks (paragraph separation)
    return '\n\n'.join(formatted)

# Category mapping for Build Room
BUILD_ROOM_CATEGORIES = {
    "announcements": "Announcements",
    "daily": "Daily Actions",
    "roadmap": "$1M Roadmap",
    "youtube": "YouTube Tutorials",
    "wins": "Wins",
    "strategy": "Business Strategy",
    "hangout": "Hangout",
    "checkins": "Check-Ins",
    "help": "Help!"
}

if __name__ == "__main__":
    # Test
    title = "Quick question for the group"
    body = "What's one automation you built this week that actually saved you time? I'm curious what's working for people right now. Drop it below."
    
    body_formatted = format_post_body(body)
    
    print("Test post formatting:")
    print("─" * 60)
    print(f"Title: {title}")
    print(f"\nBody:\n{body_formatted}")
    print("─" * 60)
    
    # result = post_to_skool("buildroom", title, body_formatted, "Hangout")
    # print(f"\nResult: {result}")
