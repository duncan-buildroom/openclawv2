#!/usr/bin/env python3
"""Post video to all platforms via Blotato MCP."""

import json
import os
import sys
import time
import requests

BLOTATO_KEY = os.environ.get("BLOTATO_API_KEY", "")
MCP_URL = "https://mcp.blotato.com/mcp"
MCP_HEADERS = {
    "blotato-api-key": BLOTATO_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

ACCOUNTS = {
    "instagram": "571",
    "twitter": "906",
    "youtube": "323",
    "linkedin": "654"
}


def mcp_call(method, params=None):
    """Make an MCP JSON-RPC call to Blotato."""
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": int(time.time() * 1000),
        "params": {
            "name": method,
            "arguments": params or {}
        }
    }

    resp = requests.post(MCP_URL, headers=MCP_HEADERS, json=payload, timeout=120)
    data = resp.json()

    if "error" in data:
        return {"error": data["error"]}

    result = data.get("result", {})
    content = result.get("content", [])
    for item in content:
        if item.get("type") == "text":
            try:
                return json.loads(item["text"])
            except json.JSONDecodeError:
                return {"text": item["text"]}
    return result


def post_to_platform(platform, account_id, text, media_url, extra_params=None):
    """Post to a platform via Blotato MCP."""
    print(f"\nPosting to {platform}...")

    params = {
        "accountId": account_id,
        "platform": platform,
        "text": text,
        "mediaUrls": [media_url] if media_url else []
    }

    if extra_params:
        params.update(extra_params)

    result = mcp_call("blotato_create_post", params)

    if isinstance(result, dict):
        if "error" in result:
            print(f"  ❌ {platform}: {result['error']}")
            return {"status": "failed", "platform": platform, "error": result['error']}
        
        status = result.get("status", "")
        if status in ("published", "scheduled"):
            url = result.get("publicUrl", "posted")
            print(f"  ✅ {platform}: {url}")
            return {"status": "success", "platform": platform, "url": url}
        elif status == "in-progress":
            sub_id = result.get("postSubmissionId", "")
            if sub_id:
                print(f"  ⏳ {platform}: processing (submission {sub_id})...")
                for i in range(12):  # Max 2 min
                    time.sleep(10)
                    check = mcp_call("blotato_get_post_status", {"postSubmissionId": sub_id})
                    if isinstance(check, dict):
                        check_status = check.get("status", "")
                        if check_status == "published":
                            url = check.get("publicUrl", "posted")
                            print(f"  ✅ {platform}: {url}")
                            return {"status": "success", "platform": platform, "url": url}
                        elif check_status == "failed":
                            error = check.get("errorMessage", "unknown error")
                            print(f"  ❌ {platform}: {error}")
                            return {"status": "failed", "platform": platform, "error": error}
                
                print(f"  ⏰ {platform}: timeout waiting for publish")
                return {"status": "timeout", "platform": platform}

    print(f"  ❌ {platform}: unexpected response {result}")
    return {"status": "failed", "platform": platform, "error": str(result)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: post_to_platforms.py <video_url>")
        sys.exit(1)

    video_url = sys.argv[1]
    day_number = sys.argv[2] if len(sys.argv) > 2 else "3"

    # Platform-native captions
    captions = {
        "youtube": {
            "title": f"Day {day_number} of building a $1M personal brand with AI | Clone creator content",
            "description": f"""Day {day_number} of building a $1M personal brand with AI.

You can clone any creator's best content packaging in 60 seconds.

Here's what it does:
• Plug in YouTube channel IDs of creators you follow
• Pulls every video they've posted
• Rewrites their best performing titles for your niche
• Upload your face photo
• Swaps you into their proven viral thumbnail layouts

You're not guessing what works anymore. You're taking what already works and making it yours.

The full app is in The Build Room. Master prompt + complete code files. Whatever I build, you get.

#AIAutomation #PersonalBrand #ContentCreation #YouTubeGrowth #AITools

The Build Room, link in bio."""
        },
        "instagram": {
            "text": f"""Day {day_number} of building a $1M personal brand with AI.

Clone any creator's best titles and thumbnails in 60 seconds. Plug in their YouTube, select videos to remix, get viral titles + thumbnail swaps with your face.

No more guessing. Just take what works and make it yours.

#AI #PersonalBrand #ContentCreation #Automation #CreatorEconomy

The Build Room, link in bio."""
        },
        "twitter": {
            "text": f"""Day {day_number}. Clone any creator's best content packaging in 60 seconds. Titles + thumbnails, rewritten for your niche, with your face.

The Build Room, link in bio."""
        },
        "linkedin": {
            "text": f"""Day {day_number} of documenting the path to $1M personal brand with AI.

Today I'm giving you an app that clones any creator's best content packaging in 60 seconds.

Here's what it does:

You plug in the YouTube channel IDs of creators you follow. It pulls every video they've ever posted. Then it rewrites their best performing titles for your niche.

But here's where it gets interesting: you upload a photo of your face and it swaps you into their thumbnail layouts. Their proven, viral thumbnail layouts—with your face.

You're not guessing what works anymore. You're just taking what already works and making it yours.

Inside The Build Room, you get the master prompt to build this instantly, plus all the code files. Everything I build, you get.

The Build Room, link in bio."""
        }
    }

    results = []

    # YouTube Shorts
    yt_result = post_to_platform(
        "youtube",
        ACCOUNTS["youtube"],
        captions["youtube"]["description"],
        video_url,
        {
            "title": captions["youtube"]["title"],
            "privacyStatus": "public",
            "shouldNotifySubscribers": True
        }
    )
    results.append(yt_result)
    time.sleep(2)

    # Instagram Reels
    ig_result = post_to_platform(
        "instagram",
        ACCOUNTS["instagram"],
        captions["instagram"]["text"],
        video_url,
        {"mediaType": "reel"}
    )
    results.append(ig_result)
    time.sleep(2)

    # Twitter/X
    x_result = post_to_platform(
        "twitter",
        ACCOUNTS["twitter"],
        captions["twitter"]["text"],
        video_url
    )
    results.append(x_result)
    time.sleep(2)

    # LinkedIn
    li_result = post_to_platform(
        "linkedin",
        ACCOUNTS["linkedin"],
        captions["linkedin"]["text"],
        video_url
    )
    results.append(li_result)

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for r in results:
        status_icon = "✅" if r["status"] == "success" else "❌"
        print(f"{status_icon} {r['platform'].upper()}: {r.get('url', r.get('error', r['status']))}")

    print(json.dumps(results, indent=2))
