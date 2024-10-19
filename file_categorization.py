import streamlit as st
from groq import Groq
from fuzzywuzzy import fuzz

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])




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


def clean_category_name(category):
    # Remove numbers and trailing punctuation, then strip whitespace
    return category.split('. ', 1)[-1].rstrip('.)').strip()
