from google import genai
import os

api_key = "os.environ.get("GOOGLE_API_KEY", "")"
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

for model in client.models.list():
    print(model)
