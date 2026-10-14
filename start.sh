#!/usr/bin/env bash
set -e

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$repo_root"

echo "======================================================"
echo "   Starting FX Learning Studio (Moodle Course Creator)"
echo "======================================================"
echo ""

# 1. Check Python
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3 is not installed or not in your PATH!"
    echo "Please install Python 3 from https://www.python.org/downloads/ or via Homebrew (brew install python)."
    exit 1
fi

# 2. Check Ollama (Informational)
if ! command -v ollama &>/dev/null && [ ! -d "/Applications/Ollama.app" ]; then
    echo "[INFO] Ollama is not detected on this machine."
    echo "For free local AI, download Ollama from https://ollama.com or run 'brew install ollama'."
    echo "(You can still run the app and use Cloud AI accounts if you prefer)."
    echo ""
fi

# 3. Check dependencies
echo "[1/3] Checking dependencies..."
python3 -m pip install -q -r backend/requirements.txt 2>/dev/null || true

# 4. Resolve free port (fallback if default is busy)
DESIRED_PORT="${PORT:-8088}"
PORT=$(python3 -m backend.app.find_port "$DESIRED_PORT")

if [ "$PORT" != "$DESIRED_PORT" ]; then
    echo "[INFO] Port $DESIRED_PORT was busy; automatically switched to available port $PORT."
fi

HOST="${HOST:-0.0.0.0}"

echo "[2/3] Launching Web Studio in browser..."
URL="http://localhost:${PORT}/"
if command -v open &>/dev/null; then
    (sleep 1 && open "$URL") &
elif command -v xdg-open &>/dev/null; then
    (sleep 1 && xdg-open "$URL") &
fi

echo "[3/3] Server is live on http://localhost:${PORT}/ (Press Ctrl+C to stop)"
echo ""
python3 -m uvicorn backend.app.main:app --host "$HOST" --port "$PORT" --reload
