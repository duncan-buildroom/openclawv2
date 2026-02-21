# AI Dream Team — Agent Architecture

## System Overview

```
                    ┌─────────────────┐
                    │                 │
                    │  ORCHESTRATOR   │
                    │  (main agent)   │
                    │                 │
                    └────────┬────────┘
                             │
                             │ Routes & coordinates
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│               │    │               │    │               │
│  RESEARCHER   │───▶│    WRITER     │    │  CHIEF OF     │
│               │    │               │    │    STAFF      │
└───────────────┘    └───────┬───────┘    └───────────────┘
                             │
                             │ Hands off to
                             ▼
                     ┌───────────────┐
                     │               │
                     │    BUILDER    │
                     │               │
                     └───────────────┘
```

## Agent Roles

### 🧠 Orchestrator
**Never executes. Only routes.**

- Receives user request
- Analyzes task requirements
- Selects appropriate specialist
- Coordinates multi-step workflows
- Delivers final results to user

**Spawn triggers:**
- Complex tasks requiring specialist knowledge
- Multi-step workflows (research → write → build)
- Any task that fits a specialist's domain

### 🔍 Researcher
**Intel engine.**

**Domain:**
- Web research
- Trend analysis
- Competitive intelligence
- Topic deep-dives
- Source aggregation

**Input:** Topic, depth, output format, specific questions  
**Output:** Structured brief with sources

**Typical workflow:**
1. Search web (Brave API)
2. Fetch relevant pages
3. Synthesize findings
4. Cite sources
5. Return actionable brief

### ✍️ Writer
**Content creation specialist.**

**Domain:**
- Social media (Twitter, LinkedIn, etc.)
- Email sequences
- Blog posts and articles
- Landing pages
- Scripts and video content
- Ad copy

**Input:** Content type, topic, context/research, tone, constraints  
**Output:** Ready-to-publish copy

**Typical workflow:**
1. Read research (if provided)
2. Adapt to user's voice (from USER.md)
3. Write platform-optimized content
4. Include hooks, CTAs, formatting
5. Return polished copy

### 📋 Chief of Staff
**Operations manager.**

**Domain:**
- Daily briefings
- Task tracking
- Meeting prep
- Decision logging
- Progress summaries
- Blocker identification

**Input:** Request type, timeframe, context, focus areas  
**Output:** Structured briefings with action items

**Typical workflow:**
1. Check calendar/memory files
2. Review recent progress
3. Flag priorities and blockers
4. Deliver concise briefing
5. Track decisions/commitments

**Special:** Can run automated (cron/heartbeat) for morning briefings

### 🔧 Builder
**Technical implementation.**

**Domain:**
- Code (scripts, apps, tools)
- Automation workflows
- System design
- Debugging
- API integrations

**Input:** Project description, requirements, tech stack, input/output, context  
**Output:** Working code with docs

**Typical workflow:**
1. Understand requirements
2. Choose tech stack
3. Write code
4. Test functionality
5. Document setup/usage
6. Return complete package

## Multi-Agent Workflow Patterns

### Pattern 1: Research → Write
```
User: "Write a Twitter thread about AI agents"
  ↓
Orchestrator: Spawn Researcher
  ↓
Researcher: Finds trends, examples, use cases
  ↓
Orchestrator: Spawn Writer with research
  ↓
Writer: Creates 10-tweet thread
  ↓
User: Receives polished thread
```

### Pattern 2: Write → Build
```
User: "Build a landing page for my product"
  ↓
Orchestrator: Spawn Writer
  ↓
Writer: Creates landing page copy
  ↓
Orchestrator: Spawn Builder with copy
  ↓
Builder: Builds HTML/CSS page
  ↓
User: Receives working page
```

### Pattern 3: Research → Write → Build
```
User: "Create a lead magnet with landing page"
  ↓
Orchestrator: Spawn Researcher (topic intel)
  ↓
Researcher: Returns competitive analysis
  ↓
Orchestrator: Spawn Writer (create content)
  ↓
Writer: Returns lead magnet copy
  ↓
Orchestrator: Spawn Builder (build page)
  ↓
Builder: Returns working landing page
  ↓
User: Receives complete package
```

### Pattern 4: Chief (Recurring)
```
Cron: 8:00 AM daily
  ↓
Chief: Check calendar, review yesterday
  ↓
Chief: Identify priorities, flag blockers
  ↓
User: Receives morning briefing
```

## Communication Protocol

### Orchestrator → Specialist
```
[Agent name]: [Clear task description]

Input: [What they're working with]
Output: [Exact deliverable expected]
Constraints: [Any limits/requirements]
```

### Specialist → Orchestrator
```
[Deliverable]

[Any context the user needs to know]
```

### Orchestrator → User
```
[Final result or summary]

[Process overview if helpful]
```

## Upgrade Agents (Future)

### 📱 Publisher
**Social media automation**
- Auto-posts to platforms
- Scheduling optimization
- Cross-platform formatting
- Analytics tracking

### 🎨 Designer
**Visual content creation**
- Graphics and branded assets
- Slide decks
- Social media visuals
- Brand consistency

### 🎯 Strategist
**High-level planning**
- Quarterly goal setting
- Strategic analysis
- Market positioning
- Long-term roadmapping

### 📊 Analyst
**Data and metrics**
- Performance tracking
- A/B test analysis
- Growth metrics
- Reporting dashboards

## File Structure

```
/main/
  SOUL.md        ← Orchestrator identity
  AGENTS.md      ← Registry of specialists
  USER.md        ← User profile and preferences
  TOOLS.md       ← Local configs

/researcher/
  SOUL.md        ← Researcher identity
  TOOLS.md       ← Preferred sources, search patterns

/writer/
  SOUL.md        ← Writer identity
  TOOLS.md       ← Voice profile, successful hooks

/chief/
  SOUL.md        ← Chief of Staff identity
  TOOLS.md       ← Recurring events, key contacts

/builder/
  SOUL.md        ← Builder identity
  TOOLS.md       ← Tech preferences, deployment targets
```

## Memory System

```
/main/memory/
  2026-02-15.md  ← Daily log (today)
  2026-02-14.md  ← Daily log (yesterday)
  ...
  MEMORY.md      ← Long-term curated memory (main session only)
```

Each agent reads:
1. Their SOUL.md (who they are)
2. USER.md (who they're helping)
3. Recent memory files (context)

## Operating Costs

**Baseline (5 agents):**
- ~$5/day with moderate usage
- GPT-4 level models
- Includes research API calls (Brave Search)

**Scales with:**
- Number of tasks per day
- Complexity of workflows
- Length of outputs
- Frequency of briefings

## Real-World Performance

**Duncan's system (6 agents, 24/7):**
- Replaces: VA + designer + social media manager
- Built in: ~2 weeks
- Results: 110K+ followers, full business automation
- Cost: ~$5/day

## Key Principles

1. **Specialization:** Each agent does one thing extremely well
2. **Coordination:** Orchestrator handles handoffs
3. **Context:** Tight scope, clear inputs/outputs
4. **Memory:** Agents learn and improve over time
5. **Scalability:** Add specialists as needed

---

**This is not theory. This is the working architecture Duncan uses daily.**
