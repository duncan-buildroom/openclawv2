# Skool Automation — Testing Guide

## System Built

**What it does:**
1. Generates posts/comments via `skoolposts` agent
2. Posts directly to Skool via browser automation
3. Logs to Notion AFTER successful posting (for review)

**Current mode:** TEST MODE (Build Room only)

---

## Quick Test (Manual)

Run this to post 1 test message to Build Room:

```bash
cd /data/.openclaw/workspace/agents/skoolposts
export $(grep -v '^#' /data/.openclaw/workspace/.env | xargs)
python3 test_post_buildroom.py
```

**What it does:**
1. Spawns agent to generate a 50-80 word test post
2. Shows you the generated text
3. Asks for confirmation
4. Opens browser, logs in, posts to Build Room
5. Logs to Notion with "Posted ✅ (TEST)" status
6. Closes browser tabs

**Expected result:**
- Post appears in Build Room
- Log appears in Notion DB with link

---

## Test Mode Configuration

File: `config.json`

```json
{
  "test_mode": true,                    // Set to false for production
  "test_communities": ["buildroom"],    // Communities for testing
  "test_limits": {
    "posts_per_day": 3,                 // Max posts in test mode
    "comments_per_day": 10              // Max comments in test mode
  }
}
```

**In test mode:**
- Only posts to Build Room
- Ignores rotation system
- Limited to 3 posts + 10 comments per day
- Notion logs marked "(TEST)"

---

## Testing Phases

### Phase 1: Manual Verification (This Week)

**Goal:** Verify browser automation + formatting + voice

**Tasks:**
1. Run `test_post_buildroom.py` 2-3 times
2. Check Build Room for posts
3. Verify:
   - ✅ Formatting (sentence per paragraph)
   - ✅ Voice (matches Build Room engagement style)
   - ✅ No duplicate posts
   - ✅ Browser closes tabs properly
   - ✅ Notion log created with correct URL

### Phase 2: Automated Test Mode (Next 3-5 Days)

**Goal:** Run cron in test mode, monitor output

**Enable crons:**
```bash
# Add to /data/.openclaw/cron/jobs.json
{
  "id": "77d52982-test",
  "name": "Skool Posts (TEST)",
  "schedule": "0 9 * * *",  // 9am daily
  "command": "cd /data/.openclaw/workspace/agents/skoolposts && python3 skool_posts_cron.py"
}
```

**What happens:**
- 9am: Posts 3x to Build Room (staggered)
- 10am: Comments 10x in Build Room (staggered)
- All logged to Notion

**Monitor:**
- Build Room activity
- Notion log (check URLs work, text looks good)
- No errors in cron logs

### Phase 3: Production Ramp (After Test Mode Success)

**Goal:** Scale to all 13 communities

**Steps:**
1. Set `test_mode: false` in `config.json`
2. Crons will now:
   - Pick 5 communities daily (weighted rotation)
   - Post 5x across different communities
   - Comment 30x across 5-6 communities
3. Monitor Notion log for quality
4. Adjust voice per community as needed

---

## Browser Automation Notes

**Current implementation:**
- Uses OpenClaw browser tool (headless Chromium)
- Profile: "openclaw"
- Login once per session
- Single tab per community (sequential navigation)
- Closes tabs after each batch

**Known issues to watch for:**
- Skool UI changes (selectors may break)
- Login challenges (captcha, 2FA)
- Slow page loads (timeouts)

**Fallback:**
If browser automation fails, cron logs error to Notion and skips that post/comment.

---

## Notion Log Format

**Properties:**
- **Community:** (select) Which community
- **Type:** Post or Comment
- **Status:** Posted ✅ or Posted ✅ (TEST)
- **Posted:** Timestamp
- **URL:** Link to actual Skool post/comment

**Page body:** Full text of what was posted

---

## Troubleshooting

**Test script fails at browser step:**
- Check browser is installed: `openclaw browser status`
- Try manual login: Navigate to skool.com/login in browser, verify credentials work

**Post appears but Notion log missing:**
- Check `NOTION_TOKEN` in .env
- Verify DB ID in config.json matches Skool Posts DB

**Voice doesn't match community:**
- Update `SKOOL_POSTING_STRATEGY.md` with correct voice rules
- Agent reads this file before generating content

**Browser leaves tabs open:**
- Check `close_all_tabs()` is called at end of cron
- May need manual cleanup if script crashes

---

## Next Steps

1. ✅ Run manual test (`test_post_buildroom.py`)
2. ⏳ Verify formatting + voice in Build Room
3. ⏳ Enable test mode crons (9am posts, 10am comments)
4. ⏳ Monitor for 3-5 days
5. ⏳ Switch to production mode (`test_mode: false`)
6. ⏳ Monitor Notion log across all communities
7. ⏳ Adjust voice/formatting as needed

---

**Status:** Ready for manual testing ✅

Run `test_post_buildroom.py` when ready.
