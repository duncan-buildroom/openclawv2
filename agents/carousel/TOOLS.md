# TOOLS.md - Carousel Agent Local Notes

## Key References

### n8n Instance
- **URL:** `https://duncanrogoff.app.n8n.cloud/`
- Used for: Real workflow screenshots in carousels
- Screenshots are captured by the orchestrator, NOT this agent
- When specifying `SCREENSHOT_NEEDED:`, describe which workflow and what view to capture

### GitHub: 30 Automations Repo
- **URL:** `https://github.com/duncan-buildroom/n8n-automations`
- Contains all 30 production n8n workflows
- Reference for automation names, descriptions, and capabilities

### Duncan's Likeness Reference
- **Imgur:** `https://i.imgur.com/vc7pPOC.jpeg`
- 4-angle reference sheet (front, side, back, three-quarter)
- Orange hoodie is signature outfit
- Used by imgen agent for character shots

### Visual Theme Bank
- **File:** `/data/.openclaw/workspace/CAROUSEL_THEMES.md`
- **MUST READ** before every carousel — contains 50 themes + recent history
- Never repeat a theme from the last 5 carousels

### Process Doc
- **File:** `/data/.openclaw/workspace/CAROUSEL_PROCESS.md`
- Single source of truth for the full carousel pipeline

## Fixed Slide Structure (every 7-slide carousel)
| Slide | Role | Shot Type |
|-------|------|-----------|
| 1 | Hook | character |
| 2 | Problem/context | establishing or detail |
| 3 | Solution + workflow | **screenshot** (real n8n) |
| 4 | How it works | **infographic (ALWAYS)** |
| 5-6 | Proof/details | character, detail, or establishing |
| 7 | CTA | composite or character |

- Slide 4 is ALWAYS an infographic. Non-negotiable.
- CTA: "Comment 'AI' to get access to all 30 automations"

## Notion
- **Carousels DB:** `cf399acfd5aa479c86b92cdea1d819d7`
- Pushed by orchestrator after QA — not this agent's job

## Imgur
- **Client ID:** `546c25a59c58ad7` (anonymous uploads)
- Uploaded by orchestrator/imgen — not this agent's job
