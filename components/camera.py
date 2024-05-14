import cv2
from pyzbar import pyzbar
import streamlit as st
import os
import requests

api_key = st.secrets['FOODDATA_API_KEY']

# Set to keep track of detected barcodes
detected_barcodes = set()

# Gets product info from JSON data
def extract_product_info(data: dict):
    description = data['description']
    ingredients = data.get('ingredients', 'Not available')
    macros = data.get('labelNutrients', {})
    return description, ingredients, macros

# Makes API Call request to USDA API, finds food ID
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

# Makes API Call request with FoodID to extract info
def get_nutritional_info(food_id):
    url = f"https://api.nal.usda.gov/fdc/v1/food/{food_id}?api_key={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'description' in data and 'foodNutrients' in data:
            description, ingredients, macros = extract_product_info(data)
            return f"Description: {description}\nIngredients: {ingredients}\nMacros: {macros}"
        else:
            return "Nutritional information not available"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to decode barcode and highlight it in the frame
def decode_barcode(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect barcodes in the frame
    barcodes = pyzbar.decode(gray)

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        barcode_data = barcode.data.decode("utf-8")

        cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        if barcode_data not in detected_barcodes:
            # Get product information based on the barcode
            product_info = get_product_nutrition(barcode_data)
            
            st.write(product_info)

            #TODO Create Add to List Function, Learn More About Ingredients Function
          
            detected_barcodes.add(barcode_data)
    
    return frame

def camera():
    st.title("Barcode Scanner")

    # Buttons to start and stop camera feed
    start_button = st.button("Start Camera Feed")
    stop_button = st.button("Stop Camera Feed")

    if start_button:
        # Create a VideoCapture object
        cap = cv2.VideoCapture(0)

        # Display live video feed
        video_placeholder = st.empty()

        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()

            # If the frame was not captured successfully, break the loop
            if not ret:
                break

            # Call the function to decode barcodes
            frame = decode_barcode(frame)

            # Display the resulting frame
            video_placeholder.image(frame, channels="BGR")

            # Check if the stop button is clicked
            if stop_button:
                break

        # Release the capture
        cap.release()

if __name__ == "__main__":
    camera()