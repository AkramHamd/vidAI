from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import os
import pickle


def get_authenticated_service():
    credentials = None
    pickle_file = 'token.pickle'
    
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except Exception as e:
                print(f"Error al refrescar el token: {e}. Iniciando nuevo flujo de autenticación.")
                credentials = None  # Forzar nuevo flujo de autenticación
                
        if not credentials:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                scopes=['https://www.googleapis.com/auth/youtube.upload'])
            credentials = flow.run_local_server(port=8080)
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

def upload_video_to_youtube(video_file_path, title, description, category_id, keywords, privacy_status, thumbnail_file_path=None):
    youtube = get_authenticated_service()

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': keywords,  # Use the keywords list directly
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

    # Subir la miniatura, if provided
    if thumbnail_file_path:
        upload_thumbnail(youtube, video_id, thumbnail_file_path)


output_video_path="./videos/Exploring_a_Haunted_House_Thrilling_Scares_&_Chilling_Secrets_6078239f-0bfb-401f-9b67-f4a3ba0811ed.mp4"
video_title="TEST"

# # Ejemplo de uso
upload_video_to_youtube(
    video_file_path=output_video_path,
    title=video_title,
    description=f"A video about: {video_title}",
    category_id='22',
    keywords=['horror', 'scary stories', 'ghost tales', 'haunted places', 'supernatural', 'creepy tales', 'urban legends', 'chilling narrations', 'spooky content', 'paranormal activity', 'dark tales', 'eerie experiences', 'frightful stories', 'spine-tingling adventures', 'macabre mysteries', 'fear-inducing tales', 'horror narration', 'bone-chilling stories', 'terrifying encounters', 'mysterious phenomena'],  # Define las palabras clave apropiadas
    privacy_status='public',
    #thumbnail_file_path=thumbnail_path  # Assuming thumbnail_path is defined elsewhere
    )
print("Video subido a YouTube con éxito.")


