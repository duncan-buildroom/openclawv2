from google import genai
from google.genai import types
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import base64
import requests

# 1. API KEY SETUP
api_key = "os.environ.get("GOOGLE_API_KEY", "")"
os.environ["GOOGLE_API_KEY"] = api_key

# 2. IMAGE GENERATION (Nano Banana Pro)
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

prompt = """five vibrant 3D cartoon lobster mascot characters in team formation, hub and spoke layout. 
Center lobster is larger, wearing cool sunglasses, professional orchestrator pose with crossed arms. 
Four smaller specialist lobsters surround him, each holding a different tool: a magnifying glass, a pen, a clipboard, and a wrench. 
The background is a clean, simple dark charcoal gradient (NO circuit boards, NO tech patterns). 
Neon green glowing connection lines link the specialists to the center orchestrator. 
High-quality 3D render, vibrant lobster-orange colors, cinematic lighting, sharp focus. 
Leave the top 30% of the image clear for massive text overlay. 16:9 aspect ratio."""

output_base = "/data/.openclaw/workspace/agents/imgen/lobster_team_v4_base.png"
output_final = "/data/.openclaw/workspace/agents/imgen/linkedin_lobster_team_v4.png"

def generate_base():
    print("Generating v4 LinkedIn Image Base via Nano Banana Pro...")
    try:
        # Based on supported_actions=['generateContent', ...]
        response = client.models.generate_content(
            model='nano-banana-pro-preview',
            contents=prompt,
            config=types.GenerateContentConfig(
                # We need to find the correct parameter for image generation within generate_content
                # In some versions, it's automatic based on prompt or specific modality config
            )
        )

        # Check parts for image
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_bytes = base64.b64decode(part.inline_data.data)
                    image = Image.open(io.BytesIO(image_bytes))
                    image.save(output_base)
                    print(f"✅ Saved Base via generate_content")
                    return True
                if part.file_data:
                    print(f"Found file_data: {part.file_data}")

        print("No image data found in response parts.")
        print(f"Text response: {response.text}")

    except Exception as e:
        print(f"Generation error: {e}")
            
    return False

# 3. STYLING OVERLAY
def apply_v4_styling(input_path, output_path):
    img = Image.open(input_path).convert('RGBA')
    width, height = img.size
    
    text = "Deploy Your AI Team in 60 Seconds"
    font_color = "#FFD700"
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    font_size = 135 
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()
        
    draw = ImageDraw.Draw(img)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width = right - left
    
    x = (width - text_width) // 2
    y = 70
    
    # Shadow
    shadow_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    offset = 12
    sdraw.text((x+offset, y+offset), text, fill=(0,0,0,240), font=font)
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=7))
    img = Image.alpha_composite(img, shadow_img)
    
    # Text
    text_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(text_layer)
    tdraw.text((x, y), text, fill=font_color, font=font)
    img = Image.alpha_composite(img, text_layer)
    
    # Arrow
    arrow_x = width // 2
    arrow_y_start = y + (bottom - top) + 55
    arrow_y_end = arrow_y_start + 145
    
    arrow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    adraw = ImageDraw.Draw(arrow_layer)
    adraw.line([(arrow_x, arrow_y_start), (arrow_x, arrow_y_end)], fill=font_color, width=32)
    
    head_size = 65
    adraw.polygon([
        (arrow_x - head_size, arrow_y_end - head_size),
        (arrow_x + head_size, arrow_y_end - head_size),
        (arrow_x, arrow_y_end + 25)
    ], fill=font_color)
    
    # Arrow shadow
    ashadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    asdraw = ImageDraw.Draw(ashadow)
    asdraw.line([(arrow_x+6, arrow_y_start+6), (arrow_x+6, arrow_y_end+6)], fill=(0,0,0,190), width=32)
    asdraw.polygon([
        (arrow_x - head_size + 6, arrow_y_end - head_size + 6),
        (arrow_x + head_size + 6, arrow_y_end - head_size + 6),
        (arrow_x+6, arrow_y_end+31)
    ], fill=(0,0,0,190))
    ashadow = ashadow.filter(ImageFilter.GaussianBlur(radius=5))
    
    img = Image.alpha_composite(img, ashadow)
    img = Image.alpha_composite(img, arrow_layer)
    
    img.convert('RGB').save(output_path, quality=95)
    return output_path

# 4. IMGUR UPLOAD
def upload_imgur(file_path):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    resp = requests.post(
        "https://api.imgur.com/3/image",
        headers={"Authorization": "Client-ID 546c25a59c58ad7"},
        data={"image": b64, "type": "base64"},
        timeout=60
    )
    if resp.status_code == 200:
        return resp.json()["data"]["link"]
    return None

if __name__ == "__main__":
    if generate_base():
        apply_v4_styling(output_base, output_final)
        url = upload_imgur(output_final)
        print(f"RESULT_URL: {url}")
        print(f"RESULT_PATH: {output_final}")
    else:
        print("Failed to generate base image.")
