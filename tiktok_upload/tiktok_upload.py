import os
from dotenv import load_dotenv
from tiktok_uploader.upload import upload_video, upload_videos
from tiktok_uploader.auth import AuthBackend
# Asumiendo que ya has importado todos los otros módulos necesarios

# Importa tu módulo de TikTok
#import tiktok_upload.tiktok_uploader as tiktok_uploader
# Asume que esta es la ruta del video creado y una descripción para TikTok
output_video_path = "./.temp/temp_video_3b96792d-c2e8-4b47-9722-271fa567cf79.mp4"
video_title = "Horror"
video_path_tiktok = output_video_path
video_description_tiktok = f"A video about: {video_title}"

# Asume que tienes una función `upload_video_to_tiktok` adecuadamente configurada
try:
    # single video
    upload_video('./.temp/temp_video_3b96792d-c2e8-4b47-9722-271fa567cf79.mp4',
                description='this is my description',
                cookies='./tiktok_matrix_cookies.txt', browser='firefox', headless=True)


    #auth = AuthBackend(cookies='./tiktok_matrix_cookies.txt')    
    print("Video subido a TikTok con éxito.")
    
except Exception as e:
    print(f"Error al subir video a TikTok: {e}")

    