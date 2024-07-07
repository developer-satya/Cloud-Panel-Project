# from matplotlib.dviread import Page
import streamlit as st
# import pandas as pd
# import numpy as np
import google.generativeai as genai
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyDSsmJIHWyNWP6K9enJny2nO5JTdNl7OFI"

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])



st.set_page_config(page_title="GenAI")

st.title("GenAI Chat Bot")

if 'messages' not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


def genAI(prompt):
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content(prompt)
    return response.text

prompt = st.chat_input("Ask Something...")
if prompt:
    # st.write("User has send following prompt: " + prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({'role':'user', 'content': prompt})

    response = genAI(prompt)
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role":"assistant", "content":response})


