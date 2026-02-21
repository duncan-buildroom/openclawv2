from nano_banana import generate_image
import sys

prompt = "AI agent dashboard showing completed tasks and results, dark mode, futuristic"
output = "raw_dashboard.png"
aspect = "16:9"

print(f"Starting generation with prompt: {prompt}")
success = generate_image(prompt, aspect, output)

if success:
    print(f"Successfully generated {output}")
else:
    print("Generation failed")
    sys.exit(1)
