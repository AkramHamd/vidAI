import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials



def upload_video_to_youtube(video_file_path, title, description, category_id, keywords, privacy_status):
    # Cargar credenciales y crear un servicio de YouTube
    credentials = Credentials.from_authorized_user_file('credentials.json')
    youtube = build('youtube', 'v3', credentials=credentials)

    # Configurar los detalles del video
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': keywords,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    # Subir el video
    media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True, mimetype='video/*')
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    response = request.execute()

    print(f"Video uploaded. Video ID: {response['id']}")

# Ejemplo de uso
upload_video_to_youtube(
    video_file_path='.temp/final_video_sub.mp4',
    title='Titulo del Video',
    description='Descripción del Video',
    category_id='22',  # Categoría en YouTube
    keywords=['keyword1', 'keyword2'],
    privacy_status='public'  # Puede ser 'public', 'private' o 'unlisted'
)
