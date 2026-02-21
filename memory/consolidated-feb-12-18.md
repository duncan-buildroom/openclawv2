# Consolidated Memory — Feb 12-18, 2026

## Permanent Patterns & Infrastructure

### Model Hierarchy (Established)
- **Default:** Gemini 3 Flash Preview ($0.075/$0.30 per 1M tokens) — 90% cost savings
- **Content/writing:** Claude Sonnet 4.5 (currently, 4.6 when available)
- **Heavy reasoning:** Claude Opus 4.6 (only when Sonnet insufficient)
- **Rule:** Try Sonnet first, escalate to Opus only if quality insufficient

### Modular Architecture (Locked Pattern)
**Workflow:**
1. Check inventory FIRST — do utilities already exist?
2. Use what's there — call existing modules
3. Only build NEW pieces when there's a gap
4. Keep minimal — each utility does ONE thing (<150 lines)

**Architecture discovered:**
- **Utilities = format-agnostic** (work for any content type)
- **Orchestrators = format-specific** (carousel_builder vs thread_builder)
- **Configs = define the job** (JSON with prompts, text, positioning)

**Documented in:** AGENTS.md + MEMORY.md as permanent operating procedure

### Credentials Strategy
**Two-tier system:**
1. **LLM providers** → `auth-profiles.json` (Claude, Gemini, Kimi, OpenAI)
2. **Third-party services** → `.env` (GitHub, Notion, Blotato, n8n)

**Location:** `/data/.openclaw/agents/main/agent/auth-profiles.json` + `/data/.openclaw/workspace/.env`

**Reference doc:** `CREDENTIALS_INDEX.md` — NEVER say "I don't have credentials"

### Content Voice Rules (Permanent)
**Skool/Community Posts:**
- Café voice, talking to a friend
- Words: "literally," "actually," "honestly," "the thing is"
- **NEVER em dashes (—)** — use commas instead
- Personal interjections: "I know you've probably heard this before but..."
- Acknowledge cliché before giving advice
- Narrative: context → problem → switch → result
- Titles = results-driven (numbers, specific metrics)

**General Duncan Voice:**
- Direct, compressed, no fluff
- Operator not marketer
- Proof over persuasion (numbers > adjectives)
- Short sentences, strong claims, clear next steps
- First person, concrete details

### Image Styling System (Locked)
**Style signature:**
- Font: Roboto (Liberation Sans fallback)
- Alignment: Left-aligned, 80px offset
- Shadow: Soft drop shadow (NOT outline stroke)
- Positioning: Smart placement (text over buildings/open space, not subjects)
- Background: Darkened 15-35% for contrast
- **NO background boxes, NO emojis**

**Text scaling between formats:**
- 9:16 → 4:5: Scale factor 0.82× to maintain equivalent visual impact
- Formula: Geometric mean of height ratio × width ratio

**Files:** `image_styling_system.py`, `IMAGE_STYLING_GUIDE.md`

### Image Hosting Strategy
**Primary:** Google Drive Shared Drive (full quality, no compression)
**Fallback 1:** Imgur (for Notion embeds, compresses large PNGs)
**Fallback 2:** pomf.lain.la (when 0x0.st blocked)
**Retired:** 0x0.st, tmpfiles.org (403 errors)

### Notion Database IDs (Corrected Feb 14, 2026)
- **Lead Magnets & Offers:** `140dd3e4-fb8d-4066-9adc-51870ad66f07`
- **LinkedIn Posts:** `d4266f2c-ed0a-4c5b-8b81-7cb4e2ffad86` (title property = "Title" not "Name")
- **Carousels:** `cf399acfd5aa479c86b92cdea1d819d7`
- **X Threads:** `d273d932-7ff4-474a-a26e-9fee508a7164`
- **YouTube:** `aaea4588-8b61-46d2-981d-d9ef24a2749b`
- **Daily Briefings:** `306f259c0f178157bdf1c249e4f4dcb0`
- **Skool Posts:** `30cf259c-0f17-81a9-ae1f-de9720b5cb64`
- **Road to $1M:** `30bf259c-0f17-8138-b849-f25efdc0b4b0`

**Hierarchy:** Lead Magnets → LinkedIn Posts (relation) → Other channels

