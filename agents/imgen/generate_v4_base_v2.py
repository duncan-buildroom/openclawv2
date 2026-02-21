from google import genai
from google.genai import types
import os
import sys
from PIL import Image
import io

# Configure API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found.")
    sys.exit(1)

client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

# Updated prompt based on v4 iteration requirements
prompt = """five cartoon lobster mascot characters in team formation, hub and spoke layout, center lobster larger wearing sunglasses with crossed arms, four smaller lobsters holding magnifying glass, pen, clipboard, wrench, clean dark gradient background (charcoal to slightly lighter charcoal), neon green glowing connection lines, vibrant 3D cartoon style, team portrait, simple clean composition. 

IMPORTANT: 
- BACKGROUND MUST BE CLEAN: NO circuit boards, NO matrix data streams, NO busy tech patterns. 
- Just a smooth, clean dark gradient.
- The lobsters should pop against the simplicity.
- Leave the top 30% of the image relatively clear for large text overlay.
- High-quality 3D render, vibrant colors.
- 16:9 aspect ratio."""

print("Generating v4 LinkedIn Image with Imagen 3 via google-genai...")

try:
    # Based on google-genai 1.0.0+ syntax
    # We use imagen-3.0-generate-001 or similar if available, 
    # but the previous script used 'models/nano-banana-pro-preview'
    # In the new SDK it might be different. 
    # Let's try to list models or just use the known name.
    
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
        output_path = "/data/.openclaw/workspace/agents/imgen/lobster_team_v4_base.png"
        image.save(output_path)
        print(f"✅ Saved: {output_path}")
        print(f"Dimensions: {image.size}")
    else:
        print("No images generated.")

except Exception as e:
    print(f"Error during generation: {e}")
    # Fallback to checking if it's the specific model name
    print("Trying with models/nano-banana-pro-preview...")
    try:
        response = client.models.generate_image(
            model='nano-banana-pro-preview',
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
            output_path = "/data/.openclaw/workspace/agents/imgen/lobster_team_v4_base.png"
            image.save(output_path)
            print(f"✅ Saved: {output_path}")
    except Exception as e2:
        print(f"Second attempt failed: {e2}")
