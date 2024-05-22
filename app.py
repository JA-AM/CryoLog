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
    
image_paths = ["logo", "favicon", "banner", "Dave", "Niel", "Sarah"]
images = {}

for path in image_paths:
    with open(f'images/{path}.svg', "r") as f:
        images[path] = f.read()

st.set_page_config(layout="wide", page_icon=images["favicon"], page_title="CryoLog")
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
    st.image(images["banner"], width=300)
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
        chat(db, images)

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
                st.image(images['logo'], width=50)
                st.markdown("""
                        CryoLog is your all-in-one solution for optimizing your
                        nutrition and enhancing your well-being. Utilizing cutting-edge machine 
                        learning technology, CryoLog empowers you to cultivate healthier eating 
                        habits, streamline your shopping experience, and achieve peak nutrient 
                        intake effortlessly.
                        """)
            
            with st.expander('How was CryoLog built?'):
                st.image(images['logo'], width=50)
                st.markdown("""
                        Utilizing Streamlit for frontend, and components like OpenCV and streamlit-webrtc for barcode scanning,
                        the app seamlessly integrates with the FoodData Central API to provide detailed product information.
                        On the backend, Snowflake Arctic LLM is employed via Snowflake Cortex,
                        leveraging Retrieval-Augmented Generation (RAG) for contextually accurate responses based on user data and private nutritional documents.
                        The app ensures secure login, efficient data management, and personalized recommendations,
                        offering significant benefits for user engagement, healthcare providers, and retail integration,
                        while providing valuable insights into nutritional trends and consumer behavior.
                        """)

                st.link_button("Link to Full Documentation", 'https://docs.google.com/document/d/1wocwAc723T7vXrriHCnnfn_JbEPEwZsDuWmr5YuYPWc/edit?usp=sharing')
            
            #st.markdown("""<span style='color: #779ecb;'>✦ ✦ ✦ ✦""", unsafe_allow_html=True)
            st.markdown("""**With Cryolog, the journey to a healthier you is simplified, efficient, and enjoyable.
                         Take the first step towards unlocking your full potential with CryoLog today!**""")
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
