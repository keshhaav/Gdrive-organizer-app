import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
from googleapiclient.errors import HttpError
from collections import defaultdict
import json
from groq import Groq
from fuzzywuzzy import fuzz
import groq
import re
from authenticate import authenticate

if 'should_stop' not in st.session_state:
    st.session_state.should_stop = False

groq_client = groq.Groq(api_key=st.secrets["GROQ_API_KEY"])

# Set up your Google OAuth 2.0 credentials
CLIENT_CONFIG = st.secrets["google_oauth"]

SCOPES = ['https://www.googleapis.com/auth/drive']

authenticate()
    
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

def assign_files_to_categories(file_names, categories):
    categorized_files = {category: [] for category in categories}
    
    for file_name in file_names:
        best_category = None
        highest_similarity = 0
        
        for category in categories:
            similarity = calculate_similarity(file_name, category)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_category = category
        
        if best_category:
            categorized_files[best_category].append(file_name)
        else:
            # If no suitable category is found, assign to "Miscellaneous"
            if "Miscellaneous" not in categorized_files:
                categorized_files["Miscellaneous"] = []
            categorized_files["Miscellaneous"].append(file_name)
    
    return categorized_files

def calculate_similarity(file_name, category):
    # This is a simple implementation. You might want to use more sophisticated NLP techniques.
    file_words = set(file_name.lower().split())
    category_words = set(category.lower().split())
    return len(file_words.intersection(category_words)) / len(file_words.union(category_words))

def create_folder(service, folder_name, parent_id='root'):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    st.write(f"Debug: Created folder '{folder_name}' with ID: {folder.get('id')}")
    return folder.get('id')

def get_ai_categories(file_names, num_categories=15):
    try:
        file_list = "\n".join(file_names)  # Use all file names
        prompt = f"""Analyze the following list of file names and create up to {num_categories} unique, specific, and highly relevant category names that would logically group these files. 
        Only create categories that are actually needed based on the file names provided.
        Consider the content, purpose, and context of the files, not just their file types. 
        Aim for categories that reflect the actual subject matter or projects these files might belong to.
        Avoid generic categories like 'Documents', 'Images', or 'Other'.
        Ensure the categories are diverse and cover the range of topics present in the file names.
        Only provide the category names, separated by commas:

        {file_list}"""

        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are an expert file organizer with a knack for identifying unique and meaningful categories."},
                {"role": "user", "content": prompt}
            ]
        )

        categories = response.choices[0].message.content.strip().split(',')
        categories = [cat.strip() for cat in categories if cat.strip()]
        
        return categories  # Return all generated categories, may be less than num_categories

    except Exception as e:
        print(f"Error in get_ai_categories: {e}")
        return ["Miscellaneous"]

def categorize_files(file_names):
    categories = get_ai_categories(file_names, num_categories=15)
    categorized_files = {category: [] for category in categories}
    
    for file_name in file_names:
        best_match = max(categories, key=lambda x: fuzz.token_set_ratio(file_name.lower(), x.lower()))
        categorized_files[best_match].append(file_name)
    
    # Sort categories by number of files, descending
    sorted_categories = sorted(categorized_files.items(), key=lambda x: len(x[1]), reverse=True)
    
    # Keep only the top 15 categories
    top_categories = dict(sorted_categories[:15])
    
    # Add any uncategorized files to the smallest category
    if len(top_categories) < 15:
        uncategorized = [file for file in file_names if not any(file in files for files in top_categories.values())]
        if uncategorized:
            smallest_category = min(top_categories, key=lambda x: len(top_categories[x]))
            top_categories[smallest_category].extend(uncategorized)
    
    return top_categories

def clean_category_name(category):
    # Remove numbers and trailing punctuation, then strip whitespace
    return category.split('. ', 1)[-1].rstrip('.)').strip()


def categorize_files(file_names):
    categories = get_ai_categories(file_names)
    categorized_files = {}
    
    for file_name in file_names:
        best_match = max(categories, key=lambda x: fuzz.token_set_ratio(file_name.lower(), x.lower()))
        if best_match not in categorized_files:
            categorized_files[best_match] = []
        categorized_files[best_match].append(file_name)
    
    # Remove any categories that ended up empty
    categorized_files = {k: v for k, v in categorized_files.items() if v}
    
    return categorized_files

def move_file(service, file_id, folder_id):
    try:
        # Retrieve the file's current parents
        file = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents', []))
        
        # Move the file to the new folder
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

def main():
    st.title("Google Drive File Categorizer and Organizer")

    creds = authenticate()
    
    if not creds:
        return  # Exit the function if not authenticated

    # Add the stop button after authentication
    if st.button('Stop', key='stop_button', help='Click to stop the app', type='primary'):
        st.session_state.should_stop = True
        st.error('Stopping the app...')
        st.stop()

    try:
        service = build('drive', 'v3', credentials=creds)

        # Get list of files
        results = service.files().list(
            pageSize=1000, fields="nextPageToken, files(id, name, mimeType, parents)").execute()
        items = results.get('files', [])

        if not items:
            st.write('No files found.')
        else:
            st.write('Files:')
            for item in items:
                st.write(u'{0} ({1})'.format(item['name'], item['id']))

        # File categorization
        st.header("File Categorization")
        categorize = st.button("Categorize Files")

        if categorize:
            categorized_files = categorize_files(items)
            st.write("Files categorized:")
            for category, files in categorized_files.items():
                st.write(f"{category}: {len(files)} files")

        # Folder creation
        st.header("Folder Creation")
        create_folders = st.button("Create Folders")

        if create_folders:
            folder_ids = create_category_folders(service)
            st.write("Folders created:")
            for category, folder_id in folder_ids.items():
                st.write(f"{category}: {folder_id}")

        # File moving
        st.header("Move Files")
        move_files_button = st.button("Move Files to Categories")

        if move_files_button:
            categorized_files = categorize_files(items)
            folder_ids = create_category_folders(service)
            move_files_to_folders(service, categorized_files, folder_ids)
            st.write("Files moved to their respective category folders.")

    except HttpError as error:
        st.error(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
