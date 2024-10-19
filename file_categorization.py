import streamlit as st
from fuzzywuzzy import fuzz
from grow import Groq

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])


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



