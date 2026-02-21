# Classroom Module Guide

## Intro Page: "💰 Road to $1M — What This Is"

Current version is good but can be stronger. Here's the improved version:

---

I'm building a $1M personal brand with AI. In public. *Starting at $27-31K/mo.*

Every single day I post a video documenting what I'm building, what's working, what's failing, and how much money is coming in.

Real numbers. No rounding up.

**What you get:**

Every day comes with a deliverable. A workflow, a template, a prompt, a framework.

Whatever I build that day, you get it. Not a tutorial about it. The actual asset.

By Day 30 there are 30 assets in here. By Day 100 there are 100. They stack. The longer you're here, the more you have.

**Who this is for:**

You're great at what you do. Clients love you. But you're invisible online. You know you need an audience, you know you need content, you know you need leverage. You just don't have the system.

That's what I'm building, in front of you, and handing you every piece as I go.

**The goals:**

• $1M in total revenue earned
• 3,000 Build Room members
• 100K YouTube, 100K TikTok, 20K X, 10K LinkedIn
• Full transparency on every dollar, every milestone, every win and loss

**How to follow along:**

Watch the daily videos (TikTok, YouTube Shorts, Instagram Reels, LinkedIn, X). Grab the deliverable here. Use it. Build alongside me.

This isn't a course. It's a live build.

💰 **And everything I make, you get.**

---

## Day 1: "The $1M Roadmap"

Current: too short, just links to Notion. Improved (120-150 words):

---

Gatekeeping nothing to $1M.

This is the exact roadmap I'm using to build a $1M personal brand with AI. Every revenue stream, every milestone, every number is real.

Most people doing $8-20K/mo from referrals have no idea what the path to $1M actually looks like. They know they need more clients but they're guessing at how to get there. No audience, no content system, no leverage.

This roadmap breaks down exactly where the money comes from, what has to grow, and in what order. It's the same framework I'm following every single day of this series.

Use it to map your own journey. Plug in your numbers. See what $1M looks like for YOUR business.

📎 [The $1M Roadmap](https://www.notion.so/The-1M-Roadmap-30bf259c0f1781699a8bd9210570b1e3)

Whatever I build, you get.

---

## Day 2: "The Content Repurpose Agent"

---

I built an AI agent that cross-posts my content to 5 platforms automatically.

**That’s how you’re seeing this right now.**

If you're posting on TikTok but not on Instagram, YouTube, LinkedIn, and X, you're leaving 80% of your reach on the table. You already did the hard part (creating the content). Distribution shouldn't take another hour.

Today you get the "Logic Engine" for the agent that makes this happen.

**How to use this:**

1. **Copy the Prompt:** Grab the System Prompt from the deliverable link below.
2. **Setup your Agent:** Create a new Agent in Claude (Projects), OpenAI (GPTs), or OpenClaw.
3. **Paste & Run:** Paste this into the "Instructions" or "System Prompt" field. 
4. **Result:** Drop in a transcript and it will output 5 platform-native posts ready to publish.

Whatever I build, you get.

---

## Template for Daily Classroom Copy

```
[One sentence: what the asset is and what it does.]

[The "Meta Proof" line: "That's how you're seeing this right now" or similar.]

[2-3 sentences: the ICP problem. Why this matters for someone doing $8-20K/mo from referrals who's invisible online. Be specific about the pain.]

[Clear 3-Step "Stupidly Simple" implementation instructions.]

Whatever I build, you get.
```

Word count target: 120-150 words. No more.

## Formatting Rules (from Duncan's Day 1 reference)
- **One sentence per paragraph.** Every sentence gets its own `<p>` tag. This creates Skool's natural line spacing.
- **Short related lines can stay together** (e.g., "Use it to map your own journey." / "Plug in your numbers." / "See what $1M looks like for YOUR business." as 3 consecutive paragraphs)
- **Italic for key emphasis lines** (e.g., *It's the same framework I'm following every single day of this series.*)
- **Bold for the closer:** "**Whatever I build, you get.**"
- **No empty spacer paragraphs.** Each `<p>` already creates visual spacing in Skool.
- **For tight lists** (like goals), use hardBreak (Shift+Enter / `<br>`) within a single paragraph

## How to Add a Hyperlink in Body Copy (CRITICAL)
Do NOT paste raw URLs in body text. Use this exact sequence:
1. Type the link anchor text (e.g. "Get the full roadmap and every asset I build: Start Road to $1M.")
2. **Select/highlight** that text
3. A floating toolbar appears — click the **chain/link icon** (🔗)
4. A URL input box appears — paste the URL
5. Press Enter or click Save
6. The text becomes a clickable hyperlink (no raw URL visible)

## How to Replace Body Copy (CRITICAL)
1. Click the edit pencil icon
2. **Ctrl+A (Select All)** to select ALL existing body text
3. **Delete/Backspace** to clear it completely
4. Then type/paste new content from scratch
5. Never append — always replace

## Resource Links
- Resources go in Skool's built-in **Resources section** at the bottom of the page — NOT as inline links in the body text
- In edit mode: click **ADD** at bottom → select **Resource Link** → fill in title + URL → Save
- One resource per module: the deliverable (Notion page, template, prompt, etc.)
- NEVER put raw URLs or inline links in the body copy
- NEVER link to The Build Room from inside The Build Room — redundant
- "Whatever I build, you get." closes every module with no link. They know where they are.

## ProseMirror Technical Notes (for automation)
- Resources are NOT part of the ProseMirror editor content
- To add a resource: after saving body content, click ADD button → Resource Link → fill fields → Save
- The ADD button appears at the bottom of the edit view
- Resource Link has two fields: title and URL
