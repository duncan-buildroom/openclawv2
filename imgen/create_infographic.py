#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# Create output directory
os.makedirs('output/instagram-carousel', exist_ok=True)

# Instagram 4:5 format
width = 1080
height = 1350

# Create image with dark background
bg_color = (20, 20, 30)
img = Image.new('RGB', (width, height), bg_color)
draw = ImageDraw.Draw(img)

# Define colors
stage_bg = (40, 40, 60)
arrow_color = (100, 150, 255)
text_color = (255, 255, 255)
accent_color = (100, 150, 255)

# Calculate stage dimensions and positions
stage_width = 280
stage_height = 200
vertical_center = 500  # Center vertically in the image
horizontal_spacing = 100
start_x = 80

# Draw three stages
stages = [
    {"name": "Prospect\nData", "icon": "📊", "y": vertical_center},
    {"name": "AI\nEngine", "icon": "🤖", "y": vertical_center},
    {"name": "Personalized\nVideo", "icon": "📧", "y": vertical_center}
]

try:
    # Try to load a font, fall back to default
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    font_icon = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 64)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_icon = ImageFont.load_default()

# Draw stages and arrows
for i, stage in enumerate(stages):
    x = start_x + i * (stage_width + horizontal_spacing)
    y = stage["y"]
    
    # Draw stage box with rounded corners
    draw.rounded_rectangle(
        [x, y, x + stage_width, y + stage_height],
        radius=15,
        fill=stage_bg,
        outline=accent_color,
        width=3
    )
    
    # Draw icon
    icon_bbox = draw.textbbox((0, 0), stage["icon"], font=font_icon)
    icon_width = icon_bbox[2] - icon_bbox[0]
    icon_x = x + (stage_width - icon_width) // 2
    icon_y = y + 40
    draw.text((icon_x, icon_y), stage["icon"], fill=text_color, font=font_icon)
    
    # Draw stage name
    name_bbox = draw.textbbox((0, 0), stage["name"], font=font_medium)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = x + (stage_width - name_width) // 2
    name_y = y + 130
    draw.text((name_x, name_y), stage["name"], fill=text_color, font=font_medium, align='center')
    
    # Draw arrow to next stage
    if i < len(stages) - 1:
        arrow_start_x = x + stage_width + 10
        arrow_end_x = x + stage_width + horizontal_spacing - 10
        arrow_y = y + stage_height // 2
        
        # Arrow line
        draw.line(
            [(arrow_start_x, arrow_y), (arrow_end_x, arrow_y)],
            fill=arrow_color,
            width=5
        )
        
        # Arrow head
        draw.polygon(
            [
                (arrow_end_x, arrow_y),
                (arrow_end_x - 15, arrow_y - 10),
                (arrow_end_x - 15, arrow_y + 10)
            ],
            fill=arrow_color
        )

# Add text overlay at the top
overlay_text = "The Personalization Engine:\nScrapes LinkedIn and website data.\nAI scripts a unique pitch for every lead."
text_y = 100

# Draw semi-transparent background for text
text_bg_height = 180
draw.rectangle(
    [0, text_y - 30, width, text_y + text_bg_height],
    fill=(20, 20, 30, 230)
)

# Draw text
lines = overlay_text.split('\n')
current_y = text_y
for line in lines:
    bbox = draw.textbbox((0, 0), line, font=font_small)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    draw.text((text_x, current_y), line, fill=accent_color if current_y == text_y else text_color, font=font_small)
    current_y += 50

# Save base image
img.save('output/instagram-carousel/slide_4_base.png', quality=95)
print("Base image saved")

# Create final image (same as base for this infographic)
img.save('output/instagram-carousel/slide_4_final.png', quality=95)
print("Final image saved")

print("Image generation complete!")
