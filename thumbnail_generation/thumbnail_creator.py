from PIL import Image, ImageDraw, ImageFont

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
    font_size = 54
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text dimensions
    text_width, text_height = textsize(title, font)

    # Calculate text position to center it
    x_position = (base.width - text_width) / 2
    y_position = (base.height - text_height) / 2

    # Apply text to the image
    draw.text((x_position, y_position), title, fill="white", font=font)

    # Convert the image to RGB before saving
    rgb_base = base.convert("RGB")

    # Save the modified image
    rgb_base.save(output_path, "JPEG")

# Example usage
image_path = "./downloaded_images/image_0.jpg"
video_title = "Your Video Title Here"
output_path = "./.temp/thumbnail.jpg"
create_thumbnail(image_path, video_title, output_path)
