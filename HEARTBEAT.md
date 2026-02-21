# HEARTBEAT.md

## Nightly Backup (run once per day, after midnight ET)
- Check if a git backup has been done today (look at memory/heartbeat-state.json lastChecks.backup)
- If not done today and it's after midnight: run `cd /data/.openclaw/workspace && export $(grep -v '^#' .env | grep -v '^$' | xargs) && git add -A && git diff --cached --quiet || (git commit -m "nightly backup — $(date +%Y-%m-%d)" && git push origin main)`
- Update heartbeat-state.json with timestamp
- Only notify Duncan if the backup fails
