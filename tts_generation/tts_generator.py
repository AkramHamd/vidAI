import subprocess
import uuid
import os
from pydub import AudioSegment

def get_audio_duration(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return len(audio) / 1000.0  # Duración en segundos

def generate_voiceover(script, output_dir="./.temp", voice_name="en-US-ChristopherNeural"):

    voiceover_filename = f"voiceover_{uuid.uuid4()}.mp3"
    output_path = f"{output_dir}/{voiceover_filename}"
    try:
        # Ejecuta edge-tts con el comando especificado, incluyendo la voz seleccionada
        subprocess.run(["edge-tts", "--text", script, "--voice", voice_name, "--write-media", output_path], check=True)

        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar edgeTTS: {e}")
        return None


   
   
   
if __name__ == "__main__":
    # Define el guion de voz en off
    script = """
    Welcome to the world of portrait photography, where every shot is a unique opportunity to capture the essence and personality of your subject. It's a skill that requires both technical knowledge and creative vision, and with practice and dedication, you can master it.
    Are you tired of taking lackluster portraits that fail to truly capture the beauty and emotion of your subjects? Are you looking to elevate your photography game to the next level? Then this video is for you.
    We will guide you through the fundamentals of portrait photography, from choosing the right camera and lenses, to understanding lighting techniques and posing your subject. We'll teach you how to use composition and framing to tell a powerful story through your images.
    But mastering portrait photography is more than just technical skills. It's about connecting with your subject and creating a comfortable and collaborative environment. We'll show you how to build rapport with your subject and bring out their unique personality and authenticity in every shot.   
    Whether you're a beginner or an experienced photographer, this video is packed with tips and tricks that will take your portrait game to the next level. Let us help you unlock your full potential as a portrait photographer and capture the beauty of every moment. Stay tuned and get ready to master the art of portrait photography!
    """

    # Genera el voz en off
    output_audio_path = "./.temp/voiceover.mp3"
    

    generate_voiceover(script, output_audio_path )

    if output_audio_path:
        print(f"Voz en off generada correctamente: {output_audio_path}")
        # Obtén la duración del audio generado
        duration = get_audio_duration(output_audio_path)
        print(f"Duración del audio: {duration} segundos")
    else:
        print("No se pudo generar el voz en off.")