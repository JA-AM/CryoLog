import streamlit as st
import requests
from streamlit.components.v1 import html

def login(auth, db, cookie_manager):
    auth_url = auth.authenticate_login_with_google()
    col1, col2 = st.columns([1,1])

    def handle_google_request():
        nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
        """ % (auth_url)
        st.write(nav_script, unsafe_allow_html=True)

    with col2:
        login_form = st.form("Login to Existing Account")
        login_form.subheader("Login")
        email = login_form.text_input("Email")
        password = login_form.text_input("Password", type="password")
        login = login_form.form_submit_button("Login")

        google_form = st.form("Sign in with Google")
        google_form.subheader("Sign in with Google")
        google_form.form_submit_button("Sign in", on_click=handle_google_request)

    if login and email and password:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state['user'] = user
            cookie_manager.set("session_state_save", user)
            st.switch_page("app.py")
        except requests.exceptions.HTTPError as e:
            st.error("Invalid email or password!")
    
    with col1:
        signup_form = st.form("Sign Up")
        signup_form.subheader("Create New Account")
        newEmail = signup_form.text_input("Email", key="new_email")
        newUsername = signup_form.text_input("Username")
        newPassword = signup_form.text_input("Password", key="new_password", type="password")
        confirmPassword = signup_form.text_input("Confirm password", type="password")
        create = signup_form.form_submit_button("Create Account")

    if create and newEmail and newUsername and newPassword and confirmPassword:
        if newPassword!=confirmPassword:
            st.error("Password fields do not match!")
        else:
            try:
                user = auth.create_user_with_email_and_password(newEmail, newPassword)
                db.child("users").child(user["localId"]).child("Username").set(newUsername)
                db.child("users").child(user["localId"]).child("Password").set(newPassword)
                db.child("users").child(user["localId"]).child("Email").set(newEmail)

                st.session_state['user'] = user
                cookie_manager.set("session_state_save", user)
                st.switch_page("app.py")
            except requests.exceptions.HTTPError as e:
                err = e.args[0].response.json()['error']["message"]
                if "INVALID_EMAIL" in err:
                    st.error("Invalid email!")
                elif "EMAIL_EXISTS" in err:
                    st.error("Email already exists!")
                elif "WEAK_PASSWORD" in err:
                    st.error("Weak password: Password should be at least 6 characters")
                else:
                    st.error(err)

    if len(st.query_params)>4:
        try:
            url = "https://localhost:8501/?"
            for key in st.query_params:
                url+=key+"="+st.query_params[key]+"&"
            url = url[:-1]
            user = auth.sign_in_with_oauth_credential(url)
            db.child("users").child(user["localId"]).child("Email").set(user['email'])
            cookie_manager.set("session_state_save", user)
            st.query_params.clear()
            st.switch_page("app.py")
        except requests.exceptions.HTTPError as e:
            st.error("Something went wrong. Please try again.")
        
    



