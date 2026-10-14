@echo off
title FX Learning Agent - Web Studio
echo ======================================================
echo    Starting FX Learning Studio (Moodle Course Creator)
echo ======================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH!
    echo Please download and install Python from https://www.python.org/downloads/
    echo Be sure to check 'Add Python to PATH' during installation.
    pause
    exit /b
)

REM Check if Ollama is running
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Ollama is not installed!
    echo For free local AI, download Ollama from https://ollama.com
    echo (You can still run the app and use Cloud keys if you prefer).
    echo.
)

REM Navigate to backend and install requirements if needed
echo [1/3] Checking dependencies...
python -m pip install -q -r backend\requirements.txt >nul 2>&1

REM Resolve free port (fallback if default 8088 is busy)
set PORT=8088
for /f "delims=" %%p in ('python -c "import socket; [print(i) or exit() for i in range(8088, 8100) if socket.socket().connect_ex(('127.0.0.1', i)) != 0]"') do set PORT=%%p

echo [2/3] Starting Local Studio Server on port %PORT%...
start "" http://localhost:%PORT%/

echo [3/3] Server is live on http://localhost:%PORT%/! Press Ctrl+C in this window to stop.
echo.
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port %PORT% --reload
pause
