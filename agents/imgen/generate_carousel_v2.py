import os
import requests
import base64
import json
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter

# Configuration
API_KEY = os.getenv("GOOGLE_API_KEY")
REF_PATH = "/data/.openclaw/workspace/reference-photos/file_2---a14ce08d-ac3a-4916-b266-c920d21f40a0.jpg"
OUTPUT_DIR = "output/instagram-carousel"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Image Styling System Constants
FONT_BOLD = "/data/.fonts/Roboto-Bold.ttf"
FONT_REGULAR = "/data/.fonts/Roboto-Regular.ttf"
LEFT_MARGIN = 80
LINE_SPACING = 8
SHADOW_COLOR = (0, 0, 0, 200)
SHADOW_BLUR = 2
BACKGROUND_DARKEN = 0.85

def generate_image_api(prompt, slide_num, use_ref=False):
    print(f"Generating image for Slide {slide_num}...")
    # sys.stdout.flush()
    import sys
    sys.stdout.flush()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={API_KEY}"
    
    parts = [{"text": prompt + " 4:5 aspect ratio. Photorealistic, cinematic."}]
    
    if use_ref:
        with open(REF_PATH, "rb") as f:
            encoded_ref = base64.b64encode(f.read()).decode("utf-8")
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": encoded_ref}})
    
    payload = {
        "contents": [{"parts": parts}]
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    # In some environments, Gemini 1.5 Pro returns image parts directly if it's acting as Nano Banana Pro
    # But usually it's a separate model. Given the workspace history, let's assume it returns an image part.
    # If it fails, we'll need to adjust.
    
    try:
        for part in data['candidates'][0]['content']['parts']:
            if 'inline_data' in part:
                img_data = base64.b64decode(part['inline_data']['data'])
                base_path = f"{OUTPUT_DIR}/slide_{slide_num}_base.png"
                with open(base_path, "wb") as f:
                    f.write(img_data)
                return base_path
    except Exception as e:
        print(f"Error extracting image for slide {slide_num}: {e}")
        print(f"Response: {response.text[:500]}")
    return None

def apply_styling(image_path, text_blocks, output_path):
    img = Image.open(image_path).convert('RGBA')
    
    # 1. Resize/Crop to 1080x1350 (4:5)
    target_w, target_h = 1080, 1350
    img_aspect = img.width / img.height
    target_aspect = target_w / target_h
    
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
    
    # 2. Darken
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(BACKGROUND_DARKEN)
    
    # 3. Text Overlay
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    text_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    
    # Calculate total height for bottom alignment
    total_text_h = sum(b.get("size", 20) + LINE_SPACING for b in text_blocks)
    y = target_h - total_text_h - 150 # Bottom margin
    
    # Center alignment for slide 4
    if "slide_4" in output_path:
        y = (target_h - total_text_h) // 2

    for block in text_blocks:
        if not block.get("text"):
            y += block.get("size", 20)
            continue
            
        font_path = FONT_BOLD if block.get("weight") == "bold" else FONT_REGULAR
        font = ImageFont.truetype(font_path, block["size"])
        
        # Shadow
        shadow_offset = max(3, block["size"] // 20)
        shadow_draw.text((LEFT_MARGIN + shadow_offset, y + shadow_offset), block["text"], fill=SHADOW_COLOR, font=font)
        
        # Text
        text_draw.text((LEFT_MARGIN, y), block["text"], fill="white", font=font)
        y += block["size"] + LINE_SPACING
        
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=SHADOW_BLUR))
    result = Image.alpha_composite(img, shadow)
    result = Image.alpha_composite(result, text_layer)
    result.convert('RGB').save(output_path, quality=95)
    return output_path

