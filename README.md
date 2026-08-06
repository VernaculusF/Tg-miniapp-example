# Telegram Mini App Clicker

An example Telegram Mini App with a clicker frontend, a Flask API, and a Telegram bot. It demonstrates opening a Web App from a bot and sending requests from the frontend to the API.

## Features

- Open the Mini App from a Telegram bot.
- Award coins for clicks.
- Store user statistics in process memory.
- Display a leaderboard and process coin deductions.
- Provide bot commands for viewing statistics.

## Stack

- HTML, CSS, and JavaScript
- Telegram Web App API
- Python and Flask
- python-telegram-bot

## Quick start

Create a bot with BotFather, then prepare the backend environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
```

Set `BOT_TOKEN` and the HTTPS frontend address in `backend/.env`, then start the API:

```bash
python app.py
```

Telegram requires HTTPS for both the Web App and API. Deploy both services with HTTPS and set the frontend URL with the API query parameter:

```dotenv
FRONTEND_URL=https://example.com/?api=https://api.example.com/api
```

Start the bot in a separate process:

```bash
cd backend
python bot.py
```

The demonstration frontend is available at `https://vernaculusf.github.io/Tg-miniapp-example/`.

## Project structure

```text
.
├── index.html          # Mini App markup
├── style.css           # Frontend styles
├── script.js           # Clicker logic and API requests
├── backend/
│   ├── app.py          # Flask API
│   ├── bot.py          # Telegram bot
│   └── requirements.txt
└── .env.example        # Configuration example
```

The API stores data in memory, so all state is reset when the process restarts.

## License

MIT
