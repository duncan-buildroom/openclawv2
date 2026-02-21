# Consolidated Memory — Feb 18-19, 2026 (Skool/X/Reddit)

## Skool Communities Intelligence

### Full Catalog (29 Communities)
**Posting Tiers (Duncan-approved):**

**Daily (Tier 1):**
- The Build Room (2,500 members, $97/mo)
- AI Automation Society (260.9K members, free) — Nate Herk, biggest audience, exact ICP
- Synthesizer (35.7K, free)
- AI Automations by Jack (1.9K, $77/mo)

**2-3x/week (Tier 2):**
- Maker School (2.1K, $184/mo) — Nick Saraev
- Business Builders Club (BBC)
- AIpreneurs (free)
- GOOSIFY
- Magnetic Memberships
- RoboNuggets (/robonuggets-free)

**1-2x/week (Tier 3):**
- AI Automation Mastery (/ai-automation-mastery-group)
- Chase AI Community
- Skoolers ($9/mo, active owner)
- YouTube Blueprint (1.5K, free, Dylan Reynolds active owner)

**Full list:** `SKOOL_COMMUNITIES.md` (29 total, 13 active posting)

### Skool Credentials
- **Email:** duncan@buildroom.ai
- **Password:** Banjo#1489!
- **Location:** `.credentials` file
- **Browser access:** Working via OpenClaw headless Chromium

### Build Room Categories & IDs
| Category | ID |
|----------|-----|
| Announcements | 0dc2fa4f55944dcd9efbc207099e842f |
| Daily Actions | f00f3745d23f43e2b503f1f4afa5846c |
| $1M Roadmap | c172a360b7934d549d4d41ac663d4546 |
| YouTube Videos | 92c67c8a670047479d7e53c6f183951e |
| Wins | 950a071599854c78829b2bea775fb983 |
| Hangout | 49170f0cbacb4883a5ae072fbbbcf3f1 |
| Check-Ins | 9e6ae46a07d349809094e6704ea5ea11 |
| Help! | 85eb27a944794ab3ac1cb67bab73229a |

### Skool Poll Automation (Technical)
**Critical discovery:** Skool's React category dropdown doesn't work with normal DOM clicks.

**Solution:** Access React fiber internals:
1. Find "Select a category" button
2. Get `__reactFiber$` key from element
3. Walk fiber tree to find `memoizedProps.options`
4. Call `options[INDEX].onClick()` directly

**Category index map (Build Room):**
- 0=Announcements, 1=Daily Actions, 2=$1M Roadmap, 3=YouTube Videos, 4=Wins, 5=Hangout, 6=Check-Ins, 7=Help!

**Files:** `agents/skoolposts/skool_post.py` (reusable JS snippets)

### Skool Classroom Formatting Rules
**Line Break Protocol:** Every sentence = separate paragraph (`<p>` tag) for natural spacing

**Resource Management:**
- NEVER inline links or raw URLs in body text
- ALWAYS use Skool's "Resource Link" section at bottom of module
- Add via: ADD → Resource Link → title + URL

**Positioning shift:**
- From "ChatGPT prompts" (manual chat) → "Agent Prompts" (systemic automation)
- Frame as "System Prompts" or "Logic Engines" for agents
- Goal: execution + tool use + distribution, not just chat

**Reference:** `agents/roadto1m/CLASSROOM_GUIDE.md`

---

## X/Twitter Strategy (Active)

### Voice Rules (Duncan-approved — CRITICAL)
**Tweet voice:**
- Documenting > teaching
- First person, concrete details (say "Claude Opus" not "expensive model")
- Every tweet needs a HOOK ("This one shift 10x'd my growth")
- **NEVER post back-to-back** — always use tweet_scheduler.py with 2-4hr random gaps
- ❌ MISTAKE (Feb 18): Posted 3 tweets back-to-back. Duncan called it out. Never again.

**Engagement reply voice:**
- **Max 35 words**, single paragraph, no line breaks, no em dashes
- 6th grade reading level, coffee-with-a-peer tone
- Dig at real tension, not surface-level. Be concrete.
- Auto-posted, NO approval needed
- **3 windows:** 9am/1pm/6pm, 7 replies each, rotated across different creators
- **Daily summary at 6pm** (show Duncan what was posted)

