# ── Theme Definitions & CSS Generator ─────────────────────────────────────────
import base64
import os

THEMES = {
    "dark": {
        "name": "🌙 Tối",
        "bg": "linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%)",
        "hero": "linear-gradient(135deg, #a78bfa, #60a5fa, #34d399)",
        "t1": "#e2e8f0", "t2": "#94a3b8", "t3": "#64748b", "t4": "#475569",
        "s1": "rgba(255,255,255,0.04)", "s2": "rgba(255,255,255,0.03)",
        "b1": "rgba(255,255,255,0.08)", "b2": "rgba(255,255,255,0.07)",
        "bh": "rgba(167,139,250,0.3)",
        "ac": "#a78bfa",
        "ac_bg": "rgba(167,139,250,0.1)", "ac_bd": "rgba(167,139,250,0.2)",
        "ac_f": "rgba(167,139,250,0.5)", "ac_g": "rgba(167,139,250,0.1)",
        "in_bg": "rgba(255,255,255,0.05)", "in_bd": "rgba(255,255,255,0.1)",
        "dv": "rgba(255,255,255,0.08)",
        "tab_bg": "rgba(255,255,255,0.04)", "tab_bd": "rgba(255,255,255,0.08)",
        "tab_ac": "rgba(167,139,250,0.15)",
        "btn": "linear-gradient(135deg, #7c3aed, #4f46e5)",
        "btn_s": "rgba(124,58,237,0.4)",
        "done_bd": "rgba(52,211,153,0.2)",
        "st1": "#a78bfa", "st2": "#34d399", "st3": "#60a5fa",
        "av": "linear-gradient(135deg, #a78bfa, #60a5fa)",
    },
    "ocean": {
        "name": "🌊 Biển",
        "bg": "linear-gradient(135deg, #0c1929 0%, #0a2540 50%, #0d3b66 100%)",
        "hero": "linear-gradient(135deg, #38bdf8, #0ea5e9, #06b6d4)",
        "t1": "#e0f2fe", "t2": "#7dd3fc", "t3": "#38bdf8", "t4": "#0c4a6e",
        "s1": "rgba(14,165,233,0.08)", "s2": "rgba(14,165,233,0.05)",
        "b1": "rgba(14,165,233,0.15)", "b2": "rgba(14,165,233,0.1)",
        "bh": "rgba(56,189,248,0.3)",
        "ac": "#38bdf8",
        "ac_bg": "rgba(56,189,248,0.1)", "ac_bd": "rgba(56,189,248,0.2)",
        "ac_f": "rgba(56,189,248,0.5)", "ac_g": "rgba(56,189,248,0.1)",
        "in_bg": "rgba(14,165,233,0.08)", "in_bd": "rgba(14,165,233,0.15)",
        "dv": "rgba(56,189,248,0.15)",
        "tab_bg": "rgba(14,165,233,0.08)", "tab_bd": "rgba(14,165,233,0.15)",
        "tab_ac": "rgba(56,189,248,0.15)",
        "btn": "linear-gradient(135deg, #0284c7, #0369a1)",
        "btn_s": "rgba(2,132,199,0.4)",
        "done_bd": "rgba(52,211,153,0.2)",
        "st1": "#38bdf8", "st2": "#34d399", "st3": "#818cf8",
        "av": "linear-gradient(135deg, #38bdf8, #06b6d4)",
    },
    "white": {
        "name": "⚪ Sáng",
        "bg": "#f8fafc",
        "hero": "linear-gradient(135deg, #2563eb, #3b82f6, #60a5fa)",
        "t1": "#000000", "t2": "#1e293b", "t3": "#64748b", "t4": "#94a3b8",
        "s1": "#ffffff", "s2": "#f1f5f9",
        "b1": "#e2e8f0", "b2": "#cbd5e1",
        "bh": "rgba(59,130,246,0.5)",
        "ac": "#3b82f6",
        "ac_bg": "rgba(59,130,246,0.1)", "ac_bd": "rgba(59,130,246,0.2)",
        "ac_f": "rgba(59,130,246,0.5)", "ac_g": "rgba(59,130,246,0.1)",
        "in_bg": "#ffffff", "in_bd": "#cbd5e1",
        "dv": "#e2e8f0",
        "tab_bg": "#f8fafc", "tab_bd": "#e2e8f0",
        "tab_ac": "rgba(59,130,246,0.1)",
        "btn": "linear-gradient(135deg, #2563eb, #3b82f6)",
        "btn_s": "rgba(59,130,246,0.4)",
        "done_bd": "rgba(52,211,153,0.4)",
        "st1": "#3b82f6", "st2": "#10b981", "st3": "#6366f1",
        "av": "linear-gradient(135deg, #2563eb, #3b82f6)",
    },
}


