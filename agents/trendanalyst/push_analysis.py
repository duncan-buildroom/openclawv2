import os
#!/usr/bin/env python3
"""Push trend analysis to Notion with beautiful formatting.

Usage:
  echo '{"ranked_content_angles": [...], ...}' | python3 push_analysis.py YYYY-MM-DD [PAGE_ID]

Accepts both the new flat format (ranked_content_angles, etc.) and the legacy
sections-based format. Auto-detects based on whether a "sections" key exists.
"""

import sys, json, os, re, glob, html, requests

NOTION_DB_ID = "308f259c-0f17-8161-abe2-e074a065d10e"
REPORT_DIR = "/data/.openclaw/workspace/trend-reports"

def get_token():
    return os.getenv("NOTION_TOKEN")

def hdrs(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

def t(text, max_len=2000):
    """Truncate and clean text."""
    if not text:
        return ""
    return html.unescape(str(text))[:max_len]

# ── Notion API helpers ───────────────────────────────────────────────────────

def find_page_by_date(token, date_str):
    url = f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query"
    r = requests.post(url, headers=hdrs(token), json={
        "filter": {"property": "Date", "date": {"equals": date_str}}
    })
    r.raise_for_status()
    results = r.json().get("results", [])
    return results[0]["id"] if results else None

def archive_page(token, page_id):
    """Archive (trash) a page."""
    r = requests.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=hdrs(token),
        json={"archived": True}
    )
    r.raise_for_status()
    print(f"🗑️  Archived old page {page_id}")

def create_fresh_page(token, date_str, properties_data):
    """Create a new page in the DB with properties."""
    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "icon": {"type": "emoji", "emoji": "📈"},
        "properties": properties_data,
        "children": []
    }
    r = requests.post("https://api.notion.com/v1/pages", headers=hdrs(token), json=payload)
    r.raise_for_status()
    page_id = r.json()["id"]
    print(f"📄 Created new page {page_id}")
    return page_id

def append_blocks(token, page_id, blocks):
    """Append blocks in batches of 100."""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    total = 0
    for i in range(0, len(blocks), 100):
        chunk = blocks[i:i+100]
        r = requests.patch(url, headers=hdrs(token), json={"children": chunk})
        r.raise_for_status()
        total += len(chunk)
    print(f"✅ Appended {total} blocks")

# ── Block builders ───────────────────────────────────────────────────────────

def heading_1(text):
    return {"object": "block", "type": "heading_1", "heading_1": {
        "rich_text": [{"type": "text", "text": {"content": t(text)}}]
    }}

def heading_3(text):
    return {"object": "block", "type": "heading_3", "heading_3": {
        "rich_text": [{"type": "text", "text": {"content": t(text)}}]
    }}

def paragraph(text, bold=False, italic=False):
    if not text:
        return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": []}}
    entry = {"type": "text", "text": {"content": t(text)}}
    ann = {}
    if bold: ann["bold"] = True
    if italic: ann["italic"] = True
    if ann: entry["annotations"] = ann
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [entry]}}

def rich_paragraph(segments):
    """segments = list of dicts with keys: text, bold, italic, color, link"""
    rt = []
    for seg in segments:
        txt = t(seg.get("text", ""))
        if not txt:
            continue
        entry = {"type": "text", "text": {"content": txt}}
        if seg.get("link"):
            entry["text"]["link"] = {"url": seg["link"]}
        ann = {}
        if seg.get("bold"): ann["bold"] = True
        if seg.get("italic"): ann["italic"] = True
        if seg.get("color"): ann["color"] = seg["color"]
        if ann: entry["annotations"] = ann
        rt.append(entry)
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rt}}

def bulleted(text):
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
        "rich_text": [{"type": "text", "text": {"content": t(text)}}]
    }}

