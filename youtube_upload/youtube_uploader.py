from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import os
import pickle




def get_authenticated_service():
    credentials = None
    # Ruta al archivo de credenciales almacenadas
    pickle_file = 'token.pickle'
    
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                scopes=['https://www.googleapis.com/auth/youtube.upload'])
            credentials = flow.run_local_server(port=8080)

            
            # Guardar las credenciales para la próxima ejecución
            with open(pickle_file, 'wb') as token:
                pickle.dump(credentials, token)
                
    return build('youtube', 'v3', credentials=credentials)


def upload_thumbnail(youtube, video_id, thumbnail_file_path):
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_file_path, mimetype='image/jpeg')
    )
    response = request.execute()

    print(f"Thumbnail uploaded for video ID: {video_id}")

def upload_video_to_youtube(video_file_path, thumbnail_file_path, title, description, category_id, keywords, privacy_status):
    youtube = get_authenticated_service()

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
    media_video = MediaFileUpload(video_file_path, chunksize=-1, resumable=True, mimetype='video/*')
    request_video = youtube.videos().insert(part='snippet,status', body=body, media_body=media_video)
    response_video = request_video.execute()

    video_id = response_video['id']
    print(f"Video uploaded. Video ID: {video_id}")

    # Subir la miniatura
    #if thumbnail_file_path:
     #   upload_thumbnail(youtube, video_id, thumbnail_file_path)

# # Ejemplo de uso
# upload_video_to_youtube(
#     video_file_path='.temp/output.mp4',
#     thumbnail_file_path='.temp/thumbnail.jpg',
#     title='Test',
#     description='Descripción del Video',
#     category_id='22',  # Categoría en YouTube
#     keywords=['keyword1', 'keyword2'],
#     privacy_status='private'  # Puede ser 'public', 'private' o 'unlisted'
# )


