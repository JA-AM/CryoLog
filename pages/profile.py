import streamlit as st
import pyrebase
from components.login import login
from components.sidebar import sidebar

st.set_page_config(layout="wide")

config = st.secrets["firebaseConfig"]
firebase = pyrebase.initialize_app(config)
db = firebase.database()

if 'user' not in st.session_state:
    login()

else:
    currUser = st.session_state['user']
    username =  db.child("users").child(currUser['localId']).get().val()["Username"]
    st.title("Welcome, " + username)
    st.write('member')
    st.write('includes each members conditions')
    st.write('perferences')

sidebar(1)