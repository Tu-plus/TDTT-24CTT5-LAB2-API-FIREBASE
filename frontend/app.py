import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from PIL import Image
from streamlit_cookies_controller import CookieController

# Import internal modules
from themes import get_theme_css
from config import BACKEND_URL, load_firebase_config
from utils.api_client import load_tasks
from utils.auth_helpers import handle_auto_login
from components.layout import render_theme_picker, render_hero, render_user_badge, render_stats, render_filter_sort
from components.auth_ui import render_auth_section
from components.task_form import render_add_task_form, render_edit_task_form
from components.task_item import render_task_item

# ── Page config ──────────────────────────────────────────────────────────────
favicon_path = os.path.join(os.path.dirname(__file__), "assets", "favicon.png")
icon = Image.open(favicon_path) if os.path.exists(favicon_path) else "✅"

st.set_page_config(
    page_title="TaskFlow",
    page_icon=icon,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Dynamic Theme CSS ─────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# ── Custom Component & Cookies ──────────────────────────────────────────────
_auth_component = components.declare_component(
    "google_login",
    path=os.path.join(os.path.dirname(__file__), "auth_component")
)
controller = CookieController()

# ── Session state ─────────────────────────────────────────────────────────────
for key in ["user", "id_token", "tasks", "show_add", "edit_task_id"]:
    if key not in st.session_state:
        st.session_state[key] = None if key not in ["show_add"] else False
if st.session_state.tasks is None:
    st.session_state.tasks = []

if "http_session" not in st.session_state:
    st.session_state.http_session = requests.Session()

# ── Auto-login ────────────────────────────────────────────────────────────────
handle_auto_login(controller)

# ── Header & Theme ────────────────────────────────────────────────────────────
render_theme_picker()
render_hero()

# ══════════════════════════════════════════════════════════════════════════════
# AUTH SECTION
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.user:
    render_auth_section(_auth_component, controller)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP SECTION
# ══════════════════════════════════════════════════════════════════════════════
else:
    user = st.session_state.user
    tasks = st.session_state.tasks

    # User Profile & Stats
    render_user_badge(user)
    render_stats(tasks)

    # Main Actions
    col_add, col_refresh, col_logout = st.columns([2.2, 1.4, 1.4], gap="small")
    with col_add:
        if st.button("＋ Thêm task mới", type="primary", width="stretch"):
            st.session_state.show_add = not st.session_state.show_add
    with col_refresh:
        if st.button("Làm mới", width="stretch"):
            load_tasks()
            st.rerun()
    with col_logout:
        if st.button("Đăng xuất", width="stretch"):
            controller.remove('auth_token')
            for k in ["user", "id_token", "tasks", "show_add", "edit_task_id"]:
                st.session_state[k] = None if k not in ["show_add"] else False
            st.session_state.tasks = []
            st.rerun()

    # Add Task Form
    if st.session_state.show_add:
        render_add_task_form()

    # Filter and Sort
    filter_opt, sort_opt = render_filter_sort()

    # Logic: Filter & Sort tasks
    filtered = tasks.copy()
    if filter_opt == "Chưa xong":
        filtered = [t for t in filtered if not t.get("completed")]
    elif filter_opt == "Hoàn thành":
        filtered = [t for t in filtered if t.get("completed")]

    priority_map = {"high": 1, "medium": 2, "low": 3}
    filtered.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    if sort_opt == "Mức độ ưu tiên":
        filtered.sort(key=lambda x: (
            x.get("completed", False),
            priority_map.get(x.get("priority", "medium"), 2),
            x.get("deadline") or "9999-12-31"
        ))
    else: # Hạn chót gần nhất
        filtered.sort(key=lambda x: (
            x.get("completed", False),
            x.get("deadline") or "9999-12-31",
            priority_map.get(x.get("priority", "medium"), 2)
        ))

    # Task List
    if not filtered:
        st.markdown("""
        <div style="text-align:center; padding: 3rem 1rem; color: #475569;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📭</div>
            <div>Chưa có task nào. Hãy thêm task đầu tiên!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="section-title">📋 Danh sách ({len(filtered)})</p>', unsafe_allow_html=True)
        for task in filtered:
            # Check if this task is being edited
            if st.session_state.get("edit_task_id") == task["id"]:
                render_edit_task_form(task)
            else:
                render_task_item(task)

