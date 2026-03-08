import os
import requests
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")
VAPI_PHONE_NUMBER_ID = os.getenv("VAPI_PHONE_NUMBER_ID")

def make_reminder_call(phone_number: str, task: str) -> bool:
    url = "https://api.vapi.ai/call"
    
    clean_number = phone_number.replace("+", "").replace(" ", "")
    if not clean_number.startswith("92"):
        clean_number = f"92{clean_number}"
    formatted_number = f"+{clean_number}"
    
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "assistantId": VAPI_ASSISTANT_ID,
        "phoneNumberId": VAPI_PHONE_NUMBER_ID,
        "customer": {
            "number": formatted_number
        },
        "assistantOverrides": {
            "firstMessage": f"Hello! This is your WhatsApp Reminder Bot. You asked me to remind you to {task}. Have a productive day!"
        }
    }
    
    print(f"📞 Making call to {formatted_number} for task: {task}")
    response = requests.post(url, json=payload, headers=headers)
    print(f"📞 VAPI Response: {response.status_code} - {response.text}")
    
    if response.status_code in (200, 201):
        print(f"✅ Call initiated to {formatted_number}")
        return True
    else:
        print(f"❌ Call failed: {response.text}")
        return False