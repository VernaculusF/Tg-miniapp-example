# Telegram Mini App - Clicker Game 🎮

A simple yet powerful **Telegram Bot** with integrated **Web App** for a clicker game. Users can earn coins by clicking, compete on leaderboards, and withdraw their earnings - all within Telegram!

**Demo:** [@YourBotName](https://t.me/YourBotName)

## Features ✨

- 🎮 **Web App Integration** - Play the game directly in Telegram
- 👤 **User Management** - Persistent user profiles and statistics
- 💰 **Coin System** - Earn 10 coins per click
- 🏆 **Leaderboard** - Real-time rankings of top players
- 💸 **Withdrawal System** - Withdraw earned coins (0% fee)
- 📊 **Statistics** - View your progress and achievements
- ⚡ **Responsive Design** - Works on mobile and desktop
- 🔄 **Real-time Updates** - Live balance and leaderboard updates

## Tech Stack 🛠️

### Backend
- **Python 3.8+**
- **Flask** - Web API server
- **python-telegram-bot** - Telegram Bot API wrapper
- **Flask-CORS** - Cross-origin resource sharing
- **python-dotenv** - Environment configuration

### Frontend
- **HTML5** - Markup
- **CSS3** - Responsive styling
- **Vanilla JavaScript** - No dependencies
- **Telegram Web App API** - Bot integration

## Project Structure 📁

```
telegram-mini-app/
├── backend/
│   ├── app.py              # Flask API server
│   ├── bot.py              # Telegram bot with Web App
│   ├── .env                # Configuration (create this)
│   ├── requirements.txt     # Python dependencies
│   └── __init__.py          # Package marker
├── frontend/
│   ├── index.html          # Web App HTML
│   ├── style.css           # Styling
│   ├── script.js           # Application logic
├── README.md               # This file
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
└── .env.example            # Example configuration
```

## Installation 🚀

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- A Telegram account
- ngrok (for HTTPS tunnel during development)

### Step 1: Create Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Use `/newbot` command to create new bot
3. Copy the **Bot Token** (you'll need this)
4. Copy your **bot username** (like @MyBot)

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/telegram-mini-app.git
cd telegram-mini-app
```

### Step 3: Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create `.env` file in `backend/` directory:

```env
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
FRONTEND_URL=https://your-https-url.com
```

**Important:** Get HTTPS URL using ngrok:

```bash
# Download from https://ngrok.com/download
# And run:
./ngrok http 8000

# Copy the HTTPS URL from ngrok output
# Example: https://abc123-xyz.ngrok.io
```

### Step 5: Start Services

**Terminal 1 - Flask API:**
```bash
cd backend
python app.py
# Should show: "Starting Flask API server on http://localhost:5000"
```

**Terminal 2 - Bot:**
```bash
cd backend
python bot.py
# Should show: "Bot configured and ready!"
```

**Terminal 3 - Frontend:**
```bash
cd frontend
python -m http.server 8000
# Should show: "Serving HTTP on :: port 8000"
```

### Step 6: Test in Telegram

1. Open Telegram
2. Find your bot: `@YourBotName`
3. Send `/start`
4. Tap **"🎮 Play Game"** button
5. Start clicking to earn coins!

## API Endpoints 🔌

All endpoints expect JSON and return JSON.

### `/api/user` (POST)
Get or create user profile.

**Request:**
```json
{
  "user_id": 123456789,
  "first_name": "John",
  "username": "john_doe"
}
```

**Response:**
```json
{
  "user_id": 123456789,
  "first_name": "John",
  "username": "john_doe",
  "balance": 0,
  "clicks": 0,
  "created_at": "2024-01-01T12:00:00"
}
```

### `/api/click` (POST)
Register a click and award coins.

**Request:**
```json
{
  "user_id": 123456789
}
```

**Response:**
```json
{
  "success": true,
  "clicks": 1,
  "balance": 10
}
```

### `/api/withdraw` (POST)
Withdraw coins from balance.

**Request:**
```json
{
  "user_id": 123456789,
  "amount": 100
}
```

**Response:**
```json
{
  "success": true,
  "message": "Withdrawal of 100 coins completed",
  "balance": 900
}
```

### `/api/stats` (POST)
Get user statistics.

**Request:**
```json
{
  "user_id": 123456789
}
```

**Response:**
```json
{
  "user_id": 123456789,
  "first_name": "John",
  "username": "john_doe",
  "total_clicks": 150,
  "current_balance": 1500,
  "created_at": "2024-01-01T12:00:00"
}
```

### `/api/leaderboard` (GET)
Get top 10 players by balance.

**Response:**
```json
{
  "leaderboard": [
    {
      "user_id": 123456789,
      "first_name": "John",
      "username": "john_doe",
      "balance": 5000,
      "clicks": 500,
      "created_at": "2024-01-01T12:00:00"
    },
    ...
  ]
}
```

## Bot Commands 🤖

| Command | Description |
|---------|-------------|
| `/start` | Open the Web App |
| `/help` | Show game instructions |
| `/stats` | View your statistics |
| `/leaderboard` | See top 10 players |
| `/withdraw` | Learn about withdrawals |

## Configuration 🔧

Edit `.env` file to customize:

```env
# Telegram Bot Token (required)
BOT_TOKEN=your_token_here

# Frontend URL (must be HTTPS for Web App)
# For development use ngrok: https://abc123.ngrok.io
# For production use your domain: https://yourdomain.com
FRONTEND_URL=https://your-https-url.com
```

## Deployment 📡

### Option 1: Heroku (Recommended)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set BOT_TOKEN=your_token
heroku config:set FRONTEND_URL=https://your-app-name.herokuapp.com

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option 2: Railway

```bash
# Install Railway CLI
# https://docs.railway.app/cli/install

# Login and deploy
railway login
railway init
railway up
```

### Option 3: Render

1. Connect your GitHub repository
2. Create new Web Service
3. Set environment variables
4. Deploy

## Development Tips 💡

### Local Testing with HTTPS
Use ngrok to create secure tunnel:

```bash
ngrok http 8000
```

Update `.env`:
```env
FRONTEND_URL=https://your-ngrok-url.ngrok.io
```

### Database Migration
Replace in-memory storage with a real database:

```python
# In app.py, replace users_data dict with:
from sqlalchemy import create_engine
# ... use SQLAlchemy models
```

### Mobile Testing
Telegram Web App works best on mobile. Test using:

1. **Android:** Telegram app > Bot > Web App
2. **iOS:** Telegram app > Bot > Web App
3. **Desktop:** Telegram Desktop app (supports Web App)

## Contributing 🤝

We welcome contributions! Please:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License 📄

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

## Support 💬

- 📧 **Email:** support@example.com
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/yourusername/telegram-mini-app/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/yourusername/telegram-mini-app/discussions)
- 📚 **Documentation:** [Telegram Bot API](https://core.telegram.org/bots)
- 🎮 **Telegram Web App Docs:** [Web App API](https://core.telegram.org/bots/webapps)

## Roadmap 🗺️

- [ ] Database support (PostgreSQL/MongoDB)
- [ ] Payment integration (Stripe/TON)
- [ ] Power-ups system
- [ ] Multiplayer mode
- [ ] Mobile app version
- [ ] Analytics dashboard
- [ ] Multi-language support

## Security Notes ⚠️

- This is a demo project. In production:
  - Use proper database (PostgreSQL, MongoDB, etc.)
  - Implement authentication/authorization
  - Add rate limiting
  - Use HTTPS everywhere
  - Validate all inputs
  - Implement CSRF protection
  - Use secure session management

## Acknowledgments 🙏

- [python-telegram-bot](https://python-telegram-bot.org/) library
- [Flask](https://flask.palletsprojects.com/) framework
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Web Apps](https://core.telegram.org/bots/webapps)

## Changelog 📝

### v1.0.0 (2024-01-XX)
- Initial release
- Web App integration
- Clicker game mechanics
- Leaderboard system
- Basic withdrawal system

---

Made with ❤️ for the Telegram Bot API

**Questions?** Start a [Discussion](https://github.com/yourusername/telegram-mini-app/discussions)!
