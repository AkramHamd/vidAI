from PIL import Image, ImageDraw, ImageFont

def create_thumbnail(image_path, title, output_path="thumbnail.jpg"):
    # Cargar la imagen base
    base = Image.open(image_path).convert("RGBA")
    
    # Crear una capa para el texto
    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)

    # Definir fuente y tamaño del texto
    font = ImageFont.load_default()  # Aquí puedes personalizar la fuente
    text_size = draw.textsize(title, font=font)

    # Posición del texto
    text_position = ((base.width - text_size[0]) // 2, (base.height - text_size[1]) // 2)

    # Aplicar texto a la imagen
    draw.text(text_position, title, fill=(255, 255, 255, 255), font=font)

    # Combinar la imagen con la capa de texto
    combined = Image.alpha_composite(base, txt)

    # Guardar la miniatura
    combined.save(output_path, "JPEG")

# Ejemplo de uso
image_path = "path/to/selected_image.jpg"
video_title = "Tu Título de Video Aquí"
create_thumbnail(image_path, video_title)
