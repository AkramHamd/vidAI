from PIL import Image, ImageDraw, ImageFont
import os
import requests
import json
from image_generation.image_generator import *

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def create_thumbnail(image_path, title, output_path="thumbnail.jpg"):
    # Load the base image
    base = Image.open(image_path).convert("RGBA")

    # Create a drawing object
    draw = ImageDraw.Draw(base)

    # Define the font and text size
    font_path = "./recursos/Heavitas.ttf"  # Make sure the font path is correct
    font_size = 86
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text dimensions
    text_width, text_height = textsize(title, font)

    # Calculate text position to center it
    x_position = (base.width - text_width) / 2
    y_position = (base.height - text_height) / 2

    # Shadow offset
    shadow_offset = 5

    # Shadow color
    shadow_color = 'black'

    # Text color
    text_color = 'red'

    # Draw shadow multiple times for a denser effect
    for offset in range(1, shadow_offset):
        draw.text((x_position + offset, y_position + offset), title, fill=shadow_color, font=font)
        draw.text((x_position - offset, y_position + offset), title, fill=shadow_color, font=font)
        draw.text((x_position + offset, y_position - offset), title, fill=shadow_color, font=font)
        draw.text((x_position - offset, y_position - offset), title, fill=shadow_color, font=font)

    # Then draw the text in red on top
    draw.text((x_position, y_position), title, fill=text_color, font=font)

    # Convert the image to RGB before saving
    rgb_base = base.convert("RGB")

    # Save the modified image
    rgb_base.save(output_path, "JPEG")

def generate_dalle_thumbnail(video_title, thumbnail_output_dir, openai_api_key, num_prompts=1):
    # Ensure the output directory exists
    if not os.path.exists(thumbnail_output_dir):
        os.makedirs(thumbnail_output_dir)

    # Define the prompt based on the video title
    prompt = f"A spooky thumbnail for the video titled: '{video_title}'"

    # Generate images using DALL-E 3
    image_path = generate_dalle_images([prompt], openai_api_key, thumbnail_output_dir, num_prompts)

    # Return the path of the generated thumbnail
    return image_path



# # Example usage
# image_path = "./downloaded_images/image_0.jpg"
# video_title = "Your Video Title Here"
# output_path = "./.temp/thumbnail.jpg"
# create_thumbnail(image_path, video_title, output_path)
