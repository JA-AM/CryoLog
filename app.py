import streamlit as st
from streamlit_cookies_controller import CookieController
import firebase
from components.profile import profile
from components.chat import chat
from components.list import search
from components.login import login
from components.camera import camera
from st_on_hover_tabs import on_hover_tabs
import time


st.set_page_config(layout="wide")
st.markdown('<style>' + open('./css/style.css').read() + '</style>', unsafe_allow_html=True)

placeholder = st.empty()
with placeholder.status('Loading...'):
    cookie_manager = CookieController()
    time.sleep(0.4)
placeholder.empty()

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
    client_config = {
        "client_id": st.secrets["client_id"],
        "client_secret": st.secrets["client_secret"],
        "redirect_uris": [st.secrets["redirect_uris"]],
    }
    app = firebase.initialize_app(config)
    auth = app.auth(client_secret=client_config)
    db = app.database()
    
    return auth, db

def display_header():
    st.title("C R Y O L O G")

def display_sidebar(auth, db, cookie_manager, default_tab):
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Home', 'Profile', 'Scan', 'My List', 'Chat'], 
                            iconName=["home", 'personrounded', 'camera', "listrounded", "assistantsharp"], 
                            default_choice=default_tab)
    
    cookie_manager.set("tabs_save", ['Home', 'Profile', 'Scan', 'My List', 'Chat'].index(tabs))
    
    if 'user' not in st.session_state:
        login(auth, db, cookie_manager)
    
    elif tabs =='Home':
        st.subheader("✦ " * 4)
        st.write('Your Intelligent Nutrition Companion (catchphrase goes here)')
        st.image('https://a3.espncdn.com/combiner/i?img=%2Fi%2Fheadshots%2Fnba%2Fplayers%2Ffull%2F1966.png')
        st.write('image replace with logo svg IMPORTANT')
        st.write('Welcome to Cryolog, your all-in-one solution for optimizing your \
                 nutrition and enhancing your well-being. Utilizing cutting-edge machine \
                learning technology, Cryolog empowers you to cultivate healthier eating \
                 habits, streamline your shopping experience, and achieve peak nutrient \
                 intake effortlessly. (gpt blurb, replace with actual person speak)')
        st.image('https://a3.espncdn.com/combiner/i?img=%2Fi%2Fheadshots%2Fnba%2Fplayers%2Ffull%2F1966.png')
        st.write('image replace with smth small or uncontrasting, break up text')
        st.write('Say goodbye to guesswork and hello to precision with Cryolog\'s personalized \
                 recommendations tailored to your unique dietary needs and wellness goals. Whether \
                 you\'re striving to manage weight, increase energy levels, or simply cultivate a \
                 healthier lifestyle, Cryolog provides you with actionable insights and guidance every \
                 step of the way. (more gpt speak, remember to replace)')
        st.write("✦ " * 4)
        st.write('With Cryolog, the journey to a healthier you is simplified, efficient, and \
                 enjoyable. Take the first step towards unlocking your full potential with Cryolog today')
        

    elif tabs == 'Profile':
        profile(db, cookie_manager)
    
    elif tabs == 'Scan':
        camera(db)

    elif tabs == 'My List':
        search(db)
    
    elif tabs == 'Chat':
        chat(db)

def main():
    auth, db = firebase_setup()
    get_state_from_cookie(cookie_manager)
    default_tab = get_default_tab_from_cookie(cookie_manager)
    display_header()
    display_sidebar(auth, db, cookie_manager, default_tab)

if __name__ == '__main__':
    main()