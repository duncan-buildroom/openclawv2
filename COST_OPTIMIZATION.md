# Cost Optimization Strategy

**Philosophy:** Work smarter, not more expensive.

---

## Current Setup

**Default Model:** Gemini 3 Flash Preview
- **Cost:** $0.075 input / $0.30 output per 1M tokens
- **Savings:** 90% cheaper than Claude Sonnet 4.6 ($3/$15)
- **Use for:** Daily interactions, routine tasks, most work

**When to Use Expensive Models:**
- **Claude Opus 4.6** ($15/$75): Complex reasoning, architecture, critical debugging
- **Claude Sonnet 4.5** ($3/$15): Code generation, important decisions
- **Rule:** Only when Gemini can't handle it

---

## Immediate Wins

### 1. Batch Operations

❌ **Bad:** Multiple tool calls for similar tasks
```python
read("file1.py")
read("file2.py")
read("file3.py")
```

✅ **Good:** Single batch operation
```bash
cat file1.py file2.py file3.py
```

### 2. Use Local Tools First

❌ **Bad:** Web search for documented info
✅ **Good:** Check local docs, memory, then search

### 3. Spawn Cheap Sub-Agents

```python
sessions_spawn(
    task="Generate 10 Twitter thread ideas from carousel",
    model="google/gemini-3-flash-preview",  # Cheap model
    cleanup="delete"  # Auto-cleanup
)
```

### 4. Cache Strategy

- Save API responses to `/tmp/` for reuse
- Don't re-fetch unchanged data
- Use memory_search before re-reading full MEMORY.md

---

## Skills to Create

### High-Impact Skills

**1. Batch Image Processor**
- Process multiple images in one script
- Avoid repeated Python interpreter startup
- **Saves:** 50-70% on multi-image tasks

**2. Smart Memory Manager**
- Only load relevant MEMORY.md sections
- Cache search results
- **Saves:** 30-40% on context loading

**3. Local Content Generator**
- Templates for common outputs (Twitter threads, LinkedIn posts)
- No LLM needed for structure
- **Saves:** 80-90% on templated content

**4. Cron Job Optimizer**
- Batch multiple checks into one heartbeat
- Use cheapest model for monitoring
- **Saves:** 60-70% on automated tasks

### Medium-Impact

**5. Screenshot Batcher**
- Capture multiple browser screenshots in one session
- Reuse browser connection
- **Saves:** 20-30% on multi-capture workflows

**6. Notion Bulk Operations**
- Update multiple pages in single API call
- **Saves:** 40-50% on Notion operations

---

## Cost Tracking

**Daily Cost Tracker:** `daily_cost_tracker.py`
- Monitors Opus, Sonnet, Gemini, image costs
- Outputs to `/tmp/daily_llm_cost.json`
- Syncs to Notion daily tracker

**Current Feb 13 Costs:**
- Total: $1.77 (all Sonnet)
- Token usage: 2,297 in / 117,612 out

**Target:** <$5/day for normal operations

---

## Best Practices

### Before Every Task, Ask:

1. **Can this use Gemini instead of Claude?**
2. **Can I batch multiple operations?**
3. **Is there a local tool instead of API?**
4. **Can a sub-agent handle this cheaper?**
5. **Do I really need to re-read this file?**

### Red Flags (Cost Traps)

- ⚠️ Multiple small file reads → batch them
- ⚠️ Re-reading MEMORY.md → use memory_search
- ⚠️ Creating many images → use batch script
- ⚠️ Repeated web searches → cache results
- ⚠️ Using Opus for simple tasks → spawn Gemini sub-agent

### Green Flags (Good Patterns)

- ✅ One script processes 10 images
- ✅ Memory search before full read
- ✅ Batched API calls
- ✅ Local processing over LLM generation
- ✅ Sub-agents for parallelization

---

## Model Selection Guide

**Gemini 3 Flash Preview** (default)
- Daily chat, questions, planning
- File operations, code execution
- Simple image generation
- 90% of tasks

**Claude Sonnet 4.6** (when needed)
- Complex code generation
- Multi-step reasoning
- Important documentation
- 8% of tasks

**Claude Opus 4.6** (rare)
- Critical architecture decisions
- Advanced debugging
- Complex agent work
- 2% of tasks

---

## Action Items

**This Week:**
- [ ] Create batch image processor skill
- [ ] Optimize MEMORY.md loading (use memory_search always)
- [ ] Set up result caching for common queries
- [ ] Review all cron jobs for model usage

**This Month:**
- [ ] Build template library for common content
- [ ] Implement smart sub-agent spawning
- [ ] Create cost monitoring dashboard
- [ ] Document all cost-saving patterns

**Goal:** <$3/day average by end of February
