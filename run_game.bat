@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"
echo ==================================================
echo  Starting Family Feud+ (Flutter UI + Python Core)
echo ==================================================

if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXEC=.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXEC=python"
)

echo [1/2] Launching Python headless backend on ws://127.0.0.1:8765...
start "Family Feud Core Engine" /B %PYTHON_EXEC% backend\server.py

where flutter >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Flutter SDK was not found on PATH.
    echo Please install Flutter from: https://docs.flutter.dev/get-started/install/windows
    echo.
    pause
    exit /b 1
)

echo [2/2] Launching Flutter Frontend (Windows Desktop)...
cd flutter_frontend

if not exist "windows\" (
    echo Generating native Windows runner files...
    flutter create --platforms=windows .
)

flutter run -d windows %*
