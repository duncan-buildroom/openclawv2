#!/usr/bin/env python3
"""
Carousel 006: Claude 4.6 Prompt Pack
Full pipeline: generate → style → validate → upload
"""

import os
import sys
import base64
import io
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from google import genai
from google.genai import types

# ─── CONFIG ───────────────────────────────────────────────────────────────────
API_KEY = "os.environ.get("GOOGLE_API_KEY", "")"
IMGUR_CLIENT_ID = "546c25a59c58ad7"
OUTPUT_DIR = Path("/data/.openclaw/workspace/agents/imgen/output/carousel-006")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/data/.fonts/Roboto-Bold.ttf"
FONT_REGULAR = "/data/.fonts/Roboto-Regular.ttf"
REF_PHOTO = "/data/.openclaw/workspace/reference-photos/file_2---a14ce08d-ac3a-4916-b266-c920d21f40a0.jpg"
WORKFLOW_RAW = "/data/.openclaw/workspace/agents/imgen/output/instagram-carousel/workflow-raw.png"

TARGET_W, TARGET_H = 1080, 1350
DARKEN = 0.85
LEFT_MARGIN = 80
SCALE = 0.82  # 4:5 text scale factor

# ─── API CLIENT ───────────────────────────────────────────────────────────────
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1alpha'})

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def generate_image(prompt: str, output_path: str, with_ref: bool = True) -> bool:
    """Generate image via Nano Banana Pro."""
    print(f"  🎨 Generating {Path(output_path).stem}...")
    parts = [{"text": prompt}]
    
    if with_ref:
        with open(REF_PHOTO, "rb") as f:
            ref_b64 = base64.b64encode(f.read()).decode()
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": ref_b64}})
    
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "4:5"}
        }
    }
    
    try:
        resp = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/nano-banana-pro-preview:generateContent?key={API_KEY}",
            json=payload, timeout=120
        )
        if resp.status_code != 200:
            print(f"    ❌ API error {resp.status_code}: {resp.text[:200]}")
            return False
        
        data = resp.json()
        for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                img = Image.open(io.BytesIO(img_bytes))
                img.save(output_path, quality=95)
                print(f"    ✅ Saved: {Path(output_path).name} ({img.size})")
                return True
        print(f"    ❌ No image in response")
        return False
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False


def resize_crop(img: Image.Image, darken: float = DARKEN) -> Image.Image:
    """Proportionally resize to fill 1080x1350, center crop, darken."""
    img = img.convert("RGBA")
    src_w, src_h = img.size
    src_aspect = src_w / src_h
    tgt_aspect = TARGET_W / TARGET_H
    
    if src_aspect > tgt_aspect:
        # Wider than target: fit height
        new_h = TARGET_H
        new_w = int(src_w * (TARGET_H / src_h))
    else:
        # Taller than target: fit width
        new_w = TARGET_W
        new_h = int(src_h * (TARGET_W / src_w))
    
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - TARGET_W) // 2
    top = (new_h - TARGET_H) // 2
    img = img.crop((left, top, left + TARGET_W, top + TARGET_H))
    return ImageEnhance.Brightness(img).enhance(darken)


def add_text(img: Image.Image, lines: list, y_start: int, x_base: int = LEFT_MARGIN) -> Image.Image:
    """Add white text with drop shadow."""
    shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_layer)
    tdraw = ImageDraw.Draw(text_layer)
    
    y = y_start
    for line in lines:
        text = line.get("text", "")
        if not text:
            y += int(line.get("size", 20) * SCALE)
            continue
        
        size = max(12, int(line["size"] * SCALE))
        weight = line.get("weight", "regular")
        x_off = line.get("x_offset", x_base)
        
        try:
            font = ImageFont.truetype(FONT_BOLD if weight == "bold" else FONT_REGULAR, size)
        except:
            font = ImageFont.load_default()
        
        s = max(3, size // 20)
        sdraw.text((x_off + s, y + s), text, fill=(0, 0, 0, 200), font=font)
        tdraw.text((x_off, y), text, fill=(255, 255, 255, 255), font=font)
        y += size + 8
    
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=2))
    result = Image.alpha_composite(img.convert("RGBA"), shadow_layer)
    return Image.alpha_composite(result, text_layer)


