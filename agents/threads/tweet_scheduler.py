#!/usr/bin/env python3
"""
Tweet Scheduler — Posts tweets from a queue at randomized intervals.
Never posts back-to-back. Minimum 2 hours between tweets.

Queue file: agents/threads/cache/tweet_queue.json
Posted log: agents/threads/cache/posted_tweets.json
"""

import json
import random
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import tweepy
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "tweepy", "--break-system-packages", "-q"])
    import tweepy

CREDENTIALS_FILE = "/data/.openclaw/workspace/.credentials"
CACHE_DIR = Path(__file__).parent / "cache"
QUEUE_FILE = CACHE_DIR / "tweet_queue.json"
POSTED_FILE = CACHE_DIR / "posted_tweets.json"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Scheduling config
MIN_GAP_HOURS = 2
MAX_GAP_HOURS = 4
DAILY_TWEET_LIMIT = 5  # Max tweets per day (excluding threads)


def load_credentials():
    creds = {}
    with open(CREDENTIALS_FILE) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                creds[k] = v
    return creds


def get_client():
    creds = load_credentials()
    return tweepy.Client(
        consumer_key=creds['X_CONSUMER_KEY'],
        consumer_secret=creds['X_CONSUMER_SECRET'],
        access_token=creds['X_ACCESS_TOKEN'],
        access_token_secret=creds['X_ACCESS_TOKEN_SECRET'],
        wait_on_rate_limit=False
    )


def load_queue():
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE) as f:
            return json.load(f)
    return {"tweets": []}


def save_queue(queue):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)


def load_posted():
    if POSTED_FILE.exists():
        with open(POSTED_FILE) as f:
            return json.load(f)
    return {"tweets": []}


def save_posted(posted):
    with open(POSTED_FILE, "w") as f:
        json.dump(posted, f, indent=2)


def add_to_queue(text, scheduled_for=None):
    """Add a tweet to the queue with optional scheduled time."""
    queue = load_queue()
    
    tweet_entry = {
        "text": text,
        "char_count": len(text),
        "queued_at": datetime.now(timezone.utc).isoformat(),
        "scheduled_for": scheduled_for,
        "status": "pending"
    }
    
    queue["tweets"].append(tweet_entry)
    save_queue(queue)
    print(f"✅ Queued: {text[:60]}... ({len(text)} chars)")
    return tweet_entry


def get_last_post_time():
    """Get the timestamp of the last posted tweet."""
    posted = load_posted()
    if posted["tweets"]:
        last = posted["tweets"][-1]
        return datetime.fromisoformat(last["posted_at"])
    return None


def get_today_post_count():
    """Count tweets posted today."""
    posted = load_posted()
    today = datetime.now(timezone.utc).date()
    count = 0
    for t in posted["tweets"]:
        post_date = datetime.fromisoformat(t["posted_at"]).date()
        if post_date == today:
            count += 1
    return count


def post_next():
    """Post the next tweet in queue if enough time has passed."""
    queue = load_queue()
    pending = [t for t in queue["tweets"] if t["status"] == "pending"]
    
    if not pending:
        print("📭 Queue empty.")
        return None
    
    # Check gap since last post
    last_time = get_last_post_time()
    now = datetime.now(timezone.utc)
    
    if last_time:
        gap = (now - last_time).total_seconds() / 3600
        if gap < MIN_GAP_HOURS:
            remaining = MIN_GAP_HOURS - gap
            print(f"⏳ Too soon. {remaining:.1f} hours until next post allowed.")
            return None
    
    # Check daily limit
    today_count = get_today_post_count()
    if today_count >= DAILY_TWEET_LIMIT:
        print(f"🛑 Daily limit reached ({today_count}/{DAILY_TWEET_LIMIT})")
        return None
    
    # Post the first pending tweet
    tweet = pending[0]
    client = get_client()
    
    try:
        response = client.create_tweet(text=tweet["text"])
        tweet_id = response.data["id"]
        tweet_url = f"https://x.com/DuncanRogoff/status/{tweet_id}"
        
        # Update queue
        tweet["status"] = "posted"
        tweet["tweet_id"] = tweet_id
        tweet["posted_at"] = now.isoformat()
        save_queue(queue)
        
        # Log to posted file
        posted = load_posted()
        posted["tweets"].append({
            "text": tweet["text"],
            "tweet_id": tweet_id,
            "url": tweet_url,
            "posted_at": now.isoformat()
        })
        save_posted(posted)
        
        print(f"✅ Posted: {tweet_url}")
        print(f"   {tweet['text'][:80]}...")
        return tweet_url
        
    except Exception as e:
        print(f"❌ Failed to post: {e}")
        tweet["status"] = "failed"
        tweet["error"] = str(e)
        save_queue(queue)
        return None


def schedule_batch(tweets, start_hour=8, end_hour=20):
    """Schedule a batch of tweets with random intervals between start and end hours EST."""
    now = datetime.now(timezone.utc)
    
    # Generate random times within the window
    for i, text in enumerate(tweets):
        # Random hour offset
        random_offset = random.uniform(
            MIN_GAP_HOURS * i,
            MIN_GAP_HOURS * i + MAX_GAP_HOURS
        )
        scheduled = now + timedelta(hours=random_offset)
        add_to_queue(text, scheduled_for=scheduled.isoformat())
    
    print(f"\n📅 Scheduled {len(tweets)} tweets with {MIN_GAP_HOURS}-{MAX_GAP_HOURS}hr gaps")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "post":
            post_next()
        elif sys.argv[1] == "queue":
            queue = load_queue()
            pending = [t for t in queue["tweets"] if t["status"] == "pending"]
            print(f"📋 {len(pending)} tweets in queue:")
            for t in pending:
                print(f"  - {t['text'][:80]}...")
        elif sys.argv[1] == "status":
            today_count = get_today_post_count()
            last_time = get_last_post_time()
            queue = load_queue()
            pending = [t for t in queue["tweets"] if t["status"] == "pending"]
            print(f"📊 Today: {today_count}/{DAILY_TWEET_LIMIT} posted")
            print(f"📋 Queue: {len(pending)} pending")
            if last_time:
                gap = (datetime.now(timezone.utc) - last_time).total_seconds() / 3600
                print(f"⏰ Last post: {gap:.1f}hr ago")
    else:
        print("Usage: tweet_scheduler.py [post|queue|status]")
        print("  post   - Post next tweet from queue (if gap allows)")
        print("  queue  - Show pending tweets")
        print("  status - Show posting stats")
