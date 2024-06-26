from streamlit_webrtc import WebRtcMode, webrtc_streamer
from twilio.rest import Client
import cv2
from pyzbar.pyzbar import decode
import av
import streamlit as st
import requests

api_key = st.secrets['FOODDATA_API_KEY']

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

def callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    barcodes = decode(gray)

    if barcodes:
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')

            (x, y, w, h) = barcode.rect

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            if barcode_data not in detected_barcodes:
                print(f"Found barcode: {barcode_data}")
                product_info = get_product_nutrition(barcode_data)
                
                st.write(product_info)

                #TODO Create Add to List Function, Learn More About Ingredients Function
            
                detected_barcodes.add(barcode_data)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

def camera():
    st.title("Barcode Scanner")

    account_sid = st.secrets['TWILIO_ACCOUNT_SID']
    auth_token = st.secrets['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    token = client.tokens.create()
    webrtc_streamer(
        key="opencv-filter",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": token.ice_servers},
        video_frame_callback=callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

if __name__ == "__main__":
    camera()