from nano_banana import generate_image

prompt = "five cartoon lobster mascot characters in a team formation, hub and spoke layout, the center lobster is larger wearing sunglasses, four smaller lobsters each holding a different tool (magnifying glass, pen, clipboard, wrench), dark background, neon green glowing connection lines between them, vibrant, energetic, 3D cartoon style, team portrait, dark charcoal tech grid background, high quality, digital art, 16:9 aspect ratio"
output_path = "linkedin_lobster_team_v3_base.png"

# Generate base image
generate_image(prompt, "16:9", output_path)
