"""
reply_tweet.py — Post a reply to a tweet using Playwright browser automation.

Usage: python3 reply_tweet.py "reply text" "tweet_id"

IMPORTANT: This script uses the existing browser session via CDP (port 18800).
The browser MUST be running and logged into X as Duncan.
Do NOT fall back to Tweepy API — that produces standalone mention posts, not threaded replies.
If the browser is unavailable, this script exits with an error. Skip and log instead.
"""

import sys
import time
import re

CDP_URL = "http://127.0.0.1:18800"


def post_reply(reply_text: str, tweet_id: str, dry_run: bool = False) -> str | None:
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        print("Error: playwright is not installed. Run: pip install playwright", file=sys.stderr)
        sys.exit(1)

    with sync_playwright() as p:
        # Connect to existing browser session via CDP
        try:
            browser = p.chromium.connect_over_cdp(CDP_URL)
        except Exception as e:
            print(f"Error: Could not connect to browser via CDP at {CDP_URL}.", file=sys.stderr)
            print(f"  Is the browser running? Details: {e}", file=sys.stderr)
            print("BROWSER_UNAVAILABLE", file=sys.stderr)
            sys.exit(2)

        context = browser.contexts[0] if browser.contexts else None
        if context is None:
            print("Error: No browser contexts found. Open a browser window first.", file=sys.stderr)
            sys.exit(2)

        page = context.new_page()
        reply_tweet_id = None

        try:
            tweet_url = f"https://x.com/i/status/{tweet_id}"
            print(f"Navigating to: {tweet_url}")
            page.goto(tweet_url, wait_until="domcontentloaded")

            # Wait for network to settle — X is a heavy SPA, needs time to render
            try:
                page.wait_for_load_state("networkidle", timeout=20000)
            except PWTimeout:
                pass  # Not fatal — just move on and check for the tweet element

            time.sleep(2)

            # Verify the tweet loaded by checking for tweet articles
            try:
                page.locator('[data-testid="tweet"]').first.wait_for(timeout=20000)
            except PWTimeout:
                print("Error: Tweet not found on page — tweet may be deleted or URL is wrong.", file=sys.stderr)
                page.close()
                sys.exit(1)

            # Find the reply button on the FIRST tweet (the one we navigated to)
            first_tweet = page.locator('[data-testid="tweet"]').first
            reply_button = first_tweet.locator('[data-testid="reply"]')

            try:
                reply_button.wait_for(timeout=8000)
            except PWTimeout:
                print("Error: Reply button not found on the tweet.", file=sys.stderr)
                page.close()
                sys.exit(1)

            if dry_run:
                # Verify button is visible and enabled without clicking
                is_visible = reply_button.is_visible()
                is_enabled = reply_button.is_enabled()
                print(f"DRY RUN: reply button visible={is_visible}, enabled={is_enabled}")
                if is_visible and is_enabled:
                    print("DRY RUN OK")
                else:
                    print("DRY RUN FAIL: Reply button not interactable")
                page.close()
                return None

            # --- LIVE POST ---

            # 2-second wait before clicking Reply (ensure page is fully loaded)
            time.sleep(2)
            reply_button.click()
            time.sleep(1.5)

            # Type reply text into the composer
            composer = page.locator('[data-testid="tweetTextarea_0"]')
            try:
                composer.wait_for(timeout=8000)
            except PWTimeout:
                print("Error: Reply composer did not open.", file=sys.stderr)
                page.close()
                sys.exit(1)

            composer.fill(reply_text)
            time.sleep(0.5)

            # Listen for the new tweet URL to capture the reply tweet ID
            # We intercept the API response for tweet creation
            reply_tweet_id_captured = []

            def handle_response(response):
                if "CreateTweet" in response.url and response.status == 200:
                    try:
                        body = response.json()
                        # Navigate the nested response to get the tweet ID
                        tweet_data = (
                            body.get("data", {})
                                .get("create_tweet", {})
                                .get("tweet_results", {})
                                .get("result", {})
                        )
                        tid = tweet_data.get("rest_id") or tweet_data.get("legacy", {}).get("id_str")
                        if tid:
                            reply_tweet_id_captured.append(tid)
                    except Exception:
                        pass

            page.on("response", handle_response)

            # Click the Post/Reply button
            post_button = page.locator('[data-testid="tweetButton"]')
            try:
                post_button.wait_for(timeout=5000)
            except PWTimeout:
                print("Error: Post button not found in reply composer.", file=sys.stderr)
                page.close()
                sys.exit(1)

            post_button.click()

            # Wait for the tweet to be posted
            time.sleep(3)

            # Try to get the reply ID from the captured API response
            if reply_tweet_id_captured:
                reply_tweet_id = reply_tweet_id_captured[0]
                print(f"Success: {reply_tweet_id}")
            else:
                # Fallback: try to detect URL change or success indicator
                print("Success: reply posted (ID capture failed — check X manually)")

        except Exception as e:
            print(f"Error during reply posting: {e}", file=sys.stderr)
            page.close()
            sys.exit(1)

        page.close()
        return reply_tweet_id


if __name__ == "__main__":
    dry_run_mode = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if len(args) < 2:
        print("Usage: python3 reply_tweet.py <reply_text> <tweet_id> [--dry-run]")
        print("  --dry-run  Verify the page loads and reply button is clickable without posting")
        sys.exit(1)

    reply_text_arg = args[0]
    tweet_id_arg = args[1]

    post_reply(reply_text_arg, tweet_id_arg, dry_run=dry_run_mode)
