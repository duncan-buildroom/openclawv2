import os
import json
import base64
import requests
from pathlib import Path
from image_styling_system import DuncanImageStyler
from nano_banana import generate_image as nb_generate_image

# --- CONFIGURATION ---
IMGUR_CLIENT_ID = "546c25a59c58ad7"
OUTPUT_DIR = Path("output/insta_carousel")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Duncan's reference likeness
REF_PHOTO = "/data/.openclaw/workspace/reference-photos/file_2---a14ce08d-ac3a-4916-b266-c920d21f40a0.jpg"

# SEALCAM Framework & Proximity
SEALCAM_TWEAKS = "Photorealistic 35mm film grain, Kodak Vision3 warm tones. High-end professional photography. NO text in the image."

def upload_to_imgur(file_path):
    """Uploads a file to Imgur and returns the URL."""
    print(f"  ☁️ Uploading {Path(file_path).name} to Imgur...", flush=True)
    url = "https://api.imgur.com/3/image"
    with open(file_path, "rb") as f:
        img_data = f.read()
    
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    payload = {"image": base64.b64encode(img_data)}
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        response.raise_for_status()
        return response.json()["data"]["link"]
    except Exception as e:
        print(f"  ❌ Imgur upload failed: {e}", flush=True)
        return None

def process_text_for_styler(text_string):
    """Splits text into headline and body, scaling for 4:5."""
    parts = text_string.split('\n')
    styled_blocks = []
    
    # Text scaling factor: 0.82x for 4:5
    headline_size = int(54) 
    body_size = int(36)
    
    for i, line in enumerate(parts):
        # First line usually headline
        if i == 0:
            styled_blocks.append({"text": line, "size": headline_size, "weight": "bold"})
        else:
            styled_blocks.append({"text": line, "size": body_size, "weight": "regular"})
            
    return styled_blocks

def generate_carousel_task(slides_json):
    styler = DuncanImageStyler(1080, 1350)
    final_urls = []
    
    for slide in slides_json:
        num = slide["slide_number"]
        concept = slide["image_concept"]
        text = slide["text"]
        shot_type = slide["shot_type"]
        
        print(f"\n--- Processing Slide {num} ({shot_type}) ---", flush=True)
        
        base_img_path = OUTPUT_DIR / f"slide_{num}_base.png"
        final_img_path = OUTPUT_DIR / f"slide_{num}_final.png"
        
        # 1. Generate/Prepare Background
        if "SCREENSHOT_NEEDED" in concept:
            # Create dark placeholder
            from PIL import Image
            placeholder = Image.new('RGB', (1080, 1350), (20, 20, 25))
            placeholder.save(base_img_path)
            y_pos = "center"
        else:
            # Generate via Nano Banana
            prompt = f"{concept} {SEALCAM_TWEAKS}"
            if "character" in shot_type or "composite" in shot_type:
                # Use likeness
                nb_generate_image(prompt, "4:5", str(base_img_path), reference_photo=REF_PHOTO)
            else:
                # Establishing/Detail - still use nb_generate_image but likeness might be ignored or subtle
                nb_generate_image(prompt, "4:5", str(base_img_path))
            y_pos = "bottom" if num != 7 else "center"

        # 2. Style Text
        text_blocks = process_text_for_styler(text)
        if "cta" in slide:
            text_blocks.append({"text": "", "size": 20})
            text_blocks.append({"text": slide["cta"], "size": 36, "weight": "bold"})
            
        styler.generate(str(base_img_path), text_blocks, y_position=y_pos, output_path=str(final_img_path))
        
        # 3. Upload
        url = upload_to_imgur(final_img_path)
        final_urls.append(url)
        
    return final_urls

if __name__ == "__main__":
    import sys
    input_data = [
      {
        "slide_number": 1,
        "text": "Cold outreach is dead.\nUnless it's personal.",
        "shot_type": "character",
        "image_concept": "Duncan in an orange hoodie sitting at a small round marble table in a bright, modern minimalist coffee shop. He is looking off-camera with a neutral expression, holding a white ceramic mug. Natural morning light, shallow depth of field."
      },
      {
        "slide_number": 2,
        "text": "Text-only emails get ignored.\nPersonalized video gets 5x responses.\nMost people are too lazy to record them.",
        "shot_type": "establishing",
        "image_concept": "Wide shot of the modern coffee shop interior. Minimalist wooden furniture, large floor-to-ceiling windows, a few plants, and soft morning sunlight casting long shadows. Calm, productive atmosphere."
      },
      {
        "slide_number": 3,
        "text": "I built an n8n automation that does it for you.\nIt scrapes prospect data and generates 1:1 videos.\nZero manual recording required.",
        "shot_type": "screenshot",
        "image_concept": "SCREENSHOT_NEEDED: High-level n8n workflow view showing the full Personalized Video Prospector automation. Clean, organized layout."
      },
      {
        "slide_number": 4,
        "text": "The AI analyzes their LinkedIn profile.\nIt scripts a custom message based on their bio.\nThen it renders a video in seconds.",
        "shot_type": "detail",
        "image_concept": "Close-up detail shot of a laptop screen on the cafe table showing a blurred LinkedIn profile page. Beside it, a half-eaten croissant on a small plate. Focus is on the texture of the croissant and the edge of the laptop."
      },
      {
        "slide_number": 5,
        "text": "Scale 1:1 outreach without the effort.\nSend 100 personalized videos while you sleep.\nThis is how you win in 2026.",
        "shot_type": "screenshot",
        "image_concept": "SCREENSHOT_NEEDED: Detailed view of the n8n AI node configuration, showing the prompt logic that merges LinkedIn data into the video script template."
      },
      {
        "slide_number": 6,
        "text": "Stop sending generic templates.\nStart sending assets that actually convert.\nAutomate the personality.",
        "shot_type": "character",
        "image_concept": "Low angle shot of Duncan from the chest up, wearing his orange hoodie, walking out of the coffee shop into the sunlight. He is looking down at his phone with a slight, focused expression. Casual, street-style vibe."
      },
      {
        "slide_number": 7,
        "text": "I am giving away the entire workflow.\nPlus 29 other AI automations.",
        "shot_type": "composite",
        "image_concept": "A split-screen composition. Left side: A close-up of Duncan's face (reference likeness) looking directly at the camera. Right side: A blurred, aesthetically pleasing grid view of various n8n workflow icons representing the '30 automations' library.",
        "cta": "Comment 'AI' to get access to all 30 automations"
      }
    ]
    
    urls = generate_carousel_task(input_data)
    print("\n--- FINAL URLS ---", flush=True)
    for i, url in enumerate(urls):
        print(f"Slide {i+1}: {url}", flush=True)