# SLIDES DEFINITION
slides = [
    {
        "num": 1,
        "prompt": "Subject: Duncan, early 30s, short brown hair, trimmed beard, fitted t-shirt, walking confidently. Environment: Sun-drenched city sidewalk, golden hour light hitting buildings, urban depth. Action: Mid-stride, candid, slight motion blur on background. Lighting: Golden hour, warm directional sunlight, long shadows. Camera: 85mm, eye level, shallow depth of field, focused on subject. Medium: Photorealistic, 35mm film grain, Kodak Vision3 warmth.",
        "use_ref": True,
        "text": [
            {"text": "100 personalized videos sent.", "size": 60, "weight": "bold"},
            {"text": "Zero seconds recorded.", "size": 60, "weight": "bold"}
        ]
    },
    {
        "num": 2,
        "prompt": "Subject: None. Environment: City intersection at sunset, long architectural shadows, no people in focus. Action: Static, frozen moment. Lighting: Golden hour fading, warm-to-cool transition, lengthening shadows. Camera: 35mm wide, eye level, deep depth of field. Medium: Photorealistic, 35mm film grain, Kodak Vision3 warmth.",
        "use_ref": False,
        "text": [
            {"text": "The old way: 5 manual Looms a day.", "size": 45, "weight": "regular"},
            {"text": "The new way: 100+ AI-driven video pitches.", "size": 45, "weight": "bold"},
            {"text": "3x higher response rates while you walk.", "size": 45, "weight": "regular"}
        ]
    },
    {
        "num": 4,
        "prompt": "Simple infographic background with urban textures, dark slate gray and warm wood accents. No text.",
        "use_ref": False,
        "text": [
            {"text": "The Personalization Engine:", "size": 55, "weight": "bold"},
            {"text": "", "size": 20},
            {"text": "Scrapes LinkedIn and website data.", "size": 40, "weight": "regular"},
            {"text": "AI scripts a unique pitch for every lead.", "size": 40, "weight": "regular"}
        ]
    },
    {
        "num": 5,
        "prompt": "Subject: Steaming espresso cup on a weathered outdoor marble café table. Environment: Urban café patio, blurred city street in background, warm tones. Action: Static, steam rising from cup. Lighting: Soft diffused afternoon light, warm color temperature. Camera: 50mm macro, shallow depth of field, tight framing on cup. Medium: Photorealistic, 35mm film grain, Kodak Vision3 warmth.",
        "use_ref": False,
        "text": [
            {"text": "Spend your morning closing deals,", "size": 45, "weight": "regular"},
            {"text": "not recording scripts in your office.", "size": 45, "weight": "regular"},
            {"text": "Scalable intimacy at the click of a button.", "size": 45, "weight": "bold"}
        ]
    },
    {
        "num": 6,
        "prompt": "Subject: Duncan, short brown hair, trimmed beard, casual button-down rolled sleeves, relaxed posture. Environment: Quiet city alleyway, warm brick walls, soft ambient light. Action: Leaning against wall, checking phone, slight satisfied smile. Lighting: Soft diffused light, warm tones bouncing off brick. Camera: 85mm, slightly wide, shallow depth of field. Medium: Photorealistic, 35mm film grain, Kodak Vision3 warmth.",
        "use_ref": True,
        "text": [
            {"text": "Prospect data in.", "size": 55, "weight": "bold"},
            {"text": "Personalized video out.", "size": 55, "weight": "bold"},
            {"text": "Your calendar fills up on autopilot.", "size": 45, "weight": "regular"}
        ]
    }
]

final_results = []
for s in slides:
    base = generate_image_api(s["prompt"], s["num"], s["use_ref"])
    if base:
        final_path = apply_styling(base, s["text"], f"{OUTPUT_DIR}/slide_{s['num']}_final.png")
        final_results.append({
            "slide_number": s["num"],
            "sealcam_prompt": s["prompt"],
            "image_url": final_path,
            "dimensions": "1080x1350",
            "format": "4:5",
            "text_applied": True,
            "text_content": " ".join([b.get("text", "") for b in s["text"]])
        })
    else:
        print(f"FAILED Slide {s['num']}")

with open("carousel_output.json", "w") as f:
    json.dump(final_results, f, indent=2)

print("Done.")