def linked_bulleted(title, url, meta=""):
    rt = [{"type": "text", "text": {"content": t(title), "link": {"url": url}}, "annotations": {"bold": True}}]
    if meta:
        rt.append({"type": "text", "text": {"content": f"  {t(meta)}"}, "annotations": {"italic": True, "color": "gray"}})
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": rt}}

def numbered(text):
    return {"object": "block", "type": "numbered_list_item", "numbered_list_item": {
        "rich_text": [{"type": "text", "text": {"content": t(text)}}]
    }}

def rich_numbered(segments):
    rt = []
    for seg in segments:
        txt = t(seg.get("text", ""))
        if not txt:
            continue
        entry = {"type": "text", "text": {"content": txt}}
        ann = {}
        if seg.get("bold"): ann["bold"] = True
        if seg.get("italic"): ann["italic"] = True
        if seg.get("color"): ann["color"] = seg["color"]
        if ann: entry["annotations"] = ann
        rt.append(entry)
    return {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": rt}}

def callout(text, emoji="💡", color="gray_background"):
    return {"object": "block", "type": "callout", "callout": {
        "rich_text": [{"type": "text", "text": {"content": t(text)}}],
        "icon": {"type": "emoji", "emoji": emoji},
        "color": color
    }}

def rich_callout(segments, emoji="💡", color="gray_background"):
    rt = []
    for seg in segments:
        txt = t(seg.get("text", ""))
        if not txt:
            continue
        entry = {"type": "text", "text": {"content": txt}}
        ann = {}
        if seg.get("bold"): ann["bold"] = True
        if seg.get("italic"): ann["italic"] = True
        if seg.get("color"): ann["color"] = seg["color"]
        if ann: entry["annotations"] = ann
        rt.append(entry)
    return {"object": "block", "type": "callout", "callout": {
        "rich_text": rt,
        "icon": {"type": "emoji", "emoji": emoji},
        "color": color
    }}

def quote_block(text):
    return {"object": "block", "type": "quote", "quote": {
        "rich_text": [{"type": "text", "text": {"content": t(text)}}]
    }}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

# ── Source index parsing ─────────────────────────────────────────────────────

def parse_sources_from_reports(date_str):
    """Parse YouTube and Reddit sources from raw report files."""
    pattern = os.path.join(REPORT_DIR, f"{date_str}_*.txt")
    files = sorted(glob.glob(pattern))
    youtube_sources = []
    reddit_sources = []

    for filepath in files:
        with open(filepath) as f:
            content = html.unescape(f.read())

        is_youtube = "_youtube_" in os.path.basename(filepath)

        if is_youtube:
            # Parse YouTube video blocks
            blocks = re.split(r'(?=\*\*Y\d+\*\*)', content)
            for block in blocks:
                m = re.match(r'\*\*(Y\d+)\*\*\s*\(([^)]+)\)\s*(.+?)(?:\s*\([\d-]+\))?\s*\[.*?\]\n\s+(.+?)\n', block)
                if m:
                    views = m.group(2)
                    channel = m.group(3).strip()
                    title_text = m.group(4).strip()
                    url_m = re.search(r'(https?://(?:www\.)?youtube\.com/watch\S+)', block)
                    url = url_m.group(1) if url_m else ""
                    if url and not title_text.startswith('http'):
                        youtube_sources.append({"title": title_text, "url": url, "meta": f"{views} · {channel}"})
        else:
            # Parse Reddit blocks
            rblocks = re.split(r'(?=\*\*R\d+\*\*)', content)
            for rblock in rblocks:
                rm = re.match(r'\*\*(R\d+)\*\*\s*\(score:(\d+)\).*?\n\s+(.+?)(?:\n|$)', rblock)
                if rm:
                    score = rm.group(2)
                    title_text = rm.group(3).strip()
                    url_m = re.search(r'(https?://(?:www\.)?reddit\.com/\S+)', rblock)
                    url = url_m.group(1) if url_m else ""
                    if url and not title_text.startswith('http'):
                        reddit_sources.append({"title": title_text, "url": url, "meta": f"score:{score}"})

    return youtube_sources, reddit_sources

# ── Build blocks from NEW flat format ────────────────────────────────────────

def build_blocks_new(data, date_str):
    blocks = []

    # Count sources from reports
    yt_sources, reddit_sources = parse_sources_from_reports(date_str)
    report_files = glob.glob(os.path.join(REPORT_DIR, f"{date_str}_*.txt"))
    source_count = len(yt_sources) + len(reddit_sources)

    # 1. Summary callout
    blocks.append(callout(
        f"📅 {date_str}  •  {len(report_files)} reports  •  {source_count} sources indexed",
        "📊", "blue_background"
    ))
    blocks.append(divider())

    # 2. 🏆 Top Pick
    top = data.get("top_pick_recommendation", {})
    if top:
        blocks.append(heading_1("🏆 Top Pick"))
        blocks.append(callout(t(top.get("recommended_angle", "")), "🎯", "green_background"))
        blocks.append(rich_paragraph([
            {"text": "Why this one: ", "bold": True},
            {"text": t(top.get("why_this_one", ""))}
        ]))
        # Format execution strategy with double line breaks between steps
        exec_raw = t(top.get("execution_strategy", ""))
        exec_formatted = exec_raw.replace("Week ", "\n\nWeek ").replace("Step ", "\n\nStep ").strip()
        blocks.append(callout(
            f"Execution Strategy\n\n{exec_formatted}",
            "🔧", "blue_background"
        ))
        blocks.append(rich_paragraph([
            {"text": "Timeline: ", "bold": True},
            {"text": t(top.get("estimated_timeline", ""))},
            {"text": "  •  Revenue: ", "bold": True},
            {"text": t(top.get("revenue_potential", ""))}
        ]))
        blocks.append(rich_paragraph([
            {"text": "Risk Mitigation: ", "bold": True, "italic": True},
            {"text": t(top.get("risk_mitigation", ""))}
        ]))
        if top.get("why_now_not_later"):
            blocks.append(callout(
                f"⚡ {t(top['why_now_not_later'])}",
                "🔥", "orange_background"
            ))
        blocks.append(divider())

    # 3. 💡 Content Ideas
    ideas = data.get("specific_content_ideas", [])
    if ideas:
        blocks.append(heading_1("💡 Content Ideas This Week"))
        for i, idea in enumerate(ideas, 1):
            blocks.append(rich_numbered([
                {"text": f"{t(idea.get('title', ''))}", "bold": True},
                {"text": f"  [{t(idea.get('format', ''))}]", "italic": True, "color": "gray"}
            ]))
            if idea.get("hook"):
                blocks.append(quote_block(f"Hook: {t(idea['hook'])}"))
            if idea.get("why_it_works") or idea.get("why_this_works"):
                blocks.append(rich_paragraph([
                    {"text": "Why it works: ", "bold": True},
                    {"text": t(idea.get("why_it_works") or idea.get("why_this_works", ""))}
                ]))
            rev = idea.get("revenue_potential") or idea.get("estimated_reach", "")
            if rev:
                blocks.append(rich_paragraph([
                    {"text": "💰 ", "bold": True},
                    {"text": t(rev), "italic": True}
                ]))
        blocks.append(divider())

    # 4. 🧲 Lead Magnet Opportunities
    magnets = data.get("lead_magnet_opportunities", [])
    if magnets:
        blocks.append(heading_1("🧲 Lead Magnet Opportunities"))
        for mag in magnets:
            blocks.append(callout(t(mag.get("concept", "")), "💎", "purple_background"))
            blocks.append(rich_paragraph([
                {"text": "Why compelling: ", "bold": True},
                {"text": t(mag.get("why_compelling", ""))}
            ]))
            if mag.get("what_it_includes"):
                blocks.append(rich_paragraph([
                    {"text": "Includes: ", "bold": True},
                    {"text": t(mag["what_it_includes"])}
                ]))
            if mag.get("delivery"):
                blocks.append(rich_paragraph([
                    {"text": "Delivery: ", "bold": True},
                    {"text": t(mag["delivery"])}
                ]))
            if mag.get("conversion_path"):
                blocks.append(rich_paragraph([
                    {"text": "Conversion path: ", "bold": True, "italic": True},
                    {"text": t(mag["conversion_path"])}
                ]))
            if mag.get("market_gap"):
                blocks.append(rich_paragraph([
                    {"text": "Market gap: ", "bold": True, "color": "orange"},
                    {"text": t(mag["market_gap"])}
                ]))
            blocks.append(paragraph(""))
        blocks.append(divider())

    # 5. 🎯 Ranked Content Angles
    angles = data.get("ranked_content_angles", [])
    if angles:
        blocks.append(heading_1("🎯 Ranked Content Angles"))
        for angle in angles[:5]:
            rank = angle.get("rank", "")
            score = angle.get("momentum_score", "")
            blocks.append(rich_paragraph([
                {"text": f"#{rank}  ", "bold": True, "color": "orange"},
                {"text": t(angle.get("angle", "")), "bold": True},
                {"text": f"  [Momentum: {score}/100]", "italic": True, "color": "gray"}
            ]))
            if angle.get("why_now"):
                blocks.append(rich_paragraph([
                    {"text": "Why now: ", "bold": True},
                    {"text": t(angle["why_now"])}
                ]))
            if angle.get("audience_heat"):
                blocks.append(rich_paragraph([
                    {"text": "🔥 Audience heat: ", "bold": True},
                    {"text": t(angle["audience_heat"])}
                ]))
            if angle.get("opportunity"):
                blocks.append(rich_paragraph([
                    {"text": "→ Opportunity: ", "bold": True, "italic": True},
                    {"text": t(angle["opportunity"])}
                ]))
            blocks.append(paragraph(""))
        blocks.append(divider())

    # 6. 📋 Content Suggestions by Format
    suggestions = data.get("content_suggestions_by_format", {})
    if suggestions:
        blocks.append(heading_1("📋 Content Suggestions by Format"))
        format_map = [
            ("twitter_threads", "🐦 Twitter Threads"),
            ("youtube_videos", "🎬 YouTube Videos"),
            ("linkedin_posts", "💼 LinkedIn Posts"),
            ("blog_articles", "📝 Blog Articles"),
            ("short_form_video", "📱 Short-Form Video"),
        ]
        for key, label in format_map:
            items = suggestions.get(key, [])
            if items:
                blocks.append(heading_3(label))
                for item in items:
                    blocks.append(bulleted(t(item)))
        blocks.append(divider())

    # 7. 🗣️ Audience Language & Swipe Copy
    swipe = data.get("audience_language_and_swipe", {})
    if swipe:
        blocks.append(heading_1("🗣️ Audience Language & Swipe Copy"))

        phrases = swipe.get("power_phrases", [])
        if phrases:
            blocks.append(heading_3("Power Phrases"))
            for p in phrases:
                if isinstance(p, dict):
                    blocks.append(quote_block(f'"{t(p.get("phrase", ""))}" — {t(p.get("context", ""))}'))
                else:
                    blocks.append(quote_block(f'"{t(p)}"'))

        # emotional_triggers (non-standard but present in data)
        triggers = swipe.get("emotional_triggers", [])
        if triggers:
            blocks.append(heading_3("Emotional Triggers"))
            for tr in triggers:
                blocks.append(quote_block(t(tr)))

        themes = swipe.get("recurring_themes", [])
        if themes:
            blocks.append(heading_3("Recurring Themes"))
            for th in themes:
                blocks.append(bulleted(t(th)))

        hooks = swipe.get("hook_templates", []) or swipe.get("hooks_that_work", [])
        if hooks:
            blocks.append(heading_3("Hook Templates"))
            for h in hooks:
                blocks.append(bulleted(t(h)))

        # Sentiment analysis if present
        sentiment = swipe.get("comment_sentiment_analysis", {})
        if sentiment:
            blocks.append(heading_3("Comment Sentiment"))
            for k, v in sentiment.items():
                blocks.append(rich_paragraph([
                    {"text": f"{k.title()}: ", "bold": True},
                    {"text": t(v)}
                ]))

        blocks.append(divider())

    # 8. 🔥 Pain Points
    pain = data.get("pain_points_identified", {})
    if pain:
        blocks.append(heading_1("🔥 Pain Points & Objections"))

        primary = pain.get("primary", [])
        if primary:
            blocks.append(heading_3("Primary Pain Points"))
            for p in primary:
                intensity = p.get("intensity", "")
                blocks.append(callout(
                    f"{t(p.get('pain', ''))}\n\n{t(p.get('depth', ''))}\n\nIntensity: {t(intensity)}",
                    "🔥", "red_background"
                ))
                if p.get("quote"):
                    blocks.append(quote_block(f'"{t(p["quote"])}"'))

        secondary = pain.get("secondary", [])
        if secondary:
            blocks.append(heading_3("Secondary Pain Points"))
            for p in secondary:
                blocks.append(callout(
                    f"{t(p.get('pain', ''))}\n\n{t(p.get('depth', ''))}",
                    "⚠️", "yellow_background"
                ))
                if p.get("quote"):
                    blocks.append(quote_block(f'"{t(p["quote"])}"'))

        blocks.append(divider())

    # 9. 📌 Strategic Notes
    notes = data.get("strategic_notes", {})
    if notes:
        blocks.append(heading_1("📌 Strategic Notes"))
        if isinstance(notes, dict):
            for k, v in notes.items():
                label = k.replace("_", " ").title()
                blocks.append(rich_paragraph([
                    {"text": f"{label}: ", "bold": True},
                    {"text": t(v)}
                ]))
        elif isinstance(notes, list):
            for note in notes:
                blocks.append(bulleted(t(note)))
        blocks.append(divider())

    # 10. 📚 Source Index
    if yt_sources or reddit_sources:
        blocks.append(heading_1("📚 Source Index"))

        if yt_sources:
            blocks.append(heading_3("🎬 YouTube"))
            for src in yt_sources:
                blocks.append(linked_bulleted(src["title"], src["url"], src["meta"]))

        if reddit_sources:
            blocks.append(heading_3("💬 Reddit"))
            for src in reddit_sources:
                blocks.append(linked_bulleted(src["title"], src["url"], src["meta"]))

        blocks.append(divider())

    # 11. Footer
    blocks.append(callout("Analysis by trendanalyst agent (Sonnet 4.5)", "🤖", "gray_background"))

    return blocks

# ── Build blocks from LEGACY sections format ────────────────────────────────

def build_blocks_legacy(data):
    blocks = []
    blocks.append(divider())
    blocks.append(heading_1("🧠 Strategic Analysis"))
    blocks.append(paragraph(""))

    if data.get("top_pick"):
        blocks.append(callout(f"🏆 TOP PICK: {data['top_pick']}", "🎯", "green_background"))
        blocks.append(paragraph(""))

    for section in data.get("sections", []):
        emoji = section.get("emoji", "📌")
        heading = section.get("heading", "Untitled")
        blocks.append(heading_1(f"{emoji} {heading}"))

        for item in section.get("items", []):
            item_type = item.get("type", "insight")
            if item_type == "angle":
                blocks.append(rich_paragraph([
                    {"text": f"⭐ {t(item.get('title', ''))}", "bold": True},
                    {"text": f"  [{t(item.get('relevance', ''))}]", "color": "orange"}
                ]))
                if item.get("reasoning"):
                    blocks.append(paragraph(f"   {t(item['reasoning'])}"))
                if item.get("format"):
                    blocks.append(rich_paragraph([
                        {"text": "   → Best format: ", "italic": True},
                        {"text": t(item["format"]), "bold": True}
                    ]))
            elif item_type == "swipe":
                blocks.append(quote_block(f"🗣️ {t(item.get('text', ''))}"))
            elif item_type == "pain":
                blocks.append(callout(t(item.get("text", "")), "🔥", "red_background"))
            elif item_type == "recommendation":
                blocks.append(callout(t(item.get("text", "")), "✅", "blue_background"))
            else:
                blocks.append(bulleted(t(item.get("text", ""))))
        blocks.append(paragraph(""))

    blocks.append(divider())
    blocks.append(callout("Analysis by trendanalyst agent (Sonnet 4.5)", "🤖", "gray_background"))
    return blocks

# ── Build page properties ────────────────────────────────────────────────────

def build_properties(data, date_str, is_legacy=False):
    props = {
        "Name": {"title": [{"text": {"content": f"Weekly Trends — {date_str}"}}]},
        "Date": {"date": {"start": date_str}},
    }

    if is_legacy:
        summary = data.get("content_angles_summary", "")
        if summary:
            props["Content Angles"] = {"rich_text": [{"text": {"content": t(summary)}}]}
        return props

    # New format: build summaries from data
    # Key Findings
    top = data.get("top_pick_recommendation", {})
    findings = t(top.get("recommended_angle", ""))
    if findings:
        props["Key Findings"] = {"rich_text": [{"text": {"content": findings}}]}

    # Content Angles
    angles = data.get("ranked_content_angles", [])
    angle_summary = "; ".join([t(a.get("angle", "")) for a in angles[:3]])
    if angle_summary:
        props["Content Angles"] = {"rich_text": [{"text": {"content": t(angle_summary)}}]}

    # Queries from reports
    report_files = glob.glob(os.path.join(REPORT_DIR, f"{date_str}_*.txt"))
    queries = []
    for fp in report_files:
        with open(fp) as f:
            content = f.read()
        qm = re.search(r'researching:\s*(.+)', content)
        if qm:
            q = qm.group(1).strip()
            if "_youtube_" in os.path.basename(fp):
                q = f"[YT] {q}"
            queries.append(q)
    if queries:
        props["Queries"] = {"rich_text": [{"text": {"content": t(" | ".join(queries))}}]}

    # Sources count
    yt_sources, reddit_sources = parse_sources_from_reports(date_str)
    props["Sources"] = {"number": len(yt_sources) + len(reddit_sources)}

    # Status
    limited = all("LIMITED RECENT DATA" in open(fp).read() for fp in report_files) if report_files else False
    props["Status"] = {"select": {"name": "Limited Data" if limited else "Complete"}}

    return props

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: echo '{...}' | python3 push_analysis.py YYYY-MM-DD [PAGE_ID]", file=sys.stderr)
        sys.exit(1)

    date_str = sys.argv[1]
    token = get_token()

    page_id_arg = sys.argv[2] if len(sys.argv) >= 3 else None
    data = json.load(sys.stdin)

    # Auto-detect format
    is_legacy = "sections" in data
    print(f"📋 Format: {'legacy (sections)' if is_legacy else 'new (flat)'}")

    # Build blocks
    if is_legacy:
        blocks = build_blocks_legacy(data)
    else:
        blocks = build_blocks_new(data, date_str)

    print(f"📦 Built {len(blocks)} blocks")

    # Build properties
    properties = build_properties(data, date_str, is_legacy)

    # Find existing page
    existing_page_id = page_id_arg or find_page_by_date(token, date_str)

    # Archive old page and create fresh one
    if existing_page_id:
        archive_page(token, existing_page_id)

    new_page_id = create_fresh_page(token, date_str, properties)

    # Append all blocks
    append_blocks(token, new_page_id, blocks)

    print(f"🎉 Done! New page: {new_page_id}")

if __name__ == "__main__":
    main()
