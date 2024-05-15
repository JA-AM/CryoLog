from streamlit_webrtc import WebRtcMode, webrtc_streamer
from twilio.rest import Client
import cv2
from pyzbar.pyzbar import decode
import av
import streamlit as st
import requests
from components.food_search import get_nutritional_info

api_key = st.secrets['FOODDATA_API_KEY']

detected_barcodes = set()

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
                
                print(product_info)
                #st.write(product_info['description'])

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
        async_processing=True
    )

if __name__ == "__main__":
    camera()