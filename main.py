import os
from idea_generation.idea_generator import generate_and_choose_idea
from script_generation.script_generator import generate_script
from tts_generation.tts_generator import generate_voiceover, get_audio_duration
from image_generation.image_generator import generate_dalle_images, generate_prompts_from_script
from video_creation.video_creator import create_video
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Fase 1: Generar Idea
    niche = "history"  # Ejemplo de nicho
    idea = generate_and_choose_idea(niche, openai_api_key)
    print(f"Idea seleccionada: {idea}")

    # Fase 2: Generar Guion
    script = generate_script(idea, openai_api_key)
    print("Guion generado")

    # Fase 3: Generar Voz en Off
    voiceover_path = generate_voiceover(script)
    print(f"Voz en off generada en: {voiceover_path}")

    # Fase 4: Generar Imágenes
    audio_duration = get_audio_duration(voiceover_path)  # Asegúrate de tener esta función definida
    num_images = int(audio_duration / 3)
    prompts = generate_prompts_from_script(script, num_images, openai_api_key)
    image_paths = generate_dalle_images(prompts, openai_api_key)
    print(f"{len(image_paths)} imágenes generadas")

    # Fase 5: Crear Video
    particle_overlay_path = "path/to/particle_overlay.mp4"  # Asegúrate de tener un archivo de overlay
    final_video_path = create_video(image_paths, voiceover_path, particle_overlay_path)
    print(f"Video creado en: {final_video_path}")

if __name__ == "__main__":
    main()
