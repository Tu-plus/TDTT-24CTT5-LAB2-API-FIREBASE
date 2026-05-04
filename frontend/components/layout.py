import streamlit as st
import os
from themes import THEMES

def render_theme_picker():
    st.markdown('<div class="theme-switcher">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    for col, key in zip([c1, c2, c3], ["dark", "ocean", "white"]):
        with col:
            is_active = st.session_state.theme == key
            if st.button(THEMES[key]["name"], key=f"theme_{key}", 
                         width="stretch",
                         type="primary" if is_active else "secondary"):
                st.session_state.theme = key
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_hero():
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
    if os.path.exists(logo_path):
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.image(logo_path, width="stretch")
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="hero">
            <h1>✅ TaskFlow</h1>
            <p>Quản lý công việc đơn giản, hiệu quả</p>
        </div>
        """, unsafe_allow_html=True)

def render_user_badge(user):
    initial = (user.get("name") or user.get("email") or "U")[0].upper()
    st.markdown(f"""
    <div class="user-badge">
        <div class="avatar">{initial}</div>
        <div>
            <div class="name">{user.get("name", "")}</div>
            <div class="email">{user.get("email", "")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_stats(tasks):
    total = len(tasks)
    done  = sum(1 for t in tasks if t.get("completed"))
    left  = total - done
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box stat-total">
            <div class="stat-num">{total}</div>
            <div class="stat-label">Tổng task</div>
        </div>
        <div class="stat-box stat-done">
            <div class="stat-num">{done}</div>
            <div class="stat-label">Hoàn thành</div>
        </div>
        <div class="stat-box stat-left">
            <div class="stat-num">{left}</div>
            <div class="stat-label">Còn lại</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_filter_sort():
    c_filter, c_sort = st.columns(2)
    with c_filter:
        filter_opt = st.selectbox("Lọc trạng thái:", ["Tất cả", "Chưa xong", "Hoàn thành"])
    with c_sort:
        sort_opt = st.selectbox("Sắp xếp theo:", ["Mức độ ưu tiên", "Hạn chót gần nhất"])
    return filter_opt, sort_opt
