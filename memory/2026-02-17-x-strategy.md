# 2026-02-17 — X/Twitter Strategy Launch

## X Agent (Merged into Threads)
- **Agent ID:** `threads` (renamed to "X Agent" in config)
- **Workspace:** `/data/.openclaw/workspace/agents/threads/`
- **SOUL.md:** Expanded from thread-only to full X management (threads, tweets, replies, engagement, cross-posting)
- **Model:** Sonnet 4.6 (config), Sonnet 4.5 (actual spawns)

## Duncan's X Profile
- **Handle:** @DuncanRogoff (verified ✓, X Premium subscriber)
- **User ID:** 1372291578748837889
- **Stats (Feb 17):** 19.3K followers, 8,839 following
- **New Bio:** Ex - Apple, PlayStation, Nissan | AI agency founder | 110K followers in 12 months | Teaching 2,000+ to build an audience using AI 👇
- **Link:** skool.com/buildroom
- **Location:** San Francisco, CA

## Positioning (Stored Permanently)
- **Bio line:** 110K followers in 12 months. AI agency founder.
- **Offer:** More new leads + 1,500 followers + ALL my resources

## Pinned Thread — LIVE
- **Tweet 1 (hook):** https://x.com/DuncanRogoff/status/2023958488670470207
- 7 tweets total, narrative arc: hook → origin (Apple/PlayStation) → old world → shift (Claude 4.6) → proof → prompt pack → CTA
- CTA: Comment PROMPTS or skool.com/buildroom

## 3 Value Tweets — Written, Ready to Post
1. Cost optimization ($5/day, 90% reduction)
2. Traffic > conversion (110K by posting more)
3. Lead magnets in hours not weeks

## X API Access
- **Tier:** Free developer account + X Premium subscription
- **Can do:** get_me, create_tweet, delete_tweet (POSTING WORKS ✅)
- **Cannot do:** search, user lookup, timeline read, get_users_following (all return 401)
- **Workaround:** Web scraping for research, API for posting
- **Note:** Nitter/xcancel scraping also dead (503/empty responses) — need browser automation for engagement monitoring

## Files Created
- `agents/threads/X_WATCHLIST.md` — 30 accounts across 5 categories
- `agents/threads/X_ACTION_PLAN.md` — Full 3-phase strategy
- `agents/threads/engagement_monitor.py` — Scrapes watchlist (needs browser fix)
- `agents/threads/following_cleanse.py` — Analyzes following list (needs Basic API or data export)
- `agents/threads/repurpose_pipeline.py` — Cross-platform content conversion
- `agents/threads/fetch_remix_candidates.py` — Pulls high-performing tweets for remix
- `CREDENTIALS_INDEX.md` — Master reference for ALL credentials (never forget what we have access to)

## X Watchlist — 30 Accounts (5 Categories)
**AI Agents:** @AnthropicAI (engage EVERY launch), @alexalbert__, @nickscamara_, @RLanceMartin, @mattshumer_
**n8n/Automation:** @max_n8n, @nocodedevs, @zapier
**SaaS/Solopreneur:** @levelsio (2.8M, high visibility), @dannypostmaa, @marclouvion, @tdinh_me, @gregisenberg
**Creator Economy:** @dickiebush, @SahilBloom, @JamesClear, @AlexHormozi, @LeilaHormozi, @dankulture, @JustinWelsh
**AI Thought Leaders:** @swyx, @mattshumer_, @bindureddy

## X Action Plan — 3 Phases
**Phase 1 (This Week):** Bio ✅, Strategic follows, Pin Claude 4.6 thread ✅
**Phase 2 (Next Week):** Daily content cron (8am), Engagement monitor (3x daily: 9am/1pm/6pm), Content repurpose pipeline
**Phase 3 (Month 1):** DM automation ("AI"/"PROMPTS" triggers), Weekly analytics, Following cleanse

## Content Mix (Daily)
| Type | Frequency |
|------|-----------|
| Value bomb tweet | Daily |
| Hot take / proof point | 2-3x/week |
| Trend-jacked tweet | 2-3x/week |
| Remixed banger (from watchlist) | 2-3x/week |
| Thread | 1-2x/week |
| Proof screenshot | 2x/week |
| Engagement reply | Daily |
| AI chat/image/video (top of funnel) | TBD |

## Top-of-Funnel Content Inspiration
- Duncan shared @Whizz_ai post as example of broad-reach content
- AI chat screenshots, AI-generated images, AI video clips = high reach, low effort
- These feed the algorithm; threads and value tweets convert

## Following Cleanse
- 8,839 following is too high for 19.3K followers
- Target: ~2K following for better authority signal
- Need Duncan's X data export OR browser automation to analyze (API blocked)

## Key Decisions
- Merged X agent into existing threads agent (no unnecessary agent sprawl)
- Web scraping for research, API for posting
- Standalone xagent directory deleted
- CREDENTIALS_INDEX.md created as permanent reference — NEVER say "I don't have credentials" again
