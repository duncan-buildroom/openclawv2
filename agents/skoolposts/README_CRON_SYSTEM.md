# Skool Automation System — Daily Posting & Commenting

## Overview

Automated system that posts and comments across 13 Skool communities daily (Build Room excluded for manual handling).

**Daily output:**
- 5 posts (50-100 words each, staggered 9am-7pm)
- 30 comments (1-3 sentences each, staggered 10am-8pm, 5-6 per community)

---

## Components

### 1. `rotation_state.py`
**Purpose:** Tracks which communities used today, prevents duplicates, weights by tier

**Tiers:**
- **Tier 1 (3):** AI Automation Society, Synthesizer, AI Automations by Jack — weighted 3x
- **Tier 2 (6):** Maker School, BBC, AIpreneurs, GOOSIFY, Magnetic Memberships, RoboNuggets — weighted 2x
- **Tier 3 (4):** AI Automation Mastery, Chase AI, Skoolers, YouTube Blueprint — weighted 1x

**Commands:**
```bash
python3 rotation_state.py status          # Show today's state
python3 rotation_state.py reset           # Reset for new day
python3 rotation_state.py pick 5 posts    # Pick 5 for posts
python3 rotation_state.py pick 5 comments # Pick 5 for comments
```

---

### 2. `skool_posts_cron.py`
**Purpose:** Generate and schedule 5 posts throughout the day

**Schedule:**
- 9:00am — Community 1
- 11:30am — Community 2
- 2:00pm — Community 3
- 4:30pm — Community 4
- 7:00pm — Community 5

**Post specs:**
- 50-100 words
- Every sentence = separate paragraph
- Max 1 emoji (only if necessary)
- Voice tailored to community (see SKOOL_POSTING_STRATEGY.md)

**Output:** Drafts pushed to Notion DB `30cf259c-0f17-81a9-ae1f-de9720b5cb64` for review

---

### 3. `skool_comments_cron.py`
**Purpose:** Generate and schedule 30 comments across 5 communities

**Schedule:**
- 10:00am — Community 1 (5-6 comments)
- 12:30pm — Community 2 (5-6 comments)
- 3:00pm — Community 3 (5-6 comments)
- 5:30pm — Community 4 (5-6 comments)
- 8:00pm — Community 5 (5-6 comments)

**Comment specs:**
- 1-3 sentences
- Short, friendly, casual
- Scan ALL categories, newest posts (24h)
- Skip posts Duncan already engaged with
- Avoid politics, drama

**Browser optimization:**
- Single tab per community
- Sequential navigation through comments
- Close tabs when done

**Output:** Drafts pushed to Notion DB for review

---

## Cron Setup

Add to `/data/.openclaw/cron/jobs.json`:

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "77d52982",
      "name": "Daily Skool Posts",
      "schedule": "0 9 * * *",
      "type": "isolated",
      "command": "cd /data/.openclaw/workspace/agents/skoolposts && python3 skool_posts_cron.py",
      "enabled": true
    },
    {
      "id": "d55ff758",
      "name": "Daily Skool Comments",
      "schedule": "0 10 * * *",
      "type": "isolated",
      "command": "cd /data/.openclaw/workspace/agents/skoolposts && python3 skool_comments_cron.py",
      "enabled": true
    }
  ]
}
```

---

## Testing

### Test rotation (no actual posting):
```bash
cd /data/.openclaw/workspace/agents/skoolposts
bash test_rotation.sh
```

### Test posts cron (DRY RUN):
```bash
cd /data/.openclaw/workspace/agents/skoolposts
python3 skool_posts_cron.py
# Will show which communities selected, but won't actually spawn agents
```

### Test comments cron (DRY RUN):
```bash
cd /data/.openclaw/workspace/agents/skoolposts
python3 skool_comments_cron.py
```

---

## Production vs Testing

**Testing:** Can use Build Room to verify browser automation works

**Production:** Build Room excluded from rotation (`rotation_state.py` has all 13 communities, no Build Room)

---

## Voice Rules Per Community

See `SKOOL_POSTING_STRATEGY.md` for detailed voice guidance per community.

**Quick reference:**
- **AI Automation Society:** Technical but accessible, reference n8n/agents/model routing
- **Synthesizer:** Community growth + monetization, educator-to-educator
- **Jack's:** Deep technical, agent architecture, cost optimization
- **Maker School:** Builder-to-builder, shipping speed, automation-first
- **GOOSIFY:** Sillier, more vibey, casual, playful
- **Others:** See strategy guide

---

## Output Format

All posts/comments pushed to **Notion DB:** `30cf259c-0f17-81a9-ae1f-de9720b5cb64`

**Properties:**
- Community (select)
- Type (Post or Comment)
- Status (Draft — for review)
- Scheduled (datetime of intended post time)
- Post URL (for comments, link to parent post)

---

## Troubleshooting

**No communities picked:**
- Run `python3 rotation_state.py reset` to clear state

**Browser tabs staying open:**
- Check that `skool_post.py` closes tabs after each community batch

**Wrong voice:**
- Update `SKOOL_POSTING_STRATEGY.md` with correct voice rules
- Agent reads this file before generating content

**Duplicate communities:**
- Rotation state prevents same community appearing twice in same day for same action type
- Posts and comments rotate independently (overlap OK)

---

## Future: Autonomous Mode

Currently: All output pushed to Notion as **Draft** for Duncan's review

**To enable autonomous posting:**
1. Change `Status: "Draft"` → `Status: "Approved"` in push functions
2. Add browser automation step to actually post to Skool
3. Remove Notion push step (or keep for logging)

**Recommendation:** Keep review mode for 2 weeks, then switch to autonomous
