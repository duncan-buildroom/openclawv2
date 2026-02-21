#!/usr/bin/env python3
"""
Skool Browser Automation Helpers
Handles posting and commenting via browser automation with proper tab management.
"""

import time
from browser import browser

def login_to_skool(email, password):
    """Log in to Skool (run once at start of session)."""
    try:
        browser(action="open", targetUrl="https://www.skool.com/login", profile="openclaw")
        time.sleep(2)
        
        # Type email
        browser(
            action="act",
            request={"kind": "type", "ref": "input[type=email]", "text": email},
            profile="openclaw"
        )
        
        # Type password
        browser(
            action="act",
            request={"kind": "type", "ref": "input[type=password]", "text": password},
            profile="openclaw"
        )
        
        # Click login
        browser(
            action="act",
            request={"kind": "click", "ref": "button[Log in]"},
            profile="openclaw"
        )
        
        time.sleep(3)
        return True
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False

def post_to_community(community_slug, post_text):
    """
    Post to a Skool community.
    Returns post URL on success, None on failure.
    """
    try:
        # Navigate to community
        browser(
            action="navigate",
            targetUrl=f"https://www.skool.com/{community_slug}",
            profile="openclaw"
        )
        time.sleep(2)
        
        # Click "Create Post" or "New Post" button
        # Try multiple possible selectors
        for selector in ["button:has-text('Create Post')", "button:has-text('New Post')", "[data-test-id='create-post']"]:
            try:
                browser(
                    action="act",
                    request={"kind": "click", "selector": selector},
                    profile="openclaw"
                )
                break
            except:
                continue
        
        time.sleep(1)
        
        # Type post text (find textarea)
        browser(
            action="act",
            request={"kind": "type", "selector": "textarea", "text": post_text},
            profile="openclaw"
        )
        
        time.sleep(1)
        
        # Click Post button
        browser(
            action="act",
            request={"kind": "click", "selector": "button:has-text('Post')"},
            profile="openclaw"
        )
        
        time.sleep(3)
        
        # Get current URL (should be the new post)
        snapshot = browser(action="snapshot", profile="openclaw")
        post_url = snapshot.get("url", "")
        
        return post_url
        
    except Exception as e:
        print(f"  ❌ Post failed: {e}")
        return None

def scan_and_comment(community_slug, max_comments=6):
    """
    Scan community for comment opportunities, post comments.
    Uses single tab, sequential navigation.
    Returns list of dicts: [{"post_url": "...", "comment": "...", "comment_url": "..."}, ...]
    """
    try:
        # Navigate to community
        browser(
            action="navigate",
            targetUrl=f"https://www.skool.com/{community_slug}",
            profile="openclaw"
        )
        time.sleep(2)
        
        # Get page snapshot to find recent posts
        snapshot = browser(action="snapshot", profile="openclaw", snapshotFormat="aria")
        
        # Extract post links from snapshot (look for clickable post titles)
        # This is simplified - real implementation needs better parsing
        post_links = []
        # TODO: Parse snapshot to extract post URLs
        
        comments_posted = []
        
        for post_url in post_links[:max_comments]:
            # Navigate to post (same tab)
            browser(action="navigate", targetUrl=post_url, profile="openclaw")
            time.sleep(2)
            
            # Check if Duncan already commented (look for his name in comments)
            snapshot = browser(action="snapshot", profile="openclaw")
            page_text = snapshot.get("text", "")
            
            if "Duncan Rogoff" in page_text or "duncan@buildroom.ai" in page_text:
                print(f"  ⏭️  Already commented, skipping")
                continue
            
            # Generate comment for this post
            # TODO: Spawn agent to generate contextual comment
            comment_text = "This is helpful, thanks for sharing!"
            
            # Find comment textarea and post
            browser(
                action="act",
                request={"kind": "type", "selector": "textarea", "text": comment_text},
                profile="openclaw"
            )
            
            time.sleep(1)
            
            browser(
                action="act",
                request={"kind": "click", "selector": "button:has-text('Comment')"},
                profile="openclaw"
            )
            
            time.sleep(2)
            
            # Get comment URL
            snapshot = browser(action="snapshot", profile="openclaw")
            comment_url = snapshot.get("url", "")
            
            comments_posted.append({
                "post_url": post_url,
                "comment": comment_text,
                "comment_url": comment_url
            })
        
        return comments_posted
        
    except Exception as e:
        print(f"  ❌ Scan/comment failed: {e}")
        return []

def close_all_tabs():
    """Close all browser tabs."""
    try:
        tabs = browser(action="tabs", profile="openclaw")
        for tab in tabs.get("tabs", []):
            if tab.get("id"):
                browser(action="close", targetId=tab["id"], profile="openclaw")
    except:
        pass
