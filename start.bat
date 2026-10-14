@echo off
setlocal enabledelayedexpansion
title FX Learning Studio - AI Moodle Course Generator

REM 1. Set current working directory to the folder containing start.bat
cd /d "%~dp0"

echo ======================================================
echo    Starting FX Learning Studio (Moodle Course Creator)
echo ======================================================
echo.

REM 2. Detect Python (try 'python', then 'py -3', then 'py')
set "PYTHON_CMD="
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
) else (
    py -3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=py -3"
    ) else (
        py --version >nul 2>&1
        if %errorlevel% equ 0 (
            set "PYTHON_CMD=py"
        )
    )
)

if "%PYTHON_CMD%"=="" (
    echo [ERROR] Python is not installed or not in your Windows PATH!
    echo.
    echo Please install Python 3.10+ from:
    echo https://www.python.org/downloads/
    echo.
    echo CRITICAL: During installation, check the box:
    echo   [x] Add python.exe to PATH
    echo.
    pause
    exit /b 1
)

REM 3. Check for Ollama on Windows
set "OLLAMA_FOUND=0"
where ollama >nul 2>&1
if %errorlevel% equ 0 set "OLLAMA_FOUND=1"
if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" set "OLLAMA_FOUND=1"
if exist "%ProgramFiles%\Ollama\ollama.exe" set "OLLAMA_FOUND=1"

if "%OLLAMA_FOUND%"=="0" (
    echo [NOTICE] Ollama is not detected on this system.
    echo For free private local AI, install Ollama from: https://ollama.com/download/windows
    echo (You can also connect Cloud accounts for Claude/ChatGPT/Gemini inside the app)
    echo.
)

REM 4. Check dependencies (fast startup if already installed)
echo [1/3] Checking dependencies...
%PYTHON_CMD% -c "import fastapi, uvicorn, httpx, pydantic" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing backend dependencies...
    %PYTHON_CMD% -m pip install -r backend\requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install requirements. Check your internet connection.
        pause
        exit /b 1
    )
)

REM 5. Resolve free port (defaults to 8088, scans next if occupied)
set "PORT=8088"
for /f "delims=" %%p in ('%PYTHON_CMD% -m backend.app.find_port 8088') do set "PORT=%%p"

if not "%PORT%"=="8088" (
    echo [INFO] Port 8088 was busy; automatically switched to available port %PORT%.
)

REM 6. Launch browser
echo [2/3] Launching Web Studio in browser...
start "" "http://localhost:%PORT%/"

REM 7. Start Uvicorn Server
echo [3/3] Server is live on http://localhost:%PORT%/
echo Press Ctrl+C in this command window to stop.
echo.
%PYTHON_CMD% -m uvicorn backend.app.main:app --host 0.0.0.0 --port %PORT% --reload

if %errorlevel% neq 0 (
    echo.
    echo Server stopped with error code %errorlevel%.
    pause
)
