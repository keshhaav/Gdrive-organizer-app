import streamlit as st
from groq import Groq
import json

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ai_categories(file_names):
    try:
        file_list = "\n".join(file_names)
        prompt = f"""Analyze the following list of file names and create up to 15 unique, specific, and highly relevant category names that would logically group these files. 
        Only create categories that are actually needed based on the file names provided.
        Consider the content, purpose, and context of the files, not just their file types.
        Aim for categories that reflect the actual subject matter or projects these files might belong to.
        Avoid generic categories like 'Documents', 'Images', or 'Other'.
        Ensure the categories are diverse and cover the range of topics present in the file names.
        Respond with a JSON object where the keys are the folder names and the values are lists of file names that are relevant to that folder name and could go into that folder.

        {file_list}"""

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert file organizer with a knack for identifying unique and meaningful categories."},
                {"role": "user", "content": prompt}
            ]
        )

        # Parse the JSON from the response
        response_text = response.choices[0].message.content.strip()
        
        # Extract JSON content if it's wrapped in markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        categories_dict = json.loads(response_text)
        return categories_dict

    except Exception as e:
        st.error(f"Error in get_ai_categories: {e}")
        return {"Miscellaneous": file_names}

def categorize_files(file_names):
    return get_ai_categories(file_names)

def clean_category_name(category):
    return category.split('. ', 1)[-1].rstrip('.)').strip()
