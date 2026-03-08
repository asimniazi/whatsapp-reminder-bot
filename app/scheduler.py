from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.whatsapp_handler import send_whatsapp_message

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_reminder(phone: str, message: str, remind_at: datetime, reminder_type: str = "message"):
    job_id = f"reminder_{phone}_{remind_at.timestamp()}"
    
    if reminder_type == "message":
        reminder_msg = (
            f"⏰ *Time for your reminder!*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 *Task:* {message}\n"
            f"🕐 *Scheduled:* {remind_at.strftime('%I:%M %p')}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"_Your WhatsApp Reminder Bot_ 🤖"
        )
        scheduler.add_job(
            send_whatsapp_message,
            trigger="date",
            run_date=remind_at,
            args=[phone, reminder_msg],
            id=job_id
        )

    elif reminder_type == "call":
        from app.vapi_handler import make_reminder_call
        scheduler.add_job(
            make_reminder_call,
            trigger="date",
            run_date=remind_at,
            args=[phone, message],
            id=job_id
        )
        print(f"📞 Call reminder scheduled for {remind_at}")
    
    print(f"✅ Reminder scheduled for {remind_at} via {reminder_type}")
    return job_id

def get_all_reminders():
    jobs = scheduler.get_jobs()
    return [{"id": job.id, "next_run": str(job.next_run_time)} for job in jobs]