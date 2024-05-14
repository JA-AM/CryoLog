import streamlit as st
import pyrebase
from components.profile import profile
from components.chat import chat
from components.list import search
#from components.camera import camera
from st_on_hover_tabs import on_hover_tabs

def firebase_setup():
    config = st.secrets["firebaseConfig"]
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()
    
    return auth, db

def is_logged_in():
    return 'user' in st.session_state

def display_header():
    st.set_page_config(layout="wide")
    st.header("C R Y O L O G")

def display_sidebar(auth, db):
    st.markdown('<style>' + open('./css/style.css').read() + '</style>', unsafe_allow_html=True)

    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Home', 'Profile', 'Scan', 'List', 'Chat'], 
                            iconName=["home", 'personrounded', 'camera', "listrounded", "assistantsharp"], default_choice=0)

    if not is_logged_in():
        st.write(tabs)
        profile(auth, db)
    
    elif tabs =='Home':
        pass

    elif tabs == 'Profile':
        profile(auth, db)
    
    elif tabs == 'Scan':
        #camera()
        pass

    elif tabs == 'List':
        search()
    
    elif tabs == 'Chat':
        chat()

def main():
    auth, db = firebase_setup()
    display_header()
    display_sidebar(auth, db)

if __name__ == '__main__':
    main()