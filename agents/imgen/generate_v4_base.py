import google.generativeai as genai
import os
import sys
from PIL import Image

# Configure API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found.")
    sys.exit(1)

genai.configure(api_key=api_key)

# The model name for Nano Banana Pro in this environment
MODEL_NAME = "models/nano-banana-pro-preview"

# Updated prompt based on v4 iteration requirements
prompt = """five cartoon lobster mascot characters in team formation, hub and spoke layout, center lobster larger wearing sunglasses with crossed arms, four smaller lobsters holding magnifying glass, pen, clipboard, wrench, clean dark gradient background (charcoal to slightly lighter charcoal), neon green glowing connection lines, vibrant 3D cartoon style, team portrait, simple clean composition. 

IMPORTANT: 
- BACKGROUND MUST BE CLEAN: NO circuit boards, NO matrix data streams, NO busy tech patterns. 
- Just a smooth, clean dark gradient.
- The lobsters should pop against the simplicity.
- Leave the top 30% of the image relatively clear for large text overlay.
- High-quality 3D render, vibrant colors.
- 16:9 aspect ratio."""

print("Generating v4 LinkedIn Image with Nano Banana Pro...")

try:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            image_config=genai.ImageConfig(
                aspect_ratio="16:9",
                image_size="2K"
            )
        )
    )

    image_found = False
    for part in response.parts:
        if image := part.as_image():
            output_path = "/data/.openclaw/workspace/agents/imgen/lobster_team_v4_base.png"
            image.save(output_path)
            print(f"✅ Saved: {output_path}")
            print(f"Dimensions: {image.size}")
            image_found = True
            break
    
    if not image_found:
        print("No image found in response parts.")
        if response.text:
            print(response.text)

except Exception as e:
    print(f"Error during generation: {e}")
