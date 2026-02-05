@echo off
echo ===========================================
echo Tour Website Automation - Quick Start
echo ===========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.9+
    exit /b 1
)

echo Step 1: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Installing Playwright browsers...
playwright install chromium

echo.
echo Step 3: Initializing config...
python main.py init

echo.
echo ===========================================
echo Setup complete!
echo.
echo To run the automation:
echo   python main.py full --limit 3
echo.
echo For help:
echo   python main.py --help
echo ===========================================
pause
