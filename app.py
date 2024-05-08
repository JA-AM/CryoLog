from st_on_hover_tabs import on_hover_tabs
from components.camera import camera
from components.login import login
import streamlit as st
import pyrebase

st.set_page_config(layout="wide")

config = st.secrets["firebaseConfig"]
firebase = pyrebase.initialize_app(config)
db = firebase.database()

if 'user' not in st.session_state:
    login()

currUser = st.session_state['user']
username =  db.child("users").child(currUser['localId']).get().val()["Username"]
st.title("Welcome, " + username)

def main():
    display_header()
    display_sidebar()

def display_header():
    st.header("C R Y O L O G")

def display_sidebar():
    st.markdown('<style>' + open('./css/style.css').read() + '</style>', unsafe_allow_html=True)

    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Home', 'Profile', 'Scan', 'List', 'Chat'], 
                            iconName=["home", 'personrounded', 'camera', "listrounded", "assistantsharp"], default_choice=0)
    
    if tabs =='Home':
        st.title("MOTTO")
        st.write('description of service')

    elif tabs == 'Profile':
        st.title("{NAME}")
        st.write('members')
        st.write('includes each members conditions')
        st.write('perferences')

    elif tabs == 'Scan':
        camera()

    elif tabs == 'List':
        st.title("List")
        st.write('Name of option is {}'.format(tabs))

if __name__ == "__main__":
    main()