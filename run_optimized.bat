@echo off
REM Optimized Streamlit startup script
REM Mengurangi browser warnings dan error messages

echo 🎬 Starting SocialCount Streamlit App...
echo ⚙️ Optimizing environment...

REM Set environment variables untuk mengurangi warnings
set PYTHONWARNINGS=ignore
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
set STREAMLIT_SERVER_HEADLESS=true
set STREAMLIT_GLOBAL_LOG_LEVEL=warning

REM Disable Chrome/Chromium warnings
set CHROME_LOG_FILE=NUL
set CHROMIUM_FLAGS=--disable-logging --disable-gpu-sandbox --no-sandbox --disable-dev-shm-usage

echo ✅ Environment optimized
echo 🌐 Starting Streamlit server...
echo.
echo 📱 Access your app at: http://localhost:8501
echo 🛑 Press Ctrl+C to stop
echo.

streamlit run app.py --server.headless=true --browser.gatherUsageStats=false --global.logLevel=warning
