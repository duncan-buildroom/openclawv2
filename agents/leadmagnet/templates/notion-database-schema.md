# Notion Database Schemas for Multi-Agent Systems

## 1. Engagement Tracking Database

**Purpose:** Track social media performance metrics automatically

### Properties

| Property Name | Type | Description | Formula/Options |
|--------------|------|-------------|-----------------|
| Post Title | Title | Name of the content | - |
| Date | Date | When it was published | - |
| Platform | Select | Social platform | Instagram, LinkedIn, Twitter, Facebook, YouTube |
| Impressions | Number | Total views | - |
| Likes | Number | Likes/reactions | - |
| Comments | Number | Comment count | - |
| Shares | Number | Shares/reposts | - |
| Engagement Rate | Formula | Calculated engagement | `(prop("Likes") + prop("Comments") + prop("Shares")) / prop("Impressions") * 100` |
| Post URL | URL | Link to the post | - |
| Agent | Select | Which agent created it | carousel, threads, video, shorts, article |
| Status | Select | Content lifecycle | Draft, Published, Archived |
| Topic | Multi-select | Content categories | Productivity, AI, Business, Tech, Personal |
| Created By | Created by | Auto-populated | - |
| Last Updated | Last edited time | Auto-populated | - |

---

## 2. Content Pipeline Database

**Purpose:** Track content from idea → creation → publication

### Properties

| Property Name | Type | Description | Formula/Options |
|--------------|------|-------------|-----------------|
| Content Idea | Title | The core concept | - |
| Status | Status | Pipeline stage | Idea, In Progress, Review, Scheduled, Published |
| Format | Select | Content type | Carousel, Thread, Video, Article, Newsletter |
| Platform | Multi-select | Where to publish | Instagram, LinkedIn, Twitter, YouTube, Blog |
| Agent Assigned | Select | Which agent handles it | carousel, imgen, threads, video, publisher |
| Deadline | Date | Target publish date | - |
| Priority | Select | Urgency level | High, Medium, Low |
| Output Path | Text | File location | - |
| Published URL | URL | Live link | - |
| Notes | Text | Additional context | - |

---

## 3. Agent Activity Log Database

**Purpose:** Track all agent actions for debugging and optimization

### Properties

| Property Name | Type | Description | Formula/Options |
|--------------|------|-------------|-----------------|
| Activity | Title | What the agent did | - |
| Timestamp | Created time | When it happened | Auto-populated |
| Agent | Select | Which agent | orchestrator, carousel, imgen, briefer, publisher, engagement, leadmagnet |
| Status | Select | Result | Success, Failed, Partial |
| Input | Text | What was requested | - |
| Output | Text | What was delivered | - |
| Tokens Used | Number | API token count | - |
| Cost | Number | Estimated cost ($) | - |
| Duration (sec) | Number | How long it took | - |
| Error Log | Text | If failed, why? | - |

---

## 4. Memory & Learnings Database

**Purpose:** Store long-term insights from MEMORY.md

### Properties

| Property Name | Type | Description | Formula/Options |
|--------------|------|-------------|-----------------|
| Insight | Title | The key learning | - |
| Date | Date | When it was learned | - |
| Category | Select | Type of insight | User Preference, Decision, Mistake, Optimization, Project Milestone |
| Source | Text | Where it came from | e.g., "2026-02-15 carousel failure" |
| Impact | Select | Importance level | High, Medium, Low |
| Applied | Checkbox | Is this actively used? | - |
| Notes | Text | Additional context | - |

---

## Setup Instructions

1. **Create databases in Notion:**
   - Go to your workspace
   - Create a new database for each schema above
   - Add the properties exactly as listed

2. **Connect to agents:**
   - Get your Notion API key (Settings → Integrations)
   - Share the databases with your integration
   - Add database IDs to your agent configs

3. **Automate updates:**
   - Engagement agent populates Engagement Tracking daily
   - Publisher agent updates Content Pipeline on publish
   - All agents log to Activity Log on every action
   - Main agent syncs MEMORY.md to Memory & Learnings weekly

4. **Create views:**
   - **Engagement Tracking:** Gallery by Platform, Table by Date
   - **Content Pipeline:** Kanban by Status, Calendar by Deadline
   - **Agent Activity:** Timeline by Agent, List by Status
   - **Memory & Learnings:** Table by Category, List by Impact

---

## Example API Integration (Python)

```python
import requests

NOTION_API_KEY = "your_api_key_here"
DATABASE_ID = "your_database_id_here"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Example: Log engagement data
data = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Post Title": {"title": [{"text": {"content": "My Carousel About AI"}}]},
        "Date": {"date": {"start": "2026-02-15"}},
        "Platform": {"select": {"name": "Instagram"}},
        "Impressions": {"number": 2300},
        "Likes": {"number": 145},
        "Comments": {"number": 23},
        "Shares": {"number": 12},
        "Post URL": {"url": "https://instagram.com/p/example"},
        "Agent": {"select": {"name": "carousel"}}
    }
}

response = requests.post(
    "https://api.notion.com/v1/pages",
    headers=headers,
    json=data
)

print(response.json())
```

---

Your agents will now automatically populate these databases, giving you a living dashboard of your entire content system.
