from streamlit_webrtc import WebRtcMode, webrtc_streamer
from twilio.rest import Client
import cv2
from pyzbar.pyzbar import decode
import av
import streamlit as st
from components.food_search import get_nutritional_info_barcode

def get_barcode_set() -> set:
    if 'detected_barcodes' not in st.session_state:
        st.session_state['detected_barcodes'] = set()
    
    return st.session_state['detected_barcodes']

detected_barcodes = get_barcode_set()

def callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    font = cv2.FONT_HERSHEY_SIMPLEX  # Font for text overlay
    font_scale = 0.5  # Adjust font size as needed
    font_thickness = 2  # Adjust text thickness as needed
    text_color = (0, 255, 0)  # Text color (green)

    barcodes = decode(gray)

    if barcodes:
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')

            (x, y, w, h) = barcode.rect

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text_x = int(x + w / 2 - (len(barcode_data) * font_scale * 6.5) / 2)
            text_y = y + h - 5

            text = f"{barcode_data}"
            cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)
            
            if barcode_data not in detected_barcodes:
                detected_barcodes.add(barcode_data)
    
    text = ""
    for barcode in detected_barcodes:
        text += barcode + " "
    
    cv2.putText(img, f"Barcodes found: {text}", (50, 50), font, font_scale, text_color, font_thickness)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

def display_scanned_items(db):
    currUser = st.session_state['user']
    user_data = db.child("users").child(currUser["localId"]).get().val()
    userFoods = user_data['Foods'] if 'Foods' in user_data else []

    st.subheader("Scanned Items")

    for i, barcode_data in enumerate(detected_barcodes):
        product_info = get_nutritional_info_barcode(barcode_data)
        if product_info is None:
            st.toast(f"No Information For Barcode: {barcode_data}")
            continue
        with st.popover(f"{product_info['description']}({product_info['brandName']})"):
            st.markdown(f"Food Category: {product_info['brandedFoodCategory']}")
            st.markdown(f"FDC ID: {product_info['fdcId']}")
            st.markdown(f"Ingredients: {product_info['ingredients']}")
            
            with st.expander("Label Nutrients", expanded=False):
                st.write(product_info['labelNutrients'])
            
            if st.button("Add to List", key=i):
                st.toast(f"Added {product_info['description']} to My List", icon="✅") 
                userFoods.append(product_info)
                db.child("users").child(currUser["localId"]).child("Foods").set(userFoods)

def camera(db):
    st.title("Barcode Scanner")

    account_sid = st.secrets['TWILIO_ACCOUNT_SID']
    auth_token = st.secrets['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    token = client.tokens.create()
    
    webrtc_ctx = webrtc_streamer(
        key="opencv-filter",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={
            "iceServers": token.ice_servers,
            "iceTransportPolicy": "relay"
        },
        video_frame_callback=callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )

    if not webrtc_ctx.state.playing:
        display_scanned_items(db)

if __name__ == "__main__":
    camera()