#!/bin/bash
# Nightly backup to GitHub
cd /data/.openclaw/workspace
export $(grep -v '^#' .env | grep -v '^$' | xargs)
git add -A
git diff --cached --quiet && exit 0  # nothing to commit
git commit -m "nightly backup — $(date +%Y-%m-%d)"
git push origin main