def get_svg_data_uri(filename):
    """Read SVG file and return base64 data URI."""
    filepath = os.path.join(os.path.dirname(__file__), "assets", filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                svg_content = f.read()
            # Basic cleanup to ensure it works well in CSS
            b64 = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
            return f"data:image/svg+xml;base64,{b64}"
        except:
            return ""
    return ""


def get_theme_css(theme_name="dark"):
    """Generate complete CSS for the given theme."""
    t = THEMES.get(theme_name, THEMES["dark"])
    
    # Load icons
    icons = {
        "refresh": get_svg_data_uri("refresh.svg"),
        "logout": get_svg_data_uri("logout.svg"),
        "done": get_svg_data_uri("done.svg"),
        "edit": get_svg_data_uri("edit.svg"),
        "delete": get_svg_data_uri("deletetask.svg"),
    }

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* {{ font-family: 'Sora', sans-serif; }}

/* Hide Streamlit defaults */
#MainMenu, footer, header, .stAppToolbar, [data-testid="stStatusWidget"] {{ 
    display: none !important;
    visibility: hidden !important; 
}}
.block-container {{ padding-top: 1rem; padding-bottom: 2rem; max-width: 720px; }}


/* ── Background ── */
.stApp {{
    background: {t["bg"]};
    min-height: 100vh;
}}

/* ── Hero header ── */
.hero {{
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}}
.hero h1 {{
    font-size: 3rem;
    font-weight: 700;
    background: {t["hero"]};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -1px;
}}
.hero p {{
    color: {t["t2"]};
    font-size: 1rem;
    margin-top: 0.4rem;
}}

/* ── Card ── */
.card {{
    background: {t["s1"]};
    border: 1px solid {t["b1"]};
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}}

/* ── User badge ── */
.user-badge {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: {t["ac_bg"]};
    border: 1px solid {t["ac_bd"]};
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin-bottom: 1.5rem;
}}
.user-badge .name {{
    color: {t["t1"]};
    font-weight: 500;
    font-size: 0.9rem;
}}
.user-badge .email {{
    color: {t["t3"]};
    font-size: 0.75rem;
}}
.avatar {{
    width: 36px; height: 36px;
    border-radius: 50%;
    background: {t["av"]};
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 700; font-size: 1rem;
    flex-shrink: 0;
}}

/* ── Stats row ── */
.stats-row {{
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}}
.stat-box {{
    flex: 1;
    background: {t["s1"]};
    border: 1px solid {t["b1"]};
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}}
.stat-num {{
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}}
.stat-label {{
    font-size: 0.7rem;
    color: {t["t3"]};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.2rem;
}}
.stat-total .stat-num {{ color: {t["st1"]}; }}
.stat-done .stat-num  {{ color: {t["st2"]}; }}
.stat-left .stat-num  {{ color: {t["st3"]}; }}