def finalize(img: Image.Image, output_path: str) -> str:
    """Ensure 1080x1350, save as RGB PNG."""
    if img.size != (TARGET_W, TARGET_H):
        print(f"  ⚠️  Size mismatch {img.size}, resizing...")
        img = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    img.convert("RGB").save(output_path, format="PNG", optimize=False)
    print(f"  ✅ Finalized: {Path(output_path).name}")
    return output_path


def upload_imgur(file_path: str) -> str:
    """Upload to imgur, return URL."""
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    resp = requests.post(
        "https://api.imgur.com/3/image",
        headers={"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"},
        data={"image": b64, "type": "base64"},
        timeout=60
    )
    if resp.status_code == 200:
        url = resp.json()["data"]["link"]
        print(f"  📤 Imgur: {url}")
        return url
    else:
        print(f"  ❌ Imgur error {resp.status_code}: {resp.text[:100]}")
        return None


# ─── SLIDE 3: WORKFLOW SCREENSHOT ─────────────────────────────────────────────

def build_slide3():
    """Process n8n workflow screenshot for slide 3."""
    print("\n📸 Building Slide 3 (workflow screenshot)...")
    raw = Image.open(WORKFLOW_RAW)
    img = resize_crop(raw, darken=DARKEN)
    
    # Text: bottom-left quadrant
    text_lines = [
        {"text": "I built an automation that runs these prompts", "size": 52, "weight": "bold", "x_offset": 80},
        {"text": "on autopilot.", "size": 52, "weight": "bold", "x_offset": 80},
        {"text": "", "size": 16},
        {"text": "Pulls documents. Sends to Claude 4.6.", "size": 34, "weight": "regular", "x_offset": 100},
        {"text": "Delivers structured reports.", "size": 34, "weight": "regular", "x_offset": 100},
    ]
    
    # y_start: bottom portion (~70% down = y=945)
    img = add_text(img, text_lines, y_start=870)
    path = str(OUTPUT_DIR / "slide_03_final.png")
    return finalize(img, path)


# ─── SLIDE 4: INFOGRAPHIC ─────────────────────────────────────────────────────

