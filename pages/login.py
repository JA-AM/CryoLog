import streamlit as st
import pyrebase

config = st.secrets['firebaseConfig']

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

st.header("Login Page")

st.subheader("Login to Existing Account")
email = st.text_input("Email")
password = st.text_input("Password")
login = st.button("Login")

st.subheader("OR")

st.subheader("Create New Account")
newEmail = st.text_input("Email", key="new_email")
newPassword = st.text_input("Password", key="new_password")
confirmPassword = st.text_input("Confirm password")
create = st.button("Create Account")

if login and email and password:
    user = auth.sign_in_with_email_and_password(email, password)
    st.title("Welcome " + user['email'])
    st.balloons()

if create and newEmail and newPassword and confirmPassword and newPassword==confirmPassword:
    user = auth.create_user_with_email_and_password(newEmail, newPassword)
    st.title("Welcome")
    st.balloons()


