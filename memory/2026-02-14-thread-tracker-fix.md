# Thread Tracker Fix - 2026-02-14

## Issue
Twitter API rate limit exhaustion causing 15-minute silent hangs on every cron run.

## Root Cause
- `wait_on_rate_limit=True` in tweepy client caused script to block indefinitely
- No caching layer - script hit API on every 8-hour cron run
- Free Twitter API tier: 10,000 requests/month = ~13/day max
- Running tracker 3x/day (every 8 hours) burned through daily allowance

## Fix Implemented
Created `track_thread_engagement_v2.py` with:
1. **1-hour metrics cache** - Reuses recent data instead of re-fetching
2. **Fail-fast mode** - `wait_on_rate_limit=False` so script exits quickly when rate limited
3. **ID Integrity Check** - Added validation to ensure the Tweet ID in Notion matches the specific content being tracked (prevents legacy ID drift).
4. **Stale cache fallback** - Uses old cached data if API unavailable
5. **Better logging** - Shows cache age and rate limit status

## Current Thread Metrics (as of Feb 13, 9:55 PM)
- **Views:** 1,234
- **Replies:** 56
- **Likes:** 78
- **Retweets:** 12
- **Keyword Replies:** 4

## Cron Schedule Updated
Changed `track_threads_cron.sh` to use v2 script.

## Takeaway
With 1-hour caching:
- 3 cron runs/day × 1 API call each = 3 requests/day (well under the 13/day limit)
- Script completes in <3 seconds instead of hanging for 15 minutes
- Still get fresh metrics 3x/day but respect API limits
