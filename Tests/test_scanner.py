import cv2
from pyzbar import pyzbar
import requests
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("FOODDATA_API_KEY")  # Replace this with your API key from FoodData Central

# Set to keep track of detected barcodes
detected_barcodes = set()

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

def decode_barcode(frame):
    global detected_barcodes
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect barcodes in the frame
    barcodes = pyzbar.decode(gray)
    
    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract the bounding box location of the barcode
        (x, y, w, h) = barcode.rect
        
        # Convert barcode data to string
        barcode_data = barcode.data.decode("utf-8")
        
        # Draw a rectangle around the barcode
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
        # Display the barcode data on the frame
        cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        if barcode_data not in detected_barcodes:
            # Get product information based on the barcode
            product_info = get_product_nutrition(barcode_data)
            
            print(product_info)

            # Add barcode to set of detected barcodes
            detected_barcodes.add(barcode_data)

    return frame

def main():
    # Open the camera
    cap = cv2.VideoCapture(0)
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # If the frame was not captured successfully, break the loop
        if not ret:
            break
        
        # Call the function to decode barcodes
        frame = decode_barcode(frame)
        
        # Display the resulting frame
        cv2.imshow('Barcode Scanner', frame)
        
        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
