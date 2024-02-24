import openai
import os
from utils.utils import sanitize_filename
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def generate_script(idea):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"Create a compelling text for a video about {idea}. Don't include instructions or scenes, just include the story in plain text, avoid saying voice-over. The text should be maximum 100 words long and include hooks to keep the audience engaged."

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=3000  # Ajusta según la necesidad
    )
    
    script = response.choices[0].text.strip()
    
   # Limpiar el título para el nombre del archivo
    filename_safe_idea = sanitize_filename(idea)
    
    script_path = f"./scripts/{filename_safe_idea}.txt"

    script_path = f"./scripts/{filename_safe_idea}.txt"
    
    # Asegurarse de que el directorio existe
    os.makedirs(os.path.dirname(script_path), exist_ok=True)
    
    # Escribir el guion en un archivo
    with open(script_path, "w", encoding="utf-8") as file:
        file.write(script)
        
    print(f"Script guardado en: {script_path}")
    
    return script

# # # Ejemplo de uso
# idea = "Mastering Portrait Photography"
# script = generate_script(idea)
# print(script)
