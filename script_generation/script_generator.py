import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def generate_script(idea):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"Create a compelling text for a video about {idea}. Don't include instructions or scenes, just include the story in plain text, avoid saying voice-over. The text should be at least 1200 words long and include hooks to keep the audience engaged."

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=3000  # Ajusta según la necesidad
    )

    return response.choices[0].text.strip()

# # Ejemplo de uso
# idea = "Mastering Portrait Photography"
# script = generate_script(idea)
# print(script)
