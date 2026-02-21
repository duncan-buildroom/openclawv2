# Agent Architecture

## Orchestrator (main)
**Location:** `/data/.openclaw/workspace`
**Model:** Gemini 3 Flash Preview (default)
**Role:** Task router. Does not execute tasks directly — delegates to specialized sub-agents.

---

## Sub-Agents

All sub-agents live in `/data/.openclaw/workspace/agents/<agent-id>/`

### Content Creation Agents

| Agent ID | Name | Model | Purpose |
|----------|------|-------|---------|
| `carousel` | Carousel Content | Claude Sonnet 4.5 | Instagram/TikTok carousel content (copy + image concepts) |
| `threads` | X/Twitter Agent | Gemini Flash | X/Twitter threads, tweets, replies, engagement |
| `linkedin` | LinkedIn Agent | Gemini Flash | LinkedIn content and publishing |
| `skoolposts` | Skool Posts Agent | Gemini Flash | Skool community posts |
| `leadmagnet` | Lead Magnet Creator | Claude Sonnet 4.5 | Lead magnet creation and Notion publishing |

### Specialized Agents

| Agent ID | Name | Model | Purpose |
|----------|------|-------|---------|
| `briefer` | Daily Briefer | Gemini Flash | Daily morning briefing generation |
| `imgen` | Image Generator | Gemini Flash | Carousel image generation |
| `coder` | Code Generator | Claude Sonnet 4.5 | Code generation and debugging |
| `publisher` | Content Publisher | Gemini Flash | Cross-platform content publishing |
| `repurpose` | Content Repurposer | Gemini Flash | Content repurposing across platforms |
| `trendanalyst` | Trend Analyst | Claude Sonnet 4.5 | Trend analysis and reporting |
| `reddit` | Reddit Agent | Gemini Flash | Reddit monitoring and engagement |
| `roadto1m` | Road to 1M Agent | Gemini Flash | Road to 1M curriculum content |

---

## Model Assignment Strategy

**Gemini 3 Flash Preview** (90% cheaper)
- Daily interactions
- Content publishing
- Monitoring/engagement
- Simple content generation

**Claude Sonnet 4.5** (when quality matters)
- Complex content (carousels, lead magnets)
- Code generation
- Strategic analysis
- Architecture decisions

**Claude Opus 4.6** (rare, orchestrator only)
- Critical debugging
- Complex multi-agent orchestration
- Strategic planning

---

## How to Spawn Sub-Agents

From the orchestrator:

```python
sessions_spawn(
    agentId="carousel",
    task="Create a 7-slide carousel about AI automation. Hook: contrarian. Output JSON with slide_number, text, image_concept fields.",
    cleanup="delete"  # Auto-cleanup after completion
)
```

Available agent IDs:
- `briefer`
- `carousel`
- `threads`
- `coder`
- `imgen`
- `leadmagnet`
- `linkedin`
- `publisher`
- `reddit`
- `repurpose`
- `roadto1m`
- `skoolposts`
- `trendanalyst`

---

## File Structure

```
/data/.openclaw/workspace/
├── SOUL.md                    # Orchestrator identity
├── USER.md                    # Duncan's profile
├── TOOLS.md                   # Credentials and tool notes
├── HEARTBEAT.md               # Nightly backup config
├── COST_OPTIMIZATION.md       # Cost strategy
├── memory/                    # Daily memory logs
├── scripts/                   # Utility scripts
└── agents/                    # All sub-agents
    ├── briefer/
    │   ├── SOUL.md
    │   └── daily_briefing.py
    ├── carousel/
    │   ├── SOUL.md
    │   └── [carousel data files]
    ├── threads/
    │   ├── SOUL.md
    │   ├── X_ACTION_PLAN.md
    │   └── [X/Twitter scripts]
    └── [... other agents ...]
```

---

## Configuration

Sub-agents are configured in `~/.openclaw/openclaw.json` under `agents.list[]`.

Key fields:
- `id`: Agent identifier (must match folder name)
- `name`: Human-readable name
- `workspace`: Absolute path to agent workspace
- `model.primary`: Model assignment

Orchestrator's `subagents.allowAgents` lists all spawnable agents.
