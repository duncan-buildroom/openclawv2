#!/usr/bin/env python3
"""Clean up Skool posts: replace em dashes with commas."""
import sys
import re

def clean(text):
    # Replace em dash (—) with comma
    # Handle " — " (spaced) and "—" (unspaced)
    text = re.sub(r'\s*—\s*', ', ', text)
    # Clean up double commas or comma-period
    text = text.replace(',,', ',')
    text = text.replace(', ,', ',')
    return text

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            content = f.read()
        cleaned = clean(content)
        with open(sys.argv[1], 'w') as f:
            f.write(cleaned)
        print(f"Cleaned: {sys.argv[1]}")
    else:
        # Read from stdin
        content = sys.stdin.read()
        print(clean(content))
