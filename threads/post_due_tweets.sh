#!/bin/bash
cd /data/.openclaw/workspace
python3 << 'PYEOF'
import json, tweepy
from pathlib import Path
from datetime import datetime, timezone

creds = {}
with open(".credentials") as f:
    for line in f:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            creds[k] = v

client = tweepy.Client(
    consumer_key=creds["X_CONSUMER_KEY"],
    consumer_secret=creds["X_CONSUMER_SECRET"],
    access_token=creds["X_ACCESS_TOKEN"],
    access_token_secret=creds["X_ACCESS_TOKEN_SECRET"]
)

queue_file = Path("agents/threads/cache/tweet_queue.json")
posted_file = Path("agents/threads/cache/posted_tweets.json")

q = json.load(open(queue_file))
posted = json.load(open(posted_file)) if posted_file.exists() else []

now = datetime.now(timezone.utc).isoformat()

for t in q["tweets"]:
    if t["status"] == "pending" and t["scheduled_for"] <= now:
        try:
            resp = client.create_tweet(text=t["text"])
            t["status"] = "posted"
            t["posted_at"] = now
            t["tweet_id"] = str(resp.data["id"])
            posted.append(t)
            print(f"POSTED: {t['text'][:60]}")
        except Exception as e:
            t["status"] = "error"
            t["error"] = str(e)

json.dump(q, open(queue_file, "w"), indent=2)
json.dump(posted, open(posted_file, "w"), indent=2)
PYEOF
