#!/usr/bin/env python3
"""
Fix 3 slides for Carousel 006 (Claude 4.6 Prompt Pack)
- Slide 2: Re-center text vertically
- Slide 4: Replace infographic with Notion screenshot + text overlay
- Slide 5: Generate new image with Duncan on RIGHT, text on LEFT
"""

import os
import sys
import base64
import io
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# ─── CONFIG ───────────────────────────────────────────────────────────────────
API_KEY = "os.environ.get("GOOGLE_API_KEY", "")"
IMGUR_CLIENT_ID = "546c25a59c58ad7"
OUTPUT_DIR = Path("/data/.openclaw/workspace/agents/imgen/output/carousel-006")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/data/.fonts/Roboto-Bold.ttf"
FONT_REGULAR = "/data/.fonts/Roboto-Regular.ttf"
REF_PHOTO = "/data/.openclaw/workspace/reference-photos/file_2---a14ce08d-ac3a-4916-b266-c920d21f40a0.jpg"
NOTION_SCREENSHOT = "/data/.openclaw/workspace/carousel-system/notion-prompt-pack-screenshot.png"

TARGET_W, TARGET_H = 1080, 1350
DARKEN = 0.85
LEFT_MARGIN = 80
SCALE = 0.82

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def resize_crop(img: Image.Image, darken: float = DARKEN) -> Image.Image:
    """Proportionally resize to fill 1080x1350, center crop, darken."""
    img = img.convert("RGBA")
    src_w, src_h = img.size
    src_aspect = src_w / src_h
    tgt_aspect = TARGET_W / TARGET_H
    
    if src_aspect > tgt_aspect:
        new_h = TARGET_H
        new_w = int(src_w * (TARGET_H / src_h))
    else:
        new_w = TARGET_W
        new_h = int(src_h * (TARGET_W / src_w))
    
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - TARGET_W) // 2
    top = (new_h - TARGET_H) // 2
    img = img.crop((left, top, left + TARGET_W, top + TARGET_H))
    return ImageEnhance.Brightness(img).enhance(darken)


def measure_text_height(lines: list, scale: float = SCALE) -> int:
    """Calculate total height of text block."""
    total = 0
    for line in lines:
        text = line.get("text", "")
        size = int(line["size"] * scale)
        if not text:
            total += size
        else:
            total += size + 8  # line + spacing
    return total


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
    print(f"  ✅ Finalized: {Path(output_path).name} {img.size}")
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
        print(f"  ❌ Imgur error {resp.status_code}: {resp.text[:200]}")
        return None


def generate_image(prompt: str, output_path: str, with_ref: bool = False) -> bool:
    """Generate image via Gemini Flash."""
    print(f"  🎨 Generating {Path(output_path).stem}...")
    parts = [{"text": prompt}]
    
    if with_ref and Path(REF_PHOTO).exists():
        with open(REF_PHOTO, "rb") as f:
            ref_b64 = base64.b64encode(f.read()).decode()
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": ref_b64}})
    
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
        }
    }
    
    # Try gemini-2.0-flash-preview-image-generation first
    models_to_try = [
        "gemini-2.0-flash-preview-image-generation",
        "imagen-3.0-generate-002",
    ]
    
    for model in models_to_try:
        try:
            # For imagen, different endpoint
            if "imagen" in model:
                payload2 = {
                    "instances": [{"prompt": prompt}],
                    "parameters": {
                        "aspectRatio": "4:5",
                        "sampleCount": 1,
                    }
                }
                resp = requests.post(
                    f"https://us-central1-aiplatform.googleapis.com/v1/projects/gen-lang-client-0842961893/locations/us-central1/publishers/google/models/{model}:predict",
                    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                    json=payload2, timeout=120
                )
            else:
                resp = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}",
                    json=payload, timeout=120
                )
            
            if resp.status_code != 200:
                print(f"    ⚠️  {model}: {resp.status_code}: {resp.text[:100]}")
                continue
            
            data = resp.json()
            for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img_bytes = base64.b64decode(part["inlineData"]["data"])
                    img = Image.open(io.BytesIO(img_bytes))
                    img.save(output_path, quality=95)
                    print(f"    ✅ Saved: {Path(output_path).name} ({img.size})")
                    return True
        except Exception as e:
            print(f"    ⚠️  {model} error: {e}")
            continue
    
    print(f"    ❌ All models failed for {Path(output_path).stem}")
    return False


