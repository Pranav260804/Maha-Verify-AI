@echo off
REM Maha Verify AI - Quick Start Script for Windows

echo.
echo 🔧 Maha Verify AI - Setup
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    exit /b 1
)

echo ✓ Python detected

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install -q -r requirements.txt

REM Create directories
if not exist "uploads" mkdir uploads

REM Setup .env file
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env
        echo ⚠️ Created .env file - Please configure API keys!
    )
)

echo.
echo ✓ Setup complete!
echo.
echo To start the server, run:
echo   python quickstart.py
echo.
pause
