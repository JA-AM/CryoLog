import streamlit as st
import pyrebase
from components.login import login
from components.sidebar import sidebar

st.set_page_config(layout="wide")

config = st.secrets["firebaseConfig"]
firebase = pyrebase.initialize_app(config)
db = firebase.database()

if 'user' in st.session_state:
    currUser = st.session_state['user']
    username =  db.child("users").child(currUser['localId']).get().val()["Username"]
    st.title("Welcome, " + username)

st.header("C R Y O L O G")
st.title("Home")

sidebar(0)