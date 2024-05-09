import streamlit as st # Import python packages
from components.chat import chat
import pyrebase
from components.login import login
from components.sidebar import sidebar

config = st.secrets["firebaseConfig"]
firebase = pyrebase.initialize_app(config)
db = firebase.database()

if 'user' not in st.session_state:
    login()

else:
    currUser = st.session_state['user']
    username =  db.child("users").child(currUser['localId']).get().val()["Username"]
    st.title("Welcome, " + username)
    chat()

sidebar(4)