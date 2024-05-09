from st_on_hover_tabs import on_hover_tabs
import streamlit as st

def sidebar(selection):
    st.markdown('<style>' + open('./css/style.css').read() + '</style>', unsafe_allow_html=True)

    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Home', 'Profile', 'Scan', 'List', 'Chat'], 
                            iconName=["home", 'personrounded', 'camera', "listrounded", "assistantsharp"], default_choice=selection)

    if tabs =='Home':
        st.switch_page("app.py")

    elif tabs == 'Profile':
        st.switch_page("pages/profile.py")

    elif tabs == 'Scan':
        st.switch_page("pages/camera.py")

    elif tabs == 'List':
        st.switch_page("pages/list.py")
    
    elif tabs == 'Chat':
        st.switch_page("pages/chat.py")