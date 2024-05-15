import streamlit as st
import requests
import re

api_key = st.secrets['FOODDATA_API_KEY']

def extract_product_info(data: dict):
    keys = ["description", "brandedFoodCategory", "brandName", "fdcId"]
    product_info = {key: data.get(key, "N/A") for key in keys}
    # Removes MADE OF: in the beginning, and text in parenthesis
    product_info['ingredients'] = re.sub(r"\([^)]+\)|[*]", "", data.get('ingredients', 'N/A')).lower()

    product_info['labelNutrients'] = {macro: value_dict['value'] for macro, value_dict in data.get('labelNutrients', {'none': {'value': 'none'}}).items()}
    
    return product_info

def get_nutritional_info(food_id):
    url = f"https://api.nal.usda.gov/fdc/v1/food/{food_id}?api_key={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'description' in data and 'foodNutrients' in data:
            return extract_product_info(data)
        else:
            return "Nutritional information not available"
    except Exception as e:
        return f"Error: {str(e)}"