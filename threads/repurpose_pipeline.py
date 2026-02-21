#!/usr/bin/env python3
"""
Content Repurpose Pipeline — Auto-converts content from other platforms to X format.

Skool post → Tweet (compress to 280 chars)
LinkedIn post → Mini-thread or single tweet
Carousel topic → Hot take tweet
YouTube video → 3-5 tweet highlights

Called by orchestrator whenever new content is created on any platform.
"""

import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / "cache"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def skool_to_tweet(post_text, title=""):
    """Convert a 50-100 word Skool post into a <280 char tweet."""
    # Skool posts are already concise, just need trimming
    # Remove any narrative setup, keep the insight + result
    return {
        "source": "skool",
        "source_title": title,
        "original_length": len(post_text),
        "tweet_draft": post_text[:280] if len(post_text) <= 280 else None,
        "needs_rewrite": len(post_text) > 280,
        "original": post_text
    }


def linkedin_to_tweets(post_text, title=""):
    """Convert a ~150 word LinkedIn post into 1-3 tweets or a mini-thread."""
    sentences = [s.strip() for s in post_text.replace('\n\n', '. ').split('. ') if s.strip()]
    
    tweets = []
    current = ""
    
    for sentence in sentences:
        test = f"{current}. {sentence}" if current else sentence
        if len(test) <= 280:
            current = test
        else:
            if current:
                tweets.append(current)
            current = sentence
    
    if current:
        tweets.append(current)
    
    return {
        "source": "linkedin",
        "source_title": title,
        "format": "thread" if len(tweets) > 1 else "single",
        "tweet_count": len(tweets),
        "tweets": tweets
    }


def carousel_to_tweet(topic, hook_text, key_insight):
    """Convert a carousel topic into a hot take tweet."""
    return {
        "source": "carousel",
        "topic": topic,
        "tweet_draft": f"{hook_text}\n\n{key_insight}" if len(f"{hook_text}\n\n{key_insight}") <= 280 else hook_text[:280],
        "needs_rewrite": len(f"{hook_text}\n\n{key_insight}") > 280
    }


def youtube_to_tweets(title, key_points):
    """Convert YouTube video highlights into 3-5 standalone tweets."""
    tweets = []
    for i, point in enumerate(key_points[:5], 1):
        tweet = {
            "tweet_number": i,
            "text": point[:280],
            "needs_rewrite": len(point) > 280
        }
        tweets.append(tweet)
    
    return {
        "source": "youtube",
        "video_title": title,
        "tweet_count": len(tweets),
        "tweets": tweets
    }


def batch_repurpose(content_items):
    """Process a batch of content items from various sources."""
    results = []
    
    for item in content_items:
        source = item.get("source", "")
        
        if source == "skool":
            result = skool_to_tweet(item["text"], item.get("title", ""))
        elif source == "linkedin":
            result = linkedin_to_tweets(item["text"], item.get("title", ""))
        elif source == "carousel":
            result = carousel_to_tweet(item["topic"], item["hook"], item.get("insight", ""))
        elif source == "youtube":
            result = youtube_to_tweets(item["title"], item["key_points"])
        else:
            continue
        
        results.append(result)
    
    # Save batch results
    output_file = OUTPUT_DIR / f"repurpose_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, "w") as f:
        json.dump({
            "processed_at": datetime.now().isoformat(),
            "total_items": len(results),
            "results": results
        }, f, indent=2)
    
    return results


if __name__ == "__main__":
    # Example usage
    test_items = [
        {
            "source": "skool",
            "title": "Cost Optimization",
            "text": "I was mass spending $16/day on AI agents. Switched my default model from Opus to Gemini Flash for routine tasks. Kept Sonnet for writing. Same output quality where it matters. Cost dropped to $5/day. That's a 90% reduction by just being intentional about which model does what."
        }
    ]
    
    results = batch_repurpose(test_items)
    for r in results:
        print(json.dumps(r, indent=2))
