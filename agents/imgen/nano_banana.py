#!/usr/bin/env python3
"""Nano Banana Pro image generation module."""

import os
import base64
import requests
from pathlib import Path

API_KEY = os.getenv("GOOGLE_API_KEY")
DEFAULT_REF = "/data/.openclaw/workspace/reference-photos/file_2---a14ce08d-ac3a-4916-b266-c920d21f40a0.jpg"
GEN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/nano-banana-pro-preview:generateContent?key={API_KEY}"

ASPECT_RATIOS = {"9:16", "4:5", "16:9", "1:1"}


def generate_image(prompt: str, aspect_ratio: str, output_path: str, reference_photo: str = DEFAULT_REF) -> str | None:
    """
    Generate an image using Nano Banana Pro.
    
    Args:
        prompt: Text prompt describing the desired image.
        aspect_ratio: One of "9:16", "4:5", "16:9", "1:1".
        output_path: Where to save the generated image.
        reference_photo: Path to reference photo for likeness matching.
    
    Returns:
        output_path on success, None on failure.
    """
    if aspect_ratio not in ASPECT_RATIOS:
        print(f"❌ Invalid aspect ratio '{aspect_ratio}'. Use: {ASPECT_RATIOS}")
        return None

    # Encode reference photo
    with open(reference_photo, "rb") as f:
        ref_b64 = base64.b64encode(f.read()).decode()

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": ref_b64}}
            ]
        }],
        "generationConfig": {
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": "2K"
            }
        }
    }

    print(f"  🎨 Generating {Path(output_path).stem}...", flush=True)
    try:
        response = requests.post(GEN_URL, json=payload, timeout=120)
    except requests.RequestException as e:
        print(f"  ❌ Request error: {e}", flush=True)
        return None

    if response.status_code != 200:
        print(f"  ❌ API error {response.status_code}: {response.text[:300]}", flush=True)
        return None

    data = response.json()
    try:
        for part in data["candidates"][0]["content"]["parts"]:
            if "inlineData" in part:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(part["inlineData"]["data"]))
                print(f"  ✅ Saved: {output_path}")
                return output_path
    except (KeyError, IndexError) as e:
        print(f"  ❌ Error extracting image: {e}")
        return None

    print(f"  ❌ No image in response")
    return None
