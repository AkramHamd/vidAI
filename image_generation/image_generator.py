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
            prompt=f"Generate a creative idea for an image that represents: '{part}', remember the niche is realistic horror stories",
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


def generate_images(script, num_prompts, openai_api_key):
    prompts = generate_prompts_from_script(script, num_prompts, openai_api_key)
    image_paths = generate_dalle_images(prompts, openai_api_key)
    return image_paths