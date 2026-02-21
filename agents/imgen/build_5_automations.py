#!/usr/bin/env python3
"""Build all 8 slides for '5 AI Automations' carousel."""

import sys, json, os
sys.path.insert(0, "/data/.openclaw/workspace/carousel-system")
sys.path.insert(0, "/data/.openclaw/workspace")

from nano_banana import generate_image
from text_styler import add_text_overlay
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path
import base64, requests

OUT = Path("/data/.openclaw/workspace/agents/imgen/output/5-automations")
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw"
RAW.mkdir(exist_ok=True)
FINAL = OUT / "final"
FINAL.mkdir(exist_ok=True)

REF = "/data/.openclaw/workspace/reference-photos/DuncanReference.jpeg"
FONT_BOLD = "/data/.fonts/Roboto-Bold.ttf"
FONT_REG = "/data/.fonts/Roboto-Regular.ttf"

SEALCAM = """SEALCAM photograph. High contrast DSLR, dramatic natural lighting, shallow depth of field, cinematic composition. 
The subject is a 30-something man with short brown hair, beard, glasses, wearing an orange hoodie and dark jeans. """

# ── Slide prompts ──
PROMPTS = {
    1: SEALCAM + "He leans against a stone railing on a Barcelona terrace overlooking the city at golden hour. Relaxed posture, checking his phone. Mediterranean tiles, warm stone architecture in background. Direct confident gaze at camera. Full body shot.",
    2: "SEALCAM photograph. Extreme close-up detail shot: a small espresso cup on a Mediterranean tiled table next to an open MacBook Pro. The laptop screen shows a blurred complex node-based workflow. Warm golden morning light streams across the scene. Shallow depth of field, bokeh. Barcelona terrace setting.",
    5: SEALCAM + "He sits at a stone table on a Barcelona terrace, focused on his laptop. The city stretches out behind him with warm stone buildings. Mediterranean tiles on the table. Golden hour lighting. Medium shot, slightly from the side.",
    6: "SEALCAM photograph. Wide establishing shot of a beautiful Barcelona terrace at golden hour. Warm stone balustrade, Mediterranean tiles, potted plants. The city skyline stretches into the distance with warm orange and golden tones. A distant silhouette of a person relaxing. Cinematic, aspirational, freedom.",
    7: SEALCAM + "He stands on a Barcelona terrace at sunset, orange hoodie, looking out over the city skyline. Shot from behind/side, dramatic warm lighting. Confident posture, hands in pockets. The sky is ablaze with golden and orange tones.",
    8: SEALCAM + "He stands centered on a Barcelona terrace, facing camera with a warm smile. Orange hoodie. The background is slightly darkened with warm bokeh lights. Medium shot, approachable and inviting. Clean background for overlay elements.",
}

# ── Text configs per slide (condensed ~30%) ──
TEXTS = {
    1: [
        {"text": "I run a $25K/mo brand", "size": 66, "weight": "bold"},
        {"text": "with zero employees.", "size": 66, "weight": "bold"},
        {"text": "", "size": 30},
        {"text": "Here are the 5 AI automations", "size": 44, "weight": "regular"},
        {"text": "running it on autopilot.", "size": 44, "weight": "regular"},
    ],
    2: [
        {"text": "The bottleneck isn't talent.", "size": 58, "weight": "bold"},
        {"text": "It's manual labor.", "size": 58, "weight": "bold"},
        {"text": "", "size": 30},
        {"text": "These 5 n8n workflows do", "size": 42, "weight": "regular"},
        {"text": "80% of my heavy lifting.", "size": 42, "weight": "regular"},
    ],
    3: [
        {"text": "1: The Repurpose Engine", "size": 58, "weight": "bold"},
        {"text": "", "size": 20},
        {"text": "One TikTok → AI takes over.", "size": 42, "weight": "regular"},
        {"text": "Strips watermark, rewrites captions,", "size": 38, "weight": "regular"},
        {"text": "auto-posts to IG, LinkedIn, YT.", "size": 38, "weight": "regular"},
        {"text": "", "size": 20},
        {"text": "5x reach. 0 extra minutes.", "size": 46, "weight": "bold"},
    ],
    4: [
        {"text": "2: Trend Research Pipeline", "size": 58, "weight": "bold"},
        {"text": "", "size": 20},
        {"text": "Every Monday, AI scans Reddit", "size": 42, "weight": "regular"},
        {"text": "& YouTube for top pain points.", "size": 42, "weight": "regular"},
        {"text": "", "size": 16},
        {"text": "Delivers a Content Cheat Sheet", "size": 42, "weight": "regular"},
        {"text": "straight to my Slack.", "size": 42, "weight": "regular"},
    ],
    5: [
        {"text": "3 & 4: The Content Loop", "size": 58, "weight": "bold"},
        {"text": "", "size": 20},
        {"text": "Comment Scraper: AI extracts", "size": 40, "weight": "regular"},
        {"text": "best YT questions → to-do list.", "size": 40, "weight": "regular"},
        {"text": "", "size": 16},
        {"text": "Carousel Gen: Drop a topic →", "size": 40, "weight": "regular"},
        {"text": "AI writes slides + image prompts.", "size": 40, "weight": "regular"},
    ],
    6: [
        {"text": "5: Smart Lead Scoring", "size": 58, "weight": "bold"},
        {"text": "", "size": 20},
        {"text": "New Skool member → AI scores", "size": 42, "weight": "regular"},
        {"text": "them by revenue potential.", "size": 42, "weight": "regular"},
        {"text": "", "size": 16},
        {"text": "High-value = personal DM.", "size": 42, "weight": "regular"},
        {"text": "Others = email sequence.", "size": 42, "weight": "regular"},
        {"text": "", "size": 16},
        {"text": "No manual sorting. Just ROI.", "size": 44, "weight": "bold"},
    ],
    7: [
        {"text": "20+ hours saved", "size": 66, "weight": "bold"},
        {"text": "every single week.", "size": 66, "weight": "bold"},
        {"text": "", "size": 30},
        {"text": "110K followers in 12 months.", "size": 44, "weight": "regular"},
        {"text": "", "size": 16},
        {"text": "Stop being a worker.", "size": 46, "weight": "bold"},
        {"text": "Start being an operator.", "size": 46, "weight": "bold"},
    ],
    8: [
        {"text": "Want the blueprints?", "size": 62, "weight": "bold"},
        {"text": "", "size": 30},
        {"text": "My 30 best n8n automations", "size": 44, "weight": "regular"},
        {"text": "including all 5 from this carousel.", "size": 44, "weight": "regular"},
        {"text": "", "size": 40},
        {"text": "Comment 'AI' to get them free.", "size": 50, "weight": "bold"},
    ],
}

