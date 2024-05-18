import streamlit as st
import requests
import re

api_key = st.secrets['FOODDATA_API_KEY']

def search_food(query):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": api_key,
        "query": query,
        "limit": 10,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["foods"][:10]
    else:
        return None

def extract_product_info(data: dict):
    keys = ["description", "brandedFoodCategory", "brandName", "brandOwner"]
    nutrient_nums = ['203','204','205','208','269','291','303','307','601']
    product_info = {key: data.get(key, "N/A").title() for key in keys}
    
    product_info['fdcId'] = data["fdcId"]

    ingredients_list = data.get('ingredients', 'N/A')
    ingredients_list = re.sub(r"\([^)]+\)|[*]", "", ingredients_list)
    ingredients_list = ingredients_list.replace("MADE OF:", "")
    ingredients_list = ingredients_list.lower()

    product_info['ingredients'] = ingredients_list

    if 'labelNutrients' in data:
        product_info['labelNutrients'] = {macro: value_dict['value'] for macro, value_dict in data['labelNutrients'].items()}
    else:
        product_info['foodNutrients'] = {foodNutrient['nutrient']['name'].lower(): foodNutrient['amount'] for foodNutrient in data['foodNutrients'] if foodNutrient['nutrient']['number'] in nutrient_nums}

    return product_info

def get_nutritional_info(food_id):
    url = f"https://api.nal.usda.gov/fdc/v1/food/{food_id}"
    params = {
        'api_key': api_key,
        'format': 'full',
        'nutrients': '203,204,205,208,269,291,303,307,601'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        print(data)
        if 'description' in data and 'foodNutrients' in data:
            return extract_product_info(data)
        else:
            return None
    except Exception as e:
        print(e)
        return None

def get_nutritional_info_barcode(barcode):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={barcode}&api_key={api_key}"
        
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['foods']:
            food_id = data['foods'][0]['fdcId']
            return get_nutritional_info(food_id)
        else:
            return None
    except Exception as e:
        return None