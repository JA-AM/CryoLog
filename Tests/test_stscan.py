import cv2
from pyzbar import pyzbar
import numpy as np
import streamlit as st
import os
import requests

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("FOODDATA_API_KEY")  # Replace this with your API key from FoodData Central

# Set to keep track of detected barcodes
detected_barcodes = set()

def extract_product_info(data: dict):
    description = data['description']
    ingredients = data.get('ingredients', 'Not available')
    macros = data.get('labelNutrients', {})
    return description, ingredients, macros

def get_product_nutrition(barcode):

    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={barcode}&api_key={api_key}"
        
    try:
        response = requests.get(url)
        data = response.json()
        
        print(data)
        
        if data['foods']:
            food_id = data['foods'][0]['fdcId']
            return get_nutritional_info(food_id)
        else:
            return "Product not found"
    except Exception as e:
        return f"Error: {str(e)}"

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
    
    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract the bounding box location of the barcode
        (x, y, w, h) = barcode.rect
        
        # Draw a rectangle around the barcode
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Convert barcode data to string
        barcode_data = barcode.data.decode("utf-8")
        
        # Display the barcode data on the frame
        cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        if barcode_data not in detected_barcodes:
            # Get product information based on the barcode
            product_info = get_product_nutrition(barcode_data)
            
            st.write(product_info)

            # Add barcode to set of detected barcodes
            detected_barcodes.add(barcode_data)
    
    return frame

# Function to run the barcode detection app
def run_app():
    st.title("Barcode Scanner App")

    # Button to start camera feed
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

# Run the app
if __name__ == "__main__":
    run_app()