# Lead Magnet: OpenClaw Use Cases
**File:** `lead_magnet_openclaw_use_cases.json`

## What's Inside
- **83 Notion blocks** — valid, push-ready JSON
- **15 use cases** with copy-paste system prompts
- **6 Duncan proof points** embedded as blue callouts
- **Quick reference table** (15 rows, 5 columns)
- **CTA callout** → skool.com/buildroom

## Block Breakdown
| Type | Count | Purpose |
|------|-------|---------|
| paragraph | 32 | Body copy + metadata lines |
| callout | 25 | System prompts (gray) + Duncan results (blue) + hero + CTA |
| heading_3 | 15 | One per use case |
| heading_2 | 3 | Section headers |
| bulleted_list_item | 4 | CTA benefit bullets |
| divider | 3 | Section breaks |
| table | 1 | Quick reference (with 16 child rows: 1 header + 15 data) |

## Design Spec
| Element | Notion Color |
|---------|-------------|
| Hero callout | blue_background |
| System prompts | gray_background |
| Duncan's results | blue_background |
| Easy difficulty label | green text |
| Medium difficulty label | yellow text |
| Advanced difficulty label | red text |
| CTA callout | purple_background |

## Word Count
- **All content (incl. prompts):** ~2,350 words
- **Body copy only:** ~1,400 words ✅ (prompts are functional configs, not prose)

## Use Cases Index
| # | Use Case | Difficulty | Setup |
|---|---------|-----------|-------|
| 1 | Morning Intelligence Briefing | 🟢 Easy | 20 min |
| 2 | Email Triage Agent | 🟢 Easy | 20 min |
| 3 | Trend Research Pipeline | 🟡 Medium | 45 min |
| 4 | Content Repurposing Agent | 🟢 Easy | 15 min |
| 5 | Social Media Publishing Agent | 🟡 Medium | 30 min |
| 6 | Lead Magnet Generator | 🟢 Easy | 10 min |
| 7 | Proposal Generator | 🟢 Easy | 10 min |
| 8 | Client Onboarding Automation | 🟡 Medium | 45 min |
| 9 | Client Check-In Automation | 🟡 Medium | 30 min |
| 10 | Lead Discovery & CRM Enrichment | 🔴 Advanced | 60 min |
| 11 | Interview & Sales Call Research Brief | 🟢 Easy | 15 min |
| 12 | Calendar Management Agent | 🟡 Medium | 25 min |
| 13 | Daily Revenue & Cost Recap | 🟡 Medium | 30 min |
| 14 | GitHub Workspace Backup (Cron) | 🟢 Easy | 15 min |
| 15 | End-of-Day Shutdown Routine | 🟢 Easy | 15 min |

## How to Push to Notion
**Remove the `_meta` key first**, then either:

### Option A: Direct API
```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d @lead_magnet_openclaw_use_cases.json
```
Add `"parent": {"page_id": "YOUR_PAGE_ID"}` to the JSON first.

### Option B: push_analysis.py
Pass the `children` array to whatever push function is configured.

**Note on table rows:** The table block includes `children` (the rows) inline in the JSON. The Notion API accepts this format in a single create call — rows are created as children of the table block.
