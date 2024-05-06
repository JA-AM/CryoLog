import streamlit as st
import pyrebase
from pages import login

config = st.secrets['firebaseConfig']
firebase = pyrebase.initialize_app(config)
db = firebase.database()

if 'user' not in st.session_state:
    st.switch_page("pages/login.py")

currUser = st.session_state['user']
username =  db.child("users").child(currUser['localId']).get().val()["Username"]
st.title("Welcome, " + username)

