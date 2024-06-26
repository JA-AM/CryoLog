import cv2
import streamlit as st
from pyzbar import pyzbar
import requests
import os

api_key = st.secrets["FOODDATA_API_KEY"]  # Replace this with your API key from FoodData Central

def extract_product_info(data):
    description = data['description']
    ingredients = data.get('ingredients', 'Not available')
    macros = data.get('labelNutrients', {})
    return description, ingredients, macros

def get_product_nutrition(barcode):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={barcode}&api_key={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['foods']:
            food_id = data['foods'][0]['fdcId']
            return get_nutritional_info(food_id)
        else:
            return "Product not found"
    except Exception as e:
        return f"Error: {str(e)}"

def get_nutritional_info(food_id):
    url = f"https://api.nal.usda.gov/fdc/v1/food/{food_id}"
    params = {
        'api_key': api_key,
        'format': 'abridged',
        'nutrients': '203,204,205,208,269,291,303,307,601'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        print(data)
        
        if 'description' in data and 'foodNutrients' in data:
            for foodNutrient in data['foodNutrients']:
                print(foodNutrient)
                #print(foodNutrient['nutrient']['name'])
                #print(foodNutrient['nutrient']['unitName'])
                #print(foodNutrient['amount'])

            description, ingredients, macros = extract_product_info(data)
            return f"Description: {description}\nIngredients: {ingredients}\nMacros: {macros}"
        else:
            return "Nutritional information not available"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    barcode = "0022000159335"  # Replace this with your actual barcode number
    product_nutrition = get_nutritional_info("2341867")
    #print(product_nutrition)