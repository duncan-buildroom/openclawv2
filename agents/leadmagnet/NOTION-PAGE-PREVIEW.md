# Notion Page Preview: Visual Structure

## How the Page Will Look

```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│   The Ultimate Guide to Multi-Agent Systems in OpenClaw      │
│   How to Build an AI Employee That Runs Your Business 24/7   │
│                                                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  🤖  What you're about to learn: The exact system Duncan    │
│      uses to run his entire content business with 6 AI      │
│      sub-agents. No theory. No fluff. Just the blueprint    │
│      that replaces a VA, designer, and social media         │
│      manager for ~$5/day.                                   │
└─────────────────────────────────────────────────────────────┘
         ↑ Blue callout

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## The System in Action

Every morning at 8 AM, Duncan's **briefer** agent wakes up, 
scans his calendar, email, and social mentions, then sends a 
personalized briefing to Telegram...

┌─────────────────────────────────────────────────────────────┐
│  📊  Real numbers: 6 sub-agents | 24/7 operation |          │
│      ~$5/day API costs | Replaces 3 contractors             │
└─────────────────────────────────────────────────────────────┘
         ↑ Gray callout

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1. Why One Brain + Many Specialists (Not One Mega-Agent)

### The Problem with Mega-Agents

Most people try to build ONE agent that does everything...

• Confused about its role
• Bloated with context
• Expensive
• Fragile
• Hard to improve

### The Orchestrator Pattern

Instead, Duncan's system works like a company:

1. One orchestrator (the CEO)
2. Multiple sub-agents (the team)
3. Clear contracts

┌─────────────────────────────────────────────────────────────┐
│  💡  Mental model: You wouldn't hire one person to be       │
│      your designer, accountant, and customer support rep.   │
│      Don't build one agent to do it all.                    │
└─────────────────────────────────────────────────────────────┘
         ↑ Yellow callout

### How It Works

```
User → "Create a carousel about AI agents"
  ↓
Orchestrator reads the request
  ↓
Routes to: carousel agent
  ↓
Carousel agent generates copy
  ↓
Passes to: imgen agent (if visuals needed)
  ↓
Passes to: publisher agent
  ↓
