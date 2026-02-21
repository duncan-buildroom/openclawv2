# AGENTS.md - Sub-Agent Registry

This is the orchestrator's directory. Add every sub-agent here.

---

## [agent_name]
**Purpose:** [One-line description]  
**Triggers:** [Keywords or patterns]  
**Inputs:**  
- `input_1` (required/optional) — [description]  
- `input_2` (required/optional) — [description]  
**Outputs:**  
- [What it returns, where it saves files]  

---

## [agent_name]
**Purpose:** [One-line description]  
**Triggers:** [Keywords or patterns]  
**Inputs:**  
- `input_1` (required/optional) — [description]  
**Outputs:**  
- [What it returns]

---

## Example: carousel
**Purpose:** Generate Instagram/LinkedIn carousel posts  
**Triggers:** "carousel", "create slides", "social post"  
**Inputs:**  
- `topic` (required)  
- `audience` (optional)  
- `tone` (optional)  
**Outputs:**  
- JSON array of slides  
- Saved to `output/carousel-{date}-{topic}.json`

---

## Example: briefer
**Purpose:** Daily morning briefing (calendar, email, mentions)  
**Triggers:** Cron job (8 AM daily) or "brief me"  
**Inputs:** None (pulls from calendar/email APIs)  
**Outputs:**  
- Markdown summary sent to Telegram

---

## Example: publisher
**Purpose:** Post content to social platforms  
**Triggers:** "publish", "post this"  
**Inputs:**  
- `content` (required) — Copy or image path  
- `platforms` (required) — e.g., ["instagram", "linkedin"]  
**Outputs:**  
- Confirmation + post URLs
