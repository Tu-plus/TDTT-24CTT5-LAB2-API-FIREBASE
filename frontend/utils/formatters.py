from datetime import datetime

def format_date(iso_str):
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.astimezone().strftime("%d/%m %H:%M")
    except:
        return ""

def priority_badge(p):
    return f'<span class="badge badge-{p}">{p}</span>'
