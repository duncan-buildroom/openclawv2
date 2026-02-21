from google import genai
import os
from PIL import Image
from image_styling_system import create_styled_image
import json

# Configure API
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
ref_path = "/data/.openclaw/workspace/reference-photos/file_2---a14ce08d-ac3a-4916-b266-c920d21f40a0.jpg"
# We'll use the path directly in the API call if possible, or read it

output_dir = "output/instagram-carousel"
os.makedirs(output_dir, exist_ok=True)

results = []

def generate_image(prompt, slide_num, use_ref=False):
    print(f"Generating image for Slide {slide_num}...")
    
    config = {
        "aspect_ratio": "4:5",
    }
    
    inputs = [prompt]
    if use_ref:
        # Load ref image for the SDK
        ref_image = Image.open(ref_path)
        inputs.append(ref_image)
    
    response = client.models.generate_image(
        model="imagen-3.0-generate-001",
        prompt=prompt,
        config=genai.types.GenerateImageConfig(
            aspect_ratio="4:5",
            number_of_images=1,
            include_rai_reason=True,
        )
    )
    # The SDK for imagen-3.0 might be different. Let's check the nano_banana_proper_api.py again.
    # Actually, the user's script used 'models/nano-banana-pro-preview'.
    
    for part in response.parts:
        if image := part.as_image():
            base_path = f"{output_dir}/slide_{slide_num}_base.png"
            image.save(base_path)
            return base_path
    return None

# SLIDE 1
prompt1 = "Duncan, early 30s, short brown hair, trimmed beard, fitted t-shirt, walking confidently. Sun-drenched city sidewalk, golden hour light hitting buildings, urban depth. Mid-stride, candid, slight motion blur on background. Golden hour, warm directional sunlight, long shadows. 85mm, eye level, shallow depth of field, focused on subject. Photorealistic, 35mm film grain, Kodak Vision3 warmth."
base1 = generate_image(prompt1, 1, use_ref=True)
text1 = [
    {"text": "100 personalized videos sent.", "size": 60, "weight": "bold"},
    {"text": "Zero seconds recorded.", "size": 60, "weight": "bold"}
]
create_styled_image(base1, text1, format="instagram", y_position="bottom", output_path=f"{output_dir}/slide_1_final.png")
results.append({
    "slide_number": 1,
    "sealcam_prompt": prompt1,
    "image_url": f"{output_dir}/slide_1_final.png",
    "dimensions": "1080x1350",
    "format": "4:5",
    "text_applied": True,
    "text_content": "100 personalized videos sent.\\nZero seconds recorded."
})

# SLIDE 2
prompt2 = "Environmental shot. City intersection at sunset, long architectural shadows, no people in focus. Static, frozen moment. Golden hour fading, warm-to-cool transition, lengthening shadows. 35mm wide, eye level, deep depth of field. Photorealistic, 35mm film grain, Kodak Vision3 warmth."
base2 = generate_image(prompt2, 2, use_ref=False)
text2 = [
    {"text": "The old way: 5 manual Looms a day.", "size": 45, "weight": "regular"},
    {"text": "The new way: 100+ AI-driven video pitches.", "size": 45, "weight": "bold"},
    {"text": "3x higher response rates while you walk.", "size": 45, "weight": "regular"}
]
create_styled_image(base2, text2, format="instagram", y_position="bottom", output_path=f"{output_dir}/slide_2_final.png")
results.append({
    "slide_number": 2,
    "sealcam_prompt": prompt2,
    "image_url": f"{output_dir}/slide_2_final.png",
    "dimensions": "1080x1350",
    "format": "4:5",
    "text_applied": True,
    "text_content": "The old way: 5 manual Looms a day.\\nThe new way: 100+ AI-driven video pitches.\\n3x higher response rates while you walk."
})

# SLIDE 4 - Infographic
# We'll use the same generation model for a clean base, or just a simple colored background
prompt4 = "A clean, minimalist infographic background with subtle urban textures. Dark gray aesthetic. 4:5 aspect ratio."
base4 = generate_image(prompt4, 4, use_ref=False)
text4 = [
    {"text": "The Personalization Engine:", "size": 55, "weight": "bold"},
    {"text": "", "size": 20},
    {"text": "Scrapes LinkedIn and website data.", "size": 40, "weight": "regular"},
    {"text": "AI scripts a unique pitch for every lead.", "size": 40, "weight": "regular"}
]
create_styled_image(base4, text4, format="instagram", y_position="center", output_path=f"{output_dir}/slide_4_final.png")
results.append({
    "slide_number": 4,
    "sealcam_prompt": "Simple infographic background",
    "image_url": f"{output_dir}/slide_4_final.png",
    "dimensions": "1080x1350",
    "format": "4:5",
    "text_applied": True,
    "text_content": "The Personalization Engine:\\nScrapes LinkedIn and website data.\\nAI scripts a unique pitch for every lead."
})

# SLIDE 5
prompt5 = "Steaming espresso cup on a weathered outdoor marble café table. Urban café patio, blurred city street in background, warm tones. Static, steam rising from cup. Soft diffused afternoon light, warm color temperature. 50mm macro, shallow depth of field, tight framing on cup. Photorealistic, 35mm film grain, Kodak Vision3 warmth."
base5 = generate_image(prompt5, 5, use_ref=False)
text5 = [
    {"text": "Spend your morning closing deals,", "size": 45, "weight": "regular"},
    {"text": "not recording scripts in your office.", "size": 45, "weight": "regular"},
    {"text": "Scalable intimacy at the click of a button.", "size": 45, "weight": "bold"}
]
create_styled_image(base5, text5, format="instagram", y_position="bottom", output_path=f"{output_dir}/slide_5_final.png")
results.append({
    "slide_number": 5,
    "sealcam_prompt": prompt5,
    "image_url": f"{output_dir}/slide_5_final.png",
    "dimensions": "1080x1350",
    "format": "4:5",
    "text_applied": True,
    "text_content": "Spend your morning closing deals,\\nnot recording scripts in your office.\\nScalable intimacy at the click of a button."
})

# SLIDE 6
prompt6 = "Duncan, short brown hair, trimmed beard, casual button-down rolled sleeves, relaxed posture. Quiet city alleyway, warm brick walls, soft ambient light. Leaning against wall, checking phone, slight satisfied smile. Soft diffused light, warm tones bouncing off brick. 85mm, slightly wide, shallow depth of field. Photorealistic, 35mm film grain, Kodak Vision3 warmth."
base6 = generate_image(prompt6, 6, use_ref=True)
text6 = [
    {"text": "Prospect data in.", "size": 55, "weight": "bold"},
    {"text": "Personalized video out.", "size": 55, "weight": "bold"},
    {"text": "Your calendar fills up on autopilot.", "size": 45, "weight": "regular"}
]
create_styled_image(base6, text6, format="instagram", y_position="bottom", output_path=f"{output_dir}/slide_6_final.png")
results.append({
    "slide_number": 6,
    "sealcam_prompt": prompt6,
    "image_url": f"{output_dir}/slide_6_final.png",
    "dimensions": "1080x1350",
    "format": "4:5",
    "text_applied": True,
    "text_content": "Prospect data in.\\nPersonalized video out.\\nYour calendar fills up on autopilot."
})

with open("carousel_output.json", "w") as f:
    json.dump(results, f, indent=2)

print("Batch complete. Results saved to carousel_output.json")
