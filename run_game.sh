#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=================================================="
echo " Starting Family Feud+ (Flutter UI + Python Core)"
echo "=================================================="

# 1. Start Python backend
if [ -f ".venv/bin/python" ]; then
    PYTHON_EXEC=".venv/bin/python"
else
    PYTHON_EXEC="python3"
fi

echo "[1/2] Starting headless Python backend on port 8765..."
$PYTHON_EXEC backend/server.py &
BACKEND_PID=$!

cleanup() {
    echo "Shutting down Python backend (PID $BACKEND_PID)..."
    kill "$BACKEND_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Give server time to bind port
sleep 1

# 2. Check Flutter SDK
if ! command -v flutter &> /dev/null; then
    echo ""
    echo "⚠️  Flutter SDK was not found on your PATH."
    echo "To install Flutter on macOS using Homebrew, run:"
    echo "   brew install --cask flutter"
    echo "Or visit: https://docs.flutter.dev/get-started/install/macos"
    echo ""
    echo "Backend is running in the background. Press Ctrl+C to exit."
    wait "$BACKEND_PID"
    exit 1
fi

echo "[2/2] Launching Flutter Operator Console..."
cd flutter_frontend

# Generate native macOS/Windows runner folders if missing
if [ ! -d "macos" ] && [ ! -d "windows" ]; then
    echo "Generating platform runner files..."
    flutter create --platforms=macos,windows .
fi

flutter run -d macos "$@"
