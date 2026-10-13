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

echo [2/3] Starting Local Studio Server on port 8088...
start "" http://localhost:8088/

echo [3/3] Server is live! Press Ctrl+C in this window to stop.
echo.
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8088
pause
