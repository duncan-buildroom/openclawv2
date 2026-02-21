# TOOLS.md - Local Notes

## Credentials Policy
**All credentials, API keys, and access tokens live in `.env` ONLY.**
- Never store secrets in any other file
- `.env` is gitignored — never committed
- Reference with: `export $(grep -v '^#' .env | grep -v '^$' | xargs)`

**Credentials in `.env`:**
- `GITHUB_PAT` / `GITHUB_REPO` - GitHub backup
- `GOOGLE_API_KEY` - Gemini, Nano Banana Pro, memory search
- `NOTION_TOKEN` - Notion API integration
- `BLOTATO_API_KEY` - Social media publishing
- `N8N_INSTANCE` - n8n workflow instance URL
- `KIMI_BOT_TOKEN` - Kimi AI (primary model for all agents)
- `ANTHROPIC_API_KEY` - Claude API (legacy, not actively used)
- Telegram bot token (in openclaw config)

**Claude Authentication:**
- Primary: Claude Max setup-token (OAuth) via `anthropic:default` profile
- Fallback: API key from `ANTHROPIC_API_KEY` env var
- Automatic fallback on rate limits/409 errors
- Auth order configured in `/data/.openclaw/agents/main/agent/auth-profiles.json`

## GitHub
- Repo: duncan-buildroom/openclawv2
- Nightly backup via heartbeat (after midnight ET)
- Script: scripts/nightly-backup.sh

## Telegram
- Bot token in `.env` (referenced by openclaw config)
- Duncan's user ID: 1709288760
