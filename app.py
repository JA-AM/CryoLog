import streamlit as st
from streamlit_cookies_controller import CookieController
import pyrebase
from components.profile import profile
from components.chat import chat
from components.list import search
#from components.camera import camera
from st_on_hover_tabs import on_hover_tabs
import time

st.set_page_config(layout="wide")
st.markdown('<style>' + open('./css/style.css').read() + '</style>', unsafe_allow_html=True)

cookie_manager = CookieController()
time.sleep(0.4)

def get_state_from_cookie(cookie_manager):
    if cookie_manager.get("session_state_save"):
        st.session_state['user'] = cookie_manager.get("session_state_save")

def firebase_setup():
    config = st.secrets["firebaseConfig"]
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()
    
    return auth, db

def is_logged_in():
    return 'user' in st.session_state


def display_header():
    st.header("C R Y O L O G")

def display_sidebar(auth, db, cookie_manager):
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Home', 'Profile', 'Scan', 'List', 'Chat'], 
                            iconName=["home", 'personrounded', 'camera', "listrounded", "assistantsharp"], 
                            default_choice=cookie_manager.get("tabs_save"))

    if not is_logged_in():
        st.write(tabs)
        profile(auth, db, cookie_manager)
    
    elif tabs =='Home':
        cookie_manager.set("tabs_save", 0)

    elif tabs == 'Profile':
        cookie_manager.set("tabs_save", 1)
        profile(auth, db, cookie_manager)
    
    elif tabs == 'Scan':
        cookie_manager.set("tabs_save", 2)
        #camera()
        pass

    elif tabs == 'List':
        cookie_manager.set("tabs_save", 3)
        search(auth, db)
    
    elif tabs == 'Chat':
        cookie_manager.set("tabs_save", 4)
        chat()

def main():
    auth, db = firebase_setup()
    get_state_from_cookie(cookie_manager)
    display_header()
    display_sidebar(auth, db, cookie_manager)

if __name__ == '__main__':
    main()