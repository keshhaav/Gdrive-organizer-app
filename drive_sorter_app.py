import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from authenticate import authenticate
from drive_ops import get_files,move_file, create_folder, get_uncategorized_files
from categorization import get_ai_categories, categorize_files, clean_category_name

if 'should_stop' not in st.session_state:
    st.session_state.should_stop = False

def main():
    st.title("Google Drive File Categorizer and Organizer")
    st.sidebar.title("Authentication")
    creds = authenticate()
    
    if not creds:
        return  
        
    st.sidebar.success("Authentication successful!")
    
    if st.button('Stop', key='stop_button', help='Click to stop the app', type='primary'):
        st.session_state.should_stop = True
        st.error('Stopping the app...')
        st.stop()

    try:
        service = build('drive', 'v3', credentials=creds)
        
        
        files = []
        page_token = None
        with st.spinner("Fetching files from Google Drive..."):
            while True:
                if st.session_state.should_stop:
                    st.error('Operation stopped by user.')
                    st.stop()
                results = get_files(service).execute()
                files.extend(results.get('files', []))
                page_token = results.get('nextPageToken')
                if not page_token:
                    break

        if files:
            file_names = [file['name'] for file in files]
            st.write(f"Found {len(file_names)} files in your Google Drive.")
            
            with st.spinner("Generating categories..."):
                if st.session_state.should_stop:
                    st.error('Operation stopped by user.')
                    st.stop()
                categories_dict = categorize_files(file_names)
            
            
            st.write("Generated categories:")
            category_summary = {k: len(v) for k, v in categories_dict.items()}
            st.json(category_summary)
            
            
            with st.expander("View detailed categorization"):
                st.json(categories_dict)
            
            if st.button("Create folders and organize files",key="organize_files_button" ):
                progress_bar = st.progress(0)
                total_files = len(files)
                files_processed = 0
            
                for category, category_files in categories_dict.items():
                    if st.session_state.should_stop:
                        st.error('Operation stopped by user.')
                        st.stop()
                    clean_category = clean_category_name(category)
                    st.write(f"Processing category: {clean_category}")
                    
                    try: 
                        folder_id= create_folder(service, clean_category)
                        
                        for file_name in category_files:
                            if st.session_state.should_stop:
                                st.error('Operation stopped by user.')
                                st.stop()
                            matching_files = [file for file in files if file['name'] == file_name]
                            for file in matching_files:
                                try:
                                    if move_file(service, file['id'], folder_id):
                                        files_processed += 1
                                        progress_bar.progress(files_processed / total_files)
                                    else:
                                        st.warning(f"Failed to move file '{file['name']}'")
                                except HttpError as file_error:
                                    st.warning(f"Error moving file '{file['name']}': {file_error}")
                                    continue
                        
                        st.success(f"Created folder '{clean_category}' and moved {len(category_files)} files into it.")
                    except HttpError as error:
                        st.error(f"Error processing category '{clean_category}': {error}")
                        continue
                
                st.success(f"File organization complete! Created {len(categories_dict)} folders.")
        else:
            st.warning("No files found in your Google Drive.")
    except HttpError as error:
        st.error(f"An error occurred: {error}")

    if st.button("Find & Categorize Missed Files",key="uncategorized_files_button"):
        files = []
        
        results = get_uncategorized_files(service).execute()
        files.extend(results.get('files', []))
        page_token = results.get('nextPageToken')
        

        if files: 
                file_names = [file['name'] for file in files]
                st.write(f"Found {len(file_names)} files in your Google Drive.")
                st.spinner("Generating categories...")
                if st.session_state.should_stop:
                    st.error('Operation stopped by user.')
                    st.stop()
                uncategorized_dict = categorize_files(file_names)
                st.expander("View detailed categorization")
                st.json(uncategorized_dict)
                processed_files = 0
                progress_bar = st.progress(0)
                total_files = len(files)
                for category, category_files in uncategorized_dict.items():
                    clean_category = clean_category_name(category)
                    st.write(f"Processing category: {clean_category}")
                    folder_id= create_folder(service, clean_category)
                    for file_name in category_files:
                            matching_files = [file for file in files if file['name'] == file_name]
                            for file in matching_files:
                                try:
                                    if move_file(service, file['id'], folder_id):

                                        processed_files += 1
                                        progress_bar.progress(processed_files / total_files)
                                    else:
                                        st.warning(f"Failed to move file '{file['name']}'")
                                except HttpError as file_error:
                                    st.warning(f"Error moving file '{file['name']}': {file_error}")
                                    continue
                        
                    st.success(f"Created folder '{clean_category}' and moved {len(category_files)} files into it.")
                
                st.success(f"Scuccessfully categorized all  uncategorized files! Created {len(categories_dict)} folders.")
        else: 
            st.write ("No Uncategeroized files found in your Google Drive ")




if __name__ == "__main__":
    authenticate()
    main()

