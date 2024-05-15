import streamlit as st
from streamlit_cookies_controller import CookieController
import pyrebase
from components.profile import profile
from components.chat import chat
from components.list import search
from components.login import login
from components.camera import camera
from st_on_hover_tabs import on_hover_tabs
import time

st.set_page_config(layout="wide")
st.markdown('<style>' + open('./css/style.css').read() + '</style>', unsafe_allow_html=True)

time.sleep(0.4)

def get_state_from_cookie(cookie_manager):
    if cookie_manager.get("session_state_save"):
        st.session_state['user'] = cookie_manager.get("session_state_save")

def get_default_tab_from_cookie(cookie_manager):
    if "prev_saved_tab" not in st.session_state and cookie_manager.getAll():
        default_tab = cookie_manager.get("tabs_save") if cookie_manager.get("tabs_save") else 0
        st.session_state['prev_saved_tab'] = default_tab
        return default_tab
    else:
        return st.session_state['prev_saved_tab']

def firebase_setup():
    config = st.secrets["firebaseConfig"]
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()
    
    return auth, db

def display_header():
    st.header("C R Y O L O G")

def display_sidebar(auth, db, cookie_manager, default_tab):
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Home', 'Profile', 'Scan', 'List', 'Chat'], 
                            iconName=["home", 'personrounded', 'camera', "listrounded", "assistantsharp"], 
                            default_choice=default_tab)
    
    cookie_manager.set("tabs_save", ['Home', 'Profile', 'Scan', 'List', 'Chat'].index(tabs))
    
    if 'user' not in st.session_state:
        login(auth, db, cookie_manager)
    
    elif tabs =='Home':
        st.title('Home')

    elif tabs == 'Profile':
        profile(db, cookie_manager)
    
    elif tabs == 'Scan':
        camera()
        pass

    elif tabs == 'List':
        search(db)
    
    elif tabs == 'Chat':
        chat()

def main():
    cookie_manager = CookieController()
    auth, db = firebase_setup()
    get_state_from_cookie(cookie_manager)
    default_tab = get_default_tab_from_cookie(cookie_manager)
    display_header()
    display_sidebar(auth, db, cookie_manager, default_tab)

if __name__ == '__main__':
    main()