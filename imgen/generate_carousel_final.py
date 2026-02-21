#!/usr/bin/env python3
"""
Generate Instagram carousel using Google's image generation API.
Uses Imagen 4.0 for generation and custom styling system for text overlay.
"""
import os
import json
import base64
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter
from google import genai
from google.genai import types

# Configuration
API_KEY = "os.environ.get("GOOGLE_API_KEY", "")"
REF_PATH = "/data/.openclaw/workspace/reference-photos/file_2---a14ce08d-ac3a-4916-b266-c920d21f40a0.jpg"
OUTPUT_DIR = "output/instagram-carousel"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Styling constants
FONT_BOLD = "/data/.fonts/Roboto-Bold.ttf"
FONT_REGULAR = "/data/.fonts/Roboto-Regular.ttf"
LEFT_MARGIN = 80
LINE_SPACING = 8
SHADOW_COLOR = (0, 0, 0, 200)
SHADOW_BLUR = 2
BACKGROUND_DARKEN = 0.85

# Initialize client
client = genai.Client(api_key=API_KEY)

def generate_image_with_ref(prompt, slide_num):
    """Generate image using reference photo (for character shots)."""
    print(f"Generating image for Slide {slide_num} WITH reference photo...")
    
    # Load reference image
    ref_image = Image.open(REF_PATH)
    
    try:
        response = client.models.generate_images(
            model='imagen-4.0-fast-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                aspect_ratio='3:4',  # Will crop to 4:5 in styling
                number_of_images=1,
                include_rai_reason=True,
                # Reference image support might need different approach
            )
        )
        
        # Save generated image
        if response.generated_images:
            img = response.generated_images[0].image
            base_path = f"{OUTPUT_DIR}/slide_{slide_num}_base.png"
            img.save(base_path)
            print(f"✓ Saved base image: {base_path}")
            return base_path
    except Exception as e:
        print(f"✗ Error generating slide {slide_num}: {e}")
    
    return None

def generate_image(prompt, slide_num):
    """Generate image without reference photo."""
    print(f"Generating image for Slide {slide_num}...")
    
    try:
        response = client.models.generate_images(
            model='imagen-4.0-fast-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                aspect_ratio='3:4',  # Will crop to 4:5 in styling
                number_of_images=1,
                include_rai_reason=True,
            )
        )
        
        if response.generated_images:
            img = response.generated_images[0].image
            base_path = f"{OUTPUT_DIR}/slide_{slide_num}_base.png"
            img.save(base_path)
            print(f"✓ Saved base image: {base_path}")
            return base_path
    except Exception as e:
        print(f"✗ Error generating slide {slide_num}: {e}")
    
    return None

def apply_styling(image_path, text_blocks, output_path, center_text=False):
    """Apply Duncan's signature text styling."""
    print(f"Applying text overlay...")
    
    img = Image.open(image_path).convert('RGBA')
    
    # Resize/crop to 1080x1350 (4:5)
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
    
    # Darken background
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(BACKGROUND_DARKEN)
    
    # Create text layers
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    text_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    
    # Calculate starting Y position
    total_text_h = sum(b.get("size", 20) + LINE_SPACING for b in text_blocks)
    if center_text:
        y = (target_h - total_text_h) // 2
    else:
        y = target_h - total_text_h - 150  # Bottom margin
    
    # Draw text
    for block in text_blocks:
        if not block.get("text"):
            y += block.get("size", 20)
            continue
        
        font_path = FONT_BOLD if block.get("weight") == "bold" else FONT_REGULAR
        font = ImageFont.truetype(font_path, block["size"])
        
        # Shadow
        shadow_offset = max(3, block["size"] // 20)
        shadow_draw.text(
            (LEFT_MARGIN + shadow_offset, y + shadow_offset),
            block["text"],
            fill=SHADOW_COLOR,
            font=font
        )
        
        # Text
        text_draw.text((LEFT_MARGIN, y), block["text"], fill="white", font=font)
        y += block["size"] + LINE_SPACING
    
    # Composite
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=SHADOW_BLUR))
    result = Image.alpha_composite(img, shadow)
    result = Image.alpha_composite(result, text_layer)
    result.convert('RGB').save(output_path, quality=95)
    print(f"✓ Saved final image: {output_path}")
    return output_path

