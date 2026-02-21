from google import genai
import os

api_key = "os.environ.get("GOOGLE_API_KEY", "")"
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

# Get model details for Nano Banana Pro
model = client.models.get(model='nano-banana-pro-preview')
print(model)
