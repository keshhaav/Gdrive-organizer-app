from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st

def get_files(service):
    page_token = None
    results = service.files().list(
                q="'root' in parents and trashed=false",
                pageSize=1000,
                fields="nextPageToken, files(id, name, parents)",
                pageToken=page_token
                )
    return results

def get_uncategorized_files(service):
    files = []
    page_token = None
    
    with st.spinner("Checking for uncategorized files in Google Drive..."):
        query = "'root' in parents and mimeType != 'application/vnd.google-apps.folder'"              
        try:
                results = service.files().list(
                    q=query,
                    spaces='drive',
                    fields='nextPageToken, files(id, name, mimeType)',
                    pageToken=page_token
                )
                
        except HttpError as error:
            st.error(f"Error retrieving files: {error}")
           
    
    return results
    
def create_folder(service,clean_category):   
    folder_metadata = {
            'name': clean_category,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': ['root']
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')
    return folder_id  

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
