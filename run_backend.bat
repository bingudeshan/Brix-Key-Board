@echo off
echo Starting Brix Keyboard AI Translation Service...
cd /d "%~dp0"
if exist ..\.venv\Scripts\python.exe (
    ..\.venv\Scripts\python.exe main.py
) else (
    python main.py
)
pause
