#!/usr/bin/env python3
"""
Skool Community Rotation State Manager
Tracks which communities were used today, resets at midnight, handles weighted rotation.
"""

import json
from pathlib import Path
from datetime import datetime, timezone

STATE_FILE = Path(__file__).parent / ".rotation_state.json"

# Community tiers (Build Room excluded)
TIER_1 = ["ai-automation-society", "synthesizer", "ai-automations-by-jack"]
TIER_2 = ["makerschool", "bbc", "aipreneurs", "goosify", "magneticmemberships", "robonuggets-free"]
TIER_3 = ["ai-automation-mastery-group", "chase-ai-community", "skoolers", "youtubeblueprint"]

ALL_COMMUNITIES = TIER_1 + TIER_2 + TIER_3

def load_state():
    """Load rotation state from disk."""
    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text())
        # Check if state is from today
        state_date = data.get("date", "")
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if state_date == today:
            return data
    
    # New day or missing file
    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "posts_used": [],
        "comments_used": [],
        "tier_usage": {
            "tier1": 0,
            "tier2": 0,
            "tier3": 0
        }
    }

def save_state(state):
    """Save rotation state to disk."""
    STATE_FILE.write_text(json.dumps(state, indent=2))

def pick_communities(count, action_type="posts", exclude_used=True):
    """
    Pick N communities for posts or comments.
    
    Args:
        count: Number of communities to pick
        action_type: "posts" or "comments"
        exclude_used: Skip communities already used today for this action
    
    Returns:
        List of community slugs
    """
    state = load_state()
    used_key = f"{action_type}_used"
    used = state.get(used_key, [])
    
    # Available communities
    if exclude_used:
        available = [c for c in ALL_COMMUNITIES if c not in used]
    else:
        available = ALL_COMMUNITIES.copy()
    
    if not available:
        # All used today, reset for this action
        available = ALL_COMMUNITIES.copy()
        state[used_key] = []
    
    # Weight by tier (Tier 1 = 3x, Tier 2 = 2x, Tier 3 = 1x)
    weighted = []
    for comm in available:
        if comm in TIER_1:
            weighted.extend([comm] * 3)
        elif comm in TIER_2:
            weighted.extend([comm] * 2)
        else:
            weighted.extend([comm] * 1)
    
    # Pick N unique
    import random
    picked = []
    while len(picked) < count and weighted:
        choice = random.choice(weighted)
        if choice not in picked:
            picked.append(choice)
        # Remove all instances of this choice from weighted pool
        weighted = [c for c in weighted if c != choice]
    
    # Mark as used
    state[used_key].extend(picked)
    save_state(state)
    
    return picked

def mark_used(community, action_type="posts"):
    """Mark a community as used for posts or comments today."""
    state = load_state()
    used_key = f"{action_type}_used"
    if community not in state[used_key]:
        state[used_key].append(community)
        save_state(state)

def reset_if_new_day():
    """Reset state if it's a new day."""
    state = load_state()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if state.get("date") != today:
        state = {
            "date": today,
            "posts_used": [],
            "comments_used": [],
            "tier_usage": {"tier1": 0, "tier2": 0, "tier3": 0}
        }
        save_state(state)
        return True
    return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "reset":
            state = {
                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "posts_used": [],
                "comments_used": [],
                "tier_usage": {"tier1": 0, "tier2": 0, "tier3": 0}
            }
            save_state(state)
            print("State reset for today")
        
        elif action == "status":
            state = load_state()
            print(json.dumps(state, indent=2))
        
        elif action == "pick":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            action_type = sys.argv[3] if len(sys.argv) > 3 else "posts"
            picked = pick_communities(count, action_type)
            print(json.dumps(picked))
    else:
        print("Usage: rotation_state.py [reset|status|pick COUNT TYPE]")
