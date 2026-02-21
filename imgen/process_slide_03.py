#!/usr/bin/env python3
"""Process Slide 3 - n8n workflow screenshot."""

import sys
import base64
import requests
sys.path.insert(0, "/data/.openclaw/workspace/carousel-system")
from text_styler import add_text_overlay
from format_validator import validate_image

# Paths
RAW_PATH = "/data/.openclaw/workspace/agents/imgen/carousel-video-prospector/slide-03-raw.png"
STYLED_PATH = "/data/.openclaw/workspace/agents/imgen/carousel-video-prospector/slide-03-final.png"
IMGUR_CLIENT_ID = "546c25a59c58ad7"

# Text configuration for Slide 3
text_config = [
    {"text": "Personalized Video", "size": 52, "weight": "bold"},
    {"text": "Prospector.", "size": 52, "weight": "bold"},
    {"text": "", "size": 15},
    {"text": "Personal touch.", "size": 38, "weight": "regular"},
    {"text": "Mass scale.", "size": 38, "weight": "regular"}
]

print("Processing Slide 3: n8n Workflow Screenshot")
print(f"Raw: {RAW_PATH}")
print(f"Styled: {STYLED_PATH}")

# Apply text overlay
styled = add_text_overlay(
    RAW_PATH,
    text_config,
    STYLED_PATH,
    aspect_ratio="4:5",
    y_offset=100
)

if not styled:
    print("❌ Text styling failed")
    sys.exit(1)

# Validate
print("🔍 Validating format...")
validation = validate_image(styled)
if not validation["valid"]:
    print("⚠️  Validation issues:")
    for check, result in validation.get("checks", {}).items():
        if not result.get("valid"):
            print(f"   - {check}: {result}")

# Upload to Imgur
print("☁️  Uploading to Imgur...")
with open(styled, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "https://api.imgur.com/3/image",
    headers={"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"},
    data={"image": img_b64, "type": "base64"},
    timeout=30
)

if response.status_code == 200:
    imgur_url = response.json()["data"]["link"]
    print(f"✅ Uploaded: {imgur_url}")
    print(f"\n🎉 SLIDE 3 COMPLETE: {imgur_url}")
else:
    print(f"❌ Imgur upload failed: {response.text}")
    sys.exit(1)
