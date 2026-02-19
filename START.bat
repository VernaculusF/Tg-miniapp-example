@echo off
REM Telegram Mini App - Complete Startup Script
REM This script starts all necessary components with ngrok tunnel

echo.
echo ============================================================
echo  Telegram Mini App - Complete Setup
echo  Clicker Game with Web App Integration
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Setup backend
echo [SETUP] Installing Python dependencies...
cd backend
python -m venv venv >nul 2>&1
call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1
cd ..

echo.
echo ============================================================
echo  1. NGROK SETUP (For HTTPS Web App)
echo ============================================================
echo.
echo To use the Web App button, you need HTTPS URL.
echo.
echo Option A - Use ngrok (Recommended for development):
echo   1. Download ngrok: https://ngrok.com/download
echo   2. Extract ngrok.exe to your project folder
echo   3. Run ngrok: ngrok http 8000
echo   4. Copy the HTTPS URL from ngrok output
echo   5. Update backend\.env with FRONTIER_URL=your_ngrok_url
echo.
echo Option B - Use production domain:
echo   1. Deploy to Heroku, Railway, or Render
echo   2. Use your domain in backend\.env
echo.
pause

echo.
echo ============================================================
echo  2. CONFIGURATION
echo ============================================================
echo.

if not exist "backend\.env" (
    echo [SETUP] Creating .env file...
    type backend\.env.example > backend\.env
    echo [INFO] Please edit backend\.env with your settings:
    echo   - BOT_TOKEN: Get from @BotFather on Telegram
    echo   - FRONTEND_URL: HTTPS URL (ngrok or your domain)
    echo.
    echo   File location: backend\.env
    echo.
    pause
) else (
    echo [OK] Configuration file exists
)

echo.
echo ============================================================
echo  3. START SERVICES
echo ============================================================
echo.

echo [STARTING] Flask API on port 5000...
start "Flask API" cmd /k "cd backend && venv\Scripts\activate.bat && python app.py"

timeout /t 2 /nobreak

echo [STARTING] Frontend Server on port 8000...
start "Frontend" cmd /k "cd frontend && python -m http.server 8000"

timeout /t 2 /nobreak

echo [STARTING] Telegram Bot...
start "Telegram Bot" cmd /k "cd backend && venv\Scripts\activate.bat && python bot.py"

timeout /t 2 /nobreak

echo.
echo ============================================================
echo  STARTUP COMPLETE!
echo ============================================================
echo.
echo Services:
echo  - Flask API:      http://localhost:5000
echo  - Frontend:       http://localhost:8000
echo  - Telegram Bot:   Running (polling mode)
echo.
echo Next Steps:
echo  1. Open Telegram and find your bot
echo  2. Send /start command
echo  3. Tap "Play Game" button to open the Web App
echo.
echo Troubleshooting:
echo  - If Web App button doesn't work:
echo    -> Make sure FRONTEND_URL is HTTPS (use ngrok)
echo    -> Restart the bot after updating .env
echo.
echo  - If bot doesn't respond:
echo    -> Check BOT_TOKEN is correct in .env
echo    -> Check internet connection
echo    -> Press Ctrl+C to stop, fix issue, run this script again
echo.
echo Documentation: See README.md for detailed information
echo.
echo ============================================================
echo.

pause
