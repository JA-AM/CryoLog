import streamlit as st
import time
from snowflake.snowpark.session import Session

session = Session.builder.configs(st.secrets['SNOWFLAKE_CONFIG']).create()

def response_generator(prompt):
    cmd = f"""
             select snowflake.cortex.complete(?,?) as response
           """
    
    df_response = session.sql(cmd, params=['snowflake-arctic', prompt]).collect()
    
    for word in df_response[0].RESPONSE.split():
        yield word + " "
        time.sleep(0.05)
    
st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you?"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))

    st.session_state.messages.append({"role": "assistant", "content": response})