### Sub-Agent Spawning (Unlocked)
**Config:** `allowAgents: ["*"]` in `/data/.openclaw/openclaw.json`
**Usage:** Spawn Opus 4.6 for heavy tasks (coding, multi-step automation), Gemini for routine work
**Pattern:** Split tasks into smaller sub-agents when possible, parallel execution

### X/Twitter Strategy (Active)
**Profile:** @DuncanRogoff (verified ✓, X Premium)
**API Access:** Free tier + Premium = posting works, reading/search blocked (401 errors)
**Workaround:** Web scraping for research, API for posting only
**Watchlist:** 30 accounts in `agents/threads/X_WATCHLIST.md`
**Content Mix:** 3-5 own tweets/day + 21+ engagement replies/day
**Files:** engagement_monitor.py, following_cleanse.py, repurpose_pipeline.py, tweet_scheduler.py

### Skool Communities (Active — 13 of 29)
**Daily:** Build Room, AI Automation Society (260.9K), Synthesizer (35.7K), Jack's (1.9K)
**2-3x/week:** Maker School, BBC, AIpreneurs, GOOSIFY, Magnetic Memberships, RoboNuggets
**1-2x/week:** AI Automation Mastery, Chase AI, Skoolers (active owner), YouTube Blueprint (Dylan Reynolds)
**Full list:** `SKOOL_COMMUNITIES.md`

### Automation Cron Infrastructure
**Daily Skool Posts:** 8am EST, cron `77d52982` — 7 posts + 3-5 comments
**Daily LinkedIn Post:** 8:30am EST, cron `408d839a` — native text post + alt hooks
**Tweet Queue:** Every 30 min, cron `75d54d9e` — auto-post due tweets
**Road to $1M Check-in:** 6pm PST / 9pm EST, cron `aa54d56c` — builds next day page proactively
**Morning Briefing:** 7am EST, cron `c96ecd79`

### Key Learnings (Permanent)
1. **Content strategy = remixing proven content** into Duncan's voice/angle (NOT niching down)
2. **Every title promises a BRAND RESULT**, tool is the how not the what
3. **Lead magnet pipeline:** Every approved lead magnet → LinkedIn promo post (automatic)
4. **Briefings must be fresh daily** — never recycle items
5. **Markdown import > programmatic upload** for multi-page Notion docs
6. **Text scaling between aspect ratios is non-trivial** — visual impact ≠ pixel size
7. **Sub-agent spawning critical** for complex multi-format tasks
8. **ICP context matters:** Duncan's audience = expertise-rich, audience-poor, $8K-20K/mo from referrals

### GitHub Repo (Production Assets)
**URL:** https://github.com/duncan-buildroom/n8n-automations
**Contents:** All 30 production n8n workflows (content, lead gen, operations, research)
**Key automation:** Comment Content Engine (YouTube/TikTok/Reddit scraper → AI extraction → content ideas)

### CTA Strategy (Locked In — Feb 18, 2026)
**ALL platforms:** "The Build Room, link in bio." One destination. No exceptions.
**Key line:** "Whatever I build, you get it. Inside The Build Room. Along with everything else I've already built."
**No more "comment AI" CTAs** — all updated across agents

### Platform Bio Strategy (Feb 18, 2026)
**Discovery platforms (TikTok, X):** "Everything I build, you get."
**Conversion platforms (YouTube, Instagram, LinkedIn):** "New leads + 1,500 followers in 49 days"

### Known Issues
- Nano Banana Pro: `response_mime_type` parameter causes 400 errors (use `imageConfig.aspectRatio` instead)
- Sonnet 4.6: Model string `anthropic/claude-sonnet-4-6` not yet recognized by OpenClaw (use 4.5 for now)
- X API: Search/read endpoints blocked on free tier (web scraping required)

### Cost Optimization Rules
**Target:** <$5/day for normal operations
**Strategies:**
1. Batch operations (process multiple items in one script)
2. Local tools first (avoid API calls when possible)
3. Cheap sub-agents (spawn Gemini for routine tasks)
4. Smart caching (save and reuse results)
5. Memory efficiency (use memory_search, not full file reads)

---

## What Was Dropped (Ephemeral Details)
- Day-by-day task logs (Feb 12-18)
- Individual carousel/lead magnet generation details
- Specific cron debugging sessions
- Daily cost breakdowns
- Telegram setup steps (already complete)
- Model config patches (already applied)
- Completed deliverables (WWE strategy, specific lead magnets)
- Temporary file paths and URLs
- One-time fixes and patches
