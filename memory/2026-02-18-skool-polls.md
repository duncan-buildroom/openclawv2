# Skool Poll Automation — Feb 18, 2026

## Discovery
- Skool polls work via browser automation
- First live poll posted: "What are you building with AI right now?" in Build Room (Hangout category)
- URL: https://www.skool.com/buildroom/what-are-you-building-with-ai-right-now

## Critical Technical Detail: Category Selection
- Skool's category dropdown does NOT work with normal DOM clicks
- The React state doesn't update from simulated clicks
- **Solution:** Access React fiber internals:
  1. Find "Select a category" button
  2. Get `__reactFiber$` key
  3. Walk fiber tree to find `memoizedProps.options`
  4. Call `options[INDEX].onClick()`
- Category index map (Build Room): 0=Announcements, 1=Daily Actions, 2=$1M Roadmap, 3=YouTube Videos, 4=Wins, 5=Hangout, 6=Check-Ins, 7=Help!

## Build Room Category IDs (from URL params)
- Announcements: 0dc2fa4f55944dcd9efbc207099e842f
- Daily Actions: f00f3745d23f43e2b503f1f4afa5846c
- $1M Roadmap: c172a360b7934d549d4d41ac663d4546
- YouTube Videos: 92c67c8a670047479d7e53c6f183951e
- Wins: 950a071599854c78829b2bea775fb983
- Hangout: 49170f0cbacb4883a5ae072fbbbcf3f1
- Check-Ins: 9e6ae46a07d349809094e6704ea5ea11
- Help!: 85eb27a944794ab3ac1cb67bab73229a

## Files Updated
- `agents/skoolposts/SOUL.md` — added poll automation technical section
- `agents/skoolposts/skool_post.py` — reusable JS snippets for posting
