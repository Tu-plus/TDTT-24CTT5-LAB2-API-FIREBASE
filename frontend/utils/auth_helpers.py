import streamlit as st
import pyrebase
from config import load_firebase_config
from utils.api_client import api, load_tasks

@st.cache_resource
def init_firebase():
    config = load_firebase_config()
    firebase = pyrebase.initialize_app(config)
    return firebase.auth()

def handle_auto_login(controller):
    cookie_token = None
    try:
        cookie_token = controller.get('auth_token')
    except TypeError:
        pass

    if not st.session_state.user and cookie_token:
        st.session_state.id_token = cookie_token
        resp = api("get", "/auth/me")
        if resp and resp.status_code == 200:
            st.session_state.user = resp.json()
            load_tasks()
            st.rerun()
        else:
            st.session_state.id_token = None
            controller.remove('auth_token')
