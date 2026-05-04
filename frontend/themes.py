# ── Theme Definitions & CSS Generator ─────────────────────────────────────────

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
}


def get_theme_css(theme_name="dark"):
    """Generate complete CSS for the given theme."""
    t = THEMES.get(theme_name, THEMES["dark"])
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* {{ font-family: 'Sora', sans-serif; }}

/* Hide Streamlit defaults */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem; padding-bottom: 2rem; max-width: 720px; }}

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
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}}
.theme-btn {{
    width: 32px; height: 32px;
    border-radius: 50%;
    border: 2px solid {t["b1"]};
    cursor: pointer;
    transition: all 0.2s;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
}}
.theme-btn:hover {{ transform: scale(1.15); }}
.theme-btn.active {{ border-color: {t["ac"]}; box-shadow: 0 0 8px {t["ac_g"]}; }}

/* Streamlit widget overrides */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {{
    background: {t["in_bg"]} !important;
    border: 1px solid {t["in_bd"]} !important;
    border-radius: 10px !important;
    color: {t["t1"]} !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {t["ac_f"]} !important;
    box-shadow: 0 0 0 2px {t["ac_g"]} !important;
}}
label {{ color: {t["t2"]} !important; font-size: 0.85rem !important; }}
.stButton > button {{
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}}
.stButton > button[kind="primary"] {{
    background: {t["btn"]} !important;
    border: none !important;
    color: white !important;
}}
.stButton > button[kind="primary"]:hover {{
    transform: translateY(-1px);
    box-shadow: 0 4px 20px {t["btn_s"]} !important;
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
</style>
"""
