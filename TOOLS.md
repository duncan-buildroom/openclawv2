# TOOLS.md - Local Notes

## Credentials Policy

**Two-tier system:**

### 1. LLM Provider Keys → `auth-profiles.json`
**Location:** `/data/.openclaw/agents/main/agent/auth-profiles.json`
**What goes here:** Any API key or OAuth token for model providers
- Anthropic (Claude) - OAuth via Claude Max
- Google (Gemini) - API key
- Kimi - API key
- OpenAI - API key (if added)
- Any other LLM provider

**Why:** OpenClaw's native auth system. Handles fallbacks, rate limits, provider routing.

### 2. Third-Party Service Keys → `.env`
**Location:** `/data/.openclaw/workspace/.env`
**What goes here:** Non-LLM service credentials
- `GITHUB_PAT` / `GITHUB_REPO` - GitHub backup
- `NOTION_TOKEN` - Notion API integration
- `BLOTATO_API_KEY` - Social media publishing
- `N8N_INSTANCE` - n8n workflow instance URL
- Telegram bot token (in openclaw config)

**Why:** Single source of truth for third-party integrations. Gitignored, never committed.

**Reference .env:** `export $(grep -v '^#' .env | grep -v '^$' | xargs)`

**Claude Authentication:**
- Primary: Claude Max OAuth via `anthropic:default` profile
- Fallback: API key via `anthropic:fallback` profile
- Automatic fallback on rate limits/409 errors
- Auth order configured in `/data/.openclaw/agents/main/agent/auth-profiles.json`

## GitHub
- Repo: duncan-buildroom/openclawv2
- Nightly backup via heartbeat (after midnight ET)
- Script: scripts/nightly-backup.sh

## Telegram
- Bot token in `.env` (referenced by openclaw config)
- Duncan's user ID: 1709288760
