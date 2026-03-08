import os
import json
import pytz
from groq import Groq
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
pk_tz = pytz.timezone('Asia/Karachi')

def is_reminder_message(user_message: str) -> bool:
    prompt = f"""
    Determine if this message is a reminder request or not.
    Message: "{user_message}"
    
    Return ONLY "yes" if it's a reminder request, or "no" if it's casual conversation, greeting, or anything else.
    Examples of reminders: "remind me to...", "set a reminder for...", "don't let me forget...", "mujhe yaad dilao", "yaad karna", "reminder lagao"
    Examples of non-reminders: "hello", "how are you", "what can you do", "thanks", "assalam o alaikum"
    
    Return ONLY yes or no, nothing else.
    """
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    result = response.choices[0].message.content.strip().lower()
    print(f"🤔 Is reminder: {result}")
    return result == "yes"

def parse_reminder(user_message: str) -> dict:
    now_pk = datetime.now(pk_tz)
    
    prompt = f"""
    You are a multilingual reminder parsing assistant. You understand English, Urdu, and Roman Urdu.
    Extract reminder details from the user's message regardless of language.
    
    User message: "{user_message}"
    
    Examples of valid messages:
    - "Remind me to call John at 5pm"
    - "Mujhe yaad dilao ke 8 baje medicine leni hai"
    - "Kal subah 9 baje meeting hai mujhe remind karna"
    - "Aaj raat 10 baje paani peena yaad dilana"
    - "Call me to remind about meeting tomorrow at 9am"
    - "Call kar k remind karna kal 5 baje"
    
    Return ONLY a valid JSON object with these fields:
    - task: what to be reminded about in English (always translate to English)
    - datetime: when to remind in ISO format YYYY-MM-DDTHH:MM:SS (string)
    - reminder_type: "message" or "call" (string)
    - phone_number: extract if mentioned, else null
    
    Today's date and time is: {now_pk.strftime('%Y-%m-%d %H:%M:%S')} (Pakistan Standard Time)
    
    If user says "call me" or "call karo" or "phone karo" use reminder_type "call", otherwise use "message".
    Return ONLY the JSON, no explanation.
    """
    
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(raw)
    return parsed