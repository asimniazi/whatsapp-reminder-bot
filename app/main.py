from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import pytz
from datetime import datetime
from app.reminder_parser import parse_reminder, is_reminder_message
from app.whatsapp_handler import send_whatsapp_message, receive_webhook
from app.scheduler import schedule_reminder, get_all_reminders

load_dotenv()
app = FastAPI(title="WhatsApp Reminder Bot")
pk_tz = pytz.timezone('Asia/Karachi')

# ── Static Dashboard ──
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/index.html")

# ── Root ──
@app.get("/")
def root():
    return {"status": "online", "message": "WhatsApp Reminder Bot is running!"}

# ── API: Stats ──
@app.get("/api/stats")
def get_stats():
    reminders = get_all_reminders()
    return {
        "status": "online",
        "active_reminders": len(reminders),
        "reminders": reminders
    }

# ── API: Set Reminder ──
@app.post("/api/reminder")
async def add_reminder(request: Request):
    data          = await request.json()
    phone         = data.get("phone", "").strip()
    task          = data.get("task", "").strip()
    remind_at_str = data.get("datetime", "")
    reminder_type = data.get("reminder_type", "message")

    if not phone or not task or not remind_at_str:
        return {"status": "error", "message": "Phone, task and datetime are required."}

    try:
        remind_at = datetime.fromisoformat(remind_at_str)
        now_pk    = datetime.now(pk_tz).replace(tzinfo=None)

        if remind_at < now_pk:
            return {"status": "error", "message": "That time has already passed!"}

        schedule_reminder(phone, task, remind_at, reminder_type)

        notify_via  = "📞 Phone Call" if reminder_type == "call" else "📲 WhatsApp"
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
        return {"status": "success", "message": "Reminder set successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# ── WhatsApp Webhook ──
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(f"🌐 Raw request data: {data}")

    incoming = receive_webhook(data)
    if not incoming:
        return {"status": "ignored"}

    phone = incoming.get("phone")
    text  = incoming.get("text", "")

    if not text:
        return {"status": "no text found"}

    if not is_reminder_message(text):
        send_whatsapp_message(phone,
            f"👋 *Hey there!*\n━━━━━━━━━━━━━━━━━━━━\nI'm your *WhatsApp Reminder Bot* 🤖\n\n"
            f"I can only set reminders for you!\n\n*Try saying:*\n"
            f"• _Remind me to drink water at 5pm_\n"
            f"• _Call me to remind about meeting tomorrow at 9am_\n"
            f"• _Mujhe yaad dilao ke 8 baje medicine leni hai_\n"
            f"• _Kal subah 9 baje meeting remind karna_\n━━━━━━━━━━━━━━━━━━━━")
        return {"status": "non-reminder message"}

    try:
        parsed        = parse_reminder(text)
        task          = parsed.get("task")
        remind_at     = datetime.fromisoformat(parsed.get("datetime"))
        reminder_type = parsed.get("reminder_type", "message")
        now_pk        = datetime.now(pk_tz).replace(tzinfo=None)

        if remind_at < now_pk:
            send_whatsapp_message(phone,
                f"⚠️ *Oops! That time has already passed.*\n━━━━━━━━━━━━━━━━━━━━\n"
                f"📌 *Task:* {task}\n"
                f"🕐 *You entered:* {remind_at.strftime('%I:%M %p, %A %B %d')}\n"
                f"🕐 *Current time:* {now_pk.strftime('%I:%M %p, %A %B %d')}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n_Please set a reminder for a future time._ 🤖")
            return {"status": "past time"}

        schedule_reminder(phone, task, remind_at, reminder_type)

        notify_via  = "📞 Phone Call" if reminder_type == "call" else "📲 WhatsApp Message"
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
        return {"status": "reminder set", "details": parsed}

    except Exception as e:
        print(f"❌ Error: {e}")
        send_whatsapp_message(phone,
            "❌ *Could not process your reminder.*\n\n━━━━━━━━━━━━━━━━━━━━\n"
            "Please try again like this:\n\n"
            "• _Remind me to call John at 5pm tomorrow_\n"
            "• _Remind me to take medicine at 8am today_\n"
            "• _Mujhe yaad dilao ke kal 9 baje meeting hai_\n━━━━━━━━━━━━━━━━━━━━")
        return {"status": "error", "message": str(e)}

# ── List Reminders ──
@app.get("/reminders")
def list_reminders():
    return {"reminders": get_all_reminders()}