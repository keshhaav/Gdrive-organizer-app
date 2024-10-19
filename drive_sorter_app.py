import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from authenticate import authenticate
from drive_operations import get_files, move_file, create_folder
from file_categorization import categorize_files, clean_category_name

if 'should_stop' not in st.session_state:
    st.session_state.should_stop = False
categorize_files()
clean_category_name()
get_files()
move_file()
create_folder()
def main():
    st.title("Google Drive File Categorizer and Organizer")
    st.sidebar.title("Authentication")
    
    creds = authenticate()
    
    if not creds:
        st.write("Waiting for authentication...")
        return

    st.sidebar.success("Authentication successful!")
    
    if st.button('Stop', key='stop_button', help='Click to stop the app', type='primary'):
        st.session_state.should_stop = True
        st.error('Stopping the app...')
        st.stop()

    try:
        service = build('drive', 'v3', credentials=creds)
        
        with st.spinner("Fetching files from Google Drive..."):
            files = get_files(service)

        if files:
            st.write(f"Found {len(files)} files in your Google Drive.")
            file_names = [file['name'] for file in files]
            
            with st.spinner("Generating categories..."):
                categories_dict = categorize_files(file_names)
            
            st.write("Generated categories:")
            st.json(categories_dict)
            
            if st.button("Create folders and organize files"):
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
                        folder_id = create_folder(service, clean_category)
                        
                        for file_name in category_files:
                            if st.session_state.should_stop:
                                st.error('Operation stopped by user.')
                                st.stop()
                            matching_files = [file for file in files if file['name'] == file_name]
                            for file in matching_files:
                                if move_file(service, file['id'], folder_id):
                                    files_processed += 1
                                    progress_bar.progress(files_processed / total_files)
                                else:
                                    st.warning(f"Failed to move file '{file['name']}'")
                        
                        st.success(f"Created folder '{clean_category}' and moved {len(category_files)} files into it.")
                    except HttpError as error:
                        st.error(f"Error processing category '{clean_category}': {error}")
                        continue
                
                st.success(f"File organization complete! Created {len(categories_dict)} folders.")
        else:
            st.warning("No files found in your Google Drive.")
    except HttpError as error:
        st.error(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
