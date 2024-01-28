from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
import numpy as np
import cv2
from PIL import Image
import os
import random



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




def create_video(image_paths, audio_path, particle_overlay, output_path="final_video.mp4"):
    resized_image_paths = resize_images(image_paths, './temp_resized_images/', (1920, 1080))

    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration  # Obtener la duración del audio

    # Calcular la duración de cada imagen
    image_duration = audio_duration / len(resized_image_paths)

    # Crear un clip para cada imagen con la duración calculada y luego concatenarlos
    clips = [ImageClip(img_path, duration=image_duration) for img_path in resized_image_paths]
    final_clip = concatenate_videoclips(clips, method="compose")

    final_clip = final_clip.set_audio(audio)
    final_clip.fps = 24  # Establecer fps para el clip final

    final_clip = camera_shake(final_clip)
    #final_clip = add_particle_overlay(final_clip, particle_overlay)  # Descomentar si se desea usar

    final_clip.write_videofile(output_path, codec="libx264")

# ... Resto de tu código ...

# Configuraciones
numero_de_imagenes = 20  # Ajusta este número al total de imágenes que tienes
directorio_imagenes = './temp_resized_images/'  # Asegúrate de que la ruta sea correcta

# Generar rutas de imagen
image_paths = [f'{directorio_imagenes}image_{i}.jpg' for i in range(numero_de_imagenes)]

# Rutas para el audio y el overlay de partículas
audio_path = './videos/voiceover.mp3'
particle_overlay = './recursos/particle_overlay.mp4'

# Llamar a la función con las rutas generadas
create_video(image_paths, audio_path, particle_overlay)
