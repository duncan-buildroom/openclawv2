#!/bin/bash
# Cron Job Templates for Multi-Agent Systems
# Add these to your crontab with: crontab -e

# DAILY BRIEFING
# Runs every day at 8:00 AM
# Sends calendar, email, and social mentions summary to Telegram
0 8 * * * /usr/bin/openclaw agent:briefer --message "Generate daily briefing" >> /var/log/briefer.log 2>&1

# ENGAGEMENT TRACKING
# Runs every day at 11:00 PM
# Scrapes social media metrics and logs to Notion
0 23 * * * /usr/bin/openclaw agent:engagement --message "Track today's engagement" >> /var/log/engagement.log 2>&1

# WEEKLY REPORT
# Runs every Monday at 9:00 AM
# Compiles the week's insights and trends
0 9 * * 1 /usr/bin/openclaw agent:briefer --message "Generate weekly report" >> /var/log/weekly.log 2>&1

# BACKUP OUTPUTS
# Runs daily at midnight
# Backs up all agent outputs to cloud storage
0 0 * * * rsync -av /workspace/output/ /backup/agent-outputs/ >> /var/log/backup.log 2>&1

# MEMORY MAINTENANCE
# Runs every Sunday at 10:00 PM
# Reviews recent memory files and updates MEMORY.md
0 22 * * 0 /usr/bin/openclaw agent:main --message "Review and update MEMORY.md from recent daily files" >> /var/log/memory.log 2>&1

# CONTENT QUEUE CHECK
# Runs every 2 hours during business hours (9 AM - 7 PM)
0 9-19/2 * * * /usr/bin/openclaw agent:publisher --message "Check scheduled content queue" >> /var/log/publisher.log 2>&1

# NOTION SYNC
# Runs every 6 hours
# Syncs agent outputs with Notion databases
0 */6 * * * /usr/bin/openclaw agent:notion-sync --message "Sync outputs to Notion" >> /var/log/notion.log 2>&1

# ---
# CRON SYNTAX REMINDER:
# * * * * * command
# │ │ │ │ │
# │ │ │ │ └─── day of week (0-7, 0 and 7 = Sunday)
# │ │ │ └───── month (1-12)
# │ │ └─────── day of month (1-31)
# │ └───────── hour (0-23)
# └─────────── minute (0-59)
#
# Use https://crontab.guru to validate your schedules
