"""
Telegram Mini App Bot
Complete bot with Web App integration for the clicker game
"""

import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, BotCommand
from telegram.ext import (
    Application, CommandHandler, ContextTypes, 
    MessageHandler, filters, CallbackQueryHandler
)

load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8000')

# Store user sessions
user_sessions = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command - Show Web App button."""
    user = update.effective_user
    if not user:
        return
    
    welcome_text = (
        f"Welcome {user.first_name or 'User'}! 🎮\n\n"
        "Tap the button below to play the clicker game and earn coins!\n\n"
        "Earn 10 coins per click and compete on the leaderboard."
    )
    
    # Create keyboard with Web App button
    # NOTE: Web App requires HTTPS URL (use ngrok or deploy to production)
    keyboard = [
        [InlineKeyboardButton("🎮 Play Game", web_app=WebAppInfo(url=FRONTEND_URL))],
        [
            InlineKeyboardButton("❓ Help", callback_data="help"),
            InlineKeyboardButton("📊 Stats", callback_data="stats")
        ],
        [
            InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard"),
            InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command - Show game instructions."""
    help_text = (
        "🎮 **Game Instructions**\n\n"
        "**How to Play:**\n"
        "1. Tap the 'Play Game' button to open the mini app\n"
        "2. Click the button as many times as you can\n"
        "3. Earn 10 coins per click\n"
        "4. Build your balance and compete with others\n"
        "5. Withdraw your earnings anytime\n\n"
        "**Bot Commands:**\n"
        "/start - Open the game\n"
        "/help - This message\n"
        "/stats - Your statistics\n"
        "/leaderboard - Top 10 players\n"
        "/withdraw - Learn about withdrawals"
    )
    
    if update.message:
        await update.message.reply_text(help_text)
    elif update.callback_query:
        await update.callback_query.edit_message_text(help_text)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command - Show user statistics."""
    user = update.effective_user
    if not user:
        return
    
    stats_text = (
        f"📊 **Your Statistics**\n\n"
        f"**Profile:**\n"
        f"Name: {user.first_name or 'User'}\n"
        f"ID: {user.id}\n"
        f"Type: {'Premium' if user.is_premium else 'Regular'}\n\n"
        f"**Game Stats:**\n"
        f"Open the game to see your:\n"
        f"• Total clicks\n"
        f"• Current balance\n"
        f"• Ranking position\n\n"
        f"Tap 'Play Game' button to view detailed stats!"
    )
    
    if update.message:
        await update.message.reply_text(stats_text)
    elif update.callback_query:
        await update.callback_query.edit_message_text(stats_text)


async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /leaderboard command - Show top players."""
    leaderboard_text = (
        "🏆 **Leaderboard**\n\n"
        "**Top 10 Players by Balance:**\n\n"
        "Open the game to see the complete leaderboard with:\n"
        "• Player ranks\n"
        "• Total coins earned\n"
        "• Number of clicks\n\n"
        "**How to climb the rankings:**\n"
        "1. Click regularly to earn coins\n"
        "2. Don't withdraw too much - keep your balance high\n"
        "3. Play consistently to stay competitive\n\n"
        "Tap 'Play Game' to see live rankings!"
    )
    
    if update.message:
        await update.message.reply_text(leaderboard_text)
    elif update.callback_query:
        await update.callback_query.edit_message_text(leaderboard_text)


async def withdraw_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /withdraw command - Information about withdrawals."""
    withdraw_text = (
        "💸 **Withdraw Earnings**\n\n"
        "**How to Withdraw:**\n"
        "1. Open the game by tapping 'Play Game'\n"
        "2. Click the 'Withdraw' button\n"
        "3. Choose the amount (multiple of 100)\n"
        "4. Confirm the withdrawal\n\n"
        "**Withdrawal Details:**\n"
        "• Minimum withdrawal: 100 coins\n"
        "• Fee: 0% (instant withdrawal)\n"
        "• Processing time: Instant\n\n"
        "**Available Methods:**\n"
        "• Bank card\n"
        "• Mobile payment\n"
        "• Crypto wallet (TON)\n\n"
        "Start playing to earn coins!"
    )
    
    if update.message:
        await update.message.reply_text(withdraw_text)
    elif update.callback_query:
        await update.callback_query.edit_message_text(withdraw_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle any text message not matching commands."""
    user = update.effective_user
    if not user or not update.message:
        return
    
    response = (
        f"Hi {user.first_name or 'User'}!\n\n"
        "I'm your clicker game bot. Available commands:\n\n"
        "/start - Play the game\n"
        "/help - Game instructions\n"
        "/stats - Your statistics\n"
        "/leaderboard - Top players\n"
        "/withdraw - Withdrawal info\n\n"
        "Tap the 'Play Game' button to start earning coins!"
    )
    
    await update.message.reply_text(response)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button clicks."""
    query = update.callback_query
    if not query:
        return
    
    await query.answer()
    
    # Route to appropriate handler based on callback data
    if query.data == "help":
        await help_command(update, context)
    elif query.data == "stats":
        await stats_command(update, context)
    elif query.data == "leaderboard":
        await leaderboard_command(update, context)
    elif query.data == "withdraw":
        await withdraw_command(update, context)


async def post_init(application: Application) -> None:
    """Initialize bot after startup."""
    commands = [
        BotCommand("start", "Play the game"),
        BotCommand("help", "Game instructions"),
        BotCommand("stats", "Your statistics"),
        BotCommand("leaderboard", "Top 10 players"),
        BotCommand("withdraw", "Withdrawal info"),
    ]
    await application.bot.set_my_commands(commands)
    print("[OK] Bot commands registered")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)


def main():
    """Main bot startup function."""
    if not BOT_TOKEN:
        print("[ERROR] BOT_TOKEN not set in .env file!")
        print("Please add your Telegram bot token to the .env file")
        return
    
    print("=" * 50)
    print("[BOT] Starting Telegram Mini App Bot...")
    print(f"[BOT] Token: {BOT_TOKEN[:20]}...")
    print(f"[BOT] Web App URL: {FRONTEND_URL}")
    print("=" * 50)
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("leaderboard", leaderboard_command))
    app.add_handler(CommandHandler("withdraw", withdraw_command))
    
    # Register message handler for text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Register callback handler for button clicks
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Set post init callback
    app.post_init = post_init
    
    # Add error handler
    app.add_error_handler(error_handler)
    
    print("[OK] Bot configured and ready!")
    print("[BOT] Polling for updates from Telegram...")
    print("=" * 50)
    print("\nBot is running. Press Ctrl+C to stop.\n")
    
    # Start polling
    app.run_polling()


if __name__ == '__main__':
    main()
