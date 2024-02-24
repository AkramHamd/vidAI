
from idea_generation.idea_generator import generate_and_choose_idea
from script_generation.script_generator import generate_script
from image_generation.image_generator import generate_images
from tts_generation.tts_generator import generate_voiceover
from video_creation.subtitle_generator import add_subtitles
from video_creation.video_creator import add_subtitles, create_video
from thumbnail_generation.thumbnail_creator import generate_dalle_thumbnail
from utils.utils import *
import youtube_upload.youtube_uploader as youtube_uploader
import os
import dotenv
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def main(niche):
    
    # #  Paso 1: Generar ideas basadas en el nicho y seleccionar una como título
    # #video_title = generate_and_choose_idea(niche)
    # print(f"Título del video (idea seleccionada): {video_title}")

    # # # Paso 2: Generar el script para el video
    # #script = generate_script(video_title)
    # print("Script generado.")

    # # # Paso 3: Generar imágenes para el video
    # num_prompts = 5
    # #images = generate_images(script, num_prompts, openai_api_key)

    # # images_directory = './downloaded_images/'
    # # images = list_image_files(images_directory)
    # print("Imágenes generadas.")

    # # # Paso 4: Generar TTS para el video
    # tts_files = generate_voiceover(script)
    # print("TTS generado.")

    # # # Paso 5: Crear el video sin subtítulos
    # unique_id = str(uuid.uuid4())
    # temp_video_title = sanitize_filename(video_title)
    # output_video_path = f"./videos/{temp_video_title}_{unique_id}.mp4"

    # temp_video_path = generate_temp_video_path(video_title)
    # create_video(images, tts_files, temp_video_path, output_video_path)

    print("Video temporal creado.")

    # # Paso 7: Generar la miniatura para el video
    #     thumbnail_path = generate_dalle_thumbnail(video_title, "./.temp/", openai_api_key, 1)
    #     #thumbnail_path = "./.temp/image_0.jpg"
    #     print("Miniatura generada.")

    output_video_path="../videos/Exploring_a_Haunted_House_Thrilling_Scares_&_Chilling_Secrets_6078239f-0bfb-401f-9b67-f4a3ba0811ed.mp4"
    video_title="TEST"
    # # Paso 8: Subir el video a YouTube con el título de la idea
    youtube_uploader.upload_video_to_youtube(
    video_file_path=output_video_path,
    title=video_title,
    description=f"A video about: {video_title}",
    category_id='22',
    keywords=['horror', 'scary stories', 'ghost tales', 'haunted places', 'supernatural', 'creepy tales', 'urban legends', 'chilling narrations', 'spooky content', 'paranormal activity', 'dark tales', 'eerie experiences', 'frightful stories', 'spine-tingling adventures', 'macabre mysteries', 'fear-inducing tales', 'horror narration', 'bone-chilling stories', 'terrifying encounters', 'mysterious phenomena'],  # Define las palabras clave apropiadas
    privacy_status='public',
    #thumbnail_file_path=thumbnail_path  # Assuming thumbnail_path is defined elsewhere
    )
    print("Video subido a YouTube con éxito.")

    

if __name__ == "__main__":
    niche = "Realistic horror stories"  # Define tu nicho
    main(niche)


