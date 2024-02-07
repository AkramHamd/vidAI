from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
import numpy as np
from PIL import Image
import uuid
import os
#from subtitle_generator import add_subtitles
from subtitles.subtitle_generator import add_subtitles



def camera_shake(clip, initial_zoom=1.05, max_amplitude=5, frequency=0.5):
    """ Aplica un efecto de 'camera shake' suave al clip. """

    def fl(gf, t):
        frame = gf(t)

        # Aplicar un zoom inicial suave
        frame_zoomed = np.array(Image.fromarray(frame).resize([int(dim * initial_zoom) for dim in frame.shape[1::-1]], Image.LANCZOS))

        # Calcular un desplazamiento suave y menos pronunciado
        amplitude = max_amplitude * np.sin(frequency * t)
        dx = int(amplitude * np.cos(2 * np.pi * frequency * t))
        dy = int(amplitude * np.sin(2 * np.pi * frequency * t))

        # Desplazar el frame de forma suave
        frame_shaken = np.roll(np.roll(frame_zoomed, dy, axis=0), dx, axis=1)

        return frame_shaken

    return clip.fl(fl)


def add_particle_overlay(clip, overlay_path, opacidad=0.5):
    """ Añade un overlay de partículas al clip. """
    overlay_clip = VideoFileClip(overlay_path).loop(duration=clip.duration)
    overlay_clip = overlay_clip.set_opacity(opacidad)
    new_clip = CompositeVideoClip([clip, overlay_clip])
    print(f"Tamaño del clip después de add_particle_overlay: {new_clip.size}")
    return new_clip


def resize_images(image_paths, output_dir, target_size):
    resized_image_paths = []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for image_path in image_paths:
        with Image.open(image_path) as img:
            # Asegúrate de que las dimensiones sean múltiplos de 2
            new_size = tuple(2 * (dim // 2) for dim in target_size)
            img = img.resize(new_size, Image.LANCZOS)
            output_path = os.path.join(output_dir, os.path.basename(image_path))
            img.save(output_path)
            resized_image_paths.append(output_path)

    print(f"Tamaño objetivo de redimensionamiento: {new_size}")
    print(f"Rutas de imágenes redimensionadas: {resized_image_paths[:5]}")
    return resized_image_paths




def create_video(image_paths, audio_path, particle_overlay, output_path="./videos/final_video.mp4"):
    # Redimensionar imágenes
    #resized_image_paths = resize_images(image_paths, './temp_resized_images/', (1920, 1080))
    resized_image_paths = "./downloaded_images/"

    # Calcular duración para cada imagen basado en la duración del audio
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    image_duration = audio_duration / len(resized_image_paths)

    # Crear clips para cada imagen y concatenarlos
    clips = [ImageClip(img_path, duration=image_duration) for img_path in resized_image_paths]
    final_clip = concatenate_videoclips(clips, method="compose")

    # Configurar audio y aplicar efectos al video
    final_clip = final_clip.set_audio(audio).set_fps(24)
    final_clip = camera_shake(final_clip)

    # Guardar el video temporal sin subtítulos
    unique_id = str(uuid.uuid4())
    temp_video_path = f"./.temp/temp_video_{unique_id}.mp4"
    
    final_clip.write_videofile(temp_video_path, codec="libx264", threads=2)

    # Añadir subtítulos al video temporal y guardar el video final
    final_video_with_subtitles = add_subtitles(
        videofilename=temp_video_path, 
        outputfilename=output_path
    )


# # Configuraciones y llamada a la función create_video
# numero_de_imagenes = 20
# directorio_imagenes = './temp_resized_images/'
# image_paths = [f'{directorio_imagenes}image_{i}.jpg' for i in range(numero_de_imagenes)]
# audio_path = './videos/voiceover.mp3'
# particle_overlay = './recursos/particle_overlay.mp4'

# create_video(image_paths, audio_path, particle_overlay)