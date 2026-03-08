# whatsapp-reminder-bot
AI-powered WhatsApp reminder bot — set reminders via WhatsApp or dashboard in English &amp; Urdu. Built with FastAPI, Groq, Green API &amp; VAPI.

# 🔔 WhatsApp Reminder Bot

> AI-powered personal reminder assistant — set reminders via WhatsApp or dashboard in English & Urdu.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

<img width="485" height="442" alt="image" src="https://github.com/user-attachments/assets/b7c80b29-0f13-4fd8-bbb6-12a6aa6ea684" />
<img width="1916" height="908" alt="image" src="https://github.com/user-attachments/assets/c5ea5508-523d-4ce6-8cb2-e1325dfbbfef" />
<img width="1909" height="979" alt="image" src="https://github.com/user-attachments/assets/a00e226f-f609-4167-886e-9a19b4fabdcb" />

---

## ✨ Features

- 💬 **Natural Language** — Set reminders in English or Urdu/Roman Urdu
- 📲 **WhatsApp Integration** — Receive reminders directly on WhatsApp
- 📞 **Voice Call Reminders** — Get called when it's time (via VAPI)
- 📧 **Email Notifications** — Gmail confirmation & reminder emails
- 🌐 **Beautiful Dashboard** — Light/Dark mode HTML/CSS/JS frontend
- 🤖 **AI Powered** — Groq LLaMA 3.3 parses your reminder intent
- 🇵🇰 **Multilingual** — English, Urdu, Roman Urdu all supported

---

## 🖥️ Dashboard Preview

| Light Mode | Dark Mode |
|------------|-----------|
| Clean white UI with purple accents | Sleek dark theme |

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| AI / NLP | Groq — LLaMA 3.3 70B |
| WhatsApp | Green API |
| Voice Calls | VAPI |
| Scheduler | APScheduler |
| Frontend | HTML / CSS / JS |
| Deployment | Oracle Cloud (Free Tier) |

---

## 📁 Project Structure

```
whatsapp-reminder-bot/
├── app/
│   ├── main.py               # FastAPI app + all routes
│   ├── reminder_parser.py    # AI reminder parsing (Groq)
│   ├── whatsapp_handler.py   # Green API integration
│   ├── scheduler.py          # APScheduler jobs
│   ├── vapi_handler.py       # VAPI voice call
│   └── email_handler.py      # Gmail notifications
├── static/
│   ├── index.html            # Dashboard UI
│   ├── style.css             # Styling + dark/light mode
│   └── app.js                # Frontend logic
├── .env.example              # Environment variables template
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/asimniazi100/whatsapp-reminder-bot.git
cd whatsapp-reminder-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
```
Fill in your `.env` file (see below).

### 4. Run the server
```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Open dashboard
```
http://localhost:8000/dashboard
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
# Groq AI
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

# Green API (WhatsApp)
GREEN_API_ID=your_instance_id
GREEN_API_TOKEN=your_instance_token
GREEN_API_URL=https://xxxx.api.greenapi.com
GREEN_API_MEDIA_URL=https://xxxx.media.greenapi.com

# VAPI (Voice Calls)
VAPI_API_KEY=your_vapi_api_key
VAPI_ASSISTANT_ID=your_assistant_id
VAPI_PHONE_NUMBER_ID=your_phone_number_id

# Your WhatsApp Number
YOUR_PHONE_NUMBER=+923001234567

# Email Notifications
EMAIL_SENDER=your.email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=receiver@gmail.com
```

> ⚠️ Never commit your `.env` file — it's already in `.gitignore`

---

## 🚀 How to Use

### Via WhatsApp:
Send any of these to your bot number:

**English:**
```
Remind me to drink water at 5pm
Remind me to call John tomorrow at 9am
Call me to remind about meeting at 3pm
```

**Urdu / Roman Urdu:**
```
Mujhe yaad dilao ke 8 baje medicine leni hai
Kal subah 9 baje meeting remind karna
Aaj raat 10 baje paani peena yaad dilana
```

### Via Dashboard:
Open `http://your-server/dashboard` and fill the form.

---

## 🌐 Deployment (Oracle Cloud Free Tier)

```bash
# On Oracle VM
sudo apt update && sudo apt install python3-pip nginx -y
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Configure Nginx as reverse proxy and open port 8000 in Oracle security rules.

---

## 📜 License

MIT License — feel free to use and modify.

---

## 👨‍💻 Author

**Asim Niazi**  
Built with ❤️ using FastAPI · Groq · Green API · VAPI
