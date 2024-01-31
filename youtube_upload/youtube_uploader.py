# import os
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from google.oauth2.credentials import Credentials

# def upload_video_to_youtube(video_file_path, title, description, category_id, keywords, privacy_status):
#     # Cargar credenciales y crear un servicio de YouTube
#     credentials = Credentials.from_authorized_user_file('credentials.json')
#     youtube = build('youtube', 'v3', credentials=credentials)

#     # Configurar los detalles del video
#     body = {
#         'snippet': {
#             'title': title,
#             'description': description,
#             'tags': keywords,
#             'categoryId': category_id
#         },
#         'status': {
#             'privacyStatus': privacy_status
#         }
#     }

#     # Subir el video
#     media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True, mimetype='video/*')
#     request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
#     response = request.execute()

#     print(f"Video uploaded. Video ID: {response['id']}")

# # Ejemplo de uso
# upload_video_to_youtube(
#     video_file_path='.temp/output.mp4',
#     title='Test',
#     description='Descripción del Video',
#     category_id='22',  # Categoría en YouTube
#     keywords=['keyword1', 'keyword2'],
#     privacy_status='private'  # Puede ser 'public', 'private' o 'unlisted'
# )
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
import os

load_dotenv

# Reemplaza con tu propio ID de cliente y secreto del cliente
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Flujo de autenticación OAuth
flow = InstalledAppFlow.from_client_config({
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
        "scopes": ["https://www.googleapis.com/auth/youtube.upload"]
    }
}, scopes=["https://www.googleapis.com/auth/youtube.upload"])

# Ejecutar el flujo de autenticación local
flow.run_local_server(port=8080)

print("Refresh Token:", flow.credentials.refresh_token)
