#!/usr/bin/env python3
"""
Content Repurpose Pipeline
Takes a TikTok video URL, downloads it, uploads to temp host,
extracts transcript via Blotato, and returns data for posting.
"""

import json
import os
import re
import sys
import time
import requests
from pathlib import Path

BLOTATO_KEY = os.environ.get("BLOTATO_API_KEY", "")
MCP_URL = "https://mcp.blotato.com/mcp"
MCP_HEADERS = {
    "blotato-api-key": BLOTATO_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

# Blotato account IDs
ACCOUNTS = {
    "instagram": "571",
    "twitter": "906",
    "youtube": "323"
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

    resp = requests.post(MCP_URL, headers=MCP_HEADERS, json=payload, timeout=60)
    data = resp.json()

    if "error" in data:
        print(f"MCP error: {data['error']}")
        return None

    result = data.get("result", {})
    content = result.get("content", [])
    for item in content:
        if item.get("type") == "text":
            try:
                return json.loads(item["text"])
            except json.JSONDecodeError:
                return item["text"]
    return result


def extract_transcript(tiktok_url):
    """Use Blotato to extract TikTok transcript."""
    print(f"Extracting transcript from {tiktok_url}...")
    result = mcp_call("blotato_create_source", {
        "sourceType": "tiktok",
        "url": tiktok_url
    })

    if result and isinstance(result, dict):
        status = result.get("status", "")
        if status == "completed":
            return {
                "title": result.get("title", ""),
                "content": result.get("content", "")
            }
        elif status in ("queued", "processing"):
            source_id = result.get("id", "")
            if source_id:
                for _ in range(12):  # Max 2 min
                    time.sleep(10)
                    check = mcp_call("blotato_get_source_status", {"id": source_id})
                    if check and isinstance(check, dict):
                        if check.get("status") == "completed":
                            return {
                                "title": check.get("title", ""),
                                "content": check.get("content", "")
                            }
                        elif check.get("status") == "failed":
                            print(f"Source extraction failed: {check.get('error', 'unknown')}")
                            return None

    print(f"Transcript extraction failed: {result}")
    return None


def download_tiktok_video(tiktok_url):
    """Download TikTok video without watermark. Returns dict with content + description."""
    print(f"Downloading video from {tiktok_url}...")

    # Use a session to maintain cookies (required for video download)
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })

    # Step 1: Get the page HTML (session captures cookies)
    resp = session.get(tiktok_url, timeout=30, allow_redirects=True)

    if resp.status_code != 200:
        print(f"Failed to load TikTok page: {resp.status_code}")
        return None

    html = resp.text

    # Step 2: Extract video URL from rehydration data
    match = re.search(
        r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">([\s\S]*?)</script>',
        html
    )

    if not match:
        print("Could not find rehydration data")
        return None

    try:
        data = json.loads(match.group(1))
        item_struct = (data.get("__DEFAULT_SCOPE__", {})
                       .get("webapp.video-detail", {})
                       .get("itemInfo", {})
                       .get("itemStruct", {}))

        video_url = item_struct.get("video", {}).get("playAddr")
        description = item_struct.get("desc", "")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Failed to parse video data: {e}")
        return None

    if not video_url:
        print("Could not find video URL in page data")
        return None

    # Step 3: Download using the same session (cookies required)
    video_resp = session.get(video_url, timeout=120, headers={
        "Referer": "https://www.tiktok.com/",
        "Accept": "video/mp4,video/*;q=0.9,application/octet-stream;q=0.8",
    })

    if video_resp.status_code == 200 and len(video_resp.content) > 1000:
        print(f"Downloaded video: {len(video_resp.content)} bytes")
        return {"content": video_resp.content, "description": description}

    print(f"Video download failed: {video_resp.status_code}, size: {len(video_resp.content)}")
    return None


