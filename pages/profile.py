import streamlit as st
import pyrebase
from streamlit_tags import st_tags
from components.login import login
from components.sidebar import sidebar

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

    user_data = db.child("users").child(currUser["localId"]).get().val()

    preset_conditions = user_data['Conditions'] if 'Conditions' in user_data else []
    preset_preferences = user_data['Preferences'] if 'Preferences' in user_data else []
    conditions = st_tags(
    label='# Enter Conditions:',
    text='Press enter to add more',
    value=preset_conditions,
    suggestions=['Obesity', 'Hypertension', 'Diabetes', 
                 'Hyperlipidemia', 'Acid Reflux', 'Gallstones', 
                 'Osteoporosis', 'Irritable Bowel Syndrome', 'Gout'],
    maxtags = 20,
    key='cond')
    if st.button('Submit', key='condsub'):
        db.child("users").child(currUser["localId"]).child("Conditions").set(conditions)

    preferences = st_tags(
    label='# Enter Preferences:',
    text='Press enter to add more',
    value=preset_preferences,
    suggestions=['Fruits', 'Sweets', 'Candy', 
                 'Meats', 'Protein', 'Fiber', 
                 'Chips', 'Fried Foods', 'Boba'],
    maxtags = 20,
    key='pref')
    if st.button('Submit', key='prefsub'):
        db.child("users").child(currUser["localId"]).child("Preferences").set(preferences)
    
    # db.child("users").child(currUser["localId"]).child("Conditions").set([""])
    # db.child("users").child(currUser["localId"]).child("Preferences").set([""])


sidebar(1)