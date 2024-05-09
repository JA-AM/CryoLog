import streamlit as st
from components.camera import camera
from components.sidebar import sidebar

st.title("CAMERA")
camera()

sidebar(2)