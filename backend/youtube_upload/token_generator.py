from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
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
            credentials = flow.run_console()
            
            # Guardar las credenciales para la próxima ejecución
            with open(pickle_file, 'wb') as token:
                pickle.dump(credentials, token)
                
    return build('youtube', 'v3', credentials=credentials)
