@echo off
cd /d "%~dp0"

echo Building book...
python build.py

if errorlevel 1 (
    echo.
    echo Build failed. Check the error above.
    pause
    exit /b 1
)

echo.
echo Starting local book website...
start "" http://localhost:8000
python -m http.server 8000