#!/usr/bin/env python3
"""
Fetch high-performing tweets from watchlist accounts for remix inspiration.
Uses X API v2 (Free tier: 10K requests/month).
Caches results to avoid burning rate limits.
"""

import os
import json
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

CREDENTIALS_FILE = "/data/.openclaw/workspace/.credentials"
CACHE_DIR = Path("/data/.openclaw/workspace/agents/threads/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Watchlist accounts — handles without @
WATCHLIST = [
    "AlexHormozi", "gregisenberg", "LinusEkenstam", "nickfloats",
    "mattshumer_", "SamParr", "JustinWelsh", "dankulkov",
    "AnthropicAI", "OpenAI"
]

# Minimum engagement threshold for remix candidates
MIN_LIKES = 500


def load_bearer_token():
    """Load X bearer token from credentials file."""
    with open(CREDENTIALS_FILE, "r") as f:
        for line in f:
            if line.startswith("X_BEARER_TOKEN="):
                token = line.strip().split("=", 1)[1]
                return urllib.parse.unquote(token)
    raise ValueError("X_BEARER_TOKEN not found in credentials")


def get_cache_path(handle):
    return CACHE_DIR / f"{handle}.json"


def is_cache_fresh(handle, max_age_hours=12):
    """Check if cached data is less than max_age_hours old."""
    cache_file = get_cache_path(handle)
    if not cache_file.exists():
        return False
    mtime = cache_file.stat().st_mtime
    age_hours = (time.time() - mtime) / 3600
    return age_hours < max_age_hours


def fetch_user_id(handle, bearer_token):
    """Get user ID from handle."""
    url = f"https://api.twitter.com/2/users/by/username/{handle}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {bearer_token}"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            return data.get("data", {}).get("id")
    except urllib.error.HTTPError as e:
        print(f"  ❌ Error fetching user ID for @{handle}: {e.code} {e.reason}")
        return None


def fetch_recent_tweets(user_id, handle, bearer_token, max_results=10):
    """Fetch recent tweets with engagement metrics."""
    # Get tweets from last 7 days
    since = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    params = urllib.parse.urlencode({
        "max_results": max_results,
        "start_time": since,
        "tweet.fields": "public_metrics,created_at,text",
        "exclude": "retweets,replies"
    })
    
    url = f"https://api.twitter.com/2/users/{user_id}/tweets?{params}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {bearer_token}"
    })
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            tweets = data.get("data", [])
            
            # Sort by engagement (likes + retweets)
            for t in tweets:
                m = t.get("public_metrics", {})
                t["_engagement"] = m.get("like_count", 0) + m.get("retweet_count", 0) * 2
            
            tweets.sort(key=lambda t: t["_engagement"], reverse=True)
            return tweets
    except urllib.error.HTTPError as e:
        print(f"  ❌ Error fetching tweets for @{handle}: {e.code} {e.reason}")
        return []


def save_cache(handle, tweets):
    cache_file = get_cache_path(handle)
    with open(cache_file, "w") as f:
        json.dump({
            "handle": handle,
            "fetched_at": datetime.utcnow().isoformat(),
            "tweets": tweets
        }, f, indent=2)


def load_cache(handle):
    cache_file = get_cache_path(handle)
    if cache_file.exists():
        with open(cache_file, "r") as f:
            return json.load(f)
    return None


def main():
    bearer_token = load_bearer_token()
    all_candidates = []
    api_calls = 0
    
    print(f"🔍 Scanning {len(WATCHLIST)} accounts for remix candidates...")
    print(f"   Min engagement threshold: {MIN_LIKES} likes")
    print()
    
    for handle in WATCHLIST:
        # Check cache first
        if is_cache_fresh(handle):
            print(f"  📦 @{handle} — using cached data")
            cached = load_cache(handle)
            tweets = cached.get("tweets", []) if cached else []
        else:
            print(f"  🌐 @{handle} — fetching fresh data...")
            user_id = fetch_user_id(handle, bearer_token)
            api_calls += 1
            
            if not user_id:
                continue
            
            tweets = fetch_recent_tweets(user_id, handle, bearer_token)
            api_calls += 1
            save_cache(handle, tweets)
            
            # Rate limit courtesy — 1 second between accounts
            time.sleep(1)
        
        # Filter for remix candidates
        for t in tweets:
            likes = t.get("public_metrics", {}).get("like_count", 0)
            if likes >= MIN_LIKES:
                all_candidates.append({
                    "handle": handle,
                    "text": t.get("text", ""),
                    "likes": likes,
                    "retweets": t.get("public_metrics", {}).get("retweet_count", 0),
                    "created_at": t.get("created_at", ""),
                    "tweet_id": t.get("id", ""),
                    "url": f"https://x.com/{handle}/status/{t.get('id', '')}"
                })
    
    # Sort all candidates by engagement
    all_candidates.sort(key=lambda t: t["likes"], reverse=True)
    
    # Save remix candidates
    output_file = CACHE_DIR / "remix_candidates.json"
    with open(output_file, "w") as f:
        json.dump({
            "generated_at": datetime.utcnow().isoformat(),
            "api_calls_used": api_calls,
            "total_candidates": len(all_candidates),
            "candidates": all_candidates
        }, f, indent=2)
    
    print(f"\n✅ Found {len(all_candidates)} remix candidates ({api_calls} API calls used)")
    print(f"   Saved to: {output_file}")
    
    # Print top 5
    if all_candidates:
        print(f"\n🏆 Top 5 remix candidates:")
        for i, c in enumerate(all_candidates[:5], 1):
            preview = c["text"][:100].replace("\n", " ")
            print(f"   {i}. @{c['handle']} ({c['likes']}❤️) — {preview}...")


if __name__ == "__main__":
    main()
