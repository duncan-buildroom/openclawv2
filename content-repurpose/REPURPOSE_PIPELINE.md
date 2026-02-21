# Content Repurpose Pipeline

## Overview

Automatically cross-posts Duncan's TikTok videos to Instagram Reels, YouTube Shorts, and X with platform-native captions.

## How It Works

1. **Detection:** Cron polls Duncan's TikTok profile every 15 min via direct page scrape (no RSS, too slow)
2. **Dedup:** State file tracks every processed video ID. Never posts a video twice.
3. **Download:** Scrapes TikTok page for direct video URL (no watermark), downloads binary
4. **Upload:** Uploads video to tmpfiles.org (free, public URLs, no auth needed)
5. **Transcript:** Blotato MCP extracts transcript from TikTok URL
6. **Captions:** Agent generates platform-native captions (YouTube title + description, IG caption, X post)
7. **Publish:** Blotato MCP posts to all 3 platforms
8. **Mark done:** Video ID saved to state file
9. **Notify:** Summary sent to Duncan via Telegram

## Manual Trigger

Duncan can say "posted a TikTok" with the URL for immediate processing (no waiting for poll).

Or run directly:
```bash
python3 /data/.openclaw/workspace/content-repurpose/tiktok_poller.py manual <tiktok_url>
python3 /data/.openclaw/workspace/content-repurpose/repurpose_video.py <tiktok_url>
```

## Files

| File | Purpose |
|------|---------|
| `tiktok_poller.py` | Detects new videos via profile scrape, manages dedup state |
| `repurpose_video.py` | Downloads video, uploads to temp host, extracts transcript |
| `.processed_videos.json` | State file tracking all processed video IDs |

## Blotato MCP

- **Endpoint:** `https://mcp.blotato.com/mcp`
- **Auth:** `blotato-api-key: $BLOTATO_API_KEY`
- **Accept header:** `application/json, text/event-stream`
- **Key methods:**
  - `blotato_create_source` — extract transcript from TikTok URL
  - `blotato_create_post` — publish to any platform
  - `blotato_get_post_status` — poll for publish confirmation

## Blotato Account IDs

| Platform | Account ID | Username |
|----------|-----------|----------|
| Instagram | 571 | duncanrogoff |
| Twitter/X | 906 | DuncanRogoff |
| YouTube | 323 | Duncan Rogoff (AI Automation) |
| LinkedIn | 654 | Duncan Rogoff (personal profile) |

## Video Hosting

Videos are uploaded to Duncan's **Google Shared Drive** ("Blotato Repurpose"). Blotato downloads from the public share link during publishing. All videos stay in Duncan's Drive permanently.

- **Shared Drive ID:** `0ABeLw0N_x6XPUk9PVA` (Blotato Repurpose)
- **Service Account:** `linkedin-agent@ai-news-434806.iam.gserviceaccount.com`
- **Credentials:** `/data/.openclaw/workspace/.secrets/google-service-account.json`
- **Download URL format:** `https://drive.google.com/uc?export=download&id={file_id}`
- Files are made publicly readable so Blotato can access them

Note: Service accounts cannot upload to regular "My Drive" folders (no storage quota). Must use Shared Drives. The "Blotato Repurpose" Shared Drive was created for this purpose.

## Caption Rules

### YouTube Shorts
- **Title:** "Day [X] of building a $1M personal brand with AI | [topic]" (under 100 chars)
- **Description:** SEO-optimized, lead with series hook, relevant keywords
- **Settings:** privacyStatus: public, shouldNotifySubscribers: true

### Instagram Reels
- **Caption:** Lead with "Day [X] of building a $1M personal brand with AI." + 2-3 punchy lines + 3-5 hashtags
- **Settings:** mediaType: reel

### X / Twitter
- **Text:** Short documenting voice, max 280 chars including CTA
- **Settings:** none special

### All Platforms
- CTA: "The Build Room, link in bio." Always. One destination.
- No "comment AI" CTAs, ever
- No em dashes, use commas
- Each platform gets NATIVE copy, not the same text
- Detect day number from TikTok description/transcript

## Agent

- **ID:** `repurpose`
- **Model:** Gemini Flash (no heavy writing)
- **Workspace:** `/data/.openclaw/workspace/agents/repurpose/`
- **Cron ID:** `f6dd3a95-55b4-43ab-b2dc-4b2ada7a29e4` (every 15 min)

## State File Format

```json
{
  "processed": {
    "7285188871796491294": {
      "processed_at": "2026-02-18T21:54:30Z",
      "platforms": ["pre-existing"]
    }
  },
  "last_check": "2026-02-18T21:54:30Z"
}
```

## Troubleshooting

- **Video download fails:** TikTok page scraping can be flaky. The rehydration data format may change. Check `repurpose_video.py` download logic.
- **Blotato 401:** API key may have rotated. Check Duncan's Blotato dashboard for fresh key. MCP endpoint (`mcp.blotato.com`) uses same key as REST API.
- **Duplicate post concern:** State file is the single source of truth. If unsure, run `python3 tiktok_poller.py status` to check processed count.
- **tmpfiles.org down:** Fallback: upload to any public file host and pass URL to Blotato.
