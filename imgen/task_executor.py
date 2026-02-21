import sys
import os
import base64
import requests
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from image_styling_system import DuncanImageStyler

def upload_to_imgur(image_path):
    client_id = "546c25a59c58ad7"
    url = "https://api.imgur.com/3/image"
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read())
    
    headers = {"Authorization": f"Client-ID {client_id}"}
    payload = {"image": image_data, "type": "base64"}
    
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        print(f"Imgur upload failed: {response.status_code}")
        print(response.text)
        return None

# Duncan's customized styler for this specific request
class CustomStyler(DuncanImageStyler):
    TEXT_COLOR = "#FFD700"  # Bold Yellow
    LEFT_MARGIN = 0 # Will calculate center
    
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
                font_path = self.FONT_BOLD if weight == "bold" else self.FONT_REGULAR
                font = ImageFont.truetype(font_path, font_size)
            except:
                font = ImageFont.load_default()
            
            # Calculate center position
            bbox = text_draw.textbbox((0, 0), line["text"], font=font)
            text_width = bbox[2] - bbox[0]
            line_x = (self.width - text_width) // 2
            
            # Draw shadow (larger for very large text)
            shadow_offset = 5
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
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=3))
        
        # Composite
        result = Image.alpha_composite(img.convert('RGBA'), shadow)
        result = Image.alpha_composite(result, text_layer)
        return result

# 1. Generate the base image using Nano Banana (via exec)
# Since I cannot directly call Nano Banana tool, I will use a placeholder or 
# assume the main agent wants me to generate it. 
# Wait, I am the subagent tasked to generate it. I have browser tool.
# I will use a reliable prompt to generate an image via a web service if I had one,
# but usually I would use a tool like `image_gen`.
# Looking at my tools... I don't have a direct `image_gen`.
# I'll check if there's an image generation tool I missed.
# read, write, edit, exec, process, web_search, web_fetch, browser, canvas, nodes, message, image, tts.
# No image_gen tool.
# I'll check the main agent's request again. 
# "Nano Banana prompt guidance: ..."
# Maybe I should use the canvas or browser to find/generate?
# Actually, I'll check if I can use a local command for image generation if installed.
# Or perhaps I should ask the main agent? 
# Wait, I see 'image' tool but that's for analysis.
# Let's check `openclaw help` to see if there's a hidden tool.

pass
