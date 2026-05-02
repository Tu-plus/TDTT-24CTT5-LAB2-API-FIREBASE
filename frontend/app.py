import streamlit as st
import streamlit.components.v1 as components
import requests
import pyrebase
import json
import os
from PIL import Image
from datetime import datetime
from streamlit_cookies_controller import CookieController

# ── Page config ──────────────────────────────────────────────────────────────
favicon_path = os.path.join(os.path.dirname(__file__), "favicon.png")
icon = Image.open(favicon_path) if os.path.exists(favicon_path) else "✅"

st.set_page_config(
    page_title="TaskFlow",
    page_icon=icon,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* { font-family: 'Sora', sans-serif; }

/* Hide Streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 720px; }

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -1px;
}
.hero p {
    color: #94a3b8;
    font-size: 1rem;
    margin-top: 0.4rem;
}

/* ── Card ── */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}

/* ── User badge ── */
.user-badge {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: rgba(167,139,250,0.1);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin-bottom: 1.5rem;
}
.user-badge .name {
    color: #e2e8f0;
    font-weight: 500;
    font-size: 0.9rem;
}
.user-badge .email {
    color: #64748b;
    font-size: 0.75rem;
}
.avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 700; font-size: 1rem;
    flex-shrink: 0;
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.stat-box {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.stat-num {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.stat-label {
    font-size: 0.7rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.2rem;
}
.stat-total .stat-num { color: #a78bfa; }
.stat-done .stat-num  { color: #34d399; }
.stat-left .stat-num  { color: #60a5fa; }

/* ── Task item ── */
.task-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.2s;
}
.task-item:hover { border-color: rgba(167,139,250,0.3); }
.task-item.done {
    opacity: 0.5;
    border-color: rgba(52,211,153,0.2);
}
.task-title {
    color: #e2e8f0;
    font-weight: 500;
    font-size: 0.95rem;
}
.task-title.done-text {
    text-decoration: line-through;
    color: #64748b;
}
.task-desc {
    color: #64748b;
    font-size: 0.8rem;
    margin-top: 0.2rem;
}
.task-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
.badge {
    font-size: 0.65rem;
    padding: 0.15rem 0.5rem;
    border-radius: 20px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-high   { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.badge-medium { background: rgba(251,146,60,0.15); color: #fb923c; border: 1px solid rgba(251,146,60,0.3); }
.badge-low    { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.task-date { color: #475569; font-size: 0.7rem; margin-left: auto; }

/* ── Section title ── */
.section-title {
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 1.5rem 0 0.75rem;
}

/* ── Login form ── */
.login-box {
    max-width: 400px;
    margin: 0 auto;
}
.login-title {
    color: #e2e8f0;
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
}
.login-sub {
    color: #64748b;
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
}
.divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1rem 0;
    color: #475569;
    font-size: 0.8rem;
}
.divider::before, .divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.08);
}

/* Streamlit widget overrides */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(167,139,250,0.5) !important;
    box-shadow: 0 0 0 2px rgba(167,139,250,0.1) !important;
}
label { color: #94a3b8 !important; font-size: 0.85rem !important; }
.stButton > button {
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: none !important;
    color: white !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
}
.stCheckbox > label { color: #e2e8f0 !important; }
.stAlert { border-radius: 10px !important; }
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.08);
    gap: 0;
    display: flex;
    width: 100%;
}
.stTabs [data-baseweb="tab"] {
    flex: 1;
    display: flex;
    justify-content: center;
    color: #64748b;
    border-radius: 8px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: rgba(167,139,250,0.15) !important;
    color: #a78bfa !important;
}
</style>
""", unsafe_allow_html=True)

# ── Config ────────────────────────────────────────────────────────────────────
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Load Firebase web config from env or file
def load_firebase_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "firebase-web-config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    # Fallback: read from env variables
    return {
        "apiKey":            os.getenv("FIREBASE_API_KEY", ""),
        "authDomain":        os.getenv("FIREBASE_AUTH_DOMAIN", ""),
        "projectId":         os.getenv("FIREBASE_PROJECT_ID", ""),
        "storageBucket":     os.getenv("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId":             os.getenv("FIREBASE_APP_ID", ""),
        "databaseURL":       "",
    }

@st.cache_resource
def init_firebase():
    config = load_firebase_config()
    firebase = pyrebase.initialize_app(config)
    return firebase.auth()

# ── Custom Component ──────────────────────────────────────────────────────────
_auth_component = components.declare_component(
    "google_login",
    path=os.path.join(os.path.dirname(__file__), "auth_component")
)

controller = CookieController()

# ── Session state ─────────────────────────────────────────────────────────────
for key in ["user", "id_token", "tasks", "show_add"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "show_add" else False
if st.session_state.tasks is None:
    st.session_state.tasks = []

# ── Helpers ───────────────────────────────────────────────────────────────────
def api(method, path, **kwargs):
    headers = kwargs.pop("headers", {})
    if st.session_state.id_token:
        headers["Authorization"] = f"Bearer {st.session_state.id_token}"
    url = f"{BACKEND_URL}{path}"
    try:
        resp = getattr(requests, method)(url, headers=headers, timeout=10, **kwargs)
        return resp
    except Exception as e:
        st.error(f"Không kết nối được backend: {e}")
        return None

def load_tasks():
    resp = api("get", "/tasks/")
    if resp and resp.status_code == 200:
        st.session_state.tasks = resp.json()

def format_date(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m %H:%M")
    except:
        return ""

def priority_badge(p):
    return f'<span class="badge badge-{p}">{p}</span>'

# ── Auto-login with Cookies ──
cookie_token = controller.get('auth_token')
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

# ── Hero ─────────────────────────────────────────────────────────────────────
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
if os.path.exists(logo_path):
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.image(logo_path, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="hero">
        <h1>✅ TaskFlow</h1>
        <p>Quản lý công việc đơn giản, hiệu quả</p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.user:
    try:
        auth_client = init_firebase()
        firebase_ok = True
    except Exception as e:
        st.error(f"⚠️ Chưa cấu hình Firebase: {e}\n\nVui lòng xem hướng dẫn trong README.md")
        firebase_ok = False

    if firebase_ok:
        _, col, _ = st.columns([1, 5, 1])
        with col:
            st.markdown('<p class="login-title" style="text-align: center;">Đăng nhập</p>', unsafe_allow_html=True)
            st.markdown('<p class="login-sub" style="text-align: center;">Dùng tài khoản Email/Password để tiếp tục</p>', unsafe_allow_html=True)
    
            tab_login, tab_register = st.tabs(["🔑 Đăng nhập", "📝 Đăng ký"])
    
            with tab_login:
                email = st.text_input("Email", key="login_email", placeholder="you@example.com")
                password = st.text_input("Mật khẩu", type="password", key="login_pass", placeholder="••••••••")
                if st.button("Đăng nhập", type="primary", use_container_width=True):
                    if email and password:
                        try:
                            result = auth_client.sign_in_with_email_and_password(email, password)
                            st.session_state.id_token = result["idToken"]
                            controller.set('auth_token', result["idToken"])
                            resp = api("get", "/auth/me")
                            if resp and resp.status_code == 200:
                                st.session_state.user = resp.json()
                                load_tasks()
                                st.rerun()
                            else:
                                st.error("Lỗi xác thực với backend")
                        except Exception as e:
                            st.error("Email hoặc mật khẩu không đúng")
                    else:
                        st.warning("Vui lòng nhập đầy đủ thông tin")

                st.markdown('<div class="divider">HOẶC</div>', unsafe_allow_html=True)
                google_res = _auth_component(config=load_firebase_config(), key="google_login_btn")
                if google_res:
                    if "token" in google_res:
                        st.session_state.id_token = google_res["token"]
                        controller.set('auth_token', google_res["token"])
                        resp = api("get", "/auth/me")
                        if resp and resp.status_code == 200:
                            st.session_state.user = resp.json()
                            load_tasks()
                            st.rerun()
                        else:
                            st.error("Lỗi xác thực với backend")
                    elif "error" in google_res:
                        st.error(f"Lỗi đăng nhập Google: {google_res['error']}")

    
            with tab_register:
                r_email = st.text_input("Email", key="reg_email", placeholder="you@example.com")
                r_pass  = st.text_input("Mật khẩu", type="password", key="reg_pass", placeholder="Tối thiểu 6 ký tự")
                r_pass2 = st.text_input("Xác nhận mật khẩu", type="password", key="reg_pass2", placeholder="••••••••")
                if st.button("Tạo tài khoản", type="primary", use_container_width=True):
                    if r_email and r_pass and r_pass2:
                        if r_pass != r_pass2:
                            st.error("Mật khẩu không khớp")
                        elif len(r_pass) < 6:
                            st.error("Mật khẩu phải có ít nhất 6 ký tự")
                        else:
                            try:
                                auth_client.create_user_with_email_and_password(r_email, r_pass)
                                st.success("✅ Tạo tài khoản thành công! Hãy đăng nhập.")
                            except Exception as e:
                                st.error("Email đã tồn tại hoặc không hợp lệ")
                    else:
                        st.warning("Vui lòng nhập đầy đủ thông tin")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════════
else:
    user = st.session_state.user
    tasks = st.session_state.tasks

    # ── User badge ──
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

    # ── Stats ──
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

    # ── Add task form ──
    col_add, col_refresh, col_logout = st.columns([3, 1, 1])
    with col_add:
        if st.button("＋ Thêm task mới", type="primary", use_container_width=True):
            st.session_state.show_add = not st.session_state.show_add
    with col_refresh:
        if st.button("🔄", use_container_width=True, help="Làm mới danh sách"):
            load_tasks()
            st.rerun()
    with col_logout:
        if st.button("🚪", use_container_width=True, help="Đăng xuất"):
            controller.remove('auth_token')
            for k in ["user", "id_token", "tasks", "show_add"]:
                st.session_state[k] = None if k != "show_add" else False
            st.session_state.tasks = []
            st.rerun()

    if st.session_state.show_add:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">✏️ Task mới</p>', unsafe_allow_html=True)
        title = st.text_input("Tiêu đề *", placeholder="Ví dụ: Ôn thi môn Toán")
        desc  = st.text_area("Mô tả (tuỳ chọn)", placeholder="Thêm ghi chú...", height=80)
        priority = st.selectbox("Mức độ ưu tiên", ["medium", "high", "low"],
                                format_func=lambda x: {"high": "🔴 Cao", "medium": "🟠 Trung bình", "low": "🟢 Thấp"}[x])
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Tạo task", type="primary", use_container_width=True):
                if title.strip():
                    resp = api("post", "/tasks/", json={"title": title.strip(), "description": desc.strip(), "priority": priority})
                    if resp and resp.status_code == 200:
                        st.success("Đã thêm task!")
                        st.session_state.show_add = False
                        load_tasks()
                        st.rerun()
                    else:
                        st.error("Lỗi khi tạo task")
                else:
                    st.warning("Tiêu đề không được để trống")
        with c2:
            if st.button("Huỷ", use_container_width=True):
                st.session_state.show_add = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Filter ──
    filter_opt = st.selectbox("Lọc:", ["Tất cả", "Chưa xong", "Hoàn thành"], label_visibility="collapsed")

    filtered = tasks.copy()
    if filter_opt == "Chưa xong":
        filtered = [t for t in filtered if not t.get("completed")]
    elif filter_opt == "Hoàn thành":
        filtered = [t for t in filtered if t.get("completed")]

    # Sort tasks: created_at descending -> priority -> completed
    priority_map = {"high": 1, "medium": 2, "low": 3}
    filtered.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    filtered.sort(key=lambda x: (
        x.get("completed", False),
        priority_map.get(x.get("priority", "medium"), 2)
    ))

    # ── Task list ──
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
            tid       = task["id"]
            completed = task.get("completed", False)
            priority  = task.get("priority", "medium")
            created   = format_date(task.get("created_at", ""))

            done_cls  = "done" if completed else ""
            title_cls = "done-text" if completed else ""

            desc_html = ""
            if task.get("description"):
                safe_desc = str(task["description"]).replace('\n', '<br>')
                desc_html = f"<div class='task-desc'>{safe_desc}</div>"

            html_str = f"""
            <div class="task-item {done_cls}">
                <div class="task-title {title_cls}">{task["title"]}</div>
                {desc_html}
                <div class="task-meta">
                    {priority_badge(priority)}
                    <span class="task-date">{created}</span>
                </div>
            </div>
            """
            st.markdown(html_str.replace('\n', ''), unsafe_allow_html=True)

            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                label = "☑ Bỏ hoàn thành" if completed else "✅ Đánh dấu xong"
                if st.button(label, key=f"done_{tid}", use_container_width=True):
                    resp = api("patch", f"/tasks/{tid}", json={"completed": not completed})
                    if resp and resp.status_code == 200:
                        for t in st.session_state.tasks:
                            if t["id"] == tid:
                                t["completed"] = not completed
                        st.rerun()
            with c3:
                if st.button("🗑 Xoá", key=f"del_{tid}", use_container_width=True):
                    resp = api("delete", f"/tasks/{tid}")
                    if resp and resp.status_code == 200:
                        st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != tid]
                        st.rerun()
