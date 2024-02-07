
from idea_generation.idea_generator import generate_and_choose_idea
from script_generation.script_generator import generate_script
from image_generation.image_generator import generate_images
from tts_generation.tts_generator import generate_voiceover
from video_creation.subtitle_generator import add_subtitles
from video_creation.video_creator import add_subtitles, create_video
from thumbnail_generation.thumbnail_creator import create_thumbnail
from utils.utils import generate_temp_video_path, list_image_files
import youtube_upload.youtube_uploader as youtube_uploader
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def main(niche):
    # Paso 1: Generar ideas basadas en el nicho y seleccionar una como título
    video_title = generate_and_choose_idea(niche)
    print(f"Título del video (idea seleccionada): {video_title}")

    # Paso 2: Generar el script para el video
    script = generate_script(video_title)
    print("Script generado.")

    # Paso 3: Generar imágenes para el video
    num_prompts = 5
    #images = generate_images(script, num_prompts, openai_api_key)
    #images = './temp_resized_images/'
    
    images_directory = './downloaded_images/'
    images = list_image_files(images_directory)
    print("Imágenes generadas.")

    # Paso 4: Generar TTS para el video
    tts_files = generate_voiceover(script)
    print("TTS generado.")

    # Paso 5: Crear el video sin subtítulos
    temp_video_path = generate_temp_video_path(video_title)

    create_video(images, tts_files, temp_video_path)
    print("Video temporal creado.")

    # Paso 6: Añadir subtítulos al video
    final_video_path = f"./videos/{video_title}.mp4"
    add_subtitles(temp_video_path, final_video_path)
    print("Subtítulos añadidos al video.")

    # # Paso 7: Generar la miniatura para el video
    # thumbnail_path = ".temp/thumbnail.jpg"
    # first_image_path = "./downloaded_images/image_0.jpg"
    # create_thumbnail(first_image_path, video_title, thumbnail_path)
    # print("Miniatura generada.")

    # Paso 8: Subir el video a YouTube con el título de la idea
    youtube_uploader.upload_video_to_youtube(
        video_file_path=temp_video_path,
        title=video_title,  # El título del video es la idea generada
        description=f"Un video sobre: {video_title}",
        category_id='22',  # Define la categoría apropiada
        keywords=['keyword1', 'keyword2'],  # Define las palabras clave apropiadas
        privacy_status='private',  # Puede ser 'public', 'private' o 'unlisted'
        #thumbnail_path=thumbnail_path

    )
    print("Video subido a YouTube con éxito.")

if __name__ == "__main__":
    niche = "Realistic horror stories"  # Define tu nicho
    main(niche)
