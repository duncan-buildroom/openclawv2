import google.generativeai as genai
import os
import sys
from PIL import Image

# Configure API
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Fallback: using the generativeai library with the specific model name
# If 'google.generativeai' was not found before, I'll try to find where it is or if it's named differently.
# But wait, 'google-genai' is installed, which is the NEW SDK. 
# The new SDK uses client.models.generate_content or client.models.imagen.generate_images?
# Actually, the new SDK (google-genai) has client.models.generate_image? 
# I got "'Models' object has no attribute 'generate_image'".
# Let's check the new SDK docs briefly or try another approach.

prompt = """five cartoon lobster mascot characters in team formation, hub and spoke layout, center lobster larger wearing sunglasses with crossed arms, four smaller lobsters holding magnifying glass, pen, clipboard, wrench, clean dark gradient background (charcoal to slightly lighter charcoal), neon green glowing connection lines, vibrant 3D cartoon style, team portrait, simple clean composition. 

IMPORTANT: 
- BACKGROUND MUST BE CLEAN: NO circuit boards, NO matrix data streams, NO busy tech patterns. 
- Just a smooth, clean dark gradient.
- The lobsters should pop against the simplicity.
- Leave the top 30% of the image relatively clear for large text overlay.
- High-quality 3D render, vibrant colors.
- 16:9 aspect ratio."""

# Try the older library if it exists in another path or under a different name
try:
    import google.generativeai as genai
    model = genai.GenerativeModel("models/nano-banana-pro-preview")
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            image_config=genai.ImageConfig(
                aspect_ratio="16:9",
                image_size="2K"
            )
        )
    )
    for part in response.parts:
        if image := part.as_image():
            image.save("/data/.openclaw/workspace/agents/imgen/lobster_team_v4_base.png")
            print("Saved via google.generativeai")
except Exception as e:
    print(f"google.generativeai failed: {e}")
