import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("GREEN_API_URL", "https://7103.api.greenapi.com")
INSTANCE_ID = os.getenv("GREEN_API_ID")
TOKEN = os.getenv("GREEN_API_TOKEN")

def send_whatsapp_message(phone_number: str, message: str) -> bool:
    url = f"{BASE_URL}/waInstance{INSTANCE_ID}/sendMessage/{TOKEN}"
    clean_number = phone_number.replace("+", "").replace(" ", "")
    chat_id = f"{clean_number}@c.us"
    payload = {"chatId": chat_id, "message": message}
    print(f"📤 Sending to: {chat_id}")
    response = requests.post(url, json=payload)
    print(f"📤 Response: {response.status_code} - {response.text}")
    return response.status_code == 200

def receive_webhook(data: dict) -> dict:
    print(f"🔑 Keys: {list(data.keys())}")
    message_type = data.get("typeWebhook", "")
    print(f"📥 Type: {message_type}")
    if message_type in ("incomingMessageReceived", "outgoingMessageReceived"):
        phone = data.get("senderData", {}).get("sender", "").replace("@c.us", "")
        content = data.get("messageData", {})
        print(f"📥 Phone: {phone}, Content: {content}")
        if content.get("typeMessage") == "textMessage":
            text = content.get("textMessageData", {}).get("textMessage", "")
            return {"phone": phone, "text": text, "type": "text"}
        elif content.get("typeMessage") == "audioMessage":
            audio_url = content.get("fileMessageData", {}).get("downloadUrl", "")
            return {"phone": phone, "audio_url": audio_url, "type": "voice"}
    print(f"⚠️ Ignoring: {message_type}")
    return {}