# ─── SLIDE 2: Re-center text ──────────────────────────────────────────────────

def fix_slide2():
    """Re-apply text at vertically centered position."""
    print("\n📐 Fixing Slide 2 (centering text)...")
    
    base_path = OUTPUT_DIR / "slide_02_base.png"
    out_path = str(OUTPUT_DIR / "slide_02_fixed.png")
    
    raw = Image.open(base_path)
    img = resize_crop(raw)
    
    text_lines = [
        {"text": "1 million tokens.", "size": 54, "weight": "bold", "x_offset": 80},
        {"text": "Near-Opus quality.", "size": 54, "weight": "bold", "x_offset": 80},
        {"text": "Sonnet price.", "size": 54, "weight": "bold", "x_offset": 80},
        {"text": "", "size": 20},
        {"text": "It can hold your entire business", "size": 34, "weight": "regular", "x_offset": 105},
        {"text": "in one prompt. 4.5 couldn't.", "size": 34, "weight": "regular", "x_offset": 105},
    ]
    
    # Calculate total text height and center it
    text_h = measure_text_height(text_lines)
    y_start = (TARGET_H - text_h) // 2
    print(f"  Text height: {text_h}px, y_start: {y_start}px (centered at {TARGET_H//2})")
    
    img = add_text(img, text_lines, y_start=y_start)
    return finalize(img, out_path)


# ─── SLIDE 4: Notion screenshot ───────────────────────────────────────────────

def fix_slide4():
    """Build slide 4 from Notion screenshot."""
    print("\n📸 Building Slide 4 (Notion screenshot)...")
    
    out_path = str(OUTPUT_DIR / "slide_04_fixed.png")
    
    raw = Image.open(NOTION_SCREENSHOT)
    print(f"  Source: {raw.size}")
    img = resize_crop(raw, darken=0.85)
    
    text_lines = [
        {"text": "5 categories. 20 prompts.", "size": 54, "weight": "bold", "x_offset": 80},
        {"text": "Zero setup.", "size": 54, "weight": "bold", "x_offset": 80},
        {"text": "", "size": 16},
        {"text": "Copy. Paste. Get results.", "size": 34, "weight": "regular", "x_offset": 100},
    ]
    
    # Bottom-left: calculate y_start from bottom
    text_h = measure_text_height(text_lines)
    y_start = TARGET_H - text_h - 150  # 150px from bottom
    print(f"  Text height: {text_h}px, y_start: {y_start}px")
    
    img = add_text(img, text_lines, y_start=y_start)
    return finalize(img, out_path)


# ─── SLIDE 5: New generation with Duncan on RIGHT ─────────────────────────────

