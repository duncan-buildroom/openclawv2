from google import genai
import os
import base64

api_key = "os.environ.get("GOOGLE_API_KEY", "")"
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

prompt = "five cartoon lobsters"

response = client.models.generate_content(
    model='nano-banana-pro-preview',
    contents=prompt
)

if response.candidates:
    for i, part in enumerate(response.candidates[0].content.parts):
        print(f"Part {i}: {part}")
        if part.inline_data:
            print(f"Part {i} has inline_data, length: {len(part.inline_data.data)}")
            # Write first 100 bytes to check header
            print(f"Part {i} prefix: {part.inline_data.data[:100]}")
