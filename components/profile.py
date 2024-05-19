import streamlit as st
from streamlit_tags import st_tags
from datetime import date

def biometrics_numeric_form(label, preset_value):
        if preset_value:
            unit_selection = preset_value[-2:]
            preset_value = preset_value[:-2]
        else:
            unit_selection = 0
            preset_value = ""
        
        with st.container(border=True):
            c1, c2 = st.columns([4.6,1.3])
            with c1:
                new_value = st.text_input(label, value=preset_value, key=label+'input')
            with c2:
                if label == 'Weight':
                    selection = st.selectbox('Unit', ('kg', 'lb'), index={'kg': 0, 'lb': 1}.get(unit_selection, 0))
                elif label == 'Height':
                    selection = st.selectbox('Unit', ('ft', 'in', 'cm'), index={'ft': 0, 'in': 1, 'cm': 2}.get(unit_selection, 0))
                else:
                    return new_value

        try:
            float(new_value)
        except ValueError:
            return None
        
        return new_value + " " + selection

def profile(auth, db, cookie_manager):
    currUser = st.session_state['user']
    if "Username" in db.child("users").child(currUser['localId']).get().val():
        username =  db.child("users").child(currUser['localId']).get().val()["Username"]
    else:        
        username =  db.child("users").child(currUser['localId']).get().val()["Email"]
        username = username.split("@")[0]
    st.header("Profile")
    st.markdown("""<span style='color: #779ecb;'>✦ ✦ ✦ ✦""", unsafe_allow_html=True)

    user_data = db.child("users").child(currUser["localId"]).get().val()
    
    biometrics = user_data.get('Biometrics', {})
    preset_bday = biometrics.get('Birthday', None)
    preset_height = biometrics.get('Height', '')
    preset_weight = biometrics.get('Weight', '')
    preset_conditions = biometrics.get('Conditions', [])

    preset_goals = user_data.get('Goals', [])
    preset_preferences = user_data.get('Preferences', [])

    # Biometrics Form
    with st.container(border=True):
        st.markdown('### My Biometrics')
        with st.form('biometrics_form', border=False):
            with st.container(border=True):         
                preset_bday = date.fromisoformat(preset_bday) if isinstance(preset_bday, str) else None
                new_bday = st.date_input("Birthday:", value=preset_bday)

            new_height = biometrics_numeric_form('Height', preset_height)
            new_weight = biometrics_numeric_form('Weight', preset_weight)

            with st.container(border=True):
                conditions = st_tags(
                    label='Health Conditions:',
                    text='Press enter to add more',
                    value=preset_conditions,
                    # TODO change VVV these to a database of health conditions
                    suggestions=['Obesity', 'Hypertension', 'Diabetes', 
                                'Hyperlipidemia', 'Acid Reflux', 'Gallstones', 
                                'Osteoporosis', 'Irritable Bowel Syndrome', 'Gout'],
                    maxtags = 20,
                    key='cond'
                )
            
            if new_bday is not None:
                biometrics['Birthday'] = new_bday.isoformat()
            
            biometrics['Height'] = new_height
            biometrics['Weight'] = new_weight
            biometrics['Conditions'] = conditions
            
            can_save = True
            if st.form_submit_button('Save'):
                for key, value in biometrics.items():
                    if value is None:
                        st.error("Biometrics must be numeric values!")
                        can_save = False
                        
                if can_save:
                    db.child("users").child(currUser['localId']).child('Biometrics').set(biometrics)
                    st.toast("Biometrics Saved")
    
    # Preferences Form
    with st.form('pref_form', border=True):
        st.markdown('### My Preferences and Goals')

        c1, c2 = st.columns([1,1])
        with c1:
            with st.container(border=True):
                preferences = st_tags(
                    label='Preferences:',
                    text='Press enter to add more',
                    value=preset_preferences,
                    suggestions=['Fruits', 'Sweets', 'Candy', 
                                'Meats', 'Protein', 'Fiber', 
                                'Chips', 'Fried Foods', 'Boba'],
                    maxtags = 20,
                    key='pref'
                )
        with c2:
            with st.container(border=True):
                goals = st_tags(
                    label='Goals:',
                    text='Press enter to add more',
                    value=preset_goals,
                    suggestions=[],
                    maxtags = 20,
                    key='goals'
                    )            

        if st.form_submit_button("Save"):
            db.child("users").child(currUser["localId"]).child("Preferences").set(preferences)
            db.child("users").child(currUser["localId"]).child("Goals").set(goals)
            st.toast("Preferences and Goals Saved")
    
    # Account Settings
    with st.container(border=True):
        st.markdown('### Account Settings')
        c1, c2 = st.columns([1,1])
        with c1:
            with st.container(border=True):
                st.write("Change Username")
                if 'Username' in user_data:
                    username = st.text_input('Current Username',value=user_data['Username'], key='username')
                else:
                    username = st.text_input('Current Username',value="", key='emptyUsername')
                if st.button("Save"):
                    st.toast("Account settings saved")
                    db.child("users").child(currUser["localId"]).child("Username").set(username)
        with c2:
            with st.container(border=True):
                st.write("Change Password")
                if st.button("Reset Password"):
                    st.toast("Reset password email sent")
                    auth.send_password_reset_email(user_data['Email'])
                    


    st.markdown("""<span style='color: #779ecb;'>✦ ✦ ✦ ✦""", unsafe_allow_html=True)
    st.divider()
    if st.button('Log Out', key='logoutbtn'):
        cookie_manager.remove("session_state_save")
        del st.session_state['user']
        st.switch_page("app.py")