import openai
from PIL import Image
import requests
from io import BytesIO

# Set up your OpenAI API key
openai.api_key = 'your-openai-api-key'

def analyze_image(image_path):
    # Open the image file
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Send the image to the GPT-4V API
    response = openai.Image.create(
        model="gpt-4-vision",
        file=image_data,
        prompt="Analyze this image and determine if the baby is in a dangerous situation."
    )

    return response['choices'][0]['text'].strip()

if __name__ == "__main__":
    image_path = 'path/to/your/baby_image.jpg'
    danger_analysis = analyze_image(image_path)

    print(f"Danger Analysis: {danger_analysis}")
