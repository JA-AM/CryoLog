import streamlit as st
from streamlit_tags import st_tags
from components.login import login

def profile(db, cookie_manager):
    currUser = st.session_state['user']
    if "Username" in db.child("users").child(currUser['localId']).get().val():
        username =  db.child("users").child(currUser['localId']).get().val()["Username"]
    else:        
        username =  db.child("users").child(currUser['localId']).get().val()["Email"]
        username = username.split("@")[0]
    st.subheader("Welcome, " + username)
    st.write("✦ " * 4)


    user_data = db.child("users").child(currUser["localId"]).get().val()

    preset_want = user_data['Want'] if 'Want' in user_data else ""
    preset_conditions = user_data['Conditions'] if 'Conditions' in user_data else []
    preset_preferences = user_data['Preferences'] if 'Preferences' in user_data else []
    preset_age = user_data['Age'] if 'Age' in user_data else ""
    preset_height = user_data['Height'] if 'Height' in user_data else ""
    preset_weight = user_data['Weight'] if 'Weight' in user_data else ""

    with st.form('iwantsong'):
        c1, c2, c3= st.columns([1,5,1])
        with c1:
            st.markdown('##')
            st.write('I want to:') 
        with c2:
            new_want = st.text_input('', value=preset_want)
        with c3:
            st.markdown('##')
            saved = st.form_submit_button('Save')
        if saved:
            db.child("users").child(currUser['localId']).child("Want").set(new_want)
    
    with st.container(border=True):
        st.write('My health conditions and food preferences:')
        col1, col2 = st.columns([1,1])
        with col1:
            with st.container(border=True):
                conditions = st_tags(
                label='Conditions:',
                text='Press enter to add more',
                value=preset_conditions,
                # TODO change VVV these to a database of health conditions
                suggestions=['Obesity', 'Hypertension', 'Diabetes', 
                            'Hyperlipidemia', 'Acid Reflux', 'Gallstones', 
                            'Osteoporosis', 'Irritable Bowel Syndrome', 'Gout'],
                maxtags = 20,
                key='cond')
                if st.button('Save', key='condsub'):
                    db.child("users").child(currUser["localId"]).child("Conditions").set(conditions)

        with col2:
            with st.container(border=True):
                preferences = st_tags(
                label='Preferences:',
                text='Press enter to add more',
                value=preset_preferences,
                suggestions=['Fruits', 'Sweets', 'Candy', 
                            'Meats', 'Protein', 'Fiber', 
                            'Chips', 'Fried Foods', 'Boba'],
                maxtags = 20,
                key='pref')
                if st.button('Save', key='prefsub'):
                    db.child("users").child(currUser["localId"]).child("Preferences").set(preferences)
    st.write("✦ " * 4)

    def biometrics_form(label, preset_value):
        with st.form(label + 'form'):
            c1, c2 = st.columns([6,1])
            with c1:
                new_value = st.text_input('My '+label+':', value=preset_value, key=label+'input')
            with c2:
                st.write("##")
                saved = st.form_submit_button('Save')
            if saved:
                db.child("users").child(currUser['localId']).child(label).set(new_value)

    def biometrics_numeric_form(label, preset_value):
        if preset_value:
            unit_selection = preset_value[-2:]
            preset_value = preset_value[:-2]
        else:
            unit_selection = 0
            preset_value = ""
        
        with st.form(label + 'form'):
            c1, c2, c3 = st.columns([4.6,1.3,1])
            with c1:
                new_value = st.text_input(f'My {label}:', value=preset_value, key=label+'input')
            with c2:
                if label == 'Weight':
                    selection = st.selectbox('Unit', ('kg', 'lb'), index={'kg': 0, 'lb': 1}.get(unit_selection, 0))
                else:
                    selection = st.selectbox('Unit', ('ft', 'in', 'cm'), index={'ft': 0, 'in': 1, 'cm': 2}.get(unit_selection, 0))
            with c3:
                st.write("##")
                saved = st.form_submit_button('Save')
            if saved:
                db.child("users").child(currUser['localId']).child(label).set(new_value+selection)

    with st.container(border=True):
        st.write('My Biometrics:')
        biometrics_form('Username', username)
        biometrics_form('Age', preset_age)
        biometrics_numeric_form('Height', preset_height)
        biometrics_numeric_form('Weight', preset_weight)

    st.divider()
    if st.button('Log Out', key='logoutbtn'):
        cookie_manager.remove("session_state_save")
        del st.session_state['user']
        st.switch_page("app.py")