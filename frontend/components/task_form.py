import streamlit as st
from datetime import datetime
from utils.api_client import api, load_tasks

def render_add_task_form():
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

def render_edit_task_form(task):
    tid = task["id"]
    priority = task.get("priority", "medium")
    
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
                    # Update local state
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