/* ── Task item ── */
.task-item {{
    background: {t["s2"]};
    border: 1px solid {t["b2"]};
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.2s;
}}
.task-item:hover {{ border-color: {t["bh"]}; }}
.task-item.done {{
    opacity: 0.5;
    border-color: {t["done_bd"]};
}}
.task-title {{
    color: {t["t1"]};
    font-weight: 500;
    font-size: 0.95rem;
}}
.task-title.done-text {{
    text-decoration: line-through;
    color: {t["t3"]};
}}
.task-desc {{
    color: {t["t3"]};
    font-size: 0.8rem;
    margin-top: 0.2rem;
}}
.task-meta {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
}}
.badge {{
    font-size: 0.65rem;
    padding: 0.15rem 0.5rem;
    border-radius: 20px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.badge-high   {{ background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3); }}
.badge-medium {{ background: rgba(251,146,60,0.15); color: #fb923c; border: 1px solid rgba(251,146,60,0.3); }}
.badge-low    {{ background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }}
.task-date {{ color: {t["t4"]}; font-size: 0.7rem; margin-left: auto; }}

/* ── Section title ── */
.section-title {{
    color: {t["t2"]};
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 1.5rem 0 0.75rem;
}}

/* ── Login form ── */
.login-box {{
    max-width: 400px;
    margin: 0 auto;
}}
.login-title {{
    color: {t["t1"]};
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
}}
.login-sub {{
    color: {t["t3"]};
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
}}
.divider {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1rem 0;
    color: {t["t4"]};
    font-size: 0.8rem;
}}
.divider::before, .divider::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: {t["dv"]};
}}

/* ── Theme switcher ── */
.theme-switcher {{
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    background: {t["s2"]};
    border-radius: 12px;
    padding: 0.4rem;
    width: fit-content;
    margin-left: auto;
    border: 1px solid {t["b1"]};
}}
.theme-switcher [data-testid="column"] {{
    width: 60px !important;
    flex: none !important;
}}
.theme-switcher button {{
    height: 40px !important;
    padding: 0 !important;
    font-size: 1.2rem !important;
    border-radius: 8px !important;
}}
.theme-switcher button[kind="primary"] {{
    background: {t["ac_bg"]} !important;
    border: 1px solid {t["ac"]} !important;
    box-shadow: 0 0 10px {t["ac_g"]} !important;
}}



/* Streamlit widget overrides */
div[data-testid="stTextInput"] div[data-baseweb="input"],
div[data-testid="stTextArea"] div[data-baseweb="textarea"],
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stDateInput"] div[data-baseweb="input"],
div[data-testid="stTimeInput"] > div > div,
div[data-baseweb="select"] > div,
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"], [data-baseweb="popover"], [data-baseweb="popover"] > div {{
    background: {t["in_bg"]} !important;
    background-color: {t["in_bg"]} !important;
    border: 1px solid {t["in_bd"]} !important;
    border-radius: 10px !important;
}}




[data-baseweb="input"] input, 
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] div, 
[data-baseweb="select"] span,
[data-testid="stTimeInput"] input {{
    color: {t["t1"]} !important;
    -webkit-text-fill-color: {t["t1"]} !important;
    font-weight: 500 !important;
}}


/* Placeholder styling */
::placeholder {{
    color: #94a3b8 !important; /* Light gray (slate-400) */
    opacity: 0.8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}}
