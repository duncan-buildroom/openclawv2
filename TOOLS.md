# TOOLS.md - Local Notes

## Credentials Policy
**All credentials, API keys, and access tokens live in `.env` ONLY.**
- Never store secrets in any other file
- `.env` is gitignored — never committed
- Reference with: `export $(grep -v '^#' .env | grep -v '^$' | xargs)`

## GitHub
- Repo: duncan-buildroom/openclawv2
- Nightly backup via heartbeat (after midnight ET)
- Script: scripts/nightly-backup.sh

## Telegram
- Bot token in `.env` (referenced by openclaw config)
- Duncan's user ID: 1709288760
