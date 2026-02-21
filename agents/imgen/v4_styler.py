from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import sys

# Add current dir to path to import image_styling_system
sys.path.append('.')
from image_styling_system import DuncanImageStyler

def create_v4_image(base_image_path, output_path):
    width, height = 1920, 1080
    styler = DuncanImageStyler(width, height)
    
    # Override defaults for this specific iteration
    styler.TEXT_COLOR = "#FFD700"  # Yellow
    styler.LEFT_MARGIN = 0 # We'll center align manually
    styler.BACKGROUND_DARKEN = 1.0 # Background should already be clean/dark
    
    # 1. Prepare image (resize/crop)
    img = styler.prepare_image(base_image_path)
    
    # 2. Add "Deploy Your AI Team in 60 Seconds" at top center
    # We want it HUGE (80-90px or more)
    text = "Deploy Your AI Team in 60 Seconds"
    font_size = 110 # Extra big as requested
    
    try:
        font = ImageFont.truetype(styler.FONT_BOLD, font_size)
    except:
        font = ImageFont.load_default()
        
    draw = ImageDraw.Draw(img)
    
    # Calculate centering
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top
    
    x = (width - text_width) // 2
    y = 80 # Top margin
    
    # Add shadow
    shadow_offset = 6
    shadow_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.text((x + shadow_offset, y + shadow_offset), text, fill=(0, 0, 0, 220), font=font)
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=3))
    img = Image.alpha_composite(img.convert('RGBA'), shadow_img)
    
    # Add text
    text_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(text_layer)
    tdraw.text((x, y), text, fill="#FFD700", font=font)
    img = Image.alpha_composite(img, text_layer)
    
    # 3. Add yellow arrow pointing down to orchestrator
    # The center lobster is at the hub.
    # Hub usually is slightly below center to leave room for text.
    arrow_color = "#FFD700"
    arrow_x = width // 2
    arrow_y_start = y + text_height + 40
    arrow_y_end = arrow_y_start + 100
    
    # Draw a bold arrow
    arrow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    adraw = ImageDraw.Draw(arrow_layer)
    
    # Stem
    adraw.line([(arrow_x, arrow_y_start), (arrow_x, arrow_y_end)], fill=arrow_color, width=15)
    
    # Head
    head_size = 30
    adraw.polygon([
        (arrow_x - head_size, arrow_y_end - head_size),
        (arrow_x + head_size, arrow_y_end - head_size),
        (arrow_x, arrow_y_end + 10)
    ], fill=arrow_color)
    
    # Shadow for arrow
    ashadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    asdraw = ImageDraw.Draw(ashadow)
    asdraw.line([(arrow_x + 4, arrow_y_start + 4), (arrow_x + 4, arrow_y_end + 4)], fill=(0,0,0,150), width=15)
    asdraw.polygon([
        (arrow_x - head_size + 4, arrow_y_end - head_size + 4),
        (arrow_x + head_size + 4, arrow_y_end - head_size + 4),
        (arrow_x + 4, arrow_y_end + 10 + 4)
    ], fill=(0,0,0,150))
    ashadow = ashadow.filter(ImageFilter.GaussianBlur(radius=2))
    
    img = Image.alpha_composite(img, ashadow)
    img = Image.alpha_composite(img, arrow_layer)
    
    # Save
    img.convert('RGB').save(output_path, quality=95)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python v4_styler.py <input> <output>")
    else:
        create_v4_image(sys.argv[1], sys.argv[2])
