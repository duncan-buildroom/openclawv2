#!/usr/bin/env python3
"""
Skool Post Automation Helper
Provides the JS snippets needed to post to Skool via browser automation.

Category index mapping for The Build Room:
  0 = Announcements
  1 = Daily Actions
  2 = $1M Roadmap
  3 = YouTube Videos
  4 = Wins
  5 = Hangout
  6 = Check-Ins
  7 = Help!

Usage: This file documents the JS evaluate calls needed.
The actual posting is done via browser tool evaluate calls.
"""

# Step 1: Open composer
OPEN_COMPOSER = """
() => {
  const el = document.querySelector('[data-placeholder="Write something..."]');
  if (el) { el.click(); return 'opened'; }
  return 'not found';
}
"""

# Step 2: Enable poll (click 5th toolbar button after composer opens)
ENABLE_POLL = """
() => {
  const btns = document.querySelectorAll('button');
  const toolbar = [];
  for (const b of btns) {
    const rect = b.getBoundingClientRect();
    if (rect.top > 200 && rect.top < 400 && rect.width < 60 && rect.height < 60) {
      toolbar.push(b);
    }
  }
  // Poll is typically the 5th toolbar button
  if (toolbar.length >= 5) { toolbar[4].click(); return 'poll enabled'; }
  return 'toolbar buttons: ' + toolbar.length;
}
"""

# Step 3: Set title
def set_title(title):
    return f"""
() => {{
  const title = document.querySelector('input[placeholder="Title"]');
  if (!title) return 'no title field';
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(title, {repr(title)});
  title.dispatchEvent(new Event('input', {{bubbles: true}}));
  title.dispatchEvent(new Event('change', {{bubbles: true}}));
  return 'title set';
}}
"""

# Step 4: Set poll options
def set_options(options):
    opts_json = str(options)
    return f"""
() => {{
  const inputs = document.querySelectorAll('input');
  const opts = [];
  for (const inp of inputs) {{
    if (inp.placeholder && inp.placeholder.startsWith('Option')) opts.push(inp);
  }}
  const values = {opts_json};
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  for (let i = 0; i < Math.min(opts.length, values.length); i++) {{
    setter.call(opts[i], values[i]);
    opts[i].dispatchEvent(new Event('input', {{bubbles: true}}));
  }}
  return 'set ' + Math.min(opts.length, values.length) + ' options';
}}
"""

# Step 5: Set body text
def set_body(text):
    return f"""
() => {{
  const p = document.querySelector('[contenteditable] p, [data-placeholder]');
  if (!p) return 'no body field';
  p.focus();
  p.textContent = {repr(text)};
  p.dispatchEvent(new Event('input', {{bubbles: true}}));
  return 'body set';
}}
"""

# Step 6: Select category via React fiber (CRITICAL)
def select_category(index):
    return f"""
() => {{
  const btn = [...document.querySelectorAll('button')].find(
    b => b.textContent.trim() === 'Select a category' && b.getBoundingClientRect().height > 0
  );
  if (!btn) return 'no category button';
  const key = Object.keys(btn).find(k => k.startsWith('__reactFiber$'));
  if (!key) return 'no react fiber';
  let fiber = btn[key];
  while (fiber) {{
    const p = fiber.memoizedProps;
    if (p && p.options && p.options[{index}]) {{
      p.options[{index}].onClick();
      return 'category selected: index {index}';
    }}
    fiber = fiber.return;
  }}
  return 'no options found';
}}
"""

# Step 7: Click Post
POST = """
() => {
  const btn = [...document.querySelectorAll('button')].find(
    b => b.textContent.trim() === 'Post' && !b.disabled
  );
  if (btn) { btn.click(); return 'posted'; }
  return 'post button not found or disabled';
}
"""

CATEGORY_MAP = {
    'announcements': 0,
    'daily_actions': 1,
    '$1m_roadmap': 2,
    'youtube_videos': 3,
    'wins': 4,
    'hangout': 5,
    'check_ins': 6,
    'help': 7,
}