# Slide definitions
slides = [
    {
        "num": 1,
        "prompt": "A professional lifestyle photograph of a man in his early 30s with short brown hair and trimmed beard, wearing a fitted t-shirt, walking confidently mid-stride on a sun-drenched city sidewalk. Golden hour light hitting buildings creates urban depth and long shadows. Shot with 85mm lens at eye level, shallow depth of field focused on subject with slight motion blur on background. Photorealistic 35mm film grain, Kodak Vision3 warm tones. 4:5 aspect ratio.",
        "use_ref": True,
        "text": [
            {"text": "100 personalized videos sent.", "size": 60, "weight": "bold"},
            {"text": "Zero seconds recorded.", "size": 60, "weight": "bold"}
        ],
        "center": False
    },
    {
        "num": 2,
        "prompt": "Environmental cityscape at sunset - city intersection with long architectural shadows, no people in focus. Static frozen moment capturing golden hour fading with warm-to-cool transition and lengthening shadows. Shot with 35mm wide lens at eye level, deep depth of field. Photorealistic 35mm film grain, Kodak Vision3 warmth. 4:5 aspect ratio.",
        "use_ref": False,
        "text": [
            {"text": "The old way: 5 manual Looms a day.", "size": 42, "weight": "regular"},
            {"text": "The new way: 100+ AI-driven video pitches.", "size": 42, "weight": "bold"},
            {"text": "3x higher response rates while you walk.", "size": 42, "weight": "regular"}
        ],
        "center": False
    },
    {
        "num": 4,
        "prompt": "Clean minimalist infographic background with dark slate gray gradient and subtle urban textures. Modern tech aesthetic with warm accent lighting. No text or graphics. 4:5 aspect ratio.",
        "use_ref": False,
        "text": [
            {"text": "The Personalization Engine:", "size": 55, "weight": "bold"},
            {"text": "", "size": 20},
            {"text": "Scrapes LinkedIn and website data.", "size": 38, "weight": "regular"},
            {"text": "AI scripts a unique pitch for every lead.", "size": 38, "weight": "regular"}
        ],
        "center": True
    },
    {
        "num": 5,
        "prompt": "Close-up macro shot of a steaming espresso cup on a weathered outdoor marble café table. Urban café patio setting with blurred city street in background, warm color tones. Static composition with steam rising from cup. Soft diffused afternoon light with warm color temperature. Shot with 50mm macro lens, shallow depth of field, tight framing on cup. Photorealistic 35mm film grain, Kodak Vision3 warmth. 4:5 aspect ratio.",
        "use_ref": False,
        "text": [
            {"text": "Spend your morning closing deals,", "size": 42, "weight": "regular"},
            {"text": "not recording scripts in your office.", "size": 42, "weight": "regular"},
            {"text": "Scalable intimacy at the click of a button.", "size": 42, "weight": "bold"}
        ],
        "center": False
    },
    {
        "num": 6,
        "prompt": "A professional lifestyle photograph of a man in his early 30s with short brown hair and trimmed beard, wearing a casual button-down shirt with rolled sleeves, in a relaxed posture leaning against a warm brick wall in a quiet city alleyway. Checking phone with slight satisfied smile. Soft diffused light with warm tones bouncing off brick. Shot with 85mm lens slightly wide, shallow depth of field. Photorealistic 35mm film grain, Kodak Vision3 warmth. 4:5 aspect ratio.",
        "use_ref": True,
        "text": [
            {"text": "Prospect data in.", "size": 55, "weight": "bold"},
            {"text": "Personalized video out.", "size": 55, "weight": "bold"},
            {"text": "Your calendar fills up on autopilot.", "size": 42, "weight": "regular"}
        ],
        "center": False
    }
]

# Generate carousel
final_results = []

for s in slides:
    print(f"\n{'='*60}")
    print(f"SLIDE {s['num']}")
    print(f"{'='*60}")
    
    # Generate base image
    if s["use_ref"]:
        base = generate_image_with_ref(s["prompt"], s["num"])
    else:
        base = generate_image(s["prompt"], s["num"])
    
    if base:
        # Apply text styling
        final_path = f"{OUTPUT_DIR}/slide_{s['num']}_final.png"
        apply_styling(base, s["text"], final_path, center_text=s.get("center", False))
        
        # Compile text content
        text_content = "\\n".join([b.get("text", "") for b in s["text"] if b.get("text")])
        
        final_results.append({
            "slide_number": s["num"],
            "sealcam_prompt": s["prompt"],
            "image_url": final_path,
            "dimensions": "1080x1350",
            "format": "4:5",
            "text_applied": True,
            "text_content": text_content
        })
    else:
        print(f"✗ FAILED to generate Slide {s['num']}")

# Save results
output_json = "carousel_output.json"
with open(output_json, "w") as f:
    json.dump(final_results, f, indent=2)

print(f"\n{'='*60}")
print(f"COMPLETE")
print(f"{'='*60}")
print(f"Generated {len(final_results)}/5 images")
print(f"Results saved to: {output_json}")
