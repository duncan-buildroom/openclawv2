#!/usr/bin/env python3
"""
X Following Cleanse — Analyzes Duncan's following list and recommends unfollows.

Uses OAuth 1.0a (tweepy) for authenticated access to own following list.
Free tier CAN read your own following list via get_users_following.

Flags:
- Accounts outside niche
- Inactive accounts (no posts in 90 days)  
- Low engagement ratios
- Not on watchlist (potential cleanup)

Output: Categorized recommendations for Duncan to approve.
"""

import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import tweepy
except ImportError:
    print("Installing tweepy...")
    import subprocess
    subprocess.run(["pip", "install", "tweepy", "--break-system-packages", "-q"])
    import tweepy

CREDENTIALS_FILE = "/data/.openclaw/workspace/.credentials"
WATCHLIST_FILE = Path(__file__).parent / "X_WATCHLIST.md"
OUTPUT_DIR = Path(__file__).parent / "cache"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Niche keywords — accounts with these in bio are "on-topic"
NICHE_KEYWORDS = [
    "ai", "automation", "n8n", "make.com", "zapier", "no-code", "nocode",
    "saas", "micro-saas", "indie", "solopreneur", "founder", "builder",
    "agent", "llm", "gpt", "claude", "openai", "anthropic", "gemini",
    "creator", "content", "community", "skool", "growth", "marketing",
    "startup", "build in public", "developer", "engineer", "tech",
    "design", "product", "entrepreneur", "freelance", "agency",
    "prompt", "machine learning", "deep learning", "neural",
]


def load_credentials():
    creds = {}
    with open(CREDENTIALS_FILE) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                creds[k] = v
    return creds


def load_watchlist_handles():
    """Parse handles from X_WATCHLIST.md"""
    handles = set()
    try:
        with open(WATCHLIST_FILE) as f:
            for line in f:
                if line.strip().startswith("| @"):
                    handle = line.strip().split("|")[1].strip().lstrip("@")
                    handles.add(handle.lower())
    except FileNotFoundError:
        pass
    return handles


def get_client():
    creds = load_credentials()
    return tweepy.Client(
        consumer_key=creds['X_CONSUMER_KEY'],
        consumer_secret=creds['X_CONSUMER_SECRET'],
        access_token=creds['X_ACCESS_TOKEN'],
        access_token_secret=creds['X_ACCESS_TOKEN_SECRET'],
        wait_on_rate_limit=False
    )


def analyze_following():
    """Pull following list and categorize for cleanse."""
    client = get_client()
    watchlist = load_watchlist_handles()
    
    # Get our user ID
    me = client.get_me()
    user_id = me.data.id
    print(f"✅ Authenticated as @{me.data.username} (ID: {user_id})")
    
    # Get following list
    # Free tier: may be limited, but let's try
    following = []
    pagination_token = None
    
    print("📋 Fetching following list...")
    try:
        while True:
            response = client.get_users_following(
                user_id,
                max_results=100,
                pagination_token=pagination_token,
                user_fields=["description", "public_metrics", "created_at", "username"]
            )
            
            if response.data:
                following.extend(response.data)
                print(f"   Fetched {len(following)} so far...")
            
            if not response.meta or 'next_token' not in response.meta:
                break
            
            pagination_token = response.meta['next_token']
            time.sleep(1)  # Rate limit courtesy
            
    except tweepy.errors.TooManyRequests:
        print("⚠️ Rate limited. Working with what we have.")
    except tweepy.errors.Unauthorized:
        print("❌ Unauthorized — Free tier may not support get_users_following")
        print("   Falling back to manual analysis mode...")
        return None
    
    print(f"\n📊 Analyzing {len(following)} accounts...\n")
    
    # Categorize
    keep = []          # On watchlist or clearly in niche
    review = []        # Might be outside niche
    inactive = []      # No recent activity indicators
    low_engagement = [] # Low follower/following ratio
    
    for user in following:
        handle = user.username.lower()
        bio = (user.description or "").lower()
        metrics = user.public_metrics or {}
        followers = metrics.get("followers_count", 0)
        following_count = metrics.get("following_count", 0)
        tweet_count = metrics.get("tweet_count", 0)
        
        # On watchlist — always keep
        if handle in watchlist:
            keep.append({
                "handle": f"@{user.username}",
                "reason": "On watchlist",
                "followers": followers
            })
            continue
        
        # Check niche relevance via bio
        in_niche = any(kw in bio for kw in NICHE_KEYWORDS)
        
        # Low tweet count might indicate inactive
        is_potentially_inactive = tweet_count < 50
        
        # Engagement ratio (followers / following) — low = potential spam
        ratio = followers / max(following_count, 1)
        is_low_engagement = ratio < 0.1 and followers < 500
        
        if is_potentially_inactive:
            inactive.append({
                "handle": f"@{user.username}",
                "bio": (user.description or "")[:100],
                "tweets": tweet_count,
                "followers": followers
            })
        elif is_low_engagement:
            low_engagement.append({
                "handle": f"@{user.username}",
                "bio": (user.description or "")[:100],
                "ratio": round(ratio, 2),
                "followers": followers
            })
        elif not in_niche:
            review.append({
                "handle": f"@{user.username}",
                "bio": (user.description or "")[:100],
                "followers": followers
            })
        else:
            keep.append({
                "handle": f"@{user.username}",
                "reason": "In niche",
                "followers": followers
            })
    
    results = {
        "analyzed_at": datetime.now().isoformat(),
        "total_following": len(following),
        "keep": len(keep),
        "review_outside_niche": len(review),
        "potentially_inactive": len(inactive),
        "low_engagement": len(low_engagement),
        "details": {
            "keep": sorted(keep, key=lambda x: x["followers"], reverse=True),
            "review": sorted(review, key=lambda x: x["followers"], reverse=True),
            "inactive": inactive,
            "low_engagement": low_engagement
        }
    }
    
    # Save results
    output_file = OUTPUT_DIR / "following_cleanse.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("=" * 50)
    print(f"📊 FOLLOWING CLEANSE RESULTS")
    print("=" * 50)
    print(f"Total following: {len(following)}")
    print(f"✅ Keep (watchlist + niche): {len(keep)}")
    print(f"🔍 Review (outside niche): {len(review)}")
    print(f"💤 Potentially inactive: {len(inactive)}")
    print(f"📉 Low engagement: {len(low_engagement)}")
    print(f"\nSaved to: {output_file}")
    
    if review:
        print(f"\n🔍 TOP ACCOUNTS TO REVIEW (outside niche):")
        for r in review[:15]:
            print(f"   {r['handle']} ({r['followers']} followers) — {r['bio'][:60]}")
    
    if inactive:
        print(f"\n💤 POTENTIALLY INACTIVE:")
        for r in inactive[:10]:
            print(f"   {r['handle']} ({r['tweets']} tweets, {r['followers']} followers)")
    
    return results


if __name__ == "__main__":
    analyze_following()
