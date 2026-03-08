import streamlit as st
import requests
from datetime import datetime, time
import pytz

pk_tz = pytz.timezone('Asia/Karachi')
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Reminder Bot",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

dark = st.session_state.dark_mode

if dark:
    bg          = "#0d0d0d"
    card        = "#161616"
    card2       = "#1c1c1c"
    border      = "#2a2a2a"
    text        = "#f0f0f0"
    subtext     = "#777777"
    input_bg    = "#1e1e1e"
    input_text  = "#f0f0f0"
    input_border= "#333333"
    accent      = "#6c63ff"
    accent2     = "#a78bfa"
    tag_bg      = "#1e1a3a"
    btn_text    = "#ffffff"
else:
    bg          = "#f0f0f6"
    card        = "#ffffff"
    card2       = "#f9f9fc"
    border      = "#e2e2ee"
    text        = "#111827"
    subtext     = "#6b7280"
    input_bg    = "#ffffff"
    input_text  = "#111827"
    input_border= "#d1d5db"
    accent      = "#6c63ff"
    accent2     = "#a78bfa"
    tag_bg      = "#ede9fe"
    btn_text    = "#ffffff"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}
html, body, .stApp {{
    background: {bg} !important;
    font-family: 'Outfit', sans-serif !important;
    color: {text} !important;
}}
.stApp > header, #MainMenu, footer {{ display:none !important; visibility:hidden !important; }}
.block-container {{ padding: 2.5rem 3rem !important; max-width: 1300px !important; }}

/* ── Inputs ── */
.stTextInput > div > div > input {{
    background: {input_bg} !important;
    color: {input_text} !important;
    border: 1.5px solid {input_border} !important;
    border-radius: 12px !important;
    padding: 0.65rem 1rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    caret-color: {accent} !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: {accent} !important;
    box-shadow: 0 0 0 3px {accent}33 !important;
    outline: none !important;
}}
.stTextInput > div > div > input::placeholder {{ color: {subtext} !important; opacity:0.8 !important; }}
.stDateInput > div > div > input {{
    background: {input_bg} !important; color: {input_text} !important;
    border: 1.5px solid {input_border} !important; border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important; caret-color: {accent} !important;
}}
.stTimeInput > div > div > input {{
    background: {input_bg} !important; color: {input_text} !important;
    border: 1.5px solid {input_border} !important; border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important; caret-color: {accent} !important;
}}

/* ── Labels ── */
.stTextInput label, .stDateInput label, .stTimeInput label,
.stRadio > label, .stSelectbox label {{
    color: {subtext} !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    font-family: 'Outfit', sans-serif !important;
}}

/* ── Radio ── */
.stRadio > div {{ display:flex !important; gap:0.8rem !important; flex-direction:row !important; }}
.stRadio > div > label {{
    text-transform: none !important;
    font-size: 0.88rem !important;
    letter-spacing: 0 !important;
    color: {text} !important;
    font-weight: 500 !important;
    background: {card2} !important;
    border: 1.5px solid {input_border} !important;
    border-radius: 10px !important;
    padding: 0.45rem 1rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}}
.stRadio > div > label:has(input:checked) {{
    border-color: {accent} !important;
    background: {tag_bg} !important;
    color: {accent} !important;
}}