Posted to Instagram/LinkedIn
```
         ↑ Code block

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 2. How to Design Sub-Agents: The SOUL.md Structure

Every agent in OpenClaw has a **SOUL.md** file...

### Anatomy of a SOUL.md

• Identity — Who are you?
• Purpose — What problem do you solve?
• Inputs — What do you receive?
• Outputs — What do you deliver?
• Constraints — What are your rules?
• Examples — Show, don't just tell

┌─────────────────────────────────────────────────────────────┐
│  ⚠️  Critical: A vague SOUL.md creates a confused agent.    │
│      Be specific.                                            │
└─────────────────────────────────────────────────────────────┘
         ↑ Red callout

### Two Types of SOUL.md

▼  📋 Template #1: Orchestrator SOUL.md
   ├─ [Code block with full template]
   └─ (Click to expand/collapse)

▼  📋 Template #2: Sub-Agent SOUL.md (Example: Carousel Agent)
   ├─ [Code block with full template]
   └─ (Click to expand/collapse)

         ↑ Toggle blocks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 3. The AGENTS.md Registry: How the Orchestrator Knows Who to Call

The orchestrator needs a directory. That's **AGENTS.md**...

### What Goes in AGENTS.md

• Agent name
• Purpose
• Triggers
• Input contract
• Output contract

▼  📋 Template: AGENTS.md
   ├─ [Full registry template]
   └─ (Click to expand)

┌─────────────────────────────────────────────────────────────┐
│  🎯  Pro tip: Start with 3-4 agents. Don't build 20        │
│      upfront. Add agents as you identify repetitive tasks.  │
└─────────────────────────────────────────────────────────────┘
         ↑ Blue callout

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 4. Cron Jobs for Automation: Set It and Forget It

Cron jobs are how Duncan's system runs on autopilot...

### What to Automate

• Daily briefings (8 AM)
• Engagement tracking (11 PM)
• Content backups (daily)
• Weekly reports (Monday 9 AM)

### How to Set It Up

1. Create shell script
2. Add to crontab
3. Test manually
4. Monitor logs

▼  📋 Template: Cron Job Configs
   ├─ [Bash script with 7 cron schedules]
   └─ (Click to expand)

┌─────────────────────────────────────────────────────────────┐
│  ⚙️  Note: Cron syntax can be tricky. Use crontab.guru to  │
│      validate your schedules.                                │
└─────────────────────────────────────────────────────────────┘
         ↑ Gray callout

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Sections 5-8 follow same structure with:
 - Headings (H2, H3)
 - Paragraphs
 - Bullet lists
 - Callouts (color-coded by importance)
 - Code blocks
 - Numbered lists]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📦 Downloadable Templates

Everything you need to start building...

### Template 1: SOUL.md (Orchestrator)

```markdown
# SOUL.md - Orchestrator Agent
...
```

### Template 2: SOUL.md (Sub-Agent Example)

```markdown
# SOUL.md - [Agent Name]
...
```

[Continue with all 5 templates as code blocks]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🚀 Your Next Steps

You now have the blueprint...

1. Pick your first agent
2. Write its SOUL.md
3. Test it manually
4. Add to AGENTS.md
5. Automate with cron (if needed)
6. Iterate

┌─────────────────────────────────────────────────────────────┐
│  💡  Remember: Start small. Duncan didn't build 6 agents   │
│      overnight. He started with one (carousel), proved it   │
│      worked, then added more.                               │
└─────────────────────────────────────────────────────────────┘
         ↑ Blue callout

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🛠️ Want Help Building Your System?

This guide gives you the blueprint. But building your own 
multi-agent system? That's where most people get stuck.

**The Build Room** is Duncan's private community...

• Live troubleshooting
• Agent templates
• Weekly workshops
• Private Slack
• Early access

┌─────────────────────────────────────────────────────────────┐
│  🎯  Your goal: Ship your first agent system in 30 days.   │
│      We'll help you do it.                                  │
└─────────────────────────────────────────────────────────────┘
         ↑ Green callout (CTA emphasis)

👉 **[Join The Build Room](https://buildroomcommunity.com)**

─────────────────────────────────────────────────────────────

Questions? DM Duncan on Twitter: **[@duncanlhamilton]**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────┐
│  🤖  This guide was created by Duncan's leadmagnet agent.  │
│      Meta, right?                                           │
└─────────────────────────────────────────────────────────────┘
         ↑ Gray callout (footer)
```

---

## Color Coding System

**Blue callouts** → Educational insights  
**Yellow callouts** → Mental models / analogies  
**Red callouts** → Critical warnings  
**Gray callouts** → Tips / asides  
**Green callouts** → CTAs / action items  
**Purple callouts** → Key technical insights  

---

## Block Types Used

✅ Headings (H1, H2, H3)  
✅ Paragraphs  
✅ Bulleted lists  
✅ Numbered lists  
✅ Callouts (6 colors)  
✅ Code blocks (markdown, bash, JSON, plaintext)  
✅ Toggle blocks (for long templates)  
✅ Dividers  
✅ Tables (in Notion database section)  

---

## Page Flow

```
Hero callout (blue, 🤖)
  ↓
Proof section (story-driven intro)
  ↓
8 educational sections (pattern → examples → templates)
  ↓
Templates collection (all 5 downloadable)
  ↓
Next steps (actionable)
  ↓
CTA section (Build Room pitch)
  ↓
Meta footer (🤖)
```

**Total length:** ~8,000 words  
**Reading time:** ~30 minutes  
**Implementation time:** 1-3 hours for first agent  

---

## What Makes It Scannable

1. **Short paragraphs** (3-4 lines max)
2. **Frequent callouts** (visual breaks every ~200 words)
3. **Bullet lists** over long prose
4. **Code blocks** clearly marked
5. **Toggles** hide complexity until needed
6. **Emoji headers** on callouts for quick recognition
7. **Bolded key phrases** for skimmers

**Result:** Someone can skim in 5 minutes or deep-read in 30. Both get value.

---

This is the structure. Ready to build in Notion!
