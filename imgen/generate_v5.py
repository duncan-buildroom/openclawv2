import os
import sys
import base64
import requests
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from nano_banana import generate_image
from image_styling_system import DuncanImageStyler

# --- CONFIGURATION ---
PROMPT = "screenshot of a dark mode AI agent management dashboard, sleek modern UI, showing an orchestrator routing tasks to specialist agents named Researcher Writer Chief-of-Staff Builder, chat interface on left with agent activity feed on right, neon green accent highlights, clean minimal design, realistic software interface, high resolution product screenshot"
TEXT = "Deploy Your AI Team in 60 Seconds"
OUTPUT_FILENAME = "linkedin_agent_dashboard_v5.png"
BASE_FILENAME = "linkedin_agent_dashboard_v5_base.png"
IMGUR_CLIENT_ID = "546c25a59c58ad7"

class CustomStyler(DuncanImageStyler):
    TEXT_COLOR = "#FFD700"  # Bold Yellow
    
    def add_text_overlay(self, img, lines, y_offset):
        # Create shadow layer
        shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Create text layer
        text_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_layer)
        
        y = y_offset
        
        for line in lines:
            font_size = line["size"]
            weight = line.get("weight", "bold")
            
            try:
                # Use Roboto-Bold if available, else fallback
                font_path = "/data/.fonts/Roboto-Bold.ttf"
                if not os.path.exists(font_path):
                    font_path = self.FONT_BOLD
                font = ImageFont.truetype(font_path, font_size)
            except:
                font = ImageFont.load_default()
            
            # Calculate center position
            bbox = text_draw.textbbox((0, 0), line["text"], font=font)
            text_width = bbox[2] - bbox[0]
            line_x = (self.width - text_width) // 2
            
            # Draw shadow (heavy drop shadow as requested)
            shadow_offset = 6
            shadow_draw.text(
                (line_x + shadow_offset, y + shadow_offset),
                line["text"],
                fill=(0, 0, 0, 255),
                font=font
            )
            
            # Draw yellow text
            text_draw.text((line_x, y), line["text"], fill=self.TEXT_COLOR, font=font)
            
            y += font_size + self.LINE_SPACING
            
        # Blur shadow
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=4))
        
        # Composite
        result = Image.alpha_composite(img.convert('RGBA'), shadow)
        result = Image.alpha_composite(result, text_layer)
        return result

def upload_to_imgur(image_path):
    url = "https://api.imgur.com/3/image"
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read())
    
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    payload = {"image": image_data, "type": "base64"}
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()["data"]["link"]
    except Exception as e:
        print(f"Upload failed: {e}")
    return None

def main():
    # 1. Generate Base Image
    print("🎨 Generating base image with Nano Banana...")
    base_path = generate_image(PROMPT, "16:9", BASE_FILENAME)
    if not base_path:
        print("❌ Failed to generate base image.")
        sys.exit(1)
    
    # 2. Apply Styling
    print("🖌️ Applying text overlay and styling...")
    styler = CustomStyler(1920, 1080)
    
    # Text lines: "Deploy Your AI Team in 60 Seconds"
    # To take up top 25%, we can split or keep as one large line.
    # 90px+ Roboto Bold.
    text_blocks = [
        {"text": "Deploy Your AI Team", "size": 110, "weight": "bold"},
        {"text": "in 60 Seconds", "size": 110, "weight": "bold"}
    ]
    
    # y_offset: top center, starting higher up
    y_offset = 60 
    
    img = styler.prepare_image(base_path)
    # The prepare_image darkens by 0.85 by default.
    
    # Create a subtle dark overlay on the top section to make text pop even more
    draw = ImageDraw.Draw(img, 'RGBA')
    draw.rectangle([0, 0, 1920, 350], fill=(0, 0, 0, 180)) # Darken top 25% further
    
    result = styler.add_text_overlay(img, text_blocks, y_offset=y_offset)
    result.convert('RGB').save(OUTPUT_FILENAME, quality=95)
    print(f"✅ Styled image saved to {OUTPUT_FILENAME}")
    
    # 3. Upload to Imgur
    print("📤 Uploading to Imgur...")
    url = upload_to_imgur(OUTPUT_FILENAME)
    if url:
        print(f"🚀 SUCCESS: {url}")
        # Write the URL to a file so it's easily accessible
        with open("final_url.txt", "w") as f:
            f.write(url)
    else:
        print("❌ Imgur upload failed.")

if __name__ == "__main__":
    main()
