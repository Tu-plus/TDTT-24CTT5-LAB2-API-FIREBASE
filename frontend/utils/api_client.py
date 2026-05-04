import streamlit as st
from config import BACKEND_URL

def api(method, path, **kwargs):
    headers = kwargs.pop("headers", {})
    if st.session_state.id_token:
        headers["Authorization"] = f"Bearer {st.session_state.id_token}"
    
    url = f"{BACKEND_URL}{path}"
    try:
        session = st.session_state.http_session
        resp = getattr(session, method)(url, headers=headers, timeout=10, **kwargs)
        return resp
    except Exception as e:
        st.error(f"Không kết nối được backend: {e}")
        return None

def load_tasks():
    resp = api("get", "/tasks/")
    if resp and resp.status_code == 200:
        st.session_state.tasks = resp.json()
