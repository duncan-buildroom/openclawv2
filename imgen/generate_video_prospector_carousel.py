#!/usr/bin/env python3
"""
Generate 10-slide Instagram carousel for Personalized Video Prospector
Theme: Rooftop in downtown Manhattan - urban luxury, skyline, modern furniture
Duncan Reference: https://i.imgur.com/vc7pPOC.jpeg
"""

import os
import sys
import json
import base64
import requests
from pathlib import Path
sys.path.insert(0, "/data/.openclaw/workspace/carousel-system")
from nano_banana import generate_image
from text_styler import add_text_overlay
from format_validator import validate_image

# Configuration
WORKSPACE = Path("/data/.openclaw/workspace/agents/imgen")
OUTPUT_DIR = WORKSPACE / "carousel-video-prospector"
OUTPUT_DIR.mkdir(exist_ok=True)

DUNCAN_REF = "/data/.openclaw/workspace/reference-photos/file_2---a14ce08d-ac3a-4916-b266-c920d21f40a0.jpg"
IMGUR_CLIENT_ID = "546c25a59c58ad7"
ASPECT_RATIO = "4:5"

# Slide configurations
SLIDES = [
    {
        "slide_number": 1,
        "text": "Cold outreach is dead.\n\nUnless you do THIS.",
        "prompt": "A confident young man with an orange hoodie sitting on a modern rooftop terrace in downtown Manhattan. He's looking directly at camera with a slightly challenging expression. Urban luxury setting with sleek furniture, Manhattan skyline in background, bright afternoon lighting, clear sky. Professional photography, sharp focus on subject, shallow depth of field.",
        "shot_type": "character",
        "text_config": [
            {"text": "Cold outreach is dead.", "size": 60, "weight": "bold"},
            {"text": "", "size": 20},
            {"text": "Unless you do THIS.", "size": 54, "weight": "bold"}
        ],
        "y_offset": 180
    },
    {
        "slide_number": 2,
        "text": "Standard cold emails get ignored.\n\nLow response rates.\nHigh friction.\nZero trust.",
        "prompt": "Establishing wide shot: A luxury rooftop terrace in downtown Manhattan. Sleek modern outdoor furniture, clean minimalist design, Manhattan skyline visible in distance under bright afternoon sky. No people. Urban luxury aesthetic, professional architectural photography, golden hour lighting.",
        "shot_type": "establishing",
        "text_config": [
            {"text": "Standard cold emails", "size": 50, "weight": "bold"},
            {"text": "get ignored.", "size": 50, "weight": "bold"},
            {"text": "", "size": 15},
            {"text": "Low response rates.", "size": 40, "weight": "regular"},
            {"text": "High friction.", "size": 40, "weight": "regular"},
            {"text": "Zero trust.", "size": 40, "weight": "regular"}
        ],
        "y_offset": 850
    },
    {
        "slide_number": 3,
        "text": "Personalized Video Prospector.\n\nPersonal touch.\nMass scale.",
        "prompt": None,  # Screenshot slide
        "shot_type": "screenshot",
        "text_config": [
            {"text": "Personalized Video", "size": 52, "weight": "bold"},
            {"text": "Prospector.", "size": 52, "weight": "bold"},
            {"text": "", "size": 15},
            {"text": "Personal touch.", "size": 38, "weight": "regular"},
            {"text": "Mass scale.", "size": 38, "weight": "regular"}
        ],
        "y_offset": 100
    },
    {
        "slide_number": 4,
        "text": "How it works:\n\n1. Scrape prospect data\n2. AI writes custom script\n3. AI generates personalized video\n4. Auto-sends via DM or Email",
        "prompt": "infographic",  # Special handling
        "shot_type": "infographic",
        "text_config": [
            {"text": "How it works:", "size": 54, "weight": "bold"},
            {"text": "", "size": 25},
            {"text": "1. Scrape prospect data", "size": 38, "weight": "regular"},
            {"text": "", "size": 10},
            {"text": "2. AI writes custom script", "size": 38, "weight": "regular"},
            {"text": "", "size": 10},
            {"text": "3. AI generates video", "size": 38, "weight": "regular"},
            {"text": "", "size": 10},
            {"text": "4. Auto-sends via DM", "size": 38, "weight": "regular"}
        ],
        "y_offset": 200
    },
    {
        "slide_number": 5,
        "text": "The results are staggering.\n\n3x higher response rates.\nInstant rapport.\nWarm-feeling outreach.",
        "prompt": "A young man in orange hoodie leaning against a rooftop railing, downtown Manhattan skyline behind him. He's looking at his smartphone, appearing relaxed and successful. Urban luxury setting, golden hour lighting, professional lifestyle photography, natural candid moment.",
        "shot_type": "character",
        "text_config": [
            {"text": "The results are", "size": 52, "weight": "bold"},
            {"text": "staggering.", "size": 52, "weight": "bold"},
            {"text": "", "size": 15},
            {"text": "3x higher response rates.", "size": 38, "weight": "regular"},
            {"text": "Instant rapport.", "size": 38, "weight": "regular"},
            {"text": "Warm-feeling outreach.", "size": 38, "weight": "regular"}
        ],
        "y_offset": 850
    },
    {
        "slide_number": 6,
        "text": "What took hours now takes seconds.\n\nProspect name.\nCompany name.\nSpecific pain points.\nAll woven in automatically.",
        "prompt": "A young man in orange hoodie walking across a rooftop terrace with a laptop under his arm. Natural casual movement, modern luxury outdoor furniture, Manhattan skyline, bright daylight, lifestyle photography, motion captured naturally.",
        "shot_type": "character",
        "text_config": [
            {"text": "What took hours", "size": 50, "weight": "bold"},
            {"text": "now takes seconds.", "size": 50, "weight": "bold"},
            {"text": "", "size": 15},
            {"text": "Prospect name.", "size": 36, "weight": "regular"},
            {"text": "Company name.", "size": 36, "weight": "regular"},
            {"text": "Specific pain points.", "size": 36, "weight": "regular"},
            {"text": "All woven in automatically.", "size": 36, "weight": "regular"}
        ],
        "y_offset": 150
    },
    {
        "slide_number": 7,
        "text": "Integrates with your CRM.\n\nAutomated follow-ups.\nSynced deal stages.\nZero manual data entry.",
        "prompt": "Close-up detail shot: A high-quality modern smartphone resting on a sleek outdoor table on a rooftop. Manhattan skyline blurred in background. Sunlight reflecting beautifully off the phone surface. Product photography aesthetic, shallow depth of field, bokeh, professional lighting.",
        "shot_type": "detail",
        "text_config": [
            {"text": "Integrates with", "size": 50, "weight": "bold"},
            {"text": "your CRM.", "size": 50, "weight": "bold"},
            {"text": "", "size": 15},
            {"text": "Automated follow-ups.", "size": 38, "weight": "regular"},
            {"text": "Synced deal stages.", "size": 38, "weight": "regular"},
            {"text": "Zero manual entry.", "size": 38, "weight": "regular"}
        ],
        "y_offset": 150
    },
    {
        "slide_number": 8,
        "text": "Turn cold prospects into hot leads.\n\nWhile you sleep.\nAt scale.",
        "prompt": "Establishing shot: Manhattan skyline from a rooftop at sunset. Warm golden light hitting the buildings, dramatic sky with orange and purple tones. No people. Cinematic cityscape photography, professional real estate photography aesthetic.",
        "shot_type": "establishing",
        "text_config": [
            {"text": "Turn cold prospects", "size": 50, "weight": "bold"},
            {"text": "into hot leads.", "size": 50, "weight": "bold"},
            {"text": "", "size": 20},
            {"text": "While you sleep.", "size": 44, "weight": "regular"},
            {"text": "At scale.", "size": 44, "weight": "regular"}
        ],
        "y_offset": 180
    },
    {
        "slide_number": 9,
        "text": "I built this to save you 20 hours a week.\n\nStop grinding.\nStart closing.",
        "prompt": "A young man in orange hoodie sitting on a modern lounge chair on a rooftop, looking out at the Manhattan city view. Casual lifestyle vibe, NOT at a desk. Relaxed posture, thoughtful expression, golden hour lighting, professional lifestyle photography, urban luxury setting.",
        "shot_type": "character",
        "text_config": [
            {"text": "I built this to save you", "size": 46, "weight": "bold"},
            {"text": "20 hours a week.", "size": 46, "weight": "bold"},
            {"text": "", "size": 20},
            {"text": "Stop grinding.", "size": 42, "weight": "regular"},
            {"text": "Start closing.", "size": 42, "weight": "regular"}
        ],
        "y_offset": 850
    },
    {
        "slide_number": 10,
        "text": "Get the blueprint for all 30 automations.",
        "prompt": "composite",  # Special handling
        "shot_type": "composite",
        "text_config": [
            {"text": "Get the blueprint for", "size": 48, "weight": "bold"},
            {"text": "all 30 automations.", "size": 48, "weight": "bold"},
            {"text": "", "size": 30},
            {"text": "Comment 'AI' to get access", "size": 36, "weight": "regular"}
        ],
        "y_offset": 900
    }
]


