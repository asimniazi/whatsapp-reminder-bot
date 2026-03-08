# 🔔 WhatsApp Reminder Bot

> AI-powered personal reminder assistant — set reminders via WhatsApp or dashboard in English & Urdu.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

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

## 📸 Screenshots

### Image 1
<img width="1916" height="908" alt="image" src="https://github.com/user-attachments/assets/ad982376-1343-4020-918f-fb755a93a0a2" />

### Image 2
<img width="1916" height="910" alt="image" src="https://github.com/user-attachments/assets/38afd917-aefd-44ca-8f7a-8b1dc1c0e220" />

### Image 3
<img width="1909" height="979" alt="image" src="https://github.com/user-attachments/assets/d25e2657-cf56-4031-9197-cf7bba65b5d4" />

### Image 4
<img width="485" height="442" alt="image" src="https://github.com/user-attachments/assets/bb614223-d27c-49db-8bb2-869845417a19" />


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
