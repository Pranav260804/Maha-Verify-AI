@echo off
REM Maha Verify AI - Quick Setup for Windows (Python 3.13+)
REM This script sets up the project with pre-built wheels only (no compilation)

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  Maha Verify AI - Windows Setup (Pre-built Wheels Only)
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found. Download from python.org
    echo   https://www.python.org/downloads/windows/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVERSION=%%i
echo ✓ Python %PYVERSION% detected

REM Create virtual environment
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment activated

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --quiet --upgrade pip wheel setuptools
if errorlevel 1 (
    echo ⚠️  WARNING: pip upgrade had issues, continuing anyway...
)

REM Install dependencies with wheels-only mode
echo.
echo Installing dependencies (wheels only - no compilation)...
python -m pip install --quiet --only-binary :all: -r requirements-wheels-only.txt
if errorlevel 1 (
    echo ⚠️  WARNING: Some packages may have warnings, continuing...
    echo   This is usually safe
)

REM Create required directories
if not exist "uploads" mkdir uploads
echo ✓ Directories created

REM Setup .env file
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ✓ Created .env file
        echo.
        echo ⚠️  IMPORTANT: Edit .env with your API keys:
        echo   - GOOGLE_CLIENT_ID/SECRET
        echo   - OPENAI_API_KEY
        echo   - CAPTCHA_API_KEY
        echo.
        echo   Open .env in your editor to configure
    )
) else (
    echo ✓ .env file exists
)

echo.
echo ============================================================
echo  ✅ Setup Complete!
echo ============================================================
echo.
echo To start the server, run:
echo   python quickstart.py
echo.
echo Or manually start:
echo   uvicorn backend.main:app --reload --port 8000
echo.
echo Then visit: http://localhost:8000
echo.
pause
