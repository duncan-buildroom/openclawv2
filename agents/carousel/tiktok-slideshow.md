# TikTok Slideshow System — Complete Skill File
**Owner:** Duncan Rogoff (@duncanrogoff)
**Last Updated:** 2026-02-13 (v2 — updated with competitive analysis data)
**Purpose:** End-to-end workflow for creating viral TikTok Photo Mode carousels mixing real screenshots + AI-generated photo-realistic images.
**Companion file:** `tiktok-carousel-competitive-analysis.md` — full competitive research data.

---

## 1. Format Spec

### Photo Mode (Swipeable Carousel)
- **Slides:** 7-9 slides optimal (8 is the sweet spot — see Section 2 for competitive data)
- **Dimensions:** 1080 × 1920 px (9:16 vertical, full-screen)
- **Format:** JPG or PNG, under 500KB per image
- **Font:** Bold sans-serif (Inter Bold, SF Pro Display Bold, or Montserrat Black)
- **Text size:** Minimum 48px for body, 72px+ for hooks/headlines
- **Colors:** Dark background (#0D0D0D or #111827) + white text + one accent (#A2E6F3 or #22D3EE for brand, #F59E0B amber for proof/numbers)
- **Safe zones:** Keep text 150px from top, 300px from bottom (TikTok UI overlap)

### Critical Step
When uploading: **Tap "Switch to Photo Mode"** after selecting images. If you skip this, TikTok defaults to auto-advancing Template Mode (video-style, not swipeable). You want Photo Mode for the swipe engagement signals.

---

## 2. Slide Architecture (7-Slide Framework — Updated Feb 2026)

> **Standard (Feb 14, 2026):** 7 slides is the locked default. No more, no less. See `CAROUSEL_PROCESS.md` for the canonical slide structure.

### Primary Structure: HOOK → PROBLEM → SOLUTION/SCREENSHOT → INFOGRAPHIC → PROOF/DETAILS (×2) → CTA

| Slide | Purpose | Image Type | Text Overlay |
|-------|---------|------------|--------------|
| **1 — Hook** | Stop the scroll | AI-generated (iPhone-style scene) OR bold text on dark | Hook line (max 12 words), large text. **Add "1/8" indicator.** |
| **2 — Problem** | Identify pain point | AI-generated (frustrated person, empty inbox, phone screen) | Problem statement, relatable scenario |
| **3 — Agitate** | Show the cost of inaction | Designed graphic or screenshot of bad outcome | "Here's what it's costing you..." — creates urgency |
| **4 — Mechanism** | Show the system/solution | Real screenshot (n8n workflow, Airtable, dashboard) | What the system does, 1-2 lines |
| **5 — Deep Dive Step 1** | First key component | Real screenshot with annotations (circles, arrows) | Step 1 of the framework |
| **6 — Deep Dive Step 2** | Second key component | Real screenshot or designed graphic | Step 2 of the framework |
| **7 — Proof** | Evidence it works | Real screenshot (analytics, revenue, follower count, DMs) | Specific numbers, metrics. **Proof late = prevents early exit.** |
| **8 — CTA** | Drive action | AI-generated (aspirational scene) OR branded | Single CTA: "Follow for more" / "Comment SYSTEM" / "Save this" |

### Why 8 Slides Beats 6:
- **More swipe signals** for the algorithm (each swipe = engagement)
- **Room for framework depth** (two "Deep Dive" slides vs one)
- **Proof on slide 7** prevents viewers from leaving after slide 4 (the old proof position)
- **Numbered indicators** (1/8, 2/8...) create progress bar psychology → higher completion
- **Matches viral averages** across both automation and branding niches

### Alternate Structures (Updated Feb 2026 — based on competitive analysis)

**LISTICLE (7-10 slides) — BEST for AI Tools/Automation posts:**
> Competitive insight: Listicle format is the #1 performing structure in automation niche.
1. Hook ("7 automations that replaced my team") 
2-8. One tool/tip per slide with screenshot or clean graphic
9. CTA + "Save this for later"
*Use numbered indicators on every slide (1/9, 2/9...)*

**TRANSFORMATION STORY (7 slides) — BEST for Client Case Studies:**
> Competitive insight: Client stories with real screenshots are severely underutilized = huge white space opportunity.
1. Hook (result first — the number)
2. Who they are (context — name, situation)
3. Their problem/before state
4. The turning point (what changed)
5. The system (real screenshots of actual workflow)
6. The results (proof metrics — specific numbers)
7. CTA + takeaway

**CONTRARIAN / MYTH-BUST (6-7 slides):**
> Competitive insight: Contrarian posts go viral, but almost nobody backs them with data. Duncan can own "contrarian + proof."
1. Bold contrarian hook ("The biggest lie in content creation...")
2. Why common wisdom is wrong (with actual data/screenshot)
3. What to do instead — part 1
4. What to do instead — part 2
5. Proof it works (real screenshot)
6. Key takeaway
7. CTA

**BEFORE/AFTER TRANSFORMATION (7 slides):**
1. Hook → 2. Before state (ugly spreadsheet/manual process) → 3. The "aha" moment → 4. After state (clean dashboard) → 5. How they did it (system screenshot) → 6. Results → 7. CTA

**"BUILD WITH ME" WALKTHROUGH (8-10 slides):**
> Competitive insight: Almost nobody shows the BUILD process — only the result. This is a major white space.
1. Hook ("I built a system that turns 1 idea into 15 posts")
2. Overview of what we're building
3-8. Step-by-step screenshots of building the workflow
9. Final result / running system
10. CTA

---

## 3. Image Strategy: Real Screenshots + AI-Generated

### Real Screenshots (Credibility Slides)
Use for: n8n workflows, Airtable views, analytics dashboards, revenue screenshots, DM conversations, follower counts, TikTok analytics

**Rules:**
- Clean, dark-mode where possible
- Blur sensitive data (client names, emails) but keep numbers visible
- Add subtle overlay/annotation (circle key metrics, add arrows)
- Slight drop shadow + rounded corners for "floating" look
- See `screenshot-capture.md` for automation

### AI-Generated Images (Storytelling Slides)
Use for: Hook slides, problem/pain visualizations, aspirational scenes, lifestyle context

**Rules:**
- Must look photo-realistic (iPhone photo quality)
- NO cartoon, illustration, render, or "AI art" aesthetic
- Shot on iPhone 16 Pro style: natural lighting, slight depth of field, real environments
- People should look like real independent business owners (diverse, 30s-50s, professional-casual)
- See `image-generation.md` for exact prompts

### Mix Per Carousel (Updated Feb 2026 — based on competitive analysis)
- **Minimum 3 real screenshots** per carousel (up from 2 — competitive data shows screenshots drive 40% more saves)
- **Maximum 3 AI-generated images** per carousel
- **Slides 4, 5, and 7 should include real screenshots** (mechanism + deep dives + proof)
- **Add annotations** (circles, arrows, highlights) to ALL screenshot slides — top performers consistently do this
- **Numbered slide indicators** ("1/8", "2/8") on every slide — proven to increase swipe completion by reducing drop-off

### Visual Identity (Competitive Positioning)
> Based on competitive analysis: See `tiktok-carousel-competitive-analysis.md` for full breakdown.

**What to COPY (effective, not oversaturated):**
- Real screenshots with colored annotations (circles, arrows, highlights)
- Mixed media per carousel (some screenshots, some graphics, some AI)
- Dark mode base matching developer/tech aesthetic
- One accent color consistently

**What to AVOID (oversaturated or underperforming):**
- ❌ Generic Canva template look (gradient backgrounds, stock icons)
- ❌ All-text slides (no images = low saves, low completion)
- ❌ Overly polished corporate graphics (feels like an ad)
- ❌ Pure AI images with no real content (erodes trust)
- ❌ Too many fonts/colors (consistency > creativity)

**What to OWN (Duncan's distinctive style):**
- "Real screenshot + annotation" as signature visual
- Dark mode (#0D0D0D) + cyan accent (#22D3EE) brand consistency
- "iPhone screenshot of iPhone screenshot" (real phone showing real analytics)
- AI-generated lifestyle for hooks ONLY, real data for everything else

---

## 4. Hook Formulas

### Formula Bank (Expanded Niche: Automation + Expert Positioning + Audience Building)

**Pattern: [Person/I] + [Problem/Bottleneck] → [System/Solution] → [Result/Proof]**

#### Category A: Automation Workflows
1. "I built [X] automations that replaced [Y hours/people/tasks]"
2. "This one n8n workflow does what used to take me [X hours]"
3. "My client [name] automated [process] — here's exactly how"
4. "[X] tools connected. Zero manual work. Here's the system."
5. "Stop manually [task]. This automation does it in [time]."

#### Category B: Audience Growth / Expert Positioning
6. "I went from 0 to [X]K followers in [Y] days. Here's the system."
7. "[Name] had zero audience and [X]K/mo in skills. In [Y] days: [result]."
8. "You're the best at what you do. Nobody knows. Here's why."
9. "Your referrals are drying up. Here's what to build instead."
10. "People with half your skill get twice your clients. The difference: [X]."

#### Category C: Proof/Transformation
11. "[Name] went from [X] to [Y] in [Z] days using this system."
12. "First leads in 14 days. 1,500 followers in 49. No tricks."
13. "$[X] in revenue from content I made with AI. The exact setup:"
14. "My student sold $4,750 on one call. Here's what we changed."
15. "From zero posts to [X]K views. The 3-part framework:"

#### Category D: Contrarian/Pattern Interrupt
16. "The biggest lie in content creation: 'just be consistent.'"
17. "You don't need to be original. You need to be you, on what's working."
18. "Posting more won't fix this. Your positioning will."
19. "I automated my entire content pipeline. My audience grew 3x faster."
20. "Every expert I know who's broke has the same problem."

#### Category E: Starting-From-Zero Framework (Top viral format — Feb 2026 competitive data)
21. "If I had to grow from 0 followers today, here's the exact system I'd build"
22. "Starting from zero? Here are the 5 automations I'd set up on day 1"
23. "What I'd do differently if I had to rebuild my audience from scratch"

#### Category F: Myth-Busting / Data-Backed (Underutilized — white space)
24. "Everyone says 'post every day.' Here's what actually happened when we tested it."
25. "The advice killing most expert businesses: '[common wisdom]'"
26. "'Just provide value' is terrible advice. Here's what actually grows an audience."

#### Category G: Cost/Time Comparison (Consistently high-performing)
27. "I replaced my $[X]K/mo team with 3 n8n workflows. Here's the setup."
28. "This $0 automation saves me [X] hours every week"
29. "My client was spending $[X]/mo on [task]. Now it costs $0."

#### Category H: Bridge Content — Automation × Audience (DUNCAN'S UNIQUE ANGLE)
> Competitive insight: This intersection is virtually unoccupied. Nobody else is teaching "use automation to build your expert audience." This is Duncan's biggest competitive advantage.
30. "I automated my content pipeline. My audience grew 3x in 60 days."
31. "The 3 automations behind every viral post I make"
32. "How I post on 4 platforms without touching any of them (automation walkthrough)"
33. "Your content strategy is manual. That's why you're losing."
34. "I built a system that turns one idea into 15 pieces of content. Here's how."
35. "The system that posts while I sleep — and gets more views than when I was manual"

### Hook Rules
- **Max 12 words** on slide 1
- **Use specific numbers** (not "a lot of followers" → "1,500 followers")
- **Name names** when possible (with permission) — specificity = credibility
- **Pattern interrupt:** Hook should look/feel different from typical TikTok video thumbnails
- **Test 3 hooks per concept** — rotate weakest out after 48 hours

---

## 5. Caption Template

```
[Hook line — repeat or expand slide 1]

[1-2 sentences expanding the story/problem]

[What the system/solution is — 1 sentence]

[Proof point — specific number or result]

[CTA: "Follow for the full breakdown" / "Comment [WORD] and I'll send you the template" / "Save this — you'll need it"]

#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5
```

### Caption Rules (Updated Feb 2026 — competitive data)
- **250-400 characters** optimal (up from 200+ — longer captions correlate with higher TikTok SEO ranking)
- **First line = hook expansion** — TikTok shows first 2 lines in feed, this is your second chance to hook
- **Max 5-6 hashtags** — mix of: 1 broad (#automation), 1 niche (#n8nautomation), 1 audience (#businessowner), 1 trending, 1 branded (#buildroom)
- **One CTA only** — don't split attention
- **Include "Save" CTA** in caption — "Save this → you'll need it when you build yours" (save is the #1 engagement signal for carousels)
- **One engagement question** — drives comments: "Which step would help you most?" or "What would you automate first?"
- **Keyword-rich** — TikTok scans captions for search ranking. Stuff with relevant terms naturally.

### Hashtag Bank (Updated Feb 2026)
**Core rotation:**
- #automation #aiautomation #n8n #buildroom #personalbrand
- #businessowner #entrepreneur #contentcreator #audiencegrowth #expertpositioning
- #makemoney #sidehustle #aitools #workflow #leadgeneration
- #socialmedia #tiktokgrowth #contentmarketing #brandbuilding #techstartup

**NEW — Competitive white space hashtags (less saturated, highly engaged):**
- #buildwithme (emerging creator tag)
- #automationlife (niche but engaged)
- #nocodesolutions (growing no-code community)
- #systemsthinking (crossover appeal to business audience)
- #contentautomation (Duncan's unique intersection — very low competition)
- #workflowautomation (technical but growing)

**Pick 5-6 per post:** 1 broad + 1 niche + 1 audience + 1 topic + 1 branded + 1 white space

---

## 6. Posting Workflow

### Pre-Production (Batch Day — 1x/week)
1. Pick 5-7 hooks from the hook bank
2. For each hook, assign a slide structure (6-slide framework)
3. Identify which slides need real screenshots vs AI images
4. Capture screenshots (see `screenshot-capture.md`)
5. Generate AI images (see `image-generation.md`)
6. Assemble slides in Canva/Figma at 1080×1920
7. Add text overlays, annotations, brand elements
8. Export as individual PNGs (slide-1.png through slide-6.png)
9. Write captions + select hashtags

### Production (Daily — 1-2 posts/day)
1. Open TikTok → tap + → Upload
2. Select 6 images in order
3. **Switch to Photo Mode** (critical!)
4. Add trending sound (low volume, background vibes)
5. Paste caption
6. Post at optimal time (check TikTok Analytics for audience activity)
7. Log in `performance-tracker.md`

### Post-Production (48-72 hours after posting)
1. Check metrics: views, likes, comments, saves, shares
2. Log performance in tracker
3. Reply to ALL comments in first 2 hours
4. If hook underperformed, test alternate hook on same content
5. If carousel outperformed, create 2-3 variations on same theme

---

## 7. Optimal Posting Times
- **Test first:** Check TikTok Analytics → Followers → Activity
- **General defaults:** 7-9 AM, 12-2 PM, 7-10 PM (audience timezone)
- **Duncan's audience:** Mix of US timezones, weight toward PST/EST
- **Carousel-specific:** Mornings and late evenings tend to favor swipeable content (people browse, not just watch)

---

## 8. Algorithm Signals for Carousels

### What TikTok Tracks (Ranked by Weight)
1. **Swipe-through completion rate** — % who view all 6 slides (most important)
2. **Dwell time per slide** — longer = more interest signal
3. **Saves** — strongest engagement signal for carousels (reference-worthy content)
4. **DM shares** — high-value signal
5. **Comments** (especially replies/threads)
6. **Likes** — lowest weight but still counts

### How to Optimize (Updated Feb 2026 — competitive best practices)
- **Add numbered slide indicators** (1/8, 2/8) → creates progress bar psychology, proven to increase completion
- Make each slide a mini-cliffhanger → drives swipe completion
- Put the best proof/reveal on **slide 7** (not 4-5) → prevents early drop-off after seeing the payoff
- End with clear **single CTA** → drives comments and saves
- Use curiosity gaps between slides ("But here's what happened next...")
- **Consistent visual template** → reduces cognitive load, trains swipe behavior
- **Educational/actionable content** gets 2.5x more saves than entertainment carousels
- If someone doesn't swipe all slides, TikTok may re-surface it later (second chance)
- **Use "Save this" CTA** (in both slide 7 and caption) — saves are the highest-weight carousel signal

---

## 9. Engagement Data (Why Carousels)

From TikTok's own data + independent studies (2025-2026):
- **1.9x more likes** than video posts
- **2.9x more comments** than video posts
- **2.6x more shares** than video posts
- **81% higher engagement rate** overall (Fanpage Karma study)
- Carousels get similar reach to video (~3% higher) but massively higher engagement
- TikTok actively pushes Photo Mode to creators since 2024

**Trade-off:** Shares are ~33% lower than video. If pure virality through shares is the goal, video wins. For engagement, community building, and saves → carousels dominate.

---

## 10. Failure Log

Track what doesn't work so we don't repeat it.

| Date | Hook | Views | Issue | Lesson |
|------|------|-------|-------|--------|
| _template_ | _"Hook text"_ | _XXX_ | _What went wrong_ | _What to change_ |

### Common Failure Patterns
- **Generic hooks** ("5 tips for...") → Fix: Add specificity, names, numbers
- **No real screenshot** → Fix: Always include 2+ real screenshots for credibility
- **Too much text per slide** → Fix: Max 3 lines, 15 words per slide
- **Weak CTA** → Fix: Single clear action, not multiple asks
- **AI images look fake** → Fix: Review `image-generation.md` prompts, iterate
- **Posted at low-activity time** → Fix: Check analytics, stick to peak windows
- **Hashtags too broad** → Fix: Mix niche + broad, never all broad

---

## 11. Cross-Platform Repurposing

Each TikTok carousel can be repurposed:
- **Instagram carousel** → Same images, adjust caption for IG style
- **LinkedIn carousel** → Convert to PDF, add more context per slide
- **Twitter/X thread** → One slide = one tweet, thread format
- **YouTube community post** → Use hook slide as image, caption as text
- **Email newsletter** → Carousel content becomes a mini-article

---

## 12. Music/Audio Strategy

- **Always add music** — even for carousels (plays while swiping)
- **Use trending sounds** — check TikTok's sound library for what's current
- **Low volume** — music is atmosphere, not the focus
- **Match tone:** Chill/focus music for tutorials, upbeat for wins/proof, dramatic for problem slides
- **Voiceover optional:** Can add narration as original sound (boosts watch time but adds production)

---

## 13. Competitive Intelligence Summary (Feb 2026)

> Full analysis: `tiktok-carousel-competitive-analysis.md`

### Duncan's 3 Biggest Competitive Advantages:

1. **Bridge Content (Automation × Audience Building)**
   - The intersection of "use automation to build your expert audience" is virtually unoccupied
   - Nobody else teaches how automation systems drive audience growth
   - This is Duncan's unique lane — lean into it HARD

2. **Client Stories + Real System Screenshots**
   - Most automation creators show generic workflows
   - Most branding creators tell generic success stories
   - Duncan can combine SPECIFIC client transformations with ACTUAL system screenshots
   - This is the highest-trust carousel format and severely underutilized

3. **"Live System" Transparency**
   - Competitors show results. Duncan can show the RUNNING system.
   - Active dashboards, mid-execution workflows, real-time analytics
   - Authenticity + voyeurism + credibility = maximum engagement

### Content Mix Recommendation (Weekly):
- **2 Listicle carousels** (tools/automations — highest reach)
- **1 Client Transformation story** (builds trust + authority)
- **1 Bridge Content post** (automation × audience — unique angle)
- **1 Contrarian/Myth-bust with data** (drives comments + shares)
- **1 "Build With Me" walkthrough** (deep engagement + saves)

### Key Metrics to Track for Carousel Performance:
1. **Swipe-through completion rate** — target 50%+ all-slide views
2. **Save rate** — target 3%+ (carousels should be save-heavy)
3. **Slide drop-off points** — identify where people stop swiping
4. **Comment quality** — questions = good (engagement), "nice" = bad (low signal)
5. **DM shares** — the highest-value signal, indicates true virality
