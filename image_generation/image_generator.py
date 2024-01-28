import openai
import requests
import os
import json
from textwrap import wrap
from dotenv import load_dotenv
from PIL import Image

# Cargar variables de entorno
load_dotenv()

def generate_prompts_from_script(script, num_prompts, openai_api_key):
    words_per_prompt = len(script.split()) // num_prompts
    wrapped_script = wrap(script, words_per_prompt)

    openai.api_key = openai_api_key
    prompts = []
    print("Generando prompts...")
    for part in wrapped_script:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Generate a creative idea for an image that represents: '{part}', remember the niche is photography",
            max_tokens=60
        )
        idea = response.choices[0].text.strip()
        prompts.append(idea)

    return prompts


def download_and_resize_image(url, save_path, target_size=(1920, 1080)):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        img = Image.open(save_path)
        img = img.resize(target_size, Image.LANCZOS)
        img.save(save_path)
    else:
        raise Exception(f"Error al descargar la imagen: {response.status_code}")


def generate_dalle_images(prompts, openai_api_key, images_dir="downloaded_images"):
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    }

    image_paths = []
    print("Generando imágenes...")
    for i, prompt in enumerate(prompts):
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1792x1024"
        }

        response = requests.post('https://api.openai.com/v1/images/generations',
                                 headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            image_url = response.json()['data'][0]['url']
            image_path = os.path.join(images_dir, f"image_{i}.jpg")
            download_and_resize_image(image_url, image_path)
            image_paths.append(image_path)
        else:
            
            if response.status_code != 200:
                print(f"Error al generar la imagen: {response.status_code}")
                print("Detalle del error:", response.text)  # Imprime el mensaje de error detallado
                continue  # Continúa con el siguiente prompt

            print(f"Error al generar la imagen: {response.status_code}")

    return image_paths


# Define el guion de voz en off
script = """
Welcome to the world of portrait photography, where every shot is a unique opportunity to capture the essence and personality of your subject. It's a skill that requires both technical knowledge and creative vision, and with practice and dedication, you can master it.

Are you tired of taking lackluster portraits that fail to truly capture the beauty and emotion of your subjects? Are you looking to elevate your photography game to the next level? Then this video is for you.

We will guide you through the fundamentals of portrait photography, from choosing the right camera and lenses, to understanding lighting techniques and posing your subject. We'll teach you how to use composition and framing to tell a powerful story through your images.

But mastering portrait photography is more than just technical skills. It's about connecting with your subject and creating a comfortable and collaborative environment. We'll show you how to build rapport with your subject and bring out their unique personality and authenticity in every shot.   

Whether you're a beginner or an experienced photographer, this video is packed with tips and tricks that will take your portrait game to the next level. Let us help you unlock your full potential as a portrait photographer and capture the beauty of every moment. Stay tuned and get ready to master the art of portrait photography!
"""

# Número de ideas que deseas generar
num_prompts = 2

# Clave de API de OpenAI obtenida del archivo .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# Genera las ideas para las imágenes basadas en el guion de voz en off
prompts = generate_prompts_from_script(script, num_prompts, openai_api_key)

with open("prompts.txt", "w") as file:
    for i, prompt in enumerate(prompts):
        file.write(f"Prompt {i + 1}:\n")
        file.write(prompt + "\n\n")

# Descarga las imágenes relacionadas con las ideas generadas
image_paths = generate_dalle_images(prompts, openai_api_key, images_dir="downloaded_images")

# Imprime las rutas de las imágenes descargadas
print("Imágenes descargadas:")
for image_path in image_paths:
    print(image_path)