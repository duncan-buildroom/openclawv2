from google.genai import Client
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

# 2. IMAGE GENERATION (Imagen 3)
client = Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

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
    print("Generating v4 LinkedIn Image Base via Imagen 3...")
    try:
        # Based on the user's setup, they might be using 'imagen-3.0-generate-001'
        # with the NEW SDK 'google-genai' which I have.
        
        response = client.models.generate_image(
            model='imagen-3.0-generate-001',
            prompt=prompt,
            config=types.GenerateImageConfig(
                aspect_ratio='16:9',
                number_of_images=1,
                output_mime_type='image/png'
            )
        )

        if response.generated_images:
            image_bytes = response.generated_images[0].image_bytes
            image = Image.open(io.BytesIO(image_bytes))
            image.save(output_base)
            print(f"✅ Saved Base: {output_base}")
            return True
        else:
            print("No images generated.")
            return False
    except Exception as e:
        print(f"Imagen error: {e}")
        return False

# 3. STYLING OVERLAY
def apply_v4_styling(input_path, output_path):
    img = Image.open(input_path).convert('RGBA')
    width, height = img.size
    
    # 120px Bold Yellow Roboto (or Liberation Sans)
    # The user wanted "OVERSIZED" - takes up 25-30% of image.
    text = "Deploy Your AI Team in 60 Seconds"
    font_color = "#FFD700"
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    font_size = 120
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()
        
    draw = ImageDraw.Draw(img)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width = right - left
    
    x = (width - text_width) // 2
    y = 80
    
    # Drop Shadow
    shadow_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    offset = 8
    sdraw.text((x+offset, y+offset), text, fill=(0,0,0,230), font=font)
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=5))
    
    img = Image.alpha_composite(img, shadow_img)
    
    # Yellow Text
    text_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(text_layer)
    tdraw.text((x, y), text, fill=font_color, font=font)
    img = Image.alpha_composite(img, text_layer)
    
    # Yellow Arrow pointing down to orchestrator (center)
    arrow_x = width // 2
    arrow_y_start = y + (bottom - top) + 50
    arrow_y_end = arrow_y_start + 130
    
    arrow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    adraw = ImageDraw.Draw(arrow_layer)
    adraw.line([(arrow_x, arrow_y_start), (arrow_x, arrow_y_end)], fill=font_color, width=25)
    
    head_size = 50
    adraw.polygon([
        (arrow_x - head_size, arrow_y_end - head_size),
        (arrow_x + head_size, arrow_y_end - head_size),
        (arrow_x, arrow_y_end + 15)
    ], fill=font_color)
    
    # Arrow shadow
    ashadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    asdraw = ImageDraw.Draw(ashadow)
    asdraw.line([(arrow_x+5, arrow_y_start+5), (arrow_x+5, arrow_y_end+5)], fill=(0,0,0,180), width=25)
    asdraw.polygon([
        (arrow_x - head_size + 5, arrow_y_end - head_size + 5),
        (arrow_x + head_size + 5, arrow_y_end - head_size + 5),
        (arrow_x+5, arrow_y_end+20)
    ], fill=(0,0,0,180))
    ashadow = ashadow.filter(ImageFilter.GaussianBlur(radius=4))
    
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
