import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_cookies_controller import CookieController
import firebase
from components.profile import profile
from components.chat import chat
from components.list import search
from components.login import login
from components.camera import camera
from st_on_hover_tabs import on_hover_tabs
import time

with open("images/cryolog_logo.svg", "r") as file:
    logo = file.read()

st.set_page_config(layout="wide", page_icon=logo, page_title="CryoLog")
st.markdown('<style>' + open('./css/style.css').read() + '</style>', unsafe_allow_html=True)
cookie_manager = CookieController()

def get_state_from_cookie():
    if cookie_manager.get("session_state_save"):
        st.session_state['user'] = cookie_manager.get("session_state_save")

def get_default_tab_from_cookie():
    if "prev_saved_tab" not in st.session_state and cookie_manager.getAll():
        default_tab = cookie_manager.get("tabs_save") if cookie_manager.get("tabs_save") else 0
        st.session_state['prev_saved_tab'] = default_tab
        
    return st.session_state.get('prev_saved_tab', 0)

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
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(logo, width=90)
    with col2:
        st.title("C R Y O L O G")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

def display_sidebar(auth, db, default_tab):
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Home', 'Profile', 'Scan', 'My List', 'Chat'], 
                            iconName=["home", 'personrounded', 'camera', "listrounded", "assistantsharp"], 
                            default_choice=default_tab)
    
    cookie_manager.set("tabs_save", ['Home', 'Profile', 'Scan', 'My List', 'Chat'].index(tabs))
    
    if 'user' not in st.session_state:
        login(auth, db, cookie_manager)
    elif tabs =='Home':
        home()
    elif tabs == 'Profile':
        profile(auth, db, cookie_manager)
    elif tabs == 'Scan':
        camera(db)
    elif tabs == 'My List':
        search(db)
    elif tabs == 'Chat':
        chat(db)

def home():
    with stylable_container(
        key = "homecontainer",
        css_styles= """
        {
            background-color: #111111;
            border: 0.1px solid #222e3b;
            border-radius: 0.5rem;
            padding: 1em;
            margin:
        }
        """
        ):
        with st.container():
            st.header("Home")
            st.markdown("""<span style='color: #779ecb; font-size: 1.5em;'>✦ ✦ ✦ ✦""", unsafe_allow_html=True)
            st.markdown("**Welcome to CryoLog, your chilly grocery list powered by Streamlit and Snowflake Arctic!**")
            with st.expander("What is CryoLog?"):
                st.markdown("""
                        CryoLog is your all-in-one solution for optimizing your
                        nutrition and enhancing your well-being. Utilizing cutting-edge machine 
                        learning technology, Cryolog empowers you to cultivate healthier eating 
                        habits, streamline your shopping experience, and achieve peak nutrient 
                        intake effortlessly. (gpt blurb, replace with actual person speak)
                        """)
            
            with st.expander('Lebronify'):
                st.image('https://a3.espncdn.com/combiner/i?img=%2Fi%2Fheadshots%2Fnba%2Fplayers%2Ffull%2F1966.png')
                st.write('image replace with smth small or uncontrasting, break up text')
                st.write('Say goodbye to guesswork and hello to precision with Cryolog\'s personalized \
                        recommendations tailored to your unique dietary needs and wellness goals. Whether \
                        you\'re striving to manage weight, increase energy levels, or simply cultivate a \
                        healthier lifestyle, Cryolog provides you with actionable insights and guidance every \
                        step of the way. (more gpt speak, remember to replace)')
            #st.markdown("""<span style='color: #779ecb;'>✦ ✦ ✦ ✦""", unsafe_allow_html=True)
            st.write('With Cryolog, the journey to a healthier you is simplified, efficient, and \
                        enjoyable. Take the first step towards unlocking your full potential with Cryolog today')
def main():
    auth, db = firebase_setup()
    get_state_from_cookie()
    placeholder = st.empty()
    with placeholder.status('Loading...'):
        default_tab = get_default_tab_from_cookie()
        time.sleep(0.4)
    placeholder.empty()
    display_header()
    display_sidebar(auth, db, default_tab)

if __name__ == '__main__':
    main()