# Y positions per slide
Y_POS = {1: 120, 2: 140, 3: 80, 4: 100, 5: 100, 6: 100, 7: 120, 8: 200}

def generate_infographic(output_path):
    """Create slide 4 infographic: flow diagram on black bg."""
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font_lg = ImageFont.truetype(FONT_BOLD, 36)
        font_md = ImageFont.truetype(FONT_REG, 28)
        font_sm = ImageFont.truetype(FONT_REG, 22)
    except:
        font_lg = font_md = font_sm = ImageFont.load_default()
    
    # Colors
    GREEN = "#39FF14"
    ORANGE = "#FF6B35"
    WHITE = "#FFFFFF"
    DARK_GRAY = "#1a1a1a"
    
    # Flow: Reddit/YouTube → AI Brain → Content Ideas → Slack
    # Vertical flow diagram
    cy = 750  # center y for diagram
    boxes = [
        {"label": "Reddit + YouTube", "y": cy - 280, "color": ORANGE, "icon": "SCAN"},
        {"label": "AI Brain (n8n)", "y": cy - 90, "color": GREEN, "icon": "PROCESS"},
        {"label": "Content Ideas", "y": cy + 100, "color": GREEN, "icon": "OUTPUT"},
        {"label": "Slack Delivery", "y": cy + 290, "color": ORANGE, "icon": "DELIVER"},
    ]
    
    bw, bh = 400, 80
    cx = W // 2
    
    for i, box in enumerate(boxes):
        x1 = cx - bw // 2
        y1 = box["y"] - bh // 2
        x2 = cx + bw // 2
        y2 = box["y"] + bh // 2
        
        # Box with colored border
        draw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill=DARK_GRAY, outline=box["color"], width=3)
        
        # Label centered
        bbox = draw.textbbox((0, 0), box["label"], font=font_lg)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw//2, box["y"] - th//2), box["label"], fill=WHITE, font=font_lg)
        
        # Arrow to next
        if i < len(boxes) - 1:
            arrow_y1 = y2 + 5
            arrow_y2 = boxes[i+1]["y"] - bh//2 - 5
            draw.line([(cx, arrow_y1), (cx, arrow_y2)], fill=GREEN, width=3)
            # Arrowhead
            draw.polygon([(cx-8, arrow_y2-12), (cx+8, arrow_y2-12), (cx, arrow_y2)], fill=GREEN)
    
    # Side labels
    draw.text((cx + bw//2 + 20, boxes[0]["y"] - 12), "Every Monday", fill="#888888", font=font_sm)
    draw.text((cx + bw//2 + 20, boxes[1]["y"] - 12), "GPT-4 Analysis", fill="#888888", font=font_sm)
    draw.text((cx + bw//2 + 20, boxes[2]["y"] - 12), "Ranked by potential", fill="#888888", font=font_sm)
    draw.text((cx + bw//2 + 20, boxes[3]["y"] - 12), "Ready to film", fill="#888888", font=font_sm)
    
    # Title at top
    title = "HOW IT WORKS"
    bbox = draw.textbbox((0, 0), title, font=font_lg)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw//2, cy - 380), title, fill=GREEN, font=font_lg)
    
    # Decorative dots
    for dx in range(-3, 4):
        draw.ellipse([cx + dx*30 - 3, cy - 340, cx + dx*30 + 3, cy - 334], fill=GREEN if dx % 2 == 0 else ORANGE)
    
    img.save(output_path, quality=95)
    print(f"  ✅ Infographic: {output_path}")
    return output_path


def process_screenshot(output_path):
    """Use existing workflow screenshot for slide 3."""
    # Find best existing screenshot
    candidates = [
        "/data/.openclaw/workspace/carousel-001-images/slide4-workflow-carousel-darkmode.png",
        "/data/.openclaw/workspace/workflow-full-view.png",
        "/data/.openclaw/workspace/carousel-system/output/003/raw/workflow-full.png",
    ]
    src = None
    for c in candidates:
        if os.path.exists(c):
            src = c
            break
    
    if not src:
        print("❌ No workflow screenshot found!")
        return None
    
    # Scale proportionally and center crop to 1080x1350
    img = Image.open(src)
    target_w, target_h = 1080, 1350
    target_aspect = target_w / target_h
    img_aspect = img.width / img.height
    
    if img_aspect > target_aspect:
        new_h = target_h
        new_w = int(img.width * (target_h / img.height))
    else:
        new_w = target_w
        new_h = int(img.height * (target_w / img.width))
    
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))
    
    # Darken
    img = ImageEnhance.Brightness(img).enhance(0.70)
    img.save(output_path, quality=95)
    print(f"  ✅ Screenshot: {output_path}")
    return output_path


def upload_imgur(path):
    """Upload to imgur, return URL."""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    r = requests.post(
        "https://api.imgur.com/3/image",
        headers={"Authorization": "Client-ID 546c25a59c58ad7"},
        data={"image": b64, "type": "base64"},
        timeout=60
    )
    if r.status_code == 200:
        url = r.json()["data"]["link"]
        print(f"  📤 Uploaded: {url}")
        return url
    print(f"  ❌ Imgur error: {r.status_code}")
    return None


def main():
    # Step 1: Generate raw images
    print("=" * 50)
    print("STEP 1: Generate raw images")
    print("=" * 50)
    
    # Nano Banana for slides 1, 2, 5, 6, 7, 8
    for slide_num in [1, 2, 5, 6, 7, 8]:
        raw_path = str(RAW / f"slide-{slide_num:02d}-raw.png")
        if os.path.exists(raw_path):
            print(f"  ⏭️  Slide {slide_num} raw exists, skipping")
            continue
        ref = REF if slide_num in [1, 5, 7, 8] else REF  # Use ref for all to maintain style
        prompt = PROMPTS[slide_num]
        result = generate_image(prompt, "4:5", raw_path, reference_photo=ref)
        if not result:
            print(f"  ❌ Failed slide {slide_num}, retrying...")
            generate_image(prompt, "4:5", raw_path, reference_photo=ref)
    
    # Screenshot for slide 3
    raw_3 = str(RAW / "slide-03-raw.png")
    if not os.path.exists(raw_3):
        process_screenshot(raw_3)
    
    # Infographic for slide 4
    raw_4 = str(RAW / "slide-04-raw.png")
    if not os.path.exists(raw_4):
        generate_infographic(raw_4)
    
    # Step 2: Apply text overlay
    print("\n" + "=" * 50)
    print("STEP 2: Apply text overlay")
    print("=" * 50)
    
    for slide_num in range(1, 9):
        raw_path = str(RAW / f"slide-{slide_num:02d}-raw.png")
        final_path = str(FINAL / f"slide-{slide_num:02d}-final.png")
        
        if not os.path.exists(raw_path):
            print(f"  ❌ Missing raw for slide {slide_num}")
            continue
        
        add_text_overlay(
            raw_path,
            TEXTS[slide_num],
            final_path,
            aspect_ratio="4:5",
            y_offset=Y_POS[slide_num],
            x_offset=80,
        )
    
    # Step 3: Validate
    print("\n" + "=" * 50)
    print("STEP 3: Validate dimensions")
    print("=" * 50)
    
    all_good = True
    for slide_num in range(1, 9):
        final_path = str(FINAL / f"slide-{slide_num:02d}-final.png")
        if os.path.exists(final_path):
            img = Image.open(final_path)
            if img.size == (1080, 1350):
                print(f"  ✅ Slide {slide_num}: {img.size}")
            else:
                print(f"  ❌ Slide {slide_num}: {img.size} (expected 1080x1350)")
                all_good = False
        else:
            print(f"  ❌ Slide {slide_num}: MISSING")
            all_good = False
    
    if not all_good:
        print("\n⚠️  Some slides have issues!")
    
    # Step 4: Upload to imgur
    print("\n" + "=" * 50)
    print("STEP 4: Upload to imgur")
    print("=" * 50)
    
    urls = {}
    for slide_num in range(1, 9):
        final_path = str(FINAL / f"slide-{slide_num:02d}-final.png")
        if os.path.exists(final_path):
            url = upload_imgur(final_path)
            if url:
                urls[slide_num] = url
    
    # Summary
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    for i in range(1, 9):
        print(f"  Slide {i}: {urls.get(i, 'FAILED')}")
    
    # Save URLs
    with open(str(OUT / "imgur_urls.json"), "w") as f:
        json.dump(urls, f, indent=2)
    print(f"\nSaved to {OUT / 'imgur_urls.json'}")


if __name__ == "__main__":
    main()