def build_slide4():
    """Build infographic slide entirely with PIL."""
    print("\n🎨 Building Slide 4 (infographic)...")
    
    # Black background
    img = Image.new("RGB", (TARGET_W, TARGET_H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font_bold_lg = ImageFont.truetype(FONT_BOLD, int(54 * SCALE))
        font_bold_md = ImageFont.truetype(FONT_BOLD, int(34 * SCALE))
        font_bold_sm = ImageFont.truetype(FONT_BOLD, int(28 * SCALE))
        font_reg_sm = ImageFont.truetype(FONT_REGULAR, int(26 * SCALE))
        font_bold_xs = ImageFont.truetype(FONT_BOLD, int(22 * SCALE))
        font_reg_xs = ImageFont.truetype(FONT_REGULAR, int(20 * SCALE))
        font_num = ImageFont.truetype(FONT_BOLD, int(18 * SCALE))
    except Exception as e:
        print(f"  ❌ Font error: {e}")
        return None
    
    # Colors
    WHITE = (255, 255, 255)
    GRAY = (160, 160, 160)
    DARK_GRAY = (80, 80, 80)
    NEON_GREEN = (0, 255, 127)
    ORANGE = (255, 140, 0)
    BLUE = (64, 156, 255)
    PURPLE = (180, 80, 255)
    PINK = (255, 80, 180)
    
    # Header text
    y = 70
    draw.text((80, y), "5 categories. 20 prompts.", font=font_bold_lg, fill=WHITE)
    y += int(54 * SCALE) + 6
    draw.text((80, y), "Zero setup.", font=font_bold_lg, fill=WHITE)
    y += int(54 * SCALE) + 4
    draw.text((100, y), "Copy. Paste. Get results.", font=font_bold_md, fill=GRAY)
    y += int(34 * SCALE) + 40
    
    # Divider
    draw.line([(80, y), (TARGET_W - 80, y)], fill=DARK_GRAY, width=1)
    y += 30
    
    # Category data
    categories = [
        {
            "color": BLUE,
            "num": "01",
            "name": "Long-Context Analysis",
            "desc": "Audits hundreds of SOPs in one pass",
            "example": "Example: Scan 200-page SOP doc, flag gaps instantly"
        },
        {
            "color": PURPLE,
            "num": "02",
            "name": "Document Comprehension",
            "desc": "Extracts every obligation from any contract",
            "example": "Example: Pull all deadlines + clauses from MSA"
        },
        {
            "color": PINK,
            "num": "03",
            "name": "Frontend Design",
            "desc": "Builds a full landing page in 2 minutes",
            "example": "Example: Hero, social proof, CTA. One prompt."
        },
        {
            "color": NEON_GREEN,
            "num": "04",
            "name": "Business Planning",
            "desc": "Maps a 90-day launch plan with dependencies",
            "example": "Example: Full roadmap with milestones + owners"
        },
        {
            "color": ORANGE,
            "num": "05",
            "name": "Automation Architecture",
            "desc": "Designs multi-agent systems with real tool specs",
            "example": "Example: Full agent spec with APIs and triggers"
        },
    ]
    
    row_h = (TARGET_H - y - 120) // 5
    
    for cat in categories:
        # Colored left bar
        draw.rectangle([(80, y), (86, y + row_h - 16)], fill=cat["color"])
        
        # Number badge
        badge_x, badge_y = 96, y + 8
        draw.text((badge_x, badge_y), cat["num"], font=font_num, fill=cat["color"])
        
        # Category name
        name_y = y + 10
        draw.text((125, name_y), cat["name"], font=font_bold_sm, fill=WHITE)
        
        # Desc
        desc_y = name_y + int(28 * SCALE) + 6
        draw.text((125, desc_y), cat["desc"], font=font_reg_sm, fill=GRAY)
        
        # Example (smaller)
        ex_y = desc_y + int(26 * SCALE) + 4
        draw.text((125, ex_y), cat["example"], font=font_reg_xs, fill=DARK_GRAY)
        
        # Separator
        sep_y = y + row_h - 10
        draw.line([(80, sep_y), (TARGET_W - 80, sep_y)], fill=(30, 30, 30), width=1)
        
        y += row_h
    
    # Footer
    y = TARGET_H - 90
    draw.line([(80, y), (TARGET_W - 80, y)], fill=DARK_GRAY, width=1)
    y += 20
    draw.text((80, y), "@DuncanRogoff", font=font_bold_xs, fill=GRAY)
    
    # "20 PROMPTS" large numeral top-right
    draw.text((TARGET_W - 200, 70), "20", font=ImageFont.truetype(FONT_BOLD, 90), fill=(30, 30, 30))
    draw.text((TARGET_W - 220, 160), "PROMPTS", font=ImageFont.truetype(FONT_BOLD, 24), fill=(50, 50, 50))
    
    path = str(OUTPUT_DIR / "slide_04_final.png")
    img.save(path, format="PNG")
    print(f"  ✅ Infographic saved: slide_04_final.png")
    return path


# ─── SLIDE 8: CTA (blurred workflow) ─────────────────────────────────────────

def build_slide8(slide3_path: str):
    """Blurred slide 3 as background + large CTA text."""
    print("\n📸 Building Slide 8 (CTA)...")
    raw = Image.open(WORKFLOW_RAW)
    img = resize_crop(raw, darken=0.75)  # slightly darker for text contrast
    
    # Apply heavy blur
    blurred = img.filter(ImageFilter.GaussianBlur(radius=22))
    
    # Center headline: Comment "AI"
    img_final = blurred.convert("RGBA")
    
    text_config = [
        {"text": 'Comment "AI" to get all 20 prompts.', "size": 62, "weight": "bold", "x_offset": 80},
        {"text": "", "size": 20},
        {"text": "Free. No email required.", "size": 38, "weight": "regular", "x_offset": 100},
        {"text": "Sent automatically.", "size": 38, "weight": "regular", "x_offset": 100},
    ]
    
    img_final = add_text(img_final, text_config, y_start=480)
    path = str(OUTPUT_DIR / "slide_08_final.png")
    return finalize(img_final, path)


# ─── SLIDE STYLING FOR GENERATED IMAGES ──────────────────────────────────────

def style_slide(base_path: str, text_lines: list, output_path: str, y_start: int) -> str:
    """Load generated base image, resize/crop/darken, add text overlay."""
    try:
        raw = Image.open(base_path)
    except Exception as e:
        print(f"  ❌ Cannot open {base_path}: {e}")
        return None
    
    img = resize_crop(raw, darken=DARKEN)
    img = add_text(img, text_lines, y_start=y_start)
    return finalize(img, output_path)


# ─── TEXT CONFIGS FOR EACH SLIDE ──────────────────────────────────────────────

SLIDE_TEXTS = {
    1: {
        "lines": [
            {"text": "Claude 4.6 just dropped.", "size": 62, "weight": "bold", "x_offset": 80},
            {"text": "", "size": 16},
            {"text": "Here are 20 prompts built for it.", "size": 38, "weight": "regular", "x_offset": 100},
            {"text": "All free.", "size": 38, "weight": "regular", "x_offset": 100},
        ],
        "y_start": 120
    },
    2: {
        "lines": [
            {"text": "1 million tokens.", "size": 54, "weight": "bold", "x_offset": 80},
            {"text": "Near-Opus quality.", "size": 54, "weight": "bold", "x_offset": 80},
            {"text": "Sonnet price.", "size": 54, "weight": "bold", "x_offset": 80},
            {"text": "", "size": 20},
            {"text": "It can hold your entire business", "size": 34, "weight": "regular", "x_offset": 105},
            {"text": "in one prompt. 4.5 couldn't.", "size": 34, "weight": "regular", "x_offset": 105},
        ],
        "y_start": 120
    },
    5: {
        "lines": [
            {"text": "Paste 3 months of client emails.", "size": 54, "weight": "bold", "x_offset": 80},
            {"text": "Get every pattern.", "size": 54, "weight": "bold", "x_offset": 80},
            {"text": "", "size": 20},
            {"text": "Repeat questions. Template candidates.", "size": 32, "weight": "regular", "x_offset": 100},
            {"text": "Process fixes. One prompt.", "size": 32, "weight": "regular", "x_offset": 100},
        ],
        "y_start": 540
    },
    6: {
        "lines": [
            {"text": "Full landing page. Single HTML file.", "size": 54, "weight": "bold", "x_offset": 80},
            {"text": "2 minutes.", "size": 54, "weight": "bold", "x_offset": 80},
            {"text": "", "size": 20},
            {"text": "Hero, social proof, how it works, CTA.", "size": 32, "weight": "regular", "x_offset": 105},
            {"text": "Looks like a $5K agency built it.", "size": 32, "weight": "regular", "x_offset": 105},
        ],
        "y_start": 120
    },
    7: {
        "lines": [
            {"text": "110K followers. 12 months.", "size": 52, "weight": "bold", "x_offset": 80},
            {"text": "6 agents running for $5 a day.", "size": 52, "weight": "bold", "x_offset": 80},
            {"text": "", "size": 20},
            {"text": "I use prompts like these to run my agency.", "size": 32, "weight": "regular", "x_offset": 100},
            {"text": "Now they're yours.", "size": 32, "weight": "regular", "x_offset": 100},
        ],
        "y_start": 100
    },
}

# ─── IMAGE PROMPTS ─────────────────────────────────────────────────────────────

SLIDE_PROMPTS = {
    1: """Professional lifestyle photograph. The man from the reference photo wearing an orange hoodie stands at the entrance of a narrow Tokyo side-street alley at golden hour. Warm amber light from the left catches his face. He looks directly at the camera with relaxed confidence. Behind him: neon signs glow in Japanese, a narrow alley stretches into bokeh. Shot from slight low angle. Shallow depth of field. Cinematic, DSLR quality. 4:5 aspect ratio portrait. Leave upper-left area with darker building wall for text overlay.""",
    
    2: """Wide establishing shot of a narrow Tokyo side-street alley at golden hour. No people in frame. Neon signs glow in Japanese on both sides. Paper lanterns hang overhead. Warm golden haze at the far end of the alley where it opens up. Street food stall partially visible at left. Shot from ground level looking slightly upward. Deep perspective, cinematic composition. 4:5 portrait aspect ratio.""",
    
    5: """The man from the reference photo in an orange hoodie walking through a narrow Tokyo alley. Three-quarter angle view from the side. He looks down at his phone with a slight smile, as if reading impressive results. Warm neon glow from above catches his shoulder. Street food stall softly blurred in background. Open darker wall space visible on the left side for text overlay. Cinematic DSLR quality. 4:5 portrait.""",
    
    6: """Close-up detail shot: a laptop sitting on a rustic wooden surface at a small Tokyo street-side table. The screen glows with soft warm light, no visible UI on screen. A cup of tea on the right side, softly blurred. Warm neon light from outside casts a colored strip across the wooden surface. Shot from above at 45-degree angle. DSLR bokeh on background. An iPhone charging cable and small notebook also on the table. Cinematic product photography quality. 4:5 portrait ratio.""",
    
    7: """Tight portrait of the man from the reference photo, chest-up crop, standing in front of a neon-lit section of a Tokyo alley. Direct eye contact with camera. Genuine slight smile. Relaxed confidence. Warm amber neon light on his face. Orange hoodie. Different angle than a standard shot, this time closer and more intimate. Open darker space visible in the upper portion for text overlay. Cinematic DSLR quality. 4:5 portrait.""",
}


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    results = {}
    
    print("=" * 60)
    print("🚀 CAROUSEL 006: Claude 4.6 Prompt Pack")
    print("=" * 60)
    
    # ── STEP 1: Generate base images ──────────────────────────────
    print("\n📷 GENERATING BASE IMAGES...")
    
    for slide_num, prompt in SLIDE_PROMPTS.items():
        base_path = str(OUTPUT_DIR / f"slide_{slide_num:02d}_base.png")
        has_ref = slide_num in [1, 5, 7]  # character shots need reference
        success = generate_image(prompt, base_path, with_ref=has_ref)
        if not success:
            print(f"  ⚠️  Slide {slide_num} generation failed - will retry")
    
    # ── STEP 2: Style generated images ────────────────────────────
    print("\n✏️  APPLYING TEXT OVERLAYS...")
    
    for slide_num in [1, 2, 5, 6, 7]:
        base_path = str(OUTPUT_DIR / f"slide_{slide_num:02d}_base.png")
        out_path = str(OUTPUT_DIR / f"slide_{slide_num:02d}_final.png")
        
        if not Path(base_path).exists():
            print(f"  ❌ Missing base for slide {slide_num}")
            continue
        
        cfg = SLIDE_TEXTS[slide_num]
        result = style_slide(base_path, cfg["lines"], out_path, cfg["y_start"])
        if result:
            results[slide_num] = result
    
    # ── STEP 3: Build screenshot/infographic/CTA slides ───────────
    slide3_path = build_slide3()
    if slide3_path:
        results[3] = slide3_path
    
    slide4_path = build_slide4()
    if slide4_path:
        results[4] = slide4_path
    
    slide8_path = build_slide8(slide3_path or WORKFLOW_RAW)
    if slide8_path:
        results[8] = slide8_path
    
    # ── STEP 4: Validate all dimensions ───────────────────────────
    print("\n✅ VALIDATING DIMENSIONS...")
    for slide_num in sorted(results.keys()):
        path = results[slide_num]
        img = Image.open(path)
        w, h = img.size
        status = "✅" if (w, h) == (TARGET_W, TARGET_H) else "❌"
        print(f"  {status} Slide {slide_num}: {w}x{h} - {Path(path).name}")
        
        if (w, h) != (TARGET_W, TARGET_H):
            print(f"    🔧 Fixing dimensions...")
            img = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
            img.save(path, format="PNG")
            print(f"    ✅ Fixed to 1080x1350")
    
    # ── STEP 5: Upload to imgur ────────────────────────────────────
    print("\n📤 UPLOADING TO IMGUR...")
    imgur_urls = {}
    for slide_num in sorted(results.keys()):
        path = results[slide_num]
        url = upload_imgur(path)
        if url:
            imgur_urls[slide_num] = url
    
    # ── FINAL REPORT ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("🎉 CAROUSEL 006 COMPLETE")
    print("=" * 60)
    print(f"\nSlides generated: {len(results)}/8")
    print(f"Uploads succeeded: {len(imgur_urls)}/8")
    print("\n📎 IMGUR URLS:")
    for slide_num in sorted(imgur_urls.keys()):
        print(f"  Slide {slide_num}: {imgur_urls[slide_num]}")
    
    return imgur_urls


if __name__ == "__main__":
    main()