/* ── Buttons ── */
.stButton > button, .stFormSubmitButton > button {{
    background: {accent} !important;
    color: {btn_text} !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover {{
    background: {accent2} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px {accent}44 !important;
}}

/* ── Alerts ── */
.stSuccess > div, .stError > div, .stInfo > div, .stWarning > div {{
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: {bg}; }}
::-webkit-scrollbar-thumb {{ background: {border}; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: {accent}; }}
hr {{ border-color: {border} !important; }}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──
def check_bot_status():
    try:
        r = requests.get(f"{API_URL}/", timeout=5)
        return r.status_code == 200
    except:
        return False

def get_reminders():
    try:
        r = requests.get(f"{API_URL}/reminders", timeout=5)
        if r.status_code == 200:
            return r.json().get("reminders", [])
        return []
    except:
        return []

def set_reminder(phone, task, date, time_obj, reminder_type):
    try:
        from app.scheduler import schedule_reminder
        from app.whatsapp_handler import send_whatsapp_message
        remind_at = datetime.combine(date, time_obj)
        now_pk = datetime.now(pk_tz).replace(tzinfo=None)
        if remind_at < now_pk:
            return False, "That time has already passed! Please choose a future time."
        schedule_reminder(phone, task, remind_at, reminder_type)
        notify_via = "📞 Phone Call" if reminder_type == "call" else "📲 WhatsApp"
        confirm_msg = (
            f"✅ *Reminder Confirmed*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 *Task:* {task}\n"
            f"🗓 *Date:* {remind_at.strftime('%A, %B %d %Y')}\n"
            f"⏰ *Time:* {remind_at.strftime('%I:%M %p')}\n"
            f"📲 *Notify via:* {notify_via}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"_You'll be notified on time._ 🤖"
        )
        send_whatsapp_message(phone, confirm_msg)
        return True, "Reminder set successfully!"
    except Exception as e:
        return False, str(e)


# ── Data ──
is_online = check_bot_status()
reminders = get_reminders()
now_pk = datetime.now(pk_tz)
shadow = "0 2px 12px #00000040" if dark else "0 2px 12px #00000010"
shadow_sm = "0 2px 8px #00000030" if dark else "0 2px 8px #00000008"


# ══════════════════════════════════════
# NAVBAR
# ══════════════════════════════════════
n1, n2 = st.columns([5, 1])
with n1:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:14px; padding:1.2rem 1.8rem;
                background:{card}; border-radius:16px; border:1px solid {border};
                margin-bottom:1.5rem; box-shadow:{shadow};">
        <div style="width:40px; height:40px;
                    background:linear-gradient(135deg,{accent},{accent2});
                    border-radius:12px; display:flex; align-items:center;
                    justify-content:center; font-size:1.2rem; flex-shrink:0;">🔔</div>
        <div>
            <div style="font-size:1.2rem; font-weight:800; color:{text}; letter-spacing:-0.5px;">
                Reminder Bot
            </div>
            <div style="font-size:0.75rem; color:{subtext};">
                AI-powered WhatsApp reminder assistant
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with n2:
    st.markdown("<div style='margin-top:0.35rem'>", unsafe_allow_html=True)
    if st.button("☀️ Light" if dark else "🌙 Dark", use_container_width=True):
        toggle_theme()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════
# STATS
# ══════════════════════════════════════
s1, s2, s3 = st.columns(3, gap="medium")
status_color = "#22c55e" if is_online else "#ef4444"
status_text = "Online" if is_online else "Offline"
dot = f"<span style='display:inline-block;width:9px;height:9px;background:{status_color};border-radius:50%;margin-right:8px;{'box-shadow:0 0 8px #22c55e88' if is_online else ''}'></span>"

with s1:
    st.markdown(f"""
    <div style="background:{card}; border:1px solid {border}; border-radius:16px;
                padding:1.4rem 1.6rem; box-shadow:{shadow_sm};">
        <div style="font-size:0.7rem; color:{subtext}; font-weight:600;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">
            Bot Status
        </div>
        <div style="font-size:1.1rem; font-weight:700; color:{status_color};">
            {dot}{status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div style="background:{card}; border:1px solid {border}; border-radius:16px;
                padding:1.4rem 1.6rem; box-shadow:{shadow_sm};">
        <div style="font-size:0.7rem; color:{subtext}; font-weight:600;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">
            Active Reminders
        </div>
        <div style="font-size:1.1rem; font-weight:700; color:{text};">
            {len(reminders)}
        </div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown(f"""
    <div style="background:{card}; border:1px solid {border}; border-radius:16px;
                padding:1.4rem 1.6rem; box-shadow:{shadow_sm};">
        <div style="font-size:0.7rem; color:{subtext}; font-weight:600;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">
            Pakistan Time
        </div>
        <div style="font-size:1.1rem; font-weight:700; color:{text};">
            {now_pk.strftime('%I:%M %p')}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin:1.5rem 0'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════
# MAIN — SET REMINDER + ACTIVE REMINDERS
# ══════════════════════════════════════
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown(f"""
    <div style="font-size:1rem; font-weight:700; color:{text};
                margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
        <span style="background:{tag_bg}; color:{accent}; padding:3px 10px;
                     border-radius:8px; font-size:0.75rem; font-weight:700;">NEW</span>
        Set a Reminder
    </div>
    """, unsafe_allow_html=True)

    with st.form("reminder_form", clear_on_submit=True):
        phone = st.text_input("Phone Number", value="923000281455")
        task  = st.text_input("Task", placeholder="e.g. Drink water, Call John, Take medicine")

        col_d, col_t = st.columns(2)
        with col_d:
            date = st.date_input("Date", min_value=datetime.now().date())
        with col_t:
            selected_time = st.time_input("Time", value=time(8, 0), step=60)

        reminder_type = st.radio(
            "Notify via",
            ["message", "call"],
            horizontal=True,
            format_func=lambda x: "💬 WhatsApp" if x == "message" else "📞 Phone Call"
        )

        submitted = st.form_submit_button("Set Reminder", use_container_width=True)

        if submitted:
            if not task:
                st.error("Please enter a task!")
            else:
                success, msg = set_reminder(phone, task, date, selected_time, reminder_type)
                if success:
                    st.success(f"✅ {msg}")
                    st.balloons()
                else:
                    st.error(f"❌ {msg}")

with right:
    rc1, rc2 = st.columns([3, 1])
    with rc1:
        st.markdown(f"""
        <div style="font-size:1rem; font-weight:700; color:{text};
                    margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
            <span style="background:{tag_bg}; color:{accent}; padding:3px 10px;
                         border-radius:8px; font-size:0.75rem; font-weight:700;">LIVE</span>
            Active Reminders
        </div>
        """, unsafe_allow_html=True)
    with rc2:
        if st.button("↻ Refresh", use_container_width=True):
            st.rerun()

    # ── Fetch fresh reminders ──
    fresh_reminders = get_reminders()

    if not fresh_reminders:
        st.markdown(f"""
        <div style="background:{card}; border:1px solid {border}; border-radius:16px;
                    padding:3rem 1rem; text-align:center; box-shadow:{shadow_sm};">
            <div style="font-size:2.5rem; margin-bottom:0.8rem; opacity:0.3;">🔔</div>
            <div style="font-size:0.95rem; font-weight:600; color:{subtext};">
                No active reminders
            </div>
            <div style="font-size:0.8rem; color:{subtext}; margin-top:6px; opacity:0.7;">
                Set one using the form or send a WhatsApp message
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for r in fresh_reminders:
            job_id   = r.get("id", "")
            next_run = r.get("next_run", "")
            icon     = "📞" if "call" in job_id.lower() else "💬"
            parts    = job_id.split("_")
            task_label = " ".join(parts[1:-2]).replace("-", " ").title() if len(parts) > 3 else job_id
            notify_label = "Call" if "call" in job_id.lower() else "WhatsApp"

            try:
                dt = datetime.fromisoformat(next_run.split("+")[0].split(".")[0])
                formatted_time = dt.strftime("%I:%M %p · %A, %b %d")
            except:
                formatted_time = next_run

            st.markdown(f"""
            <div style="background:{card}; border:1px solid {border};
                        border-left:4px solid {accent}; border-radius:14px;
                        padding:1rem 1.3rem; margin-bottom:0.8rem; box-shadow:{shadow_sm};">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div style="font-size:0.95rem; font-weight:600; color:{text}; margin-bottom:4px;">
                            {task_label}
                        </div>
                        <div style="font-size:0.78rem; color:{subtext};
                                    font-family:'JetBrains Mono', monospace;">
                            ⏰ {formatted_time}
                        </div>
                    </div>
                    <div style="display:flex; flex-direction:column; align-items:flex-end; gap:4px;">
                        <span style="background:{tag_bg}; color:{accent}; padding:3px 8px;
                                     border-radius:6px; font-size:0.7rem; font-weight:700;">
                            PENDING
                        </span>
                        <span style="font-size:0.72rem; color:{subtext};">
                            {icon} {notify_label}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════
# HOW TO USE
# ══════════════════════════════════════
st.markdown(f"<hr style='border:1px solid {border}; margin:2rem 0 1.5rem'>", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size:1rem; font-weight:700; color:{text};
            margin-bottom:1.2rem; display:flex; align-items:center; gap:8px;">
    <span style="background:{tag_bg}; color:{accent}; padding:3px 10px;
                 border-radius:8px; font-size:0.75rem; font-weight:700;">GUIDE</span>
    How to Use
</div>
""", unsafe_allow_html=True)

g1, g2, g3 = st.columns(3, gap="medium")

with g1:
    st.markdown(f"""
    <div style="background:{card}; border:1px solid {border}; border-radius:16px;
                padding:1.4rem; box-shadow:{shadow_sm};">
        <div style="font-size:0.72rem; font-weight:700; color:{accent};
                    text-transform:uppercase; letter-spacing:1.2px; margin-bottom:1rem;">
            💬 English
        </div>
        <div style="padding:8px 0; border-bottom:1px solid {border};
                    font-size:0.85rem; color:{subtext};">
            Remind me to drink water at 5pm
        </div>
        <div style="padding:8px 0; border-bottom:1px solid {border};
                    font-size:0.85rem; color:{subtext};">
            Remind me to call John at 9am tomorrow
        </div>
        <div style="padding:8px 0; font-size:0.85rem; color:{subtext};">
            Set reminder for meeting on Monday 3pm
        </div>
    </div>
    """, unsafe_allow_html=True)

with g2:
    st.markdown(f"""
    <div style="background:{card}; border:1px solid {border}; border-radius:16px;
                padding:1.4rem; box-shadow:{shadow_sm};">
        <div style="font-size:0.72rem; font-weight:700; color:{accent};
                    text-transform:uppercase; letter-spacing:1.2px; margin-bottom:1rem;">
            🇵🇰 Urdu / Roman Urdu
        </div>
        <div style="padding:8px 0; border-bottom:1px solid {border};
                    font-size:0.85rem; color:{subtext};">
            Mujhe yaad dilao ke 8 baje medicine leni hai
        </div>
        <div style="padding:8px 0; border-bottom:1px solid {border};
                    font-size:0.85rem; color:{subtext};">
            Kal subah 9 baje meeting remind karna
        </div>
        <div style="padding:8px 0; font-size:0.85rem; color:{subtext};">
            Aaj raat 10 baje paani peena yaad dilana
        </div>
    </div>
    """, unsafe_allow_html=True)

with g3:
    st.markdown(f"""
    <div style="background:{card}; border:1px solid {border}; border-radius:16px;
                padding:1.4rem; box-shadow:{shadow_sm};">
        <div style="font-size:0.72rem; font-weight:700; color:{accent};
                    text-transform:uppercase; letter-spacing:1.2px; margin-bottom:1rem;">
            📞 Call Reminders
        </div>
        <div style="padding:8px 0; border-bottom:1px solid {border};
                    font-size:0.85rem; color:{subtext};">
            Call me to remind about meeting at 5pm
        </div>
        <div style="padding:8px 0; border-bottom:1px solid {border};
                    font-size:0.85rem; color:{subtext};">
            Phone kar k remind karna kal 9 baje
        </div>
        <div style="padding:8px 0; font-size:0.85rem; color:{subtext};">
            Call karo jab 3 baje ho aaj
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════
# FOOTER
# ══════════════════════════════════════
st.markdown(f"""
<div style="text-align:center; padding:2rem 0 1rem; color:{subtext}; font-size:0.78rem;">
    Built with ❤️ &nbsp;·&nbsp; FastAPI &nbsp;·&nbsp;
    Groq &nbsp;·&nbsp; Green API &nbsp;·&nbsp; VAPI
</div>
""", unsafe_allow_html=True)