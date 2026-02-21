#!/usr/bin/env python3
import os
import requests
import base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Configuration
WIDTH = 1920
HEIGHT = 1080
OUTPUT_PATH = "linkedin_results_v6.png"
IMGUR_CLIENT_ID = "546c25a59c58ad7"

# Fonts
FONT_BOLD = "/data/.fonts/Roboto-Bold.ttf"
FONT_REGULAR = "/data/.fonts/Roboto-Regular.ttf"

def create_image():
    # 1. Create Dark Mode Background (Activity Feed)
    # Dark gray background
    bg_color = (18, 18, 18)
    img = Image.new('RGB', (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Border/Entry colors
    border_color = (40, 40, 40)
    success_green = (0, 255, 0)
    text_white = (255, 255, 255)
    text_gray = (180, 180, 180)
    
    # Load fonts for the feed
    feed_font_bold = ImageFont.truetype(FONT_BOLD, 32)
    feed_font_reg = ImageFont.truetype(FONT_REGULAR, 28)
    timestamp_font = ImageFont.truetype(FONT_REGULAR, 24)
    
    tasks = [
        ("14:02", "Researcher", "Trend analysis complete — 12 sources compiled"),
        ("13:58", "Writer", "Twitter thread delivered — 10 tweets ready"),
        ("13:45", "Chief of Staff", "Morning briefing sent to Telegram"),
        ("13:30", "Builder", "Landing page deployed — live at buildroom.ai"),
        ("13:12", "Publisher", "Instagram carousel posted — 6 slides"),
        ("12:55", "Orchestrator", "All tasks complete. Cost: $0.47"),
        ("12:40", "Researcher", "Market deep dive: Competitor analysis finished"),
        ("12:20", "Designer", "Asset batch V2 exported to S3"),
        ("11:55", "Orchestrator", "Routine maintenance: All agents synchronized"),
        ("11:30", "Writer", "Blog post draft: 'The Future of AI Teams' ready")
    ]
    
    # Draw feed entries
    y_start = 300 # Leave space for headline
    entry_height = 80
    
    for i, (ts, agent, desc) in enumerate(tasks):
        y = y_start + (i * entry_height)
        if y + entry_height > HEIGHT: break
        
        # Draw border
        draw.line([(50, y), (WIDTH-50, y)], fill=border_color, width=1)
        
        # Draw checkmark
        # Simple text [x] or draw a check
        draw.text((70, y + 25), "✓", fill=success_green, font=feed_font_bold)
        
        # Draw timestamp
        draw.text((120, y + 28), ts, fill=text_gray, font=timestamp_font)
        
        # Draw agent name
        draw.text((220, y + 25), f"{agent}:", fill=text_white, font=feed_font_bold)
        
        # Draw description
        # Measure agent text width to position description
        agent_w = draw.textbbox((220, y + 25), f"{agent}:", font=feed_font_bold)[2]
        draw.text((agent_w + 15, y + 25), desc, fill=text_white, font=feed_font_reg)

    # 2. Apply Subtle Dark Overlay behind text area (top 35%)
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    # Gradient or solid box with alpha
    overlay_draw.rectangle([0, 0, WIDTH, 350], fill=(0, 0, 0, 160))
    img = Image.alpha_composite(img.convert('RGBA'), overlay)

    # 3. Add Bold Yellow Headline
    headline_text = "Deploy Your AI Team in 60 Seconds"
    headline_size = 100
    headline_font = ImageFont.truetype(FONT_BOLD, headline_size)
    yellow_color = (255, 215, 0) # FFD700
    
    # Shadow layer
    shadow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    
    # Calculate text position (Top Center)
    bbox = headline_font.getbbox(headline_text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (WIDTH - tw) // 2
    ty = 120
    
    # Shadow
    s_offset = 6
    shadow_draw.text((tx + s_offset, ty + s_offset), headline_text, fill=(0, 0, 0, 255), font=headline_font)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=4))
    
    img = Image.alpha_composite(img, shadow_layer)
    
    # Text
    text_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    text_draw.text((tx, ty), headline_text, fill=yellow_color, font=headline_font)
    
    img = Image.alpha_composite(img, text_layer)
    
    # 4. Save
    img.convert('RGB').save(OUTPUT_PATH, quality=95)
    print(f"Image saved to {OUTPUT_PATH}")

def upload_to_imgur():
    with open(OUTPUT_PATH, "rb") as f:
        img_data = f.read()
    
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    data = {
        "image": base64.b64encode(img_data),
        "type": "base64",
        "title": "LinkedIn Results v6",
        "description": "AI Agent Activity Feed"
    }
    
    response = requests.post("https://api.imgur.com/3/image", headers=headers, data=data)
    if response.status_code == 200:
        url = response.json()["data"]["link"]
        print(f"Imgur URL: {url}")
        return url
    else:
        print(f"Upload failed: {response.text}")
        return None

if __name__ == "__main__":
    create_image()
    upload_to_imgur()
