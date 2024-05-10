import streamlit as st
import pyrebase
import requests

config = st.secrets['firebaseConfig']

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def login():
    st.header("Login Page")

    st.subheader("Login to Existing Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login = st.button("Login")

    if login and email and password:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state['user'] = user
            st.switch_page("app.py")
        except requests.exceptions.HTTPError as e:
            st.error("Invalid email or password!")

    st.subheader("OR")

    st.subheader("Create New Account")
    newEmail = st.text_input("Email", key="new_email")
    newUsername = st.text_input("Username")
    newPassword = st.text_input("Password", key="new_password", type="password")
    confirmPassword = st.text_input("Confirm password", type="password")
    create = st.button("Create Account")

    if create and newEmail and newUsername and newPassword and confirmPassword:
        if newPassword!=confirmPassword:
            st.error("Password fields do not match!")
        else:
            try:
                user = auth.create_user_with_email_and_password(newEmail, newPassword)
                db.child("users").child(user["localId"]).child("Username").set(newUsername)
                db.child("users").child(user["localId"]).child("Password").set(newPassword)
                db.child("users").child(user["localId"]).child("Conditions").set([None])
                db.child("users").child(user["localId"]).child("Preferences").set([None])
                st.session_state['user'] = user
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


