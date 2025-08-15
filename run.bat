@echo off
REM SocialCount - Windows Batch Script
REM Quick launcher for SocialCount application

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    📊 SocialCount Launcher                    ║
echo ║              Social Media Analytics with AI                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if requirements are installed
if not exist "venv" (
    echo 🔧 Setting up virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Check if .env exists
if not exist ".env" (
    if exist ".env.example" (
        echo ⚙️ Creating environment file...
        copy ".env.example" ".env"
    )
)

REM Menu
:menu
echo.
echo 🚀 Choose an option:
echo    1. Launch Web Interface (Recommended)
echo    2. Run CLI Interface
echo    3. Check System Status
echo    4. Run Setup
echo    5. Exit
echo.
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" goto web
if "%choice%"=="2" goto cli
if "%choice%"=="3" goto status
if "%choice%"=="4" goto setup
if "%choice%"=="5" goto exit

echo Invalid choice. Please try again.
goto menu

:web
echo.
echo 🌐 Launching Web Interface...
echo    Opening browser at http://localhost:8501
echo    Press Ctrl+C to stop the server
echo.
python main.py --web
goto menu

:cli
echo.
echo 💻 CLI Interface
echo    Enter URLs to analyze or type 'menu' to return
echo.
python main.py
goto menu

:status
echo.
echo 🔍 Checking System Status...
python main.py --check
echo.
pause
goto menu

:setup
echo.
echo 🔧 Running Setup...
python setup.py
echo.
pause
goto menu

:exit
echo.
echo 👋 Thank you for using SocialCount!
echo.
pause
exit /b 0