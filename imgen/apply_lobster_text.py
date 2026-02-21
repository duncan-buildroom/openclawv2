import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path

# Paths (based on image_styling_system.py)
FONT_BOLD = "/data/.fonts/Roboto-Bold.ttf"

def add_lobster_text(image_path, output_path):
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    
    # 1. Darken background (85% brightness per system rules)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.85)
    
    # 2. Setup Drawing
    text_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    shadow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)
    
    # Text details
    text = "Deploy Your AI Team in 60 Seconds"
    # Large enough to read at thumbnail size. 16:9 1920x1080.
    # system uses 60-72pt for headlines. Let's go bigger for a single hero line.
    font_size = 90 
    try:
        font = ImageFont.truetype(FONT_BOLD, font_size)
    except:
        font = ImageFont.load_default()
        
    # Get text size to center it
    left, top, right, bottom = draw_text.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top
    
    x = (width - text_width) // 2
    y = 100 # Position at TOP
    
    # 3. Draw Yellow Text with Shadow
    yellow_color = "#FFD700"
    shadow_color = (0, 0, 0, 180) # Semi-transparent black
    shadow_offset = 5
    
    # Shadow
    draw_shadow.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=3))
    
    # Text
    draw_text.text((x, y), text, font=font, fill=yellow_color)
    
    # 4. Bold Arrow pointing DOWN
    # From below text toward the orchestrator (center)
    arrow_y_start = y + text_height + 40
    arrow_y_end = arrow_y_start + 80
    arrow_x = width // 2
    
    # Draw arrow on text layer
    arrow_width = 15
    # Shaft
    draw_text.line([(arrow_x, arrow_y_start), (arrow_x, arrow_y_end)], fill=yellow_color, width=arrow_width)
    # Head
    head_size = 40
    draw_text.polygon([
        (arrow_x - head_size, arrow_y_end - head_size),
        (arrow_x + head_size, arrow_y_end - head_size),
        (arrow_x, arrow_y_end)
    ], fill=yellow_color)
    
    # Composite
    combined = Image.alpha_composite(img, shadow_layer)
    combined = Image.alpha_composite(combined, text_layer)
    
    # Final save
    combined.convert('RGB').save(output_path, quality=95)
    print(f"✅ Text overlay complete: {output_path}")

if __name__ == "__main__":
    add_lobster_text("linkedin_lobster_team_v3_base.png", "linkedin_lobster_team_v3.png")
