#!/usr/bin/env python3
"""
Reddit Scanner , Finds engagement opportunities across target subreddits.
Uses Reddit's public JSON API (no auth needed for reading).
"""

import json
import urllib.request
import urllib.error
import html
import time
from datetime import datetime, timezone
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Subreddits by priority
HIGH_PRIORITY = ["ClaudeAI", "ChatGPT", "n8n", "automation"]
MEDIUM_PRIORITY = ["SaaS", "NoCode", "Entrepreneur", "smallbusiness", "ArtificialIntelligence"]
LOW_PRIORITY = ["Skool", "solopreneur", "openclaw", "content_marketing"]

# Keywords that signal Duncan can add value
RELEVANCE_KEYWORDS = [
    "ai agent", "automation", "claude", "n8n", "make.com", "zapier",
    "content system", "lead magnet", "audience", "followers", "growth",
    "solopreneur", "agency", "freelance", "no code", "nocode",
    "prompt", "workflow", "skool", "community", "saas", "micro-saas",
    "openclaw", "build in public", "solo founder", "quit my job",
    "corporate to", "side project", "digital product", "template",
    "how do you", "what tool", "struggling with", "is it worth",
    "show your setup", "tech stack", "how much do you spend",
]

USER_AGENT = "Mozilla/5.0 (compatible; BuildRoomBot/1.0)"


def fetch_subreddit_posts(subreddit, sort="hot", limit=25):
    """Fetch posts from a subreddit using public JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        posts = []
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            posts.append({
                "subreddit": subreddit,
                "title": html.unescape(post.get("title", "")),
                "selftext": html.unescape(post.get("selftext", ""))[:500],
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "created_utc": post.get("created_utc", 0),
                "author": post.get("author", ""),
                "id": post.get("id", ""),
            })
        
        return posts
    
    except Exception as e:
        print(f"  ❌ r/{subreddit}: {e}")
        return []


def score_relevance(post):
    """Score how relevant a post is to Duncan's expertise."""
    text = f"{post['title']} {post['selftext']}".lower()
    
    score = 0
    matched_keywords = []
    
    for kw in RELEVANCE_KEYWORDS:
        if kw in text:
            score += 1
            matched_keywords.append(kw)
    
    # Bonus for questions (high engagement opportunity)
    if "?" in post["title"]:
        score += 2
    
    # Bonus for post engagement
    if post["score"] >= 50:
        score += 2
    elif post["score"] >= 20:
        score += 1
    
    if post["num_comments"] >= 20:
        score += 1
    
    post["relevance_score"] = score
    post["matched_keywords"] = matched_keywords
    
    return score


def scan_all_subreddits(priorities=None):
    """Scan all target subreddits and return ranked opportunities."""
    if priorities is None:
        priorities = ["high", "medium"]
    
    subreddits = []
    if "high" in priorities:
        subreddits.extend(HIGH_PRIORITY)
    if "medium" in priorities:
        subreddits.extend(MEDIUM_PRIORITY)
    if "low" in priorities:
        subreddits.extend(LOW_PRIORITY)
    
    all_posts = []
    
    print(f"🔍 Scanning {len(subreddits)} subreddits...")
    
    for sub in subreddits:
        print(f"  📋 r/{sub}...")
        posts = fetch_subreddit_posts(sub)
        
        for post in posts:
            relevance = score_relevance(post)
            if relevance >= 2:  # Minimum relevance threshold
                all_posts.append(post)
        
        time.sleep(1)  # Rate limit courtesy
    
    # Sort by relevance score
    all_posts.sort(key=lambda p: p["relevance_score"], reverse=True)
    
    # Save results
    output = {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "subreddits_scanned": len(subreddits),
        "opportunities_found": len(all_posts),
        "posts": all_posts[:30]  # Top 30
    }
    
    output_file = CACHE_DIR / f"reddit_scan_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    # Also save as latest
    latest_file = CACHE_DIR / "reddit_latest.json"
    with open(latest_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Found {len(all_posts)} engagement opportunities")
    print(f"   Saved to: {output_file}")
    
    return all_posts


def print_top_opportunities(posts, n=10):
    """Print the top engagement opportunities."""
    print(f"\n🏆 Top {n} engagement opportunities:\n")
    for i, post in enumerate(posts[:n], 1):
        print(f"  {i}. r/{post['subreddit']} (score: {post['score']}, relevance: {post['relevance_score']})")
        print(f"     {post['title'][:80]}")
        print(f"     Keywords: {', '.join(post['matched_keywords'][:5])}")
        print(f"     {post['url']}")
        print()


if __name__ == "__main__":
    import sys
    
    priorities = ["high", "medium"]
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            priorities = ["high", "medium", "low"]
        elif sys.argv[1] == "high":
            priorities = ["high"]
    
    posts = scan_all_subreddits(priorities)
    print_top_opportunities(posts)
