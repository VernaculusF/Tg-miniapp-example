# Telegram Mini App - Clicker Game

A simple Telegram bot with a Web App clicker game. Users earn coins by clicking, see a leaderboard, and view stats.

Demo (Web App): https://vernaculusf.github.io/Tg-miniapp-example/
Repository: https://github.com/VernaculusF/Tg-miniapp-example
            
## Features
- Web App inside Telegram
- User profiles and stats
- Click-to-earn coins
- Top 10 leaderboard
- Withdraw flow

## Tech Stack
Backend: Python, Flask, python-telegram-bot
Frontend: HTML, CSS, Vanilla JavaScript, Telegram Web App API

## Project Structure
```
Tg-miniapp-example/
├── backend/
│   ├── app.py
│   ├── bot.py
│   ├── .env
│   └── requirements.txt
├── index.html
├── script.js
├── style.css
├── README.md
├── LICENSE
└── .env.example
```

## Setup

### 1) Create a Telegram Bot
1. Open Telegram and message @BotFather
2. Use /newbot
3. Copy the bot token

### 2) Install Backend Dependencies
```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3) Configure Environment
Create backend/.env:
```
BOT_TOKEN=YOUR_BOT_TOKEN
FRONTEND_URL=https://vernaculusf.github.io/Tg-miniapp-example/
```

### 4) Run Backend, HTTPS Tunnel, and Bot (Working Setup)
This app needs an HTTPS API when the Web App is opened inside Telegram.

Terminal 1 (API):
```
cd backend
python app.py
```

Terminal 2 (HTTPS tunnel for API):
```
cloudflared tunnel --url http://localhost:5000
```
Copy the HTTPS URL from cloudflared, for example:
```
https://your-random.trycloudflare.com
```

Update backend/.env so the bot opens the Web App with API param:
```
FRONTEND_URL=https://vernaculusf.github.io/Tg-miniapp-example/?api=https://your-random.trycloudflare.com/api
```

Terminal 3 (Bot):
```
cd backend
python bot.py
```

## Bot Commands
- /start
- /help
- /stats
- /leaderboard
- /withdraw

## API Endpoints
- POST /api/user
- POST /api/click
- POST /api/withdraw
- POST /api/stats
- GET  /api/leaderboard
- GET  /health

## Notes
- Telegram requires HTTPS for Web App buttons and HTTPS for API calls.
- If you host the frontend elsewhere, update FRONTEND_URL in backend/.env.
- If you see 409 Conflict, you have more than one bot instance running.
- Cloudflare Tunnel often fails when VPN is on. Turn VPN off before starting the tunnel.

## License
MIT License. See LICENSE.
