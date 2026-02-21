from image_styling_system import DuncanImageStyler, FORMATS
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys

def apply_custom_styling(input_path, output_path):
    # Dimensions for 16:9 (1920x1080)
    width, height = 1920, 1080
    styler = DuncanImageStyler(width, height)
    
    # Override settings for this specific request
    styler.TEXT_COLOR = "#FFD700"  # Yellow
    
    # Prepare image (resize, crop, darken)
    img = styler.prepare_image(input_path)
    
    # Text configuration
    lines = [
        {"text": "Deploy Your AI Team in 60 Seconds", "size": 100, "weight": "bold"}
    ]
    
    # Calculate text dimensions for centering
    try:
        font = ImageFont.truetype(styler.FONT_BOLD, 100)
    except:
        font = ImageFont.load_default()
        
    # Get text size using a temporary draw object
    temp_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    bbox = temp_draw.textbbox((0, 0), lines[0]["text"], font=font)
    text_width = bbox[2] - bbox[0]
    
    # Top Center position
    x_offset = (width - text_width) // 2
    y_offset = 150
    
    # Add text overlay without staggering
    result = styler.add_text_overlay(img, lines, y_offset, x_offset=x_offset, stagger=False)
    
    # Save output
    result.convert('RGB').save(output_path, quality=95)
    print(f"Saved styled image to {output_path}")

if __name__ == "__main__":
    apply_custom_styling("raw_dashboard.png", "linkedin_dashboard_v7.png")
