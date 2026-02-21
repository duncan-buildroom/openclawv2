from google import genai
import os

api_key = "os.environ.get("GOOGLE_API_KEY", "")"
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

prompt = "five cartoon lobsters"

try:
    # Try the most likely methods on the client or models
    print("Trying client.models.generate_content with image_generation model...")
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp-image-generation',
        contents=prompt
    )
    print(f"Success! Response: {response}")
    # Extract image if exists
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            print("Found inline_data (image?)")
except Exception as e:
    print(f"Error: {e}")