def upload_to_gdrive(video_bytes, filename):
    """Upload video to Google Shared Drive and return public download URL."""
    print(f"Uploading {filename} to Google Drive...")

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaInMemoryUpload

        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT = '/data/.openclaw/workspace/.secrets/google-service-account.json'
        SHARED_DRIVE_ID = '0ABeLw0N_x6XPUk9PVA'  # Blotato Repurpose shared drive

        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT, scopes=SCOPES)
        drive = build('drive', 'v3', credentials=creds)

        media = MediaInMemoryUpload(video_bytes, mimetype='video/mp4')
        file_meta = {
            'name': filename,
            'parents': [SHARED_DRIVE_ID]
        }

        f = drive.files().create(
            body=file_meta, media_body=media,
            fields='id,webContentLink',
            supportsAllDrives=True
        ).execute()

        file_id = f['id']

        # Make publicly accessible
        drive.permissions().create(
            fileId=file_id,
            body={'role': 'reader', 'type': 'anyone'},
            supportsAllDrives=True
        ).execute()

        download_url = f.get('webContentLink', f'https://drive.google.com/uc?export=download&id={file_id}')
        print(f"Uploaded to Drive: {download_url}")
        return download_url

    except Exception as e:
        print(f"Drive upload failed: {e}")
        print("Falling back to tmpfiles.org...")
        return upload_to_tmpfiles(video_bytes, filename)


def upload_to_tmpfiles(video_bytes, filename):
    """Fallback: Upload video to tmpfiles.org and return public direct download URL."""
    print(f"Uploading {filename} to tmpfiles.org...")

    resp = requests.post(
        "https://tmpfiles.org/api/v1/upload",
        files={"file": (filename, video_bytes, "video/mp4")},
        timeout=120
    )

    if resp.status_code == 200:
        data = resp.json()
        if data.get("status") == "success":
            url = data["data"]["url"]
            direct_url = url.replace("tmpfiles.org/", "tmpfiles.org/dl/").replace("http://", "https://")
            print(f"Uploaded: {direct_url}")
            return direct_url

    print(f"Upload failed: {resp.status_code} {resp.text[:200]}")
    return None


def post_to_platform(platform, account_id, text, media_url, extra_params=None):
    """Post to a platform via Blotato MCP."""
    print(f"Posting to {platform}...")

    params = {
        "accountId": account_id,
        "platform": platform,
        "text": text,
        "mediaUrls": [media_url] if media_url else []
    }

    if extra_params:
        params.update(extra_params)

    result = mcp_call("blotato_create_post", params)

    if result and isinstance(result, dict):
        status = result.get("status", "")
        if status in ("published", "scheduled"):
            print(f"  ✅ {platform}: {result.get('publicUrl', 'posted')}")
            return True
        elif status == "in-progress":
            sub_id = result.get("postSubmissionId", "")
            if sub_id:
                for _ in range(6):
                    time.sleep(10)
                    check = mcp_call("blotato_get_post_status", {"postSubmissionId": sub_id})
                    if check and isinstance(check, dict):
                        if check.get("status") == "published":
                            print(f"  ✅ {platform}: {check.get('publicUrl', 'posted')}")
                            return True
                        elif check.get("status") == "failed":
                            print(f"  ❌ {platform}: {check.get('errorMessage', 'failed')}")
                            return False

    print(f"  ❌ {platform}: {result}")
    return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: repurpose_video.py <tiktok_url> [day_number]")
        sys.exit(1)

    tiktok_url = sys.argv[1]
    day_num = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"\n{'='*60}")
    print(f"Content Repurpose Pipeline")
    print(f"TikTok URL: {tiktok_url}")
    print(f"{'='*60}\n")

    # Step 1: Extract transcript via Blotato
    transcript = extract_transcript(tiktok_url)

    # Step 2: Download video
    video_data = download_tiktok_video(tiktok_url)

    if not video_data:
        print("FAILED: Could not download video")
        sys.exit(1)

    # Step 3: Upload to temp host
    timestamp = int(time.time())
    public_url = upload_to_gdrive(video_data["content"], f"tiktok_{timestamp}.mp4")

    if not public_url:
        print("FAILED: Could not upload video to temp host")
        sys.exit(1)

    # Output for orchestrator
    output = {
        "tiktok_url": tiktok_url,
        "day_number": day_num,
        "description": video_data.get("description", ""),
        "transcript": transcript,
        "video_size_bytes": len(video_data["content"]),
        "public_url": public_url,
        "status": "ready_for_posting"
    }

    print(f"\n{json.dumps(output, indent=2, default=str)}")
