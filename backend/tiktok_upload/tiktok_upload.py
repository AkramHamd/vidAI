# from tiktok_uploader.upload import upload_videos
# from tiktok_uploader.auth import AuthBackend
# import os
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options

# def upload_clip_tiktok() -> None:
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')  # Opcional, para ejecutar Chrome en modo headless
#     chrome_options.add_argument('--disable-gpu')  # Opcional, recomendado para modo headless
#     chrome_options.add_argument('--no-sandbox')  # Opcional, recomendado para ejecutar en contenedores Docker
#     service = ChromeService(ChromeDriverManager().install())
#     driver = webdriver.Chrome(options=chrome_options, service=service)
#     auth = AuthBackend(cookies="./tiktok_matrix_cookies.txt")  # Asegúrate de que el archivo de cookies exista y sea válido

#     videos = []
#     for video_clip in os.listdir("./.temp/"):  # Asegúrate de que esta es la ruta correcta a tus videos
#         if video_clip.endswith(".mp4"):  # Filtra solo archivos .mp4
#             new_video = {}
#             new_video["path"] = f"./.temp/{video_clip}"
#             # Aquí puedes personalizar la descripción de cada video
#             new_video["description"] = f"{video_clip} #yourhashtags #fyp #foryoupage"
#             videos.append(new_video)

#     upload_videos(videos=videos, 
#                   auth=auth, 
#                   browser="chrome", 
#                   browser_agent=driver)
            
# upload_clip_tiktok()