### Profile (Finalized)
- **Handle:** @DuncanRogoff (verified ✓, X Premium)
- **User ID:** 1372291578748837889
- **Bio:** Ex - Apple, PlayStation, Nissan | AI agency founder | 110K followers in 12 months | Teaching 2,000+ to build an audience using AI 👇
- **Link:** skool.com/buildroom

### API Access
- **Tier:** Free developer + X Premium
- **Can do:** get_me, create_tweet, delete_tweet (posting works ✅)
- **Cannot do:** search, user lookup, timeline read (all 401)
- **Workaround:** Web scraping for research, API for posting

### Files
- `agents/threads/X_WATCHLIST.md` — 30 accounts across 5 categories
- `agents/threads/X_ACTION_PLAN.md` — 3-phase strategy
- `agents/threads/tweet_scheduler.py` — queue system, 2-4hr gaps, max 5/day
- `agents/threads/engagement_monitor.py` — watchlist scraper
- `agents/threads/following_cleanse.py` — following analysis
- `agents/threads/repurpose_pipeline.py` — cross-platform content
- `agents/threads/fetch_remix_candidates.py` — high-performing tweet finder

### Pinned Thread (LIVE)
- https://x.com/DuncanRogoff/status/2023958488670470207
- 7 tweets, Claude 4.6 Prompt Pack narrative arc

---

## Reddit Strategy (Deployed)

### Reddit Agent
- **Agent ID:** `reddit`
- **Workspace:** `/data/.openclaw/workspace/agents/reddit/`
- **Model:** Sonnet 4.6 (config) / 4.5 (actual)
- **Scanner:** reddit_scanner.py (uses Reddit public JSON API, zero cost, no auth for reading)

### Voice Rules (Different from X)
**Reddit voice:**
- **Longer replies:** 3-5 sentences, match thread energy
- Casual, lowercase ok, contractions encouraged
- Words: "honestly", "ngl", "tbh"
- **ANTI-AI DETECTION:**
  - NO "Great question!"
  - NO bullet points
  - NO structured formatting
- Never mention Build Room, Skool, or any product
- Quality gate: helpful + specific + human + not promotional

**Approval workflow:**
- First 2 weeks: Duncan reviews all replies
- After 2 weeks: Autonomous posting
- Max 3 replies per subreddit per day

### Credentials (LIVE)
- **Username:** Drogoff1489
- **Password:** ScMdvC^B^BcWc5
- **Client ID:** Og4ajvv5eBbSZCgTEhMyQQ
- **Client Secret:** DfY_FM8gNyNU63CYD_pCjK8Fty-RuA
- **User Agent:** openclaw:v1.0 (by /u/Drogoff1489)
- **Karma:** 1,706 link / 159 comment
- **Status:** Auth tested ✅, using praw library
- **Location:** `.credentials` file

### Target Subreddits
**High priority:** r/ClaudeAI, r/ChatGPT, r/n8n, r/automation

**Medium priority:** r/SaaS, r/NoCode, r/Entrepreneur, r/smallbusiness, r/ArtificialIntelligence

**Low priority:** r/Skool, r/solopreneur, r/openclaw

**Full list:** `agents/reddit/SUBREDDIT_WATCHLIST.md`

### Duncan's Top Reddit Posts (Reference)
- r/n8n "10 things I wish I knew": 833 upvotes, 144 comments (BEST)
- r/n8n "Clone ANY TikTok Video": 177 upvotes
- r/SaaS "I turned my n8n automation into a micro-saas": 45 upvotes
- **Saved in:** `agents/reddit/DUNCAN_TOP_POSTS.md`

---

## Road to $1M Series (Finalized)

### Core Structure
**Series concept:** "Day X of building a $1M personal brand with AI"

**Tagline:** "Gatekeeping nothing to $1M"

**Series thesis:** "Documenting everything AND giving you everything so you can do it too" (teaching + documenting, not just documenting)