def fix_slide5():
    """Generate new slide 5 with Duncan on right, text space on left."""
    print("\n🎨 Fixing Slide 5 (Duncan on RIGHT, text on LEFT)...")
    
    base_path = str(OUTPUT_DIR / "slide_05_right_base.png")
    out_path = str(OUTPUT_DIR / "slide_05_fixed.png")
    
    # First check if we already have a generated base
    if not Path(base_path).exists():
        prompt = """Cinematic DSLR street photography. A man in his 30s wearing a bright orange hoodie stands in the RIGHT HALF of the frame in a narrow Tokyo alley at night. He is leaning against the right wall, looking down at his phone with a slight smile. His face and body occupy the RIGHT THIRD of the image. The LEFT TWO-THIRDS of the frame is open: a dark textured wall or alley floor with atmospheric neon light reflections, providing clear empty space for text overlay. Red paper lanterns glow in the background. Wet cobblestones reflect orange neon light. Bokeh background. Shot from eye level. Warm amber neon lighting. High contrast, cinematic quality. 4:5 portrait format. IMPORTANT: Subject must be on the RIGHT side only, leaving the LEFT side completely clear for text."""
        
        success = generate_image(prompt, base_path, with_ref=True)
        if not success:
            print("  ❌ Generation failed, trying without ref photo...")
            success = generate_image(prompt, base_path, with_ref=False)
        
        if not success:
            # Fallback: use existing base but mirror it
            print("  ⚠️  Generation failed, trying to mirror existing base...")
            existing = Image.open(OUTPUT_DIR / "slide_05_base.png")
            mirrored = existing.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            mirrored.save(base_path)
            print(f"  ✅ Mirrored existing base: {mirrored.size}")
    else:
        print(f"  ✅ Using existing base: {base_path}")
    
    # Load and process
    raw = Image.open(base_path)
    img = resize_crop(raw)
    
    text_lines = [
        {"text": "Paste 3 months of", "size": 54, "weight": "bold", "x_offset": 80},
        {"text": "client emails.", "size": 54, "weight": "bold", "x_offset": 80},
        {"text": "Get every pattern.", "size": 54, "weight": "bold", "x_offset": 80},
        {"text": "", "size": 20},
        {"text": "Repeat questions.", "size": 30, "weight": "regular", "x_offset": 100},
        {"text": "Template candidates.", "size": 30, "weight": "regular", "x_offset": 100},
        {"text": "Process fixes. One prompt.", "size": 30, "weight": "regular", "x_offset": 100},
    ]
    
    # Vertically centered on LEFT side
    text_h = measure_text_height(text_lines)
    y_start = (TARGET_H - text_h) // 2
    print(f"  Text height: {text_h}px, y_start: {y_start}px")
    
    img = add_text(img, text_lines, y_start=y_start, x_base=80)
    return finalize(img, out_path)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("🔧 FIXING CAROUSEL 006 - 3 SLIDES")
    print("=" * 60)
    
    results = {}
    
    # Fix Slide 2
    path = fix_slide2()
    if path:
        results[2] = path
    
    # Fix Slide 4
    path = fix_slide4()
    if path:
        results[4] = path
    
    # Fix Slide 5
    path = fix_slide5()
    if path:
        results[5] = path
    
    # ── Validate ──────────────────────────────────────────────────
    print("\n✅ VALIDATING DIMENSIONS...")
    all_ok = True
    for slide_num in sorted(results.keys()):
        path = results[slide_num]
        img = Image.open(path)
        w, h = img.size
        status = "✅" if (w, h) == (TARGET_W, TARGET_H) else "❌"
        print(f"  {status} Slide {slide_num}: {w}x{h}")
        if (w, h) != (TARGET_W, TARGET_H):
            all_ok = False
    
    if not all_ok:
        print("  ⚠️  Fixing dimensions...")
        for slide_num in sorted(results.keys()):
            path = results[slide_num]
            img = Image.open(path)
            if img.size != (TARGET_W, TARGET_H):
                img = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
                img.save(path, format="PNG")
                print(f"    ✅ Fixed slide {slide_num}")
    
    # ── Upload ────────────────────────────────────────────────────
    print("\n📤 UPLOADING TO IMGUR...")
    imgur_urls = {}
    for slide_num in sorted(results.keys()):
        url = upload_imgur(results[slide_num])
        if url:
            imgur_urls[slide_num] = url
    
    # ── Report ────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("🎉 DONE")
    print("=" * 60)
    for slide_num in sorted(imgur_urls.keys()):
        print(f"  Slide {slide_num}: {imgur_urls[slide_num]}")
    
    return imgur_urls


if __name__ == "__main__":
    main()