input::placeholder {{
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stDateInput > div > div > input:focus,
.stTimeInput > div > div > input:focus,
[data-baseweb="input"]:focus-within {{
    border-color: {t["ac_f"]} !important;
    box-shadow: 0 0 0 2px {t["ac_g"]} !important;
}}
[data-baseweb="popover"] > div, [data-baseweb="menu"], [data-baseweb="calendar"] {{
    background: #1a1a2e !important;
    background-color: #1a1a2e !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}}
/* Dark Calendar style for all themes */
[data-baseweb="calendar"] *, [role="gridcell"] {{
    background: transparent !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}}
[data-baseweb="calendar"] [aria-selected="true"], 
[data-baseweb="calendar"] [aria-selected="true"] * {{
    background: {t["ac"]} !important;
    background-color: {t["ac"]} !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
}}
[data-baseweb="calendar"] [aria-disabled="true"] {{
    opacity: 0.2 !important;
}}




label {{ color: {t["t2"]} !important; font-size: 0.85rem !important; }}
/* Universal secondary button override */
.stButton > button, 
button[data-testid*="BaseButton-secondary"],
.stButton > button[kind="secondary"],
.stButton > button[kind="primary"] {{
    height: 38px !important;
    min-height: 38px !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    transition: all 0.2s !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

.stButton > button[kind="secondary"],
button[data-testid*="BaseButton-secondary"] {{
    background: {t["in_bg"]} !important;
    background-color: {t["in_bg"]} !important;
    border: 1px solid {t["b1"]} !important;
    color: {t["t1"]} !important;
    -webkit-text-fill-color: {t["t1"]} !important;
    font-weight: 500 !important;
}}

.stButton > button *, 
button[data-testid*="BaseButton-secondary"] *,
button[data-testid="baseButton-secondary"] * {{
    color: inherit !important;
    -webkit-text-fill-color: inherit !important;
}}
.stButton > button[kind="primary"] {{
    background: {t["btn"]} !important;
    border: none !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    font-weight: 600 !important;
}}

/* Google Login Button prominence */
div[data-testid="stVerticalBlock"] > div:has(button[key="google_login_btn"]) button,
.google-btn-wrapper button {{
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
}}

.stButton > button:hover {{
    border-color: {t["ac"]} !important;
    color: {t["ac"]} !important;
    -webkit-text-fill-color: {t["ac"]} !important;
    transform: translateY(-1px);
}}
.stButton > button[kind="primary"]:hover {{
    box-shadow: 0 4px 20px {t["btn_s"]} !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
}}
.stCheckbox > label {{ color: {t["t1"]} !important; }}
.stAlert {{ border-radius: 10px !important; }}
.stTabs [data-baseweb="tab-list"] {{
    background: {t["tab_bg"]};
    border-radius: 10px;
    border: 1px solid {t["tab_bd"]};
    gap: 0;
    display: flex;
    width: 100%;
}}
.stTabs [data-baseweb="tab"] {{
    flex: 1;
    display: flex;
    justify-content: center;
    color: {t["t3"]};
    border-radius: 8px;
    font-weight: 500;
}}
.stTabs [aria-selected="true"] {{
    background: {t["tab_ac"]} !important;
    color: {t["ac"]} !important;
}}

/* ── Icon Injection ── */
/* Hide the marker containers entirely so they don't take up space/gaps */
div.element-container:has([class^="icon-"]) {{
    display: none !important;
}}


/* Target the container containing the marker and the following button */
div.element-container:has(.icon-refresh) + div.element-container button,
div.element-container:has(.icon-logout) + div.element-container button,
div.element-container:has(.icon-done) + div.element-container button,
div.element-container:has(.icon-edit) + div.element-container button,
div.element-container:has(.icon-delete) + div.element-container button {{
    background-repeat: no-repeat !important;
    background-position: 10px center !important;
    background-size: 16px 16px !important;
    padding-left: 32px !important;
}}


div.element-container:has(.icon-refresh) + div.element-container button {{ background-image: url('{icons["refresh"]}') !important; }}
div.element-container:has(.icon-logout) + div.element-container button {{ background-image: url('{icons["logout"]}') !important; }}
div.element-container:has(.icon-done) + div.element-container button {{ background-image: url('{icons["done"]}') !important; }}
div.element-container:has(.icon-edit) + div.element-container button {{ background-image: url('{icons["edit"]}') !important; }}
div.element-container:has(.icon-delete) + div.element-container button {{ background-image: url('{icons["delete"]}') !important; }}

/* Adjustments for icons in narrow columns (task list) */
.stColumn div.element-container button {{
    font-size: 0.8rem !important;
    background-size: 14px 14px !important;
    padding-left: 28px !important;
}}


</style>
"""