**Goal:** $1M total revenue earned, no deadline

**Video skeleton (every video):**
1. Hook: "Day X of building a $1M personal brand with AI"
2. Giveaway: "Today I'm giving you [specific asset]" (IMMEDIATELY after hook)
3. Content: one idea, 30-60 seconds
4. Close: "This is in the Build Room. Along with everything else I've already built."

**Content buckets:** Build, Lesson, Giveaway, Growth, Money (rotating)

**Satellite series:** Money Check-ins, Follower Check-ins, Quick Tips (separate videos, no Day X hook)

### Duncan's Starting Numbers (Feb 2026)
- Skool low ticket: $11,760/mo
- Skool coaching: $4,899/mo
- YouTube AdSense: $2,500/mo
- Agency: $8K/mo (1 client, 2 months left)
- Sponsorships: $9K from 2 videos (lumpy)
- **Total: ~$27-31K/mo (~$325-375K annualized)**

### Milestones Upcoming
- YouTube: 50K → 100K
- TikTok: 75K → 100K
- X: 20K
- LinkedIn: 10K
- Build Room: 3K members

### Files
- **Agent:** `roadto1m` (Sonnet 4.6)
- **Workspace:** `/data/.openclaw/workspace/agents/roadto1m/`
- **Content Calendar:** `agents/roadto1m/CONTENT_CALENDAR.md` (30 days)
- **$1M Roadmap Notion:** `30bf259c-0f17-8169-9a8b-d9210570b1e3`
- **Content Strategy Notion:** `30bf259c-0f17-8133-9bec-e8901e2d3b93`

---

## CTA Strategy (Clarified Feb 18-19)

**Two-tier system:**

**Conversion platforms (X, YouTube, LinkedIn, Notion):**
- CTA: "The Build Room, link in bio" (ONE destination)
- Direct link to skool.com/buildroom

**Discovery platforms (TikTok, Instagram):**
- CTA: "Comment AI" triggers ManyChat → GHL funnel → email capture → 30 Automations access
- Passive funnel on old posts continues running
- NO new "comment AI" CTAs in new content (shifted to Build Room CTA)

**Key line:** "Whatever I build, you get it. Inside The Build Room. Along with everything else I've already built."

**Pricing clarity:** Build Room is $97/mo, NOT free. Never say "every asset is free."

---

## Cron Jobs (Complete Catalog)

| ID | Name | Schedule | Type |
|----|------|----------|------|
| 77a35d5a | last30days Research | 2am daily | isolated |
| c96ecd79 | Morning Briefing | 7am daily | isolated |
| bf23d020 | X Daily Content | 7:30am daily | isolated |
| 77d52982 | Daily Skool Posts | 8am daily | isolated |
| d55ff758 | Reddit Engagement | 8am daily | isolated |
| 408d839a | Daily LinkedIn Post | 8:30am daily | isolated |
| 8bc73619 | X Engagement 9am | 9am daily | isolated |
| ee3bf1ac | X Engagement 1pm | 1pm daily | isolated |
| d1ad38fe | X Engagement 6pm | 6pm daily | isolated |
| aa54d56c | Road to $1M Check-in | 6pm PST/9pm EST | main |
| 72bcaf09 | Midnight Tracker | midnight | main |
| 75d54d9e | Tweet Queue | every 30 min | main |
| ca019968 | Thread Engagement | every 8hrs | main |
| 5ed8e64f | GitHub Backup | midnight | main |
| 9e4fb5b4 | Weekly Trends | Sun 11pm | main |

---

## Known Issues (Feb 19)

**X Engagement crons:** Morning/midday windows fail (browser timeout), evening works. Pattern suggests browser service availability issue.

**Blotato API:** Still returning 401 after reconnect. Using tweepy + tweet_scheduler.py as fallback.

**Reddit posting:** Started March 3 after 2-week karma build period.

---

## What Was Dropped (Ephemeral)

- Daily cron execution logs (Feb 18-19)
- Individual carousel generation details (006)
- Specific tweet URLs (except pinned thread)
- Test post batches
- Awaiting approval items
- Transient browser/API failures
- "Pending" task lists
