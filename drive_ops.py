from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st

def get_files(service):
    try:
        results = service.files().list(
            pageSize=1000,
            fields="nextPageToken, files(id, name)"
        ).execute()
        return results.get('files', [])
    except HttpError as error:
        st.error(f'An error occurred: {error}')
        return None
    
def create_folder(service, folder_name, parent_id='root'):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    st.write(f"Debug: Created folder '{folder_name}' with ID: {folder.get('id')}")
    return folder.get('id')    

def move_file(service, file_id, folder_id):
    try:
        
        file = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents', []))
        
        
        file = service.files().update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        
        return True
    except Exception as e:
        st.write(f"Error moving file {file_id}: {str(e)}")
        return False
