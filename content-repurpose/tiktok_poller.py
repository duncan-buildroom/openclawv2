#!/usr/bin/env python3
"""
TikTok Content Repurpose Poller
Checks for new TikTok videos and triggers cross-posting pipeline.
Uses a state file to track already-processed videos (never post twice).
"""

import json
import os
import re
import sys
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import requests

# Paths
STATE_FILE = Path("/data/.openclaw/workspace/content-repurpose/.processed_videos.json")

# Duncan's TikTok profile
TIKTOK_PROFILE = "https://www.tiktok.com/@duncanrogoff"
TIKTOK_USERNAME = "duncanrogoff"


def load_state():
    """Load processed video state."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"processed": {}, "last_check": None}


def save_state(state):
    """Save processed video state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def scrape_tiktok_profile():
    """Scrape TikTok profile for video IDs (backup method)."""
    videos = []
    try:
        resp = requests.get(TIKTOK_PROFILE, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
        })
        if resp.status_code != 200:
            print(f"Profile scrape returned {resp.status_code}")
            return videos
        
        # Find video IDs in page
        vid_ids = re.findall(r'/video/(\d{15,})', resp.text)
        seen = set()
        for vid_id in vid_ids:
            if vid_id not in seen:
                seen.add(vid_id)
                videos.append({
                    "id": vid_id,
                    "url": f"https://www.tiktok.com/@{TIKTOK_USERNAME}/video/{vid_id}",
                    "title": "",
                    "published": ""
                })
    except Exception as e:
        print(f"Profile scrape failed: {e}")
    
    return videos


def check_for_new_videos():
    """Check TikTok profile for new videos. Returns list of unprocessed videos."""
    state = load_state()
    processed = state.get("processed", {})
    
    # Direct profile scrape only (RSS is too slow, 2-6hr delay)
    all_videos = {}
    
    profile_videos = scrape_tiktok_profile()
    for v in profile_videos:
        all_videos[v["id"]] = v
    
    # Filter to unprocessed only
    new_videos = []
    for vid_id, video in all_videos.items():
        if vid_id not in processed:
            new_videos.append(video)
    
    # Update last check time
    state["last_check"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    
    print(f"Found {len(all_videos)} total videos, {len(new_videos)} new")
    return new_videos


def mark_processed(video_id, platforms=None):
    """Mark a video as processed so it's never grabbed again."""
    state = load_state()
    state["processed"][video_id] = {
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "platforms": platforms or []
    }
    save_state(state)
    print(f"Marked {video_id} as processed")


def mark_existing_as_processed():
    """One-time: mark all currently visible videos as processed (don't repost old content)."""
    state = load_state()
    all_videos = {}
    
    profile_videos = scrape_tiktok_profile()
    for v in profile_videos:
        all_videos[v["id"]] = v
    
    for vid_id in all_videos:
        if vid_id not in state.get("processed", {}):
            state.setdefault("processed", {})[vid_id] = {
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "platforms": ["pre-existing"]
            }
    
    state["last_check"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    print(f"Marked {len(all_videos)} existing videos as processed")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "init":
            # First run: mark all existing videos so we don't repost
            mark_existing_as_processed()
        elif cmd == "check":
            # Normal poll: check for new videos
            new = check_for_new_videos()
            if new:
                for v in new:
                    print(json.dumps(v))
            else:
                print("No new videos")
        elif cmd == "mark":
            # Mark a specific video as done
            if len(sys.argv) > 2:
                mark_processed(sys.argv[2], sys.argv[3:] if len(sys.argv) > 3 else None)
        elif cmd == "status":
            state = load_state()
            print(f"Processed: {len(state.get('processed', {}))} videos")
            print(f"Last check: {state.get('last_check', 'never')}")
        elif cmd == "manual":
            # Manual trigger with a TikTok URL
            if len(sys.argv) > 2:
                url = sys.argv[2]
                vid_match = re.search(r'/video/(\d+)', url)
                vid_id = vid_match.group(1) if vid_match else hashlib.md5(url.encode()).hexdigest()
                state = load_state()
                if vid_id in state.get("processed", {}):
                    print(f"Video {vid_id} already processed!")
                else:
                    print(json.dumps({"id": vid_id, "url": url, "title": "", "published": ""}))
    else:
        print("Usage: tiktok_poller.py [init|check|mark|status|manual <url>]")