def upload_to_imgur(image_path: str) -> str:
    """Upload image to Imgur and return URL."""
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    response = requests.post(
        "https://api.imgur.com/3/image",
        headers={"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"},
        data={"image": img_b64, "type": "base64"},
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        raise Exception(f"Imgur upload failed: {response.text}")


def generate_screenshot_slide(slide_num: int, config: dict) -> str:
    """Generate screenshot slide from n8n."""
    print(f"\n📸 Slide {slide_num}: Screenshot (n8n workflow)")
    # This will be handled separately via browser tool
    return None


def generate_infographic_slide(slide_num: int, config: dict) -> str:
    """Generate infographic slide."""
    from PIL import Image, ImageDraw, ImageFont
    
    print(f"\n🎨 Slide {slide_num}: Infographic")
    
    # Create dark background
    img = Image.new("RGB", (1080, 1350), (20, 20, 25))
    draw = ImageDraw.Draw(img)
    
    # Icons and steps
    steps = [
        "1. Scrape prospect data",
        "2. AI writes custom script",
        "3. AI generates video",
        "4. Auto-sends via DM"
    ]
    
    icons = ["🌐", "🧠", "🎥", "✈️"]
    
    y = 400
    for icon, step in zip(icons, steps):
        # Draw icon circle
        draw.ellipse([180, y-30, 240, y+30], fill=(0, 255, 136))
        
        # Draw text
        try:
            font = ImageFont.truetype("/data/.fonts/Roboto-Bold.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        draw.text((280, y), step, fill="white", font=font)
        y += 160
    
    raw_path = OUTPUT_DIR / f"slide-{slide_num:02d}-raw.png"
    img.save(raw_path)
    return str(raw_path)


def generate_composite_slide(slide_num: int, config: dict) -> str:
    """Generate composite slide with phone mockup."""
    from PIL import Image, ImageDraw
    
    print(f"\n🎨 Slide {slide_num}: Composite (phone mockup)")
    
    # Generate background rooftop scene first
    bg_prompt = "Manhattan rooftop terrace at golden hour, no people, modern luxury furniture, cityscape in background, professional photography"
    raw_bg = OUTPUT_DIR / f"slide-{slide_num:02d}-bg-raw.png"
    
    if not generate_image(bg_prompt, ASPECT_RATIO, str(raw_bg), DUNCAN_REF):
        print(f"❌ Failed to generate background for slide {slide_num}")
        return None
    
    # Open background and create composite
    bg = Image.open(raw_bg).convert("RGBA")
    
    # Create phone mockup (simplified - black rectangle with rounded corners)
    phone_w, phone_h = 340, 680
    phone_x = (1080 - phone_w) // 2
    phone_y = 400
    
    draw = ImageDraw.Draw(bg)
    draw.rounded_rectangle(
        [phone_x, phone_y, phone_x + phone_w, phone_y + phone_h],
        radius=40,
        fill=(30, 30, 35, 255)
    )
    
    # Add text to "screen" area
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("/data/.fonts/Roboto-Bold.ttf", 32)
        screen_text = "leads.buildroom.ai\n30-automations"
        draw.text((phone_x + 50, phone_y + 200), screen_text, fill="white", font=font)
    except:
        pass
    
    raw_path = OUTPUT_DIR / f"slide-{slide_num:02d}-raw.png"
    bg.save(raw_path.with_suffix(".png"))
    return str(raw_path)


def generate_slide(slide_config: dict) -> dict:
    """Generate a single slide - raw image + styled version."""
    slide_num = slide_config["slide_number"]
    shot_type = slide_config["shot_type"]
    
    print(f"\n{'='*60}")
    print(f"SLIDE {slide_num}: {shot_type}")
    print(f"{'='*60}")
    
    raw_path = OUTPUT_DIR / f"slide-{slide_num:02d}-raw.png"
    styled_path = OUTPUT_DIR / f"slide-{slide_num:02d}-final.png"
    
    # Generate raw image based on shot type
    if shot_type == "screenshot":
        raw_image = generate_screenshot_slide(slide_num, slide_config)
        if not raw_image:
            print(f"⚠️  Screenshot slide will be handled separately")
            return {"slide": slide_num, "status": "pending_screenshot"}
    
    elif shot_type == "infographic":
        raw_image = generate_infographic_slide(slide_num, slide_config)
        if not raw_image:
            return {"slide": slide_num, "status": "failed", "error": "Infographic generation failed"}
    
    elif shot_type == "composite":
        raw_image = generate_composite_slide(slide_num, slide_config)
        if not raw_image:
            return {"slide": slide_num, "status": "failed", "error": "Composite generation failed"}
    
    else:
        # Character/establishing/detail shots - use Nano Banana
        prompt = slide_config["prompt"]
        print(f"🎨 Generating: {shot_type}")
        raw_image = generate_image(prompt, ASPECT_RATIO, str(raw_path), DUNCAN_REF)
        
        if not raw_image:
            return {"slide": slide_num, "status": "failed", "error": "Image generation failed"}
    
    # Apply text styling
    print(f"✍️  Applying text overlay...")
    styled = add_text_overlay(
        raw_image,
        slide_config["text_config"],
        str(styled_path),
        aspect_ratio=ASPECT_RATIO,
        y_offset=slide_config.get("y_offset")
    )
    
    if not styled:
        return {"slide": slide_num, "status": "failed", "error": "Text styling failed"}
    
    # Validate format
    print(f"🔍 Validating format...")
    validation = validate_image(styled)
    
    if not validation["valid"]:
        print(f"⚠️  Validation issues detected:")
        for check, result in validation.get("checks", {}).items():
            if not result.get("valid"):
                print(f"   - {check}: {result}")
    
    # Upload to Imgur
    print(f"☁️  Uploading to Imgur...")
    try:
        imgur_url = upload_to_imgur(styled)
        print(f"✅ Uploaded: {imgur_url}")
        
        return {
            "slide": slide_num,
            "status": "success",
            "raw_path": str(raw_path),
            "styled_path": str(styled_path),
            "imgur_url": imgur_url,
            "validation": validation
        }
    
    except Exception as e:
        return {
            "slide": slide_num,
            "status": "upload_failed",
            "styled_path": str(styled_path),
            "error": str(e)
        }


def main():
    """Generate all 10 slides."""
    print("🚀 PERSONALIZED VIDEO PROSPECTOR CAROUSEL")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Aspect ratio: {ASPECT_RATIO} (1080x1350)")
    
    results = []
    
    for slide_config in SLIDES:
        try:
            result = generate_slide(slide_config)
            results.append(result)
        except Exception as e:
            print(f"❌ Error on slide {slide_config['slide_number']}: {e}")
            results.append({
                "slide": slide_config['slide_number'],
                "status": "error",
                "error": str(e)
            })
    
    # Save results
    results_file = OUTPUT_DIR / "generation_results.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print("GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"\nResults saved to: {results_file}")
    
    # Summary
    successful = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("status") in ["failed", "error"]]
    pending = [r for r in results if r.get("status") == "pending_screenshot"]
    
    print(f"\n✅ Successful: {len(successful)}/10")
    print(f"❌ Failed: {len(failed)}/10")
    print(f"⏳ Pending: {len(pending)}/10")
    
    if successful:
        print("\n📋 IMGUR URLS:")
        for result in successful:
            print(f"Slide {result['slide']:2d}: {result['imgur_url']}")
    
    return results


if __name__ == "__main__":
    main()
