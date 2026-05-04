import streamlit as st
import streamlit.components.v1 as components
import requests
import pyrebase
import json
import os
from PIL import Image
from datetime import datetime
from streamlit_cookies_controller import CookieController
from themes import THEMES, get_theme_css

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
for key in ["user", "id_token", "tasks", "show_add", "edit_task_id"]:
    if key not in st.session_state:
        st.session_state[key] = None if key not in ["show_add"] else False
if st.session_state.tasks is None:
    st.session_state.tasks = []

# Create a global session for connection pooling
if "http_session" not in st.session_state:
    st.session_state.http_session = requests.Session()

# ── Helpers ───────────────────────────────────────────────────────────────────
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

def format_date(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.astimezone().strftime("%d/%m %H:%M")
    except:
        return ""

def priority_badge(p):
    return f'<span class="badge badge-{p}">{p}</span>'

# ── Auto-login with Cookies ──
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

# ── Theme Picker ─────────────────────────────────────────────────────────────
# ── Theme Picker ─────────────────────────────────────────────────────────────
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


# ── Hero ─────────────────────────────────────────────────────────────────────
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
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
                if st.button("Đăng nhập", type="primary", width="stretch"):
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
                st.markdown('<div class="google-btn-wrapper">', unsafe_allow_html=True)
                google_res = _auth_component(config=load_firebase_config(), key="google_login_btn")
                st.markdown('</div>', unsafe_allow_html=True)

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
                if st.button("Tạo tài khoản", type="primary", width="stretch"):
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
    col_add, col_refresh, col_logout = st.columns([2.2, 1.4, 1.4], gap="small")
    with col_add:
        if st.button("＋ Thêm task mới", type="primary", width="stretch"):
            st.session_state.show_add = not st.session_state.show_add
    with col_refresh:
        st.markdown('<div class="icon-refresh"></div>', unsafe_allow_html=True)
        if st.button("Làm mới", width="stretch", help="Làm mới danh sách"):
            load_tasks()
            st.rerun()
    with col_logout:
        st.markdown('<div class="icon-logout"></div>', unsafe_allow_html=True)
        if st.button("Đăng xuất", width="stretch", help="Đăng xuất"):
            controller.remove('auth_token')
            for k in ["user", "id_token", "tasks", "show_add", "edit_task_id"]:
                st.session_state[k] = None if k not in ["show_add"] else False
            st.session_state.tasks = []
            st.rerun()

    if st.session_state.show_add:
        st.markdown('<p class="section-title">✏️ Task mới</p>', unsafe_allow_html=True)
        title = st.text_input("Tiêu đề *", placeholder="Ví dụ: Ôn thi môn Toán")
        desc  = st.text_area("Mô tả (tuỳ chọn)", placeholder="Thêm ghi chú...", height=80)
        c_pri, c_date, c_time = st.columns([2, 1.5, 1.5])
        with c_pri:
            priority = st.selectbox("Mức độ ưu tiên", ["medium", "high", "low"],
                                    format_func=lambda x: {"high": "🔴 Cao", "medium": "🟠 Trung bình", "low": "🟢 Thấp"}[x])
        with c_date:
            deadline_date = st.date_input("Hạn chót (ngày)", value=None)
        with c_time:
            deadline_time = st.time_input("Giờ", value=None)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Tạo task", type="primary", width="stretch"):
                if title.strip():
                    payload = {"title": title.strip(), "description": desc.strip(), "priority": priority}
                    if deadline_date:
                        if deadline_time:
                            payload["deadline"] = datetime.combine(deadline_date, deadline_time).isoformat()
                        else:
                            payload["deadline"] = deadline_date.isoformat()
                    resp = api("post", "/tasks/", json=payload)
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
            if st.button("Huỷ", width="stretch"):
                st.session_state.show_add = False
                st.rerun()

    # ── Filter and Sort ──
    c_filter, c_sort = st.columns(2)
    with c_filter:
        filter_opt = st.selectbox("Lọc trạng thái:", ["Tất cả", "Chưa xong", "Hoàn thành"])
    with c_sort:
        sort_opt = st.selectbox("Sắp xếp theo:", ["Mức độ ưu tiên", "Hạn chót gần nhất"])

    filtered = tasks.copy()
    if filter_opt == "Chưa xong":
        filtered = [t for t in filtered if not t.get("completed")]
    elif filter_opt == "Hoàn thành":
        filtered = [t for t in filtered if t.get("completed")]

    # Sort tasks: created_at descending -> user choice -> completed
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

            # Handle Edit Mode
            if st.session_state.get("edit_task_id") == tid:
                edit_title = st.text_input("Tiêu đề", value=task["title"], key=f"edit_title_{tid}")
                edit_desc = st.text_area("Mô tả", value=task.get("description", ""), key=f"edit_desc_{tid}", height=80)
                
                c_pri, c_date, c_time = st.columns([2, 1.5, 1.5])
                with c_pri:
                    idx = ["medium", "high", "low"].index(priority) if priority in ["medium", "high", "low"] else 0
                    edit_prio = st.selectbox("Mức độ ưu tiên", ["medium", "high", "low"], index=idx,
                                             format_func=lambda x: {"high": "🔴 Cao", "medium": "🟠 Trung bình", "low": "🟢 Thấp"}[x],
                                             key=f"edit_prio_{tid}")
                with c_date:
                    default_date = None
                    default_time = None
                    if task.get("deadline"):
                        try:
                            d_dt = datetime.fromisoformat(task["deadline"].replace("Z", "+00:00"))
                            default_date = d_dt.date()
                            if "T" in task["deadline"]:
                                default_time = d_dt.time()
                        except:
                            pass
                    edit_date = st.date_input("Hạn chót (ngày)", value=default_date, key=f"edit_date_{tid}")
                with c_time:
                    edit_time = st.time_input("Giờ", value=default_time, key=f"edit_time_{tid}")
                
                c_save, c_cancel = st.columns(2)
                with c_save:
                    if st.button("💾 Lưu", key=f"save_{tid}", type="primary", width="stretch"):
                        if edit_title.strip():
                            payload = {
                                "title": edit_title.strip(),
                                "description": edit_desc.strip(),
                                "priority": edit_prio,
                            }
                            if edit_date:
                                if edit_time:
                                    payload["deadline"] = datetime.combine(edit_date, edit_time).isoformat()
                                else:
                                    payload["deadline"] = edit_date.isoformat()
                            else:
                                payload["deadline"] = ""
                            
                            resp = api("patch", f"/tasks/{tid}", json=payload)
                            if resp and resp.status_code == 200:
                                st.session_state.edit_task_id = None
                                for t in st.session_state.tasks:
                                    if t["id"] == tid:
                                        t.update(payload)
                                st.rerun()
                        else:
                            st.warning("Tiêu đề không được để trống")
                with c_cancel:
                    if st.button("Huỷ", key=f"cancel_{tid}", width="stretch"):
                        st.session_state.edit_task_id = None
                        st.rerun()
                continue

            done_cls  = "done" if completed else ""
            title_cls = "done-text" if completed else ""

            desc_html = ""
            if task.get("description"):
                safe_desc = str(task["description"]).replace('\n', '<br>')
                desc_html = f"<div class='task-desc'>{safe_desc}</div>"

            deadline_html = ""
            if task.get("deadline"):
                try:
                    d_dt = datetime.fromisoformat(task["deadline"].replace("Z", "+00:00"))
                    if "T" in task["deadline"]:
                        d_str = d_dt.strftime("%d/%m/%Y %H:%M")
                    else:
                        d_str = d_dt.strftime("%d/%m/%Y")
                    deadline_html = f'<span class="task-date" style="color: #ef4444; margin-left: 10px;">⏳ Hạn: {d_str}</span>'
                except:
                    pass

            html_str = f"""
            <div class="task-item {done_cls}">
                <div class="task-title {title_cls}">{task["title"]}</div>
                {desc_html}
                <div class="task-meta">
                    {priority_badge(priority)}
                    <span class="task-date">{created}</span>
                    {deadline_html}
                </div>
            </div>
            """
            st.markdown(html_str.replace('\n', ''), unsafe_allow_html=True)

            c1, c2, c3 = st.columns([4, 3, 3])
            with c1:
                label = "Bỏ hoàn thành" if completed else "Đánh dấu xong"
                st.markdown('<div class="icon-done"></div>', unsafe_allow_html=True)
                if st.button(label, key=f"done_{tid}", width="stretch"):
                    resp = api("patch", f"/tasks/{tid}", json={"completed": not completed})
                    if resp and resp.status_code == 200:
                        for t in st.session_state.tasks:
                            if t["id"] == tid:
                                t["completed"] = not completed
                        st.rerun()
            with c2:
                st.markdown('<div class="icon-edit"></div>', unsafe_allow_html=True)
                if st.button("Sửa", key=f"edit_{tid}", width="stretch"):
                    st.session_state.edit_task_id = tid
                    st.rerun()
            with c3:
                st.markdown('<div class="icon-delete"></div>', unsafe_allow_html=True)
                if st.button("Xoá", key=f"del_{tid}", width="stretch"):
                    resp = api("delete", f"/tasks/{tid}")
                    if resp and resp.status_code == 200:
                        st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != tid]
                        st.rerun()
