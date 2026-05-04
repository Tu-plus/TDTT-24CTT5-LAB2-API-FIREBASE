import streamlit as st
from datetime import datetime
from utils.api_client import api
from utils.formatters import format_date, priority_badge

def render_task_item(task):